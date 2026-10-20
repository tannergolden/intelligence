#!/usr/bin/env python3
"""Seal the ready-made prompts every repository gets in docs/Prompts.md, and check their source.

WHY THIS EXISTS. A prompt typed in a hurry leaves out what an agent needs:
the goal, the context, the limits, and how to tell when it is done. So
every repository that takes part in sync gets `docs/Prompts.md`, a page of
ready-made prompts anyone can copy into an AI app. The hub keeps the part
between its `INTELLIGENCE:PROMPTS` markers current, the way it keeps the
rules current in `AGENTS.md`: how to use a prompt, the universal prompts,
and how to write a new one. Everything outside the markers is the
repository's own, its own prompts included, and sync never changes it.

The source is `setup/Prompts.md`: the file exactly as a repository first
gets it, with its markers unsealed, so it stays a file anyone can edit.
Sealing writes the SHA-256 of the block's text into the BEGIN marker, so a
release that leaves the prompts as they were touches no repository, and a
hand edit inside the markers is caught and repaired.

WHAT --check HOLDS THE SOURCE TO. The block reaches every repository before
anyone there reads it, so `--check` names each problem a reader would miss,
with its line:

- one unsealed block, no private repository named, and no en or em dash;
- text a formatter leaves exactly as it is: no trailing whitespace or tab,
  no two blank lines in a row, `## ` and `### ` headings with a blank line
  around each, `-` bullets, and every block of code a ```text fence that
  closes, with no other fence inside it. A repository that formats its
  Markdown would otherwise rewrite the block and break its hash, and the
  standards' Machined Block Check finds the markers by skipping fences;
- no character that hides or reorders text, anywhere in the block;
- every universal prompt under its own `###` heading, with its **Use when**
  and **Fill in** lines before one block of text;
- in that text, only the sections the practices name, each closed, at most
  once and in their order: <context> and <task> always, and a <done_when>
  or an <output> to say when the work is done. A tag in backticks is only
  named, and nested tags, such as one that holds a pasted error, are free;
- each detail that changes in a {{PLACEHOLDER}} of capitals and
  underscores, at least one in every prompt, and no stray brace;
- text an agent reads as it is meant: printable ASCII, the way the rules
  are, no emphasis in capitals, which current models overreact to, and no
  slot such as $ARGUMENTS that an app fills by itself when a prompt is
  saved as its command, and none of the wording the model makers now
  find useless or harmful, such as "think step by step" or a persona;
- no prompt longer than its cap, and no two headings alike.

Run it:

    python3 .github/scripts/prompts.py            # print the file a repository first gets
    python3 .github/scripts/prompts.py --check    # fail on a broken source
"""

from __future__ import annotations

import argparse
import dataclasses
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kit  # noqa: E402  the names a public file may carry, and the dash it may not
import render  # noqa: E402  the hash a block is sealed with, and its shape

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = 'setup/Prompts.md'
TARGET = 'docs/Prompts.md'
OPT_OUT = 'no-intelligence-prompts'

BEGIN = '<!-- INTELLIGENCE:PROMPTS:BEGIN sha256:{} -->'
END = '<!-- INTELLIGENCE:PROMPTS:END -->'
BLOCK = (r'^<!-- INTELLIGENCE:PROMPTS:BEGIN{} -->[ \t]*\r?\n'
         r'(?P<inner>.*?)'
         r'^<!-- INTELLIGENCE:PROMPTS:END -->[ \t]*(?:\r?\n|\Z)')
SEALED = re.compile(BLOCK.format(r' sha256:(?P<hash>[0-9a-f]{64})'), re.M | re.S)
UNSEALED = re.compile(BLOCK.format(''), re.M | re.S)

# The sections a universal prompt is built from, in the order it holds them,
# as the practices in the block describe them to a person. Each appears at
# most once; every prompt has the first two and at least one way to tell it
# is done.
SECTIONS = ('context', 'task', 'constraints', 'done_when', 'output')
REQUIRED = ('context', 'task')
ENDINGS = ('done_when', 'output')
# The most one prompt's text may run to. A prompt is pasted whole, and each
# line it adds is one more the agent weighs against the task.
CAP = 1600

