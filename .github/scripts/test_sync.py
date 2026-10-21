#!/usr/bin/env python3
"""Tests for repository sync, audit, merge and apply.

WHY THIS EXISTS. `sync.py` writes to every repository the owner owns, under
the owner's own login, `merge` lands changes on their default branches, and
`apply` runs inside each repository that carries the stub, with that
repository's token. So it has to stop wherever it should:

- leave alone what each repository wrote for itself;
- skip what must be skipped;
- merge only a pull request whose diff is the block alone and whose checks
  have passed, and let a bot's pull request run workflows only then.

These run every command against an in-memory stand-in for GitHub, a
throwaway hub with two release tags and a throwaway checkout, and check the
pure functions directly.

Nothing here calls GitHub or touches the repository it ships in.

Run it:

    python3 .github/scripts/test_sync.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
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
_spec = importlib.util.spec_from_file_location('sync', HERE / 'sync.py')
sync = importlib.util.module_from_spec(_spec)
# Dataclasses look their own module up by name while the class is built.
sys.modules[_spec.name] = sync
_spec.loader.exec_module(sync)
render = sync.render

OLD_BLOCK = '## Working rules\n\n- SEC-001: An older wording.\n'
CURRENT_BLOCK = render.render_block(render.load_constitution(ROOT))
OLD = render.region(OLD_BLOCK)
CURRENT = render.region(CURRENT_BLOCK)
GREEN = ([{'name': 'ci', 'status': 'completed', 'conclusion': 'success'}], {'state': 'pending', 'statuses': []})


GIT = ['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.com', '-c', 'commit.gpgsign=false',
       '-c', 'tag.gpgsign=false']

# The empty page a release gives a repository; the page an earlier release delivered, with the universal
# prompts sealed in; and what that release's setup/Prompts.md held, the universal prompts for sync to seal.
PAGE = '<!--\ntitle: x\n-->\n\n# Prompts\n\n---\n\n## Use It\n\n<!-- Yours. -->\n\n---\n\nThe end.\n'
OLD_INNER = '## How\n\nCopy one.\n'
OLD_PAGE = ('# Prompts\n\n---\n\n'
            f'<!-- INTELLIGENCE:PROMPTS:BEGIN sha256:{render.digest(OLD_INNER)} -->\n\n{OLD_INNER}\n'
            '<!-- INTELLIGENCE:PROMPTS:END -->\n\n---\n\n## Prompts For This Repository\n\n_Yours._\n')
OLD_SOURCE = '<!-- INTELLIGENCE:PROMPTS:BEGIN -->\n\n## How\n\nCopy one.\n\n<!-- INTELLIGENCE:PROMPTS:END -->\n'


def git(root: pathlib.Path, *args: str) -> None:
    subprocess.run(GIT + list(args), cwd=root, check=True, capture_output=True)


def make_hub(tags: bool = True) -> pathlib.Path:
    """A throwaway hub: the real Constitution, and two releases of the home file."""
    root = pathlib.Path(tempfile.mkdtemp(prefix='sync-test-'))
    shutil.copy(ROOT / render.CONSTITUTION_FILE, root / render.CONSTITUTION_FILE)
    (root / 'home').mkdir()
    git(root, 'init', '-q')
    git(root, 'remote', 'add', 'origin', 'https://github.com/tannergolden/intelligence.git')
    for block, tag in ((OLD_BLOCK, 'v0.0.1'), (CURRENT_BLOCK, 'v0.1.0')):
        (root / 'home' / 'intelligence.md').write_text(render.region(block), encoding='utf-8')
        git(root, 'add', '-A')
        git(root, 'commit', '-q', '-m', tag)
        if tags:
            git(root, 'tag', tag)
    return root


def release_page(root: pathlib.Path, source: str = PAGE, tag: str = 'v0.2.0') -> None:
    """A later release of the throwaway hub, the first to give a repository its prompts page."""
    (root / 'setup').mkdir(exist_ok=True)
    (root / sync.prompts.TEMPLATE).write_text(source, encoding='utf-8')
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '-m', tag)
    git(root, 'tag', tag)


class FakeGitHub(sync.GitHub):
    """Repositories, branches, files and pull requests, in memory."""

    def __init__(self) -> None:
        super().__init__(owner='tannergolden', run=self.refuse)
        self.listed: list[dict] = []
        self.trees: dict[tuple[str, str], dict[str, str]] = {}
        self.prs: dict[str, dict] = {}
        self.check_results: dict[str, tuple[list[dict], dict]] = {}
        self.messages: dict[str, str] = {}
        self.writes: list[str] = []
        self.merged: list[tuple[str, str]] = []
        self.settings: dict[str, dict] = {}
        self.waiting: dict[str, list[dict]] = {}
        self.approved: list[int] = []
        self.reopened: list[str] = []
        self.approval_fails = False

    @staticmethod
    def refuse(argv, stdin):  # pragma: no cover - a test that reaches gh is a broken test
        raise AssertionError(f'the fake must never call gh: {argv}')

    def add(self, name: str, files: dict[str, str] | None = None, **flags: object) -> None:
        self.listed.append({'name': name, 'default_branch': 'Development', **flags})
        self.trees[(name, 'Development')] = dict(files or {})

    def user(self) -> dict:
        return {'login': 'tannergolden', 'id': 24684994, 'name': 'Tanner Golden'}

    def repos(self) -> list[dict]:
        return self.listed

    def repo(self, full: str) -> dict:
        return self.settings.get(full, {'name': full.split('/', 1)[1]})

    def tree(self, repo: str, ref: str) -> dict[str, str]:
        return self.trees[(repo, sync.BRANCH)] if ref == f'{repo}-head' else self.trees[(repo, ref)]

    def file(self, repo, path, ref):
        text = self.tree(repo, ref).get(path)
        return None if text is None else (text, f'sha-{len(text)}')

    def head(self, repo, branch):
        return f'{repo}-{branch}' if (repo, branch) in self.trees else None

    def point_branch(self, repo, branch, sha):
        self.writes.append(f'{repo}: point {branch}')
        self.trees[(repo, branch)] = dict(self.trees[(repo, 'Development')])

    def put(self, repo, path, text, message, branch, sha):
        self.writes.append(f'{repo}: put {path}')
        self.trees[(repo, branch)][path] = text
        self.messages[repo] = message

    def delete(self, repo, path, message, branch, sha):
        self.writes.append(f'{repo}: delete {path}')
        del self.trees[(repo, branch)][path]

    def sync_pr(self, repo):
        pr = self.prs.get(repo)
        return pr if pr and pr['state'] == 'open' else None

    def open_pr(self, repo, base, title, body):
        self.writes.append(f'{repo}: open pr')
        self.prs[repo] = {'number': 7, 'title': title, 'body': body, 'state': 'open', 'mergeable': True,
                          'mergeable_state': 'clean', 'head': {'sha': f'{repo}-head'},
                          'user': {'login': 'tannergolden', 'type': 'User'}}
        return self.prs[repo]

    def edit_pr(self, repo, number, title, body):
        self.writes.append(f'{repo}: edit pr')
        self.prs[repo].update(title=title, body=body)

    def pr(self, repo, number):
        return self.prs[repo]

    def pr_files(self, repo, number):
        base, head = self.trees[(repo, 'Development')], self.trees[(repo, sync.BRANCH)]
        files = []
        for path in sorted(set(base) | set(head)):
            if path not in base:
                files.append({'filename': path, 'status': 'added'})
            elif path not in head:
                files.append({'filename': path, 'status': 'removed'})
            elif base[path] != head[path]:
                files.append({'filename': path, 'status': 'modified'})
        return files

    def checks(self, repo, sha):
        return self.check_results.get(repo, GREEN)

    def commit_message(self, repo, sha):
        return self.messages[repo]

    def merge(self, repo, number, sha, title, message):
        self.merged.append((repo, message))
        self.prs[repo]['state'] = 'closed'
        self.trees[(repo, 'Development')] = dict(self.trees[(repo, sync.BRANCH)])

    def waiting_runs(self, repo, sha):
        return list(self.waiting.get(repo, []))

    def approve_run(self, repo, run_id):
        if self.approval_fails:
            raise sync.GitHubError(f'POST approve {run_id}: HTTP 403')
        self.approved.append(run_id)

    def reopen(self, repo, number):
        self.reopened.append(repo)


class SyncTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.hub = make_hub()
        self.gh = FakeGitHub()

    def tearDown(self) -> None:
        shutil.rmtree(self.hub, ignore_errors=True)

    def run_sync(self, *args: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = sync.main(list(args), gh=self.gh, root=self.hub)
        return code, out.getvalue()

    def branch(self, repo: str) -> dict[str, str]:
        return self.gh.trees[(repo, sync.BRANCH)]


class TestSync(SyncTestCase):
    """`sync` opens one pull request per repository, and touches only what it must."""

    def test_a_repository_with_no_agents_file_gets_one(self) -> None:
        self.gh.add('alpha', {'README.md': '# Alpha\n'})
        code, out = self.run_sync('sync')
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: opened pull request #7', out)
        agents = self.branch('alpha')['AGENTS.md']
        self.assertIn(CURRENT, agents)
        self.assertEqual(render.find(agents).marker, render.digest(CURRENT_BLOCK))
        self.assertIn('## Overrides', agents)
        self.assertIn("work in alpha: the universal rules first, then this repository''s own", agents)
        own = agents.index("> **Write this repository's own rules from here down.**")
        self.assertLess(agents.index('<!-- INTELLIGENCE:END -->'), own)
        self.assertLess(own, agents.index('## Commands'))

    def test_the_commit_follows_the_standards(self) -> None:
        self.gh.add('alpha')
        self.run_sync('sync')
        title, body = self.gh.messages['alpha'].split('\n\n', 1)
        self.assertRegex(title, r'^chore\(agents\): 🤖 sync the universal rules to [0-9a-f]{12}$')
        self.assertTrue(body.rstrip().endswith(
            'Signed-off-by: Tanner Golden <24684994+tannergolden@users.noreply.github.com>'))
        prose = [line for line in body.splitlines() if not line.startswith('Signed-off-by:')]
        self.assertTrue(all(len(line) <= 72 for line in prose), 'the body wraps at 72; trailers are exempt')
        self.assertIsNone(re.search('[\u2013-\u2015]', self.gh.messages['alpha']))

    def test_a_current_repository_is_left_alone(self) -> None:
        self.gh.add('alpha', {'AGENTS.md': '# Alpha\n\n' + CURRENT + '\n## Commands\n'})
        code, out = self.run_sync('sync')
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: current', out)
        self.assertEqual(self.gh.writes, [])

    def test_an_update_replaces_only_the_block(self) -> None:
        mine = '# Alpha\n\n' + OLD + '\n## Commands\n\n- make test\n'
        self.gh.add('alpha', {'AGENTS.md': mine})
        self.run_sync('sync')
        self.assertEqual(self.branch('alpha')['AGENTS.md'], '# Alpha\n\n' + CURRENT + '\n## Commands\n\n- make test\n')
        self.assertIn('leaves every section this repository owns', self.gh.messages['alpha'].replace('\n', ' '))

    def test_a_block_goes_after_an_existing_header(self) -> None:
        agents = ('<!--\ntitle: x\n-->\n\n<!-- markdownlint-disable MD041 -->\n<div align="center">\n\n# Alpha\n\n'
                  '</div>\n\n---\n\n## Commands\n\n- make test\n')
        self.gh.add('alpha', {'AGENTS.md': agents})
        self.run_sync('sync')
        new = self.branch('alpha')['AGENTS.md']
        self.assertIn('</div>\n\n---\n\n' + CURRENT + '\n## Commands\n\n- make test\n', new)

    def test_claude_md_is_folded_in_and_deleted(self) -> None:
        self.gh.add('alpha', {'CLAUDE.md': '# Notes for Claude\n\n## Never name private repositories\n\nNot here.\n'})
        self.run_sync('sync')
        tree = self.branch('alpha')
        self.assertNotIn('CLAUDE.md', tree)
        self.assertIn('## Folded from CLAUDE.md\n\n### Never name private repositories\n\nNot here.', tree['AGENTS.md'])
        self.assertLess(tree['AGENTS.md'].index('Folded from'), tree['AGENTS.md'].index('Back to Top'))
        self.assertIn('first sync', self.gh.prs['alpha']['body'])

    def test_a_claude_md_that_only_points_at_agents_md_is_just_deleted(self) -> None:
        self.gh.add('alpha', {'AGENTS.md': '# Alpha\n\n' + CURRENT, 'CLAUDE.md': '@AGENTS.md\n'})
        self.run_sync('sync')
        tree = self.branch('alpha')
        self.assertNotIn('CLAUDE.md', tree)
        self.assertNotIn('Folded', tree['AGENTS.md'])

    def test_golden_path_templates_forks_archives_opt_outs_and_the_hub_are_skipped(self) -> None:
        self.gh.add('path', is_template=True)
        self.gh.add('forked', fork=True)
        self.gh.add('old', archived=True)
        self.gh.add('quiet', topics=['no-intelligence'])
        self.gh.add('intelligence')
        code, out = self.run_sync('sync')
        self.assertEqual(code, 0, out)
        for line in ('path: skipped, a golden path template', 'forked: skipped, a fork', 'old: skipped, archived',
                     'quiet: skipped, opted out', 'intelligence: skipped, the hub'):
            self.assertIn(line, out)
        self.assertEqual(self.gh.writes, [])

    def test_a_template_of_its_own_takes_part(self) -> None:
        """Only the golden path templates sit out: what any other template generates inherits its AGENTS.md."""
        self.gh.add('vault', {'CLAUDE.md': 'Some notes.\n'}, is_template=True)
        code, out = self.run_sync('sync', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('vault: would adopt', out)
        self.assertNotIn('vault: skipped', out)

    def test_a_dry_run_changes_nothing(self) -> None:
        self.gh.add('alpha', {'CLAUDE.md': 'Some notes.\n'})
        code, out = self.run_sync('sync', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: would adopt', out)
        self.assertEqual(self.gh.writes, [])

    def test_a_second_sync_updates_the_open_pull_request(self) -> None:
        self.gh.add('alpha', {'AGENTS.md': '# Alpha\n\n' + OLD})
        self.run_sync('sync')
        _code, out = self.run_sync('sync')
        self.assertIn('alpha: updated pull request #7', out)
        self.assertEqual(self.gh.writes.count('alpha: open pr'), 1)

    def test_one_repository_can_be_chosen(self) -> None:
        self.gh.add('alpha')
        self.gh.add('beta')
        self.run_sync('sync', '--repo', 'beta')
        self.assertIn(('beta', sync.BRANCH), self.gh.trees)
        self.assertNotIn(('alpha', sync.BRANCH), self.gh.trees)

    def test_without_a_release_nothing_is_delivered(self) -> None:
        shutil.rmtree(self.hub)
        self.hub = make_hub(tags=False)
        self.gh.add('alpha')
        with self.assertRaises(SystemExit) as caught:
            self.run_sync('sync')
        self.assertIn('no release yet', str(caught.exception))

    def test_an_unreleased_block_needs_an_explicit_ref(self) -> None:
        shutil.rmtree(self.hub)
        self.hub = make_hub(tags=False)
        self.gh.add('alpha')
        code, out = self.run_sync('sync', '--ref', 'HEAD')
        self.assertEqual(code, 0, out)
        self.assertIn(CURRENT, self.branch('alpha')['AGENTS.md'])


class TestAudit(SyncTestCase):
    """`audit` names everything that is not as the latest release left it."""

    def audit(self, files: dict[str, str]) -> tuple[int, str]:
        self.gh.add('alpha', files)
        return self.run_sync('audit')

    def test_a_current_repository_passes(self) -> None:
        code, out = self.audit({'AGENTS.md': '# A\n\n' + CURRENT})
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: current', out)

    def test_each_problem_is_named(self) -> None:
        cases = {
            'no AGENTS.md': {},
            'AGENTS.md has no block': {'AGENTS.md': '# A\n'},
            'edited by hand': {'AGENTS.md': CURRENT.replace('Never put', 'Rarely put')},
            'the block is from v0.0.1': {'AGENTS.md': OLD},
            'not one the hub ever released': {'AGENTS.md': render.region('## Working rules\n\n- X: Mine.\n')},
            'Claude Code may skip AGENTS.md': {'AGENTS.md': CURRENT, 'CLAUDE.md': '# Notes\n'},
            'SEC-001, an Invariant': {'AGENTS.md': CURRENT + '\n## Overrides\n\n- SEC-001: we need to\n'},
            'STD-001 without a reason': {'AGENTS.md': CURRENT + '\n## Overrides\n\n- STD-001\n'},
        }
        for expected, files in cases.items():
            with self.subTest(expected=expected):
                self.gh = FakeGitHub()
                code, out = self.audit(files)
                self.assertEqual(code, 1, out)
                self.assertIn(expected, out)

    def test_an_override_of_a_default_with_a_reason_is_fine(self) -> None:
        code, out = self.audit({'AGENTS.md': CURRENT + '\n## Overrides\n\n- STD-001: this repo is the standards\n'})
        self.assertEqual(code, 0, out)

    def test_a_missing_stub_is_noted_and_is_not_a_failure(self) -> None:
        code, out = self.audit({'AGENTS.md': '# A\n\n' + CURRENT})
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: current (no stub, so only make sync updates it)', out)

    def test_a_repository_with_the_stub_gets_no_note(self) -> None:
        _code, out = self.audit({'AGENTS.md': '# A\n\n' + CURRENT, sync.STUB: 'name: x\n'})
        self.assertIn('alpha: current\n', out)


class TestMerge(SyncTestCase):
    """`merge` lands only a green pull request whose diff is the block alone."""

    def routine(self, **checks: object) -> None:
        self.gh.add('alpha', {'AGENTS.md': '# Alpha\n\n' + OLD + '\n## Commands\n'})
        self.run_sync('sync')
        if checks:
            self.gh.check_results['alpha'] = checks['results']

    def test_a_green_block_only_change_is_merged_with_its_sign_off(self) -> None:
        self.routine()
        code, out = self.run_sync('merge')
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: merged #7', out)
        _repo, message = self.gh.merged[0]
        self.assertIn('Signed-off-by: Tanner Golden', message)
        self.assertIn(CURRENT, self.gh.trees[('alpha', 'Development')]['AGENTS.md'])

    def test_a_first_sync_waits_for_review_by_hand(self) -> None:
        self.gh.add('alpha', {'README.md': '# Alpha\n'})
        self.run_sync('sync')
        _code, out = self.run_sync('merge')
        self.assertIn('review it by hand', out)
        self.assertEqual(self.gh.merged, [])

    def test_red_pending_and_missing_checks_all_wait(self) -> None:
        cases = {
            'checks failed': ([{'name': 'ci', 'status': 'completed', 'conclusion': 'failure'}], {}),
            'still running': ([{'name': 'ci', 'status': 'in_progress'}], {}),
            'no checks ran': ([], {'state': 'pending', 'statuses': []}),
            'commit status is failure': ([], {'state': 'failure', 'statuses': [{'state': 'failure'}]}),
        }
        for expected, results in cases.items():
            with self.subTest(expected=expected):
                self.gh = FakeGitHub()
                self.routine(results=results)
                _code, out = self.run_sync('merge')
                self.assertIn(expected, out)
                self.assertEqual(self.gh.merged, [])

    def test_a_pull_request_carrying_an_older_block_waits(self) -> None:
        self.routine()
        other = render.region('## Working rules\n\n- X: Y.\n')
        self.branch('alpha')['AGENTS.md'] = '# Alpha\n\n' + other + '\n## Commands\n'
        _code, out = self.run_sync('merge')
        self.assertIn('older block', out)

    def test_a_pull_request_that_is_not_mergeable_waits(self) -> None:
        self.routine()
        self.gh.prs['alpha'].update(mergeable=False, mergeable_state='dirty')
        _code, out = self.run_sync('merge')
        self.assertIn('not mergeable yet (dirty)', out)

    def test_a_dry_run_merges_nothing(self) -> None:
        self.routine()
        _code, out = self.run_sync('merge', '--dry-run')
        self.assertIn('would merge #7', out)
        self.assertEqual(self.gh.merged, [])


class TestMergeAfterTheStub(SyncTestCase):
    """A pull request the stub opened with the default token: its checks wait until merge starts them."""

    NOTHING = ([], {'state': 'pending', 'statuses': []})

    def stub_opened(self, waiting: tuple[int, ...] = (), first: bool = False) -> None:
        self.gh.add('alpha', {'README.md': '# Alpha\n'} if first else {'AGENTS.md': '# Alpha\n\n' + OLD})
        self.run_sync('sync')
        self.gh.prs['alpha']['user'] = {'login': 'github-actions[bot]', 'type': 'Bot'}
        self.gh.check_results['alpha'] = self.NOTHING
        self.gh.waiting['alpha'] = [{'id': run} for run in waiting]

    def test_waiting_runs_are_approved_and_the_next_merge_lands_it(self) -> None:
        self.stub_opened(waiting=(11, 12))
        code, out = self.run_sync('merge')
        self.assertEqual(code, 0, out)
        self.assertIn('approved its 2 waiting workflow run(s)', out)
        self.assertEqual((self.gh.approved, self.gh.reopened, self.gh.merged), ([11, 12], [], []))
        self.gh.waiting['alpha'] = []
        self.gh.check_results['alpha'] = GREEN
        _code, out = self.run_sync('merge')
        self.assertIn('alpha: merged #7', out)

    def test_with_no_run_at_all_it_is_reopened(self) -> None:
        self.stub_opened()
        _code, out = self.run_sync('merge')
        self.assertIn('reopened it, which starts its checks', out)
        self.assertEqual(self.gh.reopened, ['alpha'])

    def test_a_refused_approval_falls_back_to_reopening(self) -> None:
        self.stub_opened(waiting=(11,))
        self.gh.approval_fails = True
        _code, out = self.run_sync('merge')
        self.assertIn('reopened it', out)
        self.assertEqual(self.gh.reopened, ['alpha'])

    def test_a_dry_run_starts_nothing(self) -> None:
        self.stub_opened(waiting=(11,))
        _code, out = self.run_sync('merge', '--dry-run')
        self.assertIn('would start the checks of #7', out)
        self.assertEqual((self.gh.approved, self.gh.reopened), ([], []))

    def test_a_bigger_change_never_gets_to_run_workflows(self) -> None:
        self.stub_opened(waiting=(11,), first=True)
        _code, out = self.run_sync('merge')
        self.assertIn('review it by hand', out)
        self.assertEqual((self.gh.approved, self.gh.reopened, self.gh.merged), ([], [], []))

    def test_a_pull_request_the_owner_opened_is_never_reopened(self) -> None:
        self.stub_opened()
        self.gh.prs['alpha']['user'] = {'login': 'tannergolden', 'type': 'User'}
        _code, out = self.run_sync('merge')
        self.assertIn(sync.NOTHING_RAN, out)
        self.assertEqual(self.gh.reopened, [])


class TestPromptsPage(SyncTestCase):
    """A release that gives each repository an empty `docs/Prompts.md`, in the same pull request as the rules."""

    TARGET = sync.prompts.TARGET

    def setUp(self) -> None:
        super().setUp()
        release_page(self.hub)

    def current(self, **files: str) -> dict[str, str]:
        return {'AGENTS.md': '# Alpha\n\n' + CURRENT, **files}

    def test_a_new_repository_gets_the_empty_page_beside_its_agents_file(self) -> None:
        self.gh.add('alpha', {'README.md': '# Alpha\n'})
        code, out = self.run_sync('sync')
        self.assertEqual(code, 0, out)
        tree = self.branch('alpha')
        self.assertIn(CURRENT, tree['AGENTS.md'])
        self.assertEqual(tree[self.TARGET], PAGE)
        self.assertIn('adds `docs/Prompts.md`', self.gh.messages['alpha'].replace('\n', ' '))
        self.assertIn('first sync', self.gh.prs['alpha']['body'])

    def test_a_repository_with_current_rules_gets_the_page_alone(self) -> None:
        self.gh.add('alpha', self.current())
        self.run_sync('sync')
        self.assertNotIn('alpha: put AGENTS.md', self.gh.writes)
        self.assertEqual(self.branch('alpha')[self.TARGET], PAGE)
        title, body = self.gh.messages['alpha'].split('\n\n', 1)
        self.assertEqual(title, "chore(agents): 🤖 add a page for this repository's own prompts")
        self.assertTrue(all(len(line) <= 72 for line in body.splitlines() if not line.startswith('Signed-off-by:')))
        self.assertIn('review it by hand', self.gh.prs['alpha']['body'])

    def test_the_universal_prompts_come_out_and_its_own_prompts_stay(self) -> None:
        mine = OLD_PAGE.replace('_Yours._', '### Ship A Release\n\nOurs.')
        self.gh.add('alpha', self.current(**{self.TARGET: mine}))
        self.run_sync('sync')
        page = self.branch('alpha')[self.TARGET]
        self.assertEqual(page, '# Prompts\n\n---\n\n## Prompts For This Repository\n\n### Ship A Release\n\nOurs.\n')
        title, body = self.gh.messages['alpha'].split('\n\n', 1)
        self.assertEqual(title, 'chore(agents): 🤖 leave the universal prompts to the hub')
        self.assertIn("leaves this repository's own prompts as they were", body.replace('\n', ' '))
        self.assertIn('finds no universal prompts left', self.gh.prs['alpha']['body'])

    def test_a_page_of_its_own_and_the_topic_keep_sync_out(self) -> None:
        self.gh.add('alpha', self.current(**{self.TARGET: '# Our own prompts\n'}))
        self.gh.add('beta', self.current(), topics=['no-intelligence-prompts'])
        self.gh.add('gamma', self.current(**{self.TARGET: PAGE}))
        _code, out = self.run_sync('sync')
        for name in ('alpha', 'beta', 'gamma'):
            self.assertIn(f'{name}: current', out)
        self.assertEqual(self.gh.writes, [])

    def test_a_dry_run_names_the_change_to_the_page(self) -> None:
        self.gh.add('alpha', self.current(**{self.TARGET: OLD_PAGE}))
        _code, out = self.run_sync('sync', '--dry-run')
        self.assertIn('alpha: would update (takes the universal prompts out of `docs/Prompts.md`', out)
        self.assertEqual(self.gh.writes, [])

    def test_a_change_to_the_page_waits_for_review_by_hand(self) -> None:
        for files in ({}, {self.TARGET: OLD_PAGE}):
            with self.subTest(files=list(files)):
                self.gh = FakeGitHub()
                self.gh.add('alpha', {'AGENTS.md': '# Alpha\n\n' + OLD, **files})
                self.run_sync('sync')
                _code, out = self.run_sync('merge')
                self.assertIn('review it by hand', out)
                self.assertEqual(self.gh.merged, [])

    def test_a_release_from_before_the_page_brings_none(self) -> None:
        # Its setup/Prompts.md held the universal prompts for sync to seal; this sync delivers no prompts at all.
        release_page(self.hub, OLD_SOURCE, 'v0.3.0')
        self.gh.add('alpha', self.current())
        _code, out = self.run_sync('sync')
        self.assertIn('alpha: current', out)
        self.assertEqual(self.gh.writes, [])

    def test_audit_names_what_sync_has_left_to_do(self) -> None:
        cases = {
            'no docs/Prompts.md': {},
            'docs/Prompts.md still holds the universal prompts, which the next sync takes out':
                {self.TARGET: OLD_PAGE},
        }
        for expected, files in cases.items():
            with self.subTest(expected=expected):
                self.gh = FakeGitHub()
                self.gh.add('alpha', self.current(**files))
                code, out = self.run_sync('audit')
                self.assertEqual(code, 1, out)
                self.assertIn(expected, out)
        self.gh = FakeGitHub()
        self.gh.add('alpha', self.current(**{self.TARGET: PAGE}))
        self.gh.add('beta', self.current(**{self.TARGET: '# Ours\n'}))
        self.gh.add('gamma', self.current(), topics=['no-intelligence-prompts'])
        code, out = self.run_sync('audit')
        self.assertEqual(code, 0, out)


class TestTextHandling(unittest.TestCase):
    """The pure functions that place, fold and read text."""

    def test_the_block_goes_after_a_plain_title(self) -> None:
        text = '# Alpha\n\nIntro.\n'
        self.assertEqual(text[:sync.insert_point(text)], '# Alpha\n')

    def test_the_block_goes_at_the_top_of_a_file_with_no_header(self) -> None:
        self.assertEqual(sync.insert_point('Just notes.\n'), 0)

    def test_the_block_goes_after_yaml_frontmatter_and_its_title(self) -> None:
        front = '---\ntitle: "AGENTS.md"\nlayer: 0\n---\n'
        text = front + '\n# Agents\n\nIntro.\n'
        self.assertEqual(text[:sync.insert_point(text)], front + '\n# Agents\n')
        self.assertEqual(sync.insert_point(front + 'Notes.\n'), len(front))

    def test_a_rule_line_that_is_not_frontmatter_is_left_alone(self) -> None:
        # Frontmatter opens on the first line and closes; anything else is a rule line.
        self.assertEqual(sync.insert_point('\n---\ntitle: x\n---\nNotes.\n'), 1)
        self.assertEqual(sync.insert_point('---\nNo end to it.\n'), 0)

    def test_adopting_a_note_keeps_its_frontmatter_first(self) -> None:
        agents = '---\ntitle: "AGENTS.md"\n---\n\n# Agents\n\nRead the folder notes.\n'
        change = sync.adopt('vault', agents, None, CURRENT)
        self.assertTrue(change.agents.startswith('---\ntitle: "AGENTS.md"\n---\n\n# Agents\n\n' + CURRENT))
        self.assertTrue(change.agents.endswith('\nRead the folder notes.\n'))

    def test_headings_inside_code_fences_are_not_demoted(self) -> None:
        self.assertEqual(sync.demote('## A\n```\n# not a heading\n```\n'), '### A\n```\n# not a heading\n```\n')

    def test_pointers_are_recognised(self) -> None:
        for text in ('@AGENTS.md\n', '# Claude\n\n@./AGENTS.md\n', '<!-- x -->\n@AGENTS.md'):
            self.assertTrue(sync.is_pointer(text), text)
        self.assertFalse(sync.is_pointer('@AGENTS.md\nAlso this.\n'))

    def test_overrides_are_read_with_their_reasons(self) -> None:
        text = '## Overrides\n\n<!-- a note -->\n- `WORK-002`: we ask more\n- STD-001\n\n## Next\n\n- SEC-001: no\n'
        self.assertEqual(sync.overrides(text), [('WORK-002', 'we ask more'), ('STD-001', '')])

    def test_only_a_change_between_the_markers_counts_as_block_only(self) -> None:
        old = '# A\n\n' + OLD + '\nmine\n'
        self.assertTrue(sync.only_block_changed(old, old.replace(OLD, CURRENT)))
        self.assertFalse(sync.only_block_changed(old, old.replace('mine', 'yours')))
        self.assertFalse(sync.only_block_changed('# A\n', '# A\n'))

    def test_paginated_pages_are_joined(self) -> None:
        self.assertEqual(sync.decode_pages('[1, 2]\n[3]\n'), [1, 2, 3])
        self.assertEqual(sync.decode_pages('{"a": 1}'), {'a': 1})


class TestGhCalls(unittest.TestCase):
    """The real client's calls to `gh`, with a stand-in for the process."""

    def test_a_body_goes_on_standard_input(self) -> None:
        seen = []

        def run(argv, stdin):
            seen.append((argv, stdin))
            return subprocess.CompletedProcess(argv, 0, '{"number": 3}', '')

        gh = sync.GitHub(owner='o', run=run)
        self.assertEqual(gh.open_pr('r', 'main', 't', 'b'), {'number': 3})
        argv, stdin = seen[0]
        self.assertEqual(argv[:5], ['gh', 'api', '-X', 'POST', 'repos/o/r/pulls'])
        self.assertIn('--input', argv)
        self.assertIn('"head": "chore/intelligence"', stdin)

    def test_a_missing_file_is_none_and_other_errors_raise(self) -> None:
        def missing(argv, stdin):
            return subprocess.CompletedProcess(argv, 1, '', 'gh: Not Found (HTTP 404)')

        def broken(argv, stdin):
            return subprocess.CompletedProcess(argv, 1, '', 'gh: Bad credentials (HTTP 401)')

        self.assertIsNone(sync.GitHub(owner='o', run=missing).file('r', 'AGENTS.md', 'main'))
        with self.assertRaises(sync.GitHubError):
            sync.GitHub(owner='o', run=broken).file('r', 'AGENTS.md', 'main')

    def test_starting_checks_approves_runs_or_closes_and_reopens(self) -> None:
        seen = []

        def run(argv, stdin):
            seen.append((argv[3:5], stdin))
            return subprocess.CompletedProcess(argv, 0, '{"workflow_runs": [{"id": 5}]}', '')

        gh = sync.GitHub(owner='o', run=run)
        self.assertEqual(gh.waiting_runs('r', 'abc'), [{'id': 5}])
        gh.approve_run('r', 5)
        gh.reopen('r', 9)
        self.assertEqual(seen[0][0], ['GET', 'repos/o/r/actions/runs?head_sha=abc&status=action_required&per_page=100'])
        self.assertEqual(seen[1], (['POST', 'repos/o/r/actions/runs/5/approve'], None))
        self.assertEqual([json.loads(stdin)['state'] for _path, stdin in seen[2:]], ['closed', 'open'])


