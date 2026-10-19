#!/usr/bin/env python3
"""Deliver the universal rules to every repository the owner owns, and keep them there.

WHY THIS EXISTS. Every repository carries the rules in one root `AGENTS.md`,
between `INTELLIGENCE` markers, beside sections the repository owns. Each
release reaches a repository as one pull request on `chore/intelligence`, by
either of two routes, and merging always stays the owner's:

- THE STUB. A repository that carries `setup/intelligence-sync.yml` as
  `.github/workflows/intelligence-sync.yml` pulls the hub's latest release,
  every Monday, on its own `GITHUB_TOKEN`. The stub calls
  `.github/workflows/sync.yml`, which runs `apply` in that repository's
  checkout through `.github/actions/sync`, and the standards' open-pr
  action proposes the result. No App, no key, nothing in the hub that reaches
  another repository.
- THE PUSH. The owner runs `sync` here under their own `gh` login, for every
  repository at once, with or without the stub.

The commands:

- `audit` reports what every repository carries now: no `AGENTS.md`, no
  block, a block edited by hand, a stale or unknown block, a `CLAUDE.md`
  that makes Claude Code skip `AGENTS.md`, an Overrides entry that names an
  Invariant, and whether the stub is there.
- `sync` opens or updates one pull request per repository. A first sync
  creates `AGENTS.md`, or inserts the block into one that has none, and
  folds any `CLAUDE.md` into it.
- `merge` merges each sync pull request whose diff is exactly the block and
  whose checks passed. Anything bigger, such as a first sync, waits for the
  owner to review it by hand. A pull request the default token opened has
  checks that wait for approval: once the diff is proven to be the block
  alone, `merge` starts them, and merges on a later run.
- `apply` writes the block into the repository checked out where it runs,
  and hands the commit and pull request text to the stub's workflow.

`sync` delivers the block of the latest release tag, never unreleased work;
`apply` delivers the one in the hub tree it runs from, which is the latest
release at the hub's moving major tag. Every repository the owner owns takes part, except
templates, forks, archived ones, and any with the `no-intelligence` topic.

Run it, from the hub's root:

    python3 scripts/sync.py audit
    python3 scripts/sync.py sync --dry-run
    python3 scripts/sync.py sync
    python3 scripts/sync.py merge --dry-run
    python3 scripts/sync.py merge

and, as the stub's workflow does, in a repository's checkout:

    GITHUB_REPOSITORY=owner/name python3 /path/to/hub/scripts/sync.py apply --dry-run
"""

from __future__ import annotations

import argparse
import base64
import dataclasses
import json
import os
import pathlib
import re
import secrets
import subprocess
import sys
import textwrap
import urllib.parse
from collections.abc import Callable, Sequence

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render  # noqa: E402

ROOT = HERE.parent
BRANCH = 'chore/intelligence'
OPT_OUT = 'no-intelligence'
AGENTS = 'AGENTS.md'
CLAUDE = 'CLAUDE.md'
STUB = '.github/workflows/intelligence-sync.yml'  # where a repository keeps setup/intelligence-sync.yml
OK_CONCLUSIONS = ('success', 'neutral', 'skipped')
NOTHING_RAN = 'no checks ran, so there is nothing to trust'
OVERRIDE = re.compile(r'^\s*[-*]\s+`?(?P<id>[A-Z]{2,5}-\d{3})`?\s*:?\s*(?P<reason>.*)$')
POINTER = re.compile(r'^\s*@\.?/?AGENTS\.md\s*$')


class GitHubError(Exception):
    """A GitHub call that failed, with what GitHub said."""


class ApplyError(Exception):
    """A repository's checkout that `apply` will not write into, and why."""


def decode_pages(text: str) -> object:
    """`gh api --paginate` prints one JSON document per page; join the lists."""
    decoder = json.JSONDecoder()
    pages: list[object] = []
    index = 0
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        page, index = decoder.raw_decode(text, index)
        pages.append(page)
    if len(pages) == 1:
        return pages[0]
    joined: list[object] = []
    for page in pages:
        joined.extend(page if isinstance(page, list) else [page])
    return joined


Runner = Callable[[Sequence[str], 'str | None'], subprocess.CompletedProcess]


def run_gh(argv: Sequence[str], stdin: str | None) -> subprocess.CompletedProcess:
    return subprocess.run(list(argv), input=stdin, capture_output=True, text=True, check=False)


