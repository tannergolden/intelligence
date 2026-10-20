#!/usr/bin/env python3
"""Render the universal rules from the Constitution into every copy this hub publishes.

WHY THIS EXISTS. The rules live in one file, `CONSTITUTION.md` at the hub's
root: the precedence in Article I, every rule under the Article for its kind,
the block's heading, source line and budget in Article V, and the retired IDs
in its appendix. Every copy an agent reads is rendered from it and never
written by hand:

- the home file, `home/intelligence.md`, which the home kit copies into
  each app's folder, and which every repository's stub delivers between the
  markers of its root `AGENTS.md`;
- the kit, `home/kit.json`, which carries the guard hook, the skill and the
  subagents, rendered by `kit.py`;
- `home/SHA256SUMS`, the hashes a consumer pins.

The hub keeps no `AGENTS.md` of its own: it holds the source, not a copy.

A copy that drifts from the Constitution is a rule nobody wrote, so `--check`
fails CI until `--write` has brought every copy back in line. It also holds
the Constitution to its own Article VI:

- IDs are DOMAIN-NNN, appear once, and are never reused once retired;
- every rule is one ASCII sentence, quoted under its ID, with a reason;
- Invariants name an enforcer;
- the block fits its cap.

The block is marked with a hash of its own text, so a release that leaves it
unchanged touches no repository, and a hand edit inside the markers is
caught wherever it lands.

Run it:

    python3 scripts/render.py              # print the block
    python3 scripts/render.py --write      # rewrite every copy from the Constitution
    python3 scripts/render.py --check      # fail on a broken Constitution or a stale copy
    python3 scripts/render.py --pins v0.1.0  # the hashes to pin for a release
    python3 scripts/render.py --setup v0.1.0  # the cloud setup script, pinned
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
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
MAX_RULE = 300

CONSTITUTION_FILE = 'CONSTITUTION.md'
HOME_FILE = 'home/intelligence.md'
SUMS_FILE = 'home/SHA256SUMS'
INSTALLER = 'scripts/install.py'
KIT_FILE = kit.KIT_FILE
SETUP_FILE = 'setup/claude-cloud-setup.sh'

# The shape of CONSTITUTION.md, which Article VI describes to a person.
ARTICLE = re.compile(r'^##\s+(?:\S+\s+)?Article\s+([IVXLC]+):\s+(.+?)\s*$')
APPENDIX = re.compile(r'^##\s+(?:\S+\s+)?Appendix:\s+(.+?)\s*$')
FENCE = re.compile(r'^\s*(?:```|~~~)')
SETTING = re.compile(r'^- \*\*(?P<name>[A-Za-z]+):\*\*\s+(?P<value>.+?)\s*$')
CHARACTERS = re.compile(r'^(?P<count>\d[\d,]*) characters$')
FIELD = re.compile(r'^\*\*(?P<name>[^*]+)\*\*\s*(?P<rest>.*)$')
PRECEDENCE = 'Precedence'
THE_BLOCK = 'The Block'
RETIRED = 'Retired Rules'
# Each Article whose rules the block carries, in no particular order: the
# order of the Articles in the file is the order of the sections in the block.
SECTIONS = {
    'Invariants': ('invariant', 'every'),
    'Defaults': ('default', 'every'),
    'Owner-only Defaults': ('default', 'owner'),
}
NUMERALS = ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII')


@dataclasses.dataclass(frozen=True)
class Rule:
    id: str
    kind: str
    reach: str
    text: str
    why: str
    enforced_by: tuple[str, ...]
    to_add: tuple[str, ...]
    line: int = 0  # where its heading sits in CONSTITUTION.md


@dataclasses.dataclass(frozen=True)
class Section:
    title: str
    kind: str
    reach: str
    rules: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class Constitution:
    heading: str
    source: str
    precedence: tuple[str, ...]
    sections: tuple[Section, ...]
    target: int
    cap: int
    retired: dict[str, str]
    rules: dict[str, Rule]
    notes: tuple[str, ...] = ()  # what the reading found out of shape, as sentences


class ConstitutionError(Exception):
    """CONSTITUTION.md cannot be read, or lacks a part the block is built from."""


Line = tuple[int, str, bool]  # (line number, text, inside a code fence)


def chapters(text: str) -> list[tuple[int, str, list[Line]]]:
    """The file cut at each `## ` heading outside a code fence: (line, heading, body)."""
    out: list[tuple[int, str, list[Line]]] = []
    fenced = False
    for number, line in enumerate(text.replace('\r\n', '\n').split('\n'), 1):
        opens = bool(FENCE.match(line))
        if not fenced and not opens and line.startswith('## '):
            out.append((number, line.rstrip(), []))
        elif out:
            out[-1][2].append((number, line, fenced or opens))
        if opens:
            fenced = not fenced
    return out


def joined(parts: list[str]) -> str:
    return ' '.join(part.strip() for part in parts if part.strip())


def quoted_list(body: list[Line]) -> list[str]:
    """The items of the `> - ` list in a chapter, each wrapped line joined to its item."""
    items: list[list[str]] = []
    for _, line, fenced in body:
        if fenced or not line.startswith('>'):
            continue
        content = line[1:].strip()
        if content.startswith('- '):
            items.append([content[2:]])
        elif content and items:
            items[-1].append(content)
    return [joined(item) for item in items]


def settings(body: list[Line], where: int) -> dict[str, str]:
    found: dict[str, str] = {}
    for _, line, fenced in body:
        match = None if fenced else SETTING.match(line)
        if match:
            found[match.group('name')] = match.group('value')
    for name in ('Heading', 'Target', 'Cap'):
        if name not in found:
            raise ConstitutionError(f'{CONSTITUTION_FILE}:{where}: Article "{THE_BLOCK}" sets no **{name}:**')
    return found


def characters(value: str, name: str, where: int) -> int:
    match = CHARACTERS.match(value)
    if not match:
        raise ConstitutionError(f'{CONSTITUTION_FILE}:{where}: **{name}:** reads "N characters", not "{value}"')
    return int(match.group('count').replace(',', ''))


def retired_rows(body: list[Line], notes: list[str]) -> dict[str, str]:
    rows: dict[str, str] = {}
    for number, line, fenced in body:
        if fenced or not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        if len(cells) != 2:
            notes.append(f'{CONSTITUTION_FILE}:{number}: a retired row has an ID and where it went, nothing more')
        elif cells[0] != 'ID' and not set(cells[0]) <= set(':- '):
            rows[cells[0]] = cells[1]
    return rows


def rule_chunks(body: list[Line]) -> tuple[list[Line], list[tuple[int, str, list[Line]]]]:
    """A chapter's text before its first `### ` heading, then each `### ` heading with its body."""
    before: list[Line] = []
    chunks: list[tuple[int, str, list[Line]]] = []
    for number, line, fenced in body:
        if not fenced and line.startswith('### '):
            chunks.append((number, line[4:].strip(), []))
        elif chunks:
            chunks[-1][2].append((number, line, fenced))
        else:
            before.append((number, line, fenced))
    return before, chunks


