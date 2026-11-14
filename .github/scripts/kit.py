#!/usr/bin/env python3
"""Render everything the home kit installs besides the rules into one bundle, `home/kit.json`.

WHY THIS EXISTS. The rules are one block, and the kit is what the home kit
puts beside them: the guard hook, `kit/guard.py`, which every app's
pre-tool hook calls. A release ships it as one JSON file, so a consumer
pins one more hash beside the home file and the installer, and the
installer writes a string it never has to convert. The source stays
readable and reviewable in `kit/`.

The kit carried skills and subagents until ADR-0041 took them out. Its
format moved to 3 with them, so an installer from before reads this kit as
the wrong format rather than as a kit missing a key.

It also holds the kit to what every public file here keeps to: it names no
private repository and holds no en or em dash. `render.py` calls it, so
`make render` writes the bundle and `make check` fails on a stale one.

Run it:

    python3 .github/scripts/kit.py            # print the bundle
    python3 .github/scripts/kit.py --check    # list every problem in the sources
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
KIT_FILE = 'home/kit.json'
GUARD_FILE = 'kit/guard.py'
# 2 dropped the knowledge facts (ADR-0023), and 3 the skills and the
# subagents (ADR-0041); the installer reads this one format.
FORMAT = 3

# The line that marks a file as the kit's own. The installer replaces what
# carries it and refuses to touch what does not.
OWNED = "Part of tannergolden/intelligence's home kit, which replaces this file on every install."

# Repositories a public file may name: the public ones, and the template the
# standards name by design. Any other tannergolden repository is private.
NAMEABLE = ('intelligence', 'standards', 'dotfiles', 'path', 'knowledge', 'repo', '.github', 'tannergolden')
NAMED = re.compile(r'tannergolden/(\.?[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*)')
DASHES = re.compile('[–—―]')


def bundle(root: pathlib.Path) -> tuple[dict, list[str]]:
    """The bundle, and every problem with its source."""
    found: list[str] = []
    guard = (root / GUARD_FILE).read_text(encoding='utf-8')
    if OWNED not in guard:
        found.append(f'{GUARD_FILE}: must carry the line "# {OWNED}", which marks the installed copy')
    kit = {
        '//': 'Everything the home kit installs besides the rules, rendered by .github/scripts/kit.py from '
              'kit/guard.py. Never edit this file by hand.',
        'format': FORMAT,
        'guard': guard,
    }
    text = json.dumps(kit, ensure_ascii=False)
    for name in sorted(set(NAMED.findall(text)) - set(NAMEABLE)):
        found.append(f'the kit names tannergolden/{name}, which is not a public repository')
    if DASHES.search(text):
        found.append('the kit holds an en or em dash; use a comma, colon, parentheses or a spaced hyphen')
    return kit, found


def render_kit(root: pathlib.Path) -> str:
    kit, _ = bundle(root)
    return json.dumps(kit, indent=2, ensure_ascii=False) + '\n'


def problems(root: pathlib.Path) -> list[str]:
    return bundle(root)[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('--check', action='store_true', help='list every problem in the sources')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    found = problems(args.root)
    for line in found:
        print(f'error: {line}', file=sys.stderr)
    if not args.check and not found:
        print(render_kit(args.root), end='')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
