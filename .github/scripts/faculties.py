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
when a copy differs from its pin, so a hand edit to a copy fails CI. Each
skill's trigger test comes with it, from its `assets/trigger-evals.json` into
`evals/skills/`, in the shape `evals.py` runs.

A release is a tag `vX.Y.Z`. `--pin` downloads each archive from that tag on
GitHub, or with `--from` reads it from the tag in a clone of the template,
never from whatever the clone has checked out, so a pin always holds the
release it names.

A home copy must give way to a vault's own. Claude Code loads a person's
skill over a repository's of the same name, so in a vault the kit's copy is
the one that loads, and each faculty opens with the rule that hands it over:
in a BRAIN vault, read the vault's copy and follow it instead. The home kit
is safe to carry only a faculty that opens with that rule word for word, the
wording the loader probe's `--handover` canary proves an app follows, so
`--pin` refuses a release whose faculty lacks it and `--check` fails a copy
that does.

`--pin` takes a release whole or not at all. It refuses an archive holding
a file outside its skill's folder, more than one folder deep, not text, or
too large, a skill with no trigger test, a file git would ignore, which a
clone of the hub would never hold, and the name of a skill the hub writes
itself. It writes everything aside first and moves it into place only once
all of it is written. Line endings are stored as LF, as git stores them.

Run it:

    python3 .github/scripts/faculties.py --check
    python3 .github/scripts/faculties.py --pin v3.0.0
    python3 .github/scripts/faculties.py --pin v3.0.0 --from ../knowledge
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PIN = 'kit/faculties.json'
SKILLS = 'kit/skills'
EVALS = 'evals/skills'
# Where a release of the template keeps each skill's archive.
ARCHIVE = 'System/Skills/{name}.skill'
URL = 'https://raw.githubusercontent.com/{source}/{version}/' + ARCHIVE
NAME = re.compile(r'[a-z0-9]+(-[a-z0-9]+)*')
VERSION = re.compile(r'v[0-9]+\.[0-9]+\.[0-9]+')
SOURCE = re.compile(r'[A-Za-z0-9-]+/[A-Za-z0-9._-]+')
TRIGGER_TEST = 'assets/trigger-evals.json'
MIN_PROMPTS = 5  # evals.py's floor for each side of a trigger test
MAX_FILE = 2 * 1024 * 1024  # bytes in one file of a skill
MAX_ARCHIVE = 32 * 1024 * 1024  # bytes in one archive, packed or unpacked
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
    if not SOURCE.fullmatch(pin['source']):
        raise Refused(f'{PIN}: {pin["source"]!r} is not an owner/repository')
    for name in [*pin['names'], *pin['skills']]:
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise Refused(f'{PIN}: {name!r} is not a skill name')
    return pin


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(data: bytes) -> bytes:
    """The bytes as git stores a text file: LF line endings."""
    return data.replace(b'\r\n', b'\n')


def tree_hash(files: dict[str, bytes]) -> str:
    """One hash for a folder: every file's path and the hash of its bytes, in path order."""
    lines = ''.join(f'{rel}\0{digest(canonical(data))}\n' for rel, data in sorted(files.items()))
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
        entries = archive.infolist()
    except (zipfile.BadZipFile, zlib.error, EOFError, OSError, ValueError) as error:
        raise Refused(f'{name}.skill is not a zip archive ({error})') from error
    files: dict[str, bytes] = {}
    total = 0
    for entry in entries:
        if entry.is_dir():
            continue
        path = pathlib.PurePosixPath(entry.filename)
        if not path.parts or path.is_absolute() or '..' in path.parts or path.parts[0] != name or len(path.parts) < 2:
            raise Refused(f'{name}.skill holds {entry.filename!r}, outside the {name}/ folder')
        if len(path.parts) > 3:
            raise Refused(f'{name}.skill holds {entry.filename}, more than one folder below SKILL.md')
        rel = pathlib.PurePosixPath(*path.parts[1:]).as_posix()
        if rel in files:
            raise Refused(f'{name}.skill holds {entry.filename} twice')
        try:
            with archive.open(entry) as stream:
                content = stream.read(MAX_FILE + 1)
        except (zipfile.BadZipFile, zlib.error, EOFError, OSError, RuntimeError, NotImplementedError) as error:
            raise Refused(f'{name}.skill: {entry.filename} cannot be read ({error})') from error
        total += len(content)
        if len(content) > MAX_FILE or total > MAX_ARCHIVE:
            raise Refused(f'{name}.skill: {entry.filename} is larger than a skill file may be')
        try:
            content.decode('utf-8')
        except UnicodeDecodeError as error:
            raise Refused(f'{name}.skill holds {entry.filename}, which is not text; a skill ships text only') from error
        if b'\0' in content:
            raise Refused(f'{name}.skill holds {entry.filename}, which is not text; a skill ships text only')
        files[rel] = canonical(content)
    for rel in files:
        parent = pathlib.PurePosixPath(rel).parent.as_posix()
        if parent in files:
            raise Refused(f'{name}.skill holds {parent} both as a file and as a folder')
    if 'SKILL.md' not in files:
        raise Refused(f'{name}.skill has no {name}/SKILL.md')
    return files


