#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tanner Golden
# SPDX-License-Identifier: MIT
# =============================================================================
# check.py - the whole linter suite for the payload
# =============================================================================
# Runs twice on every sync: once here in CI against `payload/`, and again at
# the consumer against the staged bytes before a single one is written. The
# second run is the one that matters. A publisher can be wrong; a consumer
# repository that accepts the wrong bytes into an always-loaded instruction
# file has no other gate, because the delivery path has no pull request and
# therefore no human between the release and six working trees.
#
# ONE FILE, FIVE CHECKS, STANDARD LIBRARY ONLY. The runner image documents
# python3, and nothing else is guaranteed to exist at the consumer. Six
# modules with fixture directories were the earlier plan; a suite this small
# is easier to read whole than to navigate.
#
# WHAT IS DELIBERATELY NOT HERE: byte caps, directive caps and skill-catalog
# caps. Neither supported tool truncates (Anthropic loads CLAUDE.md "in full
# regardless of length"; Gemini has no context-file size limit), so the only
# honest budget is session cost, and no corpus exists to calibrate one
# against. The numbers are printed instead. See the advisory block below.
#
# Usage:  python3 check.py [DIR]          text output, exit 1 on any violation
#         python3 check.py [DIR] --json   the same result as machine input
# DIR defaults to `payload`.
# =============================================================================
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- 1. at-strict ------------------------------------------------------------
# The highest-value check in the system. Gemini CLI treats `@path` in a
# context file as an import: on any failure branch it substitutes an HTML
# comment OVER the token, silently deleting whatever directive the line
# carried, and on success it inlines the target recursively to depth 5 in a
# tree the publisher has never seen. Neither outcome is visible in a
# source-versus-output diff, because the bytes are identical and the damage
# happens at load time on someone else's machine.
#
# Strict means strict: inside inline code spans and inside fenced blocks too.
# Gemini's importer does its own backtick-region scan and a Python port of it
# was the single most intricate piece in the design; strict mode deletes that
# port and costs an author one comment on the rare line that needs an `@`.
#
# NEVER `\s` here. Python's `\s` also matches U+000B, U+000C and the Unicode
# spaces; Gemini's splitter uses exactly these four ASCII characters, so `\s`
# would reject tokens the vendor never treats as tokens.
# The hatch is deliberately one line wide: the comment must sit on the line
# IMMEDIATELY above the token, so an author grants an exemption to one line
# and never to a region. KNOWN HAZARD, measured not theorised: Prettier 3.8.1
# formatting markdown inserts a blank line after an HTML comment block, which
# separates the hatch from the line it protects and makes the routers fail
# this rule. That fails closed and is noisy rather than dangerous, but do not
# widen the hatch to absorb it; keep the formatter off these files instead.
AT = re.compile(r"(?:^|(?<=[ \t\n\r]))@[./A-Za-z][^ \t\n\r]*")
ALLOW_AT = "<!-- ai:allow-at -->"