class TestApply(unittest.TestCase):
    """`apply`, as a repository's stub runs it: one checkout, written in place, nothing pushed."""

    def setUp(self) -> None:
        self.hub = make_hub()
        self.gh = FakeGitHub()
        self.checkout = pathlib.Path(tempfile.mkdtemp(prefix='sync-checkout-'))
        self.outputs = pathlib.Path(tempfile.mkdtemp(prefix='sync-outputs-')) / 'outputs'
        for folder in (self.hub, self.checkout, self.outputs.parent):
            self.addCleanup(shutil.rmtree, folder, True)

    def run_apply(self, *args: str, repo: str = 'tannergolden/alpha', actions: str = '') -> tuple[int, str]:
        out = io.StringIO()
        env = {'GITHUB_REPOSITORY': repo, 'GITHUB_OUTPUT': str(self.outputs), 'GITHUB_ACTIONS': actions}
        with mock.patch.dict(os.environ, env), contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            code = sync.main(['apply', '--path', str(self.checkout), '--release', 'v0.1.0', *args],
                             gh=self.gh, root=self.hub)
        return code, out.getvalue()

    def written(self) -> dict[str, str]:
        """What `apply` handed the workflow, read the way Actions reads $GITHUB_OUTPUT."""
        text = self.outputs.read_text(encoding='utf-8') if self.outputs.exists() else ''
        pattern = r'^(?P<key>[\w-]+)<<(?P<end>\S+)\n(?P<value>.*?)\n(?P=end)\n'
        return {m.group('key'): m.group('value') for m in re.finditer(pattern, text, flags=re.M | re.S)}

    def agents(self) -> str:
        return (self.checkout / 'AGENTS.md').read_text(encoding='utf-8')

    def test_a_checkout_with_no_agents_file_gets_one_and_the_workflow_its_text(self) -> None:
        (self.checkout / 'README.md').write_text('# Alpha\n', encoding='utf-8')
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertIn(CURRENT, self.agents())
        values = self.written()
        self.assertEqual(values['changed'], 'true')
        self.assertRegex(values['commit-title'], r'^chore\(agents\): 🤖 sync the universal rules to [0-9a-f]{12}$')
        self.assertEqual(values['pr-title'], values['commit-title'])
        self.assertNotIn('Signed-off-by', values['commit-body'], 'the open-pr action signs off as the owner')
        self.assertIn('Approve workflows to run', values['pr-body'])
        self.assertIn('first sync', values['pr-body'])

    def test_an_update_replaces_only_the_block_and_keeps_line_endings(self) -> None:
        mine = '# Alpha\r\n\r\n' + OLD + '\r\n## Commands\r\n\r\n- make test\r\n'
        (self.checkout / 'AGENTS.md').write_bytes(mine.encode('utf-8'))
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertEqual((self.checkout / 'AGENTS.md').read_bytes().decode('utf-8'), mine.replace(OLD, CURRENT))
        self.assertIn('alpha: updates the block, to', out)
        body = self.written()['pr-body']
        self.assertIn('make merge', body)
        self.assertIn('release v0.1.0', body)

    def test_a_current_checkout_is_left_alone(self) -> None:
        (self.checkout / 'AGENTS.md').write_text('# Alpha\n\n' + CURRENT, encoding='utf-8')
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: current', out)
        self.assertEqual(self.written(), {'changed': 'false'})

    def test_claude_md_is_folded_in_and_deleted(self) -> None:
        (self.checkout / 'CLAUDE.md').write_text('# Notes\n\n## Keep this\n\nIt matters.\n', encoding='utf-8')
        self.run_apply()
        self.assertFalse((self.checkout / 'CLAUDE.md').exists())
        self.assertIn('## Folded from CLAUDE.md\n\n### Keep this', self.agents())

    def test_a_linked_claude_md_is_refused_and_nothing_is_written(self) -> None:
        (self.checkout / 'AGENTS.md').write_text('# Alpha\n\n' + OLD, encoding='utf-8')
        (self.checkout / 'CLAUDE.md').symlink_to('AGENTS.md')
        code, out = self.run_apply(actions='true')
        self.assertEqual(code, 1, out)
        self.assertIn('::error title=Intelligence Sync::alpha: CLAUDE.md is a link or a folder', out)
        self.assertIn(OLD, self.agents())
        self.assertEqual(self.written(), {})

    def test_two_blocks_are_refused(self) -> None:
        (self.checkout / 'AGENTS.md').write_text(OLD + '\n' + OLD, encoding='utf-8')
        code, out = self.run_apply()
        self.assertEqual(code, 1, out)
        self.assertIn('more than one INTELLIGENCE block', out)

    def test_the_hub_and_every_repository_left_out_are_skipped(self) -> None:
        (self.checkout / 'CONSTITUTION.md').write_text('# Constitution\n', encoding='utf-8')
        (self.checkout / '.github' / 'scripts').mkdir(parents=True)
        (self.checkout / '.github' / 'scripts' / 'render.py').write_text('', encoding='utf-8')
        _code, out = self.run_apply(repo='tannergolden/intelligence')
        self.assertIn('intelligence: skipped, the hub', out)
        (self.checkout / 'CONSTITUTION.md').unlink()
        self.gh.settings['tannergolden/path'] = {'name': 'path', 'is_template': True}
        code, out = self.run_apply(repo='tannergolden/path')
        self.assertEqual(code, 0, out)
        self.assertIn('path: skipped, a golden path template', out)
        for flags, expected in (({'fork': True}, 'a fork'),
                                ({'archived': True}, 'archived'), ({'topics': ['no-intelligence']}, 'opted out')):
            with self.subTest(expected=expected):
                self.gh.settings['tannergolden/alpha'] = flags
                code, out = self.run_apply()
                self.assertEqual(code, 0, out)
                self.assertIn(f'alpha: skipped, {expected}', out)
        self.assertFalse((self.checkout / 'AGENTS.md').exists())

    def test_a_template_of_its_own_is_written_into(self) -> None:
        self.gh.settings['tannergolden/alpha'] = {'name': 'alpha', 'is_template': True}
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertNotIn('skipped', out)
        self.assertTrue((self.checkout / 'AGENTS.md').exists())

    def test_a_dry_run_writes_nothing(self) -> None:
        code, out = self.run_apply('--dry-run')
        self.assertEqual(code, 0, out)
        self.assertIn('alpha: would adopt', out)
        self.assertFalse((self.checkout / 'AGENTS.md').exists())
        self.assertEqual(self.written(), {'changed': 'false'})

    def ship_page(self) -> None:
        """The hub tree the stub's action runs from carries the empty prompts page."""
        (self.hub / 'setup').mkdir(exist_ok=True)
        (self.hub / sync.prompts.TEMPLATE).write_text(PAGE, encoding='utf-8')

    def test_the_page_is_written_into_the_checkout(self) -> None:
        self.ship_page()
        (self.checkout / 'AGENTS.md').write_text('# Alpha\n\n' + CURRENT, encoding='utf-8')
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertEqual((self.checkout / sync.prompts.TARGET).read_text(encoding='utf-8'), PAGE)
        self.assertIn('alpha: adds `docs/Prompts.md`', out)
        values = self.written()
        self.assertEqual(values['changed'], 'true')
        self.assertEqual(values['commit-title'], "chore(agents): 🤖 add a page for this repository's own prompts")
        self.assertIn('Approve workflows to run', values['pr-body'])
        self.assertEqual((self.checkout / 'AGENTS.md').read_text(encoding='utf-8'), '# Alpha\n\n' + CURRENT)

    def test_the_universal_prompts_are_taken_out_in_place(self) -> None:
        self.ship_page()
        (self.checkout / 'AGENTS.md').write_text('# Alpha\n\n' + OLD, encoding='utf-8')
        (self.checkout / 'docs').mkdir()
        (self.checkout / sync.prompts.TARGET).write_text(OLD_PAGE, encoding='utf-8')
        code, out = self.run_apply()
        self.assertEqual(code, 0, out)
        self.assertIn('updates the block, to', out)
        self.assertIn('takes the universal prompts out of `docs/Prompts.md`', out)
        self.assertEqual((self.checkout / sync.prompts.TARGET).read_text(encoding='utf-8'),
                         '# Prompts\n\n---\n\n## Prompts For This Repository\n\n_Yours._\n')

    def test_the_topic_keeps_the_page_out_of_the_checkout(self) -> None:
        self.ship_page()
        self.gh.settings['tannergolden/alpha'] = {'name': 'alpha', 'topics': ['no-intelligence-prompts']}
        (self.checkout / 'AGENTS.md').write_text('# Alpha\n\n' + CURRENT, encoding='utf-8')
        _code, out = self.run_apply()
        self.assertIn('alpha: current', out)
        self.assertFalse((self.checkout / sync.prompts.TARGET).exists())

    def test_it_runs_only_where_actions_names_the_repository(self) -> None:
        with mock.patch.dict(os.environ, {'GITHUB_REPOSITORY': ''}), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as caught:
                sync.main(['apply'], gh=self.gh, root=self.hub)
        self.assertEqual(caught.exception.code, 2)


