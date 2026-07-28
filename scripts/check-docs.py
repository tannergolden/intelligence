#!/usr/bin/env python3
# =============================================================================
# check-docs.py - audit every document against the published styling standard
# =============================================================================
# WHY THIS EXISTS. The shared CI workflow resolves its documentation gate as
# `make lint-docs` and NOTHING ELSE: unlike lint, test and build, that stage
# has no input override. A repository with no Makefile therefore reports the
# step as skipped and the run as green, which is what this repository did on
# every commit until this file was written. The rule that AGENTS.md calls the
# one broken most often was the one rule nothing checked.
#
# THE SPEC IS UPSTREAM, NOT HERE:
# tannergolden/standards/docs/technical/interface/Document-Styling-&-Formatting.md
#
# That document is followed BY LINK, never by copy, so this file encodes only
# the subset a machine can decide. Where it says a rule is aesthetic, the rule
# is a warning here. Where a rule protects meaning, it is an error.
#
# WHAT IS DELIBERATELY OUT OF SCOPE:
#
#   skills/**  Agent Skills carry `---` fenced frontmatter, which this
#              specification forbids for documentation. Both are correct in
#              their own domain, and check-skills.py owns that tree.
#
# STANDARD LIBRARY ONLY, matching check-skills.py. A hosted runner ships a
# documented base image and nothing else, so reaching for a package would be
# adding a dependency to a gate whose whole job is to be boring and present.
#
# Usage:  python3 scripts/check-docs.py [DIR]      text output, 1 on failure
#         python3 scripts/check-docs.py --json     the same result as data
#         python3 scripts/check-docs.py --self-test  prove the rules still fire
# =============================================================================
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- what the specification requires ----------------------------------------
FRONTMATTER_KEYS = ("title", "description", "tags", "category")
TAG_COUNT = 4                      # exactly four, no more and no fewer
TAG_RE = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MD041 = "<!-- markdownlint-disable MD041 -->"
DESC_AIM = 90                      # "aim for 90 characters or fewer"

# NO EXEMPTION FOR THE ROUTER FILES. `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`
# satisfy this specification in full, frontmatter included, and are checked
# like every other document. An earlier draft of this file exempted them on
# the assumption they carried no frontmatter; they do, and the exemption made
# the checker look for the MD041 line in the wrong place.

# Banned typography and invisible characters both live in `_charclasses.py`,
# imported by BOTH checkers so neither class can drift from the other. The
# invisible set was defined only in the skill checker until an audit found that
# a hidden Unicode rule injected into AGENTS.md passed every gate here on its
# way into every consuming repository.
from _charclasses import BANNED_CHARS, INVISIBLE_RE  # noqa: E402

# UTF-8 read as Latin-1. The specification calls this zero-tolerance, and it
# is invisible to a spell checker because the result is still valid Unicode.
# Also built from codepoints: the second class is a control range whose
# endpoints do not survive being typed into a source file.
MOJIBAKE_RE = re.compile(
    f"[{chr(0x00C2)}{chr(0x00C3)}][{chr(0x0080)}-{chr(0x00BF)}]"
)

# A prompt character copied with the command is a command that fails when
# pasted. Restricted to shell fences, and requires a space and something after
# it, so a redirect written on its own line is not mistaken for a prompt.
SHELL_LANGS = ("bash", "sh", "shell", "zsh", "console")
PROMPT_RE = re.compile(r"\A\s*[$%>]\s+\S")

FENCE_MAX_LINES = 20               # beyond this the spec requires <details>

HEADING_RE = re.compile(r"\A#\s+(.+?)\s*\Z")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"\A\s*(`{3,})\s*([A-Za-z0-9_+-]*)")

# --- this repository's own product budget -----------------------------------
# NOT part of the styling standard, and deliberately kept beside it anyway,
# because this is the only checker that already reads these files.
#
# These three are DELIVERED into other people's repositories and read by an
# agent in EVERY session there, whether or not anyone invokes anything.
# Nothing else in this tree has that property: a SKILL.md costs a session, a
# document costs whoever opens it, and these cost everyone, always.
#
# The checker caps a SKILL.md at 500 lines for being expensive. Until this
# existed it left the far more expensive file unbounded, which is the wrong
# way round.
#
# THE NUMBERS ARE A DECISION, NOT A DISCOVERY. Raising one has to be a commit
# somebody reviews, which is what turns "every addition names a subtraction"
# from an aspiration into a gate. The warning fires early so the conversation
# happens before the ceiling, not at it.
DELIVERED_BUDGETS = {
    "AGENTS.md": 14000,   # the law. Every rule paid in every session, everywhere
    "CLAUDE.md": 3000,    # an envelope. Growth here means law is leaking in
    "GEMINI.md": 3000,    # the same
}
DELIVERED_WARN_AT = 0.80

