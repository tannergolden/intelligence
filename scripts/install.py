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
repository's `AGENTS.md` even beside a `CLAUDE.md`. Grok Build reads
`~/.claude` by default, so it gets no copy of its own. Cursor's User Rules
live in its settings, so they are pasted by hand.

They are copies, never links, because links fail silently in Claude's desktop
sessions and in Grok's sandbox. A file the kit owns outright holds nothing
else. In a file that also holds your own notes, the rules sit in a marked
block and your text stays.

SAFETY. Before changing a file, it records the setting's prior value and
whether it created the file. `uninstall` uses that record to put everything
back. It never overwrites a file it does not own. It runs on the Python 3.9
that macOS ships, with the standard library only, and makes no network
calls: whoever runs it has already downloaded the home file and checked
its SHA-256.

Run it:

    python3 install.py install --home-file intelligence.md
    python3 install.py check --home-file intelligence.md
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
import sys
import tempfile
from collections.abc import Mapping

REGION = re.compile(
    r'^<!-- INTELLIGENCE:BEGIN sha256:(?P<hash>[0-9a-f]{64}) -->[ \t]*\r?\n'
    r'(?P<inner>.*?)'
    r'^<!-- INTELLIGENCE:END -->[ \t]*(?:\r?\n|\Z)',
    re.M | re.S,
)

PLUGIN_IDS = ('cc-plugin-agents-md@builtin', 'agents-md@builtin')
READ_BOTH = 'claude-md-and-agents-md'
SETTINGS = '.claude/settings.json'
COPILOT_PREFIX = '---\napplyTo: "**"\n---\n\n'


@dataclasses.dataclass(frozen=True)
class Target:
    """One place an app reads its user-level instructions."""

    app: str
    rel: str  # under the home folder
    mode: str  # 'file': the kit owns the file; 'block': a marked block in a personal file
    where: str  # 'local', 'cloud' or 'both'
    prefix: str = ''  # what precedes the block in a file the kit owns


