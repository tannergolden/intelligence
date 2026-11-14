#!/usr/bin/env python3
"""Tests for the kit renderer.

WHY THIS EXISTS. `kit.py` is the last check the guard passes before every
machine installs it. A guard without the kit's mark is one the installer
can never replace, and a kit that names a private repository publishes it.
These tests hold the source to those rules, and the bundle to the one shape
the installer reads.

Run it:

    python3 .github/scripts/test_kit.py
"""

from __future__ import annotations

import importlib.util
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
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


kit = load('kit', 'kit.py')

GUARD = f'#!/usr/bin/env python3\n# {kit.OWNED}\nprint("guard")\n'


class Hub(unittest.TestCase):
    """A throwaway hub holding a guard."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='kit-test-'))
        self.write('kit/guard.py', GUARD)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel: str, text: str) -> pathlib.Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def problems(self) -> list[str]:
        return kit.problems(self.root)

    def assertProblem(self, fragment: str) -> None:
        found = self.problems()
        self.assertTrue(any(fragment in line for line in found), f'no problem mentions {fragment!r}: {found}')


class TestSound(Hub):
    def test_a_sound_hub_has_no_problems(self) -> None:
        self.assertEqual(self.problems(), [])

    def test_the_bundle_is_deterministic_json(self) -> None:
        first = kit.render_kit(self.root)
        self.assertEqual(first, kit.render_kit(self.root))
        data = json.loads(first)
        self.assertEqual(sorted(data), ['//', 'format', 'guard'])
        self.assertEqual(data['format'], kit.FORMAT)
        self.assertEqual(data['guard'], GUARD)


class TestTheGuard(Hub):
    """What holds for the guard, the one file the kit carries."""

    def test_a_guard_without_the_kits_mark_is_refused(self) -> None:
        self.write('kit/guard.py', 'print("guard")\n')
        self.assertProblem('must carry the line')

    def test_a_private_repository_is_never_named(self) -> None:
        self.write('kit/guard.py', GUARD + '# The secrets live in tannergolden/vault.\n')
        self.assertProblem('tannergolden/vault')
        self.write('kit/guard.py', GUARD + '# The rules live in tannergolden/intelligence.\n')
        self.assertEqual(self.problems(), [])

    def test_no_dash_the_standards_ban_reaches_it(self) -> None:
        self.write('kit/guard.py', GUARD + '# Every call — all of them.\n')
        self.assertProblem('en or em dash')


class TestTheRealKit(unittest.TestCase):
    """The kit in this repository."""

    root = HERE.parents[1]

    def test_it_breaks_no_rule(self) -> None:
        self.assertEqual(kit.problems(self.root), [])

    def test_it_carries_the_guard_alone(self) -> None:
        # The kit ships no skill and no subagent (ADR-0041).
        bundle, _ = kit.bundle(self.root)
        self.assertEqual(sorted(bundle), ['//', 'format', 'guard'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
