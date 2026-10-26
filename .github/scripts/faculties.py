#!/usr/bin/env python3
"""Keep the kit's copy of the faculty skills, pinned to one release of tannergolden/knowledge.

WHY THIS EXISTS. The five faculty skills, research, discover, editorial,
visualize and finance, are written in the knowledge template, beside the
vault layout they work in, and every vault takes them from there. The home
kit carries them to every other repository on its owner's machines, so the
hub keeps a copy of each in `kit/skills/`, taken from one release of the
template and pinned in `kit/faculties.json`: the release, and for each skill
the SHA-256 of the archive it came from and of the files it holds. A copy is
never edited by hand, here or anywhere: `--pin` replaces every copy with a
release's and rewrites the pin, and `--check`, which `make check` runs, fails
when a copy differs from its pin, so a hand edit cannot reach a release.
Each skill's trigger test comes with it, from its `assets/trigger-evals.json`
into `evals/skills/`, in the shape `evals.py` runs.

A home copy must give way to a vault's own. Claude Code loads a person's
skill over a repository's of the same name, so in a vault the kit's copy is
the one that loads, and each faculty opens with the rule that hands it over:
in a BRAIN vault, read the vault's copy and follow it instead. The home kit
is safe to carry only a faculty that holds that rule word for word, the
wording the loader probe's `--handover` canary proves an app follows, so
`--pin` refuses a release whose faculty lacks it and `--check` fails a copy
that does.

A faculty never replaces a skill the hub writes itself: `--pin` refuses a
name whose folder in `kit/skills/` it did not put there.

Run it:

    python3 .github/scripts/faculties.py --check
    python3 .github/scripts/faculties.py --pin v3.0.0
    python3 .github/scripts/faculties.py --pin v3.0.0 --from ../knowledge
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import re
import shutil
import sys
import urllib.request
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PIN = 'kit/faculties.json'
SKILLS = 'kit/skills'
EVALS = 'evals/skills'
# Where a release of the template serves each skill's archive.
URL = 'https://raw.githubusercontent.com/{source}/{version}/System/Skills/{name}.skill'
NAME = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
VERSION = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]*$')
TRIGGER_TEST = 'assets/trigger-evals.json'
MIN_PROMPTS = 5  # evals.py's floor for each side of a trigger test
# The rule each faculty opens with, for its own name, and the canary carries.
HANDOVER = ("**Where it runs.** In a BRAIN vault, whose `AGENTS.md` says it is one, the vault's own copy of this "
            "skill runs: if the file you loaded is not that vault's `.agents/skills/{name}/SKILL.md` or "
            "`.claude/skills/{name}/SKILL.md`, read the vault's copy and follow it instead, with the files beside "
            "it, because a vault's copy matches its layout and its owner may have changed it.")


class Refused(Exception):
    """A release, an archive or a pin this script will not take."""


def load_pin(root: pathlib.Path) -> dict:
    """The pin, held to its shape: a source, the names it carries, a release and each copy's hashes."""
    path = root / PIN
    try:
        pin = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise Refused(f'{PIN}: cannot be read ({error})') from error
    if not isinstance(pin, dict) or not isinstance(pin.get('source'), str) or not isinstance(pin.get('version'), str) \
            or not isinstance(pin.get('names'), list) or not isinstance(pin.get('skills'), dict):
        raise Refused(f'{PIN}: needs a source, a version, a list of names and a map of skills')
    for name in pin['names']:
        if not isinstance(name, str) or not NAME.match(name):
            raise Refused(f'{PIN}: {name!r} is not a skill name')
    return pin


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree_hash(files: dict[str, bytes]) -> str:
    """One hash for a folder: every file's path and the hash of its bytes, in path order."""
    lines = ''.join(f'{rel}\0{digest(data)}\n' for rel, data in sorted(files.items()))
    return digest(lines.encode('utf-8'))


def folder_files(folder: pathlib.Path) -> dict[str, bytes]:
    if not folder.is_dir():
        return {}
    return {path.relative_to(folder).as_posix(): path.read_bytes()
            for path in sorted(folder.rglob('*')) if path.is_file()}