class GitHub:
    """The GitHub calls this script makes, through `gh`: the owner's login, or a workflow's token."""

    def __init__(self, owner: str | None = None, run: Runner = run_gh) -> None:
        self.run = run
        self._owner = owner

    def api(self, path: str, method: str = 'GET', body: dict | None = None,
            paginate: bool = False, missing_ok: bool = False) -> object:
        argv = ['gh', 'api', '-X', method, path]
        if paginate:
            argv.insert(2, '--paginate')
        if body is not None:
            argv += ['--input', '-']
        done = self.run(argv, json.dumps(body) if body is not None else None)
        if done.returncode != 0:
            said = (done.stderr or done.stdout or '').strip()
            if missing_ok and ('404' in said or 'Not Found' in said):
                return None
            raise GitHubError(f'{method} {path}: {said}')
        return decode_pages(done.stdout) if done.stdout.strip() else None

    def user(self) -> dict:
        return self.api('user')

    @property
    def owner(self) -> str:
        if self._owner is None:
            self._owner = self.user()['login']
        return self._owner

    def repos(self) -> list[dict]:
        return list(self.api('user/repos?affiliation=owner&per_page=100', paginate=True) or [])

    def repo(self, full: str) -> dict:
        """One repository's settings, by `owner/name`."""
        return self.api(f'repos/{full}')

    def file(self, repo: str, path: str, ref: str) -> tuple[str, str] | None:
        """A file's text and blob SHA at `ref`, or None when it is not there."""
        data = self.api(f'repos/{self.owner}/{repo}/contents/{urllib.parse.quote(path)}'
                        f'?ref={urllib.parse.quote(ref, safe="")}', missing_ok=True)
        if not isinstance(data, dict):
            return None
        if data.get('type') != 'file':
            raise GitHubError(f'{repo}/{path} is a {data.get("type")}, not a file; review it by hand')
        return base64.b64decode(data['content']).decode('utf-8'), data['sha']

    def head(self, repo: str, branch: str) -> str | None:
        data = self.api(f'repos/{self.owner}/{repo}/git/ref/heads/{branch}', missing_ok=True)
        return data['object']['sha'] if isinstance(data, dict) else None

    def point_branch(self, repo: str, branch: str, sha: str) -> None:
        """Create `branch` at `sha`, or move it there: the sync branch is the hub's alone."""
        if self.head(repo, branch) is None:
            self.api(f'repos/{self.owner}/{repo}/git/refs', 'POST', {'ref': f'refs/heads/{branch}', 'sha': sha})
        else:
            self.api(f'repos/{self.owner}/{repo}/git/refs/heads/{branch}', 'PATCH', {'sha': sha, 'force': True})

    def put(self, repo: str, path: str, text: str, message: str, branch: str, sha: str | None) -> None:
        body = {'message': message, 'branch': branch,
                'content': base64.b64encode(text.encode('utf-8')).decode('ascii')}
        if sha:
            body['sha'] = sha
        self.api(f'repos/{self.owner}/{repo}/contents/{urllib.parse.quote(path)}', 'PUT', body)

    def delete(self, repo: str, path: str, message: str, branch: str, sha: str) -> None:
        self.api(f'repos/{self.owner}/{repo}/contents/{urllib.parse.quote(path)}', 'DELETE',
                 {'message': message, 'branch': branch, 'sha': sha})

    def sync_pr(self, repo: str) -> dict | None:
        pulls = self.api(f'repos/{self.owner}/{repo}/pulls?state=open&head={self.owner}:{BRANCH}',
                         paginate=True) or []
        return pulls[0] if pulls else None

    def open_pr(self, repo: str, base: str, title: str, body: str) -> dict:
        return self.api(f'repos/{self.owner}/{repo}/pulls', 'POST',
                        {'title': title, 'head': BRANCH, 'base': base, 'body': body})

    def edit_pr(self, repo: str, number: int, title: str, body: str) -> None:
        self.api(f'repos/{self.owner}/{repo}/pulls/{number}', 'PATCH', {'title': title, 'body': body})

    def pr(self, repo: str, number: int) -> dict:
        return self.api(f'repos/{self.owner}/{repo}/pulls/{number}')

    def pr_files(self, repo: str, number: int) -> list[dict]:
        return list(self.api(f'repos/{self.owner}/{repo}/pulls/{number}/files?per_page=100', paginate=True) or [])

    def checks(self, repo: str, sha: str) -> tuple[list[dict], dict]:
        runs = self.api(f'repos/{self.owner}/{repo}/commits/{sha}/check-runs?per_page=100') or {}
        status = self.api(f'repos/{self.owner}/{repo}/commits/{sha}/status') or {}
        return list(runs.get('check_runs', [])), status

    def commit_message(self, repo: str, sha: str) -> str:
        return self.api(f'repos/{self.owner}/{repo}/commits/{sha}')['commit']['message']

    def merge(self, repo: str, number: int, sha: str, title: str, message: str) -> None:
        self.api(f'repos/{self.owner}/{repo}/pulls/{number}/merge', 'PUT',
                 {'merge_method': 'squash', 'sha': sha, 'commit_title': title, 'commit_message': message})

    def waiting_runs(self, repo: str, sha: str) -> list[dict]:
        """The workflow runs on `sha` that wait for someone with write access to approve them."""
        data = self.api(f'repos/{self.owner}/{repo}/actions/runs?head_sha={sha}&status=action_required'
                        '&per_page=100') or {}
        return list(data.get('workflow_runs', []))

    def approve_run(self, repo: str, run_id: int) -> None:
        self.api(f'repos/{self.owner}/{repo}/actions/runs/{run_id}/approve', 'POST')

    def reopen(self, repo: str, number: int) -> None:
        """Close and reopen a pull request: done as the owner, that starts its checks."""
        for state in ('closed', 'open'):
            self.api(f'repos/{self.owner}/{repo}/pulls/{number}', 'PATCH', {'state': state})


