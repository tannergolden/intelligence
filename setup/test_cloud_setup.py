#!/usr/bin/env python3
"""Tests for the Claude cloud setup script.

WHY THIS EXISTS. The setup script runs before every Claude cloud session,
and a setup script that exits non-zero stops the session from starting. So
it has two promises to keep: install the pinned rules when everything checks
out, and exit 0, having changed nothing, when anything does not. These run
the real script with bash against a stand-in for the release, served from a
local folder, and a throwaway home folder.

Nothing here touches your real home folder or the network.

Run it:

    python3 setup/test_cloud_setup.py
"""

from __future__ import annotations

import hashlib
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPT = HERE / 'claude-cloud-setup.sh'
HOME_FILE = ROOT / 'home' / 'intelligence.md'
INSTALLER = ROOT / 'scripts' / 'install.py'


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CloudSetup(unittest.TestCase):
    """A fake release under file://, a fake home, and the real script."""

    version = 'v9.9.9'

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='cloud-setup-test-'))
        self.home = self.root / 'home'
        self.home.mkdir()
        release = self.root / 'release' / self.version
        (release / 'home').mkdir(parents=True)
        (release / 'scripts').mkdir()
        shutil.copy(HOME_FILE, release / 'home' / 'intelligence.md')
        shutil.copy(INSTALLER, release / 'scripts' / 'install.py')

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def script(self, version: str | None = None, home_sha: str | None = None,
               install_sha: str | None = None) -> pathlib.Path:
        """The setup script with its pins filled in, the way `make cloud-setup` fills them."""
        text = SCRIPT.read_text(encoding='utf-8')
        if version is not None:
            text = (text.replace("VERSION='@VERSION@'", f"VERSION='{version}'")
                    .replace("HOME_SHA256='@HOME_SHA256@'", f"HOME_SHA256='{home_sha}'")
                    .replace("INSTALL_SHA256='@INSTALL_SHA256@'", f"INSTALL_SHA256='{install_sha}'"))
        path = self.root / 'setup.sh'
        path.write_text(text, encoding='utf-8')
        return path

    def run_script(self, path: pathlib.Path) -> subprocess.CompletedProcess[str]:
        env = {key: value for key, value in os.environ.items()
               if key not in ('XDG_STATE_HOME', 'CODEX_HOME')}
        env['HOME'] = str(self.home)
        env['INTELLIGENCE_BASE'] = (self.root / 'release').as_uri()
        return subprocess.run(['bash', str(path)], env=env, capture_output=True, text=True, timeout=120,
                              check=False)

    def claude_md(self) -> pathlib.Path:
        return self.home / '.claude' / 'CLAUDE.md'

    def test_a_pinned_release_is_installed(self) -> None:
        done = self.run_script(self.script(self.version, sha256(HOME_FILE), sha256(INSTALLER)))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.claude_md().read_bytes(), HOME_FILE.read_bytes())

    def test_running_it_twice_changes_nothing(self) -> None:
        path = self.script(self.version, sha256(HOME_FILE), sha256(INSTALLER))
        self.run_script(path)
        before = self.claude_md().read_bytes()
        done = self.run_script(path)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.claude_md().read_bytes(), before)

    def test_unfilled_pins_install_nothing_and_still_exit_zero(self) -> None:
        done = self.run_script(self.script())
        self.assertEqual(done.returncode, 0)
        self.assertIn('no release is pinned', done.stderr)
        self.assertFalse(self.claude_md().exists())

    def test_a_home_file_that_misses_its_pin_is_not_installed(self) -> None:
        done = self.run_script(self.script(self.version, '0' * 64, sha256(INSTALLER)))
        self.assertEqual(done.returncode, 0)
        self.assertIn('does not match its pin', done.stderr)
        self.assertFalse(self.claude_md().exists())

    def test_an_installer_that_misses_its_pin_is_never_run(self) -> None:
        done = self.run_script(self.script(self.version, sha256(HOME_FILE), '0' * 64))
        self.assertEqual(done.returncode, 0)
        self.assertIn('installer', done.stderr)
        self.assertFalse(self.claude_md().exists())

    def test_a_release_that_cannot_be_downloaded_still_exits_zero(self) -> None:
        done = self.run_script(self.script('v0.0.0', sha256(HOME_FILE), sha256(INSTALLER)))
        self.assertEqual(done.returncode, 0)
        self.assertIn('could not download', done.stderr)
        self.assertFalse(self.claude_md().exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