def read_rule(rid: str, number: int, body: list[Line], kind: str, reach: str, notes: list[str]) -> Rule:
    """One rule: its quote, then **Why.**, **Enforced by:** and **To add:**."""
    where = f'{CONSTITUTION_FILE}:{number}: {rid}'
    quote: list[str] = []
    fields: dict[str, list[list[str]]] = {'Why.': [[]], 'Enforced by:': [], 'To add:': []}
    current = ''  # what the line being read belongs to: 'quote', a field's name, or nothing
    seen_quote = False
    for line_number, line, fenced in body:
        stripped = line.strip()
        if fenced:
            if stripped:
                notes.append(f'{CONSTITUTION_FILE}:{line_number}: {rid} holds a code block; '
                             'a rule holds its quote, **Why.**, **Enforced by:** and **To add:**')
            current = ''
            continue
        if not stripped or stripped == '---':
            if current in ('quote', 'Why.') or stripped == '---':
                current = ''
            continue
        if line.startswith('>'):
            if seen_quote and current != 'quote':
                notes.append(f'{where} quotes more than once; agents read one sentence')
            seen_quote, current = True, 'quote'
            quote.append(line[1:])
            continue
        field = FIELD.match(stripped)
        if field:
            name = field.group('name').strip()
            if name not in fields:
                notes.append(f'{CONSTITUTION_FILE}:{line_number}: {rid} has **{name}**, '
                             'which is not **Why.**, **Enforced by:** or **To add:**')
                current = ''
                continue
            if not seen_quote:
                notes.append(f'{where}: the sentence agents read is a > quote right under the heading')
                seen_quote = True
            current = name
            if field.group('rest'):
                if name == 'Why.':
                    fields[name][0].append(field.group('rest'))
                else:
                    notes.append(f'{CONSTITUTION_FILE}:{line_number}: {rid}: **{name}** is a list, '
                                 'one item to a line starting "- "')
            continue
        if current == 'Why.':
            fields['Why.'][0].append(stripped)
            continue
        if current in ('Enforced by:', 'To add:'):
            if stripped.startswith('- '):
                fields[current].append([stripped[2:]])
                continue
            if line[:1] in (' ', '\t') and fields[current]:
                fields[current][-1].append(stripped)
                continue
        notes.append(f'{CONSTITUTION_FILE}:{line_number}: {rid} has text outside its quote and fields')
        current = ''
    if not seen_quote:
        notes.append(f'{where}: the sentence agents read is a > quote right under the heading')
    return Rule(id=rid, kind=kind, reach=reach, text=joined(quote), why=joined(fields['Why.'][0]),
                enforced_by=tuple(joined(item) for item in fields['Enforced by:']),
                to_add=tuple(joined(item) for item in fields['To add:']), line=number)


