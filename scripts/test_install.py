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
import hashlib
import importlib.util
import io
import json
import pathlib
import shutil
import subprocess
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
kit = load('kit', 'kit.py')

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


FACTS = '## Facts about this setup\n\n- Every repository has one maintainer.\n'


def old_knowledge(block: str) -> str:
    """A facts block as releases before kit format 2 wrote it beside the rules."""
    digest = hashlib.sha256(block.encode('utf-8')).hexdigest()
    return f'<!-- INTELLIGENCE:KNOWLEDGE:BEGIN sha256:{digest} -->\n\n{block}\n<!-- INTELLIGENCE:KNOWLEDGE:END -->\n'


GUARD = f'#!/usr/bin/env python3\n# {kit.OWNED}\nimport sys\nprint("blocked", file=sys.stderr)\nsys.exit(2)\n'
SKILL = '---\nname: building-skills\ndescription: Builds skills. Use when asked.\n---\n\n# Building skills\n'
AGENT = kit.render_subagent('worker', 'Does one change. Use for small tasks.', ['read', 'edit'], 'Work.\n')

KIT_LOCAL = [
    '.agents/hooks/intelligence-guard.py',
    '.agents/skills/building-skills/SKILL.md',
    '.claude/agents/worker.md',
    '.claude/skills/building-skills/SKILL.md',
    '.codex/agents/worker.toml',
    '.codex/hooks.json',
    '.copilot/agents/worker.agent.md',
    '.copilot/hooks/intelligence.json',
    '.gemini/antigravity-cli/skills/building-skills/SKILL.md',
    '.gemini/config/hooks.json',
]


class KitHome(Home):
    """A throwaway home, a home file, and a kit rendered the way the hub renders one."""

    def setUp(self) -> None:
        super().setUp()
        self.kit_file = self.make_kit()

    def make_kit(self, name: str = 'kit.json', **changes: object) -> pathlib.Path:
        data = {'format': 2, 'guard': GUARD,
                'skills': {'building-skills': {'SKILL.md': SKILL, 'references/notes.md': 'Notes.\n'}},
                'subagents': {'worker': AGENT}}
        data.update(changes)
        path = self.root / name
        path.write_text(json.dumps(data), encoding='utf-8')
        return path

    def install_kit(self, *extra: str) -> tuple[int, str]:
        return self.run_kit('install', '--home-file', str(self.home_file), '--kit-file', str(self.kit_file),
                            *extra)

    def check_kit(self, *extra: str) -> tuple[int, str]:
        return self.run_kit('check', '--home-file', str(self.home_file), '--kit-file', str(self.kit_file),
                            *extra)

    def json(self, rel: str) -> dict:
        return json.loads(self.text(rel))


