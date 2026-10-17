#!/usr/bin/env python3
"""Tests for the loader probe.

WHY THIS EXISTS. The probe writes into the folders where six AI apps keep a
person's own instructions, and promises to leave every byte as it found
them, even when a run fails halfway. That promise is only worth what its
tests prove. So these run every write and every restore against a throwaway
home folder, and run whole probes against a fake app that loads the files a
real one would.

Nothing here touches your real home folder or calls a real model.

Run it:

    python3 probe/test_loader_probe.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import shlex
import shutil
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parent / 'loader-probe.py'
_spec = importlib.util.spec_from_file_location('loader_probe', SCRIPT)
probe = importlib.util.module_from_spec(_spec)
# Dataclasses look their own module up by name while the class is built.
sys.modules[_spec.name] = probe
_spec.loader.exec_module(probe)

CODES = {'PROBE_REPO': 'aaaaaaaaaaaa', 'PROBE_HOME': 'bbbbbbbbbbbb', 'PROBE_MASTER': 'cccccccccccc'}

# A stand-in for an AI app. Its second argument says what to load: paths
# starting with ~/ are under the home folder, the rest under the folder it
# runs in. Three words make it misbehave instead.
FAKE_APP = '''\
import os
import pathlib
import re
import sys
import time

home, loads = pathlib.Path(sys.argv[1]), sys.argv[2]
if loads == 'sleep':
    time.sleep(30)
if loads == 'crash':
    sys.exit('boom')
if loads == 'env':
    print('GROK_FOLDER_TRUST=' + os.environ.get('GROK_FOLDER_TRUST', 'unset'))
    sys.exit(0)
found = []
for name in loads.split(','):
    path = home / name[2:] if name.startswith('~/') else pathlib.Path(name)
    if path.exists():
        found += re.findall(r'The value of (PROBE_[A-Z]+) is ([0-9a-f]+)', path.read_text())
print('\\n'.join(key + '=' + code for key, code in found) or 'NONE')
'''


class Sandbox(unittest.TestCase):
    """A throwaway home folder and state folder for every test."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='probe-test-'))
        self.home = self.root / 'home'
        self.home.mkdir()
        self.state = self.root / 'state'
        self.manifest = probe.Manifest(self.state)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def snapshot(self) -> dict[str, bytes | None]:
        """Every file under the home folder with its bytes, and every folder."""
        return {
            path.relative_to(self.home).as_posix(): path.read_bytes() if path.is_file() else None
            for path in sorted(self.home.rglob('*'))
        }

    def personal(self, rel: str, data: bytes) -> pathlib.Path:
        """A file the person wrote, which the probe must give back intact."""
        path = self.home / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path


class TestProbeText(unittest.TestCase):
    """The text the probe plants, which a person must be able to recognise."""

    def test_a_block_carries_its_markers_name_and_code(self) -> None:
        text = probe.probe_block('PROBE_HOME', 'abc123')
        self.assertTrue(text.startswith(probe.BEGIN + '\n'))
        self.assertTrue(text.endswith(probe.END + '\n'))
        self.assertIn('The value of PROBE_HOME is abc123.', text)

    def test_copilot_gets_frontmatter_that_applies_everywhere(self) -> None:
        text = probe.home_text('copilot', 'abc123')
        self.assertTrue(text.startswith('---\napplyTo: "**"\n---\n'))
        self.assertTrue(text.endswith(probe.probe_block('PROBE_HOME', 'abc123')))

    def test_every_other_app_gets_the_bare_block(self) -> None:
        for key in ('claude', 'codex', 'antigravity'):
            self.assertEqual(probe.home_text(key, 'abc123'), probe.probe_block('PROBE_HOME', 'abc123'))