# --- What a repository's AGENTS.md should become ------------------------------------------


def skeleton(repo: str, region: str) -> str:
    """A new AGENTS.md: the Document Styling header, the block, and the owner's sections."""
    name = repo.replace("'", "''")
    return f"""<!--
title: '🤖 Agent Instructions'
description: 'How AI coding agents work in {name}: the universal rules first, then this repository''s own.'
type: standard
keywords: [agents-md, ai-agents]
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 Agent Instructions

<a name="top"></a>

**How AI coding agents work in this repository.**

_The universal rules first, then this repository's own._

</div>

---

{region}
---

## Commands

<!-- How to install, lint, test and build, exactly as CI runs them. -->

## Definition of done

<!-- What has to be true before an agent may call a change finished. -->

## Conventions

<!-- What this repository does differently from the standards, and why. -->

## Where things live

<!-- The folders an agent needs, and what each one holds. -->

## Gotchas

<!-- What has bitten someone before: generated files, slow tests, fragile steps. -->

## Ask first

<!-- Changes an agent proposes and waits on, rather than makes. -->

## Overrides

<!-- One line per Default this repository changes, as `- WORK-002: why`. Invariants cannot be overridden. -->

---

<div align="center">

**Universal rules first, this repository's own after.**

[↑ Back to Top](#top)

</div>
"""


def insert_point(text: str) -> int:
    """Where the block goes in an AGENTS.md that has none: after its header, before its body."""
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    index = 0

    def skip_blank(i: int) -> int:
        while i < len(lines) and not lines[i].strip():
            i += 1
        return i

    # YAML frontmatter, which an Obsidian note such as a knowledge vault's
    # AGENTS.md opens with, only counts on the very first line, and it must
    # stay there for its reader to see it: the block goes after it.
    if lines and lines[0].rstrip('\r\n') == '---':
        close = next((i for i in range(1, len(lines)) if lines[i].rstrip('\r\n') in ('---', '...')), None)
        if close is not None:
            index = close + 1
    index = skip_blank(index)
    if index < len(lines) and lines[index].lstrip().startswith('<!--'):
        while index < len(lines) and '-->' not in lines[index]:
            index += 1
        index = skip_blank(index + 1)
    if index < len(lines) and lines[index].strip().startswith('<!-- markdownlint-disable'):
        index = skip_blank(index + 1)
    if index < len(lines) and lines[index].strip().lower().startswith('<div align="center">'):
        while index < len(lines) and '</div>' not in lines[index]:
            index += 1
        index = skip_blank(index + 1)
        if index < len(lines) and lines[index].strip() == '---':
            index += 1
        return offsets[min(index, len(lines))]
    if index < len(lines) and lines[index].startswith('# '):
        return offsets[index + 1]
    return offsets[index]


def demote(text: str) -> str:
    """Every heading one level deeper, so folded sections sit under their new heading."""
    out = []
    fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(('```', '~~~')):
            fence = not fence
        if not fence and re.match(r'^#{1,5} ', line):
            line = '#' + line
        out.append(line)
    return ''.join(out)


