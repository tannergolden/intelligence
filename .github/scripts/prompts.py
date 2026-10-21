#!/usr/bin/env python3
"""Check the universal prompts the hub keeps, and give each repository a prompts page of its own.

WHY THIS EXISTS. A prompt typed in a hurry leaves out what an agent needs:
the goal, the context, the limits, and how to tell when it is done. So the
hub keeps universal prompts, written the way a good prompt is written, in
its own `docs/Prompts.md`, for anyone to copy into any AI app in any
repository. They stay in the hub. Every repository that takes part in sync
gets `docs/Prompts.md` once, from `setup/Prompts.md`: an empty page for its
own prompts, the ones that only make sense there, for using it, changing it
and understanding it. Sync never changes that page again.

An earlier release delivered the universal prompts into each repository's
`docs/Prompts.md`, between sealed `INTELLIGENCE:PROMPTS` markers. Sync takes
that block out again and leaves everything else in the file, the
repository's own prompts included; a file nobody touched since that release
becomes the empty page.

WHAT --check HOLDS THE HUB TO. Everyone copies the universal prompts from
here, so `--check` names each problem a reader would miss, with its line:

- no private repository named, no en or em dash, and no INTELLIGENCE:PROMPTS
  marker, in either file, since nothing seals or delivers the prompts now;
- a page a repository first gets that holds no prompt of its own;
- text a formatter leaves exactly as it is: no trailing whitespace or tab,
  no two blank lines in a row, `## ` and `### ` headings with a blank line
  around each, `-` bullets, and every block of code a ```text fence that
  closes, with no other fence inside it;
- no character that hides or reorders text, anywhere between the header and
  the footer;
- every universal prompt under its own `###` heading, with a **Use when**
  line before one block of text, and a **Fill in** line exactly when the
  prompt holds a placeholder: a prompt ready to run has nothing to fill in;
- in that text, only the sections the practices name, each closed, at most
  once and in their order: <context> and <task> always, and a <done_when>
  or an <output> to say when the work is done. A tag in backticks is only
  named, and nested tags, such as one that holds a pasted error, are free;
- each detail that changes in a {{PLACEHOLDER}} of capitals and
  underscores, and no stray brace;
- text an agent reads as it is meant: printable ASCII, the way the rules
  are, no emphasis in capitals, which current models overreact to, and no
  slot such as $ARGUMENTS that an app fills by itself when a prompt is
  saved as its command, and none of the wording the model makers now
  find useless or harmful, such as "think step by step" or a persona;
- no prompt longer than its cap, and no two headings alike;
- a "## Find A Prompt" part that links every prompt once, by its name,
  marks each prompt with details to fill in, and links nothing else, so a
  reader finds any prompt among dozens and knows which ask for details.

Run it:

    python3 .github/scripts/prompts.py            # print the page a repository first gets
    python3 .github/scripts/prompts.py --check    # fail on a broken file
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kit  # noqa: E402  the names a public file may carry, and the dash it may not
import render  # noqa: E402  the shape of a block an earlier release sealed

ROOT = pathlib.Path(__file__).resolve().parents[2]
UNIVERSAL = 'docs/Prompts.md'  # the universal prompts, in the hub
TEMPLATE = 'setup/Prompts.md'  # the page a repository first gets
TARGET = 'docs/Prompts.md'  # where a repository keeps its own prompts
OPT_OUT = 'no-intelligence-prompts'
HUB_PROMPTS = 'https://github.com/tannergolden/intelligence/blob/Development/docs/Prompts.md'

# The block an earlier release sealed into a repository's docs/Prompts.md,
# which sync takes out; and any of its markers, sealed or not, which neither
# file in the hub may carry.
SEALED = re.compile(r'^<!-- INTELLIGENCE:PROMPTS:BEGIN sha256:(?P<hash>[0-9a-f]{64}) -->[ \t]*\r?\n'
                    r'(?P<inner>.*?)'
                    r'^<!-- INTELLIGENCE:PROMPTS:END -->[ \t]*(?:\r?\n|\Z)', re.M | re.S)
MARKER = re.compile(r'^<!-- INTELLIGENCE:PROMPTS:(?:BEGIN|END)\b', re.M)
# What a file a release delivered holds outside its block, as SHA-256 of its
# text with LF line endings, for every release that delivered one: v0.3.0,
# which v0 also pointed at. A file that still holds exactly that is untouched
# since, and becomes the empty page whole.
DELIVERED = frozenset({'f9c3b26638b8940b35ac9af8084161952d8dde3ec18399e6233d0335f1523aac'})
# The note that release put above a repository's own prompts, and what
# replaces it where the repository kept the note as it was.
OLD_NOTE = ("_This repository's own prompts go here, in the shape above. \U0001f501 Intelligence Sync keeps the guide "
            "and the universal prompts above current, and never changes this section._")
NEW_NOTE = ("_This repository's own prompts go here, each with a `###` heading, a **Use when** line and one `text` "
            "block. Prompts that work in any repository, and how to write a good one, are in the "
            f"[universal prompts]({HUB_PROMPTS})._")
ADDED = "adds `docs/Prompts.md`, an empty page for this repository's own prompts"
TAKEN_OUT = ("takes the universal prompts out of `docs/Prompts.md`, since they now stay in the hub, and leaves this "
             "repository's own prompts as they were")

# The sections a universal prompt is built from, in the order it holds them,
# as the practices in the file describe them to a person. Each appears at
# most once; every prompt has the first two and at least one way to tell it
# is done.
SECTIONS = ('context', 'task', 'constraints', 'done_when', 'output')
REQUIRED = ('context', 'task')
ENDINGS = ('done_when', 'output')
# The most one prompt's text may run to. A prompt is pasted whole, and each
# line it adds is one more the agent weighs against the task.
CAP = 1600

# The part that links every prompt, so a reader finds one among dozens.
INDEX_NAME = 'Find A Prompt'
INDEX = re.compile(r'^## (?:\S+ )?' + re.escape(INDEX_NAME) + r'\s*$')
# The mark the index puts after a prompt with details to fill in, so a reader knows before copying it.
MARK = '\u270f\ufe0f'
LINK = re.compile(r'\[(?P<text>[^\]]+)\]\(#(?P<anchor>[^)\s]+)\)(?P<mark> \u270f\ufe0f?)?')

OPEN = '```text'
CLOSE = '```'
FENCE = re.compile(r'^\s*(?:```|~~~)')
RULE = re.compile(r'^---[ \t]*$', re.M)  # the line that sets the header and the footer apart
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
# Characters that hide or reorder text, which no line between the header and the footer may carry.
HIDDEN = re.compile('[\u200b\u200c\u200e\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff]')


# --- A repository's page ----------------------------------------------------------------------------


def find(text: str) -> render.Found | None:
    """The block an earlier release sealed into `text`, or None. More than one is an error."""
    matches = list(SEALED.finditer(text))
    if len(matches) > 1:
        raise ValueError('more than one INTELLIGENCE:PROMPTS block')
    if not matches:
        return None
    match = matches[0]
    inner = match.group('inner').replace('\r\n', '\n').strip('\n') + '\n'
    return render.Found(match.start(), match.end(), match.group('hash'), inner)


def page(text: str) -> str | None:
    """The page a repository first gets, from the text of a hub's `setup/Prompts.md`.

    None for a hub from before the page, whose file of that name held the
    universal prompts between markers for sync to seal.
    """
    return None if MARKER.search(text) else text


def template(root: pathlib.Path = ROOT) -> str | None:
    """The page a repository first gets, from the hub tree at `root`, or None for a hub from before it."""
    path = root / TEMPLATE
    return page(path.read_text(encoding='utf-8')) if path.is_file() else None


def opted_out(repo: dict) -> bool:
    """Whether a repository's settings keep the page out, with the `no-intelligence-prompts` topic."""
    return OPT_OUT in (repo.get('topics') or [])


