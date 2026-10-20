#!/usr/bin/env python3
"""Install the universal rules into every AI app's home folder, check them, and take them out.

WHY THIS EXISTS. Each app reads its user-level instructions from a different
place, and none of them reads one shared file. So the home kit writes a
byte-identical copy of the rules where each app looks:

- `~/.agents/AGENTS.md`: the master copy every other copy is checked
  against, which Warp, Cline, goose and Kimi Code also read
- `~/.claude/rules/intelligence.md`, or `~/.claude/CLAUDE.md` in a Claude
  cloud session
- `~/.codex/AGENTS.md`
- `~/.gemini/AGENTS.md`, for Antigravity CLI
- `~/.copilot/instructions/intelligence.instructions.md`

It also writes Claude Code's `instructionFiles` setting, so Claude reads a
repository's `AGENTS.md` even beside a `CLAUDE.md`, and, outside a cloud
session, `permissions.ask` rules, so Claude Code asks before each outward
action OPS-005 names: a push, a pull request, an issue or a comment, a
release, a new repository, fork, gist or workflow run, a write through `gh
api`, a published package, and the GitHub MCP server's writes. Permissions
of a shape it cannot add to are left alone, and never stop the setting.
Grok Build reads `~/.claude` by default, so it gets no copy of its own.
Cursor's User Rules live in its settings, so they are pasted by hand.

They are copies, never links, because links fail silently in Claude's desktop
sessions and in Grok's sandbox. A file the kit owns outright holds nothing
else. In a file that also holds your own notes, the rules sit in a marked
block and your text stays.

THE KIT. Given a release's `kit.json` as well, it installs the modules around
the rules, each only where that app reads it:

- the guard hook, `~/.agents/hooks/intelligence-guard.py`, registered as a
  pre-tool hook in Claude Code's settings (which Grok Build and Cursor also
  read), in Codex's `hooks.json`, in a file of its own for Copilot, and in
  Antigravity's `hooks.json`; outside a cloud session, Claude Code also runs
  it after each compaction, to bring the Invariants back into the
  conversation
- the skills, copied into `~/.agents/skills/`, `~/.claude/skills/` and
  Antigravity's own skills folder
- the subagents, for Claude Code, Copilot and Codex

SAFETY. Before changing a file, it records the setting's prior value, the
ask rules it added, and whether it created the file. `uninstall` uses that
record to put everything back, and leaves every rule you wrote. It never
overwrites a file it does not own: a file, folder or hook is the kit's only
if it carries the kit's mark. A file that is a symlink is written through,
so the link stays. It runs on the Python 3.9 that macOS ships,
with the standard library only, and makes no network calls: whoever runs it
has already downloaded the release files and checked their SHA-256.

Run it:

    python3 install.py install --home-file intelligence.md [--kit-file kit.json]
    python3 install.py check --home-file intelligence.md [--kit-file kit.json]
    python3 install.py uninstall
    python3 install.py install --home-file intelligence.md --cloud   # Claude cloud session
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import pathlib
import re
import shlex
import shutil
import sys
import tempfile
from collections.abc import Callable, Mapping

# `knowledge` marks the facts block earlier releases wrote beside each copy of
# the rules. The kit carries no facts now (ADR-0023); the marker stays so an
# install can find an old block and take it out.
MARKERS = {'rules': 'INTELLIGENCE', 'knowledge': 'INTELLIGENCE:KNOWLEDGE'}
# The kit format this installer reads: 2 dropped the knowledge facts.
KIT_FORMAT = 2


def pattern(name: str) -> re.Pattern:
    return re.compile(
        rf'^<!-- {re.escape(name)}:BEGIN sha256:(?P<hash>[0-9a-f]{{64}}) -->[ \t]*\r?\n'
        r'(?P<inner>.*?)'
        rf'^<!-- {re.escape(name)}:END -->[ \t]*(?:\r?\n|\Z)',
        re.M | re.S,
    )


REGIONS = {piece: pattern(name) for piece, name in MARKERS.items()}
REGION = REGIONS['rules']

PLUGIN_IDS = ('cc-plugin-agents-md@builtin', 'agents-md@builtin')
READ_BOTH = 'claude-md-and-agents-md'
SETTINGS = '.claude/settings.json'
COPILOT_PREFIX = '---\napplyTo: "**"\n---\n\n'
# What Claude Code asks your user before, every time (OPS-005): a push; a pull
# request (drafts too) or an issue, opened, edited or closed; a comment or
# review; a release; a repository, fork, gist or workflow run; a write through
# `gh api`; a published package; and the GitHub MCP server's writes. A rule
# with one ` *` at its end also matches the bare command, and a `*` elsewhere
# matches anything, so the `gh api` rules find a method flag wherever it
# stands, a field or body flag after a REST path under repos/, and a GraphQL
# mutation, leaving GraphQL queries, which read, to run without asking. A rule
# matches the command as it is usually typed, not every
# spelling of it; the guard denies the merges and deletions among these
# outright, and keeps these rules from being edited away. guard.py holds the
# same list, which a test holds.
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

# What marks a file or folder as the kit's own; it matches kit.py's OWNED.
OWNED = "Part of tannergolden/intelligence's home kit, which replaces this file on every install."
GUARD = '.agents/hooks/intelligence-guard.py'
GUARD_NAME = 'intelligence-guard'
SKILL_MARK = '.intelligence-kit'
HOOK_TIMEOUT = 30
# The tools each app's guard registration covers. Claude and Codex filter by
# name, so most tool calls never start Python; Copilot and Antigravity name
# tools in ways this kit cannot pin down, so every call reaches the guard,
# which checks the tool itself. Claude's Read is in, so the guard can deny
# reading a credential store (SEC-001), at one Python start per read; Grep
# and Glob stay out.
CLAUDE_MATCHER = '^(Bash|PowerShell|Edit|Write|MultiEdit|NotebookEdit|Read)$|mcp__'
CODEX_MATCHER = '^(Bash|apply_patch|Edit|Write)$|mcp__'
# Claude Code runs a SessionStart hook with this matcher after it compacts a
# conversation, and adds what the hook prints to the compacted context.
COMPACT_MATCHER = 'compact'


@dataclasses.dataclass(frozen=True)
class Target:
    """One place an app reads its user-level instructions."""

    app: str
    rel: str  # under the home folder
    mode: str  # 'file': the kit owns the file; 'block': a marked block in a personal file
    where: str  # 'local', 'cloud' or 'both'
    prefix: str = ''  # what precedes the block in a file the kit owns
    piece: str = 'rules'  # 'rules', from the home file, or 'knowledge', a retired block (RETIRED)

    def key(self, path: pathlib.Path) -> str:
        """The install record's name for this target; one file can hold both pieces."""
        return str(path) if self.piece == 'rules' else f'{path}#{self.piece}'