def claude_body(claude: str) -> str:
    """CLAUDE.md without its frontmatter, lint comment and title: the part worth keeping."""
    text = re.sub(r'\A\s*<!--.*?-->\s*', '', claude, count=1, flags=re.S)
    text = re.sub(r'\A\s*<!-- markdownlint-disable[^>]*-->\s*', '', text, count=1)
    text = re.sub(r'\A\s*<div align="center">.*?</div>\s*(---\s*)?', '', text, count=1, flags=re.S | re.I)
    text = re.sub(r'\A\s*# [^\n]*\n', '', text, count=1)
    return text.strip()


def is_pointer(claude: str) -> bool:
    """A CLAUDE.md that only imports AGENTS.md carries nothing to fold."""
    body = re.sub(r'<!--.*?-->', '', claude, flags=re.S)
    lines = [line for line in body.splitlines() if line.strip() and not line.startswith('#')]
    return bool(lines) and all(POINTER.match(line) for line in lines)


def footer_start(text: str) -> int:
    """Where a Document Styling footer begins, so folded text lands above it."""
    starts = [m.start() for m in re.finditer(r'^---\s*\n\s*<div align="center">', text, flags=re.M | re.I)]
    if starts and text.find('[↑ Back to Top]', starts[-1]) != -1:
        return starts[-1]
    return len(text)


def fold(agents: str, claude: str) -> str:
    """AGENTS.md with CLAUDE.md's content kept in a section of its own."""
    body = claude_body(claude)
    if not body or is_pointer(claude) or body in agents:
        return agents
    section = f'## Folded from CLAUDE.md\n\n{demote(body)}\n\n'
    at = footer_start(agents)
    before = agents[:at]
    if before and not before.endswith('\n\n'):
        before = before.rstrip('\n') + '\n\n'
    return before + section + agents[at:]


@dataclasses.dataclass(frozen=True)
class Change:
    """What a sync writes to one repository."""

    agents: str  # the new AGENTS.md
    delete_claude: bool
    adoption: list[str]  # what a first sync did, for the pull request; empty for a routine update


def adopt(repo: str, agents: str | None, claude: str | None, region: str) -> Change:
    """The repository's AGENTS.md with the release's block in place."""
    notes: list[str] = []
    if agents is None:
        text = skeleton(repo, region)
        notes.append('creates `AGENTS.md`, with empty sections for this repository to fill')
    elif render.find(agents) is not None:
        text = render.replace(agents, region)
    else:
        at = insert_point(agents)
        before, after = agents[:at], agents[at:]
        if before and not before.endswith('\n\n'):
            before = before.rstrip('\n') + '\n\n'
        text = before + region + ('\n' + after.lstrip('\n') if after.strip() else '')
        notes.append('inserts the block into the existing `AGENTS.md`, after its header')
    delete = claude is not None
    if claude is not None:
        if is_pointer(claude) or not claude_body(claude):
            notes.append('deletes `CLAUDE.md`, which only pointed at `AGENTS.md`')
        else:
            text = fold(text, claude)
            notes.append('moves `CLAUDE.md` into `AGENTS.md` under "Folded from CLAUDE.md", and deletes it')
    return Change(text, delete, notes)


def outside_block(text: str) -> str:
    found = render.find(text)
    return text if found is None else text[:found.start] + text[found.end:]


def only_block_changed(old: str, new: str) -> bool:
    """True when two versions of AGENTS.md differ only between the markers."""
    return (render.find(old) is not None and render.find(new) is not None
            and outside_block(old) == outside_block(new))


def overrides(agents: str) -> list[tuple[str, str]]:
    """The entries under `## Overrides`: each rule ID and the reason given for it."""
    match = re.search(r'^## Overrides[ \t]*\n(?P<body>.*?)(?=^## |^---[ \t]*$|\Z)', agents, flags=re.M | re.S)
    if not match:
        return []
    body = re.sub(r'<!--.*?-->', '', match.group('body'), flags=re.S)
    found = []
    for line in body.splitlines():
        entry = OVERRIDE.match(line)
        if entry:
            found.append((entry.group('id'), entry.group('reason').strip()))
    return found


# --- The hub's side: which block to deliver, and which blocks it ever shipped --------------


def git(root: pathlib.Path, *args: str) -> str:
    done = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise SystemExit(f'git {" ".join(args)}: {done.stderr.strip()}')
    return done.stdout


def releases(root: pathlib.Path) -> list[str]:
    """The hub's release tags, newest first."""
    tags = git(root, 'tag', '--list', 'v*', '--sort=-v:refname').split()
    return [tag for tag in tags if re.fullmatch(r'v\d+\.\d+\.\d+', tag)]