def hands_over(name: str, files: dict[str, bytes]) -> bool:
    """Whether the skill's SKILL.md opens with the hand-over rule, before its first section, naming its own copies."""
    opening = files.get('SKILL.md', b'').decode('utf-8', errors='replace').split('\n## ', 1)[0]
    return HANDOVER.format(name=name) in opening


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
    if not isinstance(data, dict):
        raise Refused(f'{name}/{TRIGGER_TEST} is not a JSON object')
    sides = []
    for keys in (('should_trigger',), ('should_not_trigger', 'near_miss')):
        items = next((data[key] for key in keys if data.get(key)), [])
        sides.append([p for p in (prompt(item) for item in (items if isinstance(items, list) else [])) if p])
    should, should_not = sides
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
    """One skill's archive as the release's tag holds it: in a clone of the template, or on GitHub."""
    path = ARCHIVE.format(name=name)
    if origin is not None:
        try:
            done = subprocess.run(['git', '-C', str(origin), 'cat-file', 'blob', f'refs/tags/{version}:{path}'],
                                  capture_output=True, timeout=60, check=False)
        except (OSError, subprocess.SubprocessError) as error:
            raise Refused(f'git cannot read {origin}: {error}') from error
        if done.returncode != 0:
            raise Refused(f'{origin} has no tag {version} holding {path}; fetch its tags with '
                          f'git -C {origin} fetch --tags, or check the release')
        return done.stdout
    url = URL.format(source=source, version=version, name=name)
    try:
        with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310 (a fixed https URL)
            data = response.read(MAX_ARCHIVE + 1)
    except (OSError, http.client.HTTPException, ValueError) as error:
        raise Refused(f'could not download {url}: {error}') from error
    if len(data) > MAX_ARCHIVE:
        raise Refused(f'{url} is larger than a skill archive may be')
    return data


def ignored(root: pathlib.Path, paths: list[str]) -> list[str]:
    """The paths git would ignore in the hub, which a clone of it would never hold; none outside a checkout."""
    try:
        done = subprocess.run(['git', '-C', str(root), 'check-ignore', '--no-index', '--stdin', '-z'],
                              input='\0'.join(paths).encode('utf-8'), capture_output=True, timeout=60, check=False)
    except (OSError, subprocess.SubprocessError):
        return []
    if done.returncode != 0:
        return []
    return [path for path in done.stdout.decode('utf-8', 'replace').split('\0') if path]