TARGETS = (
    Target('master copy', '.agents/AGENTS.md', 'block', 'local'),
    Target('Claude Code', '.claude/rules/intelligence.md', 'file', 'local'),
    Target('Claude Code', '.claude/CLAUDE.md', 'block', 'cloud'),
    Target('Codex', '.codex/AGENTS.md', 'block', 'local'),
    Target('Antigravity CLI', '.gemini/AGENTS.md', 'block', 'local'),
    Target('Copilot', '.copilot/instructions/intelligence.instructions.md', 'file', 'local',
           COPILOT_PREFIX),
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


def find(text: str) -> Found | None:
    matches = list(REGION.finditer(text))
    if len(matches) > 1:
        raise Refused('holds more than one INTELLIGENCE block; remove the extra by hand')
    if not matches:
        return None
    match = matches[0]
    inner = match.group('inner').replace('\r\n', '\n').strip('\n') + '\n'
    return Found(match.start(), match.end(), match.group('hash'), inner)


def read_home_file(path: pathlib.Path) -> tuple[str, str]:
    """The region to install and its hash, from a home file rendered by the hub."""
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as error:
        raise SystemExit(f'cannot read the home file {path}: {error}') from error
    found = find(text)
    if found is None or text[:found.start].strip() or text[found.end:].strip():
        raise SystemExit(f'{path} is not a home file: it must be exactly one INTELLIGENCE block')
    if found.edited:
        raise SystemExit(f'{path} was edited: its content does not match the hash in its marker')
    return text[found.start:found.end], found.marker


def resolve(target: Target, home: pathlib.Path, env: Mapping[str, str]) -> pathlib.Path:
    if target.rel == '.codex/AGENTS.md' and env.get('CODEX_HOME'):
        return pathlib.Path(env['CODEX_HOME']) / 'AGENTS.md'
    return home / target.rel


def targets_for(cloud: bool) -> list[Target]:
    return [t for t in TARGETS if t.where in ('both', 'cloud' if cloud else 'local')]


def read(path: pathlib.Path) -> str | None:
    if not path.exists():
        return None
    with open(path, encoding='utf-8', newline='') as handle:
        return handle.read()


def write(path: pathlib.Path, text: str) -> None:
    """Replace `path` in one step, keeping its permissions."""
    mode = path.stat().st_mode & 0o777 if path.exists() else None
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


def placed(target: Target, current: str | None, region: str) -> tuple[str, str]:
    """The file's new text with the block in place, and what was added before the block.

    The second value is the separator written ahead of an appended block, so
    an uninstall can take exactly that back out; it is empty when the block
    replaced an older one or the file is new.
    """
    if target.mode == 'file':
        if current is not None and find(current) is None:
            raise Refused("exists and is not the kit's; it is never overwritten")
        return target.prefix + region, ''
    if not current:
        return region, ''
    found = find(current)
    if found is not None:
        return current[:found.start] + region + current[found.end:], ''
    joiner = '\n' if current.endswith('\n') else '\n\n'
    return current + joiner + region, joiner


def removed(current: str, joiner: str) -> str:
    """The file's text with the kit's block, and the separator it added, taken out."""
    found = find(current)
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
    if not path.exists():
        return {'format': 1, 'files': {}, 'settings': None}
    return json.loads(path.read_text(encoding='utf-8'))


def save_state(path: pathlib.Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write(path, json.dumps(state, indent=2) + '\n')


def read_settings(path: pathlib.Path) -> dict:
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


def install(home: pathlib.Path, home_file: pathlib.Path, cloud: bool, env: Mapping[str, str],
            dry_run: bool = False) -> int:
    region, block_hash = read_home_file(home_file)
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
            print(f'  refused  {label} {error}')
            failures += 1
            continue
        changed = text != current
        print(f'  {"current" if not changed else "would write" if dry_run else "wrote"}  {label}')
        if dry_run:
            continue
        # Recorded before the write, and kept from the first install, so an
        # uninstall restores what was there before the kit ever ran.
        record = state['files'].setdefault(str(path), {
            'mode': target.mode, 'created': current is None, 'joiner': joiner,
            'dirs': [str(folder) for folder in missing_dirs(path)],
        })
        if joiner:
            record['joiner'] = joiner
        save_state(spath, state)
        if changed:
            for folder in missing_dirs(path):
                folder.mkdir()
            write(path, text)
    if not cloud:
        failures += install_setting(home, state, spath, dry_run)
    if not dry_run:
        state['hash'] = block_hash
        save_state(spath, state)
    print('  manual   Cursor: paste the home file into Settings > Rules > User Rules, '
          'and again whenever the block changes')
    for line in shadows(home, env):
        print(f'  warning  {line}')
    return 1 if failures else 0


def install_setting(home: pathlib.Path, state: dict, spath: pathlib.Path, dry_run: bool) -> int:
    path = home / SETTINGS
    label = f'Claude Code setting: {path}'
    try:
        data = read_settings(path)
        updated = apply_setting(data)
    except Refused as error:
        print(f'  refused  {label} {error}')
        return 1
    if updated == data:
        print(f'  current  {label}')
        return 0
    print(f'  {"would write" if dry_run else "wrote"}  {label}')
    if dry_run:
        return 0
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
        save_state(spath, state)
    for folder in missing_dirs(path):
        folder.mkdir()
    write(path, json.dumps(updated, indent=2) + '\n')
    return 0


def shadows(home: pathlib.Path, env: Mapping[str, str]) -> list[str]:
    found = []
    for rel, why in SHADOWS:
        path = (pathlib.Path(env['CODEX_HOME']) / 'AGENTS.override.md'
                if rel == '.codex/AGENTS.override.md' and env.get('CODEX_HOME') else home / rel)
        if path.exists():
            found.append(f'{path} exists: {why}')
    return found


def check(home: pathlib.Path, home_file: pathlib.Path, cloud: bool, env: Mapping[str, str]) -> int:
    region, block_hash = read_home_file(home_file)
    failures = 0
    for target in targets_for(cloud):
        path = resolve(target, home, env)
        status = target_status(target, read(path), region, block_hash)
        if status != 'current':
            failures += 1
        print(f'  {status:<8} {target.app}: {path}')
    if not cloud:
        path = home / SETTINGS
        try:
            data = read_settings(path)
            ok = all(reads_both(data, plugin) for plugin in PLUGIN_IDS)
        except Refused:
            ok = False
        failures += 0 if ok else 1
        print(f'  {"current" if ok else "missing":<8} Claude Code setting: {path}')
    for line in shadows(home, env):
        print(f'  warning  {line}')
    print('  manual   Cursor: check Settings > Rules > User Rules by hand')
    return 1 if failures else 0


def target_status(target: Target, current: str | None, region: str, block_hash: str) -> str:
    if current is None:
        return 'missing'
    try:
        found = find(current)
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


def uninstall(home: pathlib.Path, env: Mapping[str, str], dry_run: bool = False) -> int:
    spath = state_path(home, env)
    state = load_state(spath)
    records = state.get('files') or {}
    recorded = bool(records)
    if not recorded:
        # No record of an install: take out only what is unmistakably the kit's.
        records = {str(resolve(t, home, env)): {'mode': t.mode, 'created': False,
                                                  'joiner': '\n', 'dirs': []}
                   for t in TARGETS}
        print("  note     no install record, so only marked blocks and the kit's own files go")
    for name, record in records.items():
        path = pathlib.Path(name)
        current = read(path)
        if current is None:
            continue
        try:
            found = find(current)
        except Refused as error:
            print(f'  refused  {path} {error}')
            continue
        if found is None:
            continue
        rest = '' if record['mode'] == 'file' else removed(current, record.get('joiner', ''))
        created = record.get('created') if recorded else True
        gone = record['mode'] == 'file' or (created and not rest.strip())
        print(f'  {"would remove" if dry_run else "removed"}  {path}' if gone
              else f'  {"would restore" if dry_run else "restored"}  {path}')
        if dry_run:
            continue
        if gone:
            path.unlink()
        else:
            write(path, rest)
    settings = state.get('settings')
    if settings:
        restore_setting(settings, dry_run)
    elif not recorded:
        print("  note     Claude Code's instructionFiles setting was left as it is")
    if dry_run:
        return 0
    # Folders the install created, deepest first: one made for an early copy
    # may only empty out once a later one is gone.
    created = {pathlib.Path(folder) for record in records.values() for folder in record.get('dirs', [])}
    created |= {pathlib.Path(folder) for folder in (settings or {}).get('dirs', [])}
    created.add(spath.parent)
    if spath.exists():
        spath.unlink()
    for folder in sorted(created, key=lambda path: len(path.parts), reverse=True):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    return 0


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
    print(f'  {"would restore" if dry_run else "restored"}  Claude Code setting: {path}')
    if dry_run:
        return
    if settings['created'] and not data:
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
            command.add_argument('--cloud', action='store_true',
                                 help='a Claude cloud session: write ~/.claude/CLAUDE.md only')
        if name != 'check':
            command.add_argument('--dry-run', action='store_true', help='print the plan, change nothing')
    args = parser.parse_args(argv)
    if args.command == 'install':
        return install(args.home, args.home_file, args.cloud, env, args.dry_run)
    if args.command == 'check':
        return check(args.home, args.home_file, args.cloud, env)
    return uninstall(args.home, env, args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