def home_at(root: pathlib.Path, ref: str) -> str:
    return git(root, 'show', f'{ref}:{render.HOME_FILE}')


def history(root: pathlib.Path) -> dict[str, str]:
    """Every block hash a release shipped, mapped to the oldest release that carried it."""
    known: dict[str, str] = {}
    for tag in releases(root):
        try:
            found = render.find(home_at(root, tag))
        except SystemExit:
            continue
        if found is not None:
            known[found.marker] = tag
    return known


def delivered(root: pathlib.Path, ref: str | None) -> tuple[str, str]:
    """The region to deliver and the ref it came from: the latest release unless told otherwise."""
    if ref is None:
        tags = releases(root)
        if not tags:
            raise SystemExit('the hub has no release yet: cut one, or pass --ref HEAD to deliver unreleased rules')
        ref = tags[0]
    text = home_at(root, ref)
    found = render.find(text)
    if found is None or found.edited:
        raise SystemExit(f'{ref}:{render.HOME_FILE} is not a sound home file')
    return text[found.start:found.end], ref


# --- The three commands --------------------------------------------------------------------


def hub_name(root: pathlib.Path) -> str:
    """This hub's repository name, from its origin remote."""
    done = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=root, capture_output=True,
                          text=True, check=False)
    match = re.search(r'([^/:]+?)(?:\.git)?/?$', done.stdout.strip()) if done.returncode == 0 else None
    return match.group(1) if match else 'intelligence'


def left_out(repo: dict) -> str | None:
    """Why a repository takes no part, from its settings; None when it does."""
    return ('archived' if repo.get('archived') else 'a fork' if repo.get('fork')
            else 'a template' if repo.get('is_template')
            else f'opted out with {OPT_OUT}' if OPT_OUT in (repo.get('topics') or []) else None)


def targets(gh: GitHub, only: Sequence[str], hub: str) -> tuple[list[dict], list[str]]:
    """The repositories that take part, and a line for each one left out."""
    chosen, skipped = [], []
    for repo in sorted(gh.repos(), key=lambda r: r['name'].lower()):
        name = repo['name']
        if only and name not in only:
            continue
        reason = 'the hub, which holds the Constitution and carries no copy of it' if name == hub else left_out(repo)
        if reason:
            skipped.append(f'{name}: skipped, {reason}')
        else:
            chosen.append(repo)
    return chosen, skipped


def identity(gh: GitHub) -> tuple[str, str]:
    """The owner's name and GitHub no-reply address, for the sign-off."""
    user = gh.user()
    return user.get('name') or user['login'], f'{user["id"]}+{user["login"]}@users.noreply.github.com'


def messages(block_hash: str, ref: str, change: Change,
             signer: tuple[str, str] | None) -> tuple[str, str, str]:
    """The commit title, the commit body with its sign-off, and the pull request body.

    With no signer, a repository's stub opened it: the body has no sign-off,
    because the standards' open-pr action commits as the owner and signs off
    itself, and the pull request says how its checks start.
    """
    title = f'chore(agents): 🤖 sync the universal rules to {block_hash[:12]}'
    why = (f'The intelligence hub renders the universal rules from its CONSTITUTION.md. This replaces the copy '
           f'between the INTELLIGENCE markers in AGENTS.md with the one from release {ref}, and '
           f'leaves every section this repository owns as it was.')
    if change.adoption:
        why = ('The intelligence hub delivers the universal rules to every repository its owner '
               'owns, in one root AGENTS.md. This first sync ' + '; it '.join(change.adoption) + '.')
    body = textwrap.fill(why, 72) + (f'\n\nSigned-off-by: {signer[0]} <{signer[1]}>' if signer else '')
    first = ' This is a first sync, so review it by hand: `make merge` leaves it alone.'
    impact = f'Agents read the rules of release {ref} in this repository.' + (first if change.adoption else '')
    if signer is None:
        impact += " This repository's 🔁 Intelligence Sync opened it; merging it stays the owner's."
        impact += (' If its checks wait for approval, select **Approve workflows to run** here.' if change.adoption
                   else ' If its checks wait for approval, `make merge` in the hub approves them once it has '
                        'checked that the diff is the block alone.')
    pr_body = (f'## Impact\n\n{impact}\n\n'
               f"## Validation\n\nThe block's marker carries `sha256:{block_hash}`, the hash of its text, "
               'so `make audit` in the hub can prove it is unedited.\n\n'
               '## Rollback\n\nRevert this pull request. Nothing else in the repository depends on the block.\n')
    return title, body, pr_body


