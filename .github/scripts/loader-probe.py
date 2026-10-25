#!/usr/bin/env python3
"""Phase 0 loader probe: proves which AI coding app reads which instruction file.

WHY THIS EXISTS. The intelligence plan rests on claims about where each app
looks for instructions, gathered from documentation and source code. The
claims are:

- Claude Code reads ~/.claude/rules/.
- Codex reads ~/.codex/AGENTS.md.
- Antigravity CLI reads ~/.gemini/AGENTS.md.
- Copilot reads ~/.copilot/instructions/.
- Grok Build reads Claude's folder.
- Every one of them reads a repository's root AGENTS.md.
- None of them reads ~/.agents/AGENTS.md.

Apps change where they look without notice, so this probe proves the claims
on the machine that will run them, before anything is built on top.

HOW IT WORKS. The probe:

1. Writes temporary instruction files, each carrying a random code.
2. Asks every installed app, headless, which codes its instructions define.
3. Restores every file it touched.

A random twelve-character code cannot be guessed, so an app that reports one
has loaded the file that holds it.

    PROBE_REPO    a scratch git repository's root AGENTS.md
    PROBE_HOME    the home copy in each app's own folder
    PROBE_MASTER  ~/.agents/AGENTS.md, which no app should read

Negative controls check two documented exceptions:

- Claude Code skips AGENTS.md beside a CLAUDE.md or a CLAUDE.local.md
  unless its instructionFiles setting says to read both.
- Grok Build skips an untrusted folder's AGENTS.md in headless runs.

Some surfaces have no headless mode, such as Copilot in VS Code and the
Cursor editor. `--keep` writes the same files and fixtures, prints the
question to ask by hand, and leaves everything in place until `--cleanup`.

THE SKILL CANARY. With `--skills`, the probe also plants one skill under the
same name in three skills folders, each copy with its own code: the shared
`~/.agents/skills/`, Claude Code's `~/.claude/skills/` and Antigravity's
`~/.gemini/antigravity-cli/skills/`. The home kit installs its skills as
copies in all three, which is safe only if every app sees exactly one copy.
Each app is asked which copies it can see; one copy passes, none or two
fail. VS Code, which reads both `~/.claude/skills` and `~/.agents/skills`,
is checked by hand with `--keep --skills`.

SAFETY. The probe never overwrites a file it did not create. It records
every change in a manifest before making it, and restores the original
bytes when it finishes, fails, or is interrupted. A run that dies anyway
leaves the manifest behind; `--cleanup` replays it. The probe makes one
model call per check, twelve in a full run.

Run it:

    python3 .github/scripts/loader-probe.py --dry-run     # show the plan, change nothing
    python3 .github/scripts/loader-probe.py               # every installed app
    python3 .github/scripts/loader-probe.py --apps claude,grok
    python3 .github/scripts/loader-probe.py --skills      # add the skill canary
    python3 .github/scripts/loader-probe.py --keep        # set up a check by hand
    python3 .github/scripts/loader-probe.py --cleanup     # undo --keep, or a crash
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import os
import pathlib
import platform
import secrets
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
from collections.abc import Sequence

BEGIN = '<!-- INTELLIGENCE-PROBE:BEGIN -->'
END = '<!-- INTELLIGENCE-PROBE:END -->'

NAMES = ('PROBE_REPO', 'PROBE_HOME', 'PROBE_MASTER')

QUESTION = (
    'Answer only from the instructions you were given before this message. '
    'Do not use any tools, read any files or run any commands. '
    'Your instructions may define values named PROBE_REPO, PROBE_HOME and '
    'PROBE_MASTER. For each one they define, reply with one line NAME=VALUE. '
    'If they define none, reply NONE. Reply with nothing else.'
)

# Claude Code reads AGENTS.md beside a CLAUDE.md or CLAUDE.local.md only with
# this setting, under either plugin ID (the older one before v2.1.285).
CLAUDE_PLUGIN_IDS = ('cc-plugin-agents-md@builtin', 'agents-md@builtin')
READ_BOTH = 'claude-md-and-agents-md'
CLAUDE_READ_BOTH_SETTINGS = {
    'pluginConfigs': {
        plugin: {'options': {'instructionFiles': READ_BOTH}} for plugin in CLAUDE_PLUGIN_IDS
    }
}

MASTER = '.agents/AGENTS.md'

# The skill canary: one skill name, one copy per skills folder, a code each.
SKILL = 'intelligence-probe-canary'
SKILL_ROOTS = {
    'PROBE_SKILL_SHARED': '.agents/skills',
    'PROBE_SKILL_CLAUDE': '.claude/skills',
    'PROBE_SKILL_ANTIGRAVITY': '.gemini/antigravity-cli/skills',
}
SKILL_NAMES = tuple(SKILL_ROOTS)
SKILL_QUESTION = (
    'Answer only from what you were given before this message. '
    'Do not use any tools, read any files or run any commands. '
    f'You may have skills named {SKILL}. For each copy whose description you can see, '
    'reply with one line NAME=VALUE for the value that description gives. '
    'If you see none, reply NONE. Reply with nothing else.'
)
# The copy each app should see: the one in its own folder, and only that one.
# Grok Build and Cursor read both the shared folder and Claude's; either copy
# passes, as long as they see one.
SKILL_SEES = {
    'claude': 'PROBE_SKILL_CLAUDE',
    'codex': 'PROBE_SKILL_SHARED',
    'copilot': 'PROBE_SKILL_SHARED',
    'antigravity': 'PROBE_SKILL_ANTIGRAVITY',
}

# Each fixture is a scratch git repository whose AGENTS.md carries PROBE_REPO,
# beside the file named here, which defines nothing.
FIXTURES: dict[str, str | None] = {
    'plain': None,
    'claude-md': 'CLAUDE.md',
    'claude-local': 'CLAUDE.local.md',
}


@dataclasses.dataclass(frozen=True)
class App:
    """One AI coding app: how to call it and where its home copy goes."""

    key: str
    name: str
    argv: tuple[str, ...]
    home: str | None = None  # path under HOME; None when the probe writes nothing
    home_mode: str = 'file'  # "file": a file the probe owns; "block": a marked block
    reads_home_of: str | None = None  # the app whose home copy this one reads
    env: dict[str, str] = dataclasses.field(default_factory=dict)


APPS: dict[str, App] = {
    'claude': App(
        key='claude',
        name='Claude Code',
        argv=('claude', '-p', '{prompt}', '--disallowedTools',
              'Bash,Read,Grep,Glob,Edit,Write,WebFetch,WebSearch'),
        home='.claude/rules/intelligence-probe.md',
    ),
    'codex': App(
        key='codex',
        name='Codex',
        argv=('codex', 'exec', '--sandbox', 'read-only', '{prompt}'),
        home='.codex/AGENTS.md',
        home_mode='block',
    ),
    'antigravity': App(
        key='antigravity',
        name='Antigravity CLI',
        argv=('agy', '-p', '{prompt}'),
        home='.gemini/AGENTS.md',
        home_mode='block',
    ),
    'copilot': App(
        key='copilot',
        name='Copilot CLI',
        argv=('copilot', '-p', '{prompt}', '--trust-folder'),
        home='.copilot/instructions/intelligence-probe.instructions.md',
    ),
    'grok': App(
        key='grok',
        name='Grok Build',
        argv=('grok', '-p', '{prompt}'),
        reads_home_of='claude',
        env={'GROK_FOLDER_TRUST': '0'},
    ),
    'cursor': App(
        key='cursor',
        name='Cursor CLI',
        argv=('cursor-agent', '-p', '{prompt}'),
    ),
}


@dataclasses.dataclass(frozen=True)
class Check:
    """One model call and what it should report."""

    app: str
    label: str
    fixture: str  # a key of FIXTURES: which scratch repository to run in
    expect: dict[str, bool | None]  # None means "not judged"
    extra_args: tuple[str, ...] = ()
    drop_env: tuple[str, ...] = ()
    question: str = QUESTION
    names: tuple[str, ...] = NAMES
    exactly_one: bool = False  # passes only if exactly one of the names is seen


def plan_checks(apps: Sequence[str], settings_path: str,
                claude_reads_both: bool = False, skills: bool = False) -> list[Check]:
    """Every check for the chosen apps, negative controls included."""
    checks: list[Check] = []
    if skills:
        for key in apps:
            sees = SKILL_SEES.get(key)
            expect: dict[str, bool | None] = (
                {name: name == sees for name in SKILL_NAMES} if sees
                else {**{name: None for name in SKILL_NAMES}, 'PROBE_SKILL_ANTIGRAVITY': False})
            checks.append(Check(key, f'{APPS[key].name} skill copies', 'plain', expect,
                                question=SKILL_QUESTION, names=SKILL_NAMES, exactly_one=True))
    for key in apps:
        app = APPS[key]
        reads_home = bool(app.home or app.reads_home_of)
        checks.append(Check(key, app.name, 'plain', {
            'PROBE_REPO': True,
            'PROBE_HOME': True if reads_home else None,
            'PROBE_MASTER': False,
        }))
        if key == 'claude':
            for fixture in ('claude-md', 'claude-local'):
                # Your own settings may already read both files; then the
                # control is expected to see AGENTS.md too.
                label = f'Claude Code beside a {FIXTURES[fixture]}'
                mine = ' (your settings already read both)' if claude_reads_both else ''
                checks.append(Check(key, label + mine, fixture, {
                    'PROBE_REPO': claude_reads_both, 'PROBE_HOME': True, 'PROBE_MASTER': False,
                }))
                checks.append(Check(
                    key, label + ', reading both', fixture,
                    {'PROBE_REPO': True, 'PROBE_HOME': True, 'PROBE_MASTER': False},
                    extra_args=('--settings', settings_path),
                ))
        if key == 'grok':
            checks.append(Check(
                key, 'Grok Build in an untrusted folder', 'plain',
                {'PROBE_REPO': False, 'PROBE_HOME': True, 'PROBE_MASTER': False},
                drop_env=('GROK_FOLDER_TRUST',),
            ))
    return checks


def probe_block(name: str, code: str) -> str:
    """The marked text that defines one probe value."""
    return (
        f'{BEGIN}\n'
        '## Loader probe\n\n'
        'This is a temporary test written by the tannergolden/intelligence '
        f'phase 0 probe. The value of {name} is {code}.\n'
        f'{END}\n'
    )


def skill_text(name: str, code: str) -> str:
    """One copy of the canary skill, whose description carries its code."""
    return (
        '---\n'
        f'name: {SKILL}\n'
        'description: A temporary test written by the tannergolden/intelligence loader probe. '
        f'The value of {name} is {code}. Use when asked about {SKILL}.\n'
        '---\n\n'
        f'The value of {name} is {code}.\n'
    )


def home_text(app_key: str, code: str) -> str:
    """What the probe writes into one app's home location."""
    block = probe_block('PROBE_HOME', code)
    if app_key == 'copilot':
        return '---\napplyTo: "**"\n---\n\n' + block
    return block