def write_tree(folder: pathlib.Path, files: dict[str, bytes]) -> None:
    for rel, content in files.items():
        path = folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def pin_release(root: pathlib.Path, version: str, origin: pathlib.Path | None = None) -> list[str]:
    """Replace every faculty's copy with the release's, rewrite the pin, and return what changed."""
    if not VERSION.fullmatch(version):
        raise Refused(f'{version!r} is not a release; a release of the template is a tag vX.Y.Z')
    pin = load_pin(root)
    taken = {}
    for name in pin['names']:
        if (root / SKILLS / name).exists() and name not in pin['skills']:
            raise Refused(f'{SKILLS}/{name} is the hub\'s own skill; a faculty never replaces it')
        data = fetch(pin['source'], version, name, origin)
        files = read_archive(data, name)
        if not hands_over(name, files):
            raise Refused(f'{name} at {version} does not open with the hand-over rule, so a home copy of it would '
                          'run in place of a vault\'s own; if the template reworded the rule, change HANDOVER to '
                          'match and run the loader probe with --handover')
        taken[name] = (data, files, trigger_test(name, files))
    dropped = sorted(set(pin['skills']) - set(pin['names']))
    for name in dropped:
        files = folder_files(root / SKILLS / name)
        entry = pin['skills'][name]
        if files and (not isinstance(entry, dict) or entry.get('files') != tree_hash(files)):
            raise Refused(f'{SKILLS}/{name} is no longer the copy {pin["version"]} pinned, so it is not removed; '
                          'move it aside or delete it yourself')
        evals = root / EVALS / f'{name}.json'
        if evals.is_file() and (not files or canonical(evals.read_bytes()) != trigger_test(name, files).encode('utf-8')):
            raise Refused(f'{EVALS}/{name}.json is no longer the trigger test {name} shipped, so it is not removed; '
                          'move it aside or delete it yourself')
    lost = ignored(root, [f'{SKILLS}/{name}/{rel}' for name, (_, files, _) in taken.items() for rel in files])
    if lost:
        raise Refused(f'git ignores {", ".join(lost[:3])}, so a clone of the hub would not hold it')
    skills = {name: {'archive': digest(data), 'files': tree_hash(files)} for name, (data, files, _) in taken.items()}
    pin['version'], pin['skills'] = version, dict(sorted(skills.items()))
    (root / 'kit').mkdir(parents=True, exist_ok=True)
    staging = pathlib.Path(tempfile.mkdtemp(prefix='.faculties-', dir=root / 'kit'))
    moved: list[tuple[pathlib.Path, pathlib.Path]] = []
    stranded = False

    def move(source: pathlib.Path, target: pathlib.Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        os.replace(source, target)
        moved.append((source, target))

    try:
        for name, (_, files, test) in taken.items():
            write_tree(staging / 'new' / name, files)
            (staging / 'evals').mkdir(exist_ok=True)
            (staging / 'evals' / f'{name}.json').write_text(test, encoding='utf-8')
        (staging / 'faculties.json').write_text(json.dumps(pin, indent=2, ensure_ascii=False) + '\n',
                                                encoding='utf-8')
        try:
            for name in [*taken, *dropped]:
                for live, kept in ((root / SKILLS / name, staging / 'old' / name),
                                   (root / EVALS / f'{name}.json', staging / 'old' / f'{name}.json')):
                    if live.exists():
                        move(live, kept)
            for name in taken:
                move(staging / 'new' / name, root / SKILLS / name)
                move(staging / 'evals' / f'{name}.json', root / EVALS / f'{name}.json')
            move(staging / 'faculties.json', root / PIN)
        except OSError as error:
            try:
                for source, target in reversed(moved):
                    os.replace(target, source)
            except OSError:
                stranded = True
                raise Refused(f'could not move the release into place, nor put every old copy back; what was moved '
                              f'aside is in {staging}') from error
            raise
    finally:
        if not stranded:
            shutil.rmtree(staging, ignore_errors=True)
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
    if not VERSION.fullmatch(version):
        found.append(f'{PIN}: {version!r} is not a release; a release of the template is a tag vX.Y.Z')
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
            found.append(f'{SKILLS}/{name}/SKILL.md: does not open with the hand-over rule as HANDOVER words it, so '
                         'a home copy would run in place of a vault\'s own')
        try:
            test = trigger_test(name, files)
        except Refused as error:
            found.append(str(error))
            continue
        evals = root / EVALS / f'{name}.json'
        if not evals.is_file() or canonical(evals.read_bytes()) != test.encode('utf-8'):
            found.append(f'{EVALS}/{name}.json: differs from the trigger test {name} ships; {fix}')
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='fail when a copy differs from its pin')
    mode.add_argument('--pin', metavar='VERSION', help='copy every faculty from this release of the template')
    parser.add_argument('--from', dest='origin', type=pathlib.Path,
                        help='read the archives from the release tag in a clone of the template, not GitHub')
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
    except (Refused, OSError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    for folder in written:
        print(f'pinned: {folder}')
    print(f'Pinned {len(written)} faculties at {args.pin}. Run make render, then make check, and commit all of it.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
