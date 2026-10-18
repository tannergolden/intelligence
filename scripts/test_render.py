#!/usr/bin/env python3
"""Tests for the law renderer.

WHY THIS EXISTS. `render.py` is the only writer of the block every agent
reads, in every repository and on every machine. A rule it drops, reorders
or mangles reaches all of them at the next release, and a hash it computes
differently breaks every audit and every installed copy. These pin its
exact output against a small law written here, and hold the real law in
`law/` to the plan's rules.

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

RULES = {
    'SEC-001': ('invariant', 'every', 'Never put a credential in a file.', ['gitleaks'], []),
    'OPS-001': ('invariant', 'every', 'Never force-push.', [], ['a guard hook']),
    'WORK-001': ('default', 'every', 'Change only what the task needs.', [], []),
    'GIT-010': ('default', 'owner', 'Name branches by intent.', ['semantic-pr.yml'], []),
}

BLOCK = {
    'heading': 'Working rules',
    'precedence': ['Invariants: follow every one.', 'Defaults: your user wins.'],
    'sections': [
        {'title': 'Invariants', 'kind': 'invariant', 'reach': 'every', 'rules': ['SEC-001', 'OPS-001']},
        {'title': 'Defaults', 'kind': 'default', 'reach': 'every', 'rules': ['WORK-001']},
        {'title': 'Owner-only Defaults', 'kind': 'default', 'reach': 'owner', 'rules': ['GIT-010']},
    ],
    'budget': {'target': 200, 'cap': 4000},
    'retired': {'OPS-002': 'Left to CI.'},
}

EXPECTED = """## Working rules

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


class Hub:
    """A throwaway copy of the hub's layout with the small law above."""

    def __init__(self, block: dict | None = None, rules: dict | None = None) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='render-test-'))
        (self.root / 'law' / 'rules').mkdir(parents=True)
        (self.root / 'scripts').mkdir()
        (self.root / 'scripts' / 'install.py').write_text('# installer\n', encoding='utf-8')
        self.write_block(block or BLOCK)
        for rid, (kind, reach, text, today, add) in (rules or RULES).items():
            self.write_rule(rid, kind=kind, reach=reach, text=text, enforced_by=today, to_add=add)
        (self.root / 'AGENTS.md').write_text(
            '# Agents\n\n' + render.BEGIN.format('0' * 64) + '\n\n' + render.END + '\n\n## Commands\n',
            encoding='utf-8')

    def write_block(self, block: dict) -> None:
        (self.root / 'law' / 'block.json').write_text(json.dumps(block), encoding='utf-8')

    def write_rule(self, rid: str, name: str | None = None, **fields: object) -> None:
        data = {'id': rid, 'kind': 'default', 'reach': 'every', 'text': 'Do it.', 'why': 'Because.',
                'enforced_by': [], 'to_add': []}
        data.update(fields)
        rule = render.Rule(rid, data['kind'], data['reach'], '', '', (), ())
        data.setdefault('//', rule.expected_note)
        (self.root / 'law' / 'rules' / f'{name or rid}.json').write_text(json.dumps(data), encoding='utf-8')

    def law(self):
        return render.load_law(self.root)

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


class TestRendering(HubTestCase):
    """The exact bytes of the block."""

    def test_the_block_renders_exactly(self) -> None:
        self.assertEqual(render.render_block(self.hub.law()), EXPECTED)

    def test_the_marker_carries_the_hash_of_the_block(self) -> None:
        block = render.render_block(self.hub.law())
        region = render.region(block)
        self.assertTrue(region.startswith(render.BEGIN.format(render.digest(block)) + '\n\n'))
        self.assertTrue(region.endswith('\n' + render.END + '\n'))
        found = render.find(region)
        self.assertEqual(found.inner, block)
        self.assertFalse(found.edited)

    def test_size_ignores_the_final_newline(self) -> None:
        self.assertEqual(render.size('abc\n'), 3)