class TestKitInstall(KitHome):
    """What a first install with the kit writes, and where."""

    def test_every_piece_lands_where_its_app_reads_it(self) -> None:
        code, out = self.install_kit()
        self.assertEqual(code, 0, out)
        for rel in KIT_LOCAL:
            with self.subTest(rel=rel):
                self.assertTrue((self.home / rel).is_file())
        guard = self.home / '.agents' / 'hooks' / 'intelligence-guard.py'
        self.assertEqual(guard.read_text(encoding='utf-8'), GUARD)
        self.assertEqual(guard.stat().st_mode & 0o777, 0o755)
        self.assertEqual(self.text('.claude/agents/worker.md'), AGENT['claude'])
        self.assertEqual(self.text('.codex/agents/worker.toml'), AGENT['codex'])
        self.assertTrue((self.home / '.claude/skills/building-skills' / install.SKILL_MARK).is_file())
        self.assertEqual(self.text('.claude/skills/building-skills/references/notes.md'), 'Notes.\n')

    def test_the_guard_is_registered_for_every_app(self) -> None:
        self.install_kit()
        claude = self.json('.claude/settings.json')['hooks']['PreToolUse'][-1]
        self.assertEqual(claude['matcher'], install.CLAUDE_MATCHER)
        self.assertEqual(claude['hooks'][0]['onFailure'], 'block')
        self.assertTrue(claude['hooks'][0]['command'].endswith('intelligence-guard.py --app claude'))
        codex = self.json('.codex/hooks.json')['hooks']['PreToolUse'][-1]
        self.assertEqual(codex['matcher'], install.CODEX_MATCHER)
        copilot = self.json('.copilot/hooks/intelligence.json')
        self.assertEqual(copilot['version'], 1)
        self.assertIn('--app copilot', copilot['hooks']['PreToolUse'][0]['hooks'][0]['command'])
        antigravity = self.json('.gemini/config/hooks.json')['intelligence']
        self.assertIn('--app antigravity', antigravity['PreToolUse'][0]['hooks'][0]['command'])

    def test_the_registered_command_runs_the_guard(self) -> None:
        self.install_kit()
        command = self.json('.claude/settings.json')['hooks']['PreToolUse'][-1]['hooks'][0]['command']
        # Through a shell, exactly as Claude Code runs a hook command.
        done = subprocess.run(command, shell=True, input='{}', capture_output=True, text=True,  # noqa: S602
                              check=False)
        self.assertEqual(done.returncode, 2, done.stderr)
        self.assertIn('blocked', done.stderr)

    def test_your_own_hooks_keep_their_place(self) -> None:
        mine = {'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': 'my-check'}]}
        self.personal('.claude/settings.json', json.dumps({'hooks': {'PreToolUse': [mine]}}).encode())
        self.personal('.codex/hooks.json', json.dumps({'hooks': {'PreToolUse': [mine], 'Stop': [mine]}}).encode())
        self.install_kit()
        self.install_kit()
        for rel in ('.claude/settings.json', '.codex/hooks.json'):
            with self.subTest(rel=rel):
                groups = self.json(rel)['hooks']['PreToolUse']
                self.assertEqual(len(groups), 2, 'installed twice, registered once')
                self.assertEqual(groups[0], mine, 'appended after yours')
        self.assertEqual(self.json('.codex/hooks.json')['hooks']['Stop'], [mine])

    def test_a_changed_registration_is_replaced_where_it_stands(self) -> None:
        mine = {'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': 'my-check'}]}
        self.install_kit()
        data = self.json('.codex/hooks.json')
        data['hooks']['PreToolUse'][0]['hooks'][0]['command'] = '/old/python3 /x/intelligence-guard.py --app codex'
        data['hooks']['PreToolUse'].append(mine)
        self.personal('.codex/hooks.json', json.dumps(data).encode())
        self.install_kit()
        groups = self.json('.codex/hooks.json')['hooks']['PreToolUse']
        self.assertEqual(len(groups), 2)
        self.assertNotIn('/old/', groups[0]['hooks'][0]['command'], 'Codex trusts a hook by its position')
        self.assertEqual(groups[1], mine)

    def test_a_second_install_changes_nothing(self) -> None:
        self.install_kit()
        before = self.snapshot()
        code, out = self.install_kit()
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)
        self.assertNotIn('wrote', out)

    def test_a_new_release_replaces_what_it_changed(self) -> None:
        self.install_kit()
        self.kit_file = self.make_kit('newer.json', skills={'building-skills': {'SKILL.md': SKILL}})
        self.install_kit()
        self.assertFalse((self.home / '.claude/skills/building-skills/references').exists(),
                         'a file the release dropped goes')

    def test_a_dry_run_changes_nothing(self) -> None:
        before = self.snapshot()
        code, out = self.install_kit('--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('would write', out)
        self.assertEqual(self.snapshot(), before)

    def test_a_cloud_session_gets_only_claude_codes_share(self) -> None:
        code, out = self.install_kit('--cloud')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.text('.claude/CLAUDE.md'), render.region(BLOCK))
        files = sorted(rel for rel, data in self.snapshot().items() if data is not None)
        self.assertEqual(files, ['.agents/hooks/intelligence-guard.py', '.claude/CLAUDE.md',
                                 '.claude/agents/worker.md', '.claude/settings.json',
                                 '.claude/skills/building-skills/.intelligence-kit',
                                 '.claude/skills/building-skills/SKILL.md',
                                 '.claude/skills/building-skills/references/notes.md'])
        self.assertNotIn('pluginConfigs', self.json('.claude/settings.json'))
        code, out = self.check_kit('--cloud')
        self.assertEqual(code, 0, out)


