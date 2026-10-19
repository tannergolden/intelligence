#!/usr/bin/env python3
"""Tests for the develop skill's validator and packager.

WHY THIS EXISTS. `skills/develop/scripts/validate.py` is Gate 1 for every
skill and agent the develop skill builds, in every repository the home kit
reaches, and `package.py` builds the archive a person uploads to the Claude
app. A check that passes a broken skill ships it everywhere; an archive that
drops the team or changes its bytes on every rebuild cannot be trusted. The
tests live here, beside the hub's other tests, so they never ship inside the
skill.

Nothing here writes outside a temporary folder.

Run it:

    python3 scripts/test_develop.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import shutil
import sys
import tempfile
import unittest
import zipfile

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1] / 'skills' / 'develop'
SCRIPTS = SKILL_DIR / 'scripts'
sys.dont_write_bytecode = True  # keep the skill folder free of caches


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name, and package.py imports validate by name.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate = load('validate')
package = load('package')

STAR = '\u2605 '

SKILL = """---
name: sample
description: Does a sample thing. Use when the user asks for a sample, even if they never say sample.
license: MIT
metadata: {"team": "Crew", "version": "01.00.00"}
---

# Sample

Body.

## Boundaries

- Stay within samples.
"""

CHANGELOG = '# sample Changelog\n\n## Current Version\n\n**`01.00.00`**\n'

AGENT = """---
title: "{title}"
name: "{name}"
description: "Dispatch this agent to {job}."
tools: read, search
---

# {title}

## Identity
- **Name:** {name}
- **Persona:** A tester.
- **Voice:** Plain.
- **Global rules:** follow `crew.md`.

## Role & Objective
Do it.

## Inputs
The brief.

## Method
1. Do it.

## Output contract
A line.

## Examples
One.

## Boundaries
Only this.

## Recovery
Flag it.

## Non-negotiables
- Do it right.
"""

ROSTER = """---
title: "Crew"
description: "Dispatch this team to test."
members: ["{star}Crew Lead", "Crew Member"]
lead: "{star}Crew Lead"
---

