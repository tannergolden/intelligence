#!/usr/bin/env python3
"""Tests for the home kit installer.

WHY THIS EXISTS. `install.py` writes into the folders where a person keeps
their own instructions and settings for six apps, and promises two things:
it never overwrites a file it does not own, and `uninstall` puts back
exactly what was there before. Both promises are only as good as these
tests, which run every command against a throwaway home folder and compare
the result to the byte.

Nothing here touches your real home folder.

Run it:

    python3 scripts/test_install.py
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

HERE = pathlib.Path(__file__).resolve().parent


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name while the class is built.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


install = load('install', 'install.py')
render = load('render', 'render.py')

BLOCK = '## Working rules\n\n- SEC-001: Never put a credential in a file.\n'
NEWER = '## Working rules\n\n- SEC-001: Never put a credential anywhere.\n'

LOCAL = {
    '.agents/AGENTS.md': 'block',
    '.claude/rules/intelligence.md': 'file',
    '.codex/AGENTS.md': 'block',
    '.gemini/AGENTS.md': 'block',
    '.copilot/instructions/intelligence.instructions.md': 'file',
}


class Home(unittest.TestCase):
    """A throwaway home folder, and a home file rendered the way the hub renders it."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='install-test-'))
        self.home = self.root / 'home'
        self.home.mkdir()
        self.env: dict[str, str] = {}
        self.home_file = self.make_home_file(BLOCK)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def make_home_file(self, block: str, name: str = 'intelligence.md') -> pathlib.Path:
        path = self.root / name
        path.write_text(render.region(block), encoding='utf-8')
        return path

    def run_kit(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        command, rest = args[0], list(args[1:])
        argv = [command, '--home', str(self.home), *rest]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = install.main(argv, env=self.env)
        return code, out.getvalue()

    def snapshot(self) -> dict[str, bytes | None]:
        # The install record lives under ~/.local, so it is left out.
        return {path.relative_to(self.home).as_posix(): path.read_bytes() if path.is_file() else None
                for path in sorted(self.home.rglob('*'))
                if path.relative_to(self.home).parts[0] != '.local'}

    def personal(self, rel: str, data: bytes) -> pathlib.Path:
        path = self.home / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def text(self, rel: str) -> str:
        return (self.home / rel).read_text(encoding='utf-8')


class TestInstall(Home):
    """What a first install writes."""

    def test_every_local_copy_is_written(self) -> None:
        code, out = self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(code, 0, out)
        region = render.region(BLOCK)
        for rel in LOCAL:
            with self.subTest(rel=rel):
                text = self.text(rel)
                if rel.startswith('.copilot'):
                    self.assertEqual(text, install.COPILOT_PREFIX + region)
                else:
                    self.assertEqual(text, region)
        self.assertFalse((self.home / '.claude' / 'CLAUDE.md').exists())
        self.assertIn('Cursor', out)

    def test_claude_reads_agents_md_beside_claude_md(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        settings = json.loads(self.text('.claude/settings.json'))
        for plugin in install.PLUGIN_IDS:
            self.assertEqual(settings['pluginConfigs'][plugin]['options']['instructionFiles'],
                             install.READ_BOTH)

    def test_your_own_notes_stay_and_the_block_follows_them(self) -> None:
        self.personal('.codex/AGENTS.md', b'# My Codex notes\n')
        self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(self.text('.codex/AGENTS.md'), '# My Codex notes\n\n' + render.region(BLOCK))

    def test_a_second_install_changes_nothing(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        before = self.snapshot()
        code, out = self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)
        self.assertNotIn('wrote', out)

    def test_a_new_release_replaces_the_block_in_place(self) -> None:
        self.personal('.codex/AGENTS.md', b'# Mine\n')
        self.run_kit('install', '--home-file', str(self.home_file))
        self.personal('.codex/AGENTS.md', self.text('.codex/AGENTS.md').encode() + b'\n## Added later\n')
        newer = self.make_home_file(NEWER, 'newer.md')
        self.run_kit('install', '--home-file', str(newer))
        self.assertEqual(self.text('.codex/AGENTS.md'),
                         '# Mine\n\n' + render.region(NEWER) + '\n## Added later\n')

    def test_a_file_the_kit_does_not_own_is_never_overwritten(self) -> None:
        path = self.personal('.claude/rules/intelligence.md', b'my own rules\n')
        code, out = self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(code, 1, out)
        self.assertIn('refused', out)
        self.assertEqual(path.read_bytes(), b'my own rules\n')
        self.assertEqual(self.text('.codex/AGENTS.md'), render.region(BLOCK), 'the rest still installs')

    def test_settings_of_your_own_survive_the_merge(self) -> None:
        self.personal('.claude/settings.json', json.dumps({'theme': 'dark', 'pluginConfigs': {
            'other@builtin': {'options': {'x': 1}}}}).encode())
        self.run_kit('install', '--home-file', str(self.home_file))
        settings = json.loads(self.text('.claude/settings.json'))
        self.assertEqual(settings['theme'], 'dark')
        self.assertEqual(settings['pluginConfigs']['other@builtin'], {'options': {'x': 1}})

    def test_settings_that_are_not_json_are_never_overwritten(self) -> None:
        path = self.personal('.claude/settings.json', b'{ not json')
        code, out = self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(code, 1, out)
        self.assertEqual(path.read_bytes(), b'{ not json')

    def test_a_cloud_session_gets_claude_md_and_nothing_else(self) -> None:
        code, out = self.run_kit('install', '--home-file', str(self.home_file), '--cloud')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.text('.claude/CLAUDE.md'), render.region(BLOCK))
        self.assertEqual(sorted(self.snapshot()), ['.claude', '.claude/CLAUDE.md'])

    def test_codex_home_is_respected(self) -> None:
        self.env['CODEX_HOME'] = str(self.root / 'codex-home')
        (self.root / 'codex-home').mkdir()
        self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual((self.root / 'codex-home' / 'AGENTS.md').read_text(encoding='utf-8'),
                         render.region(BLOCK))
        self.assertFalse((self.home / '.codex').exists())

    def test_a_dry_run_changes_nothing(self) -> None:
        self.personal('.codex/AGENTS.md', b'# Mine\n')
        before = self.snapshot()
        code, out = self.run_kit('install', '--home-file', str(self.home_file), '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('would write', out)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.home / '.local').exists())

    def test_a_file_that_would_hide_a_copy_is_reported(self) -> None:
        self.personal('.codex/AGENTS.override.md', b'override\n')
        _code, out = self.run_kit('install', '--home-file', str(self.home_file))
        self.assertIn('AGENTS.override.md exists', out)

    def test_an_edited_home_file_is_refused(self) -> None:
        self.home_file.write_text(render.region(BLOCK).replace('file.', 'drawer.'), encoding='utf-8')
        with self.assertRaises(SystemExit):
            self.run_kit('install', '--home-file', str(self.home_file))
        self.assertEqual(self.snapshot(), {})

    def test_anything_but_one_block_is_not_a_home_file(self) -> None:
        self.home_file.write_text('# Not a home file\n' + render.region(BLOCK), encoding='utf-8')
        with self.assertRaises(SystemExit):
            self.run_kit('install', '--home-file', str(self.home_file))


class TestUninstall(Home):
    """Everything goes back to the byte."""

    def test_a_clean_home_is_clean_again(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), {})
        self.assertFalse((self.home / '.local' / 'state' / 'intelligence').exists())

    def test_personal_files_and_settings_come_back_exactly(self) -> None:
        originals = {
            '.codex/AGENTS.md': b'# Mine\r\nNo final newline',
            '.gemini/AGENTS.md': b'# Gemini notes\n',
            '.agents/AGENTS.md': b'',
        }
        for rel, data in originals.items():
            self.personal(rel, data)
        prior = {'options': {'instructionFiles': 'agents-md'}}
        settings = {'theme': 'dark', 'pluginConfigs': {'agents-md@builtin': prior}}
        self.personal('.claude/settings.json', json.dumps(settings).encode())
        self.run_kit('install', '--home-file', str(self.home_file))
        newer = self.make_home_file(NEWER, 'newer.md')
        self.run_kit('install', '--home-file', str(newer))
        self.run_kit('uninstall')
        for rel, data in originals.items():
            with self.subTest(rel=rel):
                self.assertEqual((self.home / rel).read_bytes(), data)
        self.assertEqual(json.loads(self.text('.claude/settings.json')), settings)
        self.assertFalse((self.home / '.claude' / 'rules').exists())
        self.assertFalse((self.home / '.copilot').exists())

    def test_without_a_record_only_the_kits_own_text_goes(self) -> None:
        self.personal('.codex/AGENTS.md', b'# Mine\n')
        self.run_kit('install', '--home-file', str(self.home_file))
        (self.home / '.local' / 'state' / 'intelligence' / 'install.json').unlink()
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        self.assertIn('no install record', out)
        self.assertEqual(self.text('.codex/AGENTS.md'), '# Mine\n')
        self.assertFalse((self.home / '.claude' / 'rules' / 'intelligence.md').exists())
        self.assertFalse((self.home / '.agents' / 'AGENTS.md').exists())

    def test_a_dry_run_uninstall_changes_nothing(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        before = self.snapshot()
        code, out = self.run_kit('uninstall', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)


class TestCheck(Home):
    """`check` reports every copy against the release."""

    def test_a_fresh_install_checks_clean(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        code, out = self.run_kit('check', '--home-file', str(self.home_file))
        self.assertEqual(code, 0, out)
        self.assertNotIn('missing', out)

    def test_nothing_installed_is_reported_missing(self) -> None:
        code, out = self.run_kit('check', '--home-file', str(self.home_file))
        self.assertEqual(code, 1, out)
        self.assertIn('missing', out)

    def test_a_hand_edit_is_reported(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        path = self.home / '.gemini' / 'AGENTS.md'
        path.write_text(path.read_text(encoding='utf-8').replace('file.', 'drawer.'), encoding='utf-8')
        code, out = self.run_kit('check', '--home-file', str(self.home_file))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r'edited +Antigravity CLI')

    def test_an_older_release_is_reported_stale(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        newer = self.make_home_file(NEWER, 'newer.md')
        code, out = self.run_kit('check', '--home-file', str(newer))
        self.assertEqual(code, 1, out)
        self.assertIn('stale', out)

    def test_a_lost_setting_is_reported(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file))
        (self.home / '.claude' / 'settings.json').write_text('{}\n', encoding='utf-8')
        code, out = self.run_kit('check', '--home-file', str(self.home_file))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r'missing +Claude Code setting')

    def test_a_cloud_session_checks_only_claude_md(self) -> None:
        self.run_kit('install', '--home-file', str(self.home_file), '--cloud')
        code, out = self.run_kit('check', '--home-file', str(self.home_file), '--cloud')
        self.assertEqual(code, 0, out)


if __name__ == '__main__':
    unittest.main(verbosity=2)