class TestKitRefusals(KitHome):
    """What is not the kit's stays exactly as it is."""

    def test_folders_files_and_hooks_of_your_own_are_never_overwritten(self) -> None:
        skill = self.personal('.claude/skills/building-skills/SKILL.md', b'my own skill\n')
        agent = self.personal('.claude/agents/worker.md', b'my own worker\n')
        named = self.personal('.gemini/config/hooks.json', json.dumps({'intelligence': {'Stop': []}}).encode())
        jsonc = self.personal('.codex/hooks.json', b'{ // my hooks\n}')
        code, out = self.install_kit()
        self.assertEqual(code, 1, out)
        self.assertEqual(out.count('refused'), 4, out)
        self.assertEqual(skill.read_bytes(), b'my own skill\n')
        self.assertEqual(agent.read_bytes(), b'my own worker\n')
        self.assertEqual(json.loads(named.read_text(encoding='utf-8')), {'intelligence': {'Stop': []}})
        self.assertEqual(jsonc.read_bytes(), b'{ // my hooks\n}')
        self.assertTrue((self.home / '.agents/skills/building-skills/SKILL.md').is_file(), 'the rest installs')

    def test_a_kit_that_reaches_outside_its_folders_is_refused(self) -> None:
        for change in ({'skills': {'x': {'../../.bashrc': 'evil'}}},
                       {'subagents': {'../worker': AGENT}},
                       {'guard': 'print("no mark")\n'},
                       {'format': 1}):
            with self.subTest(change=list(change)):
                self.kit_file = self.make_kit('bad.json', **change)
                with self.assertRaises(SystemExit):
                    self.install_kit()
                self.assertEqual(self.snapshot(), {})


class TestKitUninstall(KitHome):
    """Everything the kit added goes, and everything that was yours comes back to the byte."""

    def test_a_clean_home_is_clean_again(self) -> None:
        self.install_kit()
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), {})

    def test_your_own_files_settings_and_hooks_come_back_exactly(self) -> None:
        mine = {'matcher': 'Bash', 'hooks': [{'type': 'command', 'command': 'my-check'}]}
        originals = {
            '.codex/AGENTS.md': b'# Mine\r\nNo final newline',
            '.claude/settings.json': json.dumps({'theme': 'dark', 'hooks': {'PreToolUse': [mine]}}).encode(),
            '.codex/hooks.json': json.dumps({'hooks': {'Stop': [mine]}}).encode(),
            '.gemini/config/hooks.json': json.dumps({'mine': {'Stop': [mine]}}).encode(),
            '.claude/agents/helper.md': b'---\nname: helper\n---\nMine.\n',
            '.claude/skills/my-skill/SKILL.md': b'---\nname: my-skill\n---\n',
        }
        for rel, data in originals.items():
            self.personal(rel, data)
        self.install_kit()
        self.kit_file = self.make_kit('newer.json', skills={'building-skills': {'SKILL.md': SKILL}})
        self.install_kit()
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        for rel, data in originals.items():
            with self.subTest(rel=rel):
                if rel.endswith('.json'):
                    self.assertEqual(json.loads((self.home / rel).read_bytes()), json.loads(data))
                else:
                    self.assertEqual((self.home / rel).read_bytes(), data)
        left = sorted(rel for rel, data in self.snapshot().items() if data is not None)
        self.assertEqual(left, sorted(originals))

    def test_without_a_record_only_what_carries_the_kits_mark_goes(self) -> None:
        self.personal('.claude/agents/helper.md', b'mine\n')
        self.install_kit()
        (self.home / '.local' / 'state' / 'intelligence' / 'install.json').unlink()
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        left = sorted(rel for rel, data in self.snapshot().items() if data is not None)
        # With no record of what existed before, shared hook files keep everything but the guard.
        self.assertEqual(left, ['.claude/agents/helper.md', '.claude/settings.json', '.codex/hooks.json',
                                '.gemini/config/hooks.json'])
        for rel in left[1:]:
            with self.subTest(rel=rel):
                self.assertNotIn(install.GUARD_NAME, self.text(rel))

    def test_a_dry_run_uninstall_changes_nothing(self) -> None:
        self.install_kit()
        before = self.snapshot()
        code, out = self.run_kit('uninstall', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.snapshot(), before)


