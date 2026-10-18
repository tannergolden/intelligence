#!/usr/bin/env python3
"""Render the universal rules from the law into every copy this hub publishes.

WHY THIS EXISTS. The rules live in `law/`: one JSON file per rule ID, and
`law/block.json` for the order, the precedence text and the budget. Every
copy an agent reads is rendered from there and never written by hand:

- the managed block in this repository's own `AGENTS.md`;
- the home file, `home/intelligence.md`, which the home kit copies into
  each app's folder;
- the kit, `home/kit.json`, which carries the guard hook, the skills, the
  subagents and the knowledge facts, rendered by `kit.py`;
- `home/SHA256SUMS`, the hashes a consumer pins.

A copy that drifts from the law is a rule nobody wrote, so `--check` fails
CI until `--write` has brought every copy back in line. It also holds the
law itself to the rules of the plan:

- IDs are DOMAIN-NNN, unique, never retired;
- every rule is one ASCII sentence;
- Invariants reach every repository and name an enforcer;
- the block fits its cap.

The block is marked with a hash of its own text, so a release that leaves it
unchanged touches no repository, and a hand edit inside the markers is
caught wherever it lands.

Run it:

    python3 scripts/render.py              # print the block
    python3 scripts/render.py --write      # rewrite every copy from the law
    python3 scripts/render.py --check      # fail on a broken law or a stale copy
    python3 scripts/render.py --pins v0.1.0  # the hashes to pin for a release
    python3 scripts/render.py --setup v0.1.0  # the cloud setup script, pinned
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kit  # kit.py sits beside this file, wherever it is run from

ROOT = pathlib.Path(__file__).resolve().parents[1]

BEGIN = '<!-- INTELLIGENCE:BEGIN sha256:{} -->'
END = '<!-- INTELLIGENCE:END -->'
REGION = re.compile(
    r'^<!-- INTELLIGENCE:BEGIN sha256:(?P<hash>[0-9a-f]{64}) -->[ \t]*\r?\n'
    r'(?P<inner>.*?)'
    r'^<!-- INTELLIGENCE:END -->[ \t]*(?:\r?\n|\Z)',
    re.M | re.S,
)

ID = re.compile(r'^[A-Z]{2,5}-\d{3}$')
KINDS = ('invariant', 'default')
REACHES = ('every', 'owner')
MAX_RULE = 300

HOME_FILE = 'home/intelligence.md'
SUMS_FILE = 'home/SHA256SUMS'
INSTALLER = 'scripts/install.py'
KIT_FILE = kit.KIT_FILE
AGENTS_FILE = 'AGENTS.md'
SETUP_FILE = 'setup/claude-cloud-setup.sh'


@dataclasses.dataclass(frozen=True)
class Rule:
    id: str
    kind: str
    reach: str
    text: str
    why: str
    enforced_by: tuple[str, ...]
    to_add: tuple[str, ...]
    note: str = ''  # the file's "//" line, which the folder log shows

    @property
    def expected_note(self) -> str:
        kind = 'an Invariant' if self.kind == 'invariant' else 'a Default'
        reach = 'every repository' if self.reach == 'every' else "the owner's repositories"
        return f'{self.id}: {kind} for {reach}.'


@dataclasses.dataclass(frozen=True)
class Section:
    title: str
    kind: str
    reach: str
    rules: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class Law:
    heading: str
    precedence: tuple[str, ...]
    sections: tuple[Section, ...]
    target: int
    cap: int
    retired: dict[str, str]
    rules: dict[str, Rule]


class LawError(Exception):
    """The law cannot be read at all."""


def load_law(root: pathlib.Path) -> Law:
    """Read `law/block.json` and every file in `law/rules/`."""
    try:
        block = json.loads((root / 'law' / 'block.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise LawError(f'law/block.json: {error}') from error
    rules: dict[str, Rule] = {}
    for path in sorted((root / 'law' / 'rules').glob('*.json')):
        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            rule = Rule(
                id=data['id'], kind=data['kind'], reach=data['reach'], text=data['text'],
                why=data['why'], enforced_by=tuple(data.get('enforced_by', ())),
                to_add=tuple(data.get('to_add', ())), note=data.get('//', ''),
            )
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise LawError(f'{path.relative_to(root)}: {error}') from error
        if path.stem != rule.id:
            raise LawError(f'{path.relative_to(root)}: holds {rule.id}; a rule file is named for its ID')
        rules[rule.id] = rule
    try:
        return Law(
            heading=block['heading'],
            precedence=tuple(block['precedence']),
            sections=tuple(Section(s['title'], s['kind'], s['reach'], tuple(s['rules']))
                           for s in block['sections']),
            target=int(block['budget']['target']),
            cap=int(block['budget']['cap']),
            retired=dict(block.get('retired', {})),
            rules=rules,
        )
    except (KeyError, TypeError, ValueError) as error:
        raise LawError(f'law/block.json: missing or malformed {error}') from error


def plain(text: str) -> bool:
    """Printable ASCII only: no hidden, bidirectional or look-alike characters."""
    return all(' ' <= char <= '~' for char in text)


def problems(law: Law) -> list[str]:
    """Every way the law breaks the plan's rules, as sentences."""
    found: list[str] = []
    for rule in law.rules.values():
        where = f'law/rules/{rule.id}.json'
        if not ID.match(rule.id):
            found.append(f'{where}: the ID is not DOMAIN-NNN')
        if rule.id in law.retired:
            found.append(f'{where}: {rule.id} is retired and is never reused')
        if rule.kind not in KINDS:
            found.append(f'{where}: kind must be one of {", ".join(KINDS)}')
        if rule.reach not in REACHES:
            found.append(f'{where}: reach must be one of {", ".join(REACHES)}')
        if rule.kind == 'invariant' and rule.reach != 'every':
            found.append(f'{where}: an Invariant holds in every repository, so its reach is every')
        if rule.kind == 'invariant' and not (rule.enforced_by or rule.to_add):
            found.append(f'{where}: an Invariant names its enforcer, today or to add')
        if not plain(rule.text):
            found.append(f'{where}: the text must be printable ASCII on one line')
        if not rule.text.endswith('.'):
            found.append(f'{where}: the text is one sentence ending in a period')
        if len(rule.text) > MAX_RULE:
            found.append(f'{where}: the text is {len(rule.text)} characters (limit {MAX_RULE})')
        if not rule.why.strip():
            found.append(f'{where}: say why the rule exists')
        if rule.kind in KINDS and rule.reach in REACHES and rule.note != rule.expected_note:
            found.append(f'{where}: its "//" line should read "{rule.expected_note}"')
    listed: list[str] = []
    for section in law.sections:
        for rid in section.rules:
            listed.append(rid)
            rule = law.rules.get(rid)
            if rule is None:
                found.append(f'law/block.json: "{section.title}" lists {rid}, which has no rule file')
            elif (rule.kind, rule.reach) != (section.kind, section.reach):
                found.append(f'law/block.json: {rid} is a {rule.kind} for {rule.reach}, '
                             f'but sits in "{section.title}"')
    for rid in sorted(set(listed)):
        if listed.count(rid) > 1:
            found.append(f'law/block.json: {rid} is listed {listed.count(rid)} times')
    for rid in sorted(set(law.rules) - set(listed)):
        found.append(f'law/rules/{rid}.json: no section of law/block.json lists it')
    for line in (law.heading, *law.precedence, *(s.title for s in law.sections)):
        if not plain(line):
            found.append(f'law/block.json: "{line[:40]}" must be printable ASCII on one line')
    if not found and size(render_block(law)) > law.cap:
        found.append(f'the block is {size(render_block(law))} characters, over its cap of {law.cap}')
    return found


