#!/usr/bin/env python3
# =============================================================================
# check-skills.py - validate skill directories against the Agent Skills spec
# =============================================================================
# An agent authoring a skill cannot check its own work: a badly shaped skill
# does not error, it simply never fires, or it fires on the wrong request, or
# it behaves differently on one vendor than another. Every failure mode here
# is silent. That is the whole reason this file exists.
#
# STANDARD LIBRARY ONLY. There is no YAML parser on the runner image, so the
# frontmatter reader below handles the flat scalar subset the spec actually
# requires and REFUSES anything else rather than guessing. A parser that
# guesses is worse than no parser, because it turns a loud failure into a
# quiet misreading.
#
# THE THREE TIERS THIS IS DEFENDING, because every rule maps to one of them:
#
#   A  name + description   loaded at startup for EVERY skill, used or not
#   B  SKILL.md body        loaded on invocation, persists the whole session
#   C  bundled files        loaded only when the body sends the agent there
#
# Tier A is the only cost you pay for a skill nobody uses, so it is capped.
# Tier B is never re-read and never freed, so it is capped. Tier C is free
# until used, which is why the rules push everything there.
#
# THE NEGATIVE TEST LIVES IN THIS FILE, under `--self-test`. A checker that
# has never rejected anything has never been tested, and one that silently
# stopped matching looks exactly like a clean repository. Keeping the hostile
# input beside the rules it exercises is what stops the two drifting apart, or
# one of them being deleted without the other.
#
# Usage:  python3 check-skills.py [DIR]          text output, exit 1 on failure
#         python3 check-skills.py [DIR] --json   the same result as machine input
#         python3 check-skills.py --self-test    prove every rule still fires
# =============================================================================
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- the specification -------------------------------------------------------
# Verified at agentskills.io/specification: two required fields and three
# optional ones. Everything outside this set is a vendor extension.
SPEC_REQUIRED = ("name", "description")
SPEC_OPTIONAL = ("license", "compatibility", "metadata")

# Banned outright. The specification itself marks `allowed-tools` experimental,
# and it is a grant of tool access without a per-use prompt. A published skill
# may not hand itself permissions on somebody else's machine.
BANNED_KEYS = ("allowed-tools",)

# Read by Claude Code, ignored by Gemini CLI. Not forbidden, but a skill using
# one behaves differently per vendor, so it must SAY SO via `compatibility`.
# The dangerous case is not the optimization that silently does nothing, it is
# the skill whose correctness depends on the key: one relying on
# `disable-model-invocation` to avoid auto-firing will auto-fire on Gemini.
VENDOR_KEYS = (
    "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
    "user-invocable", "disallowed-tools", "model", "effort", "context",
    "agent", "background", "hooks", "paths", "shell",
)

# `^[a-z0-9]+(-[a-z0-9]+)*$` enforces all four spec rules in one expression:
# lowercase alphanumerics and hyphens only, no leading hyphen, no trailing
# hyphen, and no consecutive hyphens. Writing them as four checks is how one
# of them ends up missing.
NAME_RE = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
NAME_MAX = 64
DESC_MAX = 1024        # specification hard limit
DESC_WARN = 500        # listing-budget pressure, see below
COMPAT_MAX = 500       # specification hard limit
BODY_MAX_LINES = 500   # specification recommendation
BODY_MAX_CHARS = 20000  # the same guidance's other half, ~5,000 tokens

# A description that never says WHEN to use the skill is the single most common
# authoring defect, and its failure is silent: the skill is simply never chosen,
# with no error and no log line. The documented pattern is an instruction to the
# agent ("Use this skill when the user ..."), not a label for the skill
# ("Processes CSV files"). Agents measurably under-trigger, so a description
# that reads as appropriately modest to a human is one that never fires.
#
# DELIBERATELY PERMISSIVE. Every word here introduces a condition, and this
# rule only warns. A false positive on a warning is worse than a miss, because
# it teaches authors that the checker's advice is noise and the next warning
# is the one they actually needed.
DESC_TRIGGER_RE = re.compile(r"\b(?:when|whenever|if)\b", re.IGNORECASE)

# Documented anti-patterns. Each occupies tier B in every session and changes
# no behavior, because it carries nothing the agent did not already have.
#
# BOUNDED AT BOTH ENDS. Without the trailing `\b`, "as appropriate" matches
# inside "appropriately", so a sentence about what reads as appropriately
# modest is reported as filler. The longer phrases come first: alternation is
# leftmost-first, so "follow best practices" must be tried before the
# "best practices" it contains, or the message names the wrong span.
VAGUE_PHRASES = (
    "follow best practices",
    "best practices",
    "handle errors appropriately",
    "as appropriate",
    "where appropriate",
    "use good judgement",
    "use good judgment",
)
VAGUE_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(p) for p in VAGUE_PHRASES) + r")\b",
    re.IGNORECASE,
)