class TestInstallAndRestore(Sandbox):
    """Every write is undone to the byte."""

    def test_a_new_file_and_the_folders_made_for_it_are_removed(self) -> None:
        before = self.snapshot()
        path = self.home / '.claude' / 'rules' / 'intelligence-probe.md'
        probe.install(self.manifest, path, 'probe text\n', 'file')
        self.assertEqual(path.read_text(encoding='utf-8'), 'probe text\n')
        self.manifest.restore()
        self.assertEqual(self.snapshot(), before)

    def test_a_folder_that_was_already_there_stays(self) -> None:
        self.personal('.claude/settings.json', b'{}\n')
        before = self.snapshot()
        probe.install(self.manifest, self.home / '.claude' / 'rules' / 'x.md', 'probe\n', 'file')
        self.manifest.restore()
        self.assertEqual(self.snapshot(), before)

    def test_a_block_is_appended_and_the_original_bytes_come_back(self) -> None:
        # Windows line endings and no final newline: neither may be
        # normalised, during the run or after it.
        original = b'# Mine\r\n\r\nKeep this.'
        path = self.personal('.codex/AGENTS.md', original)
        block = probe.probe_block('PROBE_HOME', 'abc123')
        probe.install(self.manifest, path, block, 'block')
        self.assertEqual(path.read_bytes(), original + b'\n\n' + block.encode('utf-8'))
        self.manifest.restore()
        self.assertEqual(path.read_bytes(), original)

    def test_a_block_in_a_new_file_leaves_no_file_behind(self) -> None:
        before = self.snapshot()
        probe.install(self.manifest, self.home / '.agents' / 'AGENTS.md', 'probe\n', 'block')
        self.manifest.restore()
        self.assertEqual(self.snapshot(), before)

    def test_a_file_the_probe_does_not_own_is_never_overwritten(self) -> None:
        path = self.personal('.claude/rules/intelligence-probe.md', b'mine\n')
        with self.assertRaises(SystemExit):
            probe.install(self.manifest, path, 'probe\n', 'file')
        self.assertEqual(path.read_bytes(), b'mine\n')
        self.assertFalse(self.manifest.exists(), 'a refused write leaves nothing to undo')

    def test_probe_text_left_by_an_earlier_run_stops_the_write(self) -> None:
        leftover = '# Mine\n\n' + probe.probe_block('PROBE_HOME', 'old')
        path = self.personal('.codex/AGENTS.md', leftover.encode('utf-8'))
        with self.assertRaises(SystemExit):
            probe.install(self.manifest, path, probe.probe_block('PROBE_HOME', 'new'), 'block')
        self.assertEqual(path.read_text(encoding='utf-8'), leftover)

    def test_a_saved_manifest_undoes_a_run_that_died(self) -> None:
        # A run that dies leaves only its manifest. A fresh Manifest that
        # loads it must undo everything, which is what --cleanup does.
        self.personal('.codex/AGENTS.md', b'# Mine\n')
        before = self.snapshot()
        probe.install(self.manifest, self.home / '.copilot' / 'instructions' / 'x.instructions.md',
                      'probe\n', 'file')
        probe.install(self.manifest, self.home / '.codex' / 'AGENTS.md',
                      probe.probe_block('PROBE_HOME', 'abc123'), 'block')
        later = probe.Manifest(self.state)
        later.load()
        later.restore()
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(later.exists())

    def test_a_scratch_folder_is_removed_whole(self) -> None:
        scratch = pathlib.Path(tempfile.mkdtemp(prefix=probe.SCRATCH_PREFIX, dir=self.root))
        (scratch / 'plain').mkdir()
        (scratch / 'plain' / 'AGENTS.md').write_text('x\n', encoding='utf-8')
        self.manifest.remember_tree(scratch)
        self.manifest.restore()
        self.assertFalse(scratch.exists())

    def test_a_folder_the_probe_did_not_name_is_never_removed(self) -> None:
        # Whatever a damaged manifest says, a restore deletes no folder of yours.
        precious = self.home / 'projects'
        precious.mkdir()
        self.manifest.remember_tree(precious)
        self.manifest.restore()
        self.assertTrue(precious.is_dir())

    def test_replaying_a_restore_is_harmless(self) -> None:
        # A restore that dies partway keeps its manifest, so --cleanup replays
        # all of it, including the entries already put back.
        self.personal('.codex/AGENTS.md', b'# Mine\n')
        before = self.snapshot()
        probe.install(self.manifest, self.home / '.codex' / 'AGENTS.md',
                      probe.probe_block('PROBE_HOME', 'abc123'), 'block')
        probe.install(self.manifest, self.home / '.claude' / 'rules' / 'x.md', 'probe\n', 'file')
        saved = self.root / 'saved'
        shutil.copytree(self.state, saved)
        self.manifest.restore()
        shutil.rmtree(self.state)
        shutil.copytree(saved, self.state)
        again = probe.Manifest(self.state)
        again.load()
        again.restore()
        self.assertEqual(self.snapshot(), before)