def parse(text: str) -> Constitution:
    """Read the Constitution from its Markdown, as Article VI describes it."""
    notes: list[str] = []
    precedence: list[str] | None = None
    block: dict[str, str] | None = None
    block_line = 0
    retired: dict[str, str] = {}
    sections: list[Section] = []
    rules: dict[str, Rule] = {}
    count: dict[str, int] = {}
    numbered = 0
    for number, heading, body in chapters(text):
        article = ARTICLE.match(heading)
        appendix = APPENDIX.match(heading)
        title = article.group(2) if article else appendix.group(1) if appendix else ''
        if article:
            expected = NUMERALS[numbered] if numbered < len(NUMERALS) else '?'
            numbered += 1
            if article.group(1) != expected:
                notes.append(f'{CONSTITUTION_FILE}:{number}: Article {article.group(1)} should be numbered {expected}')
        before, chunks = rule_chunks(body)
        if article and title == PRECEDENCE:
            precedence = quoted_list(body)
        elif article and title == THE_BLOCK:
            block, block_line = settings(body, number), number
        elif appendix and title == RETIRED:
            retired = retired_rows(body, notes)
        elif article and title in SECTIONS:
            if any(section.title == title for section in sections):
                notes.append(f'{CONSTITUTION_FILE}:{number}: a second Article for {title}')
            kind, reach = SECTIONS[title]
            ids: list[str] = []
            for line_number, rid, chunk in chunks:
                count[rid] = count.get(rid, 0) + 1
                rule = read_rule(rid, line_number, chunk, kind, reach, notes)
                if rid not in rules:
                    rules[rid] = rule
                    ids.append(rid)
            sections.append(Section(title, kind, reach, tuple(ids)))
            continue
        for line_number, rid, _ in chunks:
            if re.match(r'^[A-Z]{2,5}-\d', rid):
                notes.append(f'{CONSTITUTION_FILE}:{line_number}: {rid} sits under "{heading[3:]}", '
                             'not under an Article whose rules the block carries')
    for rid, n in sorted(count.items()):
        if n > 1:
            notes.append(f'{CONSTITUTION_FILE}: {rid} appears {n} times; a rule has one heading')
    if precedence is None:
        raise ConstitutionError(f'{CONSTITUTION_FILE}: no "Article I: {PRECEDENCE}" quoting the precedence')
    if block is None:
        raise ConstitutionError(f'{CONSTITUTION_FILE}: no Article "{THE_BLOCK}" setting the heading and budget')
    for title in SECTIONS:
        if not any(section.title == title for section in sections):
            raise ConstitutionError(f'{CONSTITUTION_FILE}: no Article for {title}')
    return Constitution(
        heading=block['Heading'], source=block.get('Source', ''), precedence=tuple(precedence),
        sections=tuple(sections), target=characters(block['Target'], 'Target', block_line),
        cap=characters(block['Cap'], 'Cap', block_line), retired=retired, rules=rules, notes=tuple(notes),
    )


def load_constitution(root: pathlib.Path) -> Constitution:
    """Read `CONSTITUTION.md` at the hub's root."""
    try:
        text = (root / CONSTITUTION_FILE).read_text(encoding='utf-8')
    except OSError as error:
        raise ConstitutionError(f'{CONSTITUTION_FILE}: {error}') from error
    return parse(text)


def plain(text: str) -> bool:
    """Printable ASCII only: no hidden, bidirectional or look-alike characters."""
    return all(' ' <= char <= '~' for char in text)