# What counts as a citation rather than an instruction. A skill that teaches
# an anti-pattern has to be able to name it, and text inside backticks or
# quotation marks is being reported rather than told to the agent. Both are
# blanked before the filler rule runs.
QUOTED_RE = re.compile(r"\"[^\"\n]*\"")

# A path only true on the author's machine is an instruction that fails on
# everyone else's. Matched narrowly, as three unambiguous shapes: a drive
# letter, a UNC prefix, and a home directory. Never a lone backslash, which is
# an ordinary escape in markdown, and never a bare leading `/`, which is how
# repository-root paths and URLs are written.
ABS_PATH_RE = re.compile(r"(?:\A|[\s(`\"'])(?:[A-Za-z]:[\\/]|\\\\|/(?:home|Users)/)")

# Live shell in Claude Code, literal text everywhere else. Anthropic's own
# first-skill example uses the backtick form to inline `git diff` output, so
# this is a real feature and not a typo class; it is simply not portable.
#
# MATCHED AS A SHAPE, NOT AS A SUBSTRING, and the difference is not academic.
# A plain substring search fires on an ordinary code span holding a bang,
# which is how any document that DESCRIBES this syntax fails its own rule. The
# real spelling is a bang immediately followed by a backticked command, with
# the bang itself outside the code span, so the lookbehind is what tells the
# live form apart from a bang someone merely quoted.
SHELL_INLINE_RE = re.compile(r"(?<!`)!`[^`\n]+`")
SHELL_FENCE_RE = re.compile(r"\A\s*```!")

# A whitespace-bounded at-token is an import in all three supported tools. In
# a skill it either pulls an arbitrary file into context or, on a failed
# resolve, leaves a comment where a directive used to be. Never `\s` here:
# Python's `\s` also matches U+000B, U+000C and the Unicode spaces, which the
# vendors do not treat as token boundaries.
AT_RE = re.compile(r"(?:^|(?<=[ \t\n\r]))@[./A-Za-z][^ \t\n\r]*")

# Invisible characters live in `_charclasses.py`, imported by BOTH checkers so
# the class cannot drift. It used to be defined only here, which meant a hidden
# Unicode rule injected into AGENTS.md passed every documentation gate while
# the same bytes in a SKILL.md were caught.
from _charclasses import INVISIBLE_RE  # noqa: E402

# `skills/` is outside the documentation checker's scan entirely, because a
# SKILL.md needs the `---` frontmatter that specification forbids. So this is
# the only place a spelling variant in a skill is ever seen, and three arrived
# in reference files written after the last manual sweep.
from _spelling import BRITISH_SPELLINGS, british_hits  # noqa: E402

# Taken from the shared table rather than typed, so this file never
# contains the word it rejects. Same reason the invisible characters are
# built from codepoints: a rule whose own test data trips it cannot be
# tested in the repository that enforces it.
BRITISH_FIXTURE = sorted(BRITISH_SPELLINGS)[0]

# Files a skill may hold without SKILL.md naming them. `evals/` is the eval
# harness's own directory: it is read by tooling, never by an agent, so it
# costs no context and needs no reference.
UNREFERENCED_OK_PREFIX = "evals/"

# Generated or tool-owned paths that are not skill content at all. Without
# this, running the bundled script once leaves a `__pycache__` beside it and
# the next check fails on a file git already ignores. The packager already
# excludes exactly these, so the checker agreeing with it is the fix.
IGNORED_PARTS = ("__pycache__", ".git", ".DS_Store")
IGNORED_SUFFIXES = (".pyc", ".pyo")

FENCE_LINE_RE = re.compile(r"\A\s*`{3,}")


def strip_fences(text: str) -> str:
    """Blank every line inside a fenced code block, keeping line numbering."""
    out, inside = [], False
    for line in text.split("\n"):
        if FENCE_LINE_RE.match(line):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return "\n".join(out)


MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
PATHLIKE_RE = re.compile(r"\A[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*\Z")


# `description: |` and `description: >` are ordinary YAML and Anthropic ships
# skills using them. A parser refusing block scalars refuses valid skills, and
# this one is published as a composite action that runs against other people's
# repositories, so its refusals have to be right.
BLOCK_SCALAR_RE = re.compile(r"\A[|>][0-9+-]*\Z")

