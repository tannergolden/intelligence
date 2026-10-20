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
    return found


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
    prompts = load(args.root)
    if args.check:
        print(f'prompts: block sha256 {prompts.marker[:12]}')
        return 0
    print(prompts.seed, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
