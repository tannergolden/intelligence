#!/usr/bin/env python3
"""Tests for the universal prompts the hub keeps, and the page each repository gets.

WHY THIS EXISTS. The universal prompts stay in the hub's `docs/Prompts.md`,
and every repository that takes part in sync gets `docs/Prompts.md` once, as
an empty page of its own. Three promises matter: a repository's own page is
never touched, the universal prompts an earlier release sealed into a
repository come out again with nothing else lost, and every universal prompt
keeps the shape its practices describe, in text no formatter would rewrite.
These hold the change sync makes to a repository's page, each rule `--check`
holds the hub's two files to, and the real files to all three.

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
from unittest import mock

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
INNER = f'## How\n\nCopy one.\n\n## Find A Prompt\n\n- [Fix A Bug](#fix-a-bug) {prompts.MARK}\n\n{PROMPT}'
READY = ('### Tour The Code\n\n**Use when** you are new here.\n\n```text\n<context>\nI am new to this '
         'repository.\n</context>\n\n<task>\nShow me around it.\n</task>\n\n<output>\nA short tour.\n</output>\n```\n')
# The hub's universal prompts: a header, the prompts, and a footer, each part set off by a --- line.
SOURCE = '<!--\ntitle: x\n-->\n\n# Prompts\n\n---\n\n' + INNER + '\n---\n\nThe end.\n'
# The page a repository first gets.
EMPTY = '<!--\ntitle: x\n-->\n\n# Prompts\n\n---\n\n## Use It\n\n<!-- Yours. -->\n\n---\n\nThe end.\n'
# A repository's page as an earlier release delivered it, with the universal prompts sealed in.
OLD_INNER = '## How\n\nCopy one.\n'
OLD = ('# Prompts\n\n---\n\n'
       f'<!-- INTELLIGENCE:PROMPTS:BEGIN sha256:{render.digest(OLD_INNER)} -->\n\n{OLD_INNER}\n'
       '<!-- INTELLIGENCE:PROMPTS:END -->\n\n---\n\n## Prompts For This Repository\n\n'
       f'{prompts.OLD_NOTE}\n\n---\n\nThe end.\n')
# What an earlier release's setup/Prompts.md held: the universal prompts, between markers for sync to seal.
OLD_SOURCE = '<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n\nOld.\n\n<!-- INTELLIGENCE:PROMPTS:END -->\n'


class TestPage(unittest.TestCase):
    """What sync does to a repository's `docs/Prompts.md`."""

    def test_a_repository_without_the_file_gets_the_empty_page(self) -> None:
        self.assertEqual(prompts.change(None, EMPTY), (EMPTY, prompts.ADDED))

    def test_a_page_of_its_own_is_never_touched(self) -> None:
        for own in ('# Our prompts\n', EMPTY, EMPTY.replace('<!-- Yours. -->', '### Ship It\n\nOurs.')):
            with self.subTest(own=own[-30:]):
                self.assertEqual(prompts.change(own, EMPTY), (None, None))

    def test_the_universal_prompts_come_out_and_its_own_stay(self) -> None:
        mine = OLD.replace(prompts.OLD_NOTE, prompts.OLD_NOTE + '\n\n### Ship A Release\n\nOurs.')
        text, note = prompts.change(mine, EMPTY)
        self.assertEqual(note, prompts.TAKEN_OUT)
        self.assertEqual(text, '# Prompts\n\n---\n\n## Prompts For This Repository\n\n'
                               f'{prompts.NEW_NOTE}\n\n### Ship A Release\n\nOurs.\n\n---\n\nThe end.\n')

    def test_a_note_the_repository_reworded_stays_its_own(self) -> None:
        text, _note = prompts.change(OLD.replace(prompts.OLD_NOTE, '_Ours._'), EMPTY)
        self.assertIn('_Ours._', text)
        self.assertNotIn('INTELLIGENCE:PROMPTS', text)

    def test_a_block_at_either_end_comes_out_cleanly(self) -> None:
        block = OLD[OLD.index('<!-- INTELLIGENCE'):OLD.index('\n\n---\n\n## Prompts') + 1]
        for text, left in ((block + '\n# Ours\n', '# Ours\n'), ('# Ours\n\n' + block, '# Ours\n')):
            with self.subTest(text=text[:20]):
                self.assertEqual(prompts.change(text, EMPTY)[0], left)

    def test_a_file_untouched_since_its_release_becomes_the_empty_page(self) -> None:
        found = prompts.find(OLD)
        rest = OLD[:found.start] + OLD[found.end:]
        with mock.patch.object(prompts, 'DELIVERED', frozenset({prompts.hashlib.sha256(rest.encode()).hexdigest()})):
            self.assertEqual(prompts.change(OLD, EMPTY), (EMPTY, prompts.TAKEN_OUT))
            self.assertEqual(prompts.change(OLD.replace('\n', '\r\n'), EMPTY)[0], EMPTY)

    def test_the_file_the_release_delivered_becomes_the_empty_page(self) -> None:
        # v0.3.0 delivered the universal prompts; its file, sealed as sync sealed it, is the one DELIVERED knows.
        done = subprocess.run(['git', 'show', 'v0.3.0:setup/Prompts.md'], cwd=ROOT, capture_output=True, text=True,
                              check=False)
        if done.returncode != 0:
            self.skipTest('the v0.3.0 tag is not fetched here')
        source = done.stdout
        inner = re.search(r'<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n(.*?)<!-- INTELLIGENCE:PROMPTS:END -->', source,
                          re.S).group(1).strip('\n') + '\n'
        seed = source.replace('<!-- INTELLIGENCE:PROMPTS:BEGIN -->',
                              f'<!-- INTELLIGENCE:PROMPTS:BEGIN sha256:{render.digest(inner)} -->')
        self.assertEqual(prompts.change(seed, EMPTY), (EMPTY, prompts.TAKEN_OUT))

    def test_two_blocks_are_refused(self) -> None:
        found = prompts.find(OLD)
        with self.assertRaises(ValueError):
            prompts.change(OLD + OLD[found.start:found.end], EMPTY)

    def test_only_the_topic_keeps_the_page_out(self) -> None:
        self.assertTrue(prompts.opted_out({'topics': ['no-intelligence-prompts']}))
        self.assertFalse(prompts.opted_out({'topics': ['no-intelligence']}))
        self.assertFalse(prompts.opted_out({}))

    def test_a_hub_from_before_the_page_gives_none(self) -> None:
        # Its setup/Prompts.md held the universal prompts between markers, for sync to seal.
        self.assertIsNone(prompts.page(OLD_SOURCE))
        self.assertEqual(prompts.page(EMPTY), EMPTY)
        with tempfile.TemporaryDirectory() as folder:
            self.assertIsNone(prompts.template(pathlib.Path(folder)))

    def test_the_rules_block_is_never_taken_for_the_prompts(self) -> None:
        self.assertIsNone(prompts.find(render.region('## Working rules\n\n- X: Y.\n')))
        self.assertIsNone(render.find(OLD))