# `metadata` is the ONE field the specification defines as a mapping rather
# than a scalar: string keys to string values, no required keys. Everything
# else nested is still refused, because a shape this cannot verify is a shape
# it must not guess at.
MAPPING_KEYS = ("metadata",)


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str):
    """Return (fields, body_offset, error).

    Scalars, block scalars, and a mapping under `metadata`. Nothing else.
    Anything outside that is REFUSED with a readable message rather than
    half-read: this gate decides whether a skill ships, and a parser that
    silently drops what it does not understand would pass a skill whose real
    frontmatter says something else.

    WHAT THIS USED TO GET WRONG. It read flat `key: value` lines only, so it
    rejected two shapes the specification allows outright: a block-scalar
    `description`, which is how any description long enough to wrap gets
    written, and the `metadata` mapping. Both were reported as "this
    frontmatter is nested", which is a checker refusing conforming input, and
    that is worse than a checker missing something: it teaches its users that
    the specification is whatever the tool happens to accept.

    Folding for `>` is approximated by joining lines with a space. That is
    exact for the paragraph case every skill actually writes, and the value is
    used here only to measure length and to search for a trigger word.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, 0, "no frontmatter: the file must open with a '---' line"
    close = None
    for n in range(1, len(lines)):
        if lines[n].strip() == "---":
            close = n
            break
    if close is None:
        return None, 0, "frontmatter is never closed by a second '---' line"

    def indented_block(start: int):
        """Every blank or indented line from `start`, and the line after it."""
        end = start
        while end < close and (not lines[end].strip()
                               or lines[end][:1] in (" ", "\t")):
            end += 1
        return [line for line in lines[start:end] if line.strip()], end

    fields = {}
    n = 1
    while n < close:
        raw = lines[n]
        if not raw.strip() or raw.lstrip().startswith("#"):
            n += 1
            continue
        if raw[:1] in (" ", "\t"):
            return None, 0, (
                f"line {n + 1} is indented but no key opened a block above it. "
                "This checker reads scalars, block scalars, and a mapping "
                "under `metadata`. It refuses rather than guessing at a shape "
                "it cannot verify.")
        if ":" not in raw:
            return None, 0, f"line {n + 1} is not a `key: value` pair: {raw!r}"
        key, _, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        # A KEY WRITTEN TWICE IS NOT A STYLE PROBLEM. Every YAML reader keeps
        # the last one silently, so the field a reviewer read in the diff is
        # not the field the agent loads.
        if key in fields:
            return None, 0, (
                f"line {n + 1} sets `{key}` a second time. YAML readers keep "
                "the last one and report nothing, so the value a reviewer "
                "sees is not necessarily the value that loads.")
        n += 1

        if BLOCK_SCALAR_RE.match(value):
            block, n = indented_block(n)
            if not block:
                return None, 0, (
                    f"`{key}` opens a block scalar with nothing indented under it.")
            pad = min(len(line) - len(line.lstrip()) for line in block)
            body = [line[pad:] for line in block]
            fields[key] = "\n".join(body) if value[0] == "|" else " ".join(
                line.strip() for line in body)
            continue

        if value:
            fields[key] = _unquote(value)
            continue

        block, n = indented_block(n)
        if not block:
            fields[key] = ""
            continue
        if key not in MAPPING_KEYS:
            return None, 0, (
                f"`{key}` has a nested block under it. The specification "
                f"defines only {', '.join(f'`{k}`' for k in MAPPING_KEYS)} as "
                "a mapping; everything else is a scalar.")
        mapping = {}
        for line in block:
            if ":" not in line:
                return None, 0, (
                    f"`{key}` contains {line.strip()!r}, which is not a "
                    "`key: value` pair. This mapping is string to string.")
            sub_key, _, sub_value = line.partition(":")
            sub_key, sub_value = sub_key.strip(), sub_value.strip()
            if not sub_value:
                return None, 0, (
                    f"`{key}.{sub_key}` has no value. This mapping is string "
                    "to string, so a nested mapping or a list is not valid here.")
            mapping[sub_key] = _unquote(sub_value)
        fields[key] = mapping

    return fields, close + 1, None


# The directories the specification defines for bundled content. A path under
# one of these is a file the skill SHIPS; anything else backticked is prose
# about the world the skill runs in.
BUNDLE_DIRS = ("references/", "assets/", "scripts/", "evals/", "templates/")


def referenced_paths(body: str, skill_dir: Path):
    """Every relative path the body points an agent at.

    Two syntaxes, because authors use both: a markdown link target, and a
    backticked path. A code span only counts when it actually looks like a
    path, so prose like `name` or `true` is not mistaken for a missing file.

    A PATH-SHAPED TOKEN IS NOT AUTOMATICALLY A BUNDLED FILE. A skill routinely
    names files in the repository it RUNS IN: `README.md`, `AGENTS.md`, a
    `Makefile`. Those are the subject of the instruction, not cargo, and
    demanding the skill ship them is nonsense. So a token counts only when it
    sits under a bundle directory or when the skill actually ships a file by
    that name. The first keeps the missing-reference rule sharp where it
    matters, since `references/gone.md` still fails; the second keeps the
    unreferenced-file rule working for anything bundled at the top level.

    FENCED BLOCKS ARE SKIPPED. A skill that shows an author how to list their
    own resources writes the example in a fence, and that example names files
    it does not ship. Resolving it would fail every skill that teaches the
    syntax, which is the same defect as reading a bare `.zip` in prose as a
    filename. Note this does NOT relax the content-hazard rules: those still
    scan every line, because an at-token inside a fence still imports.
    """
    body = strip_fences(body)
    found = set()
    for match in MD_LINK_RE.finditer(body):
        target = match.group(1).split("#")[0]
        if target and "://" not in target and not target.startswith("#"):
            found.add(target)
    for match in CODE_SPAN_RE.finditer(body):
        token = match.group(1).strip()
        if not PATHLIKE_RE.match(token):
            continue
        # A NAME IS REQUIRED BEFORE THE EXTENSION. Without that character
        # class, a bare extension written in prose (`.zip`, `.md`, `.json`)
        # reads as a filename and gets reported as a missing reference, which
        # is exactly what happens to any skill that explains a file format.
        if "/" in token or re.search(r"[A-Za-z0-9_-]\.[A-Za-z0-9]{1,5}\Z", token):
            found.add(token)
    return {
        token for token in found
        if token.startswith(BUNDLE_DIRS) or (skill_dir / token).exists()
    }


def scan_content(label: str, text: str, declared: bool, fail, warn):
    """The rules that apply to any text an agent will load.

    RUN OVER EVERY MARKDOWN FILE IN THE SKILL, not only SKILL.md. A reference
    file is loaded into context the moment the body sends the agent to it, so
    an import token or an invisible character does identical damage there, and
    a rule scoped to the manifest alone would never see it.

    THE IMPORT RULE SKIPS CODE SPANS AND FENCES, because the vendor does.
    Claude Code's memory documentation states it outright: "Import parsing
    skips Markdown code spans and fenced code blocks", and gives backticks as
    the documented way to write a path without importing it. This rule used to
    scan every line on the reasoning that a fenced token still imports, which
    is not what the tool does. The cost was not theoretical: it failed every
    skill that teaches the import syntax, including ones the vendor publishes,
    and a gate that rejects the vendor's own examples is a gate its users turn
    off. Nothing else here relaxes; invisible characters and typography are
    still scanned on every line, fenced or not, because those are hazards to a
    reader rather than to a parser.
    """
    fenced = strip_fences(text).split("\n")
    for n, line in enumerate(text.split("\n"), 1):
        for match in AT_RE.finditer(CODE_SPAN_RE.sub(" ", fenced[n - 1])):
            fail(f"{label}:{n}: {match.group()!r} is a live import token in every "
                 "supported tool. It pulls a file into context, or leaves a "
                 "comment where your directive was. Put it in backticks, which "
                 "the vendors document as the way to write one literally, or "
                 "rewrite the line.")
        for match in INVISIBLE_RE.finditer(line):
            fail(f"{label}:{n}: invisible character U+{ord(match.group()):04X} at "
                 f"column {match.start() + 1}. Nobody can catch this by reading "
                 "the diff, which is why it is checked here.")
        for found, american in british_hits(line):
            fail(f"{label}:{n}: {found!r} is the British spelling; this "
                 f"repository is American throughout. Write {american!r}.")
        if not declared:
            hit = SHELL_INLINE_RE.search(line) or SHELL_FENCE_RE.search(line)
            if hit:
                fail(f"{label}:{n}: {hit.group().strip()!r} runs a shell command in "
                     "Claude Code and is literal text in Gemini CLI, so this "
                     "skill is grounded on one vendor and prints backticks on "
                     "the other. Declare it with `compatibility`, or remove it.")
        if ABS_PATH_RE.search(line):
            warn(f"{label}:{n}: this line carries a machine-specific path. A skill "
                 "runs on machines that are not the author's, so a path true only "
                 "on one of them is an instruction that fails everywhere else. "
                 "Use a path relative to the repository.")
        # Citations blanked first, so a document naming the anti-pattern is
        # not reported for using it.
        prose = QUOTED_RE.sub(" ", CODE_SPAN_RE.sub(" ", line))
        filler = VAGUE_RE.search(prose)
        if filler:
            warn(f"{label}:{n}: {filler.group()!r} tells the agent nothing it did "
                 "not already have, and it occupies context in every session that "
                 "loads this file. Name the practice you actually mean, or delete "
                 "the line.")


def check_evals(path: Path, skill_name: str, fail):
    """The eval file, against the schema the harness reads.

    An unreadable eval file is worse than no eval file. A missing one is
    visible, and the warning above says so; a malformed one looks like
    evidence right up until somebody tries to run it, which is usually the
    moment the skill is being changed and the evidence is most needed.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"evals/evals.json is not readable JSON: {exc}")
        return
    if not isinstance(data, dict):
        fail("evals/evals.json must hold an object with `skill_name` and `evals`.")
        return

    for key in sorted(data):
        if key not in ("skill_name", "evals") and not key.startswith("$"):
            fail(f"evals/evals.json has an unknown top-level key {key!r}. The "
                 "schema is `skill_name` and `evals`; keys beginning with `$` "
                 "are free for commentary.")

    declared_name = data.get("skill_name")
    if declared_name != skill_name:
        fail(f"evals/evals.json declares skill_name {declared_name!r} but this "
             f"skill is {skill_name!r}. A results file attributed to the wrong "
             "skill is measurement pointed at the wrong thing.")

    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        fail("evals/evals.json needs a non-empty `evals` array. An empty one "
             "reports success without running anything.")
        return

    seen = set()
    for index, case in enumerate(cases):
        where = f"evals/evals.json case {index + 1}"
        if not isinstance(case, dict):
            fail(f"{where} is not an object.")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, int):
            fail(f"{where} has no integer `id`.")
        elif case_id in seen:
            fail(f"{where} reuses id {case_id}. Results are reported by id, so "
                 "two cases sharing one are two results that cannot be told "
                 "apart.")
        else:
            seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            fail(f"{where} has no `prompt`. There is nothing to run.")
        # An assertion that cannot fail is not a test, and a case with none is
        # a transcript somebody has to read by hand.
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            fail(f"{where} has no `assertions`. Without a checkable claim the "
                 "case records what happened and grades nothing.")
        elif not all(isinstance(a, str) and a.strip() for a in assertions):
            fail(f"{where} has an empty or non-string assertion.")
        for key in sorted(case):
            if key not in ("id", "prompt", "expected_output", "files",
                           "assertions"):
                fail(f"{where} has an unknown key {key!r}.")