def untouched(rest: str) -> bool:
    """Whether what a file holds outside its block is exactly what a release delivered."""
    return hashlib.sha256(rest.replace('\r\n', '\n').encode('utf-8')).hexdigest() in DELIVERED


def without_block(current: str, empty: str) -> str:
    """`current` with the block an earlier release delivered taken out, and everything else as it was.

    A file nobody touched since that release becomes the empty page. Where the
    block sat between two `---` lines, one stays, and the note that release put
    above the repository's own prompts, where it is still as written, points
    at the hub instead.
    """
    found = find(current)
    if found is None:
        return current
    before, after = current[:found.start], current[found.end:]
    if untouched(before + after):
        return empty
    before, after = before.rstrip('\n'), after.lstrip('\n')
    if before.rsplit('\n', 1)[-1].strip() == '---' and after.split('\n', 1)[0].strip() == '---':
        after = after.split('\n', 1)[1].lstrip('\n') if '\n' in after else ''
    text = f'{before}\n\n{after}' if before and after else before + after
    text = text if text.endswith('\n') else text + '\n'
    return text.replace(OLD_NOTE, NEW_NOTE)


def change(current: str | None, empty: str) -> tuple[str | None, str | None]:
    """What `docs/Prompts.md` becomes, and a note for the pull request; (None, None) leaves it as it is.

    A repository without the file gets the empty page. A file without the
    block an earlier release delivered is the repository's own, and sync never
    touches it.
    """
    if current is None:
        return empty, ADDED
    if find(current) is None:
        return None, None
    return without_block(current, empty), TAKEN_OUT