def problems(constitution: Constitution) -> list[str]:
    """Every way the Constitution breaks its own Article VI, as sentences."""
    found = list(constitution.notes)
    for rule in constitution.rules.values():
        where = f'{CONSTITUTION_FILE}:{rule.line}: {rule.id}'
        if not ID.match(rule.id):
            found.append(f'{where}: the ID is not DOMAIN-NNN')
        if rule.id in constitution.retired:
            found.append(f'{where}: {rule.id} is retired and is never reused')
        if rule.kind == 'invariant' and not (rule.enforced_by or rule.to_add):
            found.append(f'{where}: an Invariant names its enforcer, today or to add')
        if not plain(rule.text):
            found.append(f'{where}: the quote must be printable ASCII')
        if not rule.text.endswith('.'):
            found.append(f'{where}: the quote is one sentence ending in a period')
        if len(rule.text) > MAX_RULE:
            found.append(f'{where}: the quote is {len(rule.text)} characters (limit {MAX_RULE})')
        if not rule.why:
            found.append(f'{where}: say why the rule exists, in a **Why.** paragraph')
    for rid in sorted(constitution.retired):
        if not ID.match(rid):
            found.append(f'{CONSTITUTION_FILE}: the retired ID {rid} is not DOMAIN-NNN')
    if not constitution.precedence:
        found.append(f'{CONSTITUTION_FILE}: Article I quotes no precedence')
    for line in (constitution.heading, constitution.source, *constitution.precedence):
        if not plain(line):
            found.append(f'{CONSTITUTION_FILE}: "{line[:40]}" must be printable ASCII')
    if not found and size(render_block(constitution)) > constitution.cap:
        found.append(f'the block is {size(render_block(constitution))} characters, '
                     f'over its cap of {constitution.cap}')
    return found


def size(block: str) -> int:
    """The block's length as the budget counts it: every character but the final newline."""
    return len(block.rstrip('\n'))


def render_block(constitution: Constitution) -> str:
    """The block every agent reads, ending in a newline."""
    lines = [f'## {constitution.heading}', '']
    if constitution.source:
        lines += [constitution.source, '']
    lines += [f'- {line}' for line in constitution.precedence]
    for section in constitution.sections:
        lines += ['', f'### {section.title}', '']
        lines += [f'- {rid}: {constitution.rules[rid].text}' for rid in section.rules]
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


def renderings(root: pathlib.Path, constitution: Constitution) -> dict[str, str]:
    """Every file this repository commits that the Constitution decides, and its content."""
    home = region(render_block(constitution))
    kit_text = kit.render_kit(root) if has_kit(root) else None
    out = {HOME_FILE: home}
    if kit_text is not None:
        out[KIT_FILE] = kit_text
    out[SUMS_FILE] = sums(root, home, kit_text)
    return out


def stale(root: pathlib.Path, constitution: Constitution) -> list[str]:
    """Committed copies that differ from what the Constitution renders."""
    found = []
    for rel, text in renderings(root, constitution).items():
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
    mode.add_argument('--write', action='store_true', help='rewrite every copy from the Constitution')
    mode.add_argument('--check', action='store_true', help='fail on a broken Constitution or a stale copy')
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
        constitution = load_constitution(root)
    except ConstitutionError as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    broken = problems(constitution) + (kit.problems(root) if has_kit(root) else [])
    if broken:
        for line in broken:
            print(f'error: {line}', file=sys.stderr)
        return 1
    block = render_block(constitution)

    if args.write:
        for rel, text in renderings(root, constitution).items():
            path = root / rel
            if not path.exists() or path.read_text(encoding='utf-8') != text:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
                print(f'wrote {rel}')
        return 0

    if args.check:
        drift = stale(root, constitution)
        for line in drift:
            print(f'error: {line}', file=sys.stderr)
        length = size(block)
        note = f', over its target of {constitution.target}' if length > constitution.target else ''
        print(f'{len(constitution.rules)} rules; block {length} of {constitution.cap} characters{note}; '
              f'sha256 {digest(block)[:12]}')
        if has_kit(root):
            bundle, _ = kit.bundle(root)
            counts = (len(bundle['skills']), len(bundle['subagents']))
            print('kit: ' + ', '.join(f'{n} {word}{"" if n == 1 else "s"}'
                                      for n, word in zip(counts, ('skill', 'subagent'))))
        return 1 if drift else 0

    print(block, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