def sync_one(gh: GitHub, repo: dict, region: str, ref: str, signer: tuple[str, str] | None,
             dry_run: bool) -> str:
    name, base = repo['name'], repo['default_branch']
    agents = gh.file(name, AGENTS, base)
    claude = gh.file(name, CLAUDE, base)
    change = adopt(name, agents[0] if agents else None, claude[0] if claude else None, region)
    if agents and change.agents == agents[0] and not change.delete_claude:
        return f'{name}: current'
    block_hash = render.find(region).marker
    title, body, pr_body = messages(block_hash, ref, change, signer)
    action = 'adopt' if change.adoption else 'update'
    if dry_run:
        return f'{name}: would {action} ({"; ".join(change.adoption) or "the block"})'
    base_sha = gh.head(name, base)
    if base_sha is None:
        return f'{name}: skipped, {base} has no commits'
    gh.point_branch(name, BRANCH, base_sha)
    gh.put(name, AGENTS, change.agents, f'{title}\n\n{body}', BRANCH, agents[1] if agents else None)
    if change.delete_claude and claude:
        gh.delete(name, CLAUDE, f'{title}\n\n{body}', BRANCH, claude[1])
    existing = gh.sync_pr(name)
    if existing:
        gh.edit_pr(name, existing['number'], title, pr_body)
        return f'{name}: updated pull request #{existing["number"]}'
    created = gh.open_pr(name, base, title, pr_body)
    return f'{name}: opened pull request #{created["number"]}'


def audit_one(gh: GitHub, repo: dict, current: str, known: dict[str, str], invariants: set[str]) -> list[str]:
    """What is wrong in one repository, as short phrases; empty when nothing is."""
    name, base = repo['name'], repo['default_branch']
    agents = gh.file(name, AGENTS, base)
    found: list[str] = []
    if gh.file(name, CLAUDE, base):
        found.append('a CLAUDE.md sits beside AGENTS.md, so Claude Code may skip AGENTS.md')
    if agents is None:
        return ['no AGENTS.md', *found]
    region = render.find(agents[0])
    if region is None:
        found.insert(0, 'AGENTS.md has no block')
    elif region.edited:
        found.insert(0, 'the block was edited by hand')
    elif region.marker != current:
        found.insert(0, f'the block is from {known[region.marker]}' if region.marker in known
                     else 'the block is not one the hub ever released')
    for rid, reason in overrides(agents[0]):
        if rid in invariants:
            found.append(f'Overrides names {rid}, an Invariant, which nothing waives')
        elif rid == 'STD-001' and not reason:
            found.append('Overrides names STD-001 without a reason')
    pr = gh.sync_pr(name)
    if pr:
        found.append(f'sync pull request #{pr["number"]} is open')
    return found


def checks_green(gh: GitHub, repo: str, sha: str) -> tuple[bool, str]:
    runs, status = gh.checks(repo, sha)
    pending = [run['name'] for run in runs if run.get('status') != 'completed']
    failed = [run['name'] for run in runs if run.get('status') == 'completed'
              and run.get('conclusion') not in OK_CONCLUSIONS]
    statuses = status.get('statuses') or []
    if pending:
        return False, f'checks still running: {", ".join(pending)}'
    if failed:
        return False, f'checks failed: {", ".join(failed)}'
    if statuses and status.get('state') != 'success':
        return False, f'commit status is {status.get("state")}'
    if not runs and not statuses:
        return False, NOTHING_RAN
    return True, ''


def start_checks(gh: GitHub, repo: str, number: int, waiting: list[dict]) -> str:
    """Start the checks of a pull request the default token opened, and say how.

    GitHub holds such a pull request's runs until someone with write access
    approves them. Approving is what it asks for; where that fails, or no run
    was held, closing and reopening as the owner starts them anyway.
    """
    try:
        for run in waiting:
            gh.approve_run(repo, run['id'])
    except GitHubError:
        waiting = []
    if waiting:
        return f'approved its {len(waiting)} waiting workflow run(s)'
    gh.reopen(repo, number)
    return 'reopened it, which starts its checks'