def read_archive(data: bytes, name: str) -> dict[str, bytes]:
    """The files of one skill's archive, by their path inside the skill, after every check the kit makes."""
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as error:
        raise Refused(f'{name}.skill is not a zip archive') from error
    files: dict[str, bytes] = {}
    for entry in archive.infolist():
        if entry.is_dir():
            continue
        path = pathlib.PurePosixPath(entry.filename)
        if path.is_absolute() or '..' in path.parts or path.parts[0] != name or len(path.parts) < 2:
            raise Refused(f'{name}.skill holds {entry.filename}, outside the {name}/ folder')
        content = archive.read(entry)
        try:
            content.decode('utf-8')
        except UnicodeDecodeError as error:
            raise Refused(f'{name}.skill holds {entry.filename}, which is not text; a skill ships text only') from error
        files[pathlib.PurePosixPath(*path.parts[1:]).as_posix()] = content
    if 'SKILL.md' not in files:
        raise Refused(f'{name}.skill has no {name}/SKILL.md')
    return files


def hands_over(name: str, files: dict[str, bytes]) -> bool:
    """Whether the skill's SKILL.md holds the hand-over rule, naming its own copies in a vault."""
    return HANDOVER.format(name=name) in files.get('SKILL.md', b'').decode('utf-8', errors='replace')


def prompt(item: object) -> str:
    """One prompt of a trigger test: the text itself, or the q or query a routed entry carries."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return str(item.get('q') or item.get('query') or '')
    return ''


def trigger_test(name: str, files: dict[str, bytes]) -> str:
    """The skill's trigger test in evals/skills/'s shape, from the one the skill ships."""
    if TRIGGER_TEST not in files:
        raise Refused(f'{name} ships no {TRIGGER_TEST}, so the hub would carry a skill with no trigger test')
    try:
        data = json.loads(files[TRIGGER_TEST].decode('utf-8'))
    except ValueError as error:
        raise Refused(f'{name}/{TRIGGER_TEST} is not JSON') from error
    should = [p for p in (prompt(item) for item in data.get('should_trigger') or []) if p]
    should_not = [p for p in (prompt(item) for item in data.get('should_not_trigger') or data.get('near_miss') or [])
                  if p]
    if len(should) < MIN_PROMPTS or len(should_not) < MIN_PROMPTS:
        raise Refused(f'{name}/{TRIGGER_TEST} needs at least {MIN_PROMPTS} prompts each that should and should not '
                      'trigger it')
    test = {
        '//': f'The trigger test for {name}, taken from its {TRIGGER_TEST} by .github/scripts/faculties.py. '
              'Never edit it by hand.',
        'skill': name,
        'runs': 3,
        'threshold': 0.5,
        'should_trigger': should,
        'should_not_trigger': should_not,
    }
    return json.dumps(test, indent=2, ensure_ascii=False) + '\n'


def fetch(source: str, version: str, name: str, origin: pathlib.Path | None) -> bytes:
    """One skill's archive at the release: from a checkout of the template, or from GitHub."""
    if origin is not None:
        path = origin / 'System' / 'Skills' / f'{name}.skill'
        try:
            return path.read_bytes()
        except OSError as error:
            raise Refused(f'{path}: cannot be read ({error})') from error
    url = URL.format(source=source, version=version, name=name)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310 (a fixed https URL)
            return response.read()
    except OSError as error:
        raise Refused(f'could not download {url}: {error}') from error