OPEN = '```text'
CLOSE = '```'
FENCE = re.compile(r'^\s*(?:```|~~~)')
HEADING = re.compile(r'^#{1,6}(?:[ \t]|$)')
TITLE = re.compile(r'^(?P<level>#{2,3}) (?P<name>\S(?:.*\S)?)$')
BULLET = re.compile(r'^\s*[*+][ \t]')
NUMBERED = re.compile(r'^\s*\d+\)[ \t]')
TAG = re.compile(r'<(?P<close>/?)(?P<name>[A-Za-z][\w-]*)(?:\s[^<>]*)?>')  # a tag may name its source, as an attribute
TAG_NAME = re.compile(r'^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$')
MENTION = re.compile(r'`[^`\n]*`')  # a tag in backticks is named, not opened
PLACEHOLDER = re.compile(r'\{\{[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\}\}')
BRACED = re.compile(r'\{\{[^{}\n]*\}\}')
BRACES = re.compile(r'\{\{|\}\}')
SINGLE = re.compile(r'(?<!\{)\{[A-Z][A-Z0-9_]*\}(?!\})')
# Emphasis in capitals makes current models overreact to the line it marks.
SHOUTING = re.compile(r'\b(?:MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT|REQUIRED|WARNING|NOTE|DO NOT|DON\'T)\b')
# Wording the model makers now find useless or harmful: reasoning scaffolds a reasoning model does not need,
# a tie-breaker that makes it overreach, and a persona, which studies find adds nothing.
STALE = re.compile(r'(?i)\bthink (?:it through )?step by step\b|\bif in doubt\b|\btake a deep breath\b'
                   r'|\byou are (?:an?|the) (?:expert|senior|world-class|helpful)\b')
# The slots a tool fills by itself when a prompt is saved as its command or skill, which would eat the text.
SLOTS = re.compile(r'\$ARGUMENTS|\$[0-9]|\$\{input:|\{\{args\}\}|!\{|@\{')
# Characters that hide or reorder text, which no line of the block may carry.
HIDDEN = re.compile('[\u200b\u200c\u200e\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff]')


def inner(match: re.Match) -> str:
    """A block's text, without the blank lines around it, ending in a newline."""
    return match.group('inner').replace('\r\n', '\n').strip('\n') + '\n'


def region(text: str) -> str:
    """The prompts between their sealed markers, as they sit in a file."""
    return f'{BEGIN.format(render.digest(text))}\n\n{text}\n{END}\n'


def find(text: str) -> render.Found | None:
    """The sealed prompts block in `text`, or None. More than one is an error."""
    matches = list(SEALED.finditer(text))
    if len(matches) > 1:
        raise ValueError('more than one INTELLIGENCE:PROMPTS block')
    if not matches:
        return None
    match = matches[0]
    return render.Found(match.start(), match.end(), match.group('hash'), inner(match))


@dataclasses.dataclass(frozen=True)
class Prompts:
    """What one release delivers: the file a repository without one gets, and its sealed block."""

    seed: str
    region: str

    @property
    def marker(self) -> str:
        return find(self.region).marker


def seal(source: str) -> Prompts:
    """The release's prompts, from the text of `setup/Prompts.md`."""
    matches = list(UNSEALED.finditer(source))
    if len(matches) != 1:
        raise ValueError(f'{SOURCE} must hold exactly one unsealed INTELLIGENCE:PROMPTS block')
    match = matches[0]
    sealed = region(inner(match))
    return Prompts(source[:match.start()] + sealed + source[match.end():], sealed)


def load(root: pathlib.Path = ROOT) -> Prompts | None:
    """The prompts of the hub tree at `root`, or None for a hub from before them."""
    path = root / SOURCE
    return seal(path.read_text(encoding='utf-8')) if path.is_file() else None


def opted_out(repo: dict) -> bool:
    """Whether a repository's settings keep the prompts out, with the `no-intelligence-prompts` topic."""
    return OPT_OUT in (repo.get('topics') or [])


def change(current: str | None, prompts: Prompts) -> tuple[str | None, str | None]:
    """What `docs/Prompts.md` becomes, and a note when sync adds it; None leaves it as it is.

    A file of that name without the block is the repository's own, and sync
    never touches it.
    """
    if current is None:
        return prompts.seed, ("adds `docs/Prompts.md`, with ready-made prompts to copy and a section for this "
                              "repository's own")
    found = find(current)
    if found is None:
        return None, None
    new = current[:found.start] + prompts.region + current[found.end:]
    return (None if new == current else new), None


