#!/usr/bin/env python3
"""Tests for the kit renderer.

WHY THIS EXISTS. `kit.py` is the last check a skill or a subagent passes
before every machine installs it. A skill whose name breaks one app's rule
loads nowhere and says nothing, a subagent written wrong for one app
silently goes missing there, and a file that names a private repository
publishes it. These tests hold each source to those rules, and the rendered
forms to what each app parses.

Run it:

    python3 .github/scripts/test_kit.py
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import shutil
import sys
import tempfile
import unittest

try:
    import tomllib
except ImportError:  # Python before 3.11, where only the TOML test is skipped
    tomllib = None

HERE = pathlib.Path(__file__).resolve().parent


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name while the class is built.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


kit = load('kit', 'kit.py')

SKILL = ('---\nname: processing-invoices\ndescription: Extracts line items from invoices. '
         'Use when the user has invoices to read.\n---\n\n# Processing invoices\n')
AGENT = ('---\nname: reviewer\ndescription: Reviews a change. Use after a change.\ntools: read, search, execute\n'
         '---\n\nYou review. Quote "this" and a \\ backslash.\n')


class Hub(unittest.TestCase):
    """A throwaway hub holding one skill, one subagent and a guard."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='kit-test-'))
        self.write('kit/guard.py', f'# {kit.OWNED}\nprint("guard")\n')
        self.write('kit/skills/processing-invoices/SKILL.md', SKILL)
        self.write('kit/skills/processing-invoices/references/forms.md', 'Forms.\n')
        self.write('kit/subagents/reviewer.md', AGENT)
        self.write('kit/subagents/README.md', 'The folder log, which is not an agent.\n')

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel: str, text: str) -> pathlib.Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def problems(self) -> list[str]:
        return kit.problems(self.root)

    def assertProblem(self, fragment: str) -> None:
        found = self.problems()
        self.assertTrue(any(fragment in line for line in found), f'no problem mentions {fragment!r}: {found}')


class TestSound(Hub):
    def test_a_sound_hub_has_no_problems(self) -> None:
        self.assertEqual(self.problems(), [])

    def test_the_bundle_is_deterministic_json(self) -> None:
        first = kit.render_kit(self.root)
        self.assertEqual(first, kit.render_kit(self.root))
        data = json.loads(first)
        self.assertEqual(sorted(data), ['//', 'format', 'guard', 'skills', 'subagents'])
        self.assertEqual(data['format'], 2, 'the format without the knowledge facts')
        self.assertEqual(sorted(data['skills']['processing-invoices']), ['SKILL.md', 'references/forms.md'])
        self.assertEqual(list(data['subagents']), ['reviewer'], 'the README is not an agent')


class TestSkills(Hub):
    """Each skill meets the strictest rule any app enforces."""

    def test_the_folder_name(self) -> None:
        for bad in ('Processing-Invoices', 'processing--invoices', '-invoices', 'claude-helper', 'synced'):
            with self.subTest(name=bad):
                self.write(f'kit/skills/{bad}/SKILL.md', SKILL.replace('processing-invoices', bad))
                self.assertTrue(any(f'kit/skills/{bad}' in line for line in self.problems()))
                shutil.rmtree(self.root / 'kit' / 'skills' / bad)

    def test_the_name_matches_the_folder(self) -> None:
        self.write('kit/skills/processing-invoices/SKILL.md', SKILL.replace('name: processing-invoices', 'name: other'))
        self.assertProblem('name must equal the folder name')

    def test_frontmatter_opens_the_file_and_holds_only_portable_keys(self) -> None:
        self.write('kit/skills/processing-invoices/SKILL.md', '# Title\n' + SKILL)
        self.assertProblem('must open with ---')
        self.write('kit/skills/processing-invoices/SKILL.md', SKILL.replace('---\n\n#', 'argument-hint: x\n---\n\n#'))
        self.assertProblem('not argument-hint')

    def test_the_description_triggers(self) -> None:
        cases = {
            SKILL.replace(' Use when the user has invoices to read.', ''): 'with "Use when"',
            SKILL.replace('Extracts', 'Extracts <xml>'): 'angle brackets',
            SKILL.replace('Extracts line items from invoices.', 'x' * 1100): 'limit 1024',
            SKILL.replace('description: Extracts line items from invoices. Use when the user has invoices '
                          'to read.\n', ''): 'needs a description',
        }
        for text, fragment in cases.items():
            with self.subTest(fragment=fragment):
                self.write('kit/skills/processing-invoices/SKILL.md', text)
                self.assertProblem(fragment)

    def test_the_body_and_its_references_stay_small_and_shallow(self) -> None:
        self.write('kit/skills/processing-invoices/SKILL.md', SKILL + 'line\n' * 501)
        self.assertProblem('over 500 lines')
        self.write('kit/skills/processing-invoices/SKILL.md', SKILL)
        self.write('kit/skills/processing-invoices/references/deep/nested.md', 'Too deep.\n')
        self.assertProblem('one level below SKILL.md')

    def test_a_folder_without_skill_md(self) -> None:
        self.write('kit/skills/empty-skill/notes.md', 'No skill here.\n')
        self.assertProblem('has no SKILL.md')