def size(block: str) -> int:
    """The block's length as the budget counts it: every character but the final newline."""
    return len(block.rstrip('\n'))


def render_block(law: Law) -> str:
    """The block every agent reads, ending in a newline."""
    lines = [f'## {law.heading}', '']
    lines += [f'- {line}' for line in law.precedence]
    for section in law.sections:
        lines += ['', f'### {section.title}', '']
        lines += [f'- {rid}: {law.rules[rid].text}' for rid in section.rules]
    return '\n'.join(lines) + '\n'


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def region(block: str) -> str:
    """The block between its markers, as it sits in a file."""
    return f'{BEGIN.format(digest(block))}\n\n{block}\n{END}\n'


@dataclasses.dataclass(frozen=True)
class Found:
    """A managed region found in a file."""

    start: int
    end: int
    marker: str  # the hash the BEGIN marker claims
    inner: str  # the text between the markers, without the blank lines around it

    @property
    def actual(self) -> str:
        return digest(self.inner)

    @property
    def edited(self) -> bool:
        return self.actual != self.marker


def find(text: str) -> Found | None:
    """The managed region in `text`, or None. More than one is an error."""
    matches = list(REGION.finditer(text))
    if len(matches) > 1:
        raise ValueError('more than one INTELLIGENCE block')
    if not matches:
        return None
    match = matches[0]
    inner = match.group('inner').replace('\r\n', '\n').strip('\n') + '\n'
    return Found(match.start(), match.end(), match.group('hash'), inner)


def replace(text: str, new_region: str) -> str:
    """`text` with its managed region swapped for `new_region`."""
    found = find(text)
    if found is None:
        raise ValueError('no INTELLIGENCE block to replace')
    return text[:found.start] + new_region + text[found.end:]


def sums(root: pathlib.Path, home_text: str, kit_text: str | None = None) -> str:
    """`home/SHA256SUMS`: what a consumer downloads from a release, and its hash."""
    installer = (root / INSTALLER).read_bytes()
    lines = [f'{digest(home_text)}  {HOME_FILE}']
    if kit_text is not None:
        lines.append(f'{digest(kit_text)}  {KIT_FILE}')
    lines.append(f'{hashlib.sha256(installer).hexdigest()}  {INSTALLER}')
    return '\n'.join(lines) + '\n'


