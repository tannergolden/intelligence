#!/usr/bin/env python3
"""Tests for the faculty copier.

WHY THIS EXISTS. `faculties.py` writes skills the hub did not author into
the kit that every machine installs, so it is the one place a release of
the template could slip in something the kit would never accept from the
hub's own hands: a file outside its folder, a binary, a skill with no
trigger test, or a faculty without the rule that hands a home copy over to
a vault's own. Its check is what keeps a hand edit to a copy out of a
release, and its pin is only worth something if it holds the release it
names. These tests pin from a throwaway template, a git repository with
release tags, into a throwaway hub, and hold each refusal and each check to
its word.

Nothing here touches the network or the hub's own kit: the one download
test hands the script a stand-in for GitHub.

Run it:

    python3 .github/scripts/test_faculties.py
"""

from __future__ import annotations

import contextlib
import http.client
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import zipfile
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


faculties = load('faculties', 'faculties.py')

NAMES = ['alpha', 'beta']
SHOULD = [f'a request alpha should answer, number {n}' for n in range(5)]
SHOULD_NOT = [f'a request that belongs elsewhere, number {n}' for n in range(5)]
IDENTITY = {'GIT_AUTHOR_NAME': 'Test', 'GIT_AUTHOR_EMAIL': 'test@example.com',
            'GIT_COMMITTER_NAME': 'Test', 'GIT_COMMITTER_EMAIL': 'test@example.com'}


def git(cwd: pathlib.Path, *args: str) -> None:
    subprocess.run(['git', '-c', 'commit.gpgsign=false', '-c', 'tag.gpgsign=false', *args], cwd=cwd,
                   env={**os.environ, **IDENTITY}, check=True, capture_output=True)


def manifest(name: str, rule: bool = True) -> str:
    """A faculty's SKILL.md, opening with the hand-over rule unless told otherwise."""
    lines = ['---', f'name: {name}', f'description: Does {name} work. Use when asked for {name}.', '---', '',
             f'# {name}', '']
    if rule:
        lines += [faculties.HANDOVER.format(name=name), '']
    return '\n'.join(lines + ['## Steps', '', 'The steps.', ''])


def trigger_evals(should: list | None = None, should_not: list | None = None, key: str = 'should_not_trigger') -> str:
    return json.dumps({'skill': 'x', 'should_trigger': SHOULD if should is None else should,
                       key: SHOULD_NOT if should_not is None else should_not})


def files_of(name: str, **extra: str | bytes) -> dict[str, str | bytes]:
    """A sound faculty's archive entries, with any added or replaced."""
    files: dict[str, str | bytes] = {f'{name}/SKILL.md': manifest(name),
                                     f'{name}/assets/trigger-evals.json': trigger_evals(),
                                     f'{name}/agents/Team.md': '# Team\n', f"{name}/agents/★ Devil's Lead.md": '# Lead\n'}
    files.update({f'{name}/{rel}': content for rel, content in extra.items()})
    return files


class Hub(unittest.TestCase):
    """A throwaway hub with an empty pin, and a throwaway template to pin from."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='faculties-test-'))
        self.hub = self.root / 'hub'
        self.template = self.root / 'template'
        self.template.mkdir()
        git(self.template, 'init', '-q')
        self.write_pin(version='', skills={})
        for name in NAMES:
            self.archive(name)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def write_pin(self, **fields: object) -> None:
        pin = {'//': 'test', 'source': 'tannergolden/knowledge', 'names': NAMES, **fields}
        path = self.hub / faculties.PIN
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(pin, indent=2) + '\n', encoding='utf-8')

    def pin(self) -> dict:
        return json.loads((self.hub / faculties.PIN).read_text(encoding='utf-8'))

    def archive(self, name: str, files: dict[str, str | bytes] | None = None) -> bytes:
        """The template's archive for one faculty, holding these entries."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as bundle:
            for rel, content in (files_of(name) if files is None else files).items():
                bundle.writestr(rel, content)
        path = self.template / 'System' / 'Skills' / f'{name}.skill'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(buffer.getvalue())
        return buffer.getvalue()

    def release(self, version: str) -> None:
        """Commit the template as it stands and tag it, as a release of it."""
        git(self.template, 'add', '-A')
        git(self.template, 'commit', '-q', '--allow-empty', '-m', version)
        git(self.template, 'tag', '-f', version)

    def pin_release(self, version: str = 'v3.0.0') -> list[str]:
        if faculties.VERSION.fullmatch(version):
            self.release(version)
        return faculties.pin_release(self.hub, version, self.template)

    def assertRefused(self, fragment: str, version: str = 'v3.0.0') -> None:
        with self.assertRaises(faculties.Refused) as caught:
            self.pin_release(version)
        self.assertIn(fragment, str(caught.exception))

    def assertProblem(self, fragment: str) -> None:
        found = faculties.problems(self.hub)
        self.assertTrue(any(fragment in line for line in found), f'no problem mentions {fragment!r}: {found}')

    def snapshot(self) -> dict[str, bytes]:
        return {p.relative_to(self.hub).as_posix(): p.read_bytes() for p in sorted(self.hub.rglob('*')) if p.is_file()}