@dataclasses.dataclass
class Prompt:
    """One universal prompt, as the block holds it."""

    name: str
    line: int  # where its heading sits in the file
    lead: list[str] = dataclasses.field(default_factory=list)  # the lines between its heading and its text
    text: str = ''  # what its first block of text holds
    text_line: int = 0  # the line that text starts on
    blocks: int = 0  # how many blocks of text it holds


def parse(inner: str, first: int = 1) -> tuple[list[Prompt], list[tuple[int, str]]]:
    """The universal prompts in a block's text, and each line a formatter or a fence reader would take otherwise.

    `inner` is the text between the markers as the file holds it, and `first`
    the line it starts on, so each problem names a line of the file.
    """
    text = inner.replace('\r\n', '\n')
    rows = (text[:-1] if text.endswith('\n') else text).split('\n')
    found: list[tuple[int, str]] = []
    prompts: list[Prompt] = []
    seen: dict[str, int] = {}
    kinds: list[str] = []  # what each line is, outside code: blank, heading, item, indent or text
    current: Prompt | None = None
    opened = 0  # the line the block of code being read opened on; 0 outside one
    code: list[str] = []
    for index, row in enumerate(rows):
        number, line = first + index, row.rstrip()
        if line != row:
            found.append((number, 'trailing whitespace, which a formatter strips or reads as a line break'))
        if HIDDEN.search(row):
            found.append((number, 'a character that hides or reorders text, which no reader can see'))
        if opened:
            if line == CLOSE:
                kinds.append('close')
                if current is not None:
                    current.blocks += 1
                    if current.blocks == 1:
                        current.text, current.text_line = '\n'.join(code), opened + 1
                opened = 0
                continue
            if FENCE.match(line):
                found.append((number, 'a fence inside a block of text, where a fence reader would end the block'))
            kinds.append('code')
            code.append(row)
            continue
        if FENCE.match(line):
            if line != OPEN:
                found.append((number, f'a block of code opens with {OPEN} alone, at the start of its line'))
            kinds.append('open')
            opened, code = number, []
            continue
        if '\t' in line:
            found.append((number, 'a tab, which a formatter turns into spaces'))
        if not line:
            if kinds and kinds[-1] == 'blank':
                found.append((number, 'a second blank line in a row, which a formatter folds into one'))
            kinds.append('blank')
            continue
        if HEADING.match(line):
            kinds.append('heading')
            title = TITLE.match(line)
            if title is None:
                found.append((number, 'a heading in the block is "## " for a part or "### " for a prompt, '
                                      'then its name'))
                current = None
                continue
            name = title.group('name')
            if name in seen:
                found.append((number, f'a second heading "{name}"; the first is on line {seen[name]}'))
            seen.setdefault(name, number)
            current = Prompt(name, number) if title.group('level') == '###' else None
            if current is not None:
                prompts.append(current)
            continue
        if BULLET.match(line):
            found.append((number, 'a bullet a formatter rewrites; start each item with "- "'))
        if NUMBERED.match(line):
            found.append((number, 'a numbered item a formatter rewrites; end its number with a full stop'))
        item = BULLET.match(line) or NUMBERED.match(line) or re.match(r'^(?:-|\d+\.)[ \t]', line)
        kinds.append('item' if item else 'indent' if line[0] == ' ' else 'text')
        if current is not None and not current.blocks:
            current.lead.append(line)
    if opened:
        found.append((opened, 'a block of code that never closes'))
    for index, kind in enumerate(kinds):
        before = kinds[index - 1] if index else 'blank'
        after = kinds[index + 1] if index + 1 < len(kinds) else 'blank'
        if kind in ('heading', 'open') and before != 'blank':
            found.append((first + index, 'no blank line before it, which a formatter adds'))
        if kind in ('heading', 'close') and after not in ('blank', 'heading', 'open'):
            found.append((first + index, 'no blank line after it, which a formatter adds'))
        if kind == 'item' and before == 'text':
            found.append((first + index, 'a list with no blank line before it, which a formatter adds'))
        if kind == 'text' and before == 'item':
            found.append((first + index, 'a line run on from a list item, which a formatter indents into it'))
    return prompts, found