def check_skill(skill_dir: Path, root: Path):
    """Every rule, for one skill directory."""
    problems, warnings = [], []
    rel = skill_dir.relative_to(root).as_posix()

    def fail(msg):
        problems.append({"skill": rel, "level": "error", "message": msg})

    def warn(msg):
        warnings.append({"skill": rel, "level": "warning", "message": msg})

    manifest = skill_dir / "SKILL.md"
    if not manifest.is_file():
        fail("no SKILL.md. A directory without one is not a skill: nothing "
             "discovers it, and nothing reports that it was skipped.")
        return problems, warnings

    raw = manifest.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail("SKILL.md starts with a byte order mark.")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"SKILL.md is not valid UTF-8: {exc}")
        return problems, warnings
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        fail("SKILL.md must end with exactly one trailing newline.")

    fields, body_start, error = parse_frontmatter(text)
    if error:
        fail(f"SKILL.md {error}")
        return problems, warnings

    # --- tier A: the two required fields ------------------------------------
    for key in SPEC_REQUIRED:
        if not fields.get(key):
            fail(f"frontmatter has no non-empty `{key}`. The specification "
                 f"requires it, and without `description` the agent has "
                 f"nothing to match a request against.")

    name = fields.get("name", "")
    if name:
        if len(name) > NAME_MAX:
            fail(f"`name` is {len(name)} characters (limit {NAME_MAX}).")
        if not NAME_RE.match(name):
            fail(f"`name` {name!r} must be lowercase alphanumerics and hyphens, "
                 "with no leading, trailing or consecutive hyphen.")
        if name != skill_dir.name:
            fail(f"`name` is {name!r} but the directory is {skill_dir.name!r}. "
                 "The specification requires them to match, and they are read "
                 "by different things: discovery uses the directory, the listing "
                 "uses the field. When they disagree the skill is found under "
                 "one name and invoked under another.")

    desc = fields.get("description", "")
    if len(desc) > DESC_MAX:
        fail(f"`description` is {len(desc)} characters (limit {DESC_MAX}).")
    elif len(desc) > DESC_WARN:
        warn(f"`description` is {len(desc)} characters. It is loaded for every "
             "skill whether used or not, and when the listing overflows its "
             "budget the least-used skills lose their descriptions first. A "
             "long one here quietly silences another skill.")
    if desc and not DESC_TRIGGER_RE.search(desc):
        warn("`description` never says WHEN to use this skill. It is the only "
             "thing the agent matches a request against, so a description that "
             "labels the skill rather than triggering it produces the quietest "
             "failure there is: the skill is simply never chosen, with no error "
             "and no log line. Write it as an instruction, 'Use this skill when "
             "the user ...', and name the symptom someone would describe "
             "instead of the topic.")

    # --- the other spec fields ------------------------------------------------
    compat = fields.get("compatibility", "")
    if isinstance(compat, str) and len(compat) > COMPAT_MAX:
        fail(f"`compatibility` is {len(compat)} characters (limit {COMPAT_MAX}).")

    meta = fields.get("metadata")
    if meta is not None and not isinstance(meta, dict):
        fail("`metadata` is a mapping of string keys to string values, not a "
             "scalar. Written as one it is read as a mapping by anything "
             "following the specification and as a string by anything that "
             "is not, which is two different skills from one file.")

    # --- frontmatter policy --------------------------------------------------
    declared = bool(fields.get("compatibility"))
    for key in sorted(fields):
        if key in SPEC_REQUIRED or key in SPEC_OPTIONAL:
            continue
        if key in BANNED_KEYS:
            fail(f"`{key}` is not permitted. The specification marks it "
                 "experimental and it grants tool access without a per-use "
                 "prompt, on a machine that is not yours.")
        elif key in VENDOR_KEYS:
            if not declared:
                fail(f"`{key}` is read by Claude Code and ignored by Gemini CLI, "
                     "so this skill behaves differently per vendor. Declare that "
                     "with a `compatibility` field, or remove the key.")
        else:
            fail(f"`{key}` is not a field in the specification or in the "
                 "allowlist of known vendor extensions. Unknown keys are "
                 "dropped silently by some readers, so the skill would behave "
                 "differently depending on who loaded it.")

    # --- tier B: the body ----------------------------------------------------
    body = "\n".join(text.split("\n")[body_start:])
    body_lines = len(body.split("\n"))
    if body_lines > BODY_MAX_LINES:
        fail(f"the body is {body_lines} lines (limit {BODY_MAX_LINES}). It enters "
             "the conversation once and is never re-read or freed, so every line "
             "is a recurring cost for the whole session. Move detail into "
             "references/ and name it from here.")
    # Lines and characters are not the same cap, and a body can pass one while
    # failing the other: 300 long paragraphs cost more than 480 short steps.
    elif len(body) > BODY_MAX_CHARS:
        warn(f"the body is {len(body)} characters (guideline {BODY_MAX_CHARS}, "
             "roughly 5,000 tokens). It is under the line limit but not under "
             "the token one, which is the limit that actually costs the session. "
             "Move the longest section into references/.")

    scan_content("SKILL.md", text, declared, fail, warn)

    # --- tier C: the bundled files ------------------------------------------
    refs = referenced_paths(body, skill_dir)
    # A `license` may be an SPDX identifier or the name of a bundled file. In
    # the second case the frontmatter is what points at it, so the body never
    # mentions it and the unreferenced-file rule below would demand that a
    # skill delete its own license. A path that escapes the directory still
    # fails, because the loop that follows checks that before anything else.
    license_field = fields.get("license", "")
    if isinstance(license_field, str) and license_field and (
            skill_dir / license_field).is_file():
        refs = refs | {license_field}

    for ref in sorted(refs):
        if ref.startswith("/") or ".." in Path(ref).parts:
            fail(f"reference {ref!r} escapes the skill directory. A skill may "
                 "only point at files it ships.")
            continue
        if not (skill_dir / ref).exists():
            fail(f"reference {ref!r} does not exist. An agent told to read a "
                 "missing file wastes a turn and then improvises.")
        if ref.count("/") > 1:
            warn(f"reference {ref!r} is more than one level deep. The "
                 "specification asks for shallow references: a chain of files "
                 "pointing at files is a chain an agent abandons partway.")

    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(skill_dir).parts
        if any(part in IGNORED_PARTS for part in rel_parts):
            continue
        if path.suffix in IGNORED_SUFFIXES:
            continue
        item = path.relative_to(skill_dir).as_posix()
        if item == "SKILL.md" or item.startswith(UNREFERENCED_OK_PREFIX):
            continue
        if item not in refs:
            fail(f"{item!r} is in the skill directory but SKILL.md never "
                 "references it. Gemini CLI adds the folder structure to "
                 "context and grants the model access to the whole directory, "
                 "so an unreferenced file costs context and widens what the "
                 "user is asked to approve. Reference it or delete it.")
        if path.suffix == ".md":
            try:
                scan_content(item, path.read_text(encoding="utf-8"), declared,
                             fail, warn)
            except UnicodeDecodeError as exc:
                fail(f"{item!r} is not valid UTF-8: {exc}")

    evals = skill_dir / "evals" / "evals.json"
    if not evals.is_file():
        warn("no evals/evals.json. Nothing here proves this skill beats its own "
             "baseline, so its quality is a claim rather than a measurement.")
    else:
        check_evals(evals, name or skill_dir.name, fail)
    if (skill_dir / "scripts").is_dir():
        warn("this skill bundles scripts/, which is executable content in a "
             "repository whose other files are inert. Deliberate is fine; "
             "accidental is not.")

    return problems, warnings


