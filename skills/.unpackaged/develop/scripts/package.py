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
# THE EXTENSION, AND WHY IT IS `.zip` BY DEFAULT. A `.skill` file is a ZIP:
# same bytes, same folder-at-root layout, different name. Both names are in
# circulation and neither is a distinct format.
#
# The name still matters, because the web upload at Settings, Capabilities,
# Skills asks for a ZIP, and the standing advice for a file that arrives named
# `.skill` is to RENAME IT TO `.zip` BEFORE UPLOADING. Defaulting to `.skill`
# would therefore hand every user a file they must rename before the only
# install path that needs packaging at all accepts it. `--extension skill`
# writes the identical bytes under the other name for anyone distributing
# under that convention.
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
# OUTPUT CONTRACT: the archive path on stdout, everything else on stderr, so a
# caller can use `$(package.py ...)` directly without parsing around progress
# lines. Errors say what went wrong, what was expected, and what to try.
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

# PINNED, BECAUSE `zipfile` READS IT FROM THE HOST. `ZipInfo.__init__` sets
# this field to 0 on Windows and 3 everywhere else, so the same source packed
# on two machines produced two archives that differed in one byte per entry.
# Determinism that holds only on the platform you happened to test on is not
# determinism; it is a property nobody can check from the other side. 3 is
# Unix, which is what a skill archive's permissions mean.
FIXED_SYSTEM = 3


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

    # REFUSED BEFORE ANYTHING IS READ. `is_file()` and `read_bytes()` both
    # follow a symlink, so a link named `references/guide.md` used to put the
    # TARGET's content into the archive under that name. An archive is
    # published and downloaded, so that is any file readable where the build
    # runs, shipped to everyone, under a name that looks like documentation.
    # The checker refuses these too; this is the second lock, because the
    # packager is what actually writes the bytes.
    links = sorted(p.relative_to(skill_dir).as_posix()
                   for p in skill_dir.rglob("*") if p.is_symlink())
    if links:
        raise SystemExit(
            f"error: {skill_dir} contains symlinks and a skill may only ship "
            f"files it actually contains: {', '.join(links)}. Everything that "
            "reads these follows the link, so packing one writes the target's "
            "bytes into a published archive under the in-skill name. Replace "
            "each with the real file, or delete it.")

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
            info.create_system = FIXED_SYSTEM
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())

    # STRUCTURED RESULT TO STDOUT, EVERYTHING ELSE TO STDERR. An agent reading
    # this script's output should get the archive path and nothing it has to
    # filter progress messages out of.
    for path in members:
        print(f"  {folder}/{path.relative_to(skill_dir).as_posix()}", file=sys.stderr)
    if not include_evals and (skill_dir / "evals").is_dir():
        print("  (evals/ excluded: read by tooling, never by an agent)", file=sys.stderr)
    print(f"packed {len(members)} file(s)", file=sys.stderr)
    print(archive)
    return archive


# --- the self-test -----------------------------------------------------------
# THIS SCRIPT PRODUCES EVERY RELEASE ARTIFACT, and until this existed nothing
# checked what it produced. `make build` proved only that it did not crash.
# The three properties below are the ones a caller actually depends on, and
# each fails silently: a wrong archive root is rejected on upload with an
# error that does not say why, lost determinism makes every rebuild look
# changed, and a shipped evals/ inflates the upload with cases no agent reads.
SELF_TEST_SKILL = """---
name: fixture
description: Use this skill when the packager needs a known-good input to pack.
---

## Steps

1. Do the thing.
"""