# The hooks are delivered too, and they are priced differently from a file.
# A document costs whoever opens it and the law costs one load per session;
# a hook that fires on every prompt is charged AGAIN ON EVERY TURN, which
# makes its output the highest-frequency cost anything here produces. Claude
# Code does not truncate that stream, so nothing but this stops a helpful
# paragraph being added and silently billed forever.
#
# Measured against a fixture rather than read from the source, because what
# costs context is what the script PRINTS, not what it contains.
# The budget is a PER-TURN figure. Claude Code appends hook output as a new
# context block on every turn rather than refreshing one in place, so a session
# pays budget x turns. It is also not a truncation guard: output passes through
# verbatim up to 10,000 characters and is replaced by a preview beyond that.
HOOK_SCRIPTS = (".claude/hooks/skill-router.sh", ".gemini/hooks/skill-router.sh")
HOOK_OUTPUT_BUDGET = 256          # bytes, against the fixture below
HOOK_FIXTURE_SKILLS = ("alpha", "bravo", "charlie")
# EACH DIRECTORY CONTRIBUTES A UNIQUE NAME, plus one they all share. An earlier
# fixture put the same three skills everywhere, so a router that stopped
# reading a directory still produced a complete list and the gate saw nothing.
# `shared` is present in all three, so a dedup regression doubles it.
HOOK_FIXTURE_LAYOUT = {
    ".claude/skills": ("alpha", "shared"),
    ".gemini/skills": ("bravo", "shared"),
    ".agents/skills": ("charlie", "shared"),
}
# What each router must name, given that layout. A router reading fewer
# directories than its vendor does fails on the missing name.
HOOK_EXPECTED = {
    ".claude/hooks/skill-router.sh": ("alpha", "shared"),
    ".gemini/hooks/skill-router.sh": ("bravo", "charlie", "shared"),
}
# Gemini parses hook stdout as JSON and degrades anything else to a message
# shown to the user and never to the model. Shape is therefore correctness,
# not neatness, and it is the check whose absence let an inert hook ship.
HOOK_JSON_REQUIRED = (".gemini/hooks/skill-router.sh",)

# `_` as a space is rejected across the WHOLE tree, not just docs. These are
# the names a platform or a language fixes, which cannot move at all.
UNDERSCORE_OK = {
    "pull_request_template.md", "CODE_OF_CONDUCT.md", "ISSUE_TEMPLATE",
    "FUNDING.yml", "SECURITY_CONTACTS.md",
}


def parse_frontmatter(text: str):
    """Return (fields, lines_consumed, error) for the HTML-comment form.

    The `---` fenced form is refused rather than parsed. It is not a near
    miss: GitHub renders a `---` block as a visible table above the document,
    so the first thing every reader sees is machine bookkeeping. Reading it
    anyway would let the shape this specification exists to prevent pass.
    """
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        return None, 0, (
            "frontmatter is fenced with `---`. GitHub renders that as a "
            "visible metadata table above the document; the HTML-comment form "
            "is invisible when rendered and identical when parsed.")
    if not lines or lines[0].strip() != "<!--":
        return None, 0, (
            "the file must open with `<!--` alone on line 1, beginning the "
            "hidden frontmatter comment.")
    close = None
    for n in range(1, len(lines)):
        if lines[n].strip() == "-->":
            close = n
            break
        if "-->" in lines[n]:
            return None, 0, (
                f"line {n + 1} closes the frontmatter comment early. Nothing "
                "legitimate in a title, description or tag list contains "
                "`-->`.")
    if close is None:
        return None, 0, "the frontmatter comment is never closed by a `-->` line."

    fields = {}
    for n in range(1, close):
        raw = lines[n]
        if not raw.strip():
            continue
        if ":" not in raw:
            return None, 0, f"frontmatter line {n + 1} is not `key: value`: {raw!r}"
        key, _, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
    return fields, close + 1, None


