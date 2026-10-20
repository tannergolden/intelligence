#!/usr/bin/env python3
"""Tests for the prompts file every repository gets.

WHY THIS EXISTS. `docs/Prompts.md` reaches every repository that takes part
in sync, beside the prompts its owner writes, so two promises matter: the
block between its markers is sealed the same way every time, and nothing
outside the block is ever touched. These hold the sealing, the change sync
makes to a repository's copy, and the real source to both.

Run it:

    python3 .github/scripts/test_prompts.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name while the class is built.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


prompts = load('prompts', HERE / 'prompts.py')
render = prompts.render

SOURCE = ('<!--\ntitle: x\n-->\n\n# Prompts\n\n---\n\n<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n\n## How\n\nCopy one.\n\n'
          '<!-- INTELLIGENCE:PROMPTS:END -->\n\n---\n\n## Prompts For This Repository\n\n_Yours._\n')


class TestSealing(unittest.TestCase):
    """The block is sealed with the hash of its text, and nothing else changes."""

    def test_the_block_is_sealed_with_the_hash_of_its_text(self) -> None:
        release = prompts.seal(SOURCE)
        found = prompts.find(release.seed)
        self.assertEqual(found.marker, render.digest('## How\n\nCopy one.\n'))
        self.assertFalse(found.edited)
        self.assertEqual(release.seed[found.start:found.end], release.region)
        self.assertEqual(release.marker, found.marker)

    def test_sealing_changes_nothing_but_the_marker(self) -> None:
        sealed = prompts.seal(SOURCE).seed
        self.assertEqual(re.sub(r' sha256:[0-9a-f]{64}', '', sealed), SOURCE)
        self.assertEqual(prompts.seal(SOURCE), prompts.seal(SOURCE))

    def test_a_source_without_exactly_one_block_is_refused(self) -> None:
        for text in (SOURCE.replace('<!-- INTELLIGENCE:PROMPTS:END -->\n', ''), SOURCE + SOURCE):
            with self.subTest(text=text[-40:]), self.assertRaises(ValueError):
                prompts.seal(text)

    def test_the_rules_block_and_the_prompts_block_are_never_confused(self) -> None:
        self.assertIsNone(prompts.find(render.region('## Working rules\n\n- X: Y.\n')))
        self.assertIsNone(render.find(prompts.seal(SOURCE).seed))


class TestChange(unittest.TestCase):
    """What sync does to a repository's `docs/Prompts.md`."""

    def setUp(self) -> None:
        self.release = prompts.seal(SOURCE)
        self.old = prompts.seal(SOURCE.replace('Copy one.', 'An older guide.'))

    def test_a_repository_without_the_file_gets_all_of_it(self) -> None:
        text, note = prompts.change(None, self.release)
        self.assertEqual(text, self.release.seed)
        self.assertIn('adds `docs/Prompts.md`', note)

    def test_an_older_block_is_replaced_and_everything_else_stays(self) -> None:
        mine = self.old.seed.replace('_Yours._', '### Ship A Release\n\nOurs.')
        text, note = prompts.change(mine, self.release)
        self.assertIsNone(note)
        self.assertEqual(text, mine.replace(self.old.region, self.release.region))
        self.assertIn('### Ship A Release\n\nOurs.', text)

    def test_a_current_file_is_left_as_it_is(self) -> None:
        self.assertEqual(prompts.change(self.release.seed, self.release), (None, None))

    def test_a_hand_edit_inside_the_block_is_repaired(self) -> None:
        text, _note = prompts.change(self.release.seed.replace('Copy one.', 'Copy two.'), self.release)
        self.assertEqual(text, self.release.seed)

    def test_a_file_of_the_repositorys_own_is_never_touched(self) -> None:
        self.assertEqual(prompts.change('# Our prompts\n', self.release), (None, None))

    def test_two_blocks_are_refused(self) -> None:
        with self.assertRaises(ValueError):
            prompts.change(self.release.seed + self.release.region, self.release)

    def test_only_the_topic_keeps_the_prompts_out(self) -> None:
        self.assertTrue(prompts.opted_out({'topics': ['no-intelligence-prompts']}))
        self.assertFalse(prompts.opted_out({'topics': ['no-intelligence']}))
        self.assertFalse(prompts.opted_out({}))


class TestProblems(unittest.TestCase):
    """`--check` holds the source to what every public repository can carry."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='prompts-test-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / 'setup').mkdir()

    def write(self, text: str) -> None:
        (self.root / prompts.SOURCE).write_text(text, encoding='utf-8')

    def check(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return prompts.main(['--check', '--root', str(self.root)])

    def test_a_sound_source_passes(self) -> None:
        self.write(SOURCE)
        self.assertEqual(prompts.problems(self.root), [])
        self.assertEqual(self.check(), 0)

    def test_each_problem_is_named(self) -> None:
        cases = {
            'sealed marker': prompts.seal(SOURCE).seed,
            'needs exactly one': SOURCE.replace('<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n', ''),
            'tannergolden/vault': SOURCE.replace('Copy one.', 'See tannergolden/vault.'),
            'en or em dash': SOURCE.replace('Copy one.', 'Copy one \u2014 then paste it.'),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.write(text)
                found = prompts.problems(self.root)
                self.assertTrue(any(fragment in line for line in found), found)
                self.assertEqual(self.check(), 1)

    def test_a_missing_source_is_named(self) -> None:
        self.assertEqual(prompts.problems(self.root), [f'{prompts.SOURCE} is missing'])


class TestTheRealPrompts(unittest.TestCase):
    """`setup/Prompts.md` in this repository."""

    def setUp(self) -> None:
        self.text = (ROOT / prompts.SOURCE).read_text(encoding='utf-8')
        self.release = prompts.load(ROOT)

    def test_it_breaks_no_rule(self) -> None:
        self.assertEqual(prompts.problems(ROOT), [])

    def test_it_opens_with_the_frontmatter_the_standards_require(self) -> None:
        self.assertTrue(self.text.startswith('<!--\ntitle: '))
        head = self.text.split('-->', 1)[0]
        for key in ('description', 'type', 'keywords'):
            self.assertRegex(head, rf'(?m)^{key}: ')

    def test_every_prompt_says_when_to_use_it_and_what_to_fill_in(self) -> None:
        sections = re.split(r'(?m)^### ', prompts.find(self.release.seed).inner)[1:]
        self.assertGreaterEqual(len(sections), 5)
        for section in sections:
            with self.subTest(prompt=section.splitlines()[0]):
                self.assertIn('**Use when**', section)
                self.assertIn('**Fill in**', section)
                self.assertIn('```text\n', section)

    def test_every_block_is_plain_text_so_a_formatter_leaves_it_alone(self) -> None:
        self.assertEqual(set(re.findall(r'(?m)^```(\w*)$', self.text)) - {''}, {'text'})

    def test_every_placeholder_is_in_double_braces_and_capitals(self) -> None:
        names = re.findall(r'\{\{(.*?)\}\}', self.text)
        self.assertTrue(names)
        for name in names:
            self.assertRegex(name, r'^[A-Z][A-Z_]*$')

    def test_the_repositorys_own_section_sits_outside_the_block(self) -> None:
        found = prompts.find(self.release.seed)
        self.assertGreater(self.release.seed.index('## 📌 Prompts For This Repository'), found.end)


if __name__ == '__main__':
    unittest.main(verbosity=2)