def merge_one(gh: GitHub, repo: dict, current: str, dry_run: bool) -> str:
    name, base = repo['name'], repo['default_branch']
    listed = gh.sync_pr(name)
    if not listed:
        return f'{name}: no sync pull request'
    number = listed['number']
    pr = gh.pr(name, number)
    files = gh.pr_files(name, number)
    if [f['filename'] for f in files] != [AGENTS] or files[0].get('status') != 'modified':
        return f'{name}: #{number} changes more than the block; review it by hand'
    old = gh.file(name, AGENTS, base)
    new = gh.file(name, AGENTS, pr['head']['sha'])
    if not old or not new or not only_block_changed(old[0], new[0]):
        return f'{name}: #{number} changes more than the block; review it by hand'
    if render.find(new[0]).marker != current:
        return f'{name}: #{number} carries an older block; run its 🔁 Intelligence Sync, or make sync, first'
    if pr.get('mergeable') is not True:
        return f'{name}: #{number} is not mergeable yet ({pr.get("mergeable_state")})'
    # Only now, with the diff proven to be the block alone, is it safe to let
    # a pull request a bot opened run this repository's workflows.
    sha = pr['head']['sha']
    bot = (pr.get('user') or {}).get('type') == 'Bot'
    waiting = gh.waiting_runs(name, sha) if bot else []
    green, why = checks_green(gh, name, sha)
    if waiting or (bot and why == NOTHING_RAN):
        if dry_run:
            return f'{name}: would start the checks of #{number}'
        how = start_checks(gh, name, number, waiting)
        return f'{name}: #{number} waited on its checks, so make merge {how}; run it again once they pass'
    if not green:
        return f'{name}: #{number} waits: {why}'
    if dry_run:
        return f'{name}: would merge #{number}'
    # The squash keeps the sync commit's body, sign-off included, so history
    # still says who certified the change.
    message = gh.commit_message(name, sha).split('\n\n', 1)
    gh.merge(name, number, sha, pr['title'], message[1] if len(message) > 1 else '')
    return f'{name}: merged #{number}'


# --- The stub's side: one repository, in its own workflow ------------------------------------


def write_outputs(values: dict[str, str]) -> None:
    """Hand values to the calling workflow through $GITHUB_OUTPUT; nothing happens outside Actions."""
    path = os.environ.get('GITHUB_OUTPUT')
    if not path:
        return
    with open(path, 'a', encoding='utf-8') as handle:
        for key, value in values.items():
            # A delimiter no text can contain by accident: the bodies are
            # multi-line, and the text of a release is not ours to trust blindly.
            delimiter = f'INTELLIGENCE_{secrets.token_hex(8)}'
            handle.write(f'{key}<<{delimiter}\n{value}\n{delimiter}\n')


def fail(message: str) -> int:
    """Report a problem, as an annotation when Actions runs this."""
    print(('::error title=Intelligence Sync::' if os.environ.get('GITHUB_ACTIONS') == 'true' else '') + message)
    return 1


def release_label(gh: GitHub, hub: str, ref: str) -> str:
    """The version a moving tag such as `v0` points at, so the pull request names the release."""
    if not re.fullmatch(r'v\d+', ref):
        return ref or 'the latest release'
    try:
        tags = gh.api(f'repos/{hub}/tags?per_page=100', paginate=True) or []
    except GitHubError:
        return ref
    at = {tag['name']: tag['commit']['sha'] for tag in tags if isinstance(tag, dict)}
    full = [name for name, sha in at.items()
            if sha == at.get(ref) and re.fullmatch(rf'{re.escape(ref)}\.\d+\.\d+', name)]
    return max(full, key=lambda name: [int(part) for part in name[1:].split('.')], default=ref)


def shipped(root: pathlib.Path) -> str:
    """The region in the home file of the hub tree this runs from: what its release ships."""
    text = (root / render.HOME_FILE).read_text(encoding='utf-8')
    found = render.find(text)
    if found is None or found.edited:
        raise SystemExit(f'{render.HOME_FILE} is not a sound home file')
    return text[found.start:found.end]


def is_hub(checkout: pathlib.Path) -> bool:
    """True in a checkout of the hub, which holds the Constitution and takes no copy of it."""
    return (checkout / render.CONSTITUTION_FILE).is_file() and (checkout / 'scripts' / 'render.py').is_file()


def local_file(checkout: pathlib.Path, name: str) -> str | None:
    """A file's text in the checkout, line endings as they are, or None when it is not there."""
    path = checkout / name
    if path.is_symlink() or (path.exists() and not path.is_file()):
        raise ApplyError(f'{name} is a link or a folder, not a file; review it by hand')
    if not path.exists():
        return None
    with open(path, encoding='utf-8', newline='') as handle:
        return handle.read()