class TestLawRules(HubTestCase):
    """Every way a law can break the plan, each caught with a sentence."""

    def assertProblem(self, fragment: str) -> None:
        found = render.problems(self.hub.law())
        self.assertTrue(any(fragment in line for line in found), found)

    def test_the_small_law_is_sound(self) -> None:
        self.assertEqual(render.problems(self.hub.law()), [])

    def test_a_bad_id(self) -> None:
        self.hub.write_rule('sec-1', reach='every')
        block = json.loads(json.dumps(BLOCK))
        block['sections'][1]['rules'].append('sec-1')
        self.hub.write_block(block)
        self.assertProblem('not DOMAIN-NNN')

    def test_a_rule_file_must_be_named_for_its_id(self) -> None:
        self.hub.write_rule('SEC-009', name='SEC-008')
        with self.assertRaises(render.LawError):
            self.hub.law()

    def test_a_retired_id_is_never_reused(self) -> None:
        self.hub.write_rule('OPS-002')
        block = json.loads(json.dumps(BLOCK))
        block['sections'][1]['rules'].append('OPS-002')
        self.hub.write_block(block)
        self.assertProblem('retired')

    def test_a_rule_no_section_lists(self) -> None:
        self.hub.write_rule('WORK-009')
        self.assertProblem('no section of law/block.json lists it')

    def test_a_listed_rule_with_no_file(self) -> None:
        block = json.loads(json.dumps(BLOCK))
        block['sections'][1]['rules'].append('WORK-404')
        self.hub.write_block(block)
        self.assertProblem('has no rule file')

    def test_a_rule_listed_twice(self) -> None:
        block = json.loads(json.dumps(BLOCK))
        block['sections'][1]['rules'].append('WORK-001')
        self.hub.write_block(block)
        self.assertProblem('listed 2 times')

    def test_a_rule_in_the_wrong_section(self) -> None:
        block = json.loads(json.dumps(BLOCK))
        block['sections'][0]['rules'].append('WORK-001')
        block['sections'][1]['rules'].remove('WORK-001')
        self.hub.write_block(block)
        self.assertProblem('sits in "Invariants"')

    def test_an_invariant_reaches_every_repository(self) -> None:
        self.hub.write_rule('SEC-001', kind='invariant', reach='owner', enforced_by=['x'])
        self.assertProblem('its reach is every')

    def test_an_invariant_names_an_enforcer(self) -> None:
        self.hub.write_rule('SEC-001', kind='invariant', reach='every')
        self.assertProblem('names its enforcer')

    def test_hidden_and_non_ascii_characters_are_refused(self) -> None:
        for text in ('Never\u200b do it.', 'Never \u2014 do it.', 'Two\nlines.'):
            with self.subTest(text=repr(text)):
                self.hub.write_rule('WORK-001', text=text)
                self.assertProblem('printable ASCII')

    def test_a_rule_is_a_sentence(self) -> None:
        self.hub.write_rule('WORK-001', text='No period')
        self.assertProblem('ending in a period')

    def test_a_rule_says_why(self) -> None:
        self.hub.write_rule('WORK-001', why=' ')
        self.assertProblem('say why')

    def test_the_folder_log_line_matches_the_rule(self) -> None:
        self.hub.write_rule('WORK-001', **{'//': 'WORK-001: an Invariant for every repository.'})
        self.assertProblem('should read "WORK-001: a Default for every repository."')

    def test_the_block_fits_its_cap(self) -> None:
        block = json.loads(json.dumps(BLOCK))
        block['budget']['cap'] = 100
        self.hub.write_block(block)
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
        self.assertIn('wrote AGENTS.md', out)
        code, out = self.hub.run('--check')
        self.assertEqual(code, 0, out)
        self.assertIn('over its target of 200', out)

    def test_write_keeps_the_owner_sections(self) -> None:
        self.hub.run('--write')
        agents = (self.hub.root / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertTrue(agents.startswith('# Agents\n\n'))
        self.assertTrue(agents.endswith('\n## Commands\n'))
        self.assertIn(EXPECTED, agents)

    def test_the_home_file_is_exactly_the_marked_block(self) -> None:
        self.hub.run('--write')
        home = (self.hub.root / 'home' / 'intelligence.md').read_text(encoding='utf-8')
        self.assertEqual(home, render.region(EXPECTED))

    def test_the_sums_cover_what_a_consumer_downloads(self) -> None:
        self.hub.run('--write')
        sums = (self.hub.root / 'home' / 'SHA256SUMS').read_text(encoding='utf-8').splitlines()
        self.assertEqual([line.split('  ')[1] for line in sums], ['home/intelligence.md', 'scripts/install.py'])

    def test_changing_the_installer_makes_the_sums_stale(self) -> None:
        self.hub.run('--write')
        (self.hub.root / 'scripts' / 'install.py').write_text('# changed\n', encoding='utf-8')
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('home/SHA256SUMS: stale', out)

    def test_a_hand_edit_to_the_block_fails_the_check(self) -> None:
        self.hub.run('--write')
        path = self.hub.root / 'AGENTS.md'
        path.write_text(path.read_text(encoding='utf-8').replace('Never force-push.', 'Rarely force-push.'),
                        encoding='utf-8')
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('AGENTS.md: stale', out)

    def test_an_agents_file_without_a_block_fails_the_check(self) -> None:
        (self.hub.root / 'AGENTS.md').write_text('# Agents\n', encoding='utf-8')
        code, out = self.hub.run('--check')
        self.assertEqual(code, 1, out)
        self.assertIn('carries no INTELLIGENCE block', out)

    def test_a_broken_law_stops_every_mode(self) -> None:
        self.hub.write_rule('WORK-001', text='No period')
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
        for command in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'law'], ['tag', 'v0.1.0']):
            subprocess.run(git + command, cwd=self.hub.root, check=True, capture_output=True)
        (self.hub.root / 'home' / 'intelligence.md').write_text('changed since the tag\n', encoding='utf-8')
        code, out = self.hub.run('--pins', 'v0.1.0')
        self.assertEqual(code, 0, out)
        self.assertIn('version=v0.1.0', out)
        self.assertIn(f'home_sha256={render.digest(render.region(EXPECTED))}', out)