def check_file(path: Path, root: Path, taglines, footers, fail, warn):
    """Every per-document rule."""
    rel = path.relative_to(root).as_posix()
    raw = path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        fail(rel, "starts with a byte order mark. The specification requires "
                  "UTF-8 without one.")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(rel, f"is not valid UTF-8: {exc}")
        return
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        fail(rel, "must end with exactly one trailing newline.")

    lines = text.split("\n")

    # --- typography, everywhere in the file ---------------------------------
    for n, line in enumerate(lines, 1):
        for char, name in BANNED_CHARS.items():
            if char in line:
                fail(rel, f"line {n}: {name}. Use a comma, a colon, "
                          "parentheses, or a spaced hyphen.")
        if MOJIBAKE_RE.search(line):
            fail(rel, f"line {n}: mojibake. This is UTF-8 that was read as "
                      "Latin-1 somewhere upstream; repair it at the source.")
        for m in INVISIBLE_RE.finditer(line):
            fail(rel, f"line {n}: invisible character U+{ord(m.group()):04X} at "
                      f"column {m.start() + 1}. Nobody catches this by reading "
                      "the diff, which is the point of using it: a rule hidden "
                      "this way is delivered to every repository and read by "
                      "every agent while being invisible to every reviewer.")

    # --- frontmatter ---------------------------------------------------------
    fields, body_start, error = parse_frontmatter(text)
    if error:
        fail(rel, error)
        return
    for key in FRONTMATTER_KEYS:
        if not fields.get(key):
            fail(rel, f"frontmatter has no non-empty `{key}`.")
    tags = fields.get("tags", "")
    if tags:
        if not (tags.startswith("[") and tags.endswith("]")):
            fail(rel, "`tags` must be an inline list: `[one, two, three, four]`.")
        else:
            items = [t.strip() for t in tags[1:-1].split(",") if t.strip()]
            if len(items) != TAG_COUNT:
                fail(rel, f"`tags` has {len(items)} entries and the "
                          f"specification requires exactly {TAG_COUNT}. Four "
                          "places a document on several axes and still reads "
                          "as a classification rather than a keyword dump.")
            for item in items:
                if not TAG_RE.match(item):
                    fail(rel, f"tag {item!r} is not kebab-case.")
        # The frontmatter description carries no length limit: the
        # specification asks only that it be one specific sentence, never
        # empty and never generic. The 90-character aim belongs to the
        # RENDERED header description below, which is read as a masthead.

    # --- the MD041 suppression ----------------------------------------------
    want = body_start
    while want < len(lines) and not lines[want].strip():
        want += 1
    if want >= len(lines) or lines[want].strip() != MD041:
        fail(rel, f"the first line after the frontmatter must be `{MD041}`. "
                  "Without it, the centered `div` "
                  "before the Heading 1 trips MD041 in any repository that runs "
                  "markdownlint.")

    # --- the centered header block -------------------------------------------
    head = "\n".join(lines[:60])
    if '<div align="center">' not in head:
        fail(rel, 'the header must open a `<div align="center">` block.')
    if "<a name=\"top\"></a>" not in text:
        fail(rel, 'no `<a name="top"></a>` anchor, so every "Back to Top" link '
                  "in the file goes nowhere.")

    h1s = [(n, m.group(1)) for n, m in
           ((n, HEADING_RE.match(ln)) for n, ln in enumerate(lines, 1)) if m]
    if not h1s:
        fail(rel, "has no Heading 1.")
    else:
        n, title = h1s[0]
        if len(h1s) > 1:
            warn(rel, f"has {len(h1s)} Heading 1s. A document has one title.")
        words = re.findall(r"[A-Za-z]{2,}", title)
        if words and not all(w.isupper() for w in words):
            warn(rel, f"line {n}: the Heading 1 {title!r} is not fully capped. "
                      "The specification caps display titles; this one is "
                      "aesthetic rather than load-bearing.")
        if re.search(r"\bAND\b", title):
            warn(rel, f"line {n}: the Heading 1 spells out `AND`; the "
                      "conjunction in a title is `&`.")

    # --- description and tagline, in that order, both bold and italic --------
    desc_line = tag_line = None
    for n, line in enumerate(lines[:60], 1):
        s = line.strip()
        if desc_line is None and re.fullmatch(r"\*\*.+\*\*", s):
            desc_line = (n, s[2:-2])
        elif desc_line is not None and tag_line is None and re.fullmatch(r"_.+_", s):
            tag_line = (n, s[1:-1])
            break
    if desc_line is None:
        fail(rel, "the header carries no bold one-line description.")
    if tag_line is None:
        fail(rel, "the header carries no italic tagline.")
    if desc_line and tag_line:
        if len(desc_line[1]) > DESC_AIM:
            warn(rel, f"line {desc_line[0]}: the header description is "
                      f"{len(desc_line[1])} characters. The specification aims "
                      f"for {DESC_AIM} or fewer, because a masthead that wraps "
                      "pushes the tagline down and reads as a paragraph the eye "
                      "skips on its way to the content.")
        if len(desc_line[1]) <= len(tag_line[1]):
            warn(rel, "the header description is no longer than the tagline "
                      "beneath it; the specification asks for the reverse.")
        key = tag_line[1].strip().lower()
        taglines.setdefault(key, []).append(rel)

    # --- footer --------------------------------------------------------------
    tail = lines[-25:]
    if not any("[↑ Back to Top](#top)" in ln for ln in tail):
        fail(rel, "the footer carries no `[↑ Back to Top](#top)` link.")
    phrase = None
    for line in reversed(tail):
        s = line.strip()
        if re.fullmatch(r"\*\*.+\*\*", s):
            phrase = s[2:-2]
            break
    if phrase is None:
        fail(rel, "the footer carries no bold closing phrase.")
    else:
        footers.setdefault(phrase.strip().lower(), []).append(rel)

    # --- fences, prompts, and progressive disclosure -------------------------
    # `fenced` records every line inside a code block, because a document
    # DEMONSTRATING markdown is not a document making a claim. A fenced
    # `[link](./nowhere.md)` is an illustration and must not be resolved, in
    # exactly the way a fenced example of any other syntax is not executed.
    #
    # The strict rules deliberately do NOT consult it. An at-token, an
    # invisible character and a banned dash are hazards wherever they sit: the
    # vendors scan text rather than parse markdown, so a fence protects
    # nothing, and the styling standard bans those characters outright.
    fenced = set()
    depth = 0            # <details> nesting
    fence = None         # (start_line, language, opening_ticks, in_details)
    for n, line in enumerate(lines, 1):
        if fence is not None:
            fenced.add(n)
        if fence is None:
            if "<details" in line:
                depth += 1
            elif "</details>" in line:
                depth = max(0, depth - 1)
            m = FENCE_RE.match(line)
            if m:
                fence = (n, m.group(2), m.group(1), depth > 0)
                if not m.group(2):
                    fail(rel, f"line {n}: this code fence declares no language. "
                              "Every fence names one, so it highlights and so a "
                              "reader knows what they are looking at.")
            continue
        if line.strip().startswith(fence[2]) and not FENCE_RE.match(line).group(2):
            length = n - fence[0] - 1
            if length > FENCE_MAX_LINES and not fence[3]:
                warn(rel, f"line {fence[0]}: this fence is {length} lines. The "
                          f"specification wraps anything over {FENCE_MAX_LINES} "
                          "in a `<details>` block to prevent scrolling fatigue.")
            fence = None
            continue
        if fence[1] in SHELL_LANGS and PROMPT_RE.match(line):
            fail(rel, f"line {n}: a shell block carries a leading prompt "
                      "character. Copying it pastes the prompt too, and the "
                      "command fails.")
    if fence is not None:
        fail(rel, f"line {fence[0]}: this code fence is never closed.")

    # --- accessibility and links --------------------------------------------
    for n, line in enumerate(lines, 1):
        if n in fenced:
            continue
        for m in IMAGE_RE.finditer(line):
            if not m.group(1).strip():
                fail(rel, f"line {n}: an image has empty alt text. Every image, "
                          "badges included, carries a description.")
        for m in LINK_RE.finditer(line):
            target = m.group(1)
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                fail(rel, f"line {n}: relative link {target!r} does not resolve.")