def claude_reads_both(home: pathlib.Path) -> bool:
    """Whether ~/.claude/settings.json already makes Claude read both files."""
    try:
        value: object = json.loads((home / '.claude' / 'settings.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return False
    for plugin in CLAUDE_PLUGIN_IDS:
        found = value
        for key in ('pluginConfigs', plugin, 'options', 'instructionFiles'):
            found = found.get(key) if isinstance(found, dict) else None
        if found == READ_BOTH:
            return True
    return False


SCRATCH_PREFIX = 'intelligence-probe-'


class Manifest:
    """Every change the probe makes, written down before it is made.

    The manifest lives in the state folder as JSON, so a run that dies halfway
    can be undone by a later `--cleanup`, which needs nothing but this file.
    """

    def __init__(self, state: pathlib.Path) -> None:
        self.state = state
        self.path = state / 'manifest.json'
        self.entries: list[dict[str, object]] = []

    def exists(self) -> bool:
        return self.path.exists()

    def load(self) -> None:
        self.entries = json.loads(self.path.read_text(encoding='utf-8'))['entries']

    def save(self) -> None:
        self.state.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix('.tmp')
        payload = {'format': 1, 'entries': self.entries}
        tmp.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
        os.replace(tmp, self.path)

    def remember(self, path: pathlib.Path, backup: pathlib.Path | None,
                 created_dirs: Sequence[pathlib.Path]) -> None:
        self.entries.append({
            'path': str(path),
            'backup': str(backup) if backup else None,
            'created_dirs': [str(folder) for folder in created_dirs],
        })
        self.save()

    def remember_tree(self, path: pathlib.Path) -> None:
        """A scratch folder of the probe's own, removed whole on restore."""
        self.entries.append({'tree': str(path)})
        self.save()

    def restore(self) -> list[str]:
        """Undo every recorded change, newest first, and say what it did."""
        done: list[str] = []
        for entry in reversed(self.entries):
            if entry.get('tree'):
                tree = pathlib.Path(str(entry['tree']))
                # Only ever a folder the probe named, whatever the manifest says.
                if tree.name.startswith(SCRATCH_PREFIX) and tree.is_dir():
                    shutil.rmtree(tree, ignore_errors=True)
                    done.append(f'removed scratch folder {tree}')
                continue
            path = pathlib.Path(str(entry['path']))
            backup = entry.get('backup')
            if backup:
                shutil.copy2(str(backup), path)
                done.append(f'restored {path}')
            elif path.exists():
                path.unlink()
                done.append(f'removed {path}')
            for folder in reversed(list(entry.get('created_dirs') or [])):
                folder_path = pathlib.Path(str(folder))
                if folder_path.is_dir() and not any(folder_path.iterdir()):
                    folder_path.rmdir()
                    done.append(f'removed folder {folder_path}')
        self.entries = []
        shutil.rmtree(self.state / 'backups', ignore_errors=True)
        if self.path.exists():
            self.path.unlink()
        return done


def missing_parents(path: pathlib.Path) -> list[pathlib.Path]:
    """The folders above `path` that do not exist yet, outermost first."""
    return [parent for parent in reversed(path.parents) if not parent.exists()]


def install(manifest: Manifest, path: pathlib.Path, text: str, mode: str) -> None:
    """Write probe text to `path`, recording how to undo it first.

    In "file" mode the probe owns the whole file, so the path must be free.
    In "block" mode the text is appended to a personal file between markers,
    and the original bytes are kept for an exact restore.
    """
    if path.exists() and BEGIN in path.read_text(encoding='utf-8', errors='replace'):
        raise SystemExit(f'{path} still holds probe text from an earlier run; '
                         'run with --cleanup first.')
    if mode == 'file' and path.exists():
        raise SystemExit(f"{path} already exists and is not the probe's; "
                         "refusing to overwrite it.")
    created = missing_parents(path)
    backup: pathlib.Path | None = None
    if path.exists():
        backups = manifest.state / 'backups'
        backups.mkdir(parents=True, exist_ok=True)
        backup = backups / f'{len(manifest.entries):02d}-{path.name}'
        shutil.copy2(path, backup)
    manifest.remember(path, backup, created)
    for folder in created:
        folder.mkdir()
    if mode == 'block' and path.exists():
        current = path.read_bytes()
        joiner = b'\n' if current and not current.endswith(b'\n') else b''
        path.write_bytes(current + joiner + b'\n' + text.encode('utf-8'))
    else:
        path.write_bytes(text.encode('utf-8'))


def make_fixture(root: pathlib.Path, name: str, code: str) -> pathlib.Path:
    """One of the FIXTURES, as a git repository in its own folder under `root`."""
    repo = root / name
    repo.mkdir()
    subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
    (repo / 'AGENTS.md').write_text(
        '# Probe fixture\n\n' + probe_block('PROBE_REPO', code), encoding='utf-8')
    beside = FIXTURES[name]
    if beside:
        (repo / beside).write_text(
            '# Notes\n\nNothing in this file defines a probe value.\n', encoding='utf-8')
    return repo


def build_argv(app: App, check: Check, overrides: dict[str, str]) -> list[str]:
    """The command for one check, with the question in place of {prompt}."""
    template = shlex.split(overrides[app.key]) if app.key in overrides else list(app.argv)
    return [check.question if part == '{prompt}' else part for part in template] + list(check.extra_args)


def observe(output: str, codes: dict[str, str], names: Sequence[str] = NAMES) -> dict[str, bool]:
    """Which probe values an app's output contains, in any letter case."""
    output = output.lower()
    return {name: codes[name].lower() in output for name in names}


def judge(expect: dict[str, bool | None], seen: dict[str, bool], exactly_one: bool = False) -> bool:
    """True when every judged value matches what the check expects."""
    if exactly_one and sum(seen.values()) != 1:
        return False
    return all(seen[name] == want for name, want in expect.items() if want is not None)


def as_text(value: object) -> str:
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='replace')
    return value if isinstance(value, str) else ''


def run_check(app: App, check: Check, cwd: pathlib.Path, codes: dict[str, str],
              overrides: dict[str, str], timeout: int) -> dict[str, object]:
    """Ask one app the question and judge its answer."""
    env = dict(os.environ)
    env.update(app.env)
    for name in check.drop_env:
        env.pop(name, None)
    argv = build_argv(app, check, overrides)
    started = datetime.datetime.now(datetime.timezone.utc)
    exit_code: int | None
    try:
        done = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                              text=True, timeout=timeout, check=False)
        output, exit_code = done.stdout + '\n' + done.stderr, done.returncode
    except subprocess.TimeoutExpired as error:
        output, exit_code = as_text(error.stdout) + '\n' + as_text(error.stderr), None
    except OSError as error:
        output, exit_code = str(error), 127
    seconds = (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds()
    seen = observe(output, codes, check.names)
    if exit_code is None:
        status = 'timeout'
    elif exit_code != 0 and not any(seen.values()):
        status = 'error'
    else:
        status = 'pass' if judge(check.expect, seen, check.exactly_one) else 'fail'
    return {
        'app': app.key, 'check': check.label, 'status': status,
        'exit_code': exit_code, 'seconds': round(seconds, 1),
        'expected': check.expect, 'observed': seen, 'names': list(check.names),
        'command': ['{question}' if part == check.question else part for part in argv],
        'output': output.strip()[:2000],
    }


def cell(want: bool | None, seen: bool) -> str:
    word = 'read' if seen else 'not read'
    if want is None:
        return f'{word} (not judged)'
    return word if want == seen else f"{word}, expected {'read' if want else 'not read'}"


def matrix(results: Sequence[dict[str, object]]) -> str:
    """The results as Markdown tables, ready to paste into an issue."""
    tables = []
    for names in (NAMES, SKILL_NAMES):
        rows = [row for row in results if tuple(row.get('names') or NAMES) == names]
        if not rows:
            continue
        lines = ['| Check | ' + ' | '.join(names) + ' | Result |',
                 '| --- ' * (len(names) + 2) + '|']
        for row in rows:
            if row['status'] in ('skipped', 'timeout', 'error'):
                lines.append(f"| {row['check']} | " + '- | ' * len(names) + f"{row['status']} |")
                continue
            expect = row['expected'] if isinstance(row['expected'], dict) else {}
            seen = row['observed'] if isinstance(row['observed'], dict) else {}
            cells = ' | '.join(cell(expect.get(name), bool(seen.get(name))) for name in names)
            lines.append(f"| {row['check']} | {cells} | {row['status']} |")
        tables.append('\n'.join(lines))
    return '\n\n'.join(tables)


def default_state() -> pathlib.Path:
    base = os.environ.get('XDG_CACHE_HOME') or str(pathlib.Path.home() / '.cache')
    return pathlib.Path(base) / 'intelligence-probe'


def parse_overrides(values: Sequence[str]) -> dict[str, str]:
    overrides: dict[str, str] = {}
    for value in values:
        key, sep, command = value.partition('=')
        if not sep or key not in APPS or '{prompt}' not in command:
            raise SystemExit(f"--command takes APP='argv with {{prompt}}', got {value!r}")
        overrides[key] = command
    return overrides


def planned_writes(apps: Sequence[str], home: pathlib.Path, codes: dict[str, str],
                   skills: bool = False) -> list[tuple[pathlib.Path, str, str]]:
    """Every file the probe writes for these apps: path, text and mode."""
    writes = [(home / MASTER, probe_block('PROBE_MASTER', codes['PROBE_MASTER']), 'block')]
    owners = set(apps) | {APPS[key].reads_home_of for key in apps if APPS[key].reads_home_of}
    for key in sorted(owner for owner in owners if owner):
        app = APPS[key]
        if app.home:
            writes.append((home / app.home, home_text(key, codes['PROBE_HOME']), app.home_mode))
    if skills:
        for name, root in SKILL_ROOTS.items():
            writes.append((home / root / SKILL / 'SKILL.md', skill_text(name, codes[name]), 'file'))
    return writes


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--apps', help='comma-separated, from: ' + ','.join(APPS))
    parser.add_argument('--dry-run', action='store_true',
                        help='print the plan and change nothing')
    parser.add_argument('--cleanup', action='store_true',
                        help='restore the files an interrupted run left behind')
    parser.add_argument('--home', type=pathlib.Path, default=pathlib.Path.home(),
                        help='home folder to probe (default: yours)')
    parser.add_argument('--state', type=pathlib.Path, default=None,
                        help='where the manifest and results go')
    parser.add_argument('--timeout', type=int, default=240,
                        help='seconds allowed per model call (default 240)')
    parser.add_argument('--command', action='append', default=[], metavar='APP=ARGV',
                        help="replace an app's command; it must contain {prompt}")
    parser.add_argument('--keep', action='store_true',
                        help='write the files and fixtures for a check by hand, '
                             'and leave them until --cleanup')
    parser.add_argument('--skills', action='store_true',
                        help='add the skill canary: one more model call per app')
    args = parser.parse_args(argv)

    manifest = Manifest(args.state or default_state())

    if args.cleanup:
        if not manifest.exists():
            print('Nothing to clean up: no manifest from an earlier run.')
            return 0
        manifest.load()
        for line in manifest.restore():
            print(line)
        return 0

    if manifest.exists():
        print(f'An earlier run did not finish ({manifest.path}). Run with --cleanup first.',
              file=sys.stderr)
        return 2

    overrides = parse_overrides(args.command)
    wanted = [key.strip() for key in args.apps.split(',') if key.strip()] if args.apps else list(APPS)
    unknown = [key for key in wanted if key not in APPS]
    if unknown:
        parser.error('unknown app: ' + ', '.join(unknown))

    def binary(key: str) -> str:
        return shlex.split(overrides[key])[0] if key in overrides else APPS[key].argv[0]

    installed = [key for key in wanted if shutil.which(binary(key))]
    skipped = [key for key in wanted if key not in installed]
    if not installed and not args.keep:
        print('None of these apps is installed: '
              + ', '.join(f'{APPS[key].name} (`{binary(key)}`)' for key in skipped),
              file=sys.stderr)
        return 1

    codes = {name: secrets.token_hex(6) for name in NAMES + SKILL_NAMES}
    # A check by hand needs no command line, so it writes for every app named.
    writes = planned_writes(wanted if args.keep else installed, args.home, codes, args.skills)
    both = claude_reads_both(args.home)

    if args.dry_run:
        checks = plan_checks(installed, '<scratch>/claude-read-both.json', both, args.skills)
        print('Would write, and leave in place until --cleanup:' if args.keep
              else 'Would write, then restore afterwards:')
        for path, _, mode in writes:
            print(f'  {mode:<5}  {path}')
        if args.keep:
            print('Would make fixtures: ' + ', '.join(FIXTURES))
            return 0
        print('Would run, each in a scratch git repository:')
        for check in checks:
            command = build_argv(APPS[check.app], check, overrides)
            shown = ' '.join("'{question}'" if part == check.question else shlex.quote(part)
                             for part in command)
            print(f'  {check.label}: {shown}')
        for key in skipped:
            print(f'  {APPS[key].name}: skipped, `{binary(key)}` is not installed')
        return 0

    def on_stop(signum: int, frame: object) -> None:
        raise SystemExit(128 + signum)

    # Ctrl-C raises KeyboardInterrupt by itself; these two would otherwise
    # end the run without its restore.
    stops = [getattr(signal, name) for name in ('SIGTERM', 'SIGHUP') if hasattr(signal, name)]
    previous = {stop: signal.signal(stop, on_stop) for stop in stops}

    results: list[dict[str, object]] = []
    scratch = pathlib.Path(tempfile.mkdtemp(prefix=SCRATCH_PREFIX))
    manifest.remember_tree(scratch)
    settings_path = scratch / 'claude-read-both.json'
    checks = plan_checks(installed, str(settings_path), both, args.skills)
    kept = False
    try:
        for path, text, mode in writes:
            install(manifest, path, text, mode)
        settings_path.write_text(json.dumps(CLAUDE_READ_BOTH_SETTINGS), encoding='utf-8')
        fixtures = {name: make_fixture(scratch, name, codes['PROBE_REPO']) for name in FIXTURES}
        if args.keep:
            explain_keep(writes, fixtures, settings_path, codes, args.skills)
            kept = True
            return 0
        for check in checks:
            print(f'Probing {check.label} ...', flush=True)
            results.append(run_check(APPS[check.app], check, fixtures[check.fixture],
                                     codes, overrides, args.timeout))
    finally:
        if not kept:
            for line in manifest.restore():
                print(f'  {line}')
        for stop, handler in previous.items():
            signal.signal(stop, handler)

    for key in skipped:
        results.append({'app': key, 'check': APPS[key].name, 'status': 'skipped'})

    when = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    report = {
        'format': 1,
        'when': when,
        'host': platform.node(),
        'system': f'{platform.system()} {platform.release()}',
        'python': platform.python_version(),
        'versions': {key: first_line([binary(key), '--version']) for key in installed},
        'results': results,
    }
    manifest.state.mkdir(parents=True, exist_ok=True)
    out = manifest.state / f"results-{when.replace(':', '')}.json"
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print()
    print(matrix(results))
    print()
    print(f'Full results: {out}')
    judged = [row for row in results if row['status'] != 'skipped']
    return 0 if judged and all(row['status'] == 'pass' for row in judged) else 1


def explain_keep(writes: Sequence[tuple[pathlib.Path, str, str]],
                 fixtures: dict[str, pathlib.Path], settings_path: pathlib.Path,
                 codes: dict[str, str], skills: bool = False) -> None:
    """How to run the checks by hand against what --keep left in place."""
    print('Left in place until you run --cleanup:')
    for path, _, mode in writes:
        print(f'  {mode:<5}  {path}')
    print()
    print('Fixtures, each a git repository:')
    for name, path in fixtures.items():
        print(f'  {name:<12}  {path}')
    print()
    print('Open each app in the plain fixture, start a new session, and send this:')
    print()
    print('  ' + QUESTION)
    print()
    print(f"A correct answer names PROBE_REPO={codes['PROBE_REPO']} and "
          f"PROBE_HOME={codes['PROBE_HOME']}, and never PROBE_MASTER={codes['PROBE_MASTER']}.")
    print('Cursor has no home copy: paste the PROBE_HOME line above into its User Rules '
          'first, and remove it afterwards.')
    print('Claude Code skips AGENTS.md in the claude-md and claude-local fixtures, unless')
    print(f'it starts with `--settings {settings_path}`, which reads both.')
    if skills:
        print()
        print('For the skill canary, start another new session and send this:')
        print()
        print('  ' + SKILL_QUESTION)
        print()
        print('A correct answer names exactly one of '
              + ', '.join(f'{name}={codes[name]}' for name in SKILL_NAMES) + '.')
    print()
    print('When you are done: python3 .github/scripts/loader-probe.py --cleanup')


def first_line(argv: Sequence[str]) -> str:
    """The first line an app prints for --version, or "unknown"."""
    try:
        done = subprocess.run(list(argv), capture_output=True, text=True, timeout=30,
                              check=False)
    except (OSError, subprocess.SubprocessError):
        return 'unknown'
    text = (done.stdout or done.stderr).strip()
    return text.splitlines()[0] if text else 'unknown'


if __name__ == '__main__':
    sys.exit(main())
