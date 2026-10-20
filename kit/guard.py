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
  -f`, dropped stashes, `git branch -D`, history rewrites, a recursive
  delete aimed at a root, drive or home folder (`rm -r`, and on Windows
  `rmdir /s`, `del /s` and `Remove-Item -Recurse`), and deleting databases,
  cloud resources or repository settings
- OPS-004: `--no-verify`, hooks switched off for one command, and edits
  that would remove this guard, its registrations or the ask rules the kit
  adds to Claude Code's settings
- GIT-001: a commit that git would author, or sign off, as an AI's identity;
  `git commit -s` passes whenever git's identity is your user's
- SEC-001: a credential-shaped string in a command or in a file being
  written; reading a credential store in the home folder, such as a
  private SSH key or `~/.aws/credentials`, with a read tool or with a shell
  command that prints, searches, archives or copies it; and a command that
  prints a credential, such as `gh auth token`
- SEC-004: a download a shell or an interpreter runs before anyone reads
  it, piped, fed or substituted into it, or saved and run in the same line;
  and a package install that names a registry on the command line, other
  than the public default
- DOC-002: an em dash added to a Markdown file, a commit message or a pull
  request, in a repository tannergolden owns: one with no remote yet, or
  whose every remote is on github.com under tannergolden, so never a fork
  whose `upstream` is someone else's; a DOC-002 entry under `## Overrides`
  in the repository's `AGENTS.md` turns it off there
- the hub's blocks: a hand edit inside the rules block of `AGENTS.md` or
  the prompts block of `docs/Prompts.md`, which the next sync would
  overwrite anyway

It is a seatbelt, not a sandbox. It reads a command the way a careful
reviewer would and catches the honest mistake; a determined workaround gets
past it, which is what OPS-004, the rulesets and CI are for. It runs on the
Python 3.9 that macOS ships, with the standard library only, makes no network
calls, and finishes in milliseconds.

With `--remind` it prints the Invariants from Claude Code's home copy of the
rules instead, for the hook Claude Code runs after it compacts a conversation,
and prints nothing when that copy is missing.

Run it:

    echo '{"tool_name": "Bash", "tool_input": {"command": "git push -f"}}' | python3 guard.py --app claude
    python3 guard.py --command 'git push --force origin main'   # try a command by hand
    python3 guard.py --remind                                    # what a compaction brings back