def check_names(root: Path, fail, vendored=frozenset()):
    """`_` as a space, across the whole tree rather than only docs/."""
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(f"{v}/") or rel == v for v in vendored):
            continue
        name = path.name
        if name in UNDERSCORE_OK or name.startswith("_") or "_" not in name:
            continue
        # A Python module cannot contain a hyphen and must stay importable.
        if path.suffix == ".py":
            continue
        fail(path.relative_to(root).as_posix(),
             "has `_` as a space in its name. The specification rejects that "
             "across the entire tree; the exceptions are names a platform or a "
             "language fixes.")


def submodule_paths(root: Path):
    """Every path `.gitmodules` declares, so vendored trees are skipped.

    A submodule is another repository's content pinned into this one. Its
    documents answer to ITS specification and its own gates, and linting them
    here would turn a change nobody in this repository made into a red build
    nobody in this repository can fix. Read from `.gitmodules` rather than
    hardcoded, so adding a submodule needs no edit here.
    """
    manifest = root / ".gitmodules"
    if not manifest.is_file():
        return set()
    found = set()
    for line in manifest.read_text(encoding="utf-8").split("\n"):
        key, _, value = line.partition("=")
        if key.strip() == "path" and value.strip():
            found.add(value.strip().strip("/"))
    return found