class TestReleaseLabel(unittest.TestCase):
    """A pull request names the release a moving tag points at."""

    @staticmethod
    def with_tags(tags: list[dict], ok: bool = True) -> sync.GitHub:
        def run(argv, stdin):
            if not ok:
                return subprocess.CompletedProcess(argv, 1, '', 'gh: Forbidden (HTTP 403)')
            return subprocess.CompletedProcess(argv, 0, json.dumps(tags), '')

        return sync.GitHub(owner='o', run=run)

    def test_a_moving_tag_names_the_newest_release_at_its_commit(self) -> None:
        tags = [{'name': 'v0', 'commit': {'sha': 'b'}}, {'name': 'v0.1.0', 'commit': {'sha': 'a'}},
                {'name': 'v0.2.0', 'commit': {'sha': 'b'}}, {'name': 'v0.10.0', 'commit': {'sha': 'c'}},
                {'name': 'v0.1.1', 'commit': {'sha': 'b'}}]
        self.assertEqual(sync.release_label(self.with_tags(tags), 'o/hub', 'v0'), 'v0.2.0')

    def test_anything_else_stays_as_given(self) -> None:
        self.assertEqual(sync.release_label(self.with_tags([]), 'o/hub', 'v0.3.1'), 'v0.3.1')
        self.assertEqual(sync.release_label(self.with_tags([]), 'o/hub', ''), 'the latest release')
        self.assertEqual(sync.release_label(self.with_tags([]), 'o/hub', 'v0'), 'v0')
        self.assertEqual(sync.release_label(self.with_tags([], ok=False), 'o/hub', 'v0'), 'v0')


if __name__ == '__main__':
    unittest.main(verbosity=2)