class TestKitCheck(KitHome):
    """`check` reports each piece of the kit against the release."""

    def test_a_fresh_install_checks_clean(self) -> None:
        self.install_kit()
        code, out = self.check_kit()
        self.assertEqual(code, 0, out)

    def test_hand_edits_and_lost_registrations_are_reported(self) -> None:
        self.install_kit()
        skill = self.home / '.agents/skills/building-skills/SKILL.md'
        skill.write_text(SKILL + 'extra\n', encoding='utf-8')
        (self.home / '.gemini/config/hooks.json').write_text('{}\n', encoding='utf-8')
        (self.home / '.claude/agents/worker.md').unlink()
        code, out = self.check_kit()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r'edited +the shared skills folder skill building-skills')
        self.assertRegex(out, r'missing +Antigravity CLI guard hook')
        self.assertRegex(out, r'missing +Claude Code subagent worker')

    def test_a_registration_whose_python_is_gone_is_broken(self) -> None:
        self.install_kit()
        data = self.json('.claude/settings.json')
        data['hooks']['PreToolUse'][-1]['hooks'][0]['command'] = (
            '/nowhere/python3 ' + str(self.home / install.GUARD) + ' --app claude')
        self.personal('.claude/settings.json', json.dumps(data).encode())
        code, out = self.check_kit()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r'broken +Claude Code guard hook')



class TestRetiredKnowledge(KitHome):
    """The facts an earlier release wrote beside the rules come out at the next install."""

    def plant(self) -> dict[str, pathlib.Path]:
        """A home as an earlier release left it: its facts beside the rules, and its record of them."""
        self.personal('.codex/AGENTS.md', b'# My Codex notes\n')
        self.install_kit()
        facts = old_knowledge(FACTS)
        codex = self.home / '.codex' / 'AGENTS.md'
        codex.write_text(codex.read_text(encoding='utf-8') + '\n' + facts, encoding='utf-8')
        claude = self.personal('.claude/rules/intelligence-knowledge.md', facts.encode())
        copilot = self.personal('.copilot/instructions/intelligence-knowledge.instructions.md',
                                (install.COPILOT_PREFIX + facts).encode())
        spath = install.state_path(self.home, self.env)
        state = json.loads(spath.read_text(encoding='utf-8'))
        for path, mode in ((codex, 'block'), (claude, 'file'), (copilot, 'file')):
            state['files'][f'{path}#knowledge'] = {
                'path': str(path), 'piece': 'knowledge', 'mode': mode, 'created': mode == 'file',
                'joiner': '\n' if mode == 'block' else '', 'dirs': []}
        state['knowledge_hash'] = 'f' * 64
        spath.write_text(json.dumps(state), encoding='utf-8')
        return {'codex': codex, 'claude': claude, 'copilot': copilot}

    def test_an_install_takes_out_every_block_and_file(self) -> None:
        planted = self.plant()
        code, out = self.install_kit()
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r'retired +Codex knowledge')
        self.assertEqual(self.text('.codex/AGENTS.md'), f'# My Codex notes\n\n{render.region(BLOCK)}')
        self.assertFalse(planted['claude'].exists())
        self.assertFalse(planted['copilot'].exists())
        state = json.loads(install.state_path(self.home, self.env).read_text(encoding='utf-8'))
        self.assertEqual([key for key in state['files'] if key.endswith('#knowledge')], [])
        self.assertNotIn('knowledge_hash', state)

    def test_a_dry_run_takes_nothing_out(self) -> None:
        self.plant()
        before = self.snapshot()
        code, out = self.install_kit('--dry-run')
        self.assertEqual(code, 0, out)
        self.assertRegex(out, r'would retire +Codex knowledge')
        self.assertEqual(self.snapshot(), before)

    def test_check_calls_a_block_left_behind_stale_until_an_install(self) -> None:
        self.plant()
        code, out = self.check_kit()
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r'stale +Codex knowledge')
        self.install_kit()
        code, out = self.check_kit()
        self.assertEqual(code, 0, out)

    def test_an_uninstall_takes_them_out_too(self) -> None:
        self.plant()
        code, out = self.run_kit('uninstall')
        self.assertEqual(code, 0, out)
        self.assertEqual(self.text('.codex/AGENTS.md'), '# My Codex notes\n')
        self.assertFalse((self.home / '.claude/rules/intelligence-knowledge.md').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