def check_delivered_budget(root: Path, fail, warn):
    """Size ceilings on the files this repository delivers to others.

    A file read in every session of every consuming repository is the one
    place where a paragraph nobody needed is charged to everybody, forever.
    Published research on agent memory found instructions that only ever grow
    make agents measurably WORSE at following them, so this is a correctness
    gate wearing a size gate's clothes.
    """
    for name, budget in sorted(DELIVERED_BUDGETS.items()):
        path = root / name
        if not path.is_file():
            continue
        size = path.stat().st_size
        if size > budget:
            fail(name, f"is {size} bytes against a budget of {budget}. This file "
                       "is read in every session of every repository that "
                       "receives it, so a line added here is paid by everyone "
                       "forever. Remove something, move it into a document only "
                       f"read when needed, or raise the budget in {__file__.rsplit('/', 1)[-1]} "
                       "as a deliberate commit somebody reviews.")
        elif size > budget * DELIVERED_WARN_AT:
            warn(name, f"is {size} bytes, past {int(DELIVERED_WARN_AT * 100)}% of "
                       f"its {budget}-byte budget. The next addition is the one "
                       "that should name what it replaces.")


def check_hooks(root: Path, fail, warn):
    """Syntax-check every delivered hook, and price what it prints.

    Two failures this catches, both silent otherwise. A hook with a syntax
    error does not stop the session, it just never contributes anything, so
    the router looks installed and does nothing. And a hook that grew a
    paragraph of advice costs that paragraph on every turn of every session
    in every repository that received it.
    """
    import subprocess
    import tempfile

    for rel in HOOK_SCRIPTS:
        path = root / rel
        if not path.is_file():
            continue

        syntax = subprocess.run(["sh", "-n", str(path)],
                                capture_output=True, text=True)
        if syntax.returncode != 0:
            fail(rel, f"is not valid POSIX shell: {syntax.stderr.strip()}. A "
                      "broken hook does not stop a session, it silently "
                      "contributes nothing, so it looks installed and is not.")
            continue

        with tempfile.TemporaryDirectory() as scratch:
            for base, names in HOOK_FIXTURE_LAYOUT.items():
                for name in names:
                    d = Path(scratch) / base / name
                    d.mkdir(parents=True, exist_ok=True)
                    (d / "SKILL.md").write_text("---\n", encoding="utf-8")
            env = {"PATH": "/usr/bin:/bin",
                   "CLAUDE_PROJECT_DIR": scratch, "GEMINI_PROJECT_DIR": scratch}
            run = subprocess.run(["sh", str(path)], capture_output=True,
                                 text=True, env=env)
            size = len(run.stdout.encode("utf-8"))

        if run.returncode != 0:
            fail(rel, f"exited {run.returncode} with skills installed. A "
                      "non-zero hook is not a no-op to every vendor: some read "
                      "the code as a decision about the turn.")
        if run.stderr.strip():
            fail(rel, f"wrote to stderr: {run.stderr.strip()[:120]!r}. A hook "
                      "runs on every prompt, so anything on stderr is noise in "
                      "the operator's terminal on every prompt.")

        # Exactly the names this vendor discovers, each exactly once. Catches a
        # dropped discovery directory (a name goes missing) and a dedup
        # regression (`shared` appears twice).
        for name in HOOK_EXPECTED.get(rel, ()):
            seen = run.stdout.count(name)
            if seen != 1:
                fail(rel, f"names the fixture skill {name!r} {seen} times, "
                          "expected exactly once. A missing name means a "
                          "discovery directory is not being read; a repeated "
                          "one means the dedup has regressed.")

        if rel in HOOK_JSON_REQUIRED:
            try:
                doc = json.loads(run.stdout)
                ctx = doc["hookSpecificOutput"]["additionalContext"]
                if not isinstance(ctx, str) or not ctx.strip():
                    raise ValueError("additionalContext is empty")
            except Exception as exc:
                fail(rel, f"does not emit the required JSON envelope ({exc}). "
                          "Gemini CLI parses hook stdout as JSON and converts "
                          "anything else into a message shown to the user and "
                          "never to the model, so plain text here is a hook "
                          "that runs, passes every other check, and injects "
                          "nothing at all.")

        if size > HOOK_OUTPUT_BUDGET:
            fail(rel, f"prints {size} bytes for {len(HOOK_FIXTURE_SKILLS)} "
                      f"skills, against a budget of {HOOK_OUTPUT_BUDGET}. This "
                      "runs on EVERY prompt, so that is charged again on every "
                      "turn of every session. Name the skills and stop; the "
                      "model already holds their descriptions.")

        # A router that says nothing when skills ARE present is the failure
        # that looks exactly like a working one.
        if size == 0:
            fail(rel, "printed nothing with skills installed, so it is doing "
                      "no work at all. A silent router is indistinguishable "
                      "from a correct one until someone checks.")