# --- The universal prompts ---------------------------------------------------------------------------


@dataclasses.dataclass
class Prompt:
    """One universal prompt, as the file holds it."""

    name: str
    line: int  # where its heading sits in the file
    lead: list[str] = dataclasses.field(default_factory=list)  # the lines between its heading and its text
    text: str = ''  # what its first block of text holds
    text_line: int = 0  # the line that text starts on
    blocks: int = 0  # how many blocks of text it holds

    @property
    def ready(self) -> bool:
        """Whether it runs as it is, with nothing to fill in: it has no **Fill in** line."""
        return '**Fill in**' not in '\n'.join(self.lead)


def parse(inner: str, first: int = 1) -> tuple[list[Prompt], list[tuple[int, str]]]:
    """The universal prompts in a file's text, and each line a formatter or a fence reader would take otherwise.

    `inner` is the text between the header and the footer as the file holds
    it, and `first` the line it starts on, so each problem names a line of the
    file.
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
                found.append((number, 'a heading here is "## " for a part or "### " for a prompt, '
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
    if '**Use when**' not in '\n'.join(prompt.lead):
        found.append((prompt.line, f'"{prompt.name}" says when to use it with **Use when**, before its text'))
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
    marked = PLACEHOLDER.search(text)
    if prompt.ready and marked:
        found.append((line(marked.start()), f'"{name}" holds {marked.group(0)} but no **Fill in** line; a prompt '
                                            'ready to run has nothing to fill in, and one with a placeholder says '
                                            'what to fill in'))
    if not prompt.ready and not marked:
        found.append((prompt.line, f'"{name}" says what to fill in but marks nothing; put each detail that changes '
                                   'from one use to the next in a {{PLACEHOLDER}}, or drop the **Fill in** line'))
    return found


def anchor(name: str) -> str:
    """The anchor GitHub gives a heading: lowercase, with punctuation and emoji dropped and spaces as hyphens."""
    return re.sub(r'[^\w\- ]', '', name.lower()).replace(' ', '-')


def index(inner: str, first: int, prompts: list[Prompt]) -> list[tuple[int, str]]:
    """The index part: one link to every universal prompt, each named as its heading, and no link to nowhere.

    A reader finds a prompt there among dozens, so a prompt the index leaves
    out is a prompt nobody finds.
    """
    rows = inner.replace('\r\n', '\n').split('\n')
    start = next((at for at, row in enumerate(rows) if INDEX.match(row)), None)
    if start is None:
        return [(first, f'the file has no "## {INDEX_NAME}" part, the index that links every prompt')]
    found: list[tuple[int, str]] = []
    targets: dict[str, Prompt] = {}
    for prompt in prompts:
        if anchor(prompt.name) in targets:
            found.append((prompt.line, f'"{prompt.name}" and "{targets[anchor(prompt.name)].name}" share the anchor '
                                       f'#{anchor(prompt.name)}'))
        targets.setdefault(anchor(prompt.name), prompt)
    linked: dict[str, int] = {}
    for at in range(start + 1, len(rows)):
        if re.match(r'^#{2,3} ', rows[at]):
            break
        for link in LINK.finditer(rows[at]):
            number, target = first + at, targets.get(link.group('anchor'))
            if target is None:
                found.append((number, f'the index links #{link.group("anchor")}, which no prompt heading makes'))
                continue
            if link.group('text') != target.name:
                found.append((number, f'the index calls "{target.name}" "{link.group("text")}"; name it as its '
                                      'heading does'))
            if target.name in linked:
                found.append((number, f'the index links "{target.name}" again; the first link is on line '
                                      f'{linked[target.name]}'))
            elif target.ready and link.group('mark'):
                found.append((number, f'the index marks "{target.name}" {MARK}, but it runs as it is, with '
                                      'nothing to fill in'))
            elif not target.ready and not link.group('mark'):
                found.append((number, f'"{target.name}" has details to fill in; mark its link in the index '
                                      f'with {MARK}'))
            linked.setdefault(target.name, number)
    for prompt in prompts:
        if prompt.name not in linked:
            found.append((prompt.line, f'"{prompt.name}" is missing from the "{INDEX_NAME}" index'))
    return found


def body(text: str) -> tuple[int, str] | None:
    """The part between a file's header and its footer, each set off by a `---` line, and the line it starts on."""
    rules = list(RULE.finditer(text))
    if len(rules) < 2:
        return None
    start, end = rules[0].end() + 1, rules[-1].start()
    return text.count('\n', 0, start) + 1, text[start:end]