"""

# Part of tannergolden/intelligence's home kit, which replaces this file on every install.

from __future__ import annotations

import argparse
import dataclasses
import functools
import glob
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
# Shell operators, longest first. The tokenizer returns a run of punctuation,
# such as `((` or `(<`, as one token, and these split it back apart.
OPERATORS = ('&>>', '<<<', '&&', '||', '|&', ';;', '<<', '>>', '&>', '>|', '<>', '<&', '>&', '<(', '>(',
             '(', ')', ';', '&', '|', '<', '>', '\n')
PUNCTUATION = set('();<>|&\n')

# Reading a credential store (SEC-001): the tools that only read, the commands
# that print a file or copy it, and the flags of each copier that take a value.
READ_TOOLS = {'read', 'view', 'view_file', 'read_file', 'readfile', 'read_many_files', 'notebookread', 'grep',
              'grep_search', 'search_file_content', 'glob'}
READ_PATH_KEYS = PATH_KEYS + ('absolute_path',)
PRINTERS = {'cat', 'tac', 'nl', 'less', 'more', 'most', 'head', 'tail', 'bat', 'batcat', 'view', 'base64', 'base32',
            'basenc', 'xxd', 'od', 'hexdump', 'hd', 'strings', 'grep', 'egrep', 'fgrep', 'rg', 'ag', 'sed', 'awk',
            'gawk', 'jq', 'yq'}
# Printers whose first operand is a pattern, script or filter, not a file, unless
# one of the first set of flags gives it; the second set are the flags that take
# a value. A file a flag names, such as `grep -f FILE`, is read as well.
PATTERN_FIRST = {
    'grep': ({'-e', '--regexp', '-f', '--file'},
             {'-e', '--regexp', '-f', '--file', '-m', '--max-count', '-A', '--after-context', '-B', '--before-context',
              '-C', '--context', '--include', '--exclude', '--exclude-dir', '--exclude-from', '-d', '--directories',
              '-D', '--devices', '--label', '--binary-files', '--group-separator'}),
    'rg': ({'-e', '--regexp', '-f', '--file'},
           {'-e', '--regexp', '-f', '--file', '-g', '--glob', '--iglob', '-t', '--type', '-T', '--type-not',
            '--type-add', '-m', '--max-count', '-A', '--after-context', '-B', '--before-context', '-C', '--context',
            '-j', '--threads', '-r', '--replace', '-E', '--encoding', '-d', '--max-depth', '-M', '--max-columns',
            '--max-filesize', '--pre', '--pre-glob', '--sort', '--sortr', '--color', '--colors', '--ignore-file',
            '--engine', '--path-separator', '--context-separator'}),
    'ag': (set(), {'-G', '--file-search-regex', '--ignore', '-A', '--after', '-B', '--before', '-C', '--context',
                   '-m', '--max-count', '--depth', '-p', '--path-to-ignore'}),
    'sed': ({'-e', '--expression', '-f', '--file'}, {'-e', '--expression', '-f', '--file', '-l', '--line-length'}),
    'awk': ({'-f', '--file'}, {'-f', '--file', '-F', '--field-separator', '-v', '--assign', '-i', '--include', '-l',
                               '--load'}),
    'jq': ({'-f', '--from-file'}, {'-f', '--from-file', '--indent', '-L', '--arg', '--argjson', '--slurpfile',
                                   '--rawfile'}),
}
PATTERN_FIRST.update({'egrep': PATTERN_FIRST['grep'], 'fgrep': PATTERN_FIRST['grep'], 'gawk': PATTERN_FIRST['awk'],
                      'yq': PATTERN_FIRST['jq']})
FILE_FLAGS = {'-f', '--file', '--from-file'}  # a flag that names a file to read the pattern from
TWO_VALUES = {'--arg', '--argjson', '--slurpfile', '--rawfile'}  # jq's flags that take a name and a value
COPIERS = {
    'cp': {'-t', '--target-directory', '-S', '--suffix'},
    'scp': {'-i', '-F', '-P', '-c', '-l', '-o', '-S', '-J', '-D', '-X'},
    'rsync': {'-e', '--rsh', '-f', '--filter', '--exclude', '--include', '--exclude-from', '--include-from',
              '--files-from', '-T', '--temp-dir', '--partial-dir', '--log-file', '--password-file'},
}
# Archivers, which copy what they are given, and the flags of each that take a value.
TAR_VALUED = set('fCTXbHKNV')
ZIP_VALUED = {'-b', '-n', '-t', '-tt', '-P', '-Z', '-O', '--out', '-x', '-i'}
# The stores, by their path under the home folder, and what each holds. Under
# ~/.ssh every file is a private key unless ssh_public() says it is not.
CREDENTIAL_FILES = {
    ('.aws', 'credentials'): 'AWS credentials',
    ('.docker', 'config.json'): 'Docker registry logins',
    ('.netrc',): 'netrc logins',
    ('_netrc',): 'netrc logins',
    ('.git-credentials',): 'stored git credentials',
    ('.config', 'git', 'credentials'): 'stored git credentials',
    ('.pypirc',): 'PyPI credentials',
    ('.npmrc',): 'npm registry tokens',
    ('.config', 'gh', 'hosts.yml'): "the GitHub CLI's token",
    ('.config', 'gcloud', 'credentials.db'): 'gcloud credentials',
    ('.config', 'gcloud', 'access_tokens.db'): 'gcloud credentials',
    ('.config', 'gcloud', 'application_default_credentials.json'): 'gcloud credentials',
    ('.kube', 'config'): 'Kubernetes credentials',
    ('.cargo', 'credentials'): 'a crates.io token',
    ('.cargo', 'credentials.toml'): 'a crates.io token',
    ('.gem', 'credentials'): 'RubyGems API keys',
    ('.gnupg', 'secring.gpg'): 'GnuPG private keys',
}
AZURE_TOKENS = ('msal_token_cache', 'service_principal_entries', 'accesstokens.json', 'tokencache.dat')
# The folders that hold a store and little else, so searching, archiving or
# copying one whole, or a folder inside one, reads the store too.
STORE_FOLDERS = (('.ssh',), ('.aws',), ('.azure',), ('.docker',), ('.gnupg',), ('.kube',), ('.config', 'gcloud'),
                 ('.config', 'gh'), ('.config', 'git'))
# The settings `aws configure get` would print that are secrets.
AWS_SECRETS = ('aws_secret_access_key', 'aws_session_token')
AWS_VALUED = {'--profile', '--region', '--output', '--endpoint-url', '--query', '--color', '--ca-bundle',
              '--cli-read-timeout', '--cli-connect-timeout'}

# The home folder as PowerShell and cmd name it too, and a drive's root: C:\
# on Windows, /c/ in Git Bash.
HOME_WORDS = re.compile(r'^(?:~|\$home|\$\{home\}|\$env:userprofile|\$\{env:userprofile\}|%userprofile%'
                        r'|\$env:home|\$\{env:home\})(?=/|$)', re.I)
DRIVE_ROOT = re.compile(r'[A-Za-z]:/?|/[A-Za-z]/?')
# Words in a cmd or PowerShell line, which keep their backslashes, and the
# commands there that delete or print.
WINDOWS_WORD = re.compile(r'''&&|\|\||[;&|\n()]|(?:"[^"]*"?|'[^']*'?|[^\s;&|()"'])+''')
WINDOWS_DELETES = {'rmdir', 'rd', 'del', 'erase', 'remove-item', 'ri', 'rm'}
WINDOWS_PRINTERS = {'get-content', 'gc', 'type', 'cat', 'more'}

# Running a download (SEC-004): what fetches a URL, what runs code, and the
# first letter of an interpreter's flag that hands it code inline or names a
# module, so its input is only data. A line that names no downloader skips
# these checks, so a long script costs no more than it must.
DOWNLOADERS = {'curl', 'wget', 'fetch', 'http', 'https', 'xh', 'iwr', 'irm', 'invoke-webrequest',
               'invoke-restmethod'}
DOWNLOAD_HINT = re.compile(r'\b(?:curl|wget|fetch|xh|iwr|irm|invoke-webrequest|invoke-restmethod)\b'
                           r'|\bhttps?(?=[\s\'"]|$)|downloadstring', re.I)
CODE_RUNNERS = re.compile(r'(?:bash|dash|zsh|ksh|mksh|ash|csh|tcsh|fish|sh)|python[0-9.]*|pypy[0-9.]*|perl|ruby'
                          r'|node(?:js)?|php|lua')
INLINE = {'python': 'cm', 'pypy': 'cm', 'perl': 'eE', 'ruby': 'e', 'node': 'ep', 'php': 'rfBRFE', 'lua': 'e'}
# The flags of a shell or interpreter that take a value, so the word after one is not the script it runs.
RUNNER_VALUED = {'sh': {'-o', '+o', '-O', '+O', '--rcfile', '--init-file'}, 'python': {'-W', '-X'},
                 'pypy': {'-W', '-X'}, 'perl': {'-I', '-M', '-m'}, 'ruby': {'-I', '-r'}, 'php': {'-c', '-d'},
                 'node': {'-r', '--require', '--import', '--loader'}, 'lua': {'-l'}}
# What a curl or wget command saves its download to, and the short flags of each that take a value.
CURL_VALUED = 'AbcCdDeEFHKmoPQrtTuUwxXyYz'
WGET_VALUED = 'OoaPUtTweiBlARDIXQ'
# PowerShell's downloaders, whose output `iex` would run.
PS_DOWNLOADERS = {'iwr', 'irm', 'invoke-webrequest', 'invoke-restmethod', 'curl', 'wget'}
PS_DOWNLOADS = re.compile(r'\b(?P<tool>iwr|irm|invoke-webrequest|invoke-restmethod|curl|wget)\b'
                          r'|\.(?P<method>downloadstring)\s*\(', re.I)
# A registry named on the command line (SEC-004): each package manager's
# install commands, and the variables that name a registry for one command.
# A bare `yarn` installs too.
PACKAGE_INSTALLS = {
    'npm': {'install', 'i', 'in', 'add', 'ci', 'clean-install', 'ic', 'install-clean', 'install-test',
            'it', 'install-ci-test', 'cit'},
    'pnpm': {'install', 'i', 'add'},
    'yarn': {'install', 'add', ''},
    'bun': {'install', 'i', 'add', 'a'},
}
REGISTRY_VARIABLES = {
    'npm': ('npm_config_registry', 'yarn_registry', 'bun_config_registry'),
    'pip': ('pip_index_url', 'pip_extra_index_url'),
    'uv': ('uv_index_url', 'uv_extra_index_url', 'uv_default_index', 'uv_index'),
}
# The public registries each tool uses when nothing names another, which may be named outright.
DEFAULT_REGISTRIES = {'https://registry.npmjs.org', 'https://registry.yarnpkg.com', 'https://pypi.org/simple',
                      'https://pypi.python.org/simple', 'https://rubygems.org', 'crates-io',
                      'sparse+https://index.crates.io', 'https://github.com/rust-lang/crates.io-index'}

# The em dash the standards ban (DOC-002), written as an escape so this file
# never holds one; the files it is checked in; the remote URLs that make a
# repository tannergolden's; and the Overrides section that turns it off, in
# the shape sync.py reads.
EM_DASH = '\u2014'
MARKDOWN = ('.md', '.mdx', '.markdown')
OWNER_REMOTE = re.compile(r'(?:(?:https?|ssh|git)://(?:[^@/]+@)?github\.com(?::\d+)?/|(?:[^@/:]+@)?github\.com:)'
                          r'tannergolden/', re.I)
OVERRIDES = re.compile(r'^## Overrides[ \t]*\n(?P<body>.*?)(?=^## |^---[ \t]*$|\Z)', re.M | re.S)
OVERRIDE = re.compile(r'^\s*[-*]\s+`?(?P<id>[A-Z]{2,5}-\d{3})`?\s*:?\s*(?P<reason>.*)$')

# The ask rules the installer adds to Claude Code's settings (OPS-005), which
# an edit must not drop (OPS-004). They match install.py's ASK_RULES, which a
# test holds.
ASK_RULES = (
    'Bash(git push *)',
    'Bash(gh pr create *)',
    'Bash(gh pr edit *)',
    'Bash(gh pr ready *)',
    'Bash(gh pr close *)',
    'Bash(gh pr comment *)',
    'Bash(gh pr review *)',
    'Bash(gh issue create *)',
    'Bash(gh issue edit *)',
    'Bash(gh issue close *)',
    'Bash(gh issue comment *)',
    'Bash(gh release create *)',
    'Bash(gh release upload *)',
    'Bash(gh release edit *)',
    'Bash(gh repo create *)',
    'Bash(gh repo fork *)',
    'Bash(gh workflow run *)',
    'Bash(gh gist create *)',
    'Bash(gh api *-X*POST*)',
    'Bash(gh api *-X*PATCH*)',
    'Bash(gh api *-X*PUT*)',
    'Bash(gh api *-X*DELETE*)',
    'Bash(gh api *--method*POST*)',
    'Bash(gh api *--method*PATCH*)',
    'Bash(gh api *--method*PUT*)',
    'Bash(gh api *--method*DELETE*)',
    'Bash(gh api repos/* -f *)',
    'Bash(gh api repos/* -F *)',
    'Bash(gh api repos/* --field*)',
    'Bash(gh api repos/* --raw-field*)',
    'Bash(gh api repos/* --input*)',
    'Bash(gh api /repos/* -f *)',
    'Bash(gh api /repos/* -F *)',
    'Bash(gh api /repos/* --field*)',
    'Bash(gh api /repos/* --raw-field*)',
    'Bash(gh api /repos/* --input*)',
    'Bash(gh api graphql *mutation*)',
    'Bash(npm publish *)',
    'Bash(pnpm publish *)',
    'Bash(yarn publish *)',
    'Bash(yarn npm publish *)',
    'Bash(cargo publish *)',
    'Bash(twine upload *)',
    'Bash(python -m twine upload *)',
    'Bash(python3 -m twine upload *)',
    'Bash(gem push *)',
    'Bash(docker push *)',
    'Bash(docker image push *)',
    'mcp__github__create_pull_request',
    'mcp__github__update_pull_request',
    'mcp__github__update_pull_request_branch',
    'mcp__github__pull_request_review_write',
    'mcp__github__add_comment_to_pending_review',
    'mcp__github__add_reply_to_pull_request_comment',
    'mcp__github__add_issue_comment',
    'mcp__github__update_issue_comment',
    'mcp__github__issue_write',
    'mcp__github__sub_issue_write',
    'mcp__github__request_copilot_review',
    'mcp__github__resolve_review_thread',
    'mcp__github__unresolve_review_thread',
    'mcp__github__create_or_update_file',
    'mcp__github__push_files',
    'mcp__github__delete_file',
    'mcp__github__create_branch',
    'mcp__github__create_repository',
    'mcp__github__fork_repository',
    'mcp__github__actions_run_trigger',
)

# Where Claude Code's home copy of the rules sits: a local install, then a
# cloud one. `--remind` prints the Invariants from the first that has them.
REMINDER = 'These rules from {where} still hold after compaction.'
CLAUDE_COPIES = ('.claude/rules/intelligence.md', '.claude/CLAUDE.md')


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
    """One simple command: its words, the variables set before it, where it runs, and the files it writes and reads."""

    words: list[str]
    env: dict[str, str]
    cwd: pathlib.Path
    writes: list[str] = dataclasses.field(default_factory=list)
    reads: list[str] = dataclasses.field(default_factory=list)


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
    remote_urls.cache_clear()  # git lookups and AGENTS.md reads are cached for one call only
    overridden.cache_clear()
    name = call.tool.lower()
    if 'mcp' in name or 'merge_pull_request' in name:
        # A remote tool: nothing it names is a local file, so only its intent and its text count.
        return (check_mcp(name, call.args) or secret_in(strings(call.args), 'the tool call')
                or mcp_dashes(name, call.args, call.cwd))
    patch = patch_of(call.args)
    if patch is not None:
        return check_patch(patch, call.cwd, home)
    command = command_of(call.args)
    path = first(call.args, PATH_KEYS)
    if command is not None and (name in SHELL_TOOLS or path is None):
        return check_command(command, call.cwd, home)
    if name in READ_TOOLS:
        # A read changes nothing, so only what it would read counts.
        return check_read_call(name, call.args, call.cwd, home)
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
        return [part for token in lexer for part in operators(token)]
    except ValueError:
        # An unbalanced quote: fall back to words, which still find most mistakes.
        return text.replace(';', ' ; ').replace('&&', ' && ').replace('|', ' | ').split()


def operators(token: str) -> list[str]:
    """A run of punctuation split into the shell operators it holds, longest first: `(<` is `(` then `<`."""
    if not token or any(char not in PUNCTUATION for char in token):
        return [token]
    parts = []
    while token:
        operator = next(op for op in OPERATORS if token.startswith(op))
        parts.append(operator)
        token = token[len(operator):]
    return parts


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
    # A `cd` earlier in the line moves the commands after it; a bare one goes home.
    here = cwd
    for command in found:
        command.cwd = here if command.cwd == cwd else command.cwd
        if command.words[:1] == ['cd']:
            targets = [word for word in command.words[1:] if word == '-' or not word.startswith('-')]
            if targets[:1] != ['-']:  # `cd -` goes back to a folder this line never named
                here = resolve(targets[0] if targets else '~', here)
    return found


def expand(words: list[str], cwd: pathlib.Path, depth: int) -> list[Simple]:
    """Peel redirections, assignments and wrappers off one command, and open `sh -c` and `eval`."""
    words, env, writes, reads = peel(words)
    if not words:
        return [Simple([':'], env, cwd, writes, reads)] if writes or reads else []
    program = os.path.basename(words[0])
    if program in SHELLS:
        for index, word in enumerate(words[1:], 1):
            if word.startswith('-') and 'c' in word.lstrip('-') and index + 1 < len(words):
                return simple_commands(words[index + 1], cwd, depth + 1)
    if program == 'eval':
        return simple_commands(' '.join(words[1:]), cwd, depth + 1)
    return [Simple(words, env, cwd, writes, reads)]


def peel(words: list[str]) -> tuple[list[str], dict[str, str], list[str], list[str]]:
    """A command's words without redirections, assignments and wrappers; and its variables, writes and reads."""
    plain: list[str] = []
    writes: list[str] = []
    reads: list[str] = []
    index = 0
    while index < len(words):
        word = words[index]
        if word in REDIRECTS or word in READS:
            if word in REDIRECTS and index + 1 < len(words):
                writes.append(words[index + 1])
            if word in ('<', '<>') and index + 1 < len(words):
                reads.append(words[index + 1])
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
    return words, env, writes, reads