class TestEmptyPin(Hub):
    def test_no_release_and_no_copies_pass(self) -> None:
        self.assertEqual(faculties.problems(self.hub), [])

    def test_a_faculty_with_no_release_pinned_fails(self) -> None:
        (self.hub / faculties.SKILLS / 'alpha').mkdir(parents=True)
        (self.hub / faculties.SKILLS / 'alpha' / 'SKILL.md').write_text(manifest('alpha'), encoding='utf-8')
        self.assertProblem('kit/skills/alpha: a faculty with no release pinned')

    def test_a_pin_with_no_release_records_no_skills(self) -> None:
        self.write_pin(version='', skills={'alpha': {'archive': 'x', 'files': 'y'}})
        self.assertProblem('pins no release, so it records no skills')

    def test_a_pin_of_the_wrong_shape_is_one_problem(self) -> None:
        (self.hub / faculties.PIN).write_text('{"names": "alpha"}\n', encoding='utf-8')
        self.assertEqual(len(faculties.problems(self.hub)), 1)
        self.assertProblem('needs a source, a version, a list of names and a map of skills')

    def test_a_name_that_is_not_a_skill_name_is_refused(self) -> None:
        self.write_pin(version='', skills={}, names=['../alpha'])
        self.assertProblem("'../alpha' is not a skill name")
        self.write_pin(version='', skills={'../beta': {}})
        self.assertProblem("'../beta' is not a skill name")


class TestPinning(Hub):
    def test_a_release_writes_every_copy_its_trigger_test_and_the_pin(self) -> None:
        self.assertEqual(self.pin_release(), ['kit/skills/alpha', 'kit/skills/beta'])
        for name in NAMES:
            folder = self.hub / faculties.SKILLS / name
            self.assertEqual((folder / 'SKILL.md').read_text(encoding='utf-8'), manifest(name))
            self.assertTrue((folder / 'agents' / "★ Devil's Lead.md").is_file())
            test = json.loads((self.hub / faculties.EVALS / f'{name}.json').read_text(encoding='utf-8'))
            self.assertEqual((test['skill'], test['should_trigger'], test['should_not_trigger']),
                             (name, SHOULD, SHOULD_NOT))
            self.assertGreaterEqual(test['runs'], 3)
        pin = self.pin()
        self.assertEqual(pin['version'], 'v3.0.0')
        archive = (self.template / 'System' / 'Skills' / 'alpha.skill').read_bytes()
        self.assertEqual(pin['skills']['alpha']['archive'], faculties.digest(archive))
        self.assertEqual(faculties.problems(self.hub), [])
        self.assertEqual([p.name for p in (self.hub / 'kit').iterdir() if p.name.startswith('.faculties-')], [])

    def test_a_pin_holds_the_release_tag_not_what_the_clone_has_checked_out(self) -> None:
        self.release('v3.0.0')
        self.archive('alpha', files_of('alpha', **{'references/unreleased.md': 'not in the release\n'}))
        faculties.pin_release(self.hub, 'v3.0.0', self.template)
        self.assertFalse((self.hub / faculties.SKILLS / 'alpha' / 'references').exists())

    def test_pinning_the_same_release_again_changes_no_byte(self) -> None:
        self.pin_release()
        before = self.snapshot()
        self.pin_release()
        self.assertEqual(self.snapshot(), before)

    def test_a_new_release_replaces_a_copy_whole(self) -> None:
        self.pin_release()
        self.archive('alpha', {'alpha/SKILL.md': manifest('alpha'), 'alpha/assets/trigger-evals.json': trigger_evals()})
        self.pin_release('v3.1.0')
        self.assertFalse((self.hub / faculties.SKILLS / 'alpha' / 'agents').exists(), 'a file the release dropped')
        self.assertEqual(self.pin()['version'], 'v3.1.0')
        self.assertEqual(faculties.problems(self.hub), [])

    def test_a_name_dropped_from_the_pin_takes_its_copy_and_test_with_it(self) -> None:
        self.pin_release()
        self.write_pin(**{**self.pin(), 'names': ['alpha']})
        self.pin_release()
        self.assertFalse((self.hub / faculties.SKILLS / 'beta').exists())
        self.assertFalse((self.hub / faculties.EVALS / 'beta.json').exists())
        self.assertEqual(sorted(self.pin()['skills']), ['alpha'])

    def test_routed_near_misses_and_mode_tagged_prompts_become_plain_prompts(self) -> None:
        tagged = [{'q': text, 'mode': 'ask'} for text in SHOULD]
        routed = [{'query': text, 'route': 'research'} for text in SHOULD_NOT]
        self.archive('alpha', {'alpha/SKILL.md': manifest('alpha'),
                               'alpha/assets/trigger-evals.json': trigger_evals(tagged, routed, key='near_miss')})
        self.pin_release()
        test = json.loads((self.hub / faculties.EVALS / 'alpha.json').read_text(encoding='utf-8'))
        self.assertEqual((test['should_trigger'], test['should_not_trigger']), (SHOULD, SHOULD_NOT))

    def test_line_endings_are_stored_as_git_stores_them(self) -> None:
        self.archive('alpha', files_of('alpha', **{'SKILL.md': manifest('alpha').replace('\n', '\r\n')}))
        self.pin_release()
        copy = self.hub / faculties.SKILLS / 'alpha' / 'SKILL.md'
        self.assertNotIn(b'\r\n', copy.read_bytes())
        self.assertEqual(faculties.problems(self.hub), [])
        copy.write_bytes(copy.read_bytes().replace(b'\n', b'\r\n'))  # a checkout that writes CRLF
        self.assertEqual(faculties.problems(self.hub), [])