def lint(text: str) -> list[str]:
    """Every problem with the universal prompts in `text`, each with its line."""
    part = body(text)
    if part is None:
        return [f'{UNIVERSAL}: the file needs its header and its footer, each set off by a --- line']
    first, inner = part
    prompts, found = parse(inner, first)
    if not prompts:
        found.append((first, 'the file holds no universal prompt under a "### " heading'))
    for prompt in prompts:
        found += check(prompt)
    found += index(inner, first, prompts)
    return [f'{UNIVERSAL}:{number}: {message}' for number, message in sorted(found)]


def public(name: str, text: str) -> list[str]:
    """What keeps a file from being read in public: a private repository named, or a dash the standards ban."""
    found = [f'{name} names tannergolden/{repo}, which is not a public repository'
             for repo in sorted(set(kit.NAMED.findall(text)) - set(kit.NAMEABLE))]
    if kit.DASHES.search(text):
        found.append(f'{name} holds an en or em dash; use a comma, colon, parentheses or a spaced hyphen')
    return found


def problems(root: pathlib.Path = ROOT) -> list[str]:
    """Everything wrong with the universal prompts and with the page a repository first gets."""
    found = []
    path = root / UNIVERSAL
    if not path.is_file():
        found.append(f'{UNIVERSAL} is missing')
    else:
        text = path.read_text(encoding='utf-8')
        found += public(UNIVERSAL, text)
        if MARKER.search(text):
            found.append(f'{UNIVERSAL}: an INTELLIGENCE:PROMPTS marker; the universal prompts stay in the hub, and '
                         'nothing seals them')
        found += lint(text)
    path = root / TEMPLATE
    if not path.is_file():
        found.append(f'{TEMPLATE} is missing')
    else:
        text = path.read_text(encoding='utf-8')
        found += public(TEMPLATE, text)
        if MARKER.search(text):
            found.append(f'{TEMPLATE}: an INTELLIGENCE:PROMPTS marker; the page a repository gets is all its own')
        if re.search(r'(?m)^### |^```', text):
            found.append(f'{TEMPLATE} holds a prompt; the page a repository first gets is empty, for its own')
    return found


def universal(root: pathlib.Path = ROOT) -> list[Prompt]:
    """The universal prompts in the hub tree at `root`."""
    part = body((root / UNIVERSAL).read_text(encoding='utf-8'))
    return parse(part[1], part[0])[0] if part else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--check', action='store_true', help='fail on a broken file')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    found = problems(args.root)
    for line in found:
        print(f'error: {line}', file=sys.stderr)
    if found:
        return 1
    if args.check:
        prompts = universal(args.root)
        ready = sum(prompt.ready for prompt in prompts)
        longest = max(prompts, key=lambda prompt: len(prompt.text))
        print(f'prompts: {len(prompts)} universal prompts in {UNIVERSAL}, {ready} ready to run and '
              f'{len(prompts) - ready} to fill in; the longest "{longest.name}" at {len(longest.text)} of {CAP} '
              f'characters; {TEMPLATE} is the page a repository first gets')
        return 0
    print(template(args.root), end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