def check_root(root: Path, docs_only: bool = False):
    problems, warnings = [], []

    def fail(rel, msg):
        problems.append({"file": rel, "level": "error", "message": msg})

    def warn(rel, msg):
        warnings.append({"file": rel, "level": "warning", "message": msg})

    taglines, footers = {}, {}
    vendored = submodule_paths(root)
    files = []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        parts = rel.parts
        if ".git" in parts or "skills" in parts:
            continue
        if any(rel.as_posix().startswith(f"{v}/") for v in vendored):
            continue
        files.append(path)
    for path in files:
        check_file(path, root, taglines, footers, fail, warn)

    # Uniqueness is a whole-tree property, so it cannot be decided per file.
    # REPORTED AGAINST EVERY OWNER. Blaming whichever file sorts first would
    # be arbitrary, and it would put an error on a document that is otherwise
    # correct because of a copy made somewhere else. Both ends of a collision
    # need changing anyway: only the author knows which one owns the phrase.
    for kind, table in (("tagline", taglines), ("footer phrase", footers)):
        for value, owners in sorted(table.items()):
            if len(owners) > 1:
                for owner in owners:
                    others = [o for o in owners if o != owner]
                    fail(owner, f"this {kind} is shared with {', '.join(others)}. "
                                "The specification requires it to be unique to "
                                "the document: a repeated one is a closing "
                                "argument that argues nothing.")
    if not docs_only:
        check_names(root, fail, vendored)
        check_delivered_budget(root, fail, warn)
        check_hooks(root, fail, warn)
    return files, problems, warnings


# --- the negative test -------------------------------------------------------
# Same reasoning as check-skills.py: a checker that has never rejected
# anything has never been tested, and one that quietly stopped matching looks
# exactly like a clean repository.
SELF_TEST_ERRORS = (
    "fenced with `---`",
    "exactly 4",
    "markdownlint-disable MD041",
    "em dash",
    "invisible character",
    "declares no language",
    "leading prompt character",
    "empty alt text",
    "does not resolve",
    "Back to Top",
    "is shared with",
)
SELF_TEST_WARNINGS = (
    "not fully capped",
    "spells out `AND`",
)
SELF_TEST_BUDGET = "against a budget of"

GOOD = """<!--
title: '📝 GOOD'
description: 'A document that satisfies every rule this checker enforces.'
tags: [one, two, three, four]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📝 GOOD

<a name="top"></a>

**A document that satisfies every rule this checker enforces here.**

_Correct by construction._

</div>

---

## 💡 Body

```bash
make lint-docs
```

A fenced example names files it does not ship, and must not be resolved:

```markdown
[a guide](./Does-Not-Exist.md)
![](./no-alt.png)
```

---

<div align="center">

**Nothing to report.**

[↑ Back to Top](#top)

</div>
"""