def apply(gh: GitHub, full: str, checkout: pathlib.Path, region: str, ref: str, dry_run: bool) -> int:
    """Write the release's block into one repository's checkout, for the stub's workflow."""
    name = full.split('/', 1)[1]
    unchanged = {'changed': 'false'}
    if is_hub(checkout):
        print(f'{name}: skipped, the hub, which holds the Constitution and carries no copy of it')
        write_outputs(unchanged)
        return 0
    try:
        reason = left_out(gh.repo(full))
        if reason:
            print(f'{name}: skipped, {reason}')
            write_outputs(unchanged)
            return 0
        agents, claude = local_file(checkout, AGENTS), local_file(checkout, CLAUDE)
        change = adopt(name, agents, claude, region)
    except (GitHubError, ApplyError, ValueError) as error:
        return fail(f'{name}: {error}')
    if agents is not None and change.agents == agents and not change.delete_claude:
        print(f'{name}: current')
        write_outputs(unchanged)
        return 0
    block_hash = render.find(region).marker
    title, body, pr_body = messages(block_hash, ref, change, None)
    what = '; '.join(change.adoption) or f'the block, to {block_hash[:12]} from {ref}'
    if dry_run:
        print(f'{name}: would {"adopt" if change.adoption else "update"} ({what})')
        write_outputs(unchanged)
        return 0
    with open(checkout / AGENTS, 'w', encoding='utf-8', newline='') as handle:
        handle.write(change.agents)
    if change.delete_claude:
        (checkout / CLAUDE).unlink()
    print(f'{name}: {"first sync, which " if change.adoption else "updates "}{what}')
    write_outputs({'changed': 'true', 'commit-title': title, 'commit-body': body,
                   'pr-title': title, 'pr-body': pr_body})
    return 0


def main(argv: Sequence[str] | None = None, gh: GitHub | None = None, root: pathlib.Path = ROOT) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('command', choices=('audit', 'sync', 'merge', 'apply'))
    parser.add_argument('--repo', action='append', default=[], metavar='NAME',
                        help='only this repository; repeat for more')
    parser.add_argument('--ref', help='deliver the block from this hub ref instead of the latest release')
    parser.add_argument('--dry-run', action='store_true', help='print what would change, change nothing')
    parser.add_argument('--path', default='.', help='apply: the checkout to write into (default: here)')
    parser.add_argument('--release', default='',
                        help="apply: the hub ref this tree came from, such as v0, for the pull request's text")
    parser.add_argument('--hub', default='tannergolden/intelligence',
                        help='apply: the hub repository, to name the version a moving tag points at')
    args = parser.parse_args(argv)
    if args.command == 'apply':
        full = os.environ.get('GITHUB_REPOSITORY', '')
        if not re.fullmatch(r'[^/\s]+/[^/\s]+', full):
            parser.error("apply runs in a repository's workflow, which sets GITHUB_REPOSITORY to owner/name")
        gh = gh or GitHub(full.split('/', 1)[0])
        return apply(gh, full, pathlib.Path(args.path), shipped(root),
                     release_label(gh, args.hub, args.release), args.dry_run)
    gh = gh or GitHub()
    region, ref = delivered(root, args.ref)
    current = render.find(region).marker
    try:
        chosen, skipped = targets(gh, args.repo, hub_name(root))
    except GitHubError as error:
        print(f'cannot list your repositories through gh: {error}', file=sys.stderr)
        return 1
    for line in skipped:
        print(line)
    failures = 0
    if args.command == 'audit':
        known = history(root)
        constitution = render.load_constitution(root)
        invariants = {rid for rid, rule in constitution.rules.items() if rule.kind == 'invariant'}
        print(f'Auditing against {ref}, block sha256 {current[:12]}')
        for repo in chosen:
            try:
                found = audit_one(gh, repo, current, known, invariants)
                stub = gh.file(repo['name'], STUB, repo['default_branch']) is not None
            except GitHubError as error:
                found, stub = [str(error)], True
            failures += bool(found)
            # The stub is a choice, not a defect: without it the block is still
            # whole, and only make sync keeps it current.
            print(f'{repo["name"]}: ' + ('; '.join(found) if found else 'current')
                  + ('' if stub else ' (no stub, so only make sync updates it)'))
        return 1 if failures else 0
    signer = identity(gh) if args.command == 'sync' and not args.dry_run else None
    for repo in chosen:
        try:
            if args.command == 'sync':
                print(sync_one(gh, repo, region, ref, signer, args.dry_run))
            else:
                print(merge_one(gh, repo, current, args.dry_run))
        except GitHubError as error:
            failures += 1
            print(f'{repo["name"]}: {error}')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
