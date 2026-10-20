#!/usr/bin/env python3
"""Build a skill's .skill archive: the skill folder at its root, its team vendored, the same bytes every time.

Publish in the develop skill. It validates the skill first and refuses one
with errors. When the skill names a team in metadata.team and carries no
agents/ folder of its own, it copies that team's roster and member agents
from the agent home into the archive's agents/ folder, so the published
skill runs with nothing beside it. It leaves out hidden files, caches and
older archives, writes every entry with the same date and mode, and never
changes the source folder.

Run it:

    python3 scripts/package.py <skill folder> [--agents <agent home>]... [--out <folder>]
    python3 scripts/package.py <skill folder> --dry-run      # list the entries, write nothing

Add --json for one JSON object on stdout. It exits 1 when the skill fails
validation or its team cannot be found, and 0 once the archive is written.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import validate  # validate.py sits beside this file, wherever it is run from

LEFT_OUT_NAMES = ('.DS_Store', 'Thumbs.db', '__pycache__')
LEFT_OUT_SUFFIXES = ('.pyc', '.pyo', '.skill', '.swp')
FIXED_DATE = (1980, 1, 1, 0, 0, 0)  # the earliest a zip can record, so a rebuild changes no byte


def left_out(relative: pathlib.Path) -> bool:
    return (any(part.startswith('.') or part in LEFT_OUT_NAMES for part in relative.parts)
            or relative.suffix in LEFT_OUT_SUFFIXES)


def entries(folder: pathlib.Path, homes: list[pathlib.Path]) -> tuple[dict[str, pathlib.Path], list[str]]:
    """Each path in the archive and the file it comes from, and anything that stops the build."""
    name = folder.name
    out: dict[str, pathlib.Path] = {}
    problems: list[str] = []
    for path in sorted(folder.rglob('*')):
        relative = path.relative_to(folder)
        if left_out(relative) or path.is_dir():
            continue
        if path.is_symlink():
            problems.append(f'{path}: is a link; a skill ships real files')
            continue
        out[f'{name}/{relative.as_posix()}'] = path
    fields, _ = validate.read_frontmatter(folder / 'SKILL.md')
    metadata = fields.get('metadata')
    team = str(metadata.get('team', '')) if isinstance(metadata, dict) else ''
    if team and not (folder / 'agents').is_dir():
        roster, members = validate.find_team(team, homes, validate.Report())
        if roster is None:
            problems.append(f'{folder}: metadata.team names {team}, which no roster in the agent homes defines; '
                            'pass the home with --agents')
        else:
            wanted = [str(member) for member in roster.fields.get('members') or []]
            if len(members) != len(wanted):
                found = {member.title for member in members}
                missing = ', '.join(member for member in wanted if member not in found)
                problems.append(f'{roster.path}: names {missing}, which no agent file in the agent homes is titled')
            for spec in [roster, *members]:
                out[f'{name}/agents/{spec.path.name}'] = spec.path
    return dict(sorted(out.items())), problems


def build(folder: pathlib.Path, homes: list[pathlib.Path], target: pathlib.Path) -> None:
    """Write the archive at `target`, every entry with the same date and mode."""
    files, _ = entries(folder, homes)
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + '.partial')
    with zipfile.ZipFile(partial, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for arcname, path in files.items():
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    partial.replace(target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or '').split('\n', 1)[0])
    parser.add_argument('skill', type=pathlib.Path, help='the skill folder to package')
    parser.add_argument('--agents', action='append', default=[], type=pathlib.Path, metavar='HOME',
                        help="an agent home holding the skill's team; repeat for more")
    parser.add_argument('--out', type=pathlib.Path, default=pathlib.Path('.'), help='where to write <name>.skill')
    parser.add_argument('--allow-em-dash', action='store_true', help='for repositories whose rules allow the character')
    parser.add_argument('--dry-run', action='store_true', help='list the entries and write nothing')
    parser.add_argument('--json', action='store_true', help='print one JSON object instead of lines')
    args = parser.parse_args(argv)
    folder = args.skill.resolve()

    report = validate.Report()
    validate.check_skill(folder, args.agents, report, args.allow_em_dash)
    files: dict[str, pathlib.Path] = {}
    problems = list(report.errors)
    if not report.errors:
        files, more = entries(folder, args.agents)
        problems += more
    target = (args.out / f'{folder.name}.skill').resolve()
    written = not problems and not args.dry_run
    if written:
        build(folder, args.agents, target)
    vendored = sorted(arcname for arcname in files if arcname.startswith(f'{folder.name}/agents/'))
    if args.json:
        print(json.dumps({'archive': str(target) if written else None, 'entries': list(files),
                          'vendored': vendored, 'errors': problems, 'warnings': report.warnings}, indent=2))
    else:
        for line in problems:
            print(f'error: {line}')
        for line in report.warnings:
            print(f'warning: {line}')
        if args.dry_run and not problems:
            for arcname in files:
                print(arcname)
        if written:
            print(f'wrote {target}: {len(files)} files, {len(vendored)} of them the team in agents/')
        elif not problems:
            print(f'would write {target}: {len(files)} files')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