class TestRefusals(Hub):
    def assertUntouched(self) -> None:
        self.assertFalse((self.hub / faculties.SKILLS).exists())
        self.assertFalse((self.hub / faculties.EVALS).exists())
        self.assertEqual(self.pin()['version'], '')

    def test_a_skill_the_hub_wrote_itself_is_never_replaced(self) -> None:
        own = self.hub / faculties.SKILLS / 'alpha' / 'SKILL.md'
        own.parent.mkdir(parents=True)
        own.write_text('the hub\'s own\n', encoding='utf-8')
        self.assertRefused("kit/skills/alpha is the hub's own skill")
        self.assertEqual(own.read_text(encoding='utf-8'), 'the hub\'s own\n')

    def test_a_dropped_faculty_that_is_no_longer_its_pinned_copy_is_kept(self) -> None:
        self.pin_release()
        self.write_pin(**{**self.pin(), 'names': ['alpha']})
        mine = self.hub / faculties.SKILLS / 'beta' / 'SKILL.md'
        mine.write_text('the hub now writes beta itself\n', encoding='utf-8')
        self.assertRefused('kit/skills/beta is no longer the copy v3.0.0 pinned, so it is not removed')
        self.assertEqual(mine.read_text(encoding='utf-8'), 'the hub now writes beta itself\n')
        shutil.rmtree(mine.parent)
        (self.hub / faculties.EVALS / 'beta.json').write_text('{"skill": "beta"}\n', encoding='utf-8')
        self.assertRefused('evals/skills/beta.json is no longer the trigger test beta shipped')

    def test_a_faculty_that_does_not_open_with_the_rule_is_refused(self) -> None:
        self.archive('beta', {'beta/SKILL.md': manifest('beta', rule=False),
                              'beta/assets/trigger-evals.json': trigger_evals()})
        self.assertRefused('beta at v3.0.0 does not open with the hand-over rule')
        self.assertUntouched()

    def test_the_rule_must_name_the_faculty_itself_and_come_before_its_steps(self) -> None:
        for text in (manifest('beta', rule=False).replace('## Steps', faculties.HANDOVER.format(name='alpha') +
                                                          '\n\n## Steps'),
                     manifest('beta', rule=False) + '\n' + faculties.HANDOVER.format(name='beta') + '\n'):
            with self.subTest(text=text[-80:]):
                self.archive('beta', {'beta/SKILL.md': text, 'beta/assets/trigger-evals.json': trigger_evals()})
                self.assertRefused('does not open with the hand-over rule')

    def test_a_file_outside_the_skill_folder_is_refused(self) -> None:
        for path in ('alpha/../../evil.md', '/etc/evil.md', 'other/SKILL.md', 'alpha', '.'):
            with self.subTest(path=path):
                self.archive('alpha', {'alpha/SKILL.md': manifest('alpha'), path: 'x'})
                self.assertRefused('outside the alpha/ folder')
                self.assertUntouched()

    def test_a_file_two_folders_deep_is_refused(self) -> None:
        self.archive('alpha', files_of('alpha', **{'references/deeper/x.md': 'x'}))
        self.assertRefused('more than one folder below SKILL.md')

    def test_a_name_held_both_as_a_file_and_a_folder_is_refused(self) -> None:
        self.archive('beta', files_of('beta', notes='a file', **{'notes/inner.md': 'and a folder'}))
        self.assertRefused('holds notes both as a file and as a folder')
        self.assertUntouched()

    def test_a_binary_file_is_refused(self) -> None:
        for content in (b'\x89PNG\r\n\x1a\n\xff', b'text with a NUL\x00 in it'):
            with self.subTest(content=content):
                self.archive('alpha', files_of('alpha', **{'assets/logo.png': content}))
                self.assertRefused('which is not text')

    def test_a_file_too_large_for_a_skill_is_refused(self) -> None:
        self.archive('alpha', files_of('alpha', **{'assets/big.md': 'x' * 300}))
        with mock.patch.object(faculties, 'MAX_FILE', 200):
            self.assertRefused('larger than a skill file may be')

    def test_an_archive_with_no_manifest_is_refused(self) -> None:
        self.archive('alpha', {'alpha/README.md': 'no skill here\n'})
        self.assertRefused('has no alpha/SKILL.md')

    def test_a_file_that_is_not_an_archive_is_refused(self) -> None:
        (self.template / 'System' / 'Skills' / 'alpha.skill').write_text('not a zip\n', encoding='utf-8')
        self.assertRefused('alpha.skill is not a zip archive')

    def test_a_release_without_an_archive_is_refused(self) -> None:
        (self.template / 'System' / 'Skills' / 'beta.skill').unlink()
        self.assertRefused('has no tag v3.0.0 holding System/Skills/beta.skill')
        self.assertUntouched()

    def test_a_faculty_with_no_trigger_test_or_a_broken_one_is_refused(self) -> None:
        for evals, fragment in ((None, 'alpha ships no assets/trigger-evals.json'),
                                ('[]', 'is not a JSON object'), ('{', 'is not JSON'),
                                (trigger_evals(should_not=SHOULD_NOT[:4]), 'needs at least 5 prompts each')):
            with self.subTest(fragment=fragment):
                files = {'alpha/SKILL.md': manifest('alpha')}
                if evals is not None:
                    files['alpha/assets/trigger-evals.json'] = evals
                self.archive('alpha', files)
                self.assertRefused(fragment)

    def test_a_file_git_ignores_is_refused(self) -> None:
        git(self.hub, 'init', '-q')
        (self.hub / '.gitignore').write_text('build/\n', encoding='utf-8')
        self.archive('alpha', files_of('alpha', **{'build/notes.md': 'never committed\n'}))
        self.assertRefused('git ignores kit/skills/alpha/build/notes.md')
        self.assertUntouched()

    def test_only_a_release_tag_is_a_release(self) -> None:
        for version in ('', '../main', 'Development', 'v3', 'v3.0', '3.0.0', 'v3.0.0\n', 'v3.0.0-rc.1'):
            with self.subTest(version=version):
                self.assertRefused('is not a release', version)
        self.assertUntouched()

    def test_a_failed_move_puts_every_old_copy_back(self) -> None:
        self.pin_release()
        before = self.snapshot()
        self.archive('alpha', files_of('alpha', **{'references/new.md': 'new\n'}))
        real = os.replace

        def failing(source: object, target: object) -> None:
            if pathlib.Path(str(target)) == self.hub / faculties.PIN:
                raise OSError('disk full')
            real(source, target)

        with mock.patch.object(faculties.os, 'replace', failing), self.assertRaises(OSError):
            self.pin_release('v3.1.0')
        self.assertEqual(self.snapshot(), before)
        self.assertEqual([p.name for p in (self.hub / 'kit').iterdir() if p.name.startswith('.faculties-')], [])