def has_kit(root: pathlib.Path) -> bool:
    """Whether this hub ships the modules; a hub without the guard ships the rules alone."""
    return (root / kit.GUARD_FILE).exists()


def renderings(root: pathlib.Path, law: Law) -> dict[str, str]:
    """Every file this repository commits that the law decides, and its content."""
    block = render_block(law)
    home = region(block)
    agents_path = root / AGENTS_FILE
    agents = agents_path.read_text(encoding='utf-8') if agents_path.exists() else ''
    kit_text = kit.render_kit(root) if has_kit(root) else None
    out = {HOME_FILE: home}
    if kit_text is not None:
        out[KIT_FILE] = kit_text
    out[SUMS_FILE] = sums(root, home, kit_text)
    if find(agents) is not None:
        out[AGENTS_FILE] = replace(agents, home)
    return out


def stale(root: pathlib.Path, law: Law) -> list[str]:
    """Committed copies that differ from what the law renders."""
    found = []
    agents_path = root / AGENTS_FILE
    if not agents_path.exists() or find(agents_path.read_text(encoding='utf-8')) is None:
        found.append(f'{AGENTS_FILE}: carries no INTELLIGENCE block')
    for rel, text in renderings(root, law).items():
        path = root / rel
        current = path.read_text(encoding='utf-8') if path.exists() else None
        if current != text:
            found.append(f'{rel}: stale; run `python3 scripts/render.py --write`')
    return found


def git_show(root: pathlib.Path, ref: str, rel: str) -> bytes:
    done = subprocess.run(['git', 'show', f'{ref}:{rel}'], cwd=root, capture_output=True, check=False)
    if done.returncode != 0:
        raise SystemExit(f'{ref}:{rel} is not in this repository: {done.stderr.decode().strip()}')
    return done.stdout


def pins(root: pathlib.Path, ref: str | None) -> str:
    """The lines a consumer pins: the version and the hash of each file it downloads.

    A release from before the kit existed pins no kit, and `kit_sha256` is empty.
    """
    def read(rel: str) -> bytes:
        return git_show(root, ref, rel) if ref else (root / rel).read_bytes()

    def optional(rel: str) -> str:
        try:
            return hashlib.sha256(read(rel)).hexdigest()
        except (OSError, SystemExit):
            return ''
    return (f'version={ref or "unreleased"}\n'
            f'home_sha256={hashlib.sha256(read(HOME_FILE)).hexdigest()}\n'
            f'install_sha256={hashlib.sha256(read(INSTALLER)).hexdigest()}\n'
            f'kit_sha256={optional(KIT_FILE)}\n')


def setup_script(root: pathlib.Path, ref: str) -> str:
    """The cloud setup script with the pins of the release at `ref` filled in."""
    values = dict(line.split('=', 1) for line in pins(root, ref).splitlines())
    text = (root / SETUP_FILE).read_text(encoding='utf-8')
    for name, key in (('VERSION', 'version'), ('HOME_SHA256', 'home_sha256'),
                      ('INSTALL_SHA256', 'install_sha256'), ('KIT_SHA256', 'kit_sha256')):
        placeholder = f"{name}='@{name}@'"
        if placeholder not in text:
            if name == 'KIT_SHA256':
                continue  # a script from before the kit pins the rules alone
            raise SystemExit(f'{SETUP_FILE} has no {placeholder} to fill')
        text = text.replace(placeholder, f"{name}='{values[key]}'")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--write', action='store_true', help='rewrite every copy from the law')
    mode.add_argument('--check', action='store_true', help='fail on a broken law or a stale copy')
    mode.add_argument('--pins', nargs='?', const='', metavar='REF',
                      help='print the hashes to pin, for a tag or for this checkout')
    mode.add_argument('--setup', metavar='REF',
                      help='print the cloud setup script with the pins of a release tag')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = args.root

    if args.pins is not None:
        print(pins(root, args.pins or None), end='')
        return 0
    if args.setup:
        print(setup_script(root, args.setup), end='')
        return 0

    try:
        law = load_law(root)
    except LawError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    broken = problems(law) + (kit.problems(root) if has_kit(root) else [])
    if broken:
        for line in broken:
            print(f'error: {line}', file=sys.stderr)
        return 1
    block = render_block(law)

    if args.write:
        for rel, text in renderings(root, law).items():
            path = root / rel
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
                print(f'wrote {rel}')
        return 0

    if args.check:
        drift = stale(root, law)
        for line in drift:
            print(f'error: {line}', file=sys.stderr)
        length = size(block)
        note = f', over its target of {law.target}' if length > law.target else ''
        print(f'{len(law.rules)} rules; block {length} of {law.cap} characters{note}; '
              f'sha256 {digest(block)[:12]}')
        if has_kit(root):
            bundle, _ = kit.bundle(root)
            counts = (len(bundle['skills']), len(bundle['subagents']), bundle['knowledge'].count('\n- '))
            print('kit: ' + ', '.join(f'{n} {word}{"" if n == 1 else "s"}'
                                      for n, word in zip(counts, ('skill', 'subagent', 'fact'))))
        return 1 if drift else 0

    print(block, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