def check_command(text: str, cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    verdict = secret_in(text, 'the command')
    if verdict:
        return verdict
    if re.search(r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}', text):
        return Verdict('OPS-003', 'the command is a fork bomb', 'Do not run it')
    kept, bodies = strip_heredocs(text)
    commands = simple_commands(kept, cwd)
    if any(os.path.basename(c.words[0]) == 'git' and 'commit' in c.words for c in commands):
        # Here-document bodies are data, but a commit message written in one still counts.
        verdict = check_signoff_lines(text, 'the commit message')
        if verdict:
            return verdict
    for command in commands:
        verdict = check_simple(command, home)
        if verdict:
            return verdict
    if DOWNLOAD_HINT.search(kept):
        verdict = check_downloads(kept) or check_powershell_download(kept)
        if verdict:
            return verdict
    return check_windows(kept, cwd, home) or check_messages(commands, bodies) or check_api_merge(text)


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
    return check_reads(command, home) or check_install(command) or check_writes(command, home)


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
        return short_flag(self.args, letter, takes_value)

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
        if recursive and catastrophic(target, command.cwd, home):
            return lost(f'`rm -r {target}` deletes a root, home or repository folder')
        if has_region(path):
            return block_edit(path)
    return None


def portable(raw: str) -> str:
    """A path as a POSIX shell writes it: forward slashes, no quotes, and `~` however the home folder is named."""
    return HOME_WORDS.sub('~', raw.strip('"\'').replace('\\', '/'))


def catastrophic(raw: str, cwd: pathlib.Path, home: pathlib.Path) -> bool:
    """Whether deleting `raw` with everything under it takes a root, drive, home, system or repository folder."""
    folder = re.sub(r'/\*(?:\.\*)?$', '', portable(raw))  # deleting what is in a folder empties the folder
    if folder.rstrip('/') in ('', '~', '.', '..', '*', '*.*') or DRIVE_ROOT.fullmatch(folder):
        return True
    try:
        real = pathlib.Path(os.path.normpath(str(resolve(folder, cwd))))
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


# --- credential stores --------------------------------------------------------


def under_home(path: pathlib.Path, home: pathlib.Path) -> pathlib.PurePath | None:
    """`path` relative to the home folder, or None outside it."""
    try:
        return pathlib.PurePath(os.path.normpath(str(path))).relative_to(os.path.normpath(str(home)))
    except ValueError:
        return None


def ssh_public(parts: tuple[str, ...]) -> bool:
    """Whether a path under ~/.ssh, in lowercase parts, is one of its public files: settings, host keys, public
    keys, and anything in a `*.d` folder. Every other file there is taken for a private key."""
    name = parts[-1]
    return (name.startswith(('config', 'known_hosts', 'authorized_keys', 'allowed_signers'))
            or name in ('environment', 'rc') or name.endswith(('.pub', '.conf'))
            or any(part.endswith('.d') for part in parts[1:]))


def credential_store(path: pathlib.Path, home: pathlib.Path) -> str | None:
    """What a credential store in the home folder holds, when `path` is one."""
    relative = under_home(path, home)
    parts = tuple(part.lower() for part in relative.parts) if relative else ()
    if not parts:
        return None
    if parts[0] == '.ssh' and len(parts) > 1:
        return None if ssh_public(parts) else 'a private SSH key'
    if parts[:3] == ('.config', 'gcloud', 'legacy_credentials') and len(parts) > 3:
        return 'gcloud credentials'
    if parts[:2] == ('.gnupg', 'private-keys-v1.d') and len(parts) > 2:
        return 'GnuPG private keys'
    if len(parts) == 2 and parts[0] == '.azure' and parts[1].startswith(AZURE_TOKENS):
        return 'Azure tokens'
    return CREDENTIAL_FILES.get(parts)


def holds_store(path: pathlib.Path, home: pathlib.Path, above: bool = True) -> str | None:
    """What a folder holds when a credential store sits inside it: a store's folder, one inside it, or one that
    holds it. With `above`, the home folder and the folders above it count too."""
    folder, base = os.path.normpath(str(path)), os.path.normpath(str(home))
    if above and (base == folder or base.startswith(folder.rstrip(os.sep) + os.sep)):
        return 'every credential store in the home folder'
    relative = under_home(path, home)
    parts = tuple(part.lower() for part in relative.parts) if relative else ()
    if not parts:
        return None
    for store in STORE_FOLDERS:
        if parts == store[:len(parts)]:
            return 'credential stores'
        if parts[:len(store)] == store and not (store == ('.ssh',) and ssh_public(parts)):
            return 'credential stores'
    return None


def stores_named(raw: str, cwd: pathlib.Path, home: pathlib.Path, whole: bool = False,
                 above: bool = True) -> tuple[str, str] | None:
    """Where a path word points and what it holds, when that is a credential store, or with `whole` a folder of one
    (`above` as holds_store takes it)."""
    path = resolve(portable(raw), cwd)
    paths = [path]
    if any(char in raw for char in '*?['):
        paths = [pathlib.Path(name) for name in glob.glob(str(path))] or paths
    for each in paths:
        kind = credential_store(each, home) or (holds_store(each, home, above) if whole else None)
        if kind:
            relative = under_home(each, home)
            where = str(each) if relative is None else '~' if str(relative) == '.' else f'~/{relative.as_posix()}'
            return where, kind
    return None


def exposes(actor: str, verb: str, where: str, kind: str) -> Verdict:
    return Verdict('SEC-001', f'{actor} would {verb} {where}, which holds {kind}',
                   'Leave credential stores unread: let the tool that owns the login use it, or ask your user')


def check_reads(command: Simple, home: pathlib.Path) -> Verdict | None:
    """A shell command that prints, searches, archives or copies a credential store, or feeds one to a program on
    its input."""
    for raw in command.reads:
        found = stores_named(raw, command.cwd, home)
        if found:
            return exposes('the command', 'read', *found)
    program, args = os.path.basename(command.words[0]), command.words[1:]
    if program in PRINTERS:
        operands, recursive, hidden = printed(program, args)
        for raw in operands:
            # A recursive search reads every file in a folder; rg and ag skip a hidden one unless told not to.
            found = stores_named(raw, command.cwd, home, whole=recursive, above=hidden)
            if found:
                return exposes(f'`{program}`', 'read', *found)
    sources: list[tuple[str, pathlib.Path]] = []
    if program in COPIERS:
        names = bare(args, COPIERS[program])
        if not (program == 'cp' and option(args, '-t', '--target-directory')):
            names = names[:-1]  # the last operand is where the copy goes
        sources = [(raw, command.cwd) for raw in names]
    elif program in ('tar', 'bsdtar', 'gtar'):
        sources = tar_sources(args, command.cwd)
    elif program == 'zip':
        sources = [(raw, command.cwd) for raw in bare(args, ZIP_VALUED)[1:]]  # the first operand is the archive
    for raw, base in sources:
        found = stores_named(raw, base, home, whole=True)
        if found:
            return exposes(f'`{program}`', 'copy', *found)
    return prints_credential(command)


def printed(program: str, args: list[str]) -> tuple[list[str], bool, bool]:
    """The files a printer reads, whether it reads folders whole, and whether it reads their hidden files too.

    A grep, sed, awk or jq takes its pattern, script or filter as its first
    operand, unless a flag gives it, and a flag such as `grep -f` names a file
    it reads as well. A recursive grep, rg or ag with no file reads the
    folder it runs in.
    """
    if program not in PATTERN_FIRST:
        return bare(args, set()), False, True
    given, valued = PATTERN_FIRST[program]
    grep = program in ('grep', 'egrep', 'fgrep')
    searcher = program in ('rg', 'ag')
    operands: list[str] = []
    files: list[str] = []
    found, recursive, hidden = False, searcher, not searcher
    index, flags = 0, True
    while index < len(args):
        arg = args[index]
        index += 1
        if not flags or arg == '-' or not arg.startswith('-'):
            operands.append(arg)
            continue
        if arg == '--':
            flags = False
            continue
        if arg.startswith('--'):
            name, equals, value = arg.partition('=')
            if name in valued and not equals:
                if name in TWO_VALUES:  # jq's `--arg NAME VALUE`, whose second word is the value
                    index += 1
                value = args[index] if index < len(args) else ''
                index += 1
            found = found or name in given
            recursive = recursive or (grep and (name in ('--recursive', '--dereference-recursive') or (
                name == '--directories' and value == 'recurse')))
            hidden = hidden or name in ('--hidden', '--unrestricted')
            if name in FILE_FLAGS or name in ('--slurpfile', '--rawfile'):
                files.append(value)
            continue
        for position, letter in enumerate(arg[1:], 1):
            flag = '-' + letter
            recursive = recursive or (grep and letter in 'rR')
            hidden = hidden or (searcher and (letter == '.' or arg.startswith('-uu')
                                              or (program == 'ag' and letter == 'u')))
            if flag in valued:
                attached = arg[position + 1:]
                value = attached or (args[index] if index < len(args) else '')
                index += 0 if attached else 1
                found = found or flag in given
                recursive = recursive or (grep and flag == '-d' and value == 'recurse')
                if flag in FILE_FLAGS:
                    files.append(value)
                break
    if not found:
        operands = operands[1:]  # the pattern, script or filter
    if recursive and not operands:
        operands = ['.']
    return operands + files, recursive, hidden


def tar_sources(args: list[str], cwd: pathlib.Path) -> list[tuple[str, pathlib.Path]]:
    """What `tar` puts into an archive it creates or adds to, each with the folder it is read from."""
    words = list(args)
    old_style = bool(words) and not words[0].startswith('-')
    if old_style:
        words[0] = '-' + words[0]  # `tar czf out.tgz dir`, whose letters take their values from the words after
    found: list[tuple[str, pathlib.Path]] = []
    here, creates, index = cwd, False, 0
    while index < len(words):
        word = words[index]
        index += 1
        if word.startswith('--'):
            name, equals, value = word.partition('=')
            creates = creates or name in ('--create', '--append', '--update', '--catenate', '--concatenate')
            if name in ('--file', '--directory', '--files-from', '--exclude-from', '--exclude') and not equals:
                value = words[index] if index < len(words) else ''
                index += 1
            if name == '--directory':
                here = resolve(portable(value), here)
            continue
        if word.startswith('-') and len(word) > 1:
            first_word = old_style and index == 1
            for position, letter in enumerate(word[1:], 1):
                creates = creates or letter in 'cru'
                if letter in TAR_VALUED:
                    attached = '' if first_word else word[position + 1:]
                    value = attached or (words[index] if index < len(words) else '')
                    index += 0 if attached else 1
                    if letter == 'C':
                        here = resolve(portable(value), here)
                    if attached:
                        break
            continue
        found.append((word, here))
    return found if creates else []


def prints_credential(command: Simple) -> Verdict | None:
    """A command that prints a credential when it runs, such as `gh auth token` or `aws configure
    export-credentials`."""
    words = command.words
    program, args = os.path.basename(words[0]), words[1:]
    shown = kind = ''
    if program == 'gh':
        group, action = [*bare(args, GH_VALUED), '', ''][:2]
        if (group, action) == ('auth', 'token'):
            shown, kind = 'gh auth token', "the GitHub CLI's token"
        elif (group, action) == ('auth', 'status') and ('--show-token' in args or '-t' in args):
            shown, kind = f'gh auth status {"-t" if "-t" in args else "--show-token"}', "the GitHub CLI's token"
    elif program == 'git':
        git = parse_git(command)
        if git is not None and ((git.sub == 'credential' and git.args[:1] == ['fill'])
                                or (git.sub.startswith('credential-') and 'get' in git.args)):
            shown, kind = f'git {git.sub} {git.args[0]}', 'stored git credentials'
    elif program == 'aws':
        plain = bare(args, AWS_VALUED)
        if plain[:2] == ['configure', 'export-credentials'] or (
                plain[:2] == ['configure', 'get'] and any(word.lower().endswith(AWS_SECRETS) for word in plain[2:])):
            shown, kind = f'aws configure {plain[1]}', 'AWS credentials'
    elif program == 'gcloud':
        plain = bare(args, set())
        printer = next((word for word in plain if word in ('print-access-token', 'print-identity-token')), '')
        if plain[:1] == ['auth'] and printer:
            shown, kind = f'gcloud auth {printer}', 'a gcloud token'
    elif program == 'az':
        if bare(args, set())[:2] == ['account', 'get-access-token']:
            shown, kind = 'az account get-access-token', 'an Azure access token'
    elif program == 'security':
        plain = bare(args, {'-p'})
        flag = next((word for word in args if word in ('-w', '-g')), '')
        if plain[:1] in (['find-generic-password'], ['find-internet-password']) and flag:
            shown, kind = f'security {plain[0]} {flag}', 'a keychain password'
    if not kind:
        return None
    return Verdict('SEC-001', f'`{shown}` prints {kind}',
                   'Let the tool that owns the login use it without printing it, or ask your user')


def check_read_call(name: str, args: Mapping, cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    """A read tool aimed at a credential store, or a search tool at a folder that holds one."""
    search = name in ('grep', 'grep_search', 'search_file_content')
    listed = args.get('paths')
    for raw in [args.get(key) for key in READ_PATH_KEYS] + (listed if isinstance(listed, list) else []):
        if isinstance(raw, str) and raw:
            # A search reads a folder whole, but, as rg does, not the home folder's hidden ones.
            found = stores_named(raw, cwd, home, whole=search, above=False)
            if found:
                return exposes('the call', 'read', *found)
    return None


# --- downloads and installs ---------------------------------------------------


def command_name(word: str) -> str:
    """A program's name however it is typed: no folder, no `.exe`, in lowercase."""
    name = os.path.basename(word.replace('\\', '/')).lower()
    return name[:-4] if name.endswith('.exe') else name


def runs_unread(runner: str, downloader: str) -> Verdict:
    return Verdict('SEC-004', f'the command runs what `{downloader}` downloads in `{runner}` before anyone reads it',
                   'Save it to a file and show your user what it would run, or install the tool from a package '
                   'registry')


def runs_saved(name: str, downloader: str) -> Verdict:
    return Verdict('SEC-004', f'the command runs `{name}`, which `{downloader}` downloads earlier in the same line, '
                   'before anyone reads it',
                   'Download it in one command, show your user what it would run, and run it in another once they '
                   'agree')


def check_downloads(text: str, depth: int = 0) -> Verdict | None:
    """A download a shell or interpreter would run unread: piped in, fed in by a process substitution or a
    here-string, substituted in by `$(...)`, or saved and then run in the same line."""
    return downloads_in(joined(tokens(text)), depth, {})


def joined(stream: list[str]) -> list[str]:
    """Tokens with each unquoted `$(...)` put back into one word, as the tokenizer keeps a quoted one."""
    found: list[str] = []
    index = 0
    while index < len(stream):
        token = stream[index]
        index += 1
        if token.endswith('$') and index < len(stream) and stream[index] == '(':
            inner, index = group(stream, index + 1)
            token = f'{token}({" ".join(joined(inner))})'
        found.append(token)
    return found


def group(stream: list[str], index: int, end: int | None = None) -> tuple[list[str], int]:
    """The tokens from `index` to the `)` that closes the bracket opened just before it, and the index after it;
    an unclosed bracket runs to `end`."""
    end = len(stream) if end is None else end
    level, start = 1, index
    while index < end:
        if stream[index] in ('(', '<(', '>('):
            level += 1
        elif stream[index] == ')':
            level -= 1
            if level == 0:
                return stream[start:index], index + 1
        index += 1
    return stream[start:end], end


def downloads_in(stream: list[str], depth: int, saved: dict[str, str]) -> Verdict | None:
    """check_downloads on a line's tokens; `saved` maps each file a download went to, so far, to its downloader."""
    if depth > 4:
        return None
    pipeline: list[list[str]] = []
    words: list[str] = []
    feeds: list[tuple[str, list[str]]] = []
    stream = [*stream, ';']
    index = 0
    while index < len(stream):
        token = stream[index]
        index += 1
        if token in ('<(', '>('):
            # A process substitution: `<(curl URL)` is a file that holds the download, and `>(sh)` one whose
            # text sh runs. After a redirection, `sh < <(curl URL)`, it is the command's input or output.
            inner, index = group(stream, index, len(stream) - 1)  # never past the `;` that ends the line
            verdict = downloads_in(inner, depth + 1, saved)
            if verdict:
                return verdict
            feeds.append((words.pop() if words and words[-1] in ('<', '>') else token, inner))
            continue
        if token == '<<<' and index < len(stream) - 1 and stream[index] not in SEPARATORS:
            # A here-string, the input of the command it ends.
            for inner in substitutions(stream[index]):
                verdict = check_downloads(inner, depth + 1)
                if verdict:
                    return verdict
            feeds.append((token, [stream[index]]))
            index += 1
            continue
        if token in SEPARATORS:
            segment = peel(words)[0] if words else []
            if segment:
                verdict = runs_download(segment, feeds, pipeline, depth, saved)
                if verdict:
                    return verdict
                pipeline.append(segment)
                if command_name(segment[0]) in DOWNLOADERS:
                    saved.update(dict.fromkeys(saved_files(segment), os.path.basename(segment[0])))
            words, feeds = [], []
            if token not in ('|', '|&'):
                verdict = piped_download(pipeline)
                if verdict:
                    return verdict
                pipeline = []
            continue
        for inner in substitutions(token):
            verdict = check_downloads(inner, depth + 1)
            if verdict:
                return verdict
        words.append(token)
    return None


def segments(stream: list[str]) -> list[list[str]]:
    """The commands in a list of tokens, in order, without their redirections and wrappers."""
    found: list[list[str]] = []
    words: list[str] = []
    for token in [*stream, ';']:
        if token in SEPARATORS:
            segment = peel(words)[0] if words else []
            if segment:
                found.append(segment)
            words = []
        else:
            words.append(token)
    return found


def substituted_download(word: str) -> str | None:
    """The downloader a `$(...)` or backtick substitution in one word runs, if one does."""
    for inner in substitutions(word):
        for command in simple_commands(inner, pathlib.Path('.')):
            if command_name(command.words[0]) in DOWNLOADERS:
                return os.path.basename(command.words[0])
    return None


def piped_download(pipeline: list[list[str]]) -> Verdict | None:
    for index, segment in enumerate(pipeline):
        if command_name(segment[0]) in DOWNLOADERS:
            for later in pipeline[index + 1:]:
                if runs_input(later):
                    return runs_unread(os.path.basename(later[0]), os.path.basename(segment[0]))
    return None


def runs_input(words: list[str]) -> bool:
    """Whether a command runs what arrives on its input as code, as `sh`, `bash -s`, `python3 -` and `iex` do."""
    program = command_name(words[0])
    if program in ('iex', 'invoke-expression'):
        return True
    if program in ('source', '.'):
        return words[1:2] in (['/dev/stdin'], ['-'])
    if program in ('pwsh', 'powershell'):
        return len(words) == 1 or '-' in words[1:]
    if not CODE_RUNNERS.fullmatch(program):
        return False
    shell = program.endswith('sh')
    inline = INLINE.get(re.match(r'[a-z]*', program).group(0), '')
    script = False  # `sh -s` runs its input and passes the words after it as arguments
    for word in words[1:]:
        if word in ('-', '/dev/stdin'):
            return True
        if word.startswith('--'):
            if word.split('=')[0] in ('--eval', '--print', '--command'):
                return False
            continue
        if word.startswith('-') and len(word) > 1:
            if (shell and 'c' in word[1:]) or (not shell and word[1] in inline):
                return False  # code given inline, so the input is only data
            script = script or (shell and 's' in word[1:])
            continue
        return script  # a script file, which runs instead of the input
    return True


def inline_code(words: list[str]) -> str | None:
    """The code a command line hands a shell or interpreter: `sh -c CODE`, `python3 -c CODE`, `eval CODE`."""
    program = command_name(words[0])
    if program == 'eval':
        return ' '.join(words[1:])
    if not CODE_RUNNERS.fullmatch(program):
        return None
    shell = program.endswith('sh')
    inline = INLINE.get(re.match(r'[a-z]*', program).group(0), '')
    for index, word in enumerate(words[1:], 1):
        if word.startswith('-') and not word.startswith('--') and len(word) > 1 and (
                (shell and 'c' in word[1:]) or (not shell and word[1] in inline)):
            attached = '' if shell else word[2:]
            return attached or (words[index + 1] if index + 1 < len(words) else None)
    return None


def script_of(words: list[str]) -> str | None:
    """The file a shell or interpreter runs: its first operand, unless code comes inline or from a module."""
    program = command_name(words[0])
    if program in ('source', '.'):
        return words[1] if len(words) > 1 else None
    if program == 'eval' or not CODE_RUNNERS.fullmatch(program) or inline_code(words) is not None:
        return None
    valued = RUNNER_VALUED.get('sh' if program.endswith('sh') else re.match(r'[a-z]*', program).group(0), set())
    skip = False
    for word in words[1:]:
        if skip or word == '--':
            skip = False
            continue
        if word == '-m' and program.startswith(('python', 'pypy')):
            return None  # a module, from wherever the interpreter finds one
        if word.startswith(('-', '+')) and len(word) > 1:
            skip = word in valued
            continue
        return word
    return None


def saved_files(words: list[str]) -> list[str]:
    """Where a curl or wget command saves what it downloads; standard output is nowhere."""
    program, args = command_name(words[0]), words[1:]
    names = [re.sub(r'[?#].*$', '', arg).rstrip('/').rsplit('/', 1)[-1]
             for arg in args if re.match(r'(?:https?|ftp)://', arg, re.I)]
    if program == 'curl':
        found = short_values(args, 'o', CURL_VALUED) + values(args, '--output')
        if short_flag(args, 'O', CURL_VALUED) or '--remote-name' in args or '--remote-name-all' in args:
            found += names
    elif program == 'wget':
        found = short_values(args, 'O', WGET_VALUED) + values(args, '--output-document') or names
    else:
        return []
    return [os.path.normpath(os.path.expanduser(name)) for name in found if name and name != '-']


def runs_download(words: list[str], feeds: list[tuple[str, list[str]]], pipeline: list[list[str]], depth: int,
                  saved: dict[str, str]) -> Verdict | None:
    """A download handed to a shell or interpreter as a file, `bash <(curl ...)`, as its input, `sh < <(curl ...)`
    or `bash <<< "$(curl ...)"`, or as code, `sh -c "$(curl ...)"`; a download written into one, `curl ... >
    >(sh)`; or a file a download saved earlier in the line, run."""
    program = command_name(words[0])
    runner = os.path.basename(words[0])
    code_runner = program in ('eval', 'source', '.') or bool(CODE_RUNNERS.fullmatch(program))
    fetched = next((os.path.basename(segment[0]) for segment in [*pipeline, words]
                    if command_name(segment[0]) in DOWNLOADERS), None)
    for kind, inner in feeds:
        if kind in ('<', '<(', '<<<'):
            source = substituted_download(inner[0]) if kind == '<<<' else next(
                (os.path.basename(segment[0]) for segment in segments(inner)
                 if command_name(segment[0]) in DOWNLOADERS), None)
            if source and (code_runner if kind == '<(' else runs_input(words)):
                return runs_unread(runner, source)
            if kind == '<<<' and runs_input(words):
                verdict = check_downloads(inner[0], depth + 1)  # a here-string a shell runs is code
                if verdict:
                    return verdict
        elif fetched:
            sinks = segments(inner)  # what the command writes goes to the input of the first command inside
            if sinks and runs_input(sinks[0]):
                return runs_unread(os.path.basename(sinks[0][0]), fetched)
    if not code_runner:
        name = os.path.normpath(os.path.expanduser(words[0]))
        return runs_saved(words[0], saved[name]) if '/' in words[0] and name in saved else None
    script = script_of(words)
    if script is not None and os.path.normpath(os.path.expanduser(script)) in saved:
        return runs_saved(script, saved[os.path.normpath(os.path.expanduser(script))])
    code = inline_code(words)
    if code is None:
        return None
    source = substituted_download(code)
    if source:
        return runs_unread(runner, source)
    if program == 'eval' or program.endswith('sh'):
        # Only a shell's code is a shell line; an interpreter's would cost a parse and find nothing.
        return downloads_in(joined(tokens(code)), depth + 1, saved)
    return None


def check_powershell_download(text: str, depth: int = 0) -> Verdict | None:
    """`iex` or `Invoke-Expression`, as a statement's command, running what `iwr`, `irm` or a WebClient downloads:
    piped into it, or handed to it as its argument. Quoted text is never a command."""
    if depth > 3:
        return None
    for pipeline in powershell_pipelines(text):
        fetched = ''
        for element in pipeline:
            commands = [match for match in element if match.group(0) not in ('(', ')')]
            if not commands:
                continue
            program = unquoted(commands[0].group(0))
            if command_name(program) in ('iex', 'invoke-expression'):
                # What iex runs is its argument, code or an expression that makes code.
                found = PS_DOWNLOADS.search(text, commands[0].end(), element[-1].end())
                if fetched or found:
                    return runs_unread(program, fetched or found.group('tool') or found.group('method'))
            inner = windows_inner([unquoted(match.group(0)) for match in commands])
            if inner is not None:
                verdict = check_powershell_download(inner, depth + 1)
                if verdict:
                    return verdict
            fetched = fetched or ps_fetches(element)
    return None


def powershell_pipelines(text: str) -> list[list[list[re.Match]]]:
    """Each pipeline in a cmd or PowerShell line, as its commands, each a list of tokens: a bracket keeps what it
    holds in the command it is part of, and quoted text stays in one token."""
    pipelines: list[list[list[re.Match]]] = []
    pipeline: list[list[re.Match]] = []
    element: list[re.Match] = []
    level = 0
    for match in WINDOWS_WORD.finditer(text):
        token = match.group(0)
        if token == '(':
            level += 1
        elif token == ')':
            level = max(level - 1, 0)
        elif level == 0 and token in ('|', ';', '&&', '||', '&', '\n'):
            if element:
                pipeline.append(element)
            element = []
            if token != '|':
                if pipeline:
                    pipelines.append(pipeline)
                pipeline = []
            continue
        element.append(match)
    if element:
        pipeline.append(element)
    if pipeline:
        pipelines.append(pipeline)
    return pipelines


def ps_fetches(element: list[re.Match]) -> str:
    """The downloader one PowerShell command runs, as a command of its own or a WebClient's DownloadString; ''."""
    previous = '('
    for match in element:
        token = match.group(0)
        if previous in ('(', '{') and command_name(unquoted(token).lstrip('{')) in PS_DOWNLOADERS:
            return unquoted(token).lstrip('{')
        if '.downloadstring' in re.sub(r'"[^"]*"?|\'[^\']*\'?', '', token).lower():
            return 'DownloadString'
        previous = token
    return ''


def unquoted(word: str) -> str:
    return word.replace('"', '').replace("'", '')


def option(args: list[str], *names: str) -> str | None:
    """The first of these options given, alone or as `--name=value`."""
    for arg in args:
        for name in names:
            if arg == name or (name.startswith('--') and arg.startswith(name + '=')):
                return name
    return None


def option_values(args: list[str], *names: str) -> list[tuple[str, str]]:
    """Each of these long options given, `--name value` or `--name=value`, with its value."""
    found = []
    for index, arg in enumerate(args):
        name, equals, value = arg.partition('=')
        if name in names:
            found.append((name, value if equals else (args[index + 1] if index + 1 < len(args) else '')))
    return found


def check_install(command: Simple) -> Verdict | None:
    """A package install that names a registry on the command line, other than the public one its tool uses when
    nothing names another."""
    program, args = os.path.basename(command.words[0]), command.words[1:]
    if re.fullmatch(r'python[0-9.]*|py', program) and args[:2] == ['-m', 'pip']:
        program, args = 'pip', args[2:]
    elif program == 'uv' and args[:1] in (['pip'], ['tool']):
        program, args = f'uv {args[0]}', args[1:]
    elif re.fullmatch(r'pip[0-9.]*', program):
        program = 'pip'
    variables = {key.lower(): value for key, value in command.env.items()}
    named: list[tuple[str, str]] = []  # what names a registry, and the registry it names
    sub = ''
    if program in PACKAGE_INSTALLS:
        sub = next(iter(bare(args, {'--registry', '--prefix', '-C', '--dir', '-w', '--workspace', '--filter',
                                    '--cwd'})), '')
        if sub in PACKAGE_INSTALLS[program]:
            scoped = {arg.partition('=')[0] for arg in args if re.fullmatch(r'--@[^:=\s]+:registry',
                                                                            arg.partition('=')[0])}
            named = option_values(args, '--registry', *scoped) + variables_of(variables, 'npm')
    elif program in ('pip', 'pipx', 'uv', 'uv pip', 'uv tool'):
        sub = next(iter(bare(args, {'--proxy', '--cache-dir', '--log', '--python', '-p', '-i', '--index-url',
                                    '--extra-index-url', '--index', '--default-index', '--pip-args', '--suffix'})), '')
        if (program, sub) in (('pip', 'install'), ('pipx', 'install'), ('uv', 'add'), ('uv', 'sync'),
                              ('uv', 'lock'), ('uv pip', 'install'), ('uv tool', 'install')):
            uv = program.startswith('uv')
            named = option_values(args, '--index-url', '--extra-index-url', *(
                ('--index', '--default-index') if uv else ()))
            named += [('-i', value) for value in short_values(args, 'i', 'rcefipt' if uv else 'rcetfi')]
            named += variables_of(variables, 'uv' if uv else 'pip')
    elif program == 'gem':
        sub = next(iter(bare(args, set())), '')
        if sub == 'install':
            named = option_values(args, '--source') + [('-s', value) for value in values(args, '-s')]
    elif program == 'cargo':
        sub = next(iter(word for word in bare(args, {'-Z', '--config', '--color', '-C'})
                        if not word.startswith('+')), '')
        if sub in ('install', 'add'):
            named = option_values(args, '--index', '--registry')
    found = next((name for name, value in named if not default_registry(value)), None)
    if found is None:
        return None
    shown = ' '.join(part for part in (program, sub) if part)
    return Verdict('SEC-004', f'`{shown}` with `{found}` installs from a registry named on the command line, '
                   "not the project's own",
                   "Install from the registry the project's configuration names, or ask your user to add this one "
                   'there')


def variables_of(variables: Mapping[str, str], tool: str) -> list[tuple[str, str]]:
    """The variables set for one command that name a registry for this tool, with their values."""
    return [(name.upper(), variables[name]) for name in REGISTRY_VARIABLES[tool] if name in variables]


def default_registry(value: str) -> bool:
    """Whether a registry named on the command line is the public one its tool uses anyway."""
    url = re.sub(r'^[\w.-]+=(?=[a-z]+:)', '', value.strip('\'"'), flags=re.I)  # uv's `--index name=URL`
    return url.rstrip('/').lower() in DEFAULT_REGISTRIES


# --- cmd and PowerShell -------------------------------------------------------


def windows_statements(text: str, depth: int = 0) -> list[list[str]]:
    """Each simple statement in a cmd or PowerShell line: its words without quotes, backslashes kept."""
    found: list[list[str]] = []
    words: list[str] = []
    for token in [*WINDOWS_WORD.findall(text), ';']:
        if token in ('&&', '||', ';', '&', '|', '\n', '(', ')'):
            if words:
                found.extend(windows_opened(words, depth))
            words = []
        else:
            words.append(token.replace('"', '').replace("'", ''))
    return found


def windows_inner(words: list[str]) -> str | None:
    """The line a statement hands to `cmd /c` or `powershell -Command`, if it does."""
    program = command_name(words[0])
    for index, word in enumerate(words[1:], 1):
        word = word.lower()
        if (program == 'cmd' and word in ('/c', '/k')) or (
                program in ('powershell', 'pwsh') and len(word) > 1 and '-command'.startswith(word)):
            return ' '.join(words[index + 1:])
    return None


def windows_opened(words: list[str], depth: int) -> list[list[str]]:
    """One statement, or the statements it hands to `cmd /c` or `powershell -Command`."""
    inner = windows_inner(words)
    if inner is not None and depth < 3:
        return windows_statements(inner, depth + 1)
    return [words]


def check_windows(text: str, cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    """What cmd and PowerShell spell their own way: a recursive delete of a root, drive or home folder, and
    printing a credential store. A `cd` moves the statements after it, as in the shell pass."""
    here = cwd
    for words in windows_statements(text):
        program = command_name(words[0])
        if program in ('cd', 'chdir', 'set-location', 'sl', 'pushd'):
            # The last word that is not a flag: `cd /d D:\x` and `Set-Location -Path x` name the folder last.
            targets = [word for word in words[1:] if not word.startswith('-') and not re.fullmatch(r'/[a-z]', word,
                                                                                                    re.I)]
            if targets and targets[-1] != '-':
                here = resolve(portable(targets[-1]), here)
            continue
        if program in WINDOWS_DELETES:
            verdict = windows_delete(words, here, home)
            if verdict:
                return verdict
        if program in WINDOWS_PRINTERS:
            redirected = False
            for raw in words[1:]:
                if redirected or raw.startswith('-') or re.match(r'\d*>', raw):
                    # A flag, or where output goes: `> file` writes it, and never reads it.
                    redirected = bool(re.fullmatch(r'\d*>>?', raw))
                    continue
                found = stores_named(raw, here, home)
                if found:
                    return exposes(f'`{words[0]}`', 'read', *found)
    return None


def windows_delete(words: list[str], cwd: pathlib.Path, home: pathlib.Path) -> Verdict | None:
    """`rmdir /s`, `del /s` or `Remove-Item -Recurse`, or an alias of it, aimed at a root, drive or home folder."""
    args = words[1:]
    lowered = [arg.lower() for arg in args]
    if any(low in ('-whatif', '-wi') or low.startswith('-whatif:') for low in lowered):
        return None  # a dry run
    recursive = next((arg for arg, low in zip(args, lowered) if (
        re.fullmatch(r'(?:/[a-z](?::[^/\s]*)?)+', low) and '/s' in re.findall(r'/[a-z]', low))
        or (len(low) > 1 and low.startswith('-') and '-recurse'.startswith(low.partition(':')[0]))), None)
    if recursive is None:
        return None
    targets: list[str] = []
    skip = False
    for arg, low in zip(args, lowered):
        name, colon, value = low.partition(':')
        if skip:
            skip = False
        elif low.startswith('-'):
            if colon and len(name) > 2 and any(full.startswith(name) for full in ('-path', '-literalpath')):
                targets.append(arg.partition(':')[2])
            skip = not colon and len(name) > 3 and any(full.startswith(name)
                                                       for full in ('-include', '-exclude', '-filter'))
        elif not re.fullmatch(r'(?:/[a-z](?::[^/\s]*)?)+', low):  # a cmd switch such as /s, /q or /a:h
            targets += [part for part in arg.split(',') if part]
    for target in targets:
        if catastrophic(target, cwd, home):
            return lost(f'`{words[0]} {recursive} {target}` deletes a root, home or repository folder')
    return None


# --- the em dash --------------------------------------------------------------


@functools.lru_cache(maxsize=None)
def remote_urls(folder: str) -> tuple[str, ...] | None:
    """Each remote's URL in the repository that holds `folder`: none yet, or None outside a repository."""
    try:
        done = subprocess.run(['git', '-C', folder, 'config', '--local', '--get-regexp', r'^remote\..*\.url$'],
                              capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode not in (0, 1):
        return None  # 1 is a repository with no remote yet; 128 is no repository at all
    return tuple(line.split(None, 1)[-1] for line in done.stdout.splitlines() if line.strip())


def owner_repository(folder: str) -> bool:
    """Whether the repository holding `folder` is tannergolden's: no remote yet, or every remote on GitHub under
    tannergolden. A fork, whose `upstream` is someone else's, is not, and outside a repository nothing is."""
    urls = remote_urls(folder)
    return urls is not None and all(OWNER_REMOTE.match(url) for url in urls)


@functools.lru_cache(maxsize=None)
def overridden(folder: str, rule: str) -> bool:
    """Whether the `AGENTS.md` at the root of the repository holding `folder` names `rule` under `## Overrides`, in
    the shape sync.py reads: an entry such as `- DOC-002: reason`, with HTML comments left out."""
    here = pathlib.Path(folder)
    for root in (here, *here.parents):
        if (root / '.git').exists():
            break
    else:
        return False
    try:
        text = (root / 'AGENTS.md').read_text(encoding='utf-8').replace('\r\n', '\n')
    except (OSError, UnicodeDecodeError):
        return False
    section = OVERRIDES.search(text)
    body = re.sub(r'<!--.*?-->', '', section.group('body'), flags=re.S) if section else ''
    return any(entry.group('id') == rule for entry in map(OVERRIDE.match, body.splitlines()) if entry)


def dash_banned(folder: str, repository: tuple[str, str] | None = None) -> bool:
    """Whether DOC-002 holds where an em dash would go: in a repository tannergolden owns, unless its `AGENTS.md`
    overrides the rule. A repository a command or tool names, as (owner, name), counts in place of the folder's;
    the folder's override still counts when the folder is a clone of it."""
    if repository is None:
        return owner_repository(folder) and not overridden(folder, 'DOC-002')
    owner, name = repository
    if owner.lower() != 'tannergolden':
        return False
    clone = re.compile(rf'[/:]tannergolden/{re.escape(name)}(?:\.git)?/?$', re.I)
    return not (any(clone.search(url) for url in remote_urls(folder) or ()) and overridden(folder, 'DOC-002'))


def nearest_folder(path: pathlib.Path) -> str:
    """The closest folder that exists on the way to `path`, which may not exist yet."""
    folder = path.parent
    while not folder.is_dir() and folder != folder.parent:
        folder = folder.parent
    return str(folder)


def em_dash(where: str) -> Verdict:
    return Verdict('DOC-002', f'{where} holds an em dash (U+2014), which the standards ban in this repository',
                   'Use a comma, colon, parentheses or a spaced hyphen instead; if your user asked for the dash, '
                   "they can add a DOC-002 entry to the Overrides in the repository's AGENTS.md")


def edit_dashes(path: pathlib.Path, new_text: str | None, olds: list[str], news: list[str]) -> Verdict | None:
    """A write or an edit that adds an em dash to a Markdown file; one kept from the text it replaces does not
    count, and neither does code or data, where the character can be what the file is about."""
    if not path.name.lower().endswith(MARKDOWN):
        return None
    if new_text is not None:
        added = new_text.count(EM_DASH)
        if added:
            try:
                added -= path.read_text(encoding='utf-8').count(EM_DASH)
            except (OSError, UnicodeDecodeError):
                pass
    else:
        added = sum(text.count(EM_DASH) for text in news) - sum(text.count(EM_DASH) for text in olds)
    if added > 0 and dash_banned(nearest_folder(path)):
        return em_dash(f'the text being written to {path.name}')
    return None


def mcp_dashes(name: str, args: Mapping, cwd: pathlib.Path) -> Verdict | None:
    """An em dash in the title or body of a pull request the GitHub MCP server would open or edit, in a repository
    tannergolden owns."""
    if not name.endswith(('create_pull_request', 'update_pull_request')):
        return None
    if not any(isinstance(args.get(key), str) and EM_DASH in args[key] for key in ('title', 'body')):
        return None
    repository = (str(args.get('owner') or ''), str(args.get('repo') or ''))
    return em_dash('the pull request title or body') if dash_banned(str(cwd), repository) else None


def short_flag(args: list[str], letter: str, takes_value: str = '') -> bool:
    """Whether a short flag appears, alone or clustered (`-sn`), before any value a letter in `takes_value` holds."""
    for arg in args:
        if arg == '--':
            return False
        if arg.startswith('-') and not arg.startswith('--') and len(arg) > 1:
            for char in arg[1:]:
                if char == letter:
                    return True
                if char in takes_value:
                    break
    return False


def short_values(args: list[str], letter: str, takes_value: str) -> list[str]:
    """Each value of a short flag, alone, attached (`-mfix`) or ending a cluster (`-am fix`)."""
    found = []
    for index, arg in enumerate(args):
        if arg == '--':
            break
        if arg.startswith('-') and not arg.startswith('--') and len(arg) > 1:
            for position, char in enumerate(arg[1:], 1):
                if char in takes_value:
                    if char == letter:
                        found.append(arg[position + 1:] or (args[index + 1] if index + 1 < len(args) else ''))
                    break
    return found


def check_messages(commands: list[Simple], bodies: str) -> Verdict | None:
    """An em dash in a commit message, or in a pull request's title or body."""
    for command in commands:
        program = os.path.basename(command.words[0])
        repo = None
        if program == 'git':
            git = parse_git(command)
            if git is None or git.sub != 'commit':
                continue
            texts = short_values(git.args, 'm', COMMIT_VALUED) + values(git.args, '--message')
            files = short_values(git.args, 'F', COMMIT_VALUED) + values(git.args, '--file')
            where, folder = 'the commit message', git.cwd
        elif program == 'gh':
            words = command.words[1:]
            if [*bare(words, GH_VALUED), '', ''][:2] not in (['pr', 'create'], ['pr', 'edit']):
                continue
            texts = [text for flag in ('--title', '-t', '--body', '-b') for text in values(words, flag)]
            files = values(words, '--body-file') + values(words, '-F')
            repo = (values(words, '--repo') + values(words, '-R') or [None])[-1]
            where, folder = 'the pull request title or body', command.cwd
        else:
            continue
        if any(name in ('-', '/dev/stdin') for name in files) or any('<<' in text for text in texts):
            texts.append(bodies)  # the message comes from a here-document
        if not any(EM_DASH in text for text in texts):
            continue
        parts = [part for part in re.sub(r'\.git$', '', repo or '').split('/') if part]
        banned = (len(parts) > 1 and dash_banned(str(folder), (parts[-2], parts[-1]))) if repo else dash_banned(
            str(folder))
        if banned:
            return em_dash(where)
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
    edits = args.get('edits')
    # Each replacement, in order: the text it finds, the text it puts there, and whether it replaces every copy.
    pairs = [(first(args, OLD_KEYS), first(args, NEW_KEYS), args.get('replace_all') is True)] + [
        (first(edit, OLD_KEYS), first(edit, NEW_KEYS), edit.get('replace_all') is True)
        for edit in (edits if isinstance(edits, list) else []) if isinstance(edit, dict)]
    olds = [old for old, _new, _every in pairs if old]
    news = [new for _old, new, _every in pairs if new]
    written = '\n'.join(text for text in [new_text, *news] if text)
    verdict = secret_in(written, f'the text being written to {path.name}') or (
        edit_dashes(path, new_text, olds, news) if EM_DASH in written else None)
    if verdict:
        return verdict
    if path.name in ('COMMIT_EDITMSG', 'MERGE_MSG'):
        return check_signoff_lines(written, f'the text written to {path.name}')
    owned, shared = guard_files(home)
    if path in owned:
        return tampers(path)
    if path in shared:
        return check_registration(path, new_text, pairs, home)
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


def check_registration(path: pathlib.Path, new_text: str | None, pairs: list[tuple[str | None, str | None, bool]],
                       home: pathlib.Path) -> Verdict | None:
    """An edit to a shared settings file that drops one of the guard's hooks or one of the kit's ask rules, or
    switches every hook off."""
    try:
        current = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        current = ''
    if new_text is not None:
        # Each registration names the guard once: the pre-tool hook, and in Claude Code the compaction reminder.
        if new_text.count('intelligence-guard') < current.count('intelligence-guard'):
            return tampers(path)
        after = added = new_text
    else:
        if any(old and 'intelligence-guard' in old for old, _new, _every in pairs):
            return tampers(path)
        after = current
        for old, new, every in pairs:
            if old:
                after = after.replace(old, new or '', -1 if every else 1)
        added = '\n'.join(new for _old, new, _every in pairs if new)
    if 'disableAllHooks' in added and 'disableAllHooks' not in current:
        return Verdict('OPS-004', 'the edit turns every hook off', 'Leave the hooks on, and report what blocked you')
    if path == home / '.claude' / 'settings.json':
        rule = dropped_ask(current, after)
        if rule:
            return drops_ask(rule, path)
    return None


def ask_rules(text: str) -> set[str] | None:
    """The `permissions.ask` rules in Claude Code's settings; None when the text is not JSON."""
    try:
        data = json.loads(text) if text.strip() else {}
    except ValueError:
        return None
    permissions = data.get('permissions') if isinstance(data, dict) else None
    asks = permissions.get('ask') if isinstance(permissions, dict) else None
    return {rule for rule in asks if isinstance(rule, str)} if isinstance(asks, list) else set()


def dropped_ask(before: str, after: str, parse: bool = True) -> str | None:
    """The first of the kit's ask rules that Claude Code's settings hold before a change and not after it."""
    had, has = (ask_rules(before), ask_rules(after)) if parse else (None, None)
    if had is None or has is None:  # not JSON, such as a patch's lines, so count each rule's quoted text instead
        return next((rule for rule in ASK_RULES if after.count(json.dumps(rule)) < before.count(json.dumps(rule))),
                    None)
    return next((rule for rule in ASK_RULES if rule in had and rule not in has), None)


def drops_ask(rule: str, path: pathlib.Path) -> Verdict:
    return Verdict('OPS-004', f'the change would drop `{rule}` from the ask rules in {path}, which make Claude Code '
                   'ask your user before an outward action',
                   'Leave the ask rules in place and let Claude Code ask your user; make agents-uninstall is what '
                   'takes them out')


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
        added = [line[1:] for line in body.split('\n') if line.startswith('+')]
        removed = [line[1:] for line in body.split('\n') if line.startswith('-')]
        if path == home / '.claude' / 'settings.json':
            rule = dropped_ask('\n'.join(removed), '\n'.join(added), parse=False)
            if rule:
                return drops_ask(rule, path)
        if (path.name.lower().endswith(MARKDOWN)
                and sum(line.count(EM_DASH) for line in added) > sum(line.count(EM_DASH) for line in removed)
                and dash_banned(nearest_folder(path))):
            return em_dash(f'the patch for {path.name}')
        if not str(path).endswith(BLOCK_SUFFIXES):
            continue
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


# --- the compaction reminder --------------------------------------------------


def reminder(home: pathlib.Path) -> str:
    """The precedence line for Invariants and the Invariants, from Claude Code's home copy of the rules; '' without."""
    for rel in CLAUDE_COPIES:
        try:
            text = (home / rel).read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        block = next((match.group(0) for match in REGION.finditer(text) if match.group('name') == 'INTELLIGENCE'),
                     '')
        lines = block.replace('\r\n', '\n').split('\n')
        precedence = next((line for line in lines if line.startswith('- Invariants:')), None)
        start = next((index for index, line in enumerate(lines) if line.strip() == '### Invariants'), None)
        if precedence is None or start is None:
            continue
        end = next((index for index in range(start + 1, len(lines)) if lines[index].startswith(('#', '<!--'))),
                   len(lines))
        section = '\n'.join(lines[start:end]).strip()
        return f'{REMINDER.format(where="~/" + rel)}\n\n{precedence}\n\n{section}\n'
    return ''


def remind(home: pathlib.Path, stdin: str | None) -> int:
    """Print the reminder, unless the payload names a session start other than a compaction. It never fails."""
    try:
        if stdin is None:
            stdin = '' if sys.stdin is None or sys.stdin.isatty() else sys.stdin.read()
        payload = json.loads(stdin) if stdin.strip() else {}
        if isinstance(payload, dict) and payload.get('source', 'compact') != 'compact':
            return 0
        text = reminder(home)
    except Exception:  # a reminder that cannot be read is no reason to disturb the session
        return 0
    print(text, end='')
    return 0


def main(argv: list[str] | None = None, stdin: str | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--app', default='unknown',
                        help='the app whose hook calls this: claude, codex, copilot or antigravity')
    parser.add_argument('--command', help='check one shell command by hand instead of reading a payload')
    parser.add_argument('--remind', action='store_true',
                        help="print the Invariants from Claude Code's home copy of the rules, for after a compaction")
    args = parser.parse_args(argv)
    home = pathlib.Path(os.environ.get('HOME') or pathlib.Path.home())
    if args.remind:
        return remind(home, stdin)
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