class TestSubagents(Hub):
    """Each subagent renders for every app that reads one."""

    def forms(self) -> dict[str, str]:
        return json.loads(kit.render_kit(self.root))['subagents']['reviewer']

    def test_claude_code_gets_its_own_tool_names(self) -> None:
        claude = self.forms()['claude']
        fields, body = kit.frontmatter(claude)
        self.assertEqual(fields['name'], 'reviewer')
        self.assertEqual(fields['tools'], 'Read, Grep, Glob, Bash')
        self.assertIn(kit.OWNED, claude)
        self.assertTrue(body.startswith('You review.'))

    def test_copilot_gets_its_aliases(self) -> None:
        fields, _ = kit.frontmatter(self.forms()['copilot'])
        self.assertEqual(json.loads(fields['tools']), ['read', 'search', 'execute'])

    @unittest.skipIf(tomllib is None, 'tomllib arrived in Python 3.11')
    def test_codex_gets_toml_with_the_prompt_intact(self) -> None:
        data = tomllib.loads(self.forms()['codex'])
        self.assertEqual(sorted(data), ['description', 'developer_instructions', 'name'])
        self.assertEqual(data['developer_instructions'], 'You review. Quote "this" and a \\ backslash.\n')

    def test_a_subagent_breaking_the_format_is_refused(self) -> None:
        cases = {
            AGENT.replace('name: reviewer', 'name: Reviewer'): 'name must equal the file name',
            AGENT.replace('tools: read, search, execute', 'tools: read, teleport'): 'unknown tools teleport',
            AGENT.replace('tools:', 'model: opus\ntools:'): 'not model',
            AGENT.replace('description: Reviews a change. Use after a change.\n', ''): 'needs a description',
        }
        for text, fragment in cases.items():
            with self.subTest(fragment=fragment):
                self.write('kit/subagents/reviewer.md', text)
                self.assertProblem(fragment)


class TestEveryFile(Hub):
    """What holds for every file the kit carries, whatever its source."""

    def test_a_private_repository_is_never_named(self) -> None:
        forms = 'kit/skills/processing-invoices/references/forms.md'
        self.write(forms, 'The secrets live in tannergolden/vault.\n')
        self.assertProblem('tannergolden/vault')
        self.write(forms, 'The rules live in tannergolden/intelligence.\n')
        self.assertEqual(self.problems(), [])

    def test_no_dash_the_standards_ban_reaches_any_file(self) -> None:
        self.write('kit/skills/processing-invoices/references/forms.md', 'Forms \u2014 all of them.\n')
        self.assertProblem('en or em dash')

    def test_a_guard_without_the_kits_mark_is_refused(self) -> None:
        self.write('kit/guard.py', 'print("guard")\n')
        self.assertProblem('must carry the line')


class TestTheRealKit(unittest.TestCase):
    """The modules in this repository."""

    root = HERE.parents[1]

    def test_they_break_no_rule(self) -> None:
        self.assertEqual(kit.problems(self.root), [])

    def test_the_skills_are_develop_and_the_faculties_the_pin_records(self) -> None:
        # The hub writes one skill (ADR-0021) and carries the faculties it has pinned (ADR-0033); no other.
        bundle, _ = kit.bundle(self.root)
        pin = json.loads((self.root / 'kit' / 'faculties.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(bundle['skills']), sorted(['develop', *pin['skills']]))
        self.assertEqual(sorted(bundle['subagents']), ['reviewer', 'worker'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