def check_root(root: Path):
    skills = sorted(p for p in root.iterdir() if p.is_dir())
    problems, warnings = [], []
    for skill in skills:
        found, warned = check_skill(skill, root)
        problems.extend(found)
        warnings.extend(warned)
    return skills, problems, warnings


# --- the negative test -------------------------------------------------------
# Every rule that must still be capable of firing, each with hostile input
# written to trip it. The input is BUILT HERE rather than committed, so a rule
# and the thing that proves it works cannot be deleted separately, and the
# invisible character is constructed from its codepoint so this file never
# contains one.
SELF_TEST_ERRORS = (
    "no SKILL.md",
    "does not exist",
    "never references it",
    "directory is",
    "live import token",
    "invisible character",
    "runs a shell command",
    "not permitted",
    "reuses id",
    "no `assertions`",
    "declares skill_name",
    "unknown key",
    "a second time",
    f"limit {COMPAT_MAX}",
    "is a mapping of string keys",
    "British spelling",
)

# WARNINGS ARE ASSERTED TOO, and for the same reason as the errors. The rules
# that catch the quietest defects are advisory by design, since a skill with a
# label for a description still runs. A rule nobody proves is a rule that
# stops matching without anyone noticing, whichever level it reports at.
SELF_TEST_WARNINGS = (
    "never says WHEN",
    "machine-specific path",
    "already have",
)


