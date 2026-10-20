#!/usr/bin/env python3
"""Tests for the Constitution renderer.

WHY THIS EXISTS. `render.py` is the only writer of the block every agent
reads, in every repository and on every machine. A rule it drops, reorders
or mangles reaches all of them at the next release, and a hash it computes
differently breaks every audit and every installed copy. These pin its
exact output against a small Constitution written here, and hold the real
`CONSTITUTION.md` to its own Article VI.

Nothing here writes to the repository it ships in.

Run it:

    python3 scripts/test_render.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / 'render.py'
_spec = importlib.util.spec_from_file_location('render', SCRIPT)
render = importlib.util.module_from_spec(_spec)
# Dataclasses look their own module up by name while the class is built.
sys.modules[_spec.name] = render
_spec.loader.exec_module(render)

SPEC = {
    'heading': 'Constitution',
    'source': 'From CONSTITUTION.md, which gives the reasons.',
    'precedence': ['Invariants: follow every one.', 'Defaults: your user wins.'],
    'sections': {
        'Invariants': [('SEC-001', 'Never put a credential in a file.', ['gitleaks'], []),
                       ('OPS-001', 'Never force-push.', [], ['a guard hook'])],
        'Defaults': [('WORK-001', 'Change only what the task needs.', [], [])],
        'Owner-only Defaults': [('GIT-010', 'Name branches by intent.', ['semantic-pr.yml'], [])],
    },
    'target': '200 characters',
    'cap': '4000 characters',
    'retired': {'OPS-002': 'Left to CI.'},
}

EXPECTED = """## Constitution

From CONSTITUTION.md, which gives the reasons.

- Invariants: follow every one.
- Defaults: your user wins.

### Invariants

- SEC-001: Never put a credential in a file.
- OPS-001: Never force-push.

### Defaults

- WORK-001: Change only what the task needs.

### Owner-only Defaults