class TestDownload(Hub):
    def response(self, data: bytes) -> mock.MagicMock:
        response = mock.MagicMock()
        response.__enter__.return_value.read = lambda limit=-1: data
        return response

    def test_each_archive_comes_from_the_release_on_github(self) -> None:
        archives = {name: (self.template / 'System' / 'Skills' / f'{name}.skill').read_bytes() for name in NAMES}
        asked = []

        def urlopen(url: str, timeout: int = 0) -> mock.MagicMock:
            asked.append(url)
            return self.response(archives[url.rsplit('/', 1)[1][:-len('.skill')]])

        with mock.patch.object(faculties.urllib.request, 'urlopen', urlopen):
            faculties.pin_release(self.hub, 'v3.0.0')
        self.assertEqual(asked, [f'https://raw.githubusercontent.com/tannergolden/knowledge/v3.0.0/System/Skills/{name}.skill'
                                 for name in NAMES])
        self.assertEqual(faculties.problems(self.hub), [])

    def test_a_failed_download_is_refused_and_changes_nothing(self) -> None:
        for error in (urllib.error.URLError('no route'), http.client.IncompleteRead(b'part'), ValueError('bad url')):
            with self.subTest(error=type(error).__name__):
                with mock.patch.object(faculties.urllib.request, 'urlopen', side_effect=error):
                    with self.assertRaises(faculties.Refused) as caught:
                        faculties.pin_release(self.hub, 'v3.0.0')
                self.assertIn('could not download', str(caught.exception))
                self.assertFalse((self.hub / faculties.SKILLS).exists())