def pin_release(root: pathlib.Path, version: str, origin: pathlib.Path | None = None) -> list[str]:
    """Replace every faculty's copy with the release's, rewrite the pin, and return what changed."""
    if not VERSION.match(version):
        raise Refused(f'{version!r} is not a release name')
    pin = load_pin(root)
    taken = {}
    for name in pin['names']:
        folder = root / SKILLS / name
        if folder.exists() and name not in pin['skills']:
            raise Refused(f'{SKILLS}/{name} is the hub\'s own skill; a faculty never replaces it')
        data = fetch(pin['source'], version, name, origin)
        files = read_archive(data, name)
        if not hands_over(name, files):
            raise Refused(f'{name} at {version} lacks the hand-over rule, so a home copy of it would run in place '
                          'of a vault\'s own; if the template reworded the rule, change HANDOVER to match and '
                          'run the loader probe with --handover')
        taken[name] = (data, files, trigger_test(name, files))
    for name in sorted(set(pin['skills']) - set(pin['names'])):
        shutil.rmtree(root / SKILLS / name, ignore_errors=True)
        (root / EVALS / f'{name}.json').unlink(missing_ok=True)
    skills = {}
    for name, (data, files, test) in sorted(taken.items()):
        folder = root / SKILLS / name
        shutil.rmtree(folder, ignore_errors=True)
        for rel, content in files.items():
            path = folder / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        (root / EVALS).mkdir(parents=True, exist_ok=True)
        (root / EVALS / f'{name}.json').write_text(test, encoding='utf-8')
        skills[name] = {'archive': digest(data), 'files': tree_hash(files)}
    pin['version'], pin['skills'] = version, skills
    (root / PIN).write_text(json.dumps(pin, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return [f'{SKILLS}/{name}' for name in sorted(skills)]


def problems(root: pathlib.Path) -> list[str]:
    """Every way the copies, their trigger tests and the pin disagree."""
    try:
        pin = load_pin(root)
    except Refused as error:
        return [str(error)]
    found = []
    names, skills, version = pin['names'], pin['skills'], pin['version']
    fix = f'run make faculties VERSION={version or "vX.Y.Z"}, never an edit by hand'
    if not version:
        if skills:
            found.append(f'{PIN}: pins no release, so it records no skills')
        for name in names:
            if (root / SKILLS / name).exists():
                found.append(f'{SKILLS}/{name}: a faculty with no release pinned; {fix}')
        return found
    if sorted(skills) != sorted(names):
        found.append(f'{PIN}: records {", ".join(sorted(skills)) or "no skills"}, but carries {", ".join(sorted(names))}; '
                     f'{fix}')
    for name in sorted(set(names) & set(skills)):
        files = folder_files(root / SKILLS / name)
        entry = skills[name]
        if not files:
            found.append(f'{SKILLS}/{name}: missing; {fix}')
            continue
        if not isinstance(entry, dict) or entry.get('files') != tree_hash(files):
            found.append(f'{SKILLS}/{name}: differs from the copy {version} pinned; {fix}')
            continue
        if not hands_over(name, files):
            found.append(f'{SKILLS}/{name}/SKILL.md: lacks the hand-over rule as HANDOVER words it, so a home copy '
                         'would run in place of a vault\'s own')
        try:
            test = trigger_test(name, files)
        except Refused as error:
            found.append(str(error))
            continue
        evals = root / EVALS / f'{name}.json'
        if not evals.is_file() or evals.read_text(encoding='utf-8') != test:
            found.append(f'{EVALS}/{name}.json: differs from the trigger test {name} ships; {fix}')
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='fail when a copy differs from its pin')
    mode.add_argument('--pin', metavar='VERSION', help='copy every faculty from this release of the template')
    parser.add_argument('--from', dest='origin', type=pathlib.Path,
                        help='read the archives from a checkout of the template at that release, not GitHub')
    parser.add_argument('--root', type=pathlib.Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.check:
        found = problems(args.root)
        for line in found:
            print(f'error: {line}', file=sys.stderr)
        if not found:
            pin = load_pin(args.root)
            print(f'The faculties match their pin ({pin["version"] or "no release pinned yet"}).')
        return 1 if found else 0
    try:
        written = pin_release(args.root, args.pin, args.origin)
    except Refused as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    for folder in written:
        print(f'pinned: {folder}')
    print(f'Pinned {len(written)} faculties at {args.pin}. Run make render, then make check, and commit all of it.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