def check(prompt: Prompt) -> list[tuple[int, str]]:
    """Every way one universal prompt departs from the shape the practices describe."""
    found: list[tuple[int, str]] = []
    lead = '\n'.join(prompt.lead)
    if '**Use when**' not in lead or '**Fill in**' not in lead:
        found.append((prompt.line, f'"{prompt.name}" says when to use it with **Use when**, and what to fill in '
                                   'with **Fill in**, before its text'))
    if prompt.blocks != 1:
        found.append((prompt.line, f'"{prompt.name}" holds {prompt.blocks} blocks of text, where a prompt is one '
                                   'block, copied whole'))
    if not prompt.blocks:
        return found
    if len(prompt.text) > CAP:
        found.append((prompt.line, f'"{prompt.name}" runs to {len(prompt.text)} characters, over the cap of {CAP}'))
    for offset, row in enumerate(prompt.text.split('\n')):
        number = prompt.text_line + offset
        if not render.plain(row):
            found.append((number, f'"{prompt.name}": a character outside printable ASCII; the text an agent reads '
                                  'carries no hidden, bidirectional or look-alike character'))
        bare = PLACEHOLDER.sub('', row)
        for word in SHOUTING.findall(bare):
            found.append((number, f'"{prompt.name}": {word} in capitals; current models overreact to emphasis, so '
                                  'say it plainly once'))
        for phrase in STALE.findall(row):
            found.append((number, f'"{prompt.name}": "{phrase}" is wording current models do no better for, '
                                  'or worse; say what you need plainly'))
        for slot in SLOTS.findall(row):
            found.append((number, f'"{prompt.name}": {slot} is a slot an app fills by itself when the prompt is '
                                  'saved as its command; mark a detail as a {{PLACEHOLDER}}'))
    return found + sections(prompt) + placeholders(prompt)


def sections(prompt: Prompt) -> list[tuple[int, str]]:
    """The tags in a prompt's text: each closed in order, and its sections the ones the practices name."""
    name, found = prompt.name, []
    stack: list[tuple[str, int]] = []
    top: list[str] = []
    for offset, row in enumerate(prompt.text.split('\n')):
        number = prompt.text_line + offset
        for tag in TAG.finditer(MENTION.sub('', row)):
            word = tag.group('name')
            if not TAG_NAME.match(word):
                found.append((number, f'"{name}": {tag.group(0)} is not a tag this file writes; name one in '
                                      'lowercase words joined by underscores'))
            elif not tag.group('close'):
                if not stack and word not in SECTIONS:
                    found.append((number, f'"{name}": <{word}> is not a section the practices name: '
                                          + ', '.join(f'<{section}>' for section in SECTIONS)))
                elif not stack and word in top:
                    found.append((number, f'"{name}": a second <{word}>'))
                if not stack:
                    top.append(word)
                stack.append((word, number))
            elif any(word == open_word for open_word, _ in stack):
                while stack[-1][0] != word:
                    unclosed, at = stack.pop()
                    found.append((at, f'"{name}": <{unclosed}> is never closed'))
                stack.pop()
            else:
                found.append((number, f'"{name}": </{word}> closes a tag that is not open'))
    found += [(at, f'"{name}": <{word}> is never closed') for word, at in stack]
    known = [word for word in top if word in SECTIONS]
    if known != sorted(known, key=SECTIONS.index):
        found.append((prompt.text_line, f'"{name}": its sections run ' + ', '.join(f'<{word}>' for word in known)
                      + '; keep them in the order ' + ', '.join(f'<{section}>' for section in SECTIONS)))
    missing = [f'<{section}>' for section in REQUIRED if section not in top]
    if missing:
        found.append((prompt.line, f'"{name}" has no ' + ' and no '.join(missing)))
    if not any(section in top for section in ENDINGS):
        found.append((prompt.line, f'"{name}" has no <done_when> or <output>, so nothing says when the work is done'))
    return found


