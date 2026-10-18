#!/usr/bin/env python3
"""Tests for the guard hook.

WHY THIS EXISTS. `guard.py` sits in front of every shell command and file
edit an agent makes, in every app the kit supports. It earns that place only
if it blocks exactly what the rules forbid and nothing an agent does all day:
a guard that cries wolf gets switched off, and one that misses a force-push
is worse than none. These tests hold both sides, against a throwaway git
repository and home folder, with the payload each app actually sends.

Credentials in these tests are assembled at run time, so no file here holds
anything a secret scanner would flag.

Run it:

    python3 scripts/test_guard.py
"""

from __future__ import annotations

import contextlib
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
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent


def load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    # Dataclasses look their own module up by name while the class is built.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


guard = load('guard', 'guard.py')
render = load('render', 'render.py')

HUMAN = 'Tanner Golden <24684994+tannergolden@users.noreply.github.com>'
GITHUB_TOKEN = 'ghp_' + 'a1B2c3D4e5' * 4
BLOCK = '## Working rules\n\n- SEC-001: Never put a credential in a file.\n'


def git(cwd: pathlib.Path, *args: str) -> None:
    subprocess.run(['git', '-C', str(cwd), *args], check=True, capture_output=True)


class Sandbox(unittest.TestCase):
    """A git repository on a feature branch, owned by a person, inside a throwaway home."""

    def setUp(self) -> None:
        self.root = pathlib.Path(tempfile.mkdtemp(prefix='guard-test-'))
        self.home = self.root / 'home'
        self.repo = self.root / 'repo'
        self.home.mkdir()
        self.repo.mkdir()
        git(self.repo, 'init', '-q', '-b', 'main')
        git(self.repo, 'config', 'user.name', 'Tanner Golden')
        git(self.repo, 'config', 'user.email', '24684994+tannergolden@users.noreply.github.com')
        (self.repo / 'README.md').write_text('# Repo\n', encoding='utf-8')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-q', '-m', 'init')
        git(self.repo, 'checkout', '-q', '-b', 'feat/work')
        environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        environment['HOME'] = str(self.home)
        environment.pop('CODEX_HOME', None)
        patcher = mock.patch.dict(os.environ, environment, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def verdict(self, command: str):
        return guard.decide(guard.Call('Bash', {'command': command}, self.repo), self.home)

    def denied(self, command: str, rule: str) -> None:
        verdict = self.verdict(command)
        self.assertIsNotNone(verdict, f'{command!r} should be denied')
        self.assertEqual(verdict.rule, rule, f'{command!r}: {verdict.line()}')

    def allowed(self, command: str) -> None:
        verdict = self.verdict(command)
        self.assertIsNone(verdict, f'{command!r} should pass: {verdict.line() if verdict else ""}')

    def edit(self, tool: str, **args: object):
        return guard.decide(guard.Call(tool, dict(args), self.repo), self.home)

    def run_hook(self, payload: object) -> tuple[int, str]:
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = guard.main(['--app', 'test'], stdin=json.dumps(payload))
        return code, err.getvalue()


class TestPush(Sandbox):
    """OPS-001: no force, no deletion, no tags, nothing straight onto a protected branch."""

    def test_an_ordinary_push_of_your_branch_passes(self) -> None:
        for command in ('git push origin feat/work', 'git push -u origin feat/work', 'git push',
                        'git push origin HEAD', 'git push --force-with-lease origin feat/work',
                        'git push --force-with-lease=feat/work --force-if-includes origin feat/work',
                        'git push -n --force origin main'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_force_is_blocked_in_every_spelling(self) -> None:
        for command in ('git push --force', 'git push -f origin feat/work', 'git push -uf origin feat/work',
                        'git push origin +feat/work', 'git push --force --force-with-lease origin feat/work',
                        'git -C . push --force'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-001')

    def test_protected_branches_are_blocked(self) -> None:
        for command in ('git push origin main', 'git push origin HEAD:Development', 'git push origin Release',
                        'git push origin feat/work:refs/heads/main', 'git push --force-with-lease origin main'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-001')

    def test_a_bare_push_from_a_protected_branch_is_blocked(self) -> None:
        git(self.repo, 'checkout', '-q', 'main')
        self.denied('git push', 'OPS-001')
        self.denied('git push origin HEAD', 'OPS-001')

    def test_the_remotes_own_default_branch_counts(self) -> None:
        git(self.repo, 'update-ref', 'refs/remotes/origin/trunk-line', 'HEAD')
        git(self.repo, 'symbolic-ref', 'refs/remotes/origin/HEAD', 'refs/remotes/origin/trunk-line')
        self.denied('git push origin trunk-line', 'OPS-001')

    def test_deletions_tags_and_everything_at_once_are_blocked(self) -> None:
        git(self.repo, 'tag', 'v1.0.0')
        for command in ('git push origin :old', 'git push --delete origin old', 'git push -d origin old',
                        'git push --prune origin', 'git push --mirror', 'git push --tags',
                        'git push --follow-tags', 'git push origin refs/tags/v1.0.0',
                        'git push origin tag v1.0.0', 'git push origin v1.0.0', 'git push --all origin'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-001')


class TestCommit(Sandbox):
    """GIT-001 and OPS-004: your user's identity, and the hooks left on."""

    def test_signing_off_as_a_person_passes(self) -> None:
        for command in ('git commit -s -m "feat(x): add y"', 'git commit -sm "msg"', 'git commit --signoff -m x',
                        f"git commit -m x --trailer 'Signed-off-by: {HUMAN}'", 'git commit -ms',
                        "git commit -m x --trailer 'Co-Authored-By: Claude <noreply@anthropic.com>'"):
            with self.subTest(command=command):
                self.allowed(command)

    def test_an_ai_identity_in_git_config_blocks_the_sign_off_and_the_author(self) -> None:
        git(self.repo, 'config', 'user.name', 'Claude')
        git(self.repo, 'config', 'user.email', 'noreply@anthropic.com')
        self.denied('git commit -s -m x', 'GIT-001')
        self.denied('git rebase --signoff main', 'GIT-001')
        self.denied('git cherry-pick -s abc123', 'GIT-001')
        self.denied('git commit -m x', 'GIT-001')
        self.allowed(f"git commit --author '{HUMAN}' -m x --trailer 'Signed-off-by: {HUMAN}'")
        self.allowed('git commit --amend --no-edit')
        self.allowed('git merge -s ours other')  # -s is a strategy for merge

    def test_an_ai_named_on_the_command_line_is_blocked(self) -> None:
        for command in ('git commit -m x --author "Claude <noreply@anthropic.com>"',
                        "git commit -m x --trailer 'Signed-off-by: Codex <codex@openai.com>'",
                        'git -c user.name=Copilot -c user.email=copilot@github.com commit -s -m x',
                        'GIT_AUTHOR_NAME=Claude GIT_AUTHOR_EMAIL=noreply@anthropic.com git commit -m x',
                        'git commit -m "feat(x): y\n\nSigned-off-by: Claude <noreply@anthropic.com>"'):
            with self.subTest(command=command):
                self.denied(command, 'GIT-001')

    def test_a_sign_off_in_a_here_document_counts(self) -> None:
        command = ("git commit -F - <<'EOF'\nfeat(x): y\n\nbody\n\n"
                   'Signed-off-by: Claude <noreply@anthropic.com>\nEOF')
        self.denied(command, 'GIT-001')
        command = f'git commit -m "$(cat <<\'EOF\'\nfeat(x): y\n\nSigned-off-by: {HUMAN}\nEOF\n)"'
        self.allowed(command)

    def test_skipping_hooks_is_blocked(self) -> None:
        for command in ('git commit --no-verify -m x', 'git commit -n -m x', 'git commit -sn -m x',
                        'git push --no-verify origin feat/work', 'HUSKY=0 git commit -m x',
                        'SKIP=gitleaks git commit -m x', 'git -c core.hooksPath=/dev/null commit -m x',
                        'git merge --no-verify other'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-004')


class TestIrreversible(Sandbox):
    """OPS-003: what git cannot undo, only when there is something to lose."""

    def dirty(self) -> None:
        (self.repo / 'README.md').write_text('# Changed\n', encoding='utf-8')

    def test_a_clean_tree_can_be_reset_and_checked_out(self) -> None:
        for command in ('git reset --hard', 'git checkout -- .', 'git restore .', 'git checkout -f main'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_uncommitted_work_is_protected(self) -> None:
        self.dirty()
        for command in ('git reset --hard', 'git reset --hard origin/main', 'git checkout -- .',
                        'git checkout .', 'git restore .', 'git checkout -f main', 'git switch --discard-changes main'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-003')
        for command in ('git restore --staged .', 'git checkout -- README.md', 'git restore README.md',
                        'git checkout -b feat/new', 'git stash', 'git reset --soft HEAD~1'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_deleting_untracked_files_stashes_and_unmerged_branches_is_blocked(self) -> None:
        for command in ('git clean -fd', 'git clean -xfd', 'git clean --force', 'git stash drop',
                        'git stash clear', 'git branch -D feat/old', 'git branch --delete --force feat/old',
                        'git filter-branch --tree-filter x', 'git filter-repo --path x', 'git reflog expire --all',
                        'git gc --prune=now', 'git update-ref -d refs/heads/x'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-003')
        for command in ('git clean -n', 'git clean -fdn', 'git branch -d feat/old', 'git gc', 'git stash list'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_rm_is_blocked_only_at_a_root_home_or_repository_folder(self) -> None:
        for command in ('rm -rf /', 'rm -rf ~', 'rm -rf ~/', 'rm -rf "$HOME"', 'rm -rf .', 'rm -rf ..',
                        'rm -rf *', 'rm -rf .git', 'rm -r /usr', 'sudo rm -rf /', 'sudo -u root rm -rf /',
                        f'rm -rf {self.home}', 'rm -fr /etc'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-003')
        for command in ('rm -rf build', 'rm -rf node_modules dist', 'rm -f notes.txt', 'rm -rf /tmp/scratch',
                        'rm -rf ~/scratch/old'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_databases_infrastructure_and_disks_are_blocked(self) -> None:
        for command in ('psql -c "DROP TABLE users"', 'mysql -e "drop database app"', 'dropdb app',
                        'sqlite3 app.db "TRUNCATE TABLE x"', 'redis-cli FLUSHALL', 'bin/rails db:drop',
                        'npx prisma migrate reset', 'terraform destroy', 'terraform apply -destroy',
                        'kubectl delete deployment web', 'helm uninstall web', 'aws ec2 terminate-instances --x',
                        'aws s3 rb s3://bucket', 'aws s3 rm s3://bucket --recursive', 'gcloud sql instances delete x',
                        'docker volume prune', 'docker system prune -a --volumes', 'mkfs.ext4 /dev/sdb',
                        'dd if=/dev/zero of=/dev/sda', ':(){ :|:& };:'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-003')
        for command in ('psql -c "select 1"', 'terraform plan', 'kubectl get pods', 'aws s3 ls',
                        'docker system prune', 'dd if=a of=b'):
            with self.subTest(command=command):
                self.allowed(command)


class TestGitHub(Sandbox):
    """OPS-001 and OPS-003 through gh, the REST API and GitHub's MCP tools."""

    def test_merging_is_your_users_call(self) -> None:
        for command in ('gh pr merge 3 --squash', 'gh pr merge', 'gh -R owner/repo pr merge 3',
                        'gh pr merge 3 --repo owner/repo --auto', 'gh api -X PUT repos/o/r/pulls/1/merge',
                        'gh api --method PUT -H "Accept: application/vnd.github+json" repos/o/r/pulls/1/merge',
                        'curl -X PUT https://api.github.com/repos/o/r/pulls/1/merge',
                        'gh repo sync --force'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-001')

    def test_settings_and_deletions_are_blocked(self) -> None:
        for command in ('gh repo delete o/r --yes', 'gh repo edit --visibility public', 'gh secret set X',
                        'gh release delete v1.0.0', 'gh api -X DELETE repos/o/r/git/refs/heads/x',
                        'gh api -X PATCH repos/o/r -f visibility=private',
                        'gh api repos/o/r/rulesets --input ruleset.json'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-003')

    def test_reading_and_proposing_pass(self) -> None:
        for command in ('gh pr create --fill', 'gh pr view 3', 'gh pr checks', 'gh api repos/o/r/pulls',
                        'gh api repos/o/r/issues/1/comments -f body=hi', 'gh run view 12 --log'):
            with self.subTest(command=command):
                self.allowed(command)

    def test_mcp_merges_ref_deletions_and_protected_writes_are_blocked(self) -> None:
        cases = [
            ('mcp__github__merge_pull_request', {'owner': 'o', 'repo': 'r', 'pullNumber': 1}, 'OPS-001'),
            ('mcp__github__enable_pr_auto_merge', {'pullNumber': 1}, 'OPS-001'),
            ('github-mcp-server-merge_pull_request', {}, 'OPS-001'),
            ('mcp__github__delete_branch', {'branch': 'x'}, 'OPS-001'),
            ('mcp__github__push_files', {'branch': 'main', 'files': []}, 'OPS-001'),
            ('mcp__github__create_or_update_file', {'branch': 'Development', 'path': 'a', 'content': 'b'},
             'OPS-001'),
            ('mcp__github__create_or_update_file', {'branch': 'feat/x', 'path': 'a', 'content': GITHUB_TOKEN},
             'SEC-001'),
        ]
        for tool, args, rule in cases:
            with self.subTest(tool=tool):
                verdict = self.edit(tool, **args)
                self.assertIsNotNone(verdict)
                self.assertEqual(verdict.rule, rule)
        for tool, args in (('mcp__github__create_pull_request', {'head': 'feat/x', 'base': 'main'}),
                           ('mcp__github__disable_pr_auto_merge', {'pullNumber': 1}),
                           ('mcp__github__push_files', {'branch': 'feat/x', 'files': []})):
            with self.subTest(tool=tool):
                self.assertIsNone(self.edit(tool, **args))


class TestSecrets(Sandbox):
    """SEC-001: a credential-shaped string never goes into a command or a file."""

    def test_credentials_are_blocked_without_being_repeated(self) -> None:
        tokens = [GITHUB_TOKEN, 'github_pat_' + 'A1b2C3d4E5' * 7, 'sk-ant-api03-' + 'x' * 40,
                  'AKIA' + 'ABCDEFGHIJKLMNOP', 'xoxb-' + '1234567890-' * 3, 'AIza' + 'b' * 35,
                  '-----BEGIN OPENSSH ' + 'PRIVATE KEY-----', 'npm_' + 'c' * 36, 'hf_' + 'd' * 34]
        for token in tokens:
            with self.subTest(token=token[:12]):
                verdict = self.verdict(f'export TOKEN={token}')
                self.assertEqual(verdict.rule, 'SEC-001')
                self.assertNotIn(token, verdict.line())
                verdict = self.edit('Write', file_path=str(self.repo / 'config.py'), content=f'KEY = "{token}"\n')
                self.assertEqual(verdict.rule, 'SEC-001')

    def test_ordinary_text_passes(self) -> None:
        for command in ('echo "$GITHUB_TOKEN" | gh auth login --with-token', 'grep -r "sk-" docs',
                        'export AWS_PROFILE=dev'):
            with self.subTest(command=command):
                self.allowed(command)
        self.assertIsNone(self.edit('Edit', file_path=str(self.repo / 'a.py'), old_string='a', new_string='b'))


class TestBlocks(Sandbox):
    """A block the hub renders is never edited by hand."""

    def setUp(self) -> None:
        super().setUp()
        self.region = render.region(BLOCK)
        self.agents = self.repo / 'AGENTS.md'
        self.agents.write_text(f'# Repo\n\n{self.region}\n## Commands\n\n- make check\n', encoding='utf-8')

    def test_edits_outside_the_block_pass(self) -> None:
        self.assertIsNone(self.edit('Edit', file_path=str(self.agents), old_string='- make check',
                                    new_string='- make check\n- make test'))
        new = self.agents.read_text(encoding='utf-8') + '\n## Gotchas\n\n- None.\n'
        self.assertIsNone(self.edit('Write', file_path=str(self.agents), content=new))

    def test_edits_inside_the_block_are_blocked(self) -> None:
        verdict = self.edit('Edit', file_path=str(self.agents), old_string='Never put a credential in a file.',
                            new_string='Credentials are fine.')
        self.assertEqual(verdict.rule, 'machine-written block')
        verdict = self.edit('MultiEdit', file_path=str(self.agents),
                            edits=[{'old_string': '- make check', 'new_string': '- make all'},
                                   {'old_string': '## Working rules', 'new_string': '## Rules'}])
        self.assertEqual(verdict.rule, 'machine-written block')
        verdict = self.edit('Write', file_path=str(self.agents), content='# Repo\n\nNo rules.\n')
        self.assertEqual(verdict.rule, 'machine-written block')

    def test_a_hand_made_block_is_blocked(self) -> None:
        fresh = self.repo / 'docs' / 'NEW.md'
        verdict = self.edit('Write', file_path=str(fresh), content=f'# New\n\n{self.region}')
        self.assertEqual(verdict.rule, 'machine-written block')
        self.assertIsNone(self.edit('Write', file_path=str(self.repo / 'test_x.py'),
                                    content=f'TEXT = """\n{self.region}"""\n'))

    def test_shell_writes_into_the_block_are_blocked(self) -> None:
        for command in ("sed -i 's/credential/key/' AGENTS.md", 'echo x >> AGENTS.md', 'echo x > AGENTS.md',
                        'cat other.md | tee AGENTS.md', 'cp other.md AGENTS.md', 'rm AGENTS.md',
                        "perl -pi -e 's/a/b/' AGENTS.md"):
            with self.subTest(command=command):
                self.denied(command, 'machine-written block')
        self.allowed("sed -n '1,5p' AGENTS.md")
        self.allowed('cat AGENTS.md > /tmp/copy.md')

    def test_a_patch_into_the_block_is_blocked(self) -> None:
        inside = ('*** Begin Patch\n*** Update File: AGENTS.md\n@@\n-- SEC-001: Never put a credential in a file.\n'
                  '+- SEC-001: Anything goes.\n*** End Patch\n')
        outside = ('*** Begin Patch\n*** Update File: AGENTS.md\n@@\n-- make check\n+- make all\n*** End Patch\n')
        verdict = self.edit('apply_patch', input=inside)
        self.assertEqual(verdict.rule, 'machine-written block')
        self.assertIsNone(self.edit('apply_patch', input=outside))
        verdict = self.edit('apply_patch', input='*** Begin Patch\n*** Delete File: AGENTS.md\n*** End Patch\n')
        self.assertEqual(verdict.rule, 'machine-written block')


class TestSelfProtection(Sandbox):
    """OPS-004: the guard stays registered, and hooks stay on."""

    def setUp(self) -> None:
        super().setUp()
        self.script = self.home / '.agents' / 'hooks' / 'intelligence-guard.py'
        self.settings = self.home / '.claude' / 'settings.json'
        self.script.parent.mkdir(parents=True)
        self.settings.parent.mkdir(parents=True)
        self.script.write_text('# guard\n', encoding='utf-8')
        entry = {'type': 'command', 'command': f'python3 {self.script} --app claude'}
        self.settings.write_text(json.dumps({'hooks': {'PreToolUse': [{'matcher': 'Bash', 'hooks': [entry]}]},
                                             'theme': 'dark'}, indent=2), encoding='utf-8')

    def test_the_guard_and_its_registration_cannot_be_removed(self) -> None:
        self.assertEqual(self.edit('Write', file_path=str(self.script), content='').rule, 'OPS-004')
        self.assertEqual(self.edit('Write', file_path=str(self.settings), content='{"theme": "light"}').rule,
                         'OPS-004')
        self.assertEqual(self.edit('Edit', file_path=str(self.settings),
                                   old_string=f'python3 {self.script} --app claude', new_string='true').rule,
                         'OPS-004')
        self.assertEqual(self.edit('Edit', file_path=str(self.settings), old_string='"theme": "dark"',
                                   new_string='"disableAllHooks": true').rule, 'OPS-004')
        for command in (f'rm {self.script}', f'mv {self.script} /tmp/x', f'echo {{}} > {self.settings}',
                        f"sed -i 's/guard//' {self.settings}", 'codex --dangerously-bypass-hook-trust exec x'):
            with self.subTest(command=command):
                self.denied(command, 'OPS-004')

    def test_other_settings_can_change(self) -> None:
        self.assertIsNone(self.edit('Edit', file_path=str(self.settings), old_string='"theme": "dark"',
                                    new_string='"theme": "light"'))
        new = self.settings.read_text(encoding='utf-8').replace('dark', 'light')
        self.assertIsNone(self.edit('Write', file_path=str(self.settings), content=new))


class TestPayloads(Sandbox):
    """Each app's payload reaches the same decision, and the verdict blocks in each."""

    def test_every_apps_shape_is_understood(self) -> None:
        cases = {
            'Claude Code': {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash',
                            'tool_input': {'command': 'git push --force'}, 'cwd': str(self.repo)},
            'Codex': {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash',
                      'tool_input': {'command': ['bash', '-lc', 'git push --force']}, 'cwd': str(self.repo)},
            'Copilot, camelCase': {'toolName': 'bash', 'toolArgs': json.dumps({'command': 'git push --force'}),
                                   'cwd': str(self.repo)},
            'Copilot, PascalCase': {'hook_event_name': 'PreToolUse', 'tool_name': 'Bash',
                                    'tool_input': {'command': 'git push --force', 'description': 'push'},
                                    'cwd': str(self.repo)},
            'Antigravity': {'tool_name': 'run_command', 'tool_input': {'CommandLine': 'git push --force'},
                            'cwd': str(self.repo)},
        }
        for app, payload in cases.items():
            with self.subTest(app=app):
                code, err = self.run_hook(payload)
                self.assertEqual(code, 2)
                self.assertIn('(OPS-001)', err)
                self.assertTrue(err.strip(), 'Codex blocks on exit 2 only with a reason on stderr')

    def test_harmless_and_unreadable_payloads_pass_silently(self) -> None:
        for payload in ({'tool_name': 'Read', 'tool_input': {'file_path': '/etc/hosts'}},
                        {'tool_name': 'Bash', 'tool_input': {'command': 'ls -la'}, 'cwd': str(self.repo)},
                        {}, []):
            with self.subTest(payload=payload):
                self.assertEqual(self.run_hook(payload), (0, ''))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(guard.main([], stdin='not json'), 0)

    def test_a_bug_in_the_guard_lets_the_call_through_and_says_so(self) -> None:
        with mock.patch.object(guard, 'decide', side_effect=RuntimeError('boom')):
            code, err = self.run_hook({'tool_name': 'Bash', 'tool_input': {'command': 'ls'}})
        self.assertEqual(code, 0)
        self.assertIn('internal error', err)

    def test_the_command_option_tries_one_command_by_hand(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(guard.main(['--command', 'ls']), 0)
            self.assertEqual(guard.main(['--command', 'git push --force']), 2)
        self.assertIn('allowed', out.getvalue())


class TestParsing(unittest.TestCase):
    """The shell reading underneath every check."""

    def test_nested_and_chained_commands_are_all_found(self) -> None:
        here = pathlib.Path('/tmp')
        found = [command.words[0] for command in guard.simple_commands(
            'a && b; c | d || e\nf $(g) "$(h)" `i` & bash -c "j k" ; eval l m', here)]
        for name in 'abcdefghijl':
            self.assertIn(name, found)

    def test_here_document_bodies_are_not_commands(self) -> None:
        kept, bodies = guard.strip_heredocs("cat <<'EOF' > f\ngit push --force\nEOF\necho done")
        self.assertNotIn('git push', kept)
        self.assertIn('git push --force', bodies)
        self.assertEqual(guard.strip_heredocs('cat <<< "word"\nnext')[0], 'cat <<< "word"\nnext')

    def test_a_cd_moves_the_commands_after_it(self) -> None:
        commands = guard.simple_commands('cd sub && git status', pathlib.Path('/repo'))
        self.assertEqual(commands[-1].cwd, pathlib.Path('/repo/sub'))

    def test_redirections_and_wrappers_are_peeled_off(self) -> None:
        (command,) = guard.simple_commands('FOO=1 sudo -u root nice -n 5 git status 2>&1 > out.md',
                                           pathlib.Path('/r'))
        self.assertEqual(command.words, ['git', 'status'])
        self.assertEqual(command.env, {'FOO': '1'})
        self.assertEqual(command.writes, ['out.md'])

    def test_the_region_pattern_agrees_with_the_renderers(self) -> None:
        rendered = render.region(BLOCK)
        texts = [rendered, f'# Title\n\n{rendered}\nafter\n', rendered.replace('BEGIN', 'BEGAN'),
                 rendered.replace('<!-- INTELLIGENCE:END -->', ''), '  ' + rendered, rendered.replace('\n', '\r\n')]
        for text in texts:
            with self.subTest(text=text[:40]):
                self.assertEqual(bool(guard.REGION.search(text)), bool(render.REGION.search(text)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
