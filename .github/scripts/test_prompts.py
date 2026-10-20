#!/usr/bin/env python3
"""Tests for the prompts file every repository gets.

WHY THIS EXISTS. `docs/Prompts.md` reaches every repository that takes part
in sync, beside the prompts its owner writes, so three promises matter: the
block between its markers is sealed the same way every time, nothing
outside the block is ever touched, and every universal prompt keeps the
shape its practices describe, in text no formatter would rewrite. These
hold the sealing, the change sync makes to a repository's copy, each rule
`--check` holds the source to, and the real source to all three.

Run it:

    python3 .github/scripts/test_prompts.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import re
import shutil
import subprocess
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

PROMPT = ('### Fix A Bug\n\n**Use when** it breaks. **Fill in** what broke.\n\n```text\n<context>\n'
          '{{WHAT_BROKE}} is broken.\n</context>\n\n<task>\nFix it.\n</task>\n\n<done_when>\n'
          '- The checks pass.\n</done_when>\n```\n')
INNER = f'## How\n\nCopy one.\n\n{PROMPT}'
SOURCE = ('<!--\ntitle: x\n-->\n\n# Prompts\n\n---\n\n<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n\n' + INNER +
          '\n<!-- INTELLIGENCE:PROMPTS:END -->\n\n---\n\n## Prompts For This Repository\n\n_Yours._\n')


class TestSealing(unittest.TestCase):
    """The block is sealed with the hash of its text, and nothing else changes."""

    def test_the_block_is_sealed_with_the_hash_of_its_text(self) -> None:
        release = prompts.seal(SOURCE)
        found = prompts.find(release.seed)
        self.assertEqual(found.marker, render.digest(INNER))
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

    def test_a_broken_prompt_fails_the_check_with_its_line(self) -> None:
        self.write(SOURCE.replace('<task>\n', '<task>\n<constraints>\n', 1))
        found = prompts.problems(self.root)
        line = SOURCE.splitlines().index('<task>') + 2
        self.assertIn(f'{prompts.SOURCE}:{line}: "Fix A Bug": <constraints> is never closed', found)
        self.assertEqual(self.check(), 1)


def changed(*pairs: tuple[str, str]) -> str:
    """SOURCE with each `(old, new)` replaced once, in order."""
    text = SOURCE
    for old, new in pairs:
        if old not in text:
            raise AssertionError(f'{old!r} is not in the source')
        text = text.replace(old, new, 1)
    return text


# What each rule the formatter would enforce catches, by a fragment of its message.
FORMATTER_CASES = {
    'trailing whitespace': changed(('Fix it.\n', 'Fix it.  \n')),
    'a tab': changed(('Copy one.', 'Copy\tone.')),
    'a second blank line in a row': changed(('Copy one.\n', 'Copy one.\n\n')),
    'a bullet a formatter rewrites': changed(('Copy one.', '* Copy one.')),
    'a numbered item a formatter rewrites': changed(('Copy one.', '1) Copy one.')),
    'no blank line before it': changed(('Copy one.\n\n###', 'Copy one.\n###')),
    'no blank line after it': changed(('## How\n\n', '## How\n')),
    'a list with no blank line before it': changed(('Copy one.', 'Copy one.\n- Paste it.')),
    'a line run on from a list item': changed(('Copy one.', '- Copy one.\nPaste it.')),
}


class TestLint(unittest.TestCase):
    """Each rule `--check` holds the universal prompts to, caught where it breaks."""

    def assertCaught(self, fragment: str, text: str) -> None:
        found = prompts.lint(text)
        self.assertTrue(any(fragment in line for line in found), found)

    def test_a_sound_block_passes(self) -> None:
        self.assertEqual(prompts.lint(SOURCE), [])

    def test_each_problem_names_its_line(self) -> None:
        line = SOURCE.splitlines().index('Fix it.') + 1
        self.assertEqual(prompts.lint(changed(('Fix it.\n', 'Fix it. \n'))), [
            f'{prompts.SOURCE}:{line}: trailing whitespace, which a formatter strips or reads as a line break'])

    def test_text_a_formatter_would_rewrite_is_caught(self) -> None:
        for fragment, text in FORMATTER_CASES.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_every_block_of_code_is_a_text_fence_that_closes(self) -> None:
        cases = {
            'opens with ```text alone': changed(('```text\n', '```python\n')),
            'opens with ```text alone, at the start': changed(('```text\n', '  ```text\n')),
            'a fence inside a block of text': changed(('Fix it.\n', 'Fix it.\n```bash\n')),
            'a block of code that never closes': changed(('</done_when>\n```\n', '</done_when>\n')),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_every_prompt_keeps_the_shape_the_practices_describe(self) -> None:
        cases = {
            'says when to use it with **Use when**': changed(('**Use when** it breaks. ', '')),
            'holds 2 blocks of text': changed(('</done_when>\n```\n', '</done_when>\n```\n\n```text\nMore.\n```\n')),
            'holds 0 blocks of text': changed((PROMPT[PROMPT.index('```text'):], 'Only prose.\n')),
            'has no <context>': changed(('<context>\n{{WHAT_BROKE}} is broken.\n</context>', '{{WHAT_BROKE}} broke.')),
            'has no <task>': changed(('<task>\nFix it.\n</task>\n\n', '')),
            'has no <done_when> or <output>': changed(('\n\n<done_when>\n- The checks pass.\n</done_when>', '')),
            'is not a section the practices name': changed(('<done_when>', '<finish>'), ('</done_when>', '</finish>')),
            'a second <context>': changed(('<task>', '<context>\nMore.\n</context>\n\n<task>')),
            'keep them in the order': changed((
                '<context>\n{{WHAT_BROKE}} is broken.\n</context>\n\n<task>\nFix it.\n</task>',
                '<task>\nFix it.\n</task>\n\n<context>\n{{WHAT_BROKE}} is broken.\n</context>')),
            '<task> is never closed': changed(('</task>\n', '')),
            'closes a tag that is not open': changed(('Fix it.\n', 'Fix it.\n</constraints>\n')),
            'is not a tag this file writes': changed(('<task>', '<Task>'), ('</task>', '</Task>')),
            'over the cap': changed(('Fix it.', 'Fix it. ' + 'Then check it. ' * (prompts.CAP // 15))),
            'a second heading "Fix A Bug"': changed((PROMPT, f'{PROMPT}\n{PROMPT}')),
            'a heading in the block is': changed(('### Fix A Bug', '#### Fix A Bug')),
            'holds no universal prompt': changed((PROMPT, 'No prompt here.\n')),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_each_detail_that_changes_is_a_placeholder(self) -> None:
        cases = {
            'is not a placeholder': changed(('{{WHAT_BROKE}}', '{{what broke}}')),
            'a stray {{': changed(('{{WHAT_BROKE}}', '{{WHAT_BROKE}')),
            'takes double braces, as {{WHAT_BROKE}}': changed(('{{WHAT_BROKE}}', '{WHAT_BROKE}')),
            'marks nothing to fill in': changed(('{{WHAT_BROKE}}', 'The parser')),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_tags_and_braces_inside_a_section_are_free(self) -> None:
        text = changed(('{{WHAT_BROKE}} is broken.\n', '{{WHAT_BROKE}} is broken.\n<error>\n{{ERROR}}\n</error>\n'),
                       ('Fix it.', 'Fix it, and keep {"a": 1} as it is.'))
        self.assertEqual(prompts.lint(text), [])

    def test_a_tag_may_name_its_source(self) -> None:
        text = changed(('{{WHAT_BROKE}} is broken.\n', '{{WHAT_BROKE}} is broken.\n<error_output source="CI log">\n'
                                                      '{{ERROR}}\n</error_output>\n'))
        self.assertEqual(prompts.lint(text), [])

    def test_a_tag_named_in_backticks_is_a_mention_not_a_section(self) -> None:
        self.assertEqual(prompts.lint(changed(('Fix it.', 'Fix it, and keep `<task>` in mind.'))), [])

    def test_the_text_an_agent_reads_is_plain_and_calm(self) -> None:
        cases = {
            'MUST in capitals': changed(('Fix it.', 'You MUST fix it.')),
            'NEVER in capitals': changed(('Fix it.', 'Fix it. NEVER skip a test.')),
            'outside printable ASCII': changed(('Fix it.', 'Fix it \u2192 then test it.')),
            '$ARGUMENTS is a slot an app fills by itself': changed(('Fix it.', 'Fix $ARGUMENTS.')),
            '$1 is a slot': changed(('Fix it.', 'Fix $1.')),
            '${input: is a slot': changed(('Fix it.', 'Fix ${input:what}.')),
            '!{ is a slot': changed(('Fix it.', 'Fix it, then run !{make check}.')),
            '"Think step by step" is wording': changed(('Fix it.', 'Think step by step, then fix it.')),
            '"If in doubt" is wording': changed(('Fix it.', 'Fix it. If in doubt, ask.')),
            '"You are an expert" is wording': changed(('Fix it.', 'You are an expert. Fix it.')),
            'hides or reorders text': changed(('Copy one.', 'Copy\u200b one.')),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_capitals_in_a_placeholder_are_no_emphasis(self) -> None:
        self.assertEqual(prompts.lint(changed(('{{WHAT_BROKE}}', '{{WHAT_MUST_WORK}}'))), [])


class TestCompare(unittest.TestCase):
    """What a newer block does to the universal prompts, named for the pull request that delivers it."""

    def inner(self, text: str) -> str:
        return prompts.find(prompts.seal(text).seed).inner

    def test_each_prompt_added_reworded_and_dropped_is_named(self) -> None:
        old = self.inner(changed((PROMPT, PROMPT + '\n' + PROMPT.replace('Fix A Bug', 'Explain This Code'))))
        new = self.inner(changed((PROMPT, PROMPT + '\n' + PROMPT.replace('Fix A Bug', 'Plan A Change')),
                                 ('Fix it.', 'Find the cause, and fix it.')))
        self.assertEqual(prompts.compare(old, new),
                         'adds Plan A Change, rewords Fix A Bug and drops Explain This Code')

    def test_a_change_to_the_guide_alone_says_so(self) -> None:
        old = self.inner(SOURCE)
        self.assertEqual(prompts.compare(old, self.inner(changed(('Copy one.', 'Copy it.')))),
                         'changes only the guide around the prompts')

    def test_a_new_use_when_line_is_a_rewording(self) -> None:
        old = self.inner(SOURCE)
        self.assertEqual(prompts.compare(old, self.inner(changed(('it breaks.', 'it fails.')))),
                         'rewords Fix A Bug')

    def test_names_read_as_prose(self) -> None:
        self.assertEqual([prompts.listed(names) for names in (['A'], ['A', 'B'], ['A', 'B', 'C'])],
                         ['A', 'A and B', 'A, B and C'])


@unittest.skipUnless(shutil.which('prettier'), 'Prettier is not installed')
class TestPrettierAgrees(unittest.TestCase):
    """Where Prettier is installed: it leaves the real source as it is, and rewrites what each formatter rule finds."""

    # The standards' config/prettierrc.json, which their auto-format workflow formats every repository with.
    CONFIG = {'singleQuote': True, 'tabWidth': 2, 'printWidth': 80, 'trailingComma': 'es5'}

    def formatted(self, text: str) -> str:
        with tempfile.TemporaryDirectory() as folder:
            config = pathlib.Path(folder) / 'prettierrc.json'
            config.write_text(json.dumps(self.CONFIG), encoding='utf-8')
            done = subprocess.run(['prettier', '--config', str(config), '--parser', 'markdown'], input=text,
                                  capture_output=True, text=True, check=True)
        return done.stdout

    def test_the_real_source_is_as_prettier_writes_it(self) -> None:
        text = (ROOT / prompts.SOURCE).read_text(encoding='utf-8')
        self.assertEqual(self.formatted(text), text)

    def test_each_formatter_rule_catches_a_change_prettier_would_make(self) -> None:
        self.assertEqual(self.formatted(SOURCE), SOURCE)
        for fragment, text in FORMATTER_CASES.items():
            with self.subTest(fragment=fragment):
                self.assertNotEqual(self.formatted(text), text)


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

    def test_it_holds_the_universal_prompts(self) -> None:
        universal, _ = prompts.parse(prompts.find(self.release.seed).inner)
        self.assertGreaterEqual(len(universal), 5)
        self.assertTrue(all(prompt.blocks == 1 for prompt in universal))

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