def build_compliant(root: Path):
    """One correct skill, which the checker must NOT reject.

    Every other fixture here is hostile, and a checker tested only on hostile
    input can pass its whole suite while rejecting everything.

    IT IS DELIBERATELY THE AWKWARD KIND OF CORRECT, because every shape in it
    was rejected by some earlier version of this checker: a fenced example
    naming a file it does not ship, a block-scalar `description`, a `metadata`
    mapping, a `license` naming a bundled file the body never mentions, and
    both documented ways of writing an import token without importing it.
    """
    d = root / "compliant"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: compliant\n"
        "description: >\n"
        "  Use this skill when the user wants a correct skill to compare\n"
        "  against, or when checking that the checker still accepts one\n"
        "  written in the shapes the specification allows.\n"
        "license: LICENSE.txt\n"
        "metadata:\n"
        "  author: the specification\n"
        "  version: '1'\n"
        "---\n\n"
        "## Steps\n\n"
        "1. Do the thing.\n\n"
        "## Additional resources\n\n"
        "Check the repository's own `README.md` and `Makefile` first: those\n"
        "live in the tree this skill runs in, not in the skill.\n\n"
        "To name a file without importing it, write `@README` in backticks.\n\n"
        "List your own resources like this:\n\n"
        "```markdown\n"
        "- `references/not-shipped.md` - read this if X.\n"
        "@some/import.md\n"
        "```\n\n"
        "- `references/real.md` - read this when you need the real one.\n",
        encoding="utf-8")
    (d / "LICENSE.txt").write_text(
        "Named by the `license` field, never by the body.\n", encoding="utf-8")
    (d / "references").mkdir()
    (d / "references" / "real.md").write_text(
        "The reference this skill actually ships.\n", encoding="utf-8")