- GIT-010: Name branches by intent.
"""


def copy(spec: dict) -> dict:
    return json.loads(json.dumps(spec))


def markdown(spec: dict) -> str:
    """A CONSTITUTION.md laid out as Article VI describes, from a small spec."""
    lines = ['<!--', "title: 'Constitution'", '-->', '', '# Constitution', '', '## What This Is', '',
             'Prose, ignored.', '', '---', '', '## Article I: Precedence', '', 'Quoted into the block:', '']
    lines += [f'> - {line}' for line in spec['precedence']]
    number = 1
    for title, rules in spec['sections'].items():
        number += 1
        lines += ['', '---', '', f'## Article {render.NUMERALS[number - 1]}: {title}', '', 'Prose, ignored.']
        for rid, text, today, add in rules:
            lines += ['', f'### {rid}', '', f'> {text}', '', '**Why.** Because.']
            for label, items in (('Enforced by:', today), ('To add:', add)):
                if items:
                    lines += ['', f'**{label}**', ''] + [f'- {item}' for item in items]
    number += 1
    lines += ['', '---', '', f'## Article {render.NUMERALS[number - 1]}: The Block', '',
              f"- **Heading:** {spec['heading']}"]
    if spec.get('source'):
        lines.append(f"- **Source:** {spec['source']}")
    lines += [f"- **Target:** {spec['target']}", f"- **Cap:** {spec['cap']}", '',
              '---', '', '## Appendix: Retired Rules', '', '| ID | Where it went |', '| :- | :- |']
    lines += [f'| {rid} | {where} |' for rid, where in spec['retired'].items()]
    return '\n'.join(lines + ['', '---', '', 'Footer.', ''])


class Hub:
    """A throwaway copy of the hub's layout with the small Constitution above."""

    def __init__(self, spec: dict | None = None) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='render-test-'))
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts' / 'install.py').write_text('# installer\n', encoding='utf-8')
        self.write(spec or SPEC)

    def ship_kit(self) -> None:
        """Give this hub the guard, so it renders the kit too."""
        (self.root / 'scripts' / 'guard.py').write_text(f'# {render.kit.OWNED}\n', encoding='utf-8')

    def write(self, spec: dict) -> None:
        self.write_text(markdown(spec))

    def write_text(self, text: str) -> None:
        (self.root / 'CONSTITUTION.md').write_text(text, encoding='utf-8')

    def text(self) -> str:
        return (self.root / 'CONSTITUTION.md').read_text(encoding='utf-8')

    def constitution(self):
        return render.load_constitution(self.root)

    def run(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = render.main(['--root', str(self.root), *args])
        return code, out.getvalue()

    def cleanup(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class HubTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = Hub()

    def tearDown(self) -> None:
        self.hub.cleanup()

    def with_rule(self, section: str, rule: tuple) -> None:
        spec = copy(SPEC)
        spec['sections'][section].append(list(rule))
        self.hub.write(spec)

    def assertProblem(self, fragment: str) -> None:
        found = render.problems(self.hub.constitution())
        self.assertTrue(any(fragment in line for line in found), found)


class TestRendering(HubTestCase):
    """The exact bytes of the block."""

    def test_the_block_renders_exactly(self) -> None:
        self.assertEqual(render.render_block(self.hub.constitution()), EXPECTED)

    def test_the_marker_carries_the_hash_of_the_block(self) -> None:
        block = render.render_block(self.hub.constitution())
        region = render.region(block)
        self.assertTrue(region.startswith(render.BEGIN.format(render.digest(block)) + '\n\n'))
        self.assertTrue(region.endswith('\n' + render.END + '\n'))
        found = render.find(region)
        self.assertEqual(found.inner, block)
        self.assertFalse(found.edited)

    def test_size_ignores_the_final_newline(self) -> None:
        self.assertEqual(render.size('abc\n'), 3)

    def test_a_block_with_no_source_line_starts_at_the_precedence(self) -> None:
        spec = copy(SPEC)
        spec['source'] = ''
        self.hub.write(spec)
        self.assertEqual(render.render_block(self.hub.constitution()),
                         EXPECTED.replace('From CONSTITUTION.md, which gives the reasons.\n\n', ''))


class TestReading(HubTestCase):
    """How the Markdown is read: what counts, and what is left out."""

    def test_every_part_is_read(self) -> None:
        constitution = self.hub.constitution()
        self.assertEqual(constitution.heading, 'Constitution')
        self.assertEqual(constitution.precedence, ('Invariants: follow every one.', 'Defaults: your user wins.'))
        self.assertEqual([s.title for s in constitution.sections], ['Invariants', 'Defaults', 'Owner-only Defaults'])
        self.assertEqual((constitution.target, constitution.cap), (200, 4000))
        self.assertEqual(constitution.retired, {'OPS-002': 'Left to CI.'})
        rule = constitution.rules['SEC-001']
        self.assertEqual((rule.kind, rule.reach, rule.why, rule.enforced_by), ('invariant', 'every', 'Because.',
                                                                               ('gitleaks',)))
        self.assertEqual(constitution.rules['GIT-010'].reach, 'owner')

    def test_a_wrapped_quote_and_list_item_are_joined(self) -> None:
        self.hub.write_text(self.hub.text().replace('> Never force-push.', '> Never\n> force-push.')
                            .replace('- a guard hook', '- a guard\n  hook'))
        rule = self.hub.constitution().rules['OPS-001']
        self.assertEqual((rule.text, rule.to_add), ('Never force-push.', ('a guard hook',)))

    def test_a_wrapped_why_is_joined(self) -> None:
        self.hub.write_text(self.hub.text().replace('**Why.** Because.\n\n**Enforced by:**',
                                                    '**Why.** Because\nit matters.\n\n**Enforced by:**', 1))
        self.assertEqual(self.hub.constitution().rules['SEC-001'].why, 'Because it matters.')

    def test_windows_line_endings_read_the_same(self) -> None:
        self.hub.write_text(self.hub.text().replace('\n', '\r\n'))
        self.assertEqual(render.render_block(self.hub.constitution()), EXPECTED)
        self.assertEqual(render.problems(self.hub.constitution()), [])

    def test_a_heading_inside_a_code_block_is_not_a_rule(self) -> None:
        self.hub.write_text(self.hub.text().replace('Prose, ignored.\n\n### OPS-001',
                                                    'Prose, ignored.\n\n```text\n### SEC-009\n> Not a rule.\n```'
                                                    '\n\n### OPS-001'))
        self.assertNotIn('SEC-009', self.hub.constitution().rules)
        self.assertEqual(render.problems(self.hub.constitution()), [])

    def test_a_budget_may_carry_thousands_separators(self) -> None:
        spec = copy(SPEC)
        spec['cap'] = '4,000 characters'
        self.hub.write(spec)
        self.assertEqual(self.hub.constitution().cap, 4000)

    def test_a_missing_part_stops_the_read(self) -> None:
        for old, new in (('## Article I: Precedence', '## Article I: Order'),
                         ('## Article III: Defaults', '## Article III: Suggestions'),
                         ('- **Cap:** 4000 characters', ''),
                         ('- **Target:** 200 characters', '- **Target:** about two hundred')):
            with self.subTest(old=old):
                self.hub.write_text(markdown(SPEC).replace(old, new))
                with self.assertRaises(render.ConstitutionError):
                    self.hub.constitution()

    def test_no_file_stops_the_read(self) -> None:
        (self.hub.root / 'CONSTITUTION.md').unlink()
        with self.assertRaises(render.ConstitutionError):
            self.hub.constitution()


class TestConstitutionRules(HubTestCase):
    """Every way the file can break its own Article VI, each caught with a sentence."""

    def test_the_small_constitution_is_sound(self) -> None:
        self.assertEqual(render.problems(self.hub.constitution()), [])

    def test_a_bad_id(self) -> None:
        self.with_rule('Defaults', ('sec-1', 'Do it.', [], []))
        self.assertProblem('not DOMAIN-NNN')

    def test_a_retired_id_is_never_reused(self) -> None:
        self.with_rule('Defaults', ('OPS-002', 'Do it.', [], []))
        self.assertProblem('retired')

    def test_an_id_appears_once(self) -> None:
        self.with_rule('Defaults', ('SEC-001', 'Do it.', [], []))
        self.assertProblem('SEC-001 appears 2 times')

    def test_a_rule_outside_an_article_of_the_block(self) -> None:
        self.hub.write_text(self.hub.text().replace('## Appendix: Retired Rules',
                                                    '### WORK-009\n\n> Stray.\n\n## Appendix: Retired Rules'))
        self.assertProblem('WORK-009 sits under')

    def test_articles_are_numbered_in_order(self) -> None:
        self.hub.write_text(self.hub.text().replace('## Article III: Defaults', '## Article VII: Defaults'))
        self.assertProblem('should be numbered III')

    def test_an_invariant_names_an_enforcer(self) -> None:
        self.with_rule('Invariants', ('SEC-009', 'Never do it.', [], []))
        self.assertProblem('names its enforcer')

    def test_hidden_and_non_ascii_characters_are_refused(self) -> None:
        for text in ('Never\u200b do it.', 'Never \u2014 do it.'):
            with self.subTest(text=repr(text)):
                self.with_rule('Defaults', ('WORK-009', text, [], []))
                self.assertProblem('printable ASCII')

    def test_a_rule_is_a_sentence(self) -> None:
        self.with_rule('Defaults', ('WORK-009', 'No period', [], []))
        self.assertProblem('ending in a period')

    def test_a_rule_is_short(self) -> None:
        self.with_rule('Defaults', ('WORK-009', 'A' * 300 + '.', [], []))
        self.assertProblem('(limit 300)')

    def test_a_rule_says_why(self) -> None:
        self.hub.write_text(self.hub.text().replace('**Why.** Because.\n\n**Enforced by:**', '**Enforced by:**', 1))
        self.assertProblem('say why')

    def test_a_rule_needs_its_quote(self) -> None:
        self.hub.write_text(self.hub.text().replace('> Never put a credential in a file.\n\n', '', 1))
        self.assertProblem('is a > quote right under the heading')

    def test_a_rule_quotes_once(self) -> None:
        self.hub.write_text(self.hub.text().replace('**Why.** Because.', '**Why.** Because.\n\n> Again.', 1))
        self.assertProblem('quotes more than once')

    def test_an_unknown_field(self) -> None:
        self.hub.write_text(self.hub.text().replace('**Why.** Because.', '**Why.** Because.\n\n**Owner:** me', 1))
        self.assertProblem('which is not **Why.**')

    def test_text_outside_the_fields(self) -> None:
        self.hub.write_text(self.hub.text().replace('- gitleaks', '- gitleaks\n\nA stray paragraph.', 1))
        self.assertProblem('text outside its quote and fields')

    def test_the_block_fits_its_cap(self) -> None:
        spec = copy(SPEC)
        spec['cap'] = '100 characters'
        self.hub.write(spec)
        self.assertProblem('over its cap of 100')


class TestRegions(unittest.TestCase):
    """Finding, checking and replacing the managed block inside a file."""

    block = '## Working rules\n\n- A: Do it.\n'

    def test_a_region_is_found_with_its_text(self) -> None:
        text = '# Title\n\n' + render.region(self.block) + '\n## Mine\n'
        found = render.find(text)
        self.assertEqual(found.inner, self.block)
        self.assertEqual(text[found.end:], '\n## Mine\n')

    def test_a_hand_edit_inside_the_markers_is_caught(self) -> None:
        text = render.region(self.block).replace('Do it.', 'Do it later.')
        self.assertTrue(render.find(text).edited)

    def test_blank_lines_around_the_block_do_not_count_as_an_edit(self) -> None:
        text = render.region(self.block).replace('\n\n## Working', '\n\n\n\n## Working')
        self.assertFalse(render.find(text).edited)

    def test_windows_line_endings_do_not_count_as_an_edit(self) -> None:
        text = render.region(self.block).replace('\n', '\r\n')
        self.assertFalse(render.find(text).edited)

    def test_replacing_keeps_everything_around_the_block(self) -> None:
        old = '# Title\n\n' + render.region('## Old\n') + '\n## Mine\n'
        new = render.replace(old, render.region(self.block))
        self.assertEqual(new, '# Title\n\n' + render.region(self.block) + '\n## Mine\n')

    def test_two_blocks_are_an_error(self) -> None:
        with self.assertRaises(ValueError):
            render.find(render.region(self.block) + render.region(self.block))

    def test_no_block_is_none(self) -> None:
        self.assertIsNone(render.find('# Just a file\n'))


class TestCommandLine(HubTestCase):
    """`--write` and `--check` against a throwaway hub."""

    def test_a_stale_copy_fails_the_check_until_written(self) -> None:
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('stale', out)
        code, out = self.hub.run('--write')
        self.assertEqual(code, 0, out)
        self.assertIn('wrote home/intelligence.md', out)
        code, out = self.hub.run('--check')
        self.assertEqual(code, 0, out)
        self.assertIn('over its target of 200', out)

    def test_the_hub_keeps_no_agents_file(self) -> None:
        self.hub.run('--write')
        self.assertFalse((self.hub.root / 'AGENTS.md').exists())

    def test_the_home_file_is_exactly_the_marked_block(self) -> None:
        self.hub.run('--write')
        home = (self.hub.root / 'home' / 'intelligence.md').read_text(encoding='utf-8')
        self.assertEqual(home, render.region(EXPECTED))

    def test_the_sums_cover_what_a_consumer_downloads(self) -> None:
        self.hub.run('--write')
        sums = (self.hub.root / 'home' / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
        self.assertEqual([line.split('  ')[1] for line in sums], ['home/intelligence.md', 'scripts/install.py'])

    def test_a_hub_with_the_modules_ships_and_pins_the_kit(self) -> None:
        self.hub.ship_kit()
        code, out = self.hub.run('--write')
        self.assertEqual(code, 0, out)
        kit_text = (self.hub.root / 'home' / 'kit.json').read_text(encoding='utf-8')
        sums = (self.hub.root / 'home' / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
        self.assertEqual([line.split('  ')[1] for line in sums],
                         ['home/intelligence.md', 'home/kit.json', 'scripts/install.py'])
        self.assertIn(f'{render.digest(kit_text)}  home/kit.json', sums)
        code, out = self.hub.run('--pins')
        self.assertIn(f'kit_sha256={render.digest(kit_text)}', out)
        code, out = self.hub.run('--check')
        self.assertEqual(code, 0, out)
        self.assertIn('kit: 0 skills, 0 subagents', out)

    def test_a_hub_without_the_modules_pins_no_kit(self) -> None:
        self.hub.run('--write')
        self.assertFalse((self.hub.root / 'home' / 'kit.json').exists())
        code, out = self.hub.run('--pins')
        self.assertEqual(code, 0, out)
        self.assertIn('kit_sha256=\n', out)

    def test_a_broken_module_stops_the_render(self) -> None:
        self.hub.ship_kit()
        (self.hub.root / 'scripts' / 'guard.py').write_text('# a guard without the mark\n', encoding='utf-8')
        code, out = self.hub.run('--write')
        self.assertEqual(code, 1, out)
        self.assertIn('must carry the line', out)

    def test_changing_the_installer_makes_the_sums_stale(self) -> None:
        self.hub.run('--write')
        (self.hub.root / 'scripts' / 'install.py').write_text('# changed\n', encoding='utf-8')
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('home/SHA256SUMS: stale', out)

    def test_a_hand_edit_to_the_home_file_fails_the_check(self) -> None:
        self.hub.run('--write')
        path = self.hub.root / 'home' / 'intelligence.md'
        path.write_text(path.read_text(encoding='utf-8').replace('Never force-push.', 'Rarely force-push.'),
                        encoding='utf-8')
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('home/intelligence.md: stale', out)

    def test_a_broken_constitution_stops_every_mode(self) -> None:
        self.hub.write_text(self.hub.text().replace('> Change only what the task needs.', '> No period'))
        for mode in ([], ['--write'], ['--check']):
            with self.subTest(mode=mode):
                code, out = self.hub.run(*mode)
                self.assertEqual(code, 1, out)
                self.assertIn('ending in a period', out)

    def test_pins_hash_what_a_consumer_downloads(self) -> None:
        self.hub.run('--write')
        code, out = self.hub.run('--pins')
        self.assertEqual(code, 0, out)
        home = (self.hub.root / 'home' / 'intelligence.md').read_text(encoding='utf-8')
        self.assertIn(f'home_sha256={render.digest(home)}', out)
        self.assertIn('version=unreleased', out)

    def test_pins_read_a_tag(self) -> None:
        self.hub.run('--write')
        git = ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', '-c', 'commit.gpgsign=false']
        for command in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'rules'], ['tag', 'v0.1.0']):
            subprocess.run(git + command, cwd=self.hub.root, check=True, capture_output=True)
        (self.hub.root / 'home' / 'intelligence.md').write_text('changed since the tag\n', encoding='utf-8')
        code, out = self.hub.run('--pins', 'v0.1.0')
        self.assertEqual(code, 0, out)
        self.assertIn('version=v0.1.0', out)
        self.assertIn(f'home_sha256={render.digest(render.region(EXPECTED))}', out)


class TestCloudSetup(HubTestCase):
    """`--setup` fills the cloud setup script with the pins of a release tag."""

    template = "VERSION='@VERSION@'\nHOME_SHA256='@HOME_SHA256@'\nINSTALL_SHA256='@INSTALL_SHA256@'\n"
    kit_template = template + "KIT_SHA256='@KIT_SHA256@'\n"

    def tag(self) -> None:
        git = ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', '-c', 'commit.gpgsign=false',
               '-c', 'tag.gpgsign=false']
        for command in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'rules'], ['tag', 'v0.1.0']):
            subprocess.run(git + command, cwd=self.hub.root, check=True, capture_output=True)

    def test_the_pins_come_from_the_tag(self) -> None:
        (self.hub.root / 'setup').mkdir()
        (self.hub.root / 'setup' / 'claude-cloud-setup.sh').write_text(self.template, encoding='utf-8')
        self.hub.run('--write')
        self.tag()
        code, out = self.hub.run('--setup', 'v0.1.0')
        self.assertEqual(code, 0, out)
        self.assertIn("VERSION='v0.1.0'", out)
        self.assertIn(f"HOME_SHA256='{render.digest(render.region(EXPECTED))}'", out)
        self.assertNotIn('@', out)

    def test_the_kit_pin_comes_from_the_tag_too(self) -> None:
        (self.hub.root / 'setup').mkdir()
        (self.hub.root / 'setup' / 'claude-cloud-setup.sh').write_text(self.kit_template, encoding='utf-8')
        self.hub.ship_kit()
        self.hub.run('--write')
        self.tag()
        code, out = self.hub.run('--setup', 'v0.1.0')
        self.assertEqual(code, 0, out)
        kit_text = (self.hub.root / 'home' / 'kit.json').read_text(encoding='utf-8')
        self.assertIn(f"KIT_SHA256='{render.digest(kit_text)}'", out)

    def test_a_template_without_its_placeholders_is_refused(self) -> None:
        (self.hub.root / 'setup').mkdir()
        (self.hub.root / 'setup' / 'claude-cloud-setup.sh').write_text("VERSION='v0.0.1'\n", encoding='utf-8')
        self.hub.run('--write')
        self.tag()
        with self.assertRaises(SystemExit):
            self.hub.run('--setup', 'v0.1.0')

    def test_the_real_template_has_every_placeholder(self) -> None:
        text = (SCRIPT.parents[1] / render.SETUP_FILE).read_text(encoding='utf-8')
        for name in ('VERSION', 'HOME_SHA256', 'INSTALL_SHA256', 'KIT_SHA256'):
            self.assertIn(f"{name}='@{name}@'", text)


class TestTheRealConstitution(unittest.TestCase):
    """The Constitution in this repository, and the copies rendered from it."""

    root = SCRIPT.parents[1]

    def test_it_breaks_no_rule_and_fits_its_cap(self) -> None:
        constitution = render.load_constitution(self.root)
        self.assertEqual(render.problems(constitution), [])
        self.assertLessEqual(render.size(render.render_block(constitution)), constitution.cap)

    def test_every_copy_is_current(self) -> None:
        self.assertEqual(render.stale(self.root, render.load_constitution(self.root)), [])

    def test_it_ships_the_kit(self) -> None:
        self.assertTrue(render.has_kit(self.root))
        self.assertIn(render.KIT_FILE, render.renderings(self.root, render.load_constitution(self.root)))

    def test_the_hub_keeps_no_agents_file(self) -> None:
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((self.root / 'law').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