class TestCheck(Hub):
    def setUp(self) -> None:
        super().setUp()
        self.pin_release()

    def test_a_hand_edit_to_a_copy_fails(self) -> None:
        path = self.hub / faculties.SKILLS / 'alpha' / 'SKILL.md'
        path.write_text(path.read_text(encoding='utf-8') + 'One more step.\n', encoding='utf-8')
        self.assertProblem('kit/skills/alpha: differs from the copy v3.0.0 pinned')

    def test_a_file_added_to_a_copy_fails(self) -> None:
        (self.hub / faculties.SKILLS / 'beta' / 'references').mkdir()
        (self.hub / faculties.SKILLS / 'beta' / 'references' / 'extra.md').write_text('x\n', encoding='utf-8')
        self.assertProblem('kit/skills/beta: differs from the copy v3.0.0 pinned')

    def test_a_missing_copy_fails(self) -> None:
        shutil.rmtree(self.hub / faculties.SKILLS / 'beta')
        self.assertProblem('kit/skills/beta: missing')

    def test_a_hand_edit_to_a_trigger_test_fails(self) -> None:
        path = self.hub / faculties.EVALS / 'alpha.json'
        path.write_text(path.read_text(encoding='utf-8').replace('"runs": 3', '"runs": 1'), encoding='utf-8')
        self.assertProblem('evals/skills/alpha.json: differs from the trigger test alpha ships')

    def test_a_pin_that_forgets_a_faculty_fails(self) -> None:
        pin = self.pin()
        del pin['skills']['beta']
        self.write_pin(**pin)
        self.assertProblem('records alpha, but carries alpha, beta')

    def test_a_pin_that_names_no_release_tag_fails(self) -> None:
        self.write_pin(**{**self.pin(), 'version': 'Development'})
        self.assertProblem("'Development' is not a release")

    def test_a_reworded_rule_fails_every_copy_until_a_release_carries_it(self) -> None:
        original = faculties.HANDOVER
        faculties.HANDOVER = original.replace('read the vault', 'open the vault')
        try:
            self.assertProblem('kit/skills/alpha/SKILL.md: does not open with the hand-over rule')
            self.assertProblem('kit/skills/beta/SKILL.md: does not open with the hand-over rule')
        finally:
            faculties.HANDOVER = original

    def test_the_command_line_says_what_fails(self) -> None:
        (self.hub / faculties.EVALS / 'beta.json').unlink()
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = faculties.main(['--check', '--root', str(self.hub)])
        self.assertEqual(code, 1)
        self.assertIn('error: evals/skills/beta.json', out.getvalue())


class TestCommandLine(Hub):
    def run_main(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = faculties.main([*args, '--root', str(self.hub)])
        return code, out.getvalue()

    def test_pin_from_a_clone_prints_what_it_pinned(self) -> None:
        self.release('v3.0.0')
        code, out = self.run_main('--pin', 'v3.0.0', '--from', str(self.template))
        self.assertEqual(code, 0, out)
        self.assertIn('pinned: kit/skills/alpha', out)
        self.assertIn('Run make render, then make check', out)

    def test_a_refused_pin_says_why_and_exits_1(self) -> None:
        code, out = self.run_main('--pin', 'Development', '--from', str(self.template))
        self.assertEqual(code, 1)
        self.assertIn("error: 'Development' is not a release", out)


class TestTheRule(unittest.TestCase):
    def test_the_rule_names_both_copies_a_vault_keeps(self) -> None:
        rule = faculties.HANDOVER.format(name='research')
        self.assertIn('`.agents/skills/research/SKILL.md`', rule)
        self.assertIn('`.claude/skills/research/SKILL.md`', rule)
        self.assertIn('BRAIN vault', rule)

    def test_the_hubs_own_pin_passes_its_check(self) -> None:
        self.assertEqual(faculties.problems(faculties.ROOT), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