TARGETS = (
    Target('master copy', '.agents/AGENTS.md', 'block', 'local'),
    Target('Claude Code', '.claude/rules/intelligence.md', 'file', 'local'),
    Target('Claude Code', '.claude/CLAUDE.md', 'block', 'cloud'),
    Target('Codex', '.codex/AGENTS.md', 'block', 'local'),
    Target('Antigravity CLI', '.gemini/AGENTS.md', 'block', 'local'),
    Target('Copilot', '.copilot/instructions/intelligence.instructions.md', 'file', 'local',
           COPILOT_PREFIX),
)

# Where earlier releases wrote the knowledge facts, beside each copy of the
# rules. The kit carries none now (ADR-0023), so an install takes out what one
# of those releases left, and so does an uninstall without a record.
RETIRED = (
    Target('master copy', '.agents/AGENTS.md', 'block', 'local', piece='knowledge'),
    Target('Claude Code', '.claude/rules/intelligence-knowledge.md', 'file', 'local', piece='knowledge'),
    Target('Claude Code', '.claude/CLAUDE.md', 'block', 'cloud', piece='knowledge'),
    Target('Codex', '.codex/AGENTS.md', 'block', 'local', piece='knowledge'),
    Target('Antigravity CLI', '.gemini/AGENTS.md', 'block', 'local', piece='knowledge'),
    Target('Copilot', '.copilot/instructions/intelligence-knowledge.instructions.md', 'file', 'local',
           COPILOT_PREFIX, piece='knowledge'),
)

# Where each app reads skills; Claude Code reads nothing under .agents/.
SKILL_ROOTS = (
    ('the shared skills folder', '.agents/skills', 'local'),
    ('Claude Code', '.claude/skills', 'both'),
    ('Antigravity CLI', '.gemini/antigravity-cli/skills', 'local'),
)

# Files that would hide a copy, or load the rules a second time.
SHADOWS = (
    ('.codex/AGENTS.override.md', 'Codex reads this instead of ~/.codex/AGENTS.md'),
    ('AGENTS.md', 'apps that walk up the folder tree load it in every project under home'),
    ('CLAUDE.md', 'Claude Code loads it in every project under home'),
)


class Refused(Exception):
    """A change the kit will not make, with the reason as its message."""


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


@dataclasses.dataclass(frozen=True)
class Found:
    start: int
    end: int
    marker: str
    inner: str

    @property
    def edited(self) -> bool:
        return digest(self.inner) != self.marker


def find(text: str, piece: str = 'rules') -> Found | None:
    matches = list(REGIONS[piece].finditer(text))
    if len(matches) > 1:
        raise Refused(f'holds more than one {MARKERS[piece]} block; remove the extra by hand')
    if not matches:
        return None
    match = matches[0]
    inner = match.group('inner').replace('\r\n', '\n').strip('\n') + '\n'
    return Found(match.start(), match.end(), match.group('hash'), inner)


def read_region_file(path: pathlib.Path, piece: str, what: str) -> tuple[str, str]:
    """The region in a file that must be exactly one unedited block, and its hash."""
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as error:
        raise SystemExit(f'cannot read the {what} {path}: {error}') from error
    return exact_region(text, piece, f'{path}', what)


def exact_region(text: str, piece: str, where: str, what: str) -> tuple[str, str]:
    found = find(text, piece)
    if found is None or text[:found.start].strip() or text[found.end:].strip():
        raise SystemExit(f'{where} is not a {what}: it must be exactly one {MARKERS[piece]} block')
    if found.edited:
        raise SystemExit(f'{where} was edited: its content does not match the hash in its marker')
    return text[found.start:found.end], found.marker


def read_home_file(path: pathlib.Path) -> tuple[str, str]:
    """The region to install and its hash, from a home file rendered by the hub."""
    return read_region_file(path, 'rules', 'home file')


@dataclasses.dataclass(frozen=True)
class Kit:
    """A release's kit.json: the guard, the skills and the subagents."""

    guard: str
    skills: dict[str, dict[str, str]]
    subagents: dict[str, dict[str, str]]