# --- 2. shellbang ------------------------------------------------------------
# Anthropic's own skill importers refuse to auto-port these two spellings:
# inert in Gemini, LIVE in Claude Code. A file that ships them executes on
# one vendor and reads as documentation on the other.
#
# SCOPED TO EVERY FILE THAT CARRIES INSTRUCTIONS, not to `SKILL.md` alone. A
# rule that keys on a basename the v1 emit set does not contain protects
# nothing and fires only on its own fixture. The hazard is identical, and
# worse, in an always-loaded file: `` !`cmd` `` in a delivered CLAUDE.md is
# live on every Claude Code session in every consuming repository, and the
# same is true of consumer-authored local law, which is injected into
# AGENTS.md and lands in exactly the same place.
SHELLBANG = ("```!", "!`")
SHELLBANG_FILES = ("SKILL.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "agents-local.md")

# --- 3. invisible ------------------------------------------------------------
# Bidi controls, zero-width characters, format characters that render as
# nothing, and Unicode tag characters. The only defect class in always-loaded
# instruction text that a human provably cannot catch by reading the diff,
# which is why it is worth twenty lines. Written as escapes so this file never
# contains one of them.
#
# THE FAMILIES ARE COVERED WHOLE, deliberately. An earlier form of this rule
# stopped at U+200D and so missed U+200E and U+200F, the left-to-right and
# right-to-left marks, which are directional controls of the same class as the
# U+202A-U+202E it did catch and which split a word just as invisibly. A range
# that stops one codepoint short of the hazard is the failure mode this rule
# exists to prevent, so each family below runs to its end.
#
# KNOWN GAP, DELIBERATE: U+FE00-U+FE0F, the variation selectors, are NOT here.
# U+FE0F is how half the emoji in this ecosystem's own house style render, and
# it is at least as likely in a consumer's hand-written local law. A rule that
# rejects a warning sign in somebody's own repository law is a rule that gets
# switched off, and a switched-off rule catches nothing at all. Recorded in
# docs/Threat-Model.md beside homoglyphs rather than left to be rediscovered.
INVISIBLE = re.compile(
    "["
    "\u00ad"              # soft hyphen
    "\u034f"              # combining grapheme joiner
    "\u061c"             # arabic letter mark
    "\u115f\u1160"        # hangul choseong and jungseong fillers
    "\u17b4\u17b5"        # khmer inherent vowels, rendered as nothing
    "\u180b-\u180e"       # mongolian variation selectors and vowel separator
    "\u200b-\u200f"       # zero width space through right-to-left mark
    "\u202a-\u202e"       # bidi embedding and override controls
    "\u2060-\u2064"       # word joiner and the invisible operators
    "\u2066-\u2069"       # bidi isolates
    "\u3164"              # hangul filler
    "\ufeff"              # zero width no-break space, also a stray BOM
    "\uffa0"              # halfwidth hangul filler
    "\U000e0000-\U000e007f"  # unicode tag characters
    "]"
)

# --- 4. permalink ------------------------------------------------------------
PERMALINK = re.compile(
    r"github\.com/[^/ \t\n\r]+/[^/ \t\n\r]+/(?:blob|tree)/([^/ \t\n\r]+)/"
)
SHA40 = re.compile(r"\A[0-9a-f]{40}\Z")
# The wording is load-bearing. Without it the first author to hit this rule
# reaches for sed, SHA-pins every offender, and converts "may change
# silently" into "guaranteed stale forever".
PERMALINK_MSG = (
    "This link is a Tier 3 reference in a Tier 1 file. Agents do not follow "
    "it. Inline what matters or delete the link. SHA-pin only if a human "
    "reader genuinely needs that revision."
)

# --- 5. shape ----------------------------------------------------------------
# THE COMPLETE SET OF PATHS THIS PUBLISHER MAY DELIVER. Anything under
# `payload/` outside this set is a violation, which is what keeps the README's
# table of published paths true and keeps the uninstall a two-directory
# delete. Adding a third vendor is one entry here and a router beside it.
ALLOWED_FILES = frozenset({"AGENTS.md", "CLAUDE.md", "GEMINI.md"})
ALLOWED_DIRS = (".ai/", ".claude/", ".gemini/", ".agents/")

# The interpreter is the one dependency you cannot fix remotely. A shipped
# script that needs python3 on a machine without it fails on every session
# forever, and the consumer cannot be reached except by another sync. Scoped
# to every `.sh` that ships rather than to `.ai/hooks/` alone: `.ai/ai.sh`
# carries the same contract in its own header and had nothing enforcing it.
BANNED_IN_HOOKS = re.compile(r"\b(?:python3|jq|node|npx)\b")


def permitted(rel: Path) -> bool:
    posix = rel.as_posix()
    return posix in ALLOWED_FILES or posix.startswith(ALLOWED_DIRS)

# THE FROZEN COMMAND SET. Every hook command this publisher may ship, spelled
# byte for byte, and `sync.py` owns any entry in a consumer's settings file
# whose command begins with the same prefix.
#
# THIS ASSERTION IS THE WHOLE SAFETY MECHANISM FOR THE HOOK LAYER, and it
# exists because of an asymmetry that is easy to get backwards. Gemini CLI
# fingerprints a hook as `name:command` and warns when that changes. Claude
# Code has no fingerprint, no hash and no re-warning of any kind: its docs
# describe `.claude/settings.json` as watched and picked up automatically. So
# a publisher that renames a hook script on a later release executes new code
# in every already-trusted consumer with no prompt and no signal anywhere.
#
# The consequence is a rule, not a preference: ALL CHURN GOES INSIDE THE
# SCRIPTS. Those are in the lockfile with a sha256 and are diffable in the
# release notes, so the command surface a human reviewed once stays the
# command surface. Adding a hook means adding a line here, deliberately, in
# the same commit a reviewer reads.
#
# `bash "<path>"` rather than a bare path, because the transport that delivers
# these files probably cannot express mode 100755, so nothing may depend on
# the executable bit.
HOOK_PREFIX = 'bash "$CLAUDE_PROJECT_DIR/.ai/hooks/'
FROZEN_COMMANDS = {'bash "$CLAUDE_PROJECT_DIR/.ai/hooks/ai-context.sh"'}

# --- advisories, printed and never enforced ----------------------------------
# These are numbers, not gates, and they stay numbers until three things are
# true: the corpus exists, the counting rule is one written paragraph, and it
# has run against the real files once WITHOUT being tuned until it passed. A
# regex over MUST/NEVER/ALWAYS is satisfied by rephrasing rather than by
# removing a directive, so gating on it would buy compliance and not brevity.
# Longest alternative first, so MUST NOT counts once rather than twice.
DIRECTIVE = re.compile(r"\b(?:MUST NOT|DO NOT|MUST|NEVER|ALWAYS)\b")
ALWAYS_LOADED = ("AGENTS.md", "CLAUDE.md", "GEMINI.md")


def scan(rel: Path, text: str, allow_at: bool = True, emit_paths: bool = True) -> list[dict]:
    """Every per-line rule, in one pass over one file."""
    found = []

    def hit(line: int, rule: str, message: str) -> None:
        found.append({"path": str(rel), "line": line, "rule": rule, "message": message})

    # shape (d): THE EMIT SET IS AN ALLOWLIST, NOT A DENYLIST. Every path
    # under `payload/` is copied into a repository the publisher has never
    # seen, so the question is not "which paths are known to be dangerous"
    # but "which paths did anyone agree to receive". A denylist answers the
    # first and lets a `.vscode/tasks.json` with `runOn: folderOpen` through,
    # which is arbitrary execution the moment a developer opens the folder,
    # with no agent involved and no kill switch that reaches it: the sentinel
    # at `.ai/hooks/.disabled` disables things under `.ai/hooks/`.
    #
    # It is also the machine-checked form of two sentences this repository
    # already prints: the README's table of what is published, and the claim
    # that the uninstall is a two-directory delete. Adding a third vendor
    # stays a one-line change here, which is requirement 1's actual test.
    if emit_paths and not permitted(rel):
        hit(1, "shape", f"{rel.as_posix()} is not a path this publisher may deliver. "
            f"Files: {sorted(ALLOWED_FILES)}. Directories: {list(ALLOWED_DIRS)}. "
            "Everything delivered lives under those, so the uninstall stays a "
            "two-directory delete and the kill switch keeps covering everything "
            "that executes. Adding a path means adding it here, in the same commit "
            "a reviewer reads.")
        return found

    is_shipped_shell = rel.suffix == ".sh"
    allowed = False  # set by ALLOW_AT on the immediately preceding line
    for n, line in enumerate(text.split("\n"), 1):
        if not allowed:
            for m in AT.finditer(line):
                hit(n, "at-strict", f"live Gemini import token {m.group()!r}; " + (
                    f"rewrite the line, or put {ALLOW_AT} on the line directly "
                    "above it with no blank line between" if allow_at else
                    "the escape hatch is not available here. It exists so this "
                    "publisher's own routers can spell their import line, and "
                    "text from a repository the publisher has never seen may not "
                    "claim it: a live import token in injected law inlines an "
                    "arbitrary file into every agent session. Rewrite the line."))
        # With the hatch off, a line that spells it is just a comment.
        allowed = allow_at and line.strip() == ALLOW_AT

        for m in INVISIBLE.finditer(line):
            hit(n, "invisible", f"U+{ord(m.group()):04X} at column {m.start() + 1}")

        for m in PERMALINK.finditer(line):
            if not SHA40.match(m.group(1)):
                hit(n, "permalink", PERMALINK_MSG)

        if rel.name in SHELLBANG_FILES:
            for lit in SHELLBANG:
                if lit in line:
                    hit(n, "shellbang", f"{lit!r} is inert in Gemini and live in Claude Code")

        if is_shipped_shell:
            m = BANNED_IN_HOOKS.search(line)
            if m:
                hit(n, "shape", f"{m.group()} is not POSIX sh and may not exist "
                    "on the consumer's machine; every shipped script uses sh "
                    "builtins and POSIX utilities only")

    return found


def check_commands(rel: str, data: dict) -> list[dict]:
    """Assert the shipped hook commands are exactly the frozen set.

    Both directions matter and they fail differently. A command NOT on the
    list is new code arriving in an already-trusted consumer with no prompt.
    A frozen command MISSING is a hook this repository still documents,
    silently no longer wired, which nothing else here would notice: a hook
    that is not installed is invisible in headless mode.

    Takes the parsed object rather than the path: the caller has already
    parsed it once to check its top-level keys, and parsing a second time is
    how the two halves of this check end up disagreeing about the same file.
    """
    def hit(message: str) -> dict:
        return {"path": rel, "line": 1, "rule": "shape", "message": message}

    hooks = data.get("hooks")
    if hooks is not None and not isinstance(hooks, dict):
        return [hit(f"'hooks' is a {type(hooks).__name__}, not a JSON object")]

    shipped, malformed = set(), []
    for event, groups in (hooks or {}).items():
        if not isinstance(groups, list):
            malformed.append(f"hooks.{event} is not a list")
            continue
        for group in groups:
            entries = (group or {}).get("hooks") if isinstance(group, dict) else None
            if not isinstance(entries, list):
                malformed.append(f"a group under hooks.{event} has no 'hooks' list")
                continue
            for entry in entries:
                shipped.add(str((entry or {}).get("command", "")))

    found = [hit(m) for m in malformed]
    for command in sorted(shipped - FROZEN_COMMANDS):
        found.append(hit(
            f"hook command {command!r} is not in the frozen set. Claude Code has no "
            "fingerprint and no re-warning for a changed hook command, so a rename "
            "runs new code in every already-trusted consumer with no prompt. Put the "
            "change inside the script, which is in the lockfile with a digest, or add "
            "the new command to FROZEN_COMMANDS in check.py in the same commit."))
    for command in sorted(FROZEN_COMMANDS - shipped):
        found.append(hit(
            f"frozen hook command {command!r} is no longer wired by this file. A hook "
            "that is not installed is invisible in headless mode, so nothing "
            "downstream would report it. Remove it from FROZEN_COMMANDS if that is "
            "intended."))
    for command in sorted(shipped):
        if command and not command.startswith(HOOK_PREFIX):
            found.append(hit(
                f"hook command {command!r} does not begin with {HOOK_PREFIX!r}. That "
                "prefix is the ONLY thing that tells the merge which entries in a "
                "consumer's settings file are ours; an entry outside it can never be "
                "updated or retired."))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint the payload before it is published.")
    ap.add_argument("root", nargs="?", default="payload", help="directory to check")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    # Both flags say the same thing about the caller and neither one implies
    # the other, which is why they are two: the hostile fixtures are not the
    # emit set but DO exercise the hatch on purpose, and staged local law is
    # neither the emit set nor entitled to the hatch. Both default to the
    # strict answer, so the payload gets the full suite by forgetting rather
    # than by remembering.
    ap.add_argument("--no-hatch", dest="hatch", action="store_false",
                    help="Reject every import token, ignoring the escape hatch. For text "
                         "this publisher did not author, which may not claim it.")
    ap.add_argument("--any-path", dest="emit_paths", action="store_false",
                    help="Do not apply the emitted-path allowlist. For directories that "
                         "are not the emit set, such as the fixtures.")
    args = ap.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"{root}: shape: not a directory", file=sys.stderr)
        return 2

    every = sorted(p for p in root.rglob("*") if p.is_file())
    # .gitkeep holds an empty directory open in git. It is publisher
    # scaffolding and must never reach a consumer, so it is excluded from the
    # emit set here rather than filtered downstream.
    emit = [p for p in every if p.name != ".gitkeep"]

    violations: list[dict] = []
    for path in emit:
        rel = path.relative_to(root)
        try:
            text = path.read_bytes().decode("utf-8")
        except UnicodeDecodeError as exc:
            violations.append({"path": str(rel), "line": 1, "rule": "shape",
                               "message": f"not valid UTF-8: {exc}"})
            continue
        violations.extend(scan(rel, text, allow_at=args.hatch, emit_paths=args.emit_paths))

    # shape (a): a .gitkeep beside real files is dead scaffolding. It stops
    # holding anything open the moment a sibling exists, and a stale one is
    # how a .gitkeep eventually gets swept into an emit set by hand.
    for path in every:
        if path.name == ".gitkeep" and any(q.parent == path.parent for q in emit):
            violations.append({"path": str(path.relative_to(root)), "line": 1,
                               "rule": "shape", "message": "directory is no longer "
                               "empty; delete this scaffolding file"})

    # shape (b): .claude/settings.json is the consumer's only committed,
    # team-shared Claude configuration file. This publisher owns hook entries
    # in it and nothing else, and an invalid VALUE on a known key voids the
    # whole file silently, taking the consumer's own hooks down with it.
    settings = root / ".claude" / "settings.json"
    if settings.is_file():
        rel = str(settings.relative_to(root))
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except ValueError as exc:
            violations.append({"path": rel, "line": 1, "rule": "shape",
                               "message": f"not valid JSON: {exc}"})
        else:
            # Parsed once, shape asserted before anything reads into it. Every
            # other malformed-input path in this file produces a formatted
            # violation, and a linter that crashes on the input it exists to
            # judge has stopped being a linter.
            if not isinstance(data, dict):
                violations.append({"path": rel, "line": 1, "rule": "shape",
                                   "message": f"is a JSON {type(data).__name__}, not an object"})
            else:
                keys = list(data)
                if keys != ["hooks"]:
                    violations.append({"path": rel, "line": 1, "rule": "shape",
                                       "message": f"only top-level key may be 'hooks', found {keys}"})
                # shape (c): the frozen command strings. See FROZEN_COMMANDS.
                violations.extend(check_commands(rel, data))

    advisories = []
    for name in ALWAYS_LOADED:
        path = root / name
        if path.is_file():
            raw = path.read_bytes()
            count = len(DIRECTIVE.findall(raw.decode("utf-8", "replace")))
            advisories.append({"path": name, "bytes": len(raw), "directives": count})

    if args.json:
        print(json.dumps({"root": str(root), "ok": not violations,
                          "files": [str(p.relative_to(root)) for p in emit],
                          "violations": violations, "advisories": advisories}, indent=2))
    else:
        for v in violations:
            print(f"{root / v['path']}:{v['line']}: {v['rule']}: {v['message']}")
        for a in advisories:
            print(f"{root / a['path']}: bytes: {a['bytes']}, "
                  f"directives: {a['directives']} (advisory ceiling 25)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
