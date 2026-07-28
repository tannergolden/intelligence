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

# --- the specification -------------------------------------------------------
# Verified at agentskills.io/specification: two required fields and four
# optional ones. Everything outside this set is a vendor extension.
SPEC_REQUIRED = ("name", "description")
SPEC_OPTIONAL = ("license", "compatibility", "metadata")

# Banned outright. The specification itself marks `allowed-tools` experimental,
# and it is a grant of tool access without a per-use prompt. A published skill
# may not hand itself permissions on somebody else's machine.
BANNED_KEYS = ("allowed-tools",)

# Read by Claude Code, ignored by Gemini CLI. Not forbidden, but a skill using
# one behaves differently per vendor, so it must SAY SO via `compatibility`.
# The dangerous case is not the optimisation that silently does nothing, it is
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
BODY_MAX_LINES = 500   # specification recommendation

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

# Built from CODEPOINTS so this file never contains one of the characters it
# rejects. Each family runs to its end: a range stopping one codepoint short
# of the hazard is the failure this rule exists to prevent.
INVISIBLE_FAMILIES = (
    (0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C), (0x115F, 0x1160),
    (0x17B4, 0x17B5), (0x180B, 0x180E), (0x200B, 0x200F), (0x202A, 0x202E),
    (0x2060, 0x2064), (0x2066, 0x2069), (0x3164, 0x3164), (0xFEFF, 0xFEFF),
    (0xFFA0, 0xFFA0), (0xE0000, 0xE007F),
)
INVISIBLE_RE = re.compile(
    "[" + "".join(
        chr(lo) if lo == hi else f"{chr(lo)}-{chr(hi)}"
        for lo, hi in INVISIBLE_FAMILIES
    ) + "]"
)

# Files a skill may hold without SKILL.md naming them. `evals/` is the eval
# harness's own directory: it is read by tooling, never by an agent, so it
# costs no context and needs no reference.
UNREFERENCED_OK_PREFIX = "evals/"

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
PATHLIKE_RE = re.compile(r"\A[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*\Z")


def parse_frontmatter(text: str):
    """Return (fields, body_offset, error).

    The flat scalar subset, and nothing more. A nested block, a multi-line
    string or an anchor is REFUSED with a readable message rather than
    half-read: this gate decides whether a skill ships, and a parser that
    silently drops what it does not understand would pass a skill whose real
    frontmatter says something else.
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

    fields = {}
    for n in range(1, close):
        raw = lines[n]
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:1] in (" ", "\t"):
            return None, 0, (
                f"line {n + 1} is indented, so this frontmatter is nested. This "
                "checker reads flat `key: value` pairs only, deliberately: it "
                "refuses rather than guessing at a shape it cannot verify. Keep "
                "the frontmatter flat.")
        if ":" not in raw:
            return None, 0, f"line {n + 1} is not a `key: value` pair: {raw!r}"
        key, _, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        # Inline lists and quoted scalars are both flat, so both are read.
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
    return fields, close + 1, None


def referenced_paths(body: str):
    """Every relative path the body points an agent at.

    Two syntaxes, because authors use both: a markdown link target, and a
    backticked path. A code span only counts when it actually looks like a
    path, so prose like `name` or `true` is not mistaken for a missing file.
    """
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
    return found


def scan_content(label: str, text: str, declared: bool, fail):
    """The rules that apply to any text an agent will load.

    RUN OVER EVERY MARKDOWN FILE IN THE SKILL, not only SKILL.md. A reference
    file is loaded into context the moment the body sends the agent to it, so
    an import token or an invisible character does identical damage there, and
    a rule scoped to the manifest alone would never see it.
    """
    for n, line in enumerate(text.split("\n"), 1):
        for match in AT_RE.finditer(line):
            fail(f"{label}:{n}: {match.group()!r} is a live import token in every "
                 "supported tool. It pulls a file into context, or leaves a "
                 "comment where your directive was. Rewrite the line.")
        for match in INVISIBLE_RE.finditer(line):
            fail(f"{label}:{n}: invisible character U+{ord(match.group()):04X} at "
                 f"column {match.start() + 1}. Nobody can catch this by reading "
                 "the diff, which is why it is checked here.")
        if not declared:
            hit = SHELL_INLINE_RE.search(line) or SHELL_FENCE_RE.search(line)
            if hit:
                fail(f"{label}:{n}: {hit.group().strip()!r} runs a shell command in "
                     "Claude Code and is literal text in Gemini CLI, so this "
                     "skill is grounded on one vendor and prints backticks on "
                     "the other. Declare it with `compatibility`, or remove it.")


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

    scan_content("SKILL.md", text, declared, fail)

    # --- tier C: the bundled files ------------------------------------------
    refs = referenced_paths(body)
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
                scan_content(item, path.read_text(encoding="utf-8"), declared, fail)
            except UnicodeDecodeError as exc:
                fail(f"{item!r} is not valid UTF-8: {exc}")

    if not (skill_dir / "evals" / "evals.json").is_file():
        warn("no evals/evals.json. Nothing here proves this skill beats its own "
             "baseline, so its quality is a claim rather than a measurement.")
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
SELF_TEST_REQUIRED = (
    "no SKILL.md",
    "does not exist",
    "never references it",
    "directory is",
    "live import token",
    "invisible character",
    "runs a shell command",
    "not permitted",
)


def build_hostile(root: Path):
    """Three deliberately broken skills, covering every asserted rule."""
    d = root / "no-manifest"
    d.mkdir()
    (d / "stray.md").write_text("No SKILL.md here, so nothing discovers this.\n",
                                encoding="utf-8")

    d = root / "wrong-name"
    d.mkdir()
    (d / "SKILL.md").write_text(
        "---\n"
        "name: not-the-directory-name\n"
        "description: Its name disagrees with its directory, it points at a file "
        "that does not exist, and it ships a file it never references.\n"
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
        "description: Carries one of each content hazard the checker must reject.\n"
        "allowed-tools: Read Grep\n"
        "---\n\n"
        "Ask @someone before running this.\n\n"
        "Diagnostic: !`echo hello`\n\n"
        "A zero width space splits these:\nsplit" + chr(0x200B) + "word\n",
        encoding="utf-8")


def self_test() -> int:
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        build_hostile(root)
        skills, problems, warnings = check_root(root)
        blob = " ".join(item["message"] for item in problems)

        print(f"self-test: {len(skills)} hostile skill(s), {len(problems)} error(s), "
              f"{len(warnings)} warning(s)")
        missing = [phrase for phrase in SELF_TEST_REQUIRED if phrase not in blob]
        for phrase in SELF_TEST_REQUIRED:
            print(f"  {'fired    ' if phrase not in missing else 'DID NOT  '} {phrase}")

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
        print("Every asserted rule still rejects what it exists to reject.")
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
