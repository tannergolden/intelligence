#!/usr/bin/env python3
"""Block the few tool calls the universal rules forbid outright, before they run.

WHY THIS EXISTS. Prose rules are followed most of the time, and a few of
them guard against damage nobody can take back: a force-push, a merge of an
agent's own pull request, a deleted working tree, a credential in a commit.
Each app's pre-tool hook pipes the call it is about to make to this script,
which denies it with exit 2 and one line on stderr saying why and what to do
instead. Exit 2 with a reason on stderr is the one verdict that blocks in
every app this kit supports, so the script never allows and never asks: it
denies or stays silent, and each app's own permissions decide the rest.

WHAT IT BLOCKS, and the rule behind each:

- OPS-001: pushing to a default or protected branch, force-pushing without
  `--force-with-lease`, deleting or pruning remote refs, pushing tags, and
  merging a pull request, through `git`, `gh` or a GitHub MCP tool
- OPS-003: what git cannot undo, when there is something to lose: `git
  reset --hard` or a whole-tree checkout over uncommitted work, `git clean
  -f`, dropped stashes, `git branch -D`, history rewrites, `rm -r` aimed at
  a root or home folder, and deleting databases, cloud resources or
  repository settings
- OPS-004: `--no-verify`, hooks switched off for one command, and edits
  that would remove this guard or its registrations
- GIT-001: a commit that git would author, or sign off, as an AI's identity;
  `git commit -s` passes whenever git's identity is your user's
- SEC-001: a credential-shaped string in a command or in a file being written
- the hub's blocks: a hand edit inside the rules block of `AGENTS.md` or
  the prompts block of `docs/Prompts.md`, which the next sync would
  overwrite anyway

It is a seatbelt, not a sandbox. It reads a command the way a careful
reviewer would and catches the honest mistake; a determined workaround gets
past it, which is what OPS-004, the rulesets and CI are for. It runs on the
Python 3.9 that macOS ships, with the standard library only, makes no network
calls, and finishes in milliseconds.

Run it:

    echo '{"tool_name": "Bash", "tool_input": {"command": "git push -f"}}' | python3 guard.py --app claude
    python3 guard.py --command 'git push --force origin main'   # try a command by hand
"""

# Part of tannergolden/intelligence's home kit, which replaces this file on every install.

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
from collections.abc import Iterable, Mapping

# Branch names that are protected in every repository this kit serves, on top
# of whatever branch a remote reports as its default: the standards' four
# long-lived branches, and the usual default names elsewhere.
PROTECTED = {'Experimental', 'Development', 'Preview', 'Release', 'main', 'master', 'development',
             'develop', 'trunk'}

# Who an author or sign-off must never be (GIT-001). Co-Authored-By is not
# checked: naming the model there is what GIT-013 asks for.
AI_IDENTITY = re.compile(
    r'\b(claude|anthropic|openai|chatgpt|codex|copilot|gemini|antigravity|cursor|grok|x\.ai|devin)\b',
    re.I,
)