class TestJudging(unittest.TestCase):
    """What counts as proof that an app read a file."""

    def test_only_a_code_counts_as_read(self) -> None:
        seen = probe.observe('PROBE_REPO=aaaaaaaaaaaa\nPROBE_HOME=wrong', CODES)
        self.assertEqual(seen, {'PROBE_REPO': True, 'PROBE_HOME': False, 'PROBE_MASTER': False})

    def test_echoing_the_question_proves_nothing(self) -> None:
        # The question names every value, and some apps print it back.
        self.assertFalse(any(probe.observe(probe.QUESTION, CODES).values()))

    def test_letter_case_does_not_matter(self) -> None:
        self.assertTrue(probe.observe('PROBE_REPO=AAAAAAAAAAAA', CODES)['PROBE_REPO'])

    def test_a_value_expected_as_none_is_not_judged(self) -> None:
        expect = {'PROBE_REPO': True, 'PROBE_HOME': None, 'PROBE_MASTER': False}
        self.assertTrue(probe.judge(expect, {'PROBE_REPO': True, 'PROBE_HOME': True, 'PROBE_MASTER': False}))
        self.assertTrue(probe.judge(expect, {'PROBE_REPO': True, 'PROBE_HOME': False, 'PROBE_MASTER': False}))
        self.assertFalse(probe.judge(expect, {'PROBE_REPO': True, 'PROBE_HOME': True, 'PROBE_MASTER': True}))


class TestPlan(unittest.TestCase):
    """Which checks run, and what each expects."""

    def test_claude_gets_a_control_and_its_fix_beside_each_file(self) -> None:
        checks = probe.plan_checks(['claude'], 'read-both.json')
        self.assertEqual([check.fixture for check in checks],
                         ['plain', 'claude-md', 'claude-md', 'claude-local', 'claude-local'])
        self.assertEqual([check.expect['PROBE_REPO'] for check in checks],
                         [True, False, True, False, True])
        for fix in (checks[2], checks[4]):
            self.assertEqual(fix.extra_args, ('--settings', 'read-both.json'))

    def test_settings_that_already_read_both_flip_the_controls(self) -> None:
        checks = probe.plan_checks(['claude'], 'read-both.json', claude_reads_both=True)
        self.assertIs(checks[1].expect['PROBE_REPO'], True)
        self.assertIs(checks[3].expect['PROBE_REPO'], True)

    def test_grok_gets_the_untrusted_folder_control(self) -> None:
        checks = probe.plan_checks(['grok'], 'read-both.json')
        self.assertEqual(len(checks), 2)
        self.assertEqual(checks[1].drop_env, ('GROK_FOLDER_TRUST',))
        self.assertIs(checks[1].expect['PROBE_REPO'], False)

    def test_an_app_with_no_home_copy_is_not_judged_on_one(self) -> None:
        (check,) = probe.plan_checks(['cursor'], 'read-both.json')
        self.assertIsNone(check.expect['PROBE_HOME'])

    def test_no_app_may_read_the_master(self) -> None:
        # One that did would load the rules twice once the kit writes its copy.
        for check in probe.plan_checks(list(probe.APPS), 'read-both.json'):
            self.assertIs(check.expect['PROBE_MASTER'], False, check.label)


class TestPlannedWrites(unittest.TestCase):
    """Which files a run writes, and how."""

    home = pathlib.Path('/home/someone')

    def writes(self, apps: list[str]) -> dict[str, str]:
        return {path.relative_to(self.home).as_posix(): mode
                for path, _, mode in probe.planned_writes(apps, self.home, CODES)}

    def test_the_master_is_always_written(self) -> None:
        self.assertEqual(self.writes(['cursor']), {'.agents/AGENTS.md': 'block'})

    def test_grok_is_probed_through_claudes_copy(self) -> None:
        self.assertIn('.claude/rules/intelligence-probe.md', self.writes(['grok']))

    def test_personal_files_get_a_block_and_folders_get_a_file(self) -> None:
        self.assertEqual(self.writes(['claude', 'codex', 'antigravity', 'copilot']), {
            '.agents/AGENTS.md': 'block',
            '.claude/rules/intelligence-probe.md': 'file',
            '.codex/AGENTS.md': 'block',
            '.gemini/AGENTS.md': 'block',
            '.copilot/instructions/intelligence-probe.instructions.md': 'file',
        })


