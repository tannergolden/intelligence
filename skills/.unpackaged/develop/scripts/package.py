#!/usr/bin/env python3
# =============================================================================
# package.py - pack a skill directory into an archive claude.ai can install
# =============================================================================
# WHAT A PACKAGED SKILL ACTUALLY IS, because the naming invites a wrong guess:
# it is a ZIP archive containing the skill FOLDER at its root, not a bespoke
# binary format. There is no parser, no manifest header and no signature. The
# only documented consumer is the web upload at Settings, Capabilities, Skills,
# which reads the SKILL.md inside and shows you the name it found.
#
# THE COMMAND-LINE TOOLS DO NOT READ ARCHIVES AT ALL. They read directories:
# a skill is installed by copying its folder into whichever directory the tool
# discovers. So packaging is for the web upload and for handing someone a
# single file, and never for the tools most of this repository targets.
#
# THE EXTENSION. Every source says the upload takes a ZIP: "package your skill
# folder as a ZIP file", "upload a ZIP file containing your skill folder". No
# documentation anywhere describes a `.skill` extension, and the file picker is
# the thing that would reject it, so `.zip` is the default because installing
# is the point. `--extension skill` writes the identical bytes under the other
# name for anyone who wants it; if an upload refuses that file, the fix is to
# rename it back.
#
# THE MOST COMMON UPLOAD FAILURE is an archive whose root is SKILL.md rather
# than the folder holding it. The upload then cannot find the manifest, and the
# error does not say that. This script cannot produce that shape.
#
# DETERMINISTIC BY CONSTRUCTION. Entries are sorted and every timestamp and
# permission bit is fixed, so packing unchanged source twice produces
# byte-identical archives. Without that, a rebuilt package always looks
# changed, and "did the content change?" stops being answerable.
#
# Usage:  python3 package.py <skill-dir> [--out DIR] [--include-evals]
#                                        [--extension zip|skill]
# =============================================================================
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

# `evals/` is read by evaluation tooling and never by an agent. Shipping it
# inflates the upload with cases the reader cannot act on.
EXCLUDED_DIRS = ("evals",)
EXCLUDED_NAMES = (".DS_Store", "Thumbs.db", ".gitkeep")
EXCLUDED_SUFFIXES = (".pyc",)

NAME_RE = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")

# A fixed timestamp for every entry. ZIP cannot store a year before 1980, so
# this is the earliest legal value rather than an arbitrary one.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
FIXED_MODE = 0o644 << 16


def frontmatter_name(manifest: Path):
    """The `name` field, read without a YAML parser.

    Flat scalars only, which is all the specification requires. Anything more
    elaborate is refused by the repository's own checker before a skill gets
    this far, so this reads the simple shape and reports when it cannot.
    """
    lines = manifest.read_text(encoding="utf-8").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if key.strip() == "name":
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            return value
    return None


def included(rel: Path, include_evals: bool) -> bool:
    parts = rel.parts
    if not include_evals and parts and parts[0] in EXCLUDED_DIRS:
        return False
    if rel.name in EXCLUDED_NAMES or rel.suffix in EXCLUDED_SUFFIXES:
        return False
    # A dot-directory inside a skill is development scaffolding, never content.
    return not any(part.startswith(".") for part in parts[:-1])


def package(skill_dir: Path, out_dir: Path, include_evals: bool, extension: str):
    if not skill_dir.is_dir():
        raise SystemExit(f"error: {skill_dir} is not a directory")

    manifest = skill_dir / "SKILL.md"
    if not manifest.is_file():
        raise SystemExit(
            f"error: {skill_dir} has no SKILL.md, so it is not a skill. Nothing "
            "discovers a directory without one, and nothing reports it as skipped.")

    folder = skill_dir.name
    if not NAME_RE.match(folder):
        raise SystemExit(
            f"error: directory name {folder!r} must be lowercase alphanumerics and "
            "single hyphens, with no leading or trailing hyphen.")

    declared = frontmatter_name(manifest)
    if declared is None:
        raise SystemExit("error: SKILL.md has no readable `name` in its frontmatter.")
    if declared != folder:
        raise SystemExit(
            f"error: frontmatter name is {declared!r} but the directory is {folder!r}. "
            "They must match: discovery uses the directory and the listing uses the "
            "field, so a mismatch is found under one name and invoked under another.")

    members = sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and included(p.relative_to(skill_dir), include_evals)
    )
    if not members:
        raise SystemExit(f"error: {skill_dir} has no files to package.")

    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{folder}.{extension}"

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in members:
            rel = path.relative_to(skill_dir)
            # THE FOLDER IS THE ROOT OF THE ARCHIVE. An archive whose root is
            # SKILL.md rather than the folder is rejected on upload, and the
            # error does not say why.
            info = zipfile.ZipInfo(f"{folder}/{rel.as_posix()}", date_time=FIXED_TIME)
            info.external_attr = FIXED_MODE
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    print(f"packaged {len(members)} file(s) into {archive}")
    for path in members:
        print(f"  {folder}/{path.relative_to(skill_dir).as_posix()}")
    if not include_evals and (skill_dir / "evals").is_dir():
        print("  (evals/ excluded: read by tooling, never by an agent)")
    return archive


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack a skill directory into a ZIP archive with the folder at its root.")
    parser.add_argument("skill", type=Path, help="the skill directory to package")
    parser.add_argument("--out", type=Path, default=Path("dist"),
                        help="where to write the archive (default: dist)")
    parser.add_argument("--include-evals", action="store_true",
                        help="ship evals/ too. Off by default: no agent reads it.")
    parser.add_argument("--extension", choices=("zip", "skill"), default="zip",
                        help="archive extension. The bytes are a ZIP either way, "
                             "and every documented upload path asks for zip, so "
                             "that is the default.")
    args = parser.parse_args(argv)
    package(args.skill, args.out, args.include_evals, args.extension)
    return 0


if __name__ == "__main__":
    sys.exit(main())