# Credential shapes with almost no false positives. Each names its kind,
# because a denial says where a credential is, never what it is.
SECRETS = (
    ('a GitHub token', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{60,255})\b')),
    ('an Anthropic key', re.compile(r'\bsk-ant-[A-Za-z0-9_-]{32,}')),
    ('an OpenAI key', re.compile(r'\bsk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{40,}|\bsk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}')),
    ('an AWS access key', re.compile(r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b')),
    ('a Slack token', re.compile(r'\bxox[abposr]-[0-9A-Za-z-]{20,}')),
    ('a Google API key', re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b')),
    ('a Stripe live key', re.compile(r'\b[rs]k_live_[0-9A-Za-z]{24,}')),
    ('an npm token', re.compile(r'\bnpm_[A-Za-z0-9]{36}\b')),
    ('a PyPI token', re.compile(r'\bpypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{50,}')),
    ('a GitLab token', re.compile(r'\bglpat-[0-9A-Za-z_-]{20,}')),
    ('a Hugging Face token', re.compile(r'\bhf_[A-Za-z0-9]{34,}\b')),
    ('a private key', re.compile(r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----')),
)

# The blocks the hub renders, in the files that carry one: the rules, and the
# prompts. The pattern matches render.py's for the one and prompts.py's for the
# other.
REGION = re.compile(
    r'^<!-- (?P<name>INTELLIGENCE(?::PROMPTS)?):BEGIN sha256:[0-9a-f]{64} -->[ \t]*\r?\n'
    r'.*?'
    r'^<!-- (?P=name):END -->[ \t]*(?:\r?\n|\Z)',
    re.M | re.S,
)
MARKER = re.compile(r'^<!-- INTELLIGENCE(?::PROMPTS)?:(?:BEGIN|END)\b', re.M)
BLOCK_SUFFIXES = ('.md', '.markdown', '.mdc')

SHELL_TOOLS = {'bash', 'powershell', 'pwsh', 'shell', 'run_shell_command', 'exec_command', 'local_shell',
               'shell_command', 'run_command', 'run_terminal_cmd', 'terminal', 'execute', 'exec'}
PATH_KEYS = ('file_path', 'filePath', 'path', 'notebook_path', 'TargetFile', 'target_file', 'AbsolutePath')
CONTENT_KEYS = ('content', 'contents', 'file_text', 'CodeContent', 'text', 'new_source')
OLD_KEYS = ('old_string', 'old_str', 'oldString', 'TargetContent')
NEW_KEYS = ('new_string', 'new_str', 'newString', 'ReplacementContent')
COMMAND_KEYS = ('command', 'cmd', 'CommandLine', 'commandLine', 'script')

# Commands that run another command, and the flags of theirs that take a value.
WRAPPERS = {
    'sudo': {'-u', '-g', '-C', '-D', '-h', '-p', '-r', '-t', '-U'}, 'doas': {'-u', '-C'},
    'env': {'-u', '-C', '-S'}, 'command': set(), 'builtin': set(), 'exec': {'-a'}, 'nohup': set(),
    'time': set(), 'nice': {'-n'}, 'ionice': {'-c', '-n', '-p'}, 'timeout': {'-s', '-k'},
    'xargs': {'-I', '-n', '-L', '-P', '-d', '-E', '-s', '-a'}, 'stdbuf': set(), 'caffeinate': set(),
}
SHELLS = {'sh', 'bash', 'zsh', 'dash', 'ksh', 'fish'}
SEPARATORS = {';', '&&', '||', '|', '&', '\n', '(', ')', '|&', ';;', '{', '}'}
REDIRECTS = {'>', '>>', '>|', '&>', '&>>', '<>'}
READS = {'<', '<<<', '>&', '<&', '&>&'}
HEREDOC = re.compile(r"(?<!<)<<(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
ASSIGNMENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*=')
HOOK_SKIPS = {'HUSKY': {'0', 'false'}, 'HUSKY_SKIP_HOOKS': None, 'SKIP': None, 'LEFTHOOK': {'0', 'false'}}
DB_CLIENTS = {'psql', 'mysql', 'mariadb', 'sqlite3', 'sqlcmd', 'mongosh', 'mongo', 'cockroach', 'duckdb'}
DB_DROP = re.compile(r'\b(drop\s+(database|schema|table)|truncate\s+(table\s+)?\w)', re.I)


@dataclasses.dataclass(frozen=True)
class Verdict:
    """Why a call is denied: the rule, what is wrong, and what to do instead."""

    rule: str
    reason: str
    instead: str

    def line(self) -> str:
        return f'intelligence guard blocked this ({self.rule}): {self.reason}. {self.instead}'


@dataclasses.dataclass(frozen=True)
class Call:
    """One tool call, in the same shape whichever app made it."""

    tool: str
    args: dict
    cwd: pathlib.Path


@dataclasses.dataclass
class Simple:
    """One simple command: its words, the variables set before it, where it runs, and what it writes."""

    words: list[str]
    env: dict[str, str]
    cwd: pathlib.Path
    writes: list[str] = dataclasses.field(default_factory=list)


def normalize(payload: Mapping) -> Call:
    """The call inside a hook payload from Claude Code, Codex, Copilot (both casings) or Antigravity."""
    tool = str(payload.get('tool_name') or payload.get('toolName') or '')
    args = payload.get('tool_input', payload.get('toolArgs', payload.get('input', {})))
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            args = {'command': args}
    if not isinstance(args, dict):
        args = {}
    cwd = payload.get('cwd') or os.environ.get('CLAUDE_PROJECT_DIR') or os.getcwd()
    return Call(tool, args, pathlib.Path(str(cwd)))


def first(args: Mapping, keys: Iterable[str]) -> str | None:
    for key in keys:
        value = args.get(key)
        if isinstance(value, str):
            return value
    return None


def command_of(args: Mapping) -> str | None:
    for key in COMMAND_KEYS:
        value = args.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, list) and all(isinstance(part, str) for part in value):
            # Codex passes `["bash", "-lc", "<script>"]`; quoting keeps it one shell line.
            return shlex.join(value)
    return None


def patch_of(args: Mapping) -> str | None:
    for value in args.values():
        if isinstance(value, str) and value.lstrip().startswith('*** Begin Patch'):
            return value
    return None


def decide(call: Call, home: pathlib.Path) -> Verdict | None:
    """Why this call is denied, or None to let it through."""
    name = call.tool.lower()
    if 'mcp' in name or 'merge_pull_request' in name:
        # A remote tool: nothing it names is a local file, so only its intent and its text count.
        return check_mcp(name, call.args) or secret_in(strings(call.args), 'the tool call')
    patch = patch_of(call.args)
    if patch is not None:
        return check_patch(patch, call.cwd, home)
    command = command_of(call.args)
    path = first(call.args, PATH_KEYS)
    if command is not None and (name in SHELL_TOOLS or path is None):
        return check_command(command, call.cwd, home)
    if path is not None:
        return check_edit(call.args, resolve(path, call.cwd), home)
    return None


def strings(value: object) -> str:
    """Every string inside a tool's arguments, one per line."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return '\n'.join(strings(item) for item in value.values())
    if isinstance(value, list):
        return '\n'.join(strings(item) for item in value)
    return ''


def secret_in(text: str, where: str) -> Verdict | None:
    for kind, pattern in SECRETS:
        if pattern.search(text):
            return Verdict('SEC-001', f'{where} holds {kind}',
                           'Never put a credential in a command, file or commit; read it from the '
                           'environment or a secret store, and tell your user where you found it')
    return None


# --- shell commands -----------------------------------------------------------


def strip_heredocs(text: str) -> tuple[str, str]:
    """The command text without here-document bodies, and the bodies themselves.

    A body is data, not commands, so it is never parsed as commands; it is
    still scanned for credentials and sign-offs.
    """
    kept: list[str] = []
    bodies: list[str] = []
    pending: list[tuple[str, bool]] = []
    for line in text.split('\n'):
        if pending:
            delimiter, dash = pending[0]
            if (line.lstrip('\t') if dash else line).rstrip() == delimiter:
                pending.pop(0)
            else:
                bodies.append(line)
            continue
        kept.append(line)
        pending.extend((m.group(3), m.group(1) == '-') for m in HEREDOC.finditer(line))
    return '\n'.join(kept), '\n'.join(bodies)


def tokens(text: str) -> list[str]:
    lexer = shlex.shlex(text, posix=True, punctuation_chars='();<>|&\n')
    lexer.whitespace = ' \t\r'
    lexer.whitespace_split = True
    lexer.commenters = ''
    try:
        return list(lexer)
    except ValueError:
        # An unbalanced quote: fall back to words, which still find most mistakes.
        return text.replace(';', ' ; ').replace('&&', ' && ').replace('|', ' | ').split()


def substitutions(word: str) -> list[str]:
    """The commands inside `$( )` and backticks in one word."""
    found: list[str] = []
    start = word.find('$(')
    while start != -1:
        depth, index = 0, start + 1
        while index < len(word):
            if word[index] == '(':
                depth += 1
            elif word[index] == ')':
                depth -= 1
                if depth == 0:
                    break
            index += 1
        found.append(word[start + 2:index])
        start = word.find('$(', index)
    found.extend(re.findall(r'`([^`]*)`', word))
    return found


def simple_commands(text: str, cwd: pathlib.Path, depth: int = 0) -> list[Simple]:
    """Every simple command a shell line would run, nested ones included."""
    if depth > 4:
        return []
    found: list[Simple] = []
    words: list[str] = []
    for token in [*tokens(text), ';']:
        if token in SEPARATORS:
            if words:
                found.extend(expand(words, cwd, depth))
            words = []
            continue
        for inner in substitutions(token):
            found.extend(simple_commands(inner, cwd, depth + 1))
        words.append(token)
    # A `cd` earlier in the line moves the commands after it.
    here = cwd
    for command in found:
        command.cwd = here if command.cwd == cwd else command.cwd
        if command.words[:1] == ['cd'] and len(command.words) > 1:
            here = resolve(command.words[1], here)
    return found


def expand(words: list[str], cwd: pathlib.Path, depth: int) -> list[Simple]:
    """Peel redirections, assignments and wrappers off one command, and open `sh -c` and `eval`."""
    plain: list[str] = []
    writes: list[str] = []
    index = 0
    while index < len(words):
        word = words[index]
        if word in REDIRECTS or word in READS:
            if word in REDIRECTS and index + 1 < len(words):
                writes.append(words[index + 1])
            index += 2
            continue
        if word.isdigit() and index + 1 < len(words) and (words[index + 1] in REDIRECTS
                                                          or words[index + 1] in READS):
            index += 1  # a file descriptor number, as in 2>&1
            continue
        plain.append(word)
        index += 1
    words = plain
    env: dict[str, str] = {}
    while words and ASSIGNMENT.match(words[0]):
        key, _, value = words[0].partition('=')
        env[key] = value
        words = words[1:]
    while words and os.path.basename(words[0]) in WRAPPERS:
        valued = WRAPPERS[os.path.basename(words[0])]
        words = words[1:]
        while words and (words[0].startswith('-') or ASSIGNMENT.match(words[0])
                         or re.fullmatch(r'\d+(\.\d+)?[smhd]?', words[0])):
            if ASSIGNMENT.match(words[0]):
                key, _, value = words[0].partition('=')
                env[key] = value
            words = words[2:] if words[0] in valued else words[1:]
    if not words:
        return [Simple([':'], env, cwd, writes)] if writes else []
    program = os.path.basename(words[0])
    if program in SHELLS:
        for index, word in enumerate(words[1:], 1):
            if word.startswith('-') and 'c' in word.lstrip('-') and index + 1 < len(words):
                return simple_commands(words[index + 1], cwd, depth + 1)
    if program == 'eval':
        return simple_commands(' '.join(words[1:]), cwd, depth + 1)
    return [Simple(words, env, cwd, writes)]


def check_command(text: str, cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    verdict = secret_in(text, 'the command')
    if verdict:
        return verdict
    if re.search(r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}', text):
        return Verdict('OPS-003', 'the command is a fork bomb', 'Do not run it')
    commands = simple_commands(strip_heredocs(text)[0], cwd)
    if any(os.path.basename(c.words[0]) == 'git' and 'commit' in c.words for c in commands):
        # Here-document bodies are data, but a commit message written in one still counts.
        verdict = check_signoff_lines(text, 'the commit message')
        if verdict:
            return verdict
    for command in commands:
        verdict = check_simple(command, home)
        if verdict:
            return verdict
    return check_api_merge(text)


def check_simple(command: Simple, home: pathlib.Path) -> Verdict | None:
    words = command.words
    program = os.path.basename(words[0])
    checks = {
        'git': check_git,
        'gh': check_gh,
        'rm': check_rm,
    }
    if program in checks:
        verdict = checks[program](command, home)
        if verdict:
            return verdict
    verdict = check_destructive(program, words)
    if verdict:
        return verdict
    return check_writes(command, home)


def resolve(path: str, cwd: pathlib.Path) -> pathlib.Path:
    expanded = os.path.expandvars(os.path.expanduser(path))
    candidate = pathlib.Path(expanded)
    return candidate if candidate.is_absolute() else cwd / candidate


def git_output(cwd: pathlib.Path, *args: str) -> str:
    """One local git query; empty when git or the repository is not there."""
    try:
        done = subprocess.run(['git', '-C', str(cwd), *args], capture_output=True, text=True,
                              timeout=5, check=False)
    except (OSError, subprocess.SubprocessError):
        return ''
    return done.stdout.strip() if done.returncode == 0 else ''


@dataclasses.dataclass
class Git:
    """A git command split into where it runs, its config overrides, subcommand and arguments."""

    cwd: pathlib.Path
    config: dict[str, str]
    sub: str
    args: list[str]
    env: dict[str, str]

    def has(self, *flags: str) -> bool:
        return any(arg in flags or any(arg.startswith(f + '=') for f in flags if f.startswith('--'))
                   for arg in self.args)

    def short(self, letter: str, takes_value: str = '') -> bool:
        """Whether a short flag appears, alone or clustered (`-sn`), before any value it holds."""
        for arg in self.args:
            if arg == '--':
                return False
            if arg.startswith('-') and not arg.startswith('--') and len(arg) > 1:
                for char in arg[1:]:
                    if char == letter:
                        return True
                    if char in takes_value:
                        break
        return False

    def positionals(self, valued: Iterable[str] = ()) -> list[str]:
        found, skip = [], False
        valued = set(valued)
        for arg in self.args:
            if skip:
                skip = False
            elif arg in valued:
                skip = True
            elif not arg.startswith('-'):
                found.append(arg)
        return found

    def query(self, *args: str) -> str:
        overrides = [part for key, value in self.config.items() for part in ('-c', f'{key}={value}')]
        return git_output(self.cwd, *overrides, *args)

    def dirty(self) -> bool:
        return bool(self.query('status', '--porcelain', '--untracked-files=no'))


def parse_git(command: Simple) -> Git | None:
    words, cwd, config = command.words[1:], command.cwd, {}
    while words and words[0].startswith('-'):
        flag = words[0]
        if flag == '-C' and len(words) > 1:
            cwd = resolve(words[1], cwd)
            words = words[2:]
        elif flag == '-c' and len(words) > 1:
            key, _, value = words[1].partition('=')
            config[key.lower()] = value
            words = words[2:]
        elif flag in ('--git-dir', '--work-tree', '--namespace', '--exec-path') and len(words) > 1:
            words = words[2:]
        else:
            words = words[1:]
    if not words:
        return None
    return Git(cwd, config, words[0], words[1:], command.env)


def check_git(command: Simple, home: pathlib.Path) -> Verdict | None:
    git = parse_git(command)
    if git is None:
        return None
    if 'core.hookspath' in git.config or any(
            key in git.env and (allowed is None or git.env[key].lower() in allowed)
            for key, allowed in HOOK_SKIPS.items()):
        return Verdict('OPS-004', 'the command switches git hooks off for itself',
                       'Run it with the hooks on, and fix or report what they find')
    if git.has('--no-verify') or (git.sub == 'commit' and git.short('n', COMMIT_VALUED)):
        return Verdict('OPS-004', f'`git {git.sub}` skips the hooks with --no-verify',
                       'Run it without that flag, and fix or report what the hooks find')
    verdict = check_signoff(git)
    if verdict:
        return verdict
    handler = GIT_CHECKS.get(git.sub)
    return handler(git) if handler else None


# Short flags of `git commit` that take a value, so `-ms` is a message, not a sign-off.
COMMIT_VALUED = 'mFCctuS'
# Where `-s` means --signoff; for `git merge`, `-s` picks a strategy instead.
SHORT_SIGNOFF = {'commit', 'am', 'cherry-pick', 'revert'}
LONG_SIGNOFF = SHORT_SIGNOFF | {'rebase', 'merge', 'pull', 'format-patch'}


def check_signoff(git: Git) -> Verdict | None:
    """A sign-off git would add as the committer, when the committer is an AI (GIT-001)."""
    if git.sub not in LONG_SIGNOFF:
        return None
    if not (git.has('--signoff') or (git.sub in SHORT_SIGNOFF and git.short('s', COMMIT_VALUED))):
        return None
    name, email = identity(git, 'COMMITTER')
    if is_ai(f'{name} {email}'):
        return Verdict('GIT-001', f'`git {git.sub} --signoff` signs off as the committer, {name} <{email}>, '
                       "an AI's identity",
                       "Add --trailer 'Signed-off-by: <your user's name and email>' instead, "
                       'or ask your user whose identity to use')
    return None


def check_push(git: Git) -> Verdict | None:
    if git.short('n') or git.has('--dry-run'):
        return None
    force = git.has('--force') or git.short('f', 'o')
    if force:
        return Verdict('OPS-001', '`git push --force` can overwrite commits on the remote',
                       'Use --force-with-lease on a branch you created, or ask your user')
    if git.has('--delete') or git.short('d', 'o') or git.has('--prune') or git.has('--mirror'):
        return Verdict('OPS-001', 'the push deletes branches or tags on the remote',
                       'Leave deletions to your user')
    if git.has('--tags') or git.has('--follow-tags'):
        return Verdict('OPS-001', 'the push sends tags, which only the release workflow creates',
                       'Push the branch alone')
    if git.has('--all') or git.has('--branches'):
        return Verdict('OPS-001', 'the push sends every branch, protected ones included',
                       'Push the one branch you are working on')
    positionals = git.positionals(('-o', '--push-option', '--repo', '--receive-pack', '--exec'))
    remote = positionals[0] if positionals else ''
    refspecs = positionals[1:]
    protected = PROTECTED | default_branches(git, remote)
    if not refspecs:
        branch = git.query('rev-parse', '--abbrev-ref', 'HEAD')
        if branch in protected:
            return pushes_protected(branch)
        return None
    if refspecs[0] == 'tag' or any(spec.lstrip('+').startswith('refs/tags/') for spec in refspecs):
        return Verdict('OPS-001', 'the push sends a tag, which only the release workflow creates',
                       'Push the branch alone')
    for spec in refspecs:
        if spec.startswith('+'):
            return Verdict('OPS-001', f'`{spec}` force-pushes, which can overwrite commits on the remote',
                           'Use --force-with-lease on a branch you created, or ask your user')
        source, colon, target = spec.partition(':')
        if colon and not source:
            return Verdict('OPS-001', f'`{spec}` deletes a branch or tag on the remote',
                           'Leave deletions to your user')
        target = target if colon else source
        if target == 'HEAD':
            target = git.query('rev-parse', '--abbrev-ref', 'HEAD')
        target = target.removeprefix('refs/heads/')
        if target in protected:
            return pushes_protected(target)
        if not colon and git.query('rev-parse', '--verify', '--quiet', f'refs/tags/{source}'):
            if not git.query('rev-parse', '--verify', '--quiet', f'refs/heads/{source}'):
                return Verdict('OPS-001', f'`{source}` is a tag, which only the release workflow pushes',
                               'Push the branch alone')
    return None


def pushes_protected(branch: str) -> Verdict:
    return Verdict('OPS-001', f'the push goes straight to `{branch}`, a protected branch',
                   'Push a branch of your own and open a pull request, if your user asked for one')


def default_branches(git: Git, remote: str) -> set[str]:
    names = set()
    for name in {remote or 'origin', 'origin'}:
        head = git.query('symbolic-ref', '--quiet', '--short', f'refs/remotes/{name}/HEAD')
        if head:
            names.add(head.split('/', 1)[-1])
    return names


def check_commit(git: Git) -> Verdict | None:
    """An author or Signed-off-by that names an AI (GIT-001); -s is check_signoff's."""
    for value in values(git.args, '--trailer'):
        if re.match(r'\s*signed-off-by\s*[:=]', value, re.I) and is_ai(value):
            return Verdict('GIT-001', "the commit's Signed-off-by names an AI",
                           "Sign off as your user, or ask whose identity to use")
    for value in values(git.args, '--author'):
        if is_ai(value):
            return Verdict('GIT-001', f"the commit's author, {value}, is an AI's identity",
                           "Author it as your user, or ask whose identity to use")
    if not values(git.args, '--author') and not (git.has('--amend') and not git.has('--reset-author')):
        name, email = identity(git, 'AUTHOR')
        if is_ai(f'{name} {email}'):
            return Verdict('GIT-001', f'git would author this commit as {name} <{email}>, an AI\'s identity',
                           "Ask your user whose name and email to use, then pass --author 'Name <email>'")
    return None


def identity(git: Git, role: str) -> tuple[str, str]:
    """The name and email git would record for AUTHOR or COMMITTER."""
    name = git.env.get(f'GIT_{role}_NAME') or os.environ.get(f'GIT_{role}_NAME')
    email = git.env.get(f'GIT_{role}_EMAIL') or os.environ.get(f'GIT_{role}_EMAIL')
    name = name or git.config.get('user.name') or git.query('config', 'user.name')
    email = email or git.config.get('user.email') or git.query('config', 'user.email')
    return name, email


def values(args: list[str], flag: str) -> list[str]:
    found = []
    for index, arg in enumerate(args):
        if arg == flag and index + 1 < len(args):
            found.append(args[index + 1])
        elif arg.startswith(flag + '='):
            found.append(arg[len(flag) + 1:])
    return found


def is_ai(text: str) -> bool:
    return bool(AI_IDENTITY.search(text))


def check_signoff_lines(text: str, where: str) -> Verdict | None:
    for line in re.findall(r'(?im)^\W*signed-off-by:\s*(.+)$', text):
        if is_ai(line):
            return Verdict('GIT-001', f'{where} carries a Signed-off-by for an AI, {line.strip()}',
                           "Sign off as your user, or ask whose identity to use")
    return None


def check_reset(git: Git) -> Verdict | None:
    if git.has('--hard') and git.dirty():
        return lost('`git reset --hard` throws away the uncommitted changes in this working tree')
    return None


def check_clean(git: Git) -> Verdict | None:
    if (git.has('--force') or git.short('f', 'e')) and not (git.has('--dry-run') or git.short('n', 'e')):
        return lost('`git clean -f` deletes untracked files, which git cannot bring back')
    return None


def check_checkout(git: Git) -> Verdict | None:
    whole_tree = any(arg in ('.', ':/', '*', ':(top)') for arg in git.args)
    forced = git.has('--force', '--discard-changes') or git.short('f', 'bBc')
    if git.sub == 'restore' and (git.has('--staged') or git.short('S')) and not (
            git.has('--worktree') or git.short('W')):
        return None
    if (forced or whole_tree) and git.dirty():
        return lost(f'`git {git.sub}` here throws away uncommitted changes across the working tree')
    return None


def check_stash(git: Git) -> Verdict | None:
    if git.args[:1] in (['drop'], ['clear']):
        return lost(f'`git stash {git.args[0]}` deletes stashed work')
    return None


def check_branch(git: Git) -> Verdict | None:
    if git.short('D') or (git.has('--delete') and git.has('--force')) or (
            git.short('d') and git.short('f')):
        return lost('`git branch -D` deletes the branch even if its commits were never merged',
                    'Use `git branch -d`, which refuses to drop unmerged commits, or ask your user')
    return None


def rewrites(git: Git) -> Verdict | None:
    if git.sub in ('filter-branch', 'filter-repo'):
        return lost(f'`git {git.sub}` rewrites history')
    if git.sub == 'reflog' and git.args[:1] in (['expire'], ['delete']):
        return lost('the reflog is how git undoes mistakes; this deletes it')
    if git.sub == 'gc' and any(arg.startswith('--prune=') and arg[8:] in ('now', 'all') for arg in git.args):
        return lost('`git gc --prune=now` deletes unreachable commits for good')
    if git.sub == 'update-ref' and git.short('d'):
        return lost('`git update-ref -d` deletes a ref outright')
    return None


def lost(reason: str, instead: str = '') -> Verdict:
    return Verdict('OPS-003', reason,
                   instead or 'Show your user the command and let them run it if they want it')


GIT_CHECKS = {
    'push': check_push,
    'commit': check_commit,
    'reset': check_reset,
    'clean': check_clean,
    'checkout': check_checkout,
    'restore': check_checkout,
    'switch': check_checkout,
    'stash': check_stash,
    'branch': check_branch,
    'filter-branch': rewrites,
    'filter-repo': rewrites,
    'reflog': rewrites,
    'gc': rewrites,
    'update-ref': rewrites,
}


GH_VALUED = {'-R', '--repo', '--hostname'}
GH_API_VALUED = {'-X', '--method', '-H', '--header', '-f', '-F', '--field', '--raw-field', '--input',
                 '-q', '--jq', '-t', '--template', '--cache', '--hostname', '-p', '--preview'}


def bare(words: list[str], valued: set[str]) -> list[str]:
    """The words that are neither flags nor the values those flags take."""
    found, skip = [], False
    for word in words:
        if skip:
            skip = False
        elif word in valued:
            skip = True
        elif not word.startswith('-'):
            found.append(word)
    return found


def check_gh(command: Simple, home: pathlib.Path) -> Verdict | None:
    words = command.words[1:]
    group, action = [*bare(words, GH_VALUED), '', ''][:2]
    if group == 'pr' and action == 'merge':
        return Verdict('OPS-001', '`gh pr merge` merges a pull request, which stays your user\'s call',
                       'Tell your user the pull request is ready to merge')
    if group == 'repo' and action == 'sync' and ('--force' in words or '-f' in words):
        return Verdict('OPS-001', '`gh repo sync --force` overwrites the branch',
                       'Ask your user')
    settings = {('repo', 'delete'), ('repo', 'archive'), ('repo', 'rename'), ('repo', 'edit'),
                ('secret', 'set'), ('secret', 'delete'), ('secret', 'remove'), ('variable', 'set'),
                ('variable', 'delete'), ('release', 'delete'), ('release', 'delete-asset'),
                ('label', 'delete'), ('issue', 'delete'), ('workflow', 'disable'), ('ruleset', 'delete'),
                ('cache', 'delete'), ('run', 'delete'), ('codespace', 'delete')}
    if (group, action) in settings:
        return lost(f'`gh {group} {action}` changes repository settings or deletes what cannot come back')
    if group == 'api':
        return check_gh_api(words[words.index('api') + 1:])
    return None


def check_gh_api(args: list[str]) -> Verdict | None:
    method = 'GET'
    for flag in ('-X', '--method'):
        found = values(args, flag)
        if found:
            method = found[-1].upper()
    if method == 'GET' and any(arg in ('-f', '-F', '--field', '--raw-field', '--input') for arg in args):
        method = 'POST'
    path = next(iter(bare(args, GH_API_VALUED)), '')
    if method == 'PUT' and re.search(r'/pulls/[^/]+/merge\b', path):
        return Verdict('OPS-001', 'the API call merges a pull request, which stays your user\'s call',
                       'Tell your user the pull request is ready to merge')
    if method == 'DELETE':
        return lost(f'`gh api -X DELETE {path}` deletes what cannot come back')
    if method in ('PUT', 'PATCH', 'POST') and re.search(
            r'^/?repos/[^/]+/[^/]+/?$|/(branches/[^/]+/protection|rulesets|actions/secrets|'
            r'actions/variables|collaborators|hooks|environments|actions/permissions)', path):
        return lost('the API call changes repository settings')
    return None


def check_api_merge(text: str) -> Verdict | None:
    if re.search(r'api\.github\.com/repos/[^\s/]+/[^\s/]+/pulls/\d+/merge', text) and re.search(
            r'(-X|--request)\s*PUT', text):
        return Verdict('OPS-001', 'the request merges a pull request, which stays your user\'s call',
                       'Tell your user the pull request is ready to merge')
    return None


def check_rm(command: Simple, home: pathlib.Path) -> Verdict | None:
    words = command.words[1:]
    flags = ''.join(word[1:] for word in words if word.startswith('-') and not word.startswith('--'))
    recursive = 'r' in flags or 'R' in flags or '--recursive' in words
    targets = [word for word in words if not word.startswith('-')]
    for target in targets:
        path = resolve(target, command.cwd)
        if recursive and catastrophic(target, path, home):
            return lost(f'`rm -r {target}` deletes a root, home or repository folder')
        if has_region(path):
            return block_edit(path)
    return None


def catastrophic(raw: str, path: pathlib.Path, home: pathlib.Path) -> bool:
    if raw.rstrip('/') in ('', '~', '.', '..', '*', '$HOME', '${HOME}') or raw in ('/*', '~/*', './*'):
        return True
    try:
        real = pathlib.Path(os.path.normpath(str(path)))
    except (OSError, ValueError):
        return False
    tops = {pathlib.Path('/'), home, home.parent}
    tops |= {pathlib.Path('/') / name for name in ('bin', 'boot', 'dev', 'etc', 'home', 'lib', 'opt',
                                                    'private', 'root', 'sbin', 'System', 'usr',
                                                    'Users', 'var', 'Library', 'Applications')}
    return real in tops or real.name == '.git'


def check_destructive(program: str, words: list[str]) -> Verdict | None:
    joined = ' '.join(words)
    if program.startswith('mkfs') or program in ('fdisk', 'sfdisk', 'wipefs') or (
            program == 'diskutil' and re.search(r'\berase|\bpartitionDisk|\bzeroDisk', joined)):
        return lost(f'`{program}` erases a disk')
    if program == 'dd' and any(word.startswith('of=/dev/') for word in words):
        return lost('`dd` writes straight onto a device')
    if program in ('chmod', 'chown') and ('-R' in words or '--recursive' in words) and any(
            word in ('/', '~', '$HOME') for word in words):
        return lost(f'`{program} -R` on a root or home folder')
    if program in ('dropdb', 'dropuser') or (program in DB_CLIENTS and DB_DROP.search(joined)) or (
            program == 'redis-cli' and re.search(r'\bflush(all|db)\b', joined, re.I)):
        return lost('the command deletes a database or its data')
    if re.search(r'\bdb:(drop|reset|purge)\b', joined) or (program in ('prisma', 'npx', 'pnpm', 'bunx')
                                                            and 'migrate reset' in joined):
        return lost('the command deletes a database or its data')
    cloud = (
        (program in ('terraform', 'tofu', 'pulumi') and ('destroy' in words or '-destroy' in words))
        or (program == 'kubectl' and 'delete' in words)
        or (program == 'helm' and ('uninstall' in words or 'delete' in words))
        or (program == 'aws' and any(re.match(r'(delete|terminate|remove|deregister)-', w) for w in words))
        or (program == 'aws' and 's3' in words and ('rb' in words or ('rm' in words and '--recursive' in words)))
        or (program in ('gcloud', 'az', 'doctl') and 'delete' in words)
        or (program in ('fly', 'flyctl') and 'destroy' in words)
        or (program == 'heroku' and any(w in ('apps:destroy', 'pg:reset') for w in words))
        or (program == 'vercel' and words[1:2] in (['rm'], ['remove']))
        or (program == 'supabase' and 'reset' in words)
        or (program == 'docker' and words[1:3] in (['volume', 'rm'], ['volume', 'prune']))
        or (program == 'docker' and words[1:3] == ['system', 'prune'] and '--volumes' in words)
    )
    if cloud:
        return lost(f'`{program}` here deletes infrastructure or the data it holds')
    return None


def check_writes(command: Simple, home: pathlib.Path) -> Verdict | None:
    """Shell writes into a rendered block, or onto the guard and its registrations."""
    words = command.words
    program = os.path.basename(words[0])
    operands = [word for word in words[1:] if not word.startswith('-')]
    targets = list(command.writes)
    if program in ('tee', 'truncate'):
        targets += operands
    if program in ('sed', 'perl', 'ruby') and any(re.match(r'-[a-zA-Z]*i', word) or word.startswith('--in-place')
                                                    for word in words[1:]):
        targets += operands[1:]  # the first operand is the script
    if program in ('cp', 'mv', 'install', 'ln') and operands:
        targets.append(operands[-1])
    if program in ('rm', 'mv', 'chmod', 'chown', 'unlink', 'shred'):
        targets += operands  # removing or moving the guard is as good as editing it
    for target in targets:
        path = resolve(target, command.cwd)
        if has_region(path):
            return block_edit(path)
        if protects(path, home):
            return tampers(path)
    joined = ' '.join(words)
    if 'disableAllHooks' in joined or '--dangerously-bypass-hook-trust' in joined:
        return Verdict('OPS-004', 'the command turns hooks off', 'Leave the hooks on, and report what blocked you')
    return None


# --- file edits ---------------------------------------------------------------


def has_region(path: pathlib.Path) -> bool:
    if not str(path).endswith(BLOCK_SUFFIXES):
        return False
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return False
    return bool(REGION.search(text))


def block_edit(path: pathlib.Path) -> Verdict:
    return Verdict('machine-written block', f'{path.name} holds a block that tannergolden/intelligence renders, '
                   'and a hand edit there is overwritten by the next sync',
                   'Leave the block as it is; change it in the hub, or tell your user')


def tampers(path: pathlib.Path) -> Verdict:
    return Verdict('OPS-004', f'the change would remove or alter the guard registered in {path}',
                   'Leave the guard in place, and report what it blocked')


def guard_files(home: pathlib.Path) -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    """The files that are wholly the guard's, and the shared files that register it."""
    codex = pathlib.Path(os.environ['CODEX_HOME']) if os.environ.get('CODEX_HOME') else home / '.codex'
    owned = [home / '.agents' / 'hooks' / 'intelligence-guard.py', home / '.copilot' / 'hooks' / 'intelligence.json']
    shared = [home / '.claude' / 'settings.json', codex / 'hooks.json', home / '.gemini' / 'config' / 'hooks.json']
    return owned, shared


def protects(path: pathlib.Path, home: pathlib.Path) -> bool:
    owned, shared = guard_files(home)
    return path in owned or path in shared


def check_edit(args: Mapping, path: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    new_text = first(args, CONTENT_KEYS)
    olds = [first(args, OLD_KEYS)] + [first(edit, OLD_KEYS) for edit in args.get('edits', [])
                                      if isinstance(edit, dict)]
    news = [first(args, NEW_KEYS)] + [first(edit, NEW_KEYS) for edit in args.get('edits', [])
                                      if isinstance(edit, dict)]
    olds = [old for old in olds if old]
    news = [new for new in news if new]
    written = '\n'.join(text for text in [new_text, *news] if text)
    verdict = secret_in(written, f'the text being written to {path.name}')
    if verdict:
        return verdict
    if path.name in ('COMMIT_EDITMSG', 'MERGE_MSG'):
        return check_signoff_lines(written, f'the text written to {path.name}')
    owned, shared = guard_files(home)
    if path in owned:
        return tampers(path)
    if path in shared:
        return check_registration(path, new_text, olds, news)
    if not str(path).endswith(BLOCK_SUFFIXES):
        return None
    try:
        current = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        current = ''
    regions = [match.group(0) for match in REGION.finditer(current)]
    if new_text is not None:
        if any(region not in new_text for region in regions) or (
                len(MARKER.findall(new_text)) > len(MARKER.findall(current))):
            return block_edit(path)
        return None
    spans = [(match.start(), match.end()) for match in REGION.finditer(current)]
    for old in olds:
        for match in re.finditer(re.escape(old), current):
            if any(match.start() < end and start < match.end() for start, end in spans):
                return block_edit(path)
    if len(MARKER.findall('\n'.join(news))) > len(MARKER.findall('\n'.join(olds))):
        return block_edit(path)
    return None


def check_registration(path: pathlib.Path, new_text: str | None, olds: list[str],
                       news: list[str]) -> Verdict | None:
    """An edit to a shared settings file that drops the guard or switches every hook off."""
    try:
        current = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        current = ''
    if new_text is not None:
        if 'intelligence-guard' in current and 'intelligence-guard' not in new_text:
            return tampers(path)
        added = new_text
    else:
        if any('intelligence-guard' in old for old in olds):
            return tampers(path)
        added = '\n'.join(news)
    if 'disableAllHooks' in added and 'disableAllHooks' not in current:
        return Verdict('OPS-004', 'the edit turns every hook off', 'Leave the hooks on, and report what blocked you')
    return None


def check_patch(patch: str, cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    """An apply_patch body: each file it adds, updates or deletes."""
    verdict = secret_in(patch, 'the patch')
    if verdict:
        return verdict
    sections = re.split(r'^\*\*\* (Add|Update|Delete) File: (.+)$', patch, flags=re.M)
    for index in range(1, len(sections) - 2, 3):
        action, name, body = sections[index], sections[index + 1].strip(), sections[index + 2]
        path = resolve(name, cwd)
        owned, shared = guard_files(home)
        if path in owned or (path in shared and 'intelligence-guard' in body):
            return tampers(path)
        if not str(path).endswith(BLOCK_SUFFIXES):
            continue
        added = [line[1:] for line in body.split('\n') if line.startswith('+')]
        removed = [line[1:] for line in body.split('\n') if line.startswith('-')]
        if any(MARKER.match(line) for line in added + removed):
            return block_edit(path)
        if action == 'Add':
            continue
        try:
            current = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        inside = {line.strip() for region in (m.group(0) for m in REGION.finditer(current))
                  for line in region.split('\n') if line.strip()}
        if inside and (action == 'Delete' or any(line.strip() in inside for line in removed if line.strip())):
            return block_edit(path)
    return None


def check_mcp(name: str, args: Mapping) -> Verdict | None:
    if 'merge_pull_request' in name or ('auto_merge' in name and 'disable' not in name):
        return Verdict('OPS-001', 'the tool merges a pull request, which stays your user\'s call',
                       'Tell your user the pull request is ready to merge')
    if re.search(r'delete_(branch|tag|ref)', name):
        return Verdict('OPS-001', 'the tool deletes a branch or tag on the remote',
                       'Leave deletions to your user')
    if re.search(r'delete_repo', name):
        return lost('the tool deletes a repository')
    branch = str(args.get('branch') or args.get('ref') or '').removeprefix('refs/heads/')
    if branch in PROTECTED and re.search(r'push_files|create_or_update_file|delete_file|update_ref', name):
        return pushes_protected(branch)
    return None


def main(argv: list[str] | None = None, stdin: str | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--app', default='unknown',
                        help='the app whose hook calls this: claude, codex, copilot or antigravity')
    parser.add_argument('--command', help='check one shell command by hand instead of reading a payload')
    args = parser.parse_args(argv)
    home = pathlib.Path(os.environ.get('HOME') or pathlib.Path.home())
    if args.command is not None:
        call = Call('Bash', {'command': args.command}, pathlib.Path.cwd())
    else:
        raw = sys.stdin.read() if stdin is None else stdin
        try:
            payload = json.loads(raw) if raw.strip() else {}
        except ValueError:
            return 0  # not a tool call this script understands; the app's own permissions decide
        if not isinstance(payload, dict):
            return 0
        call = normalize(payload)
    try:
        verdict = decide(call, home)
    except Exception as error:  # a bug here must never stop every tool call
        print(f'intelligence guard: internal error, call allowed: {error!r}', file=sys.stderr)
        return 0
    if verdict is None:
        if args.command is not None:
            print('allowed')
        return 0
    print(verdict.line(), file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