class TestClaudeSettings(Sandbox):
    """Reading whether your own Claude settings already read both files."""

    def settings(self, text: str) -> None:
        self.personal('.claude/settings.json', text.encode('utf-8'))

    def test_no_settings_means_claude_md_only(self) -> None:
        self.assertFalse(probe.claude_reads_both(self.home))

    def test_either_plugin_id_counts(self) -> None:
        for plugin in probe.CLAUDE_PLUGIN_IDS:
            with self.subTest(plugin=plugin):
                options = {'options': {'instructionFiles': probe.READ_BOTH}}
                self.settings(json.dumps({'pluginConfigs': {plugin: options}}))
                self.assertTrue(probe.claude_reads_both(self.home))

    def test_the_settings_the_probe_passes_read_both(self) -> None:
        self.settings(json.dumps(probe.CLAUDE_READ_BOTH_SETTINGS))
        self.assertTrue(probe.claude_reads_both(self.home))

    def test_settings_of_any_shape_are_not_fatal(self) -> None:
        for text in ('{not json', '[]', '{"pluginConfigs": []}',
                     '{"pluginConfigs": {"agents-md@builtin": null}}'):
            with self.subTest(text=text):
                self.settings(text)
                self.assertFalse(probe.claude_reads_both(self.home))


class TestCommands(unittest.TestCase):
    """Replacing an app's command, and building the one that runs."""

    def test_a_command_with_a_prompt_slot_is_accepted(self) -> None:
        self.assertEqual(probe.parse_overrides(['codex=codex exec {prompt}']),
                         {'codex': 'codex exec {prompt}'})

    def test_a_bad_command_is_refused(self) -> None:
        for value in ('codex', 'codex=codex exec', 'nobody=x {prompt}'):
            with self.subTest(value=value), self.assertRaises(SystemExit):
                probe.parse_overrides([value])

    def test_the_question_fills_the_slot_and_extra_arguments_follow(self) -> None:
        check = probe.Check('claude', 'x', 'plain', {}, extra_args=('--settings', 's.json'))
        argv = probe.build_argv(probe.APPS['claude'], check, {'claude': 'claude -p "{prompt}"'})
        self.assertEqual(argv, ['claude', '-p', probe.QUESTION, '--settings', 's.json'])


class TestMatrix(unittest.TestCase):
    """The table a run prints."""

    def test_a_wrong_answer_says_what_was_expected(self) -> None:
        table = probe.matrix([{
            'check': 'Codex', 'status': 'fail',
            'expected': {'PROBE_REPO': True, 'PROBE_HOME': True, 'PROBE_MASTER': False},
            'observed': {'PROBE_REPO': True, 'PROBE_HOME': False, 'PROBE_MASTER': False},
        }])
        self.assertIn('| Codex | read | not read, expected read | not read | fail |', table)

    def test_a_row_with_no_answer_has_no_cells(self) -> None:
        table = probe.matrix([{'check': 'Cursor CLI', 'status': 'skipped'}])
        self.assertIn('| Cursor CLI | - | - | - | skipped |', table)