# Crew
"""


class Fixture(unittest.TestCase):
    """A throwaway skill and an agent home holding its team."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='develop-test-'))
        self.skill = self.root / 'sample'
        self.home = self.root / 'agents-home'
        self.write('sample/SKILL.md', SKILL)
        self.write('sample/License.txt', 'MIT License\n')
        self.write('sample/Changelog.md', CHANGELOG)
        for folder in validate.SKILL_FOLDERS:
            self.write(f'sample/{folder}/notes.md', 'Notes.\n')
        self.write('agents-home/crew/crew.md', ROSTER.format(star=STAR))
        self.write('agents-home/crew/crew-lead.md', AGENT.format(title=STAR + 'Crew Lead', name='Ada', job='lead'))
        self.write('agents-home/crew/crew-member.md', AGENT.format(title='Crew Member', name='Ben', job='work'))

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel: str, text: str) -> pathlib.Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def edit(self, rel: str, old: str, new: str) -> None:
        path = self.root / rel
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding='utf-8')

    def skill_report(self, **kwargs: object):
        report = validate.Report()
        validate.check_skill(self.skill, [self.home], report, **kwargs)
        return report

    def assertError(self, fragment: str, report=None) -> None:
        report = report or self.skill_report()
        self.assertTrue(any(fragment in line for line in report.errors), report.errors)

    def run_cli(self, module, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                code = module.main(list(args))
            except SystemExit as error:
                code = int(error.code or 0)
        return code, out.getvalue()


class TestFrontmatter(unittest.TestCase):
    """The YAML subset skill and agent files are written in."""

    def parse(self, block: str) -> dict:
        return validate.parse_frontmatter(block)

    def test_plain_quoted_and_flow_values(self) -> None:
        fields = self.parse('name: a\ntitle: "Q: x"\nother: \'it\'\'s\'\n'
                            'members: ["A", B]\nmetadata: {"team": "T", version: "01.00.00"}')
        self.assertEqual(fields['name'], 'a')
        self.assertEqual(fields['title'], 'Q: x')
        self.assertEqual(fields['other'], "it's")
        self.assertEqual(fields['members'], ['A', 'B'])
        self.assertEqual(fields['metadata'], {'team': 'T', 'version': '01.00.00'})

    def test_folded_literal_list_and_nested_values(self) -> None:
        fields = self.parse('description: >-\n  One\n  two.\nbody: |\n  a\n  b\n'
                            'members:\n  - A\n  - "B"\nmetadata:\n  version: "02.00.00"\n  team: T')
        self.assertEqual(fields['description'], 'One two.')
        self.assertEqual(fields['body'], 'a\nb')
        self.assertEqual(fields['members'], ['A', 'B'])
        self.assertEqual(fields['metadata'], {'version': '02.00.00', 'team': 'T'})

    def test_a_flow_list_laid_out_over_lines(self) -> None:
        fields = self.parse("members:\n  [\n    'A',\n    'B',\n  ]\nlead: 'A'")
        self.assertEqual(fields['members'], ['A', 'B'])
        self.assertEqual(fields['lead'], 'A')

    def test_a_dashed_line_inside_a_value_does_not_close_it(self) -> None:
        block, body = validate.split_frontmatter('---\ndescription: a --- b\n---\nBody.\n')
        self.assertEqual(self.parse(block)['description'], 'a --- b')
        self.assertEqual(body, 'Body.\n')

    def test_broken_frontmatter_is_refused(self) -> None:
        for text in ('no fence\n', '---\nname: a\n'):
            with self.subTest(text=text), self.assertRaises(validate.FrontmatterError):
                validate.split_frontmatter(text)
        for block in ('  indented: x', 'not a key', 'a: 1\na: 2', 'm: [open'):
            with self.subTest(block=block), self.assertRaises(validate.FrontmatterError):
                self.parse(block)


class TestSkill(Fixture):
    """Every way a skill can break the format every app accepts."""

    def test_a_sound_skill_passes(self) -> None:
        report = self.skill_report()
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_develop_passes_its_own_gate(self) -> None:
        report = validate.Report()
        validate.check_skill(SKILL_DIR, [], report)
        self.assertEqual((report.errors, report.warnings), ([], []))
        self.assertEqual(report.checked, 7, 'the skill, its five agents and its roster')

    def test_a_missing_manifest(self) -> None:
        (self.skill / 'SKILL.md').unlink()
        self.assertError('has no SKILL.md at its root')

    def test_a_second_manifest(self) -> None:
        self.write('sample/templates/SKILL.md', SKILL)
        self.assertError('is a second SKILL.md')

    def test_an_unknown_key(self) -> None:
        self.edit('sample/SKILL.md', 'license: MIT', 'license: MIT\nversion: 1')
        self.assertError('frontmatter may hold only')

    def test_the_name_rules(self) -> None:
        for name, fragment in (('Sample', 'lowercase words'), ('other', 'equals the folder name'),
                               ('claude-sample', 'may not contain claude')):
            with self.subTest(name=name):
                self.setUp()
                self.edit('sample/SKILL.md', 'name: sample', f'name: {name}')
                self.assertError(fragment)

    def test_the_description_rules(self) -> None:
        for old, new, fragment in (('Use when', 'For when', 'with "Use when"'),
                                   ('a sample thing', 'a <sample> thing', 'angle brackets'),
                                   ('a sample thing', 'x' * 1100, 'limit 1024')):
            with self.subTest(fragment=fragment):
                self.setUp()
                self.edit('sample/SKILL.md', old, new)
                self.assertError(fragment)

    def test_a_licence_and_a_version_are_required(self) -> None:
        self.edit('sample/SKILL.md', 'license: MIT\n', '')
        self.assertError('needs a license')
        self.setUp()
        self.edit('sample/SKILL.md', 'metadata: {"team": "Crew", "version": "01.00.00"}', 'metadata: {"team": "Crew"}')
        self.assertError('metadata carries the version')

    def test_the_changelog_carries_the_same_version(self) -> None:
        self.edit('sample/Changelog.md', '01.00.00', '01.01.00')
        self.assertError('differs from metadata.version')
        self.edit('sample/Changelog.md', '## Current Version', '## Version')
        self.assertError('needs a "## Current Version" line')

    def test_required_files_and_folders(self) -> None:
        (self.skill / 'License.txt').unlink()
        shutil.rmtree(self.skill / 'assets')
        report = self.skill_report()
        self.assertError('needs License.txt', report)
        self.assertTrue(any('has no assets/ folder' in line for line in report.warnings), report.warnings)

    def test_files_sit_one_level_down(self) -> None:
        self.write('sample/templates/skill/t-SKILL.md', 'x\n')
        self.assertError('at most one folder below SKILL.md')

    def test_the_body_rules(self) -> None:
        self.edit('sample/SKILL.md', '## Boundaries', '## Limits')
        self.assertError('needs a ## Boundaries section')
        self.setUp()
        self.edit('sample/SKILL.md', 'Body.', 'Body.\n\n## Bootstrap\n\nHow it began.')
        self.assertError('belongs to develop alone')
        self.setUp()
        self.edit('sample/SKILL.md', 'Body.', 'Read C:\\skills\\x first.')
        self.assertError('forward slashes')

    def test_a_heading_inside_a_code_fence_does_not_count(self) -> None:
        self.edit('sample/SKILL.md', '## Boundaries', '```\n## Boundaries\n```')
        self.assertError('needs a ## Boundaries section')

    def test_dashes_fail_unless_allowed(self) -> None:
        self.write('sample/references/notes.md', 'One \u2014 two.\n')
        self.assertError('references/notes.md:1: holds an em dash')
        self.assertEqual(self.skill_report(allow_dash=True).errors, [])

    def test_the_team_must_resolve(self) -> None:
        report = validate.Report()
        validate.check_skill(self.skill, [], report)
        self.assertError('metadata.team names Crew', report)
        self.edit('sample/SKILL.md', '"team": "Crew"', '"team": "Nobody"')
        self.assertError('metadata.team names Nobody')

    def test_a_vendored_team_is_checked_too(self) -> None:
        shutil.copytree(self.home / 'crew', self.skill / 'agents')
        report = validate.Report()
        validate.check_skill(self.skill, [], report)
        self.assertEqual(report.errors, [])
        self.edit('sample/agents/crew-member.md', '## Method', '## Approach')
        self.assertError('is missing its Method section')

    def test_pre_approved_writes_only_warn(self) -> None:
        self.edit('sample/SKILL.md', 'license: MIT', 'license: MIT\nallowed-tools: Read, Bash')
        report = self.skill_report()
        self.assertEqual(report.errors, [])
        self.assertTrue(any('pre-approves' in line for line in report.warnings), report.warnings)


class TestAgentsAndTeams(Fixture):
    """Agent specs, rosters and whole libraries."""

    def agent_report(self, rel: str):
        report = validate.Report()
        validate.check_agent(self.root / rel, report)
        return report

    def library_report(self, *homes: pathlib.Path):
        report = validate.Report()
        validate.check_library(list(homes) or [self.home], report)
        return report

    def test_a_sound_library_passes(self) -> None:
        report = self.library_report()
        self.assertEqual((report.errors, report.warnings), ([], []))
        self.assertEqual(report.checked, 3)

    def test_both_file_names_are_accepted_and_others_are_not(self) -> None:
        (self.home / 'crew' / 'crew-member.md').rename(self.home / 'crew' / 'Crew Member.md')
        self.assertEqual(self.agent_report('agents-home/crew/Crew Member.md').errors, [])
        (self.home / 'crew' / 'Crew Member.md').rename(self.home / 'crew' / 'member.md')
        self.assertError('the file is named for its title', self.agent_report('agents-home/crew/member.md'))

    def test_an_agent_needs_its_sections_and_identity(self) -> None:
        self.edit('agents-home/crew/crew-member.md', '- **Voice:** Plain.\n', '')
        self.edit('agents-home/crew/crew-member.md', '## Recovery', '## Fallback')
        report = self.agent_report('agents-home/crew/crew-member.md')
        self.assertError('is missing its Recovery section', report)
        self.assertTrue(any('no **Voice:** line' in line for line in report.warnings), report.warnings)

    def test_unknown_tools_warn(self) -> None:
        self.edit('agents-home/crew/crew-member.md', 'tools: read, search', 'tools: read, teleport')
        report = self.agent_report('agents-home/crew/crew-member.md')
        self.assertEqual(report.errors, [])
        self.assertTrue(any('unknown tools teleport' in line for line in report.warnings), report.warnings)

    def test_the_roster_rules(self) -> None:
        for old, new, fragment in ((f'lead: "{STAR}Crew Lead"', 'lead: "Crew Member"', 'is marked with a star'),
                                   (f'lead: "{STAR}Crew Lead"', f'lead: "{STAR}Someone"', 'is not among its members'),
                                   ('"Crew Member"]', f'"{STAR}Crew Member"]', 'only the lead carries the star'),
                                   ('"Crew Member"]', '"Crew Member", "Ghost"]', 'lists Ghost')):
            with self.subTest(fragment=fragment):
                self.setUp()
                self.edit('agents-home/crew/crew.md', old, new)
                self.assertError(fragment, self.library_report())

    def test_titles_and_names_are_unique_across_homes(self) -> None:
        other = self.root / 'other-home'
        self.write('other-home/twin.md', AGENT.format(title='Crew Member', name='BEN', job='copy'))
        (other / 'twin.md').rename(other / 'crew-member.md')
        report = self.library_report(self.home, other)
        self.assertError('shares its title, Crew Member', report)
        self.assertError('shares its spoken name', report)


class TestPackage(Fixture):
    """The archive a person uploads to the Claude app."""

    def build(self, *extra: str) -> tuple[int, str, pathlib.Path]:
        out = self.root / 'out'
        code, text = self.run_cli(package, str(self.skill), '--agents', str(self.home), '--out', str(out), *extra)
        return code, text, out / 'sample.skill'

    def names(self, archive: pathlib.Path) -> list[str]:
        with zipfile.ZipFile(archive) as opened:
            return opened.namelist()

    def test_the_archive_holds_the_skill_and_its_vendored_team(self) -> None:
        code, text, archive = self.build()
        self.assertEqual(code, 0, text)
        names = self.names(archive)
        self.assertIn('sample/SKILL.md', names)
        self.assertEqual(sum(name.endswith('SKILL.md') for name in names), 1)
        self.assertEqual(sorted(n for n in names if '/agents/' in n),
                         ['sample/agents/crew-lead.md', 'sample/agents/crew-member.md', 'sample/agents/crew.md'])
        self.assertFalse((self.skill / 'agents').exists(), 'the source folder is never changed')

    def test_a_rebuild_is_byte_identical(self) -> None:
        _, _, first = self.build()
        before = first.read_bytes()
        _, _, second = self.build()
        self.assertEqual(second.read_bytes(), before)

    def test_caches_hidden_files_and_older_archives_stay_out(self) -> None:
        for rel in ('sample/.hidden.md', 'sample/assets/__pycache__/x.pyc', 'sample/old.skill', 'sample/.DS_Store'):
            self.write(rel, 'x')
        _, _, archive = self.build()
        names = self.names(archive)
        self.assertFalse([n for n in names if 'hidden' in n or 'pycache' in n or n.endswith('.skill')
                          or 'DS_Store' in n], names)

    def test_a_skill_with_errors_is_refused(self) -> None:
        self.edit('sample/SKILL.md', 'Use when', 'For when')
        code, text, archive = self.build()
        self.assertEqual(code, 1, text)
        self.assertIn('Use when', text)
        self.assertFalse(archive.exists())

    def test_a_team_that_cannot_be_found_is_refused(self) -> None:
        out = self.root / 'out'
        code, text = self.run_cli(package, str(self.skill), '--out', str(out))
        self.assertEqual(code, 1, text)
        self.assertIn('metadata.team names Crew', text)

    def test_a_dry_run_writes_nothing(self) -> None:
        code, text, archive = self.build('--dry-run')
        self.assertEqual(code, 0, text)
        self.assertIn('sample/agents/crew.md', text)
        self.assertFalse(archive.exists())

    def test_json_output(self) -> None:
        code, text, archive = self.build('--json')
        self.assertEqual(code, 0, text)
        data = json.loads(text)
        self.assertEqual(data['archive'], str(archive.resolve()))
        self.assertEqual(len(data['vendored']), 3)


class TestCommandLine(Fixture):
    """Exit codes and output a script or an agent can branch on."""

    def test_exit_codes_and_json(self) -> None:
        code, text = self.run_cli(validate, 'skill', str(self.skill), '--agents', str(self.home))
        self.assertEqual(code, 0, text)
        self.assertIn('0 errors', text)
        self.edit('sample/SKILL.md', 'Use when', 'For when')
        code, text = self.run_cli(validate, 'skill', str(self.skill), '--agents', str(self.home), '--json')
        self.assertEqual(code, 1, text)
        self.assertEqual(json.loads(text)['checked'], 1)
        code, _ = self.run_cli(validate, 'nonsense', 'x')
        self.assertEqual(code, 2)

    def test_team_and_library_commands(self) -> None:
        roster = str(self.home / 'crew' / 'crew.md')
        self.assertEqual(self.run_cli(validate, 'team', roster)[0], 0)
        self.assertEqual(self.run_cli(validate, 'library', str(self.home))[0], 0)
        self.assertEqual(self.run_cli(validate, 'agent', str(self.home / 'crew' / 'crew-member.md'))[0], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