def self_test() -> int:
    import contextlib
    import hashlib
    import io
    import tempfile

    # `package` prints the archive path to stdout, which is its contract for a
    # caller. Here that path is an intermediate, so it is swallowed and only
    # the invariant results reach the reader.
    def pack(*a, **kw):
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return package(*a, **kw)

    failures = []

    def check(label, ok, detail=""):
        print(f"  {'ok      ' if ok else 'FAILED  '} {label}")
        if not ok:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        src = root / "fixture"
        (src / "evals").mkdir(parents=True)
        (src / "SKILL.md").write_text(SELF_TEST_SKILL, encoding="utf-8")
        (src / "evals" / "evals.json").write_text("{}\n", encoding="utf-8")

        first = pack(src, root / "a", include_evals=False, extension="zip")
        with zipfile.ZipFile(first) as zf:
            names = zf.namelist()

        check("the skill FOLDER is the archive root, never SKILL.md",
              all(n.startswith("fixture/") for n in names), str(names))
        check("evals/ is excluded by default",
              not any(n.startswith("fixture/evals/") for n in names), str(names))

        second = pack(src, root / "b", include_evals=False, extension="zip")
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
        check("packing unchanged source twice is byte-identical",
              digest(first) == digest(second))

        # THE PREVIOUS CHECK CANNOT SEE THIS ONE. Two runs on the same machine
        # agree whatever the host-derived fields say; the question is whether
        # two DIFFERENT machines agree, and only reading the field answers it.
        with zipfile.ZipFile(first) as zf:
            systems = {i.create_system for i in zf.infolist()}
        check("every entry records a fixed creating system, not the host's",
              systems == {FIXED_SYSTEM}, str(systems))

        with_evals = pack(src, root / "c", include_evals=True, extension="zip")
        with zipfile.ZipFile(with_evals) as zf:
            check("--include-evals ships them",
                  any(n.startswith("fixture/evals/") for n in zf.namelist()))

        # A name that disagrees with its directory is found under one name and
        # invoked under another, so the packager must refuse rather than warn.
        wrong = root / "renamed"
        wrong.mkdir()
        (wrong / "SKILL.md").write_text(SELF_TEST_SKILL, encoding="utf-8")
        try:
            pack(wrong, root / "d", include_evals=False, extension="zip")
            check("a name/directory mismatch is refused", False, "it was packed")
        except SystemExit:
            check("a name/directory mismatch is refused", True)

        # A symlink is the one input where packing SUCCEEDS and the archive is
        # wrong: the entry carries the target's bytes under the in-skill name,
        # so nothing downstream can tell it was ever a link.
        linked = root / "linked"
        (linked / "references").mkdir(parents=True)
        (linked / "SKILL.md").write_text(
            SELF_TEST_SKILL.replace("name: fixture", "name: linked"),
            encoding="utf-8")
        (root / "outside.txt").write_text("Outside every skill.\n",
                                          encoding="utf-8")
        (linked / "references" / "guide.md").symlink_to(
            Path("..") / ".." / "outside.txt")
        try:
            pack(linked, root / "f", include_evals=False, extension="zip")
            check("a symlink out of the skill is refused", False,
                  "it was packed, and the archive carries the target's bytes")
        except SystemExit:
            check("a symlink out of the skill is refused", True)

        bare = root / "bare"
        bare.mkdir()
        try:
            pack(bare, root / "e", include_evals=False, extension="zip")
            check("a directory with no SKILL.md is refused", False, "it was packed")
        except SystemExit:
            check("a directory with no SKILL.md is refused", True)

    if failures:
        print(f"::error title=Package::{len(failures)} invariant(s) broken: {failures}")
        return 1
    print("Every packaging invariant holds.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack a skill directory into a ZIP archive with the folder at its root.")
    parser.add_argument("skill", nargs="?", type=Path, help="the skill directory to package")
    parser.add_argument("--out", type=Path, default=Path("dist"),
                        help="where to write the archive (default: dist)")
    parser.add_argument("--include-evals", action="store_true",
                        help="ship evals/ too. Off by default: no agent reads it.")
    parser.add_argument("--extension", choices=("zip", "skill"), default="zip",
                        help="archive extension. The bytes are a ZIP either way, "
                             "and every documented upload path asks for zip, so "
                             "that is the default.")
    parser.add_argument("--self-test", action="store_true",
                        help="Prove the packaging invariants still hold, using a "
                             "fixture skill built in a temporary directory.")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.skill is None:
        parser.error("a skill directory is required (or pass --self-test)")
    package(args.skill, args.out, args.include_evals, args.extension)
    return 0


if __name__ == "__main__":
    sys.exit(main())