class TestWholeRun(Sandbox):
    """Whole probes against the fake app: the probe's own end-to-end test."""

    def setUp(self) -> None:
        super().setUp()
        self.fake = self.root / 'fake-app.py'
        self.fake.write_text(FAKE_APP, encoding='utf-8')
        self.personal('.codex/AGENTS.md', b'# My Codex notes\n')

    def command(self, app: str, loads: str) -> str:
        parts = (sys.executable, str(self.fake), str(self.home), loads)
        return app + '=' + ' '.join(shlex.quote(part) for part in parts) + ' {prompt}'

    def run_probe(self, loads: str, *extra: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = probe.main(['--apps', 'codex', '--home', str(self.home),
                               '--state', str(self.state),
                               '--command', self.command('codex', loads), *extra])
        return code, out.getvalue()

    def test_an_app_that_reads_the_right_files_passes_and_nothing_is_left(self) -> None:
        before = self.snapshot()
        code, out = self.run_probe('AGENTS.md,~/.codex/AGENTS.md')
        self.assertEqual(code, 0, out)
        self.assertIn('| Codex | read | read | not read | pass |', out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.manifest.exists())
        (results,) = self.state.glob('results-*.json')
        report = json.loads(results.read_text(encoding='utf-8'))
        self.assertEqual([row['status'] for row in report['results']], ['pass'])

    def test_an_app_that_reads_the_master_fails(self) -> None:
        code, out = self.run_probe('AGENTS.md,~/.codex/AGENTS.md,~/.agents/AGENTS.md')
        self.assertEqual(code, 1, out)
        self.assertIn('read, expected not read', out)

    def test_an_app_that_misses_its_home_copy_fails(self) -> None:
        code, out = self.run_probe('AGENTS.md')
        self.assertEqual(code, 1, out)
        self.assertIn('| Codex | read | not read, expected read |', out)

    def test_an_app_that_crashes_is_an_error_not_a_verdict(self) -> None:
        before = self.snapshot()
        code, out = self.run_probe('crash')
        self.assertEqual(code, 1, out)
        self.assertIn('| Codex | - | - | - | error |', out)
        self.assertEqual(self.snapshot(), before)

    def test_a_slow_app_times_out_and_the_files_still_come_back(self) -> None:
        before = self.snapshot()
        code, out = self.run_probe('sleep', '--timeout', '1')
        self.assertEqual(code, 1, out)
        self.assertIn('| Codex | - | - | - | timeout |', out)
        self.assertEqual(self.snapshot(), before)

    def test_a_dry_run_changes_nothing(self) -> None:
        before = self.snapshot()
        code, out = self.run_probe('AGENTS.md', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('.codex/AGENTS.md', out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.state.exists())

    def test_an_app_that_is_not_installed_touches_nothing(self) -> None:
        before = self.snapshot()
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = probe.main(['--apps', 'cursor', '--home', str(self.home),
                               '--state', str(self.state),
                               '--command', 'cursor=/nonexistent/cursor-agent -p {prompt}'])
        self.assertEqual(code, 1, out.getvalue())
        self.assertIn('None of these apps is installed', out.getvalue())
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(self.state.exists())

    def test_keep_leaves_everything_for_a_check_by_hand_until_cleanup(self) -> None:
        before = self.snapshot()
        code, out = self.run_probe('AGENTS.md', '--keep', '--apps', 'codex,cursor')
        self.assertEqual(code, 0, out)
        self.assertIn(probe.QUESTION, out)
        self.assertIn('--cleanup', out)
        self.assertIn(probe.BEGIN, (self.home / '.codex' / 'AGENTS.md').read_text(encoding='utf-8'))
        self.assertTrue(self.manifest.exists())
        manifest = probe.Manifest(self.state)
        manifest.load()
        (scratch,) = [pathlib.Path(entry['tree']) for entry in manifest.entries if entry.get('tree')]
        self.assertEqual(sorted(path.name for path in scratch.iterdir() if path.is_dir()),
                         sorted(probe.FIXTURES))
        code, out = self.run_probe('AGENTS.md', '--cleanup')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(scratch.exists())

    def test_a_leftover_manifest_blocks_a_run_until_cleanup(self) -> None:
        # A run that died right after its first write.
        before = self.snapshot()
        probe.install(self.manifest, self.home / '.codex' / 'AGENTS.md',
                      probe.probe_block('PROBE_HOME', 'c0ffee'), 'block')
        code, out = self.run_probe('AGENTS.md,~/.codex/AGENTS.md')
        self.assertEqual(code, 2, out)
        self.assertIn('--cleanup', out)
        code, out = self.run_probe('AGENTS.md', '--cleanup')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)
        code, out = self.run_probe('AGENTS.md,~/.codex/AGENTS.md')
        self.assertEqual(code, 0, out)

    def test_grok_is_trusted_everywhere_but_its_untrusted_control(self) -> None:
        trusted, untrusted = probe.plan_checks(['grok'], 'read-both.json')
        overrides = probe.parse_overrides([self.command('grok', 'env')])
        outputs = [probe.run_check(probe.APPS['grok'], check, self.root, CODES, overrides, 60)['output']
                   for check in (trusted, untrusted)]
        self.assertEqual(outputs, ['GROK_FOLDER_TRUST=0', 'GROK_FOLDER_TRUST=unset'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
