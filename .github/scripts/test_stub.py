#!/usr/bin/env python3
"""Tests for the stub a repository carries, and the workflow and action it calls.

WHY THIS EXISTS. The stub lives in other repositories, the reusable workflow
and the action live here, and only a release joins them. A stub that grants
less than the workflow asks for fails before any job starts, with no log to
read. A stub that names a major the action is not called at, or a release
missing a file the action runs, fails the same way in every repository at
once. These read the files as text and hold them to each other.

Nothing here calls GitHub.

Run it:

    python3 .github/scripts/test_stub.py
"""

from __future__ import annotations

import importlib.util
import io
import pathlib
import re
import subprocess
import sys
import tarfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
STUB = ROOT / 'setup' / 'intelligence-sync.yml'
WORKFLOW = ROOT / '.github' / 'workflows' / 'sync.yml'
ACTION = ROOT / '.github' / 'actions' / 'sync' / 'action.yml'
RELEASE = ROOT / '.github' / 'workflows' / 'cut-release.yml'
GUIDE = ROOT / 'docs' / 'technical' / 'Repository-Sync.md'

_spec = importlib.util.spec_from_file_location('sync', ROOT / '.github' / 'scripts' / 'sync.py')
sync = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = sync
_spec.loader.exec_module(sync)


def text(path: pathlib.Path) -> str:
    return path.read_text(encoding='utf-8')


def job_permissions(workflow: str) -> dict[str, str]:
    """The `permissions:` of a workflow's one job, as {scope: level}."""
    jobs = workflow[workflow.index('\njobs:'):]
    block = re.search(r'^    permissions:\n((?:      [\w-]+: \w+.*\n)+)', jobs, flags=re.M)
    return dict(re.findall(r'^      ([\w-]+): (\w+)', block.group(1), flags=re.M))


def required_files() -> set[str]:
    """What Cut Release refuses to tag without, from its `required-files` input."""
    lines = text(RELEASE).splitlines()
    at = next(i for i, line in enumerate(lines) if line.strip().startswith('required-files:'))
    indent = len(lines[at]) - len(lines[at].lstrip())
    value = lines[at].split(':', 1)[1].strip()
    words = [] if value in ('>-', '>', '|', '|-') else value.strip("'\"").split()
    for line in lines[at + 1:]:
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        words += line.split()
    return set(words)


def imported_from_hub() -> set[str]:
    """Every file of this hub that loading sync.py loads, as the action does at the tag."""
    code = ('import pathlib, sys\n'
            'root = pathlib.Path.cwd().resolve()\n'
            "sys.path.insert(0, str(root / '.github' / 'scripts'))\n"
            'import sync\n'
            'for module in list(sys.modules.values()):\n'
            "    where = getattr(module, '__file__', None)\n"
            '    if where and pathlib.Path(where).resolve().is_relative_to(root):\n'
            '        print(pathlib.Path(where).resolve().relative_to(root).as_posix())\n')
    done = subprocess.run([sys.executable, '-c', code], cwd=ROOT, capture_output=True, text=True,
                          check=True)
    return set(done.stdout.split())


def archived() -> set[str]:
    """Every file in the archive GitHub would serve for this tree, as it serves a remote action.

    `git archive` leaves out every path `.gitattributes` marks export-ignore, and
    `git check-attr` cannot show it: a pattern on a folder excludes the files in
    it without matching them. So this archives the index, the tree the next
    commit holds.
    """
    tree = subprocess.run(['git', 'write-tree'], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.strip()
    tar = subprocess.run(['git', 'archive', '--worktree-attributes', tree], cwd=ROOT,
                         capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as archive:
        return {member.name for member in archive.getmembers() if member.isfile()}


class TestTheStub(unittest.TestCase):
    """The stub, the workflow it calls and the action that calls, agreeing."""

    def test_the_stub_and_the_workflow_name_the_same_major(self) -> None:
        calls = r'^    uses: tannergolden/intelligence/\.github/workflows/sync\.yml@(v\d+)$'
        runs = r'^        uses: tannergolden/intelligence/\.github/actions/sync@(v\d+)$'
        stub = re.search(calls, text(STUB), flags=re.M)
        action = re.search(runs, text(WORKFLOW), flags=re.M)
        self.assertIsNotNone(stub, 'the stub calls the hub workflow at a moving major')
        self.assertIsNotNone(action, 'the workflow calls the hub action at a moving major')
        self.assertEqual(stub.group(1), action.group(1))

    def test_the_stub_grants_exactly_what_the_workflow_asks_for(self) -> None:
        self.assertEqual(job_permissions(text(STUB)), job_permissions(text(WORKFLOW)))
        self.assertEqual(job_permissions(text(STUB)),
                         {'contents': 'write', 'pull-requests': 'write'})
        self.assertIn('permissions: {}', text(STUB))

    def test_the_stub_hands_over_one_secret_and_never_all_of_them(self) -> None:
        stub = text(STUB)
        self.assertIsNone(re.search(r'^\s*secrets:\s*inherit', stub, flags=re.M))
        handed = r'^      ([\w-]+): \$\{\{ secrets\.([\w-]+) \}\}$'
        self.assertEqual(re.findall(handed, stub, flags=re.M),
                         [('BOT_ACCESS_TOKEN', 'BOT_ACCESS_TOKEN')])
        optional = r'(?m)^      BOT_ACCESS_TOKEN:\n(?:        .*\n)*        required: false$'
        self.assertRegex(text(WORKFLOW), optional)

    def test_the_stub_lives_where_audit_looks_for_it(self) -> None:
        self.assertEqual(sync.STUB, '.github/workflows/intelligence-sync.yml')
        self.assertIn(f'`{sync.STUB}`', text(GUIDE))

    def test_the_guide_carries_the_stub_as_it_is(self) -> None:
        self.assertIn(f'```yaml\n{text(STUB)}```', text(GUIDE))

    def test_the_action_runs_the_script_beside_it_on_the_sync_branch(self) -> None:
        action = text(ACTION)
        self.assertIn('"${GITHUB_ACTION_PATH}/../../scripts/sync.py" "${args[@]}"', action)
        self.assertIn('args=(apply ', action)
        self.assertEqual((ACTION.parent / '..' / '..' / 'scripts' / 'sync.py').resolve(),
                         ROOT / '.github' / 'scripts' / 'sync.py')
        self.assertIn(f'branch: {sync.BRANCH}', text(WORKFLOW))

    def test_a_release_carries_every_file_a_stub_resolves(self) -> None:
        needed = {'.github/workflows/sync.yml', '.github/actions/sync/action.yml',
                  'setup/intelligence-sync.yml', 'home/intelligence.md', sync.prompts.SOURCE, *imported_from_hub()}
        self.assertIn('.github/scripts/kit.py', needed, 'render.py imports kit.py; the action needs both')
        self.assertIn('.github/scripts/prompts.py', needed, 'sync.py imports prompts.py')
        self.assertLessEqual(needed, required_files())
        self.assertIn('setup/claude-cloud-setup.sh', required_files(), 'the first line counts too')

    def test_the_archive_a_stub_downloads_carries_the_action_and_its_code(self) -> None:
        # GitHub hands a calling repository the action from this hub's archive at
        # the tag, so a file export-ignore leaves out fails every stub at once. The
        # reusable workflow is read from the tag itself and may stay out.
        downloaded = {ACTION.relative_to(ROOT).as_posix(), 'home/intelligence.md', sync.prompts.SOURCE,
                      *imported_from_hub()}
        self.assertEqual(downloaded - archived(), set(), 'export-ignore leaves these out')


if __name__ == '__main__':
    unittest.main(verbosity=2)