class TestProblems(unittest.TestCase):
    """`--check` holds the hub's two files to what everyone copies from them."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='prompts-test-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        (self.root / 'docs').mkdir()
        (self.root / 'setup').mkdir()
        self.write(SOURCE)
        self.write(EMPTY, prompts.TEMPLATE)

    def write(self, text: str, name: str = prompts.UNIVERSAL) -> None:
        (self.root / name).write_text(text, encoding='utf-8')

    def check(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return prompts.main(['--check', '--root', str(self.root)])

    def test_sound_files_pass(self) -> None:
        self.assertEqual(prompts.problems(self.root), [])
        self.assertEqual(self.check(), 0)

    def test_each_problem_is_named(self) -> None:
        cases = {
            'the universal prompts stay in the hub': (prompts.UNIVERSAL, SOURCE.replace(
                '## How', '<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n\n## How')),
            'tannergolden/vault': (prompts.UNIVERSAL, SOURCE.replace('Copy one.', 'See tannergolden/vault.')),
            'en or em dash': (prompts.UNIVERSAL, SOURCE.replace('Copy one.', 'Copy one \u2014 then paste it.')),
            'its header and its footer': (prompts.UNIVERSAL, SOURCE.replace('---\n', '', 1)),
            'the page a repository gets is all its own': (prompts.TEMPLATE, EMPTY + OLD_SOURCE),
            'holds a prompt': (prompts.TEMPLATE, EMPTY.replace('<!-- Yours. -->', PROMPT)),
            'setup/Prompts.md names tannergolden/vault': (prompts.TEMPLATE,
                                                          EMPTY.replace('Yours.', 'tannergolden/vault')),
        }
        for fragment, (name, text) in cases.items():
            with self.subTest(fragment=fragment):
                self.setUp()
                self.write(text, name)
                found = prompts.problems(self.root)
                self.assertTrue(any(fragment in line for line in found), found)
                self.assertEqual(self.check(), 1)

    def test_a_missing_file_is_named(self) -> None:
        (self.root / prompts.UNIVERSAL).unlink()
        (self.root / prompts.TEMPLATE).unlink()
        self.assertEqual(prompts.problems(self.root),
                         [f'{prompts.UNIVERSAL} is missing', f'{prompts.TEMPLATE} is missing'])

    def test_a_broken_prompt_fails_the_check_with_its_line(self) -> None:
        self.write(SOURCE.replace('<task>\n', '<task>\n<constraints>\n', 1))
        found = prompts.problems(self.root)
        line = SOURCE.splitlines().index('<task>') + 2
        self.assertIn(f'{prompts.UNIVERSAL}:{line}: "Fix A Bug": <constraints> is never closed', found)
        self.assertEqual(self.check(), 1)

    def test_without_check_it_prints_the_page_a_repository_first_gets(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(prompts.main(['--root', str(self.root)]), 0)
        self.assertEqual(out.getvalue(), EMPTY)


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
    'no blank line before it': changed((f'{prompts.MARK}\n\n###', f'{prompts.MARK}\n###')),
    'no blank line after it': changed(('## How\n\n', '## How\n')),
    'a list with no blank line before it': changed(('Copy one.', 'Copy one.\n- Paste it.')),
    'a line run on from a list item': changed(('Copy one.', '- Copy one.\nPaste it.')),
}


class TestLint(unittest.TestCase):
    """Each rule `--check` holds the universal prompts to, caught where it breaks."""

    def assertCaught(self, fragment: str, text: str) -> None:
        found = prompts.lint(text)
        self.assertTrue(any(fragment in line for line in found), found)

    def test_a_sound_file_passes(self) -> None:
        self.assertEqual(prompts.lint(SOURCE), [])

    def test_each_problem_names_its_line(self) -> None:
        line = SOURCE.splitlines().index('Fix it.') + 1
        self.assertEqual(prompts.lint(changed(('Fix it.\n', 'Fix it. \n'))), [
            f'{prompts.UNIVERSAL}:{line}: trailing whitespace, which a formatter strips or reads as a line break'])

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
            'a heading here is': changed(('### Fix A Bug', '#### Fix A Bug')),
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
            'says what to fill in but marks nothing': changed(('{{WHAT_BROKE}}', 'The parser')),
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

    def test_a_prompt_ready_to_run_has_nothing_to_fill_in(self) -> None:
        ready = changed((prompts.MARK, f'{prompts.MARK}, [Tour The Code](#tour-the-code)'),
                        (PROMPT, f'{PROMPT}\n{READY}'))
        self.assertEqual(prompts.lint(ready), [])
        self.assertCaught('holds {{WHERE}} but no **Fill in** line', ready.replace('Show me around it.',
                                                                                    'Show me {{WHERE}}.'))
        marked = ready.replace('(#tour-the-code)', f'(#tour-the-code) {prompts.MARK}')
        self.assertCaught('marks "Tour The Code"', marked)

    def test_the_index_links_every_prompt_once_by_its_name(self) -> None:
        cases = {
            'the file has no "## Find A Prompt" part': changed(('## Find A Prompt', '## Prompts')),
            '"Fix A Bug" is missing from the "Find A Prompt" index': changed(('- [Fix A Bug](#fix-a-bug)', '- None.')),
            'the index links #fix-it, which no prompt heading makes': changed(('(#fix-a-bug)', '(#fix-it)')),
            'the index calls "Fix A Bug" "Bug Fixing"': changed(('[Fix A Bug]', '[Bug Fixing]')),
            'the index links "Fix A Bug" again': changed(('- [Fix A Bug](#fix-a-bug)',
                                                            '- [Fix A Bug](#fix-a-bug), [Fix A Bug](#fix-a-bug)')),
            '"Fix A Bug" has details to fill in; mark its link': changed((f' {prompts.MARK}', '')),
        }
        for fragment, text in cases.items():
            with self.subTest(fragment=fragment):
                self.assertCaught(fragment, text)

    def test_a_heading_anchors_as_github_makes_it(self) -> None:
        self.assertEqual([prompts.anchor(name) for name in ('Fix A Bug', 'Clean Up & Simplify', "Owner's Guide")],
                         ['fix-a-bug', 'clean-up--simplify', 'owners-guide'])

    def test_capitals_in_a_placeholder_are_no_emphasis(self) -> None:
        self.assertEqual(prompts.lint(changed(('{{WHAT_BROKE}}', '{{WHAT_MUST_WORK}}'))), [])


@unittest.skipUnless(shutil.which('prettier'), 'Prettier is not installed')
class TestPrettierAgrees(unittest.TestCase):
    """Where Prettier is installed: it leaves the real files as they are, and rewrites what each rule finds."""

    # The standards' config/prettierrc.json, which their auto-format workflow formats every repository with.
    CONFIG = {'singleQuote': True, 'tabWidth': 2, 'printWidth': 80, 'trailingComma': 'es5'}

    def formatted(self, text: str) -> str:
        with tempfile.TemporaryDirectory() as folder:
            config = pathlib.Path(folder) / 'prettierrc.json'
            config.write_text(json.dumps(self.CONFIG), encoding='utf-8')
            done = subprocess.run(['prettier', '--config', str(config), '--parser', 'markdown'], input=text,
                                  capture_output=True, text=True, check=True)
        return done.stdout

    def test_the_real_files_are_as_prettier_writes_them(self) -> None:
        for name in (prompts.UNIVERSAL, prompts.TEMPLATE):
            with self.subTest(name=name):
                text = (ROOT / name).read_text(encoding='utf-8')
                self.assertEqual(self.formatted(text), text)

    def test_each_formatter_rule_catches_a_change_prettier_would_make(self) -> None:
        self.assertEqual(self.formatted(SOURCE), SOURCE)
        for fragment, text in FORMATTER_CASES.items():
            with self.subTest(fragment=fragment):
                self.assertNotEqual(self.formatted(text), text)


class TestTheRealPrompts(unittest.TestCase):
    """The universal prompts in this hub's `docs/Prompts.md`, and the page in `setup/Prompts.md`."""

    def setUp(self) -> None:
        self.text = (ROOT / prompts.UNIVERSAL).read_text(encoding='utf-8')
        self.page = (ROOT / prompts.TEMPLATE).read_text(encoding='utf-8')

    def test_they_break_no_rule(self) -> None:
        self.assertEqual(prompts.problems(ROOT), [])

    def test_each_opens_with_the_frontmatter_the_standards_require(self) -> None:
        for text in (self.text, self.page):
            self.assertTrue(text.startswith('<!--\ntitle: '))
            head = text.split('-->', 1)[0]
            for key in ('description', 'type', 'keywords'):
                self.assertRegex(head, rf'(?m)^{key}: ')

    def test_the_hub_holds_the_universal_prompts(self) -> None:
        universal = prompts.universal(ROOT)
        self.assertGreaterEqual(len(universal), 5)
        self.assertTrue(all(prompt.blocks == 1 for prompt in universal))

    def test_every_block_is_plain_text_so_a_formatter_leaves_it_alone(self) -> None:
        self.assertEqual(set(re.findall(r'(?m)^```(\w*)$', self.text)) - {''}, {'text'})

    def test_every_placeholder_is_in_double_braces_and_capitals(self) -> None:
        names = re.findall(r'\{\{(.*?)\}\}', self.text)
        self.assertTrue(names)
        for name in names:
            self.assertRegex(name, r'^[A-Z][A-Z_]*$')

    def test_the_page_a_repository_gets_is_empty_and_points_here(self) -> None:
        self.assertEqual(prompts.template(ROOT), self.page)
        for section in ('Use It', 'Change It', 'Understand It'):
            self.assertRegex(self.page, rf'(?m)^## \S+ {section}$')
        self.assertIn(f']({prompts.HUB_PROMPTS})', self.page)
        self.assertNotRegex(self.page, r'(?m)^### |^```')

    def test_the_note_that_replaces_the_old_one_points_here_too(self) -> None:
        self.assertIn(f']({prompts.HUB_PROMPTS})', prompts.NEW_NOTE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