def read_kit(path: pathlib.Path) -> Kit:
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if data.get('format') != KIT_FORMAT:
            raise SystemExit(f'{path} is a kit in format {data.get("format")}; '
                             f'this installer reads format {KIT_FORMAT}')
        guard, skills, subagents = data['guard'], data['skills'], data['subagents']
    except (OSError, UnicodeDecodeError, ValueError, KeyError, TypeError, AttributeError) as error:
        raise SystemExit(f'cannot read the kit {path}: {error}') from error
    if OWNED not in guard:
        raise SystemExit(f'{path} carries a guard without the kit\'s mark')
    for name, files in skills.items():
        for rel in files:
            if rel.startswith('/') or '..' in pathlib.PurePosixPath(rel).parts or not re.match(
                    r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
                raise SystemExit(f'{path} names a skill file outside its folder: {name}/{rel}')
    for name in subagents:
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            raise SystemExit(f'{path} names a subagent that is not a plain name: {name}')
    return Kit(guard, skills, subagents)


def codex_home(home: pathlib.Path, env: Mapping[str, str]) -> pathlib.Path:
    return pathlib.Path(env['CODEX_HOME']) if env.get('CODEX_HOME') else home / '.codex'


def resolve(target: Target, home: pathlib.Path, env: Mapping[str, str]) -> pathlib.Path:
    if target.rel == '.codex/AGENTS.md':
        return codex_home(home, env) / 'AGENTS.md'
    return home / target.rel


def targets_for(cloud: bool, targets: tuple[Target, ...] = TARGETS) -> list[Target]:
    return [t for t in targets if t.where in ('both', 'cloud' if cloud else 'local')]


def read(path: pathlib.Path) -> str | None:
    if not path.exists():
        return None
    with open(path, encoding='utf-8', newline='') as handle:
        return handle.read()


def write(path: pathlib.Path, text: str, mode: int | None = None) -> None:
    """Replace `path` in one step, keeping its permissions unless told otherwise.

    A symlink is written through, so a settings file your dotfiles link stays a link to the file they keep.
    """
    if path.is_symlink():
        path = path.resolve()
    if mode is None and path.exists():
        mode = path.stat().st_mode & 0o777
    fd, tmp = tempfile.mkstemp(prefix='.intelligence-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as handle:
            handle.write(text)
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def missing_dirs(path: pathlib.Path) -> list[pathlib.Path]:
    return [parent for parent in reversed(path.parents) if not parent.exists()]


def make_dirs(path: pathlib.Path) -> None:
    for folder in missing_dirs(path):
        folder.mkdir()


def placed(target: Target, current: str | None, region: str) -> tuple[str, str]:
    """The file's new text with the block in place, and what was added before the block.

    The second value is the separator written ahead of an appended block, so
    an uninstall can take exactly that back out; it is empty when the block
    replaced an older one or the file is new.
    """
    if target.mode == 'file':
        if current is not None and find(current, target.piece) is None:
            raise Refused("exists and is not the kit's; it is never overwritten")
        return target.prefix + region, ''
    if not current:
        return region, ''
    found = find(current, target.piece)
    if found is not None:
        return current[:found.start] + region + current[found.end:], ''
    joiner = '\n' if current.endswith('\n') else '\n\n'
    return current + joiner + region, joiner


def removed(current: str, joiner: str, piece: str = 'rules') -> str:
    """The file's text with the kit's block, and the separator it added, taken out."""
    found = find(current, piece)
    if found is None:
        return current
    before, after = current[:found.start], current[found.end:]
    if joiner and before.endswith(joiner):
        before = before[:-len(joiner)]
    return before + after


def state_path(home: pathlib.Path, env: Mapping[str, str]) -> pathlib.Path:
    base = env.get('XDG_STATE_HOME') or str(home / '.local' / 'state')
    return pathlib.Path(base) / 'intelligence' / 'install.json'


def load_state(path: pathlib.Path) -> dict:
    state = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    state.setdefault('format', 1)
    for key in ('files', 'owned', 'folders', 'hooks'):
        state.setdefault(key, {})
    state.setdefault('settings', None)
    return state


def save_state(path: pathlib.Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write(path, json.dumps(state, indent=2) + '\n')


def read_json(path: pathlib.Path) -> dict:
    text = read(path)
    if text is None or not text.strip():
        return {}
    try:
        data = json.loads(text)
    except ValueError as error:
        raise Refused(f'is not valid JSON ({error}); fix it first, it is never overwritten') from error
    if not isinstance(data, dict):
        raise Refused('is not a JSON object; it is never overwritten')
    return data


read_settings = read_json


def reads_both(data: dict, plugin: str) -> bool:
    value: object = data
    for key in ('pluginConfigs', plugin, 'options', 'instructionFiles'):
        value = value.get(key) if isinstance(value, dict) else None
    return value == READ_BOTH


def apply_setting(data: dict) -> dict:
    """A copy of Claude's settings with both plugin IDs reading AGENTS.md beside CLAUDE.md."""
    data = json.loads(json.dumps(data))
    configs = data.setdefault('pluginConfigs', {})
    if not isinstance(configs, dict):
        raise Refused('has a pluginConfigs that is not an object; it is never overwritten')
    for plugin in PLUGIN_IDS:
        entry = configs.setdefault(plugin, {})
        if not isinstance(entry, dict):
            raise Refused(f'has a {plugin} entry that is not an object; it is never overwritten')
        options = entry.setdefault('options', {})
        if not isinstance(options, dict):
            raise Refused(f'has {plugin} options that are not an object; it is never overwritten')
        options['instructionFiles'] = READ_BOTH
    return data


def ask_list(data: dict) -> list:
    """Claude's `permissions.ask` rules, from settings whose shape the kit can add to without guessing."""
    permissions = data.get('permissions', {})
    if not isinstance(permissions, dict):
        raise Refused('has permissions that are not an object; it is never overwritten')
    asks = permissions.get('ask', [])
    if not isinstance(asks, list):
        raise Refused('has a permissions.ask that is not a list; it is never overwritten')
    return asks


def apply_asks(data: dict, dropped: list[str]) -> dict:
    """Claude's settings with every ask rule in place, and the kit's own rules a release dropped taken out."""
    asks = ask_list(data)
    missing = [rule for rule in ASK_RULES if rule not in asks]
    stale = [rule for rule in dropped if rule in asks]
    if not missing and not stale:
        return data
    data = json.loads(json.dumps(data))
    permissions = data.setdefault('permissions', {})
    kept = list(permissions.get('ask', []))
    for rule in stale:
        kept.remove(rule)  # the one the kit added; a copy of your own stays
    permissions['ask'] = kept + missing
    return data


def report(status: str, label: str) -> None:
    print(f'  {status}  {label}')


def install(home: pathlib.Path, home_file: pathlib.Path, cloud: bool, env: Mapping[str, str],
            dry_run: bool = False, kit_file: pathlib.Path | None = None) -> int:
    region, block_hash = read_home_file(home_file)
    kit = read_kit(kit_file) if kit_file else None
    spath = state_path(home, env)
    state = load_state(spath)
    failures = 0
    for target in targets_for(cloud):
        path = resolve(target, home, env)
        label = f'{target.app}: {path}'
        try:
            current = read(path)
            text, joiner = placed(target, current, region)
        except (Refused, UnicodeDecodeError) as error:
            report('refused', f'{label} {error}')
            failures += 1
            continue
        changed = text != current
        report('current' if not changed else 'would write' if dry_run else 'wrote', label)
        if dry_run:
            continue
        # Recorded before the write, and kept from the first install, so an
        # uninstall restores what was there before the kit ever ran.
        record = state['files'].setdefault(target.key(path), {
            'path': str(path), 'piece': target.piece, 'mode': target.mode, 'created': current is None,
            'joiner': joiner, 'dirs': [str(folder) for folder in missing_dirs(path)],
        })
        if joiner:
            record['joiner'] = joiner
        save_state(spath, state)
        if changed:
            make_dirs(path)
            write(path, text)
    failures += retire(home, cloud, env, state, spath, dry_run)
    if not cloud:
        failures += install_setting(home, state, spath, dry_run)
    if kit is not None:
        failures += install_kit(home, kit, cloud, env, state, spath, dry_run)
    if not dry_run:
        state['hash'] = block_hash
        state.pop('knowledge_hash', None)
        save_state(spath, state)
    print('  manual   Cursor: paste the home file into Settings > Rules > User Rules, '
          'and again whenever the block changes')
    for line in shadows(home, env):
        print(f'  warning  {line}')
    return 1 if failures else 0


def retire(home: pathlib.Path, cloud: bool, env: Mapping[str, str], state: dict, spath: pathlib.Path,
           dry_run: bool) -> int:
    """Take out the knowledge facts an earlier release wrote, and the record of them."""
    failures = 0
    for target in targets_for(cloud, RETIRED):
        path = resolve(target, home, env)
        key = target.key(path)
        label = f'{target.app} knowledge: {path}'
        try:
            current = read(path)
            found = None if current is None else find(current, target.piece)
        except (Refused, UnicodeDecodeError) as error:
            report('refused', f'{label} {error}')
            failures += 1
            continue
        if found is not None:
            report('would retire' if dry_run else 'retired', label)
            if not dry_run:
                if target.mode == 'file':
                    path.unlink()
                else:
                    # The block went in after the rules, behind the separator the install recorded.
                    joiner = state['files'].get(key, {}).get('joiner', '\n')
                    write(path, removed(current, joiner, target.piece))
        if key in state['files'] and not dry_run:
            del state['files'][key]
            save_state(spath, state)
    return failures


def install_setting(home: pathlib.Path, state: dict, spath: pathlib.Path, dry_run: bool) -> int:
    """Claude Code's instructionFiles setting and its ask rules, merged into the settings you keep. Permissions of a
    shape the kit cannot add to are refused on their own, and the setting is written all the same."""
    path = home / SETTINGS
    label, asks_label = f'Claude Code setting: {path}', f'Claude Code ask rules: {path}'
    recorded = (state.get('settings') or {}).get('asks', [])
    try:
        data = read_settings(path)
        reading = apply_setting(data)
    except Refused as error:
        report('refused', f'{label} {error}')
        return 1
    report('current' if reading == data else 'would write' if dry_run else 'wrote', label)
    failures = 0
    try:
        updated = apply_asks(reading, [rule for rule in recorded if rule not in ASK_RULES])
        added = [rule for rule in ASK_RULES if rule not in ask_list(data)]
    except Refused as error:
        report('refused', f'{asks_label} {error}')
        updated, added, failures = reading, [], 1
    else:
        report('current' if updated == reading else 'would write' if dry_run else 'wrote', asks_label)
    if updated == data or dry_run:
        return failures
    if state.get('settings') is None:
        configs = data.get('pluginConfigs')
        state['settings'] = {
            'path': str(path),
            'created': not path.exists(),
            'dirs': [str(folder) for folder in missing_dirs(path)],
            'had_plugin_configs': isinstance(configs, dict),
            'prior': {plugin: (configs or {}).get(plugin) if isinstance(configs, dict) else None
                      for plugin in PLUGIN_IDS},
        }
    record = state['settings']
    if added and 'had_permissions' not in record:
        # Whether these were yours before the kit's first rule, so an uninstall
        # takes out only what it made.
        record['had_permissions'] = 'permissions' in data
        record['had_ask'] = 'ask' in data.get('permissions', {})
    kept = [rule for rule in record.get('asks', []) if rule in ASK_RULES]
    record['asks'] = kept + [rule for rule in added if rule not in kept]
    save_state(spath, state)
    make_dirs(path)
    write(path, json.dumps(updated, indent=2) + '\n')
    return failures


# --- the kit ------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Owned:
    """A file the kit writes whole, and the text that marks it as the kit's."""

    label: str
    path: pathlib.Path
    text: str
    mark: str = OWNED
    mode: int | None = None


@dataclasses.dataclass(frozen=True)
class Registration:
    """The guard's entry in a hook file that other hooks share."""

    label: str
    path: pathlib.Path
    apply: Callable[[dict], dict]  # the file's data with the guard registered
    remove: Callable[[dict], dict]  # the file's data with the guard taken out


def guard_command(home: pathlib.Path, app: str) -> str:
    # The interpreter that is running the install, which is known to work here.
    python = sys.executable or 'python3'
    return f'{shlex.quote(python)} {shlex.quote(str(home / GUARD))} --app {app}'


def remind_command(home: pathlib.Path) -> str:
    """The guard in its other mode: print the Invariants from Claude Code's home copy, after a compaction."""
    python = sys.executable or 'python3'
    return f'{shlex.quote(python)} {shlex.quote(str(home / GUARD))} --remind'


def guard_commands(data: object) -> list[str]:
    """Every hook command in a JSON document that runs the guard."""
    if isinstance(data, dict):
        found = [data['command']] if is_guard(data) else []
        return found + [c for value in data.values() for c in guard_commands(value)]
    if isinstance(data, list):
        return [command for value in data for command in guard_commands(value)]
    return []


def is_guard(entry: object) -> bool:
    return isinstance(entry, dict) and GUARD_NAME in str(entry.get('command', ''))


def group_is_guard(group: object) -> bool:
    return isinstance(group, dict) and any(is_guard(h) for h in group.get('hooks') or [])


def put_group(data: dict, event: str, group: dict) -> dict:
    """`data` with the guard's group for `event` in place: replaced where it was, else appended.

    Replacing in place matters to Codex, which trusts a hook by its position.
    """
    data = json.loads(json.dumps(data))
    hooks = data.setdefault('hooks', {})
    if not isinstance(hooks, dict):
        raise Refused('has hooks that are not an object; it is never overwritten')
    groups = hooks.setdefault(event, [])
    if not isinstance(groups, list):
        raise Refused(f'has {event} hooks that are not a list; it is never overwritten')
    for index, existing in enumerate(groups):
        if group_is_guard(existing):
            groups[index] = group
            break
    else:
        groups.append(group)
    return data


def drop_groups(data: dict, event: str) -> dict:
    data = json.loads(json.dumps(data))
    hooks = data.get('hooks')
    if isinstance(hooks, dict) and isinstance(hooks.get(event), list):
        hooks[event] = [group for group in hooks[event] if not group_is_guard(group)]
        if not hooks[event]:
            del hooks[event]
        if not hooks:
            del data['hooks']
    return data


def entry(command: str, **extra: object) -> dict:
    return {'type': 'command', 'command': command, 'timeout': HOOK_TIMEOUT, **extra}


def kit_owned(home: pathlib.Path, kit: Kit, cloud: bool, env: Mapping[str, str]) -> list[Owned]:
    """Every file the kit writes whole, for this machine."""
    owned = [Owned('guard hook', home / GUARD, kit.guard, mode=0o755)]
    for name, forms in sorted(kit.subagents.items()):
        owned.append(Owned(f'Claude Code subagent {name}', home / '.claude' / 'agents' / f'{name}.md',
                           forms['claude']))
        if not cloud:
            owned.append(Owned(f'Copilot agent {name}', home / '.copilot' / 'agents' / f'{name}.agent.md',
                               forms['copilot']))
            owned.append(Owned(f'Codex agent {name}', codex_home(home, env) / 'agents' / f'{name}.toml',
                               forms['codex']))
    if not cloud:
        copilot = {'version': 1, 'hooks': {'PreToolUse': [
            {'hooks': [entry(guard_command(home, 'copilot'))]}]}}
        owned.append(Owned('Copilot guard hook', home / '.copilot' / 'hooks' / 'intelligence.json',
                           json.dumps(copilot, indent=2) + '\n', mark=GUARD_NAME))
    return owned


def kit_registrations(home: pathlib.Path, cloud: bool, env: Mapping[str, str]) -> list[Registration]:
    """The guard's entries in hook files the kit shares with your own hooks."""
    claude = {'matcher': CLAUDE_MATCHER,
              'hooks': [entry(guard_command(home, 'claude'), onFailure='block')]}
    found = [Registration('Claude Code guard hook (also read by Grok Build and Cursor)', home / SETTINGS,
                          lambda data: put_group(data, 'PreToolUse', claude),
                          lambda data: drop_groups(data, 'PreToolUse'))]
    if cloud:
        return found
    reminder = {'matcher': COMPACT_MATCHER, 'hooks': [entry(remind_command(home))]}
    found.append(Registration('Claude Code compaction reminder', home / SETTINGS,
                              lambda data: put_group(data, 'SessionStart', reminder),
                              lambda data: drop_groups(data, 'SessionStart')))
    codex = {'matcher': CODEX_MATCHER, 'hooks': [entry(guard_command(home, 'codex'))]}
    antigravity = {'PreToolUse': [{'hooks': [entry(guard_command(home, 'antigravity'))]}]}

    def put_named(data: dict) -> dict:
        if 'intelligence' in data and GUARD_NAME not in json.dumps(data['intelligence']):
            raise Refused('holds an "intelligence" hook that is not the kit\'s; it is never overwritten')
        data = json.loads(json.dumps(data))
        data['intelligence'] = antigravity
        return data

    def drop_named(data: dict) -> dict:
        data = json.loads(json.dumps(data))
        data.pop('intelligence', None)
        return data

    found += [
        Registration('Codex guard hook', codex_home(home, env) / 'hooks.json',
                     lambda data: put_group(data, 'PreToolUse', codex),
                     lambda data: drop_groups(data, 'PreToolUse')),
        Registration('Antigravity CLI guard hook', home / '.gemini' / 'config' / 'hooks.json',
                     put_named, drop_named),
    ]
    return found


def skill_folders(home: pathlib.Path, cloud: bool) -> list[tuple[str, pathlib.Path]]:
    return [(app, home / rel) for app, rel, where in SKILL_ROOTS if where == 'both' or not cloud]


def is_kits(path: pathlib.Path, mark: str) -> bool:
    try:
        return mark in (read(path) or '')
    except (OSError, UnicodeDecodeError):
        return False


def install_kit(home: pathlib.Path, kit: Kit, cloud: bool, env: Mapping[str, str], state: dict,
                spath: pathlib.Path, dry_run: bool) -> int:
    failures = 0
    for item in kit_owned(home, kit, cloud, env):
        label = f'{item.label}: {item.path}'
        current = read(item.path) if item.path.exists() else None
        if current is not None and item.mark not in current:
            report('refused', f"{label} exists and is not the kit's; it is never overwritten")
            failures += 1
            continue
        mode_ok = item.mode is None or (item.path.exists() and item.path.stat().st_mode & 0o777 == item.mode)
        changed = current != item.text or not mode_ok
        report('current' if not changed else 'would write' if dry_run else 'wrote', label)
        if dry_run or not changed:
            continue
        state['owned'].setdefault(str(item.path), {
            'created': current is None, 'dirs': [str(folder) for folder in missing_dirs(item.path)]})
        save_state(spath, state)
        make_dirs(item.path)
        write(item.path, item.text, item.mode)
    for registration in kit_registrations(home, cloud, env):
        failures += install_registration(registration, state, spath, dry_run)
    for name, files in sorted(kit.skills.items()):
        for app, root in skill_folders(home, cloud):
            failures += install_skill(f'{app} skill {name}', root / name, files, state, spath, dry_run)
    return failures


def install_registration(registration: Registration, state: dict, spath: pathlib.Path,
                         dry_run: bool) -> int:
    path = registration.path
    label = f'{registration.label}: {path}'
    try:
        data = read_json(path)
        updated = registration.apply(data)
    except Refused as error:
        report('refused', f'{label} {error}')
        return 1
    if updated == data:
        report('current', label)
        return 0
    report('would write' if dry_run else 'wrote', label)
    if dry_run:
        return 0
    state['hooks'].setdefault(str(path), {
        'created': not path.exists(), 'dirs': [str(folder) for folder in missing_dirs(path)]})
    save_state(spath, state)
    make_dirs(path)
    write(path, json.dumps(updated, indent=2) + '\n')
    return 0


def install_skill(label: str, folder: pathlib.Path, files: dict[str, str], state: dict,
                  spath: pathlib.Path, dry_run: bool) -> int:
    label = f'{label}: {folder}'
    if folder.exists() and not (folder / SKILL_MARK).exists():
        report('refused', f"{label} exists and is not the kit's; it is never overwritten")
        return 1
    wanted = {**files, SKILL_MARK: OWNED + '\n'}
    present = {path.relative_to(folder).as_posix() for path in folder.rglob('*') if path.is_file()} \
        if folder.exists() else set()
    changed = present != set(wanted) or any(read(folder / rel) != text for rel, text in wanted.items())
    report('current' if not changed else 'would write' if dry_run else 'wrote', label)
    if dry_run or not changed:
        return 0
    state['folders'].setdefault(str(folder), {
        'created': not folder.exists(), 'dirs': [str(path) for path in missing_dirs(folder)]})
    save_state(spath, state)
    for rel in sorted(present - set(wanted)):
        (folder / rel).unlink()
    for rel, text in sorted(wanted.items()):
        path = folder / rel
        make_dirs(path)
        write(path, text)
    for path in sorted(folder.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return 0


def shadows(home: pathlib.Path, env: Mapping[str, str]) -> list[str]:
    found = []
    for rel, why in SHADOWS:
        path = (codex_home(home, env) / 'AGENTS.override.md'
                if rel == '.codex/AGENTS.override.md' else home / rel)
        if path.exists():
            found.append(f'{path} exists: {why}')
    return found


# --- check ----------------------------------------------------------------------


def check(home: pathlib.Path, home_file: pathlib.Path, cloud: bool, env: Mapping[str, str],
          kit_file: pathlib.Path | None = None) -> int:
    region, block_hash = read_home_file(home_file)
    kit = read_kit(kit_file) if kit_file else None
    failures = 0
    for target in targets_for(cloud):
        path = resolve(target, home, env)
        status = target_status(target, read(path), region, block_hash)
        if status != 'current':
            failures += 1
        print(f'  {status:<8} {target.app}: {path}')
    for target in targets_for(cloud, RETIRED):
        path = resolve(target, home, env)
        try:
            current = read(path)
            left = current is not None and find(current, target.piece) is not None
        except (Refused, UnicodeDecodeError):
            left = True
        if left:
            failures += 1
            print(f'  {"stale":<8} {target.app} knowledge: {path}, retired; an install takes it out')
    if not cloud:
        # Each setting on its own: permissions the kit cannot read say nothing about instructionFiles.
        path = home / SETTINGS
        try:
            data = read_settings(path)
        except Refused:
            data = None
        setting = 'broken' if data is None else 'current' if all(
            reads_both(data, plugin) for plugin in PLUGIN_IDS) else 'missing'
        try:
            asks = 'broken' if data is None else 'current' if all(
                rule in ask_list(data) for rule in ASK_RULES) else 'missing'
        except Refused:
            asks = 'broken'
        failures += (setting != 'current') + (asks != 'current')
        print(f'  {setting:<8} Claude Code setting: {path}')
        print(f'  {asks:<8} Claude Code ask rules: {path}')
    if kit is not None:
        failures += check_kit(home, kit, cloud, env)
    for line in shadows(home, env):
        print(f'  warning  {line}')
    print('  manual   Cursor: check Settings > Rules > User Rules by hand')
    return 1 if failures else 0


def check_kit(home: pathlib.Path, kit: Kit, cloud: bool, env: Mapping[str, str]) -> int:
    failures = 0
    for item in kit_owned(home, kit, cloud, env):
        current = read(item.path) if item.path.exists() else None
        status = ('missing' if current is None else 'foreign' if item.mark not in current
                  else 'edited' if current != item.text else 'current')
        failures += status != 'current'
        print(f'  {status:<8} {item.label}: {item.path}')
    for registration in kit_registrations(home, cloud, env):
        try:
            data = read_json(registration.path)
            commands = guard_commands(data)
            if any(not os.path.exists(shlex.split(command)[0]) for command in commands):
                status = 'broken'  # the Python it runs with is gone; install again
            elif registration.apply(data) == data:
                status = 'current'
            else:
                # Two registrations can share a file, so each looks for its own entry.
                status = 'missing' if registration.remove(data) == data else 'stale'
        except (Refused, ValueError):
            status = 'broken'
        failures += status != 'current'
        print(f'  {status:<8} {registration.label}: {registration.path}')
    for name, files in sorted(kit.skills.items()):
        for app, root in skill_folders(home, cloud):
            folder = root / name
            if not folder.exists():
                status = 'missing'
            elif not (folder / SKILL_MARK).exists():
                status = 'foreign'
            else:
                present = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
                wanted = {**files, SKILL_MARK: OWNED + '\n'}
                status = 'current' if present == set(wanted) and all(
                    read(folder / rel) == text for rel, text in wanted.items()) else 'edited'
            failures += status != 'current'
            print(f'  {status:<8} {app} skill {name}: {folder}')
    return failures


def target_status(target: Target, current: str | None, region: str, block_hash: str) -> str:
    if current is None:
        return 'missing'
    try:
        found = find(current, target.piece)
    except Refused:
        return 'broken'
    if found is None:
        return 'missing'
    if found.edited:
        return 'edited'
    if found.marker != block_hash:
        return 'stale'
    if target.mode == 'file' and current != target.prefix + region:
        return 'edited'
    return 'current'


# --- uninstall ------------------------------------------------------------------


def uninstall(home: pathlib.Path, env: Mapping[str, str], dry_run: bool = False) -> int:
    spath = state_path(home, env)
    state = load_state(spath)
    records = state['files']
    recorded = bool(records)
    if not recorded:
        # No record of an install: take out only what is unmistakably the kit's.
        records = {t.key(resolve(t, home, env)): {'path': str(resolve(t, home, env)), 'piece': t.piece,
                                                  'mode': t.mode, 'created': False, 'joiner': '\n',
                                                  'dirs': []}
                   for t in TARGETS + RETIRED}
        print("  note     no install record, so only marked blocks and the kit's own files go")
    by_path: dict[str, list[dict]] = {}
    for key, record in records.items():
        by_path.setdefault(record.get('path', key), []).append(record)
    for name, pieces in by_path.items():
        uninstall_path(pathlib.Path(name), pieces, recorded, dry_run)
    uninstall_kit(home, env, state, dry_run)
    settings = state.get('settings')
    if settings:
        restore_setting(settings, dry_run)
    elif not recorded:
        print("  note     Claude Code's instructionFiles setting and ask rules were left as they are")
    if dry_run:
        return 0
    # Folders the install created, deepest first: one made for an early copy
    # may only empty out once a later one is gone.
    created = {pathlib.Path(folder) for record in records.values() for folder in record.get('dirs', [])}
    for group in ('owned', 'folders', 'hooks'):
        created |= {pathlib.Path(f) for record in state[group].values() for f in record.get('dirs', [])}
    created |= {pathlib.Path(folder) for folder in (settings or {}).get('dirs', [])}
    created.add(spath.parent)
    if spath.exists():
        spath.unlink()
    for folder in sorted(created, key=lambda path: len(path.parts), reverse=True):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    return 0


def uninstall_path(path: pathlib.Path, pieces: list[dict], recorded: bool, dry_run: bool) -> None:
    """Take every piece of the kit out of one file, then restore or remove the file."""
    current = read(path)
    if current is None:
        return
    rest = current
    touched = False
    # An earlier release's knowledge went in after the rules, so it comes out first.
    for record in sorted(pieces, key=lambda r: r.get('piece', 'rules') == 'rules'):
        piece = record.get('piece', 'rules')
        try:
            found = find(rest, piece)
        except Refused as error:
            print(f'  refused  {path} {error}')
            return
        if found is None:
            continue
        touched = True
        rest = '' if record['mode'] == 'file' else removed(rest, record.get('joiner', ''), piece)
    if not touched:
        return
    created = any(record.get('created') for record in pieces) if recorded else True
    gone = all(record['mode'] == 'file' for record in pieces) or (created and not rest.strip())
    print(f'  {"would remove" if dry_run else "removed"}  {path}' if gone
          else f'  {"would restore" if dry_run else "restored"}  {path}')
    if dry_run:
        return
    if gone:
        path.unlink()
    else:
        write(path, rest)


def uninstall_kit(home: pathlib.Path, env: Mapping[str, str], state: dict, dry_run: bool) -> None:
    owned_paths = {pathlib.Path(p) for p in state['owned']}
    # Without a record, the kit's files are found where the kit puts them, by their mark.
    owned_paths |= {home / GUARD, home / '.copilot' / 'hooks' / 'intelligence.json'}
    for folder in (home / '.claude' / 'agents', home / '.copilot' / 'agents', codex_home(home, env) / 'agents'):
        if folder.is_dir():
            owned_paths |= {p for p in folder.iterdir() if p.is_file()}
    for path in sorted(owned_paths):
        if path.is_file() and (is_kits(path, OWNED) or (path.name == 'intelligence.json'
                                                         and is_kits(path, GUARD_NAME))):
            print(f'  {"would remove" if dry_run else "removed"}  {path}')
            if not dry_run:
                path.unlink()
    folders = {pathlib.Path(p) for p in state['folders']}
    for _app, rel, _where in SKILL_ROOTS:
        root = home / rel
        if root.is_dir():
            folders |= {p for p in root.iterdir() if p.is_dir()}
    for folder in sorted(folders):
        if (folder / SKILL_MARK).is_file():
            print(f'  {"would remove" if dry_run else "removed"}  {folder}')
            if not dry_run:
                shutil.rmtree(folder)
    hook_files = {pathlib.Path(p): r for p, r in state['hooks'].items()}
    removers: dict[pathlib.Path, list[Callable[[dict], dict]]] = {}
    for registration in kit_registrations(home, False, env):
        hook_files.setdefault(registration.path, {'created': False})
        removers.setdefault(registration.path, []).append(registration.remove)
    for path, record in sorted(hook_files.items()):
        if not path.exists() or path not in removers:
            continue
        try:
            data = read_json(path)
        except Refused as error:
            print(f'  refused  {path} {error}')
            continue
        updated = data
        for remove in removers[path]:  # Claude Code's file holds two: the guard and the reminder
            updated = remove(updated)
        if updated == data:
            continue
        gone = bool(record.get('created')) and not updated
        verb = ('would remove' if dry_run else 'removed') if gone else ('would restore' if dry_run else 'restored')
        print(f'  {verb}  {path}')
        if dry_run:
            continue
        if gone:
            path.unlink()
        else:
            write(path, json.dumps(updated, indent=2) + '\n')


def restore_setting(settings: dict, dry_run: bool) -> None:
    path = pathlib.Path(settings['path'])
    try:
        data = read_settings(path)
    except Refused as error:
        print(f'  refused  {path} {error}')
        return
    configs = data.get('pluginConfigs')
    if isinstance(configs, dict):
        for plugin, prior in settings['prior'].items():
            if prior is None:
                configs.pop(plugin, None)
            else:
                configs[plugin] = prior
        if not configs and not settings['had_plugin_configs']:
            data.pop('pluginConfigs')
    permissions = data.get('permissions')
    if isinstance(permissions, dict) and isinstance(permissions.get('ask'), list):
        for rule in settings.get('asks', []):
            if rule in permissions['ask']:
                permissions['ask'].remove(rule)  # the one the kit added; a copy of your own stays
        if not permissions['ask'] and not settings.get('had_ask', True):
            del permissions['ask']
        if not permissions and not settings.get('had_permissions', True):
            del data['permissions']
    print(f'  {"would restore" if dry_run else "restored"}  Claude Code setting: {path}')
    if dry_run:
        return
    if settings['created'] and not data:
        if path.exists():
            path.unlink()
    else:
        write(path, json.dumps(data, indent=2) + '\n')


def main(argv: list[str] | None = None, env: Mapping[str, str] | None = None) -> int:
    env = os.environ if env is None else env
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('install', 'check', 'uninstall'):
        command = sub.add_parser(name)
        command.add_argument('--home', type=pathlib.Path, default=pathlib.Path.home(),
                             help='home folder to work in (default: yours)')
        if name != 'uninstall':
            command.add_argument('--home-file', type=pathlib.Path, required=True,
                                 help='the home file from a release, already checked against its pin')
            command.add_argument('--kit-file', type=pathlib.Path,
                                 help="the release's kit.json, already checked against its pin")
            command.add_argument('--cloud', action='store_true',
                                 help="a Claude cloud session: write only Claude Code's files")
        if name != 'check':
            command.add_argument('--dry-run', action='store_true', help='print the plan, change nothing')
    args = parser.parse_args(argv)
    if args.command == 'install':
        return install(args.home, args.home_file, args.cloud, env, args.dry_run, args.kit_file)
    if args.command == 'check':
        return check(args.home, args.home_file, args.cloud, env, args.kit_file)
    return uninstall(args.home, env, args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