class TestCloudSetup(HubTestCase):
    """`--setup` fills the cloud setup script with the pins of a release tag."""

    template = "VERSION='@VERSION@'\nHOME_SHA256='@HOME_SHA256@'\nINSTALL_SHA256='@INSTALL_SHA256@'\n"

    def tag(self) -> None:
        git = ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', '-c', 'commit.gpgsign=false',
               '-c', 'tag.gpgsign=false']
        for command in (['init', '-q'], ['add', '-A'], ['commit', '-q', '-m', 'law'], ['tag', 'v0.1.0']):
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

    def test_a_template_without_its_placeholders_is_refused(self) -> None:
        (self.hub.root / 'setup').mkdir()
        (self.hub.root / 'setup' / 'claude-cloud-setup.sh').write_text("VERSION='v0.0.1'\n", encoding='utf-8')
        self.hub.run('--write')
        self.tag()
        with self.assertRaises(SystemExit):
            self.hub.run('--setup', 'v0.1.0')

    def test_the_real_template_has_every_placeholder(self) -> None:
        text = (SCRIPT.parents[1] / render.SETUP_FILE).read_text(encoding='utf-8')
        for name in ('VERSION', 'HOME_SHA256', 'INSTALL_SHA256'):
            self.assertIn(f"{name}='@{name}@'", text)


class TestTheRealLaw(unittest.TestCase):
    """The law in this repository, and the copies rendered from it."""

    root = SCRIPT.parents[1]

    def test_it_breaks_no_rule_and_fits_its_cap(self) -> None:
        law = render.load_law(self.root)
        self.assertEqual(render.problems(law), [])
        self.assertLessEqual(render.size(render.render_block(law)), law.cap)

    def test_every_copy_is_current(self) -> None:
        self.assertEqual(render.stale(self.root, render.load_law(self.root)), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