def placeholders(prompt: Prompt) -> list[tuple[int, str]]:
    """Each detail that changes from one use to the next, marked, and no brace that only looks like a mark."""
    name, text, found = prompt.name, prompt.text, []

    def line(at: int) -> int:
        return prompt.text_line + text.count('\n', 0, at)

    groups = list(BRACED.finditer(text))
    for group in groups:
        if not PLACEHOLDER.fullmatch(group.group(0)):
            found.append((line(group.start()), f'"{name}": {group.group(0)} is not a placeholder; name one in '
                                               'capitals and underscores, such as {{ERROR_OUTPUT}}'))
    for brace in BRACES.finditer(text):
        if not any(group.start() <= brace.start() < group.end() for group in groups):
            found.append((line(brace.start()), f'"{name}": a stray {brace.group(0)}, which no placeholder closes'))
    for single in SINGLE.finditer(text):
        found.append((line(single.start()), f'"{name}": {single.group(0)} takes double braces, as '
                                            f'{{{single.group(0)}}}'))
    if not PLACEHOLDER.search(text):
        found.append((prompt.line, f'"{name}" marks nothing to fill in; put each detail that changes from one use '
                                   'to the next in a {{PLACEHOLDER}}'))
    return found


def listed(names: list[str]) -> str:
    """Names as prose: A; A and B; A, B and C."""
    return names[0] if len(names) == 1 else ', '.join(names[:-1]) + ' and ' + names[-1]


def compare(old: str, new: str) -> str:
    """What a new block's text does to the universal prompts of an old one, as a phrase for a pull request.

    A reviewer of a sync sees which prompts it adds, rewords and drops
    without reading the diff of a sealed block.
    """
    before = {prompt.name: (prompt.lead, prompt.text) for prompt in parse(old)[0]}
    after = {prompt.name: (prompt.lead, prompt.text) for prompt in parse(new)[0]}
    added = [name for name in after if name not in before]
    reworded = [name for name in after if name in before and after[name] != before[name]]
    dropped = [name for name in before if name not in after]
    parts = ([f'adds {listed(added)}'] if added else []) + ([f'rewords {listed(reworded)}'] if reworded else []) + (
        [f'drops {listed(dropped)}'] if dropped else [])
    return listed(parts) if parts else 'changes only the guide around the prompts'


def lint(source: str) -> list[str]:
    """Every problem with the universal prompts in the source's one block, each with its line."""
    match = UNSEALED.search(source)
    if match is None:
        return []
    first = source.count('\n', 0, match.start('inner')) + 1
    prompts, found = parse(match.group('inner'), first)
    if not prompts:
        found.append((first, 'the block holds no universal prompt under a "### " heading'))
    for prompt in prompts:
        found += check(prompt)
    return [f'{SOURCE}:{number}: {message}' for number, message in sorted(found)]


def problems(root: pathlib.Path = ROOT) -> list[str]:
    """Everything wrong with `setup/Prompts.md`, which reaches every public repository."""
    path = root / SOURCE
    if not path.is_file():
        return [f'{SOURCE} is missing']
    text = path.read_text(encoding='utf-8')
    found = []
    if SEALED.search(text):
        found.append(f'{SOURCE}: a sealed marker; the source keeps its markers unsealed, and sync seals them')
    count = len(UNSEALED.findall(text))
    if count != 1:
        found.append(f'{SOURCE} holds {count} INTELLIGENCE:PROMPTS blocks, where it needs exactly one')
    for name in sorted(set(kit.NAMED.findall(text)) - set(kit.NAMEABLE)):
        found.append(f'{SOURCE} names tannergolden/{name}, which is not a public repository')
    if kit.DASHES.search(text):
        found.append(f'{SOURCE} holds an en or em dash; use a comma, colon, parentheses or a spaced hyphen')
    return found + (lint(text) if count == 1 else [])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--check', action='store_true', help='fail on a broken source')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    found = problems(args.root)
    for line in found:
        print(f'error: {line}', file=sys.stderr)
    if found:
        return 1
    release = load(args.root)
    if args.check:
        universal, _ = parse(find(release.seed).inner)
        longest = max(universal, key=lambda prompt: len(prompt.text))
        print(f'prompts: {len(universal)} universal prompts, the longest "{longest.name}" at '
              f'{len(longest.text)} of {CAP} characters; sha256 {release.marker[:12]}')
        return 0
    print(release.seed, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