def build_hostile(root: Path):
    """Six deliberately broken skills, covering every asserted rule."""
    d = root / "no-manifest"
    d.mkdir()
    (d / "stray.md").write_text("No SKILL.md here, so nothing discovers this.\n",
                                encoding="utf-8")

    d = root / "wrong-name"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: not-the-directory-name\n"
        "description: Use this when its name disagrees with its directory, it "
        "points at a file that does not exist, and it ships one it never names.\n"
        "---\n\n"
        "## Additional resources\n\n"
        "- `references/absent.md` - deliberately missing.\n",
        encoding="utf-8")
    (d / "orphan.md").write_text("Never referenced from SKILL.md.\n", encoding="utf-8")

    d = root / "hazards"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: hazards\n"
        "description: Use this when you need one of each content hazard the "
        "checker must reject.\n"
        "allowed-tools: Read Grep\n"
        "---\n\n"
        "Ask @someone before running this.\n\n"
        "Diagnostic: !`echo hello`\n\n"
        f"A sentence using {BRITISH_FIXTURE}, on the wrong side of the "
        "Atlantic.\n\n"
        "A zero width space splits these:\nsplit" + chr(0x200B) + "word\n",
        encoding="utf-8")

    # The optional spec fields, both written as the wrong shape. Neither is a
    # parse error, so both have to survive to the field checks, which is why
    # they cannot share a directory with the duplicate key below.
    d = root / "bad-fields"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: bad-fields\n"
        "description: Use this when the optional specification fields are the "
        "wrong shape and nothing else is.\n"
        f"compatibility: {'x' * (COMPAT_MAX + 1)}\n"
        "metadata: not-a-mapping\n"
        "---\n\n"
        "Nothing else here is wrong.\n",
        encoding="utf-8")

    # A key set twice. Every YAML reader keeps the last one silently, so this
    # has to be a parse error rather than a field check: by the time the
    # fields dictionary exists, the evidence is gone.
    d = root / "duplicate-key"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: duplicate-key\n"
        "description: Use this when a reviewer reads one description and the "
        "agent loads another.\n"
        "description: Whatever the reader keeps.\n"
        "---\n\n"
        "The body is irrelevant: this never parses.\n",
        encoding="utf-8")

    # The quiet defects: a description that labels instead of triggering, a
    # path only the author has, filler that costs context and says nothing,
    # and an eval file that looks like evidence and cannot be run.
    d = root / "sloppy"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: sloppy\n"
        "description: Processes data files.\n"
        "---\n\n"
        "Read C:\\Users\\author\\notes.md first, then follow best practices.\n",
        encoding="utf-8")
    (d / "evals").mkdir()
    (d / "evals" / "evals.json").write_text(json.dumps({
        "skill_name": "a-different-skill",
        "evals": [
            {"id": 1, "prompt": "one", "assertions": ["checkable"]},
            {"id": 1, "prompt": "two", "assertions": []},
            {"id": 2, "prompt": "three", "assertions": ["ok"], "notes": "stray"},
        ],
    }, indent=2) + "\n", encoding="utf-8")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        build_compliant(root)
        build_hostile(root)
        skills, problems, warnings = check_root(root)

        print(f"self-test: {len(skills)} hostile skill(s), {len(problems)} error(s), "
              f"{len(warnings)} warning(s)")

        missing = []
        for label, phrases, items in (("error", SELF_TEST_ERRORS, problems),
                                      ("warning", SELF_TEST_WARNINGS, warnings)):
            blob = " ".join(item["message"] for item in items)
            for phrase in phrases:
                fired = phrase in blob
                if not fired:
                    missing.append(f"{label}: {phrase}")
                print(f"  {'fired    ' if fired else 'DID NOT  '} {label}: {phrase}")

        rejected = [p for p in problems if p["skill"] == "compliant"]
        if rejected:
            print("::error title=Check Skills::The COMPLIANT skill was rejected. A "
                  "gate that fails correct input trains everyone to ignore it.")
            for item in rejected:
                print(f"    {item['message']}")
            return 1
        if not problems:
            print("::error title=Check Skills::The hostile input was ACCEPTED. The "
                  "rules have stopped matching, which looks exactly like a clean "
                  "repository and is not one.")
            return 1
        if missing:
            print(f"::error title=Check Skills::these rules did not fire: {missing}. "
                  "Either a rule was weakened or its hostile input was changed, and "
                  "both are silent failures in production.")
            return 1
        print("Every asserted rule still rejects what it exists to reject, and "
              "the compliant skill still passes.")
        return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate skill directories.")
    parser.add_argument("root", nargs="?", default="skills")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true",
                        help="Prove every rule still rejects known-bad input, "
                             "using hostile skills built in a temporary directory.")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    root = Path(args.root)
    if not root.is_dir():
        print(f"{root}: not a directory", file=sys.stderr)
        return 2

    skills, problems, warnings = check_root(root)

    if args.json:
        print(json.dumps({"root": str(root), "skills": [p.name for p in skills],
                          "ok": not problems, "errors": problems,
                          "warnings": warnings}, indent=2))
    else:
        for item in problems + warnings:
            mark = "error" if item["level"] == "error" else "warning"
            print(f"{root}/{item['skill']}: {mark}: {item['message']}")
        print(f"{len(skills)} skill(s) checked, {len(problems)} error(s), "
              f"{len(warnings)} warning(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