# The em dash is BUILT FROM ITS CODEPOINT so this file never contains the
# character it rejects, exactly as check-skills.py builds its invisible
# characters. A rule whose own test data trips it is a rule that cannot be
# tested in the repository that enforces it.
BROKEN_BODY = """
<div align="center">

# 💥 Bad Document AND Worse

**Broken in every way the checker is supposed to notice{EM}including this.**

A rule hidden from the reviewer: split{ZWSP}word.

_Broken by construction._

</div>

```
undeclared fence language
```

```bash
$ make lint
```

![](./missing.png)

[nowhere](./absent.md)

<div align="center">

**Everything to report.**

</div>
""".replace("{EM}", chr(0x2014)).replace("{ZWSP}", chr(0x200B))

BAD = "---\ntitle: 'BAD'\ntags: [only, three, tags]\n-->\n" + BROKEN_BODY

PAST_THE_DOOR = (
    "<!--\ntitle: 'WORSE'\ndescription: 'Past the front door, and broken "
    "everywhere after it.'\ntags: [only, three, tags]\ncategory: docs\n-->\n"
    + BROKEN_BODY
)


def self_test() -> int:
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        (root / "Good.md").write_text(GOOD, encoding="utf-8")
        (root / "Bad.md").write_text(BAD, encoding="utf-8")
        # The `---` frontmatter check returns early, so Bad.md never reaches
        # the rules after it. Worse.md and Worst.md get past the front door to
        # exercise them, and share a tagline and footer with each other so the
        # uniqueness rule is proved WITHOUT implicating the compliant document.
        (root / "Worse.md").write_text(PAST_THE_DOOR, encoding="utf-8")
        (root / "Worst.md").write_text(
            PAST_THE_DOOR.replace("'WORSE'", "'WORST'"), encoding="utf-8")

        files, problems, warnings = check_root(root, docs_only=True)
        print(f"self-test: {len(files)} document(s), {len(problems)} error(s), "
              f"{len(warnings)} warning(s)")

        missing = []
        for label, phrases, items in (("error", SELF_TEST_ERRORS, problems),
                                      ("warning", SELF_TEST_WARNINGS, warnings)):
            blob = " ".join(i["message"] for i in items)
            for phrase in phrases:
                fired = phrase in blob
                if not fired:
                    missing.append(f"{label}: {phrase}")
                print(f"  {'fired    ' if fired else 'DID NOT  '} {label}: {phrase}")

        # The budget gate runs over delivered files rather than documents, so
        # it needs its own hostile input: a law that outgrew its allowance.
        budget_hits = []
        (root / "AGENTS.md").write_text(
            "x" * (DELIVERED_BUDGETS["AGENTS.md"] + 1), encoding="utf-8")
        check_delivered_budget(root, lambda f, m: budget_hits.append(m),
                               lambda f, m: None)
        fired = any(SELF_TEST_BUDGET in m for m in budget_hits)
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: {SELF_TEST_BUDGET}")
        if not fired:
            missing.append(f"error: {SELF_TEST_BUDGET}")
        (root / "AGENTS.md").unlink()

        if any(p["file"] == "Good.md" for p in problems):
            print("::error title=Check Docs::The compliant document was REJECTED. "
                  "A gate that fails correct input trains everyone to ignore it.")
            for p in problems:
                if p["file"] == "Good.md":
                    print(f"    {p['message']}")
            return 1
        if missing:
            print(f"::error title=Check Docs::these rules did not fire: {missing}.")
            return 1
        print("Every asserted rule still rejects what it exists to reject, and "
              "the compliant document still passes.")
        return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit documents against the "
                                                 "published styling standard.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true",
                        help="Prove every rule still rejects known-bad input.")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.root)
    if not root.is_dir():
        print(f"{root}: not a directory", file=sys.stderr)
        return 2

    files, problems, warnings = check_root(root)

    if args.json:
        print(json.dumps({"root": str(root), "files": len(files),
                          "ok": not problems, "errors": problems,
                          "warnings": warnings}, indent=2))
    else:
        for item in problems + warnings:
            print(f"{item['file']}: {item['level']}: {item['message']}")
        print(f"{len(files)} document(s) checked, {len(problems)} error(s), "
              f"{len(warnings)} warning(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
