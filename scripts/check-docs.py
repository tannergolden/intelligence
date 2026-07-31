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
from urllib.parse import unquote

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
from _spelling import BRITISH_SPELLINGS, british_hits  # noqa: E402

# Taken from the shared table rather than typed, for the same reason the
# em dash below is built from its codepoint: this file must not contain
# what it rejects, or it fails its own repository on the first run.
BRITISH_FIXTURE = sorted(BRITISH_SPELLINGS)[0]

# UTF-8 read as Latin-1. The specification calls this zero-tolerance, and it
# is invisible to a spell checker because the result is still valid Unicode.
# Also built from codepoints: the second class is a control range whose
# endpoints do not survive being typed into a source file.
# TWO BRANCHES, BECAUSE ONE ONLY SAW HALF THE PROBLEM. The first is the
# two-byte case: a UTF-8 lead byte of 0xC2 or 0xC3, which is everything
# encoding U+0080 to U+00FF. Three- and four-byte sequences decode to a
# LOWERCASE letter outside that pair, so the mojibake most likely to arrive
# here, a smart quote or a dash or an ellipsis, matched nothing. The second
# branch is any C1 control, which every three- and four-byte sequence carries
# as a continuation byte and which never appears in legitimate text.
MOJIBAKE_RE = re.compile(
    f"[{chr(0x00C2)}{chr(0x00C3)}][{chr(0x0080)}-{chr(0x00BF)}]"
    f"|[{chr(0x0080)}-{chr(0x009F)}]"
)

# A prompt character copied with the command is a command that fails when
# pasted. Restricted to shell fences, and requires a space and something after
# it, so a redirect written on its own line is not mistaken for a prompt.
SHELL_LANGS = ("bash", "sh", "shell", "zsh", "console")
PROMPT_RE = re.compile(r"\A\s*[$%>]\s+\S")

FENCE_MAX_LINES = 20               # beyond this the spec requires <details>

HEADING_RE = re.compile(r"\A#\s+(.+?)\s*\Z")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
# EVERY FORM CommonMark DEFINES, because the resolver is what protects
# cross-document navigation and three of them used to opt out of it silently.
# The old pattern required the closing paren to follow the target with no
# whitespace, so an optional link TITLE, which is ordinary Markdown, made the
# whole link invisible. Reference-style links and raw HTML `href` were outside
# it entirely. An author adding a hover title to a link removed it from the
# gate, and the link then rotted with nothing reporting it.
LINK_RE = re.compile(r"""\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+['"(][^)]*)?\s*\)""")
# A reference DEFINITION is where the path actually sits, so resolving the
# definition covers every usage of it without matching usages at all.
REF_DEF_RE = re.compile(r"""\A {0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?""")
HTML_HREF_RE = re.compile(r"""<(?:a|img)\s[^>]*(?:href|src)=["']([^"']+)["']""")
# BOTH FENCE CHARACTERS. CommonMark defines `~~~` alongside ``` ``` ```, and a
# checker that knows only one treats the contents of the other as live prose:
# its links get resolved, its example images get an alt-text failure, and its
# headings get counted. Probed before it was fixed, and a `~~~` block was
# completely invisible to every rule below.
FENCE_RE = re.compile(r"\A\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)")

# A span is markup a reader sees literally, so a document naming an
# anti-pattern is not a document committing one. Used only by the rules about
# rendered MEANING. The rules about bytes, typography and invisible characters,
# still read every column of every line.
CODE_SPAN_RE = re.compile(r"`[^`\n]+`")

# Two more places a tag NAME appears without being a tag. An HTML comment is
# the note somebody leaves while working toward compliance, and link text is
# prose that happens to be linked. Both used to open a `<details>` block that
# never closed, which silenced the long-fence warning for the rest of the file.
# Single-line forms only, which is what both are written as here.
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")
LINK_TEXT_RE = re.compile(r"\[([^\]]*)\]\(")

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

# The one line each envelope exists to carry, and the file it carries it to.
# `CLAUDE.md` and `GEMINI.md` hold no law of their own; this token is the whole
# of their job, and until it was checked the budget rule measured their size
# while nothing measured whether they still did anything.
ENVELOPES = ("CLAUDE.md", "GEMINI.md")
LAW = "AGENTS.md"
IMPORT_LINE = "@./AGENTS.md"

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
# THE THREE-SKILL FIXTURE PROVES A NUMBER, NOT A BOUND. Three names fit the
# budget and forty do not: both routers printed over 900 bytes for forty, on
# every turn, forever, in a repository this publisher never sees. So the
# ceiling is asserted against a fixture large enough that only a router which
# actually truncates can pass, which is the difference between measuring the
# cost and bounding it.
HOOK_FIXTURE_MANY = 40

# The registration beside each router, and nothing here used to read it.
# `check_hooks` executes the script by hardcoded path, which proves the script
# and says nothing about whether anything runs it: a command pointing at a
# renamed file ships a router that is installed, silent, and indistinguishable
# from one with no skills to name. That is the same shape as the Gemini hook
# that printed prose and injected nothing while passing every gate.
#
# THE SECOND FAILURE IS WORSE THAN THE FIRST. The sync stub writes these two
# files ONCE and never again, on purpose, because a settings file is where a
# consuming team's own `permissions.deny` and hooks live. So unlike the
# routers, which update on every sync, a bad one that lands cannot be
# corrected by any publisher-side action. Moving the tag back does not reach
# it. That makes these the only delivered files with no recall at all, which
# is the argument for checking them hardest.
DELIVERED_SETTINGS = {
    ".claude/settings.json": ("UserPromptSubmit", ".claude/hooks/skill-router.sh"),
    ".gemini/settings.json": ("BeforeAgent", ".gemini/hooks/skill-router.sh"),
}
# Keys a DELIVERED settings file may never carry, each already excluded in
# prose. `permissions` belongs to the receiving repository, and Installation
# says so where it explains why the sync will not overwrite these files;
# shipping one would preempt a decision that is not this publisher's to make,
# permanently. MCP configuration is named in Scope & Boundaries as something
# that never lives here. A gate beats a rule: it fires every time.
SETTINGS_BANNED_KEYS = ("permissions", "mcpServers", "mcp")

# --- documented numbers, asserted against the constants they describe -------
# WHY THIS EXISTS. An audit found NINE stated facts that no longer matched the
# code: a budget, two counts of checks, a count of failure modes, a count of
# hostile fixtures, an archive extension, and a rule the definitive list never
# mentioned. Every one was written correctly and then went stale in silence,
# because prose and the constant it describes live in different files and
# nothing compared them. Nine in a repository three days old is a rate, not an
# accident, and this repository's product IS its documentation.
#
# A GATE BEATS A RULE, which is the argument the law makes for itself and the
# argument the upstream-proposal reference makes for preferring a check. So the
# numbers are read out of the documents and compared to the values they claim
# to describe, and a mismatch is an error naming both sides.
#
# WHAT THIS CANNOT DO: it checks numbers, not meaning. A sentence that is
# wrong about what a check does still passes. That is the honest boundary,
# and it is where a machine stops being able to decide.
NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
}


def _sibling(name: str):
    """Load a sibling checker so its constants can be compared to the prose.

    A hyphen makes the module unimportable by name, and the point of this rule
    is that the number and the sentence live in different files, so reaching
    across is the job rather than a shortcut.
    """
    import importlib.util
    path = Path(__file__).resolve().parent / name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _count_in(path: Path, pattern: str) -> int:
    return len(re.findall(pattern, path.read_text(encoding="utf-8")))


def documented_numbers(root: Path):
    """Every (document, pattern, expected) triple, resolved against the code.

    Built lazily rather than as a module constant, because half of these read
    another file and one counts call sites in a third.
    """
    skills = _sibling("check-skills.py")
    packager = root / "skills/.unpackaged/develop/scripts/package.py"
    # READ FROM THE TREE BEING CHECKED rather than from this file's own path,
    # so the gate describes the repository it was pointed at.
    checks = root / "scripts" / "check-docs.py"
    hook_block = ""
    if checks.is_file():
        # ANCHORED ON A REAL DEFINITION, at column 0, running to the next one.
        # A plain substring search found this rule's OWN mention of the
        # function name, which sits above the function, and measured the thirty
        # characters between two string literals instead. The gate reported
        # zero and was describing itself.
        found = re.search(r"^def check_hooks\b.*?(?=^def )",
                          checks.read_text(encoding="utf-8"), re.M | re.S)
        hook_block = found.group() if found else ""

    items = [
        ("docs/Checks-&-Gates.md",
         r"\| `AGENTS\.md` \| ([\d,]+) bytes", DELIVERED_BUDGETS["AGENTS.md"],
         "the AGENTS.md byte budget"),
        ("docs/Checks-&-Gates.md",
         r"\| `CLAUDE\.md` \| ([\d,]+) bytes", DELIVERED_BUDGETS["CLAUDE.md"],
         "the CLAUDE.md byte budget"),
        ("docs/Checks-&-Gates.md",
         r"a warning fires at ([\d]+)%", int(DELIVERED_WARN_AT * 100),
         "the budget warning threshold"),
        ("docs/Checks-&-Gates.md",
         r"Output under ([\d,]+) bytes", HOOK_OUTPUT_BUDGET,
         "the hook output budget"),
        ("docs/Checks-&-Gates.md",
         r"against a \*\*(\w+)\*\*-skill fixture", HOOK_FIXTURE_MANY,
         "the large hook fixture"),
        ("docs/Skill-Authoring.md",
         r"1 to ([\d,]+) characters, matching", skills.NAME_MAX,
         "the skill name limit"),
        ("docs/Skill-Authoring.md",
         r"1 to ([\d,]+) characters, saying what", skills.DESC_MAX,
         "the description limit"),
        ("docs/Skill-Authoring.md",
         r"`compatibility` \(1 to ([\d,]+) characters\)", skills.COMPAT_MAX,
         "the compatibility limit"),
        ("docs/Skill-Authoring.md",
         r"Under ([\d,]+) lines \*\*and\*\*", skills.BODY_MAX_LINES,
         "the skill body line cap"),
        ("docs/Skill-Authoring.md",
         r"a description over ([\d,]+) characters", skills.DESC_WARN,
         "the description warning threshold"),
    ]
    if packager.is_file():
        # COUNTED FROM WHAT IT PRINTS, not from how its source is written. Two
        # of its invariants come from one call site in a loop, so counting
        # `check(` in the source gives a number no reader would recognize.
        import subprocess
        run = subprocess.run(["python3", str(packager), "--self-test"],
                             capture_output=True, text=True)
        printed = len(re.findall(r"^  ok ", run.stdout, re.MULTILINE))
        if printed:
            items.append(("docs/Checks-&-Gates.md",
                          r"(\w+) invariants, each of which", printed,
                          "the packaging invariant count"))
    if hook_block:
        items.append(("docs/Checks-&-Gates.md", r"(\w+) checks bound it",
                      len(re.findall(r"fail\(rel,", hook_block)),
                      "the hook gate check count"))
    return items


def check_documented_numbers(root: Path, fail):
    """Compare every stated number to the constant it describes."""
    for rel, pattern, expected, label in documented_numbers(root):
        path = root / rel
        if not path.is_file():
            continue
        found = re.search(pattern, path.read_text(encoding="utf-8"))
        if not found:
            fail(rel, f"no longer states {label}, which this checker asserts "
                      f"against the code. Either the sentence was reworded past "
                      f"the pattern in check-docs.py, or the claim was dropped. "
                      f"A number nothing compares is a number that goes stale.")
            continue
        raw = found.group(1).replace(",", "").strip().lower()
        actual = NUMBER_WORDS.get(raw, None)
        if actual is None:
            try:
                actual = int(raw)
            except ValueError:
                fail(rel, f"states {label} as {found.group(1)!r}, which is "
                          "neither a number nor a number word.")
                continue
        if actual != expected:
            fail(rel, f"says {label} is {found.group(1)!r}, and the code says "
                      f"{expected}. One of them is wrong, and prose is the one "
                      "that goes stale silently: nothing else in this "
                      "repository compares the two.")


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
        # A KEY WRITTEN TWICE IS NOT A STYLE PROBLEM, and the skill checker
        # has refused it from the day it was written. This parser kept the
        # last one silently, on the only three files in this repository that
        # are copied verbatim into somebody else's tree, so the description a
        # reviewer read in the diff was not necessarily the one anything
        # loaded. Same hazard, same reasoning, one checker apart.
        if key in fields:
            return None, 0, (
                f"frontmatter line {n + 1} sets `{key}` a second time. The "
                "last one wins silently, so the value a reviewer sees is not "
                "necessarily the value that is read.")
        fields[key] = value
    return fields, close + 1, None


def scan_fences(rel: str, lines, fail, warn):
    """Map every fenced line, and report what only a fence scan can see.

    RUN FIRST, because three later rules are wrong without it. A `# TITLE` in
    a fenced markdown example is not a second Heading 1. An `![](x.png)` shown
    as an example of bad alt text is not bad alt text. A `[link](nowhere.md)`
    in an example resolves to nothing on purpose. Each of those was a real
    false positive, reproduced before this was written.

    `<details>` IS COUNTED ONLY AS MARKUP. It used to be counted anywhere the
    string appeared, so a document that merely mentioned `<details>` in prose
    opened a block that never closed, and every long fence after it stopped
    being reported. That is the worst kind of gate defect: it goes quiet, and
    quiet is indistinguishable from clean.
    """
    fenced = set()
    depth = 0            # <details> nesting
    fence = None         # (start_line, language, opening_run, in_details)
    for n, line in enumerate(lines, 1):
        if fence is not None:
            fenced.add(n)
        if fence is None:
            # A MENTION IS NOT AN ELEMENT, and there are three ways to
            # mention one. Code spans were blanked from the start; an HTML
            # comment and link text were not, so `<!-- TODO: wrap this in a
            # <details> block later -->` opened a block that never closed and
            # every fence below it stopped being measured. The gate went quiet,
            # and quiet is indistinguishable from clean.
            markup = HTML_COMMENT_RE.sub(" ", line)
            markup = LINK_TEXT_RE.sub("(", markup)
            markup = CODE_SPAN_RE.sub(" ", markup)
            depth += markup.count("<details")
            depth = max(0, depth - markup.count("</details>"))
            m = FENCE_RE.match(line)
            if m:
                fence = (n, m.group(2), m.group(1), depth > 0)
                if not m.group(2):
                    fail(rel, f"line {n}: this code fence declares no language. "
                              "Every fence names one, so it highlights and so a "
                              "reader knows what they are looking at.")
            continue
        m = FENCE_RE.match(line)
        # A closer uses the SAME character, runs at least as long, and carries
        # no info string. Matching on "starts with the opener" alone closed a
        # ``` block on a ~~~ line and vice versa.
        if (m and m.group(1)[0] == fence[2][0]
                and len(m.group(1)) >= len(fence[2]) and not m.group(2)):
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
    return fenced


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
        # SPANS MOJIBAKE ALREADY OWNS ARE NOT REPORTED TWICE. A C1 control is
        # both an invisible character and the tell-tale of a mangled encoding,
        # and only one of those two messages carries the right instruction:
        # removing one byte of a three-byte sequence leaves the other two.
        mangled = {i for m in MOJIBAKE_RE.finditer(line)
                   for i in range(m.start(), m.end())}
        for m in INVISIBLE_RE.finditer(line):
            if m.start() in mangled:
                continue
            fail(rel, f"line {n}: invisible character U+{ord(m.group()):04X} at "
                      f"column {m.start() + 1}. Nobody catches this by reading "
                      "the diff, which is the point of using it: a rule hidden "
                      "this way is delivered to every repository and read by "
                      "every agent while being invisible to every reviewer.")
        for found, american in british_hits(CODE_SPAN_RE.sub(" ", line)):
            fail(rel, f"line {n}: {found!r} is the British spelling; this "
                      f"repository is American throughout, matching the "
                      f"publisher it is built alongside. Write {american!r}.")

    # --- the fence map, built BEFORE anything consults it --------------------
    fenced = scan_fences(rel, lines, fail, warn)

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

    # Fenced lines are excluded: a markdown example showing `# TITLE` is not a
    # second Heading 1, and when the example came first it was the one whose
    # capitalization got graded.
    h1s = [(n, m.group(1)) for n, m in
           ((n, HEADING_RE.match(ln)) for n, ln in enumerate(lines, 1)
            if n not in fenced) if m]
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
    # The footer is the LAST centered block, not the last 25 lines. A fixed
    # window is a guess about how long a footer is, and it reads whatever
    # content happens to sit above one that runs long.
    # FENCED LINES EXCLUDED, for the same reason the Heading 1 scan excludes
    # them twenty lines above. A document that TEACHES this format has to be
    # able to show a footer, and a fenced example is not a second footer: it
    # used to become the last centered block, so the window slid past the real
    # one and both footer rules stopped seeing it. A correct document was then
    # reported as having no back-to-top link and no closing phrase, and the
    # placeholder inside the example was what got recorded in the uniqueness
    # registry. Third instance of this bug class in this function, after the
    # fenced `# TITLE` and the `<details>` named in prose.
    centered = [i for i, ln in enumerate(lines)
                if '<div align="center">' in ln and (i + 1) not in fenced]
    tail = lines[centered[-1]:] if len(centered) > 1 else lines[-25:]
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

    # --- accessibility and links --------------------------------------------
    # Fenced lines are skipped, and so are code spans: a document DEMONSTRATING
    # markdown is not a document making a claim. Writing "never do
    # `![](x.png)`" is the sentence that teaches the rule, and it used to fail
    # it.
    for n, line in enumerate(lines, 1):
        if n in fenced:
            continue
        prose = CODE_SPAN_RE.sub(" ", line)
        for m in IMAGE_RE.finditer(prose):
            if not m.group(1).strip():
                fail(rel, f"line {n}: an image has empty alt text. Every image, "
                          "badges included, carries a description.")
        targets = [m.group(1) for m in LINK_RE.finditer(prose)]
        targets += [m.group(1) for m in HTML_HREF_RE.finditer(prose)]
        ref = REF_DEF_RE.match(prose)
        if ref:
            targets.append(ref.group(1))
        for target in targets:
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            # A LINK TARGET IS A URL, NOT A PATH. `Scope-&-Boundaries.md` is
            # written `Scope-%26-Boundaries.md` by anything that encodes
            # correctly, and `&amp;` by anything that escapes for HTML. Both
            # name a file that exists, and both were reported as broken.
            name = unquote(target.split("#")[0]).replace("&amp;", "&")
            if name and not (path.parent / name).exists():
                fail(rel, f"line {n}: relative link {target!r} does not resolve.")


# Directories that are output or machinery rather than authored text.
TREE_SKIP_DIRS = (".git", "dist", "node_modules", "__pycache__", ".venv",
                  ".ruff_cache")

# Verbatim third-party text, exempt from the typography rule by the law itself:
# "license files, vendored assets, lockfiles". A hyphen normalized inside one
# of these is a modification to somebody else's document.
TREE_VERBATIM = ("LICENSE", "LICENSE.txt", "LICENCE", "NOTICE", "COPYING")
TREE_VERBATIM_SUFFIXES = (".lock",)

# The one file whose CONTENT is the rejected text. `_charclasses.py` solves the
# same problem by building its characters from codepoints, which cannot be done
# for words without making the table unreadable. Naming the exemption here is
# the honest version: it is one path, visible in a diff, rather than a rule
# that quietly declines to check itself.
TREE_SELF_EXEMPT = ("_spelling.py",)


def check_tree(root: Path, fail, skip, vendored=frozenset()):
    """Encoding and typography, over EVERY authored file rather than the docs.

    WHY THIS EXISTS. The law says the banned characters are banned "in
    everything you write: prose, code, comments, configuration, commit
    messages, issue text and release notes alike", and until this ran, the
    gate behind that sentence read Markdown and nothing else. A hidden
    directive in a hook script, a bidirectional override in a workflow, a
    curly quote in a Python comment: none of them were checked in the one
    repository whose whole product is files delivered to other repositories.

    That is the same hole that had `AGENTS.md` unguarded while `SKILL.md` was
    guarded, one directory over. A rule enforced on the easy half of the tree
    is a rule with a documented bypass.

    Anything that is not valid UTF-8 is skipped as binary rather than failed:
    this walks a whole repository, and a PNG is not a defect.
    """
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        if any(part in TREE_SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if any(rel.startswith(f"{v}/") or rel == v for v in vendored):
            continue
        if rel in skip or path.name in TREE_VERBATIM:
            continue
        if path.name in TREE_SELF_EXEMPT:
            continue
        if path.suffix in TREE_VERBATIM_SUFFIXES:
            continue
        raw = path.read_bytes()
        if not raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            fail(rel, "starts with a byte order mark.")
        if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
            fail(rel, "must end with exactly one trailing newline.")
        for n, line in enumerate(text.split("\n"), 1):
            for char, name in BANNED_CHARS.items():
                if char in line:
                    fail(rel, f"line {n}: {name}. The ban is tree-wide, not "
                              "Markdown-only.")
            if MOJIBAKE_RE.search(line):
                fail(rel, f"line {n}: mojibake, which is UTF-8 read as Latin-1 "
                          "somewhere upstream.")
            mangled = {i for m in MOJIBAKE_RE.finditer(line)
                       for i in range(m.start(), m.end())}
            for m in INVISIBLE_RE.finditer(line):
                if m.start() in mangled:
                    continue
                fail(rel, f"line {n}: invisible character "
                          f"U+{ord(m.group()):04X} at column {m.start() + 1}. "
                          "In an executable file or a workflow this is the "
                          "shape nobody catches by reading the diff.")
            for found, american in british_hits(CODE_SPAN_RE.sub(" ", line)):
                fail(rel, f"line {n}: {found!r} is the British spelling. "
                          f"Write {american!r}.")


def check_names(root: Path, fail, vendored=frozenset()):
    """`_` as a space, across the whole tree rather than only docs/."""
    for path in sorted(root.rglob("*")):
        # THE SAME SKIP LIST THE TYPOGRAPHY RULE USES. This walk filtered only
        # `.git`, so `dist/`, `node_modules/`, `__pycache__/` and `.venv/`
        # were all name-checked, and `make lint-docs` reads the working tree
        # rather than what is tracked. Creating a virtualenv, which is the
        # reflex before running any Python here, turned the documentation gate
        # into hundreds of errors from package names nobody can rename, with
        # every real finding underneath them. The intent was already written
        # down twice, in `.gitignore` and in TREE_SKIP_DIRS; this reads it.
        if any(part in TREE_SKIP_DIRS for part in path.relative_to(root).parts):
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
                       f"read when needed, or raise the budget in {Path(__file__).name} "
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

    for rel in HOOK_SCRIPTS:
        path = root / rel
        if not path.is_file():
            # SKIPPED, AND THE ABSENCE IS REPORTED ELSEWHERE. A missing router
            # used to be a silent pass here and nothing else looked, so
            # renaming one left the gate on the only content that executes on
            # somebody else's machine reporting clean by having no subject.
            # `check_settings` is where that is caught now, because it can tell
            # the two cases apart: a tree whose settings file REGISTERS this
            # path and does not ship it is broken, and a tree that ships no
            # routers at all is most other repositories. Failing here would
            # fail every one of them, which is the false positive this file
            # exists to avoid.
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
            fail(rel, f"prints {size} bytes for "
                      f"{len(HOOK_EXPECTED.get(rel, ()))} skills, against a "
                      f"budget of {HOOK_OUTPUT_BUDGET}. This "
                      "runs on EVERY prompt, so that is charged again on every "
                      "turn of every session. Name the skills and stop; the "
                      "model already holds their descriptions.")

        # THE SAME BUDGET, AGAINST A REPOSITORY THAT USES THE FEATURE HARD.
        with tempfile.TemporaryDirectory() as scratch:
            for base in HOOK_FIXTURE_LAYOUT:
                for i in range(HOOK_FIXTURE_MANY):
                    d = Path(scratch) / base / f"skill-name-number-{i:02d}"
                    d.mkdir(parents=True, exist_ok=True)
                    (d / "SKILL.md").write_text("---\n", encoding="utf-8")
            env = {"PATH": "/usr/bin:/bin",
                   "CLAUDE_PROJECT_DIR": scratch, "GEMINI_PROJECT_DIR": scratch}
            many = subprocess.run(["sh", str(path)], capture_output=True,
                                  text=True, env=env)
            many_size = len(many.stdout.encode("utf-8"))
        if many_size > HOOK_OUTPUT_BUDGET:
            fail(rel, f"prints {many_size} bytes for {HOOK_FIXTURE_MANY} "
                      f"skills, against a budget of {HOOK_OUTPUT_BUDGET}. The "
                      "budget was only ever measured against three, so it "
                      "recorded a number rather than a ceiling: this runs on "
                      "EVERY prompt of every session in every repository that "
                      "received it, and nothing in the script stops the list "
                      "growing with the number of skills installed. Name a "
                      "bounded number of them and say how many were left out.")

        # A router that says nothing when skills ARE present is the failure
        # that looks exactly like a working one.
        if size == 0:
            fail(rel, "printed nothing with skills installed, so it is doing "
                      "no work at all. A silent router is indistinguishable "
                      "from a correct one until someone checks.")


def check_envelopes(root: Path, fail):
    """Each envelope still carries the one line it exists for.

    NOTHING CHECKED THIS, and every other gate passes without it. The budget
    rule measures size, the release loop measures presence, and a `CLAUDE.md`
    whose import has been replaced by the sentence "See AGENTS.md in this
    repository" satisfies both while reading perfectly correctly in a diff. It
    is also the one delivered failure with no symptom: the router is present,
    the law is present, and the agent simply never receives it.

    THE TOKEN HAS TO BE LIVE, which is why this consults the fence map rather
    than searching the text. Both vendors document that import parsing skips
    code spans and fenced blocks, so a backticked `@./AGENTS.md` is exactly the
    documented way to write the token WITHOUT importing, and an envelope
    carrying only that one is inert.
    """
    for rel in ENVELOPES:
        path = root / rel
        if not path.is_file():
            continue
        lines = path.read_text(encoding="utf-8").split("\n")
        fenced = scan_fences(rel, lines, lambda *_: None, lambda *_: None)
        live = [n for n, line in enumerate(lines, 1)
                if n not in fenced and line.strip() == IMPORT_LINE]
        if not live:
            fail(rel, f"carries no live `{IMPORT_LINE}` line, so it imports "
                      "nothing. This file exists only to carry that one line "
                      "to a tool that cannot discover the canonical filename. "
                      "Without it the envelope is a correct-looking document "
                      "that delivers no law at all, in every repository that "
                      "receives it, with nothing anywhere reporting a problem. "
                      "A token inside backticks or a fence does not import: "
                      "that is the documented way to write one literally.")

    law = root / LAW
    if law.is_file():
        lines = law.read_text(encoding="utf-8").split("\n")
        fenced = scan_fences(LAW, lines, lambda *_: None, lambda *_: None)
        for n, line in enumerate(lines, 1):
            if n not in fenced and line.strip() == IMPORT_LINE:
                fail(LAW, f"line {n}: the law imports itself. `{IMPORT_LINE}` "
                          "belongs in an envelope; here it is a loop.")


def check_settings(root: Path, fail):
    """The delivered registration files, which nothing used to open.

    Four things, and every one of them ships silently otherwise: a file that
    is not JSON, a file registering an event the vendor does not fire, a
    command naming a hook that is not in the tree, and a key that grants
    something on the receiving side.
    """
    for rel, (event, hook) in sorted(DELIVERED_SETTINGS.items()):
        path = root / rel
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            fail(rel, f"is not readable JSON: {exc}. This file is copied into "
                      "other people's repositories and the vendor reads it at "
                      "startup, so a syntax error here is a router that never "
                      "registers and a settings file somebody has to repair "
                      "by hand.")
            continue
        if not isinstance(data, dict):
            fail(rel, "must hold a JSON object.")
            continue

        for key in SETTINGS_BANNED_KEYS:
            if key in data:
                fail(rel, f"may not carry `{key}`. A delivered settings file is "
                          "written once into a consuming repository and never "
                          "overwritten, so anything granted here cannot be "
                          "withdrawn by moving a tag back or by any other "
                          "publisher-side action. That decision belongs to the "
                          "repository receiving it.")

        hooks = data.get("hooks")
        if not isinstance(hooks, dict) or event not in hooks:
            fail(rel, f"registers no `{event}` hook, so the router beside it is "
                      f"delivered and never runs. Found: "
                      f"{sorted(hooks) if isinstance(hooks, dict) else hooks!r}.")
            continue

        # The command has to name a file this repository actually ships. A
        # rename on either side leaves a registration pointing at nothing,
        # which looks exactly like a repository with no skills installed.
        commands = [entry.get("command", "")
                    for group in hooks[event] if isinstance(group, dict)
                    for entry in group.get("hooks", [])
                    if isinstance(entry, dict)]
        if not any(hook in command for command in commands):
            fail(rel, f"names a hook this repository does not ship: no "
                      f"registered command references {hook!r}. Found "
                      f"{commands!r}. A registration pointing at a path that "
                      "does not exist is a router that is installed, silent, "
                      "and indistinguishable from one with nothing to say.")
        elif not (root / hook).is_file():
            fail(rel, f"registers {hook!r}, which is not in this tree.")


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
        for _value, owners in sorted(table.items()):
            if len(owners) > 1:
                for owner in owners:
                    others = [o for o in owners if o != owner]
                    fail(owner, f"this {kind} is shared with {', '.join(others)}. "
                                "The specification requires it to be unique to "
                                "the document: a repeated one is a closing "
                                "argument that argues nothing.")
    if not docs_only:
        check_names(root, fail, vendored)
        # The documents above were already read line by line; passing them here
        # would report every finding twice.
        check_tree(root, fail,
                   skip={p.relative_to(root).as_posix() for p in files},
                   vendored=vendored)
        check_delivered_budget(root, fail, warn)
        check_hooks(root, fail, warn)
        check_envelopes(root, fail)
        check_documented_numbers(root, fail)
        check_settings(root, fail)
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
    "British spelling",
)
SELF_TEST_WARNINGS = (
    "not fully capped",
    "spells out `AND`",
    # Asserted because its failure mode is silence. When `<details>` was
    # counted anywhere the string appeared, one mention in prose suppressed
    # this warning for the rest of the file and nothing said so.
    "this fence is",
)
# One defect, one diagnosis. A three-byte mojibake sequence carries a C1
# continuation byte, so it trips the invisible-character rule too, and that
# rule's advice ("remove it") is wrong here: removing one byte of three leaves
# the other two.
SELF_TEST_MOJIBAKE = (chr(0x2019), "mojibake", "invisible character")
SELF_TEST_BUDGET = "against a budget of"
SELF_TEST_TREE = "tree-wide"

# Each is one hostile settings file, written in turn and run through
# `check_root` so the call site is proved along with the rule.

# THE HIDDEN-CHARACTER CLASS, ASSERTED CODEPOINT BY CODEPOINT. Asserted here
# rather than in `_charclasses.py` because that module is a table with no
# entry point, and a table nothing runs is a table nothing checks. Both
# checkers import the class, so proving it once proves it for both.
#
# The end-to-end fixtures below prove that ONE hidden character is reported.
# They cannot prove which ones, and that is the whole question: the class
# covered the tag block while missing the variation selectors one range over,
# which is the channel the published emoji-smuggling technique actually uses.
SELF_TEST_HIDDEN = (
    (0x200B, "zero width space"),
    (0xE0001, "language tag"),
    (0xE0100, "variation selector-17, the smuggling channel"),
    (0xE01EF, "variation selector-256"),
    (0xFE00, "variation selector-1"),
    (0x2800, "Braille pattern blank"),
    (0x001B, "ESC, which writes an ANSI sequence to the operator's terminal"),
    (0x007F, "DELETE"),
    (0x009B, "CSI"),
    (0x00A0, "no-break space, which changes shell word splitting"),
    (0x2003, "em space"),
    (0x2028, "line separator"),
    (0x3000, "ideographic space"),
)
# The carve-outs, each one a decision rather than an oversight. U+FE0F is the
# emoji presentation selector and sits inside 42 of this repository's own
# headings, so the family is added without it: 15 of the 16 selectors and all
# 240 of the E0100 block still fail. Tab and newline are structure.
SELF_TEST_NOT_HIDDEN = (
    (0xFE0F, "variation selector-16, which every emoji heading here carries"),
    (0x0009, "tab"),
    (0x000A, "newline"),
    (0x000D, "carriage return, which the line splitter never sees"),
)

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

A tilde fence is a fence too, and nothing inside one is a claim either:

~~~markdown
# NOT THE TITLE OF THIS DOCUMENT
[another guide](./Also-Missing.md)
~~~

Prose may name the `<details>` element without opening one, and may show
`![](./neither.png)` inside a code span without failing the alt-text rule.

Naming a third-party field the document does not control is a citation
rather than a spelling: `colour` is what that API calls it.

A link target is a URL rather than a path: [ampersand](Ampersand-%26-Test.txt)
resolves, and so does [the escaped form](Ampersand-&amp;-Test.txt).

---

<div align="center">

**Nothing to report.**

[↑ Back to Top](#top)

</div>

---

## 📐 Appendix

A document that teaches this format has to be able to show it, and the
template below is a fenced example rather than a second footer:

```markdown
<div align="center">

**Your closing phrase, which is unique to your document.**

</div>
```
"""

# The em dash is BUILT FROM ITS CODEPOINT so this file never contains the
# character it rejects, exactly as check-skills.py builds its invisible
# characters. A rule whose own test data trips it is a rule that cannot be
# tested in the repository that enforces it.
BROKEN_BODY = ("""
<div align="center">

# 💥 Bad Document AND Worse

**Broken in every way the checker is supposed to notice{EM}including this.**

A rule hidden from the reviewer: split{ZWSP}word.

A sentence using {BRITISH}, on the wrong side of the Atlantic.

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

Naming the `<details>` element in prose must not open one, or the long fence
below stops being reported and the gate goes quiet. Neither must naming it in
an HTML comment, which is exactly the note somebody leaves while working
toward compliance:

<!-- TODO: wrap the block below in a <details> block later -->

```text
""" + "padding\n" * 25 + """```

<div align="center">

**Everything to report.**

</div>
""").replace("{EM}", chr(0x2014)).replace("{ZWSP}", chr(0x200B)) \
    .replace("{BRITISH}", BRITISH_FIXTURE)

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
        # Named by two links in Good.md, one percent-encoded and one escaped
        # for HTML. Both must resolve to this file.
        (root / "Ampersand-&-Test.txt").write_text("Not a document.\n",
                                                   encoding="utf-8")

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

        # The tree gate reads files the document rules never open, so it needs
        # hostile input that is not a document: an executable one, since that
        # is the file where a hidden character does the most and is seen least.
        #
        # RUN THROUGH check_root RATHER THAN CALLED DIRECTLY. Calling the
        # function proves the function; it does not prove anything still calls
        # it. Deleting the call site passed a self-test that invoked it by
        # hand, which is the difference between a tested rule and a live one.
        (root / "hook.sh").write_text(
            "#!/bin/sh\n# a note" + chr(0x2014) + "like this\n"
            "echo split" + chr(0x200B) + "word\n", encoding="utf-8")
        _, tree_problems, _ = check_root(root, docs_only=False)
        fired = any(p["file"] == "hook.sh" and SELF_TEST_TREE in p["message"]
                    for p in tree_problems)
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: {SELF_TEST_TREE}")
        if not fired:
            missing.append(f"error: {SELF_TEST_TREE}")
        (root / "hook.sh").unlink()

        # A documented number that no longer matches its constant. Mutated in
        # a COPY of the real tree, because this rule reads the repository it is
        # given rather than a fixture: a synthetic document would prove the
        # regex and not that the numbers here are right.
        import shutil
        mirror = root / "mirror"
        for item in ("docs", "scripts", "skills"):
            src = Path(__file__).resolve().parent.parent / item
            if src.is_dir():
                shutil.copytree(src, mirror / item, dirs_exist_ok=True,
                                symlinks=True)
        drifted = mirror / "docs" / "Checks-&-Gates.md"
        if drifted.is_file():
            drifted.write_text(
                drifted.read_text(encoding="utf-8").replace(
                    "| `AGENTS.md` | 14,000 bytes", "| `AGENTS.md` | 99,000 bytes"),
                encoding="utf-8")
            hits = []
            check_documented_numbers(mirror, lambda f, m: hits.append(m))
            fired = any("the AGENTS.md byte budget" in m for m in hits)
            print(f"  {'fired    ' if fired else 'DID NOT  '} error: "
                  "a documented number that drifted from its constant")
            if not fired:
                missing.append("error: documented number drift")
        shutil.rmtree(mirror, ignore_errors=True)

        # The envelopes. Same hostile-then-correct shape, same reason for
        # going through check_root.
        (root / "AGENTS.md").write_text("The law.\n", encoding="utf-8")
        envelope = root / "CLAUDE.md"
        for phrase, body in (
            # Prose about the import reads correctly to a reviewer and imports
            # nothing. This is the exact edit that passed every gate.
            ("carries no live `@./AGENTS.md`", "See AGENTS.md in this repository.\n"),
            # Backticks are the documented way to write the token WITHOUT
            # importing, so a router carrying only that one is inert.
            ("carries no live `@./AGENTS.md`", "Write it as `@./AGENTS.md` here.\n"),
            # And inside a fence, for the same reason.
            ("carries no live `@./AGENTS.md`",
             "```markdown\n@./AGENTS.md\n```\n"),
        ):
            envelope.write_text(body, encoding="utf-8")
            _, found, _ = check_root(root, docs_only=False)
            fired = any(phrase in p["message"] and p["file"] == "CLAUDE.md"
                        for p in found)
            print(f"  {'fired    ' if fired else 'DID NOT  '} error: "
                  f"{phrase} ({body.splitlines()[0][:34]!r})")
            if not fired:
                missing.append(f"error: {phrase} for {body!r}")
        envelope.write_text("@./AGENTS.md\n", encoding="utf-8")
        _, found, _ = check_root(root, docs_only=False)
        noisy_env = [p for p in found if p["file"] == "CLAUDE.md"
                     and "@./AGENTS.md" in p["message"]]
        if noisy_env:
            print("::error title=Check Docs::A CORRECT envelope was rejected.")
            for p in noisy_env:
                print(f"    {p['message']}")
            return 1
        envelope.unlink()
        (root / "AGENTS.md").unlink()

        # The delivered registration files. RUN THROUGH check_root for the same
        # reason the tree gate is: calling the function proves the function, not
        # that anything still calls it.
        hook = root / ".claude" / "hooks"
        hook.mkdir(parents=True, exist_ok=True)
        (hook / "skill-router.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        settings = root / ".claude" / "settings.json"
        good = json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [
            {"type": "command",
             "command": 'sh "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-router.sh"'}]}]}})
        hostile = {
            "is not readable JSON": '{"hooks": {},,}',
            "registers no `": json.dumps({"hooks": {"WrongEvent": []}}),
            "names a hook this repository does not ship":
                good.replace("skill-router.sh", "renamed-router.sh"),
            "may not carry `permissions`":
                json.dumps({"permissions": {"allow": ["Bash(curl:*)"]},
                            **json.loads(good)}),
        }
        for phrase, body in hostile.items():
            settings.write_text(body + "\n", encoding="utf-8")
            _, found, _ = check_root(root, docs_only=False)
            fired = any(phrase in p["message"] for p in found)
            print(f"  {'fired    ' if fired else 'DID NOT  '} error: {phrase}")
            if not fired:
                missing.append(f"error: {phrase}")
        # And the correct pair must be accepted, or the gate cries wolf.
        settings.write_text(good + "\n", encoding="utf-8")
        _, found, _ = check_root(root, docs_only=False)
        noisy_settings = [p for p in found
                          if p["file"] == ".claude/settings.json"]
        if noisy_settings:
            print("::error title=Check Docs::A CORRECT settings file was rejected.")
            for p in noisy_settings:
                print(f"    {p['message']}")
            return 1
        settings.unlink()
        (hook / "skill-router.sh").unlink()

        # Every link FORM, not just the one the pattern happened to match.
        (root / "Links.md").write_text(
            GOOD.replace("## \U0001F4A1 Body", """## \U0001F4A1 Body

A plain broken link: [one](./Missing-A.md)

A broken link carrying a title: [two](./Missing-B.md "hover text")

An angle-bracket destination: [three](<./Missing-C.md>)

A reference-style link: [four][ref]

[ref]: ./Missing-D.md

A raw HTML link: <a href="./Missing-E.md">five</a>"""),
            encoding="utf-8")
        _, links, _ = check_root(root, docs_only=True)
        blob = " ".join(p["message"] for p in links if p["file"] == "Links.md")
        unseen = [n for n in ("Missing-A", "Missing-B", "Missing-C",
                              "Missing-D", "Missing-E") if n not in blob]
        fired = not unseen
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: "
              f"every link form is resolved")
        if unseen:
            missing.append(f"error: link forms never resolved: {unseen}")
        (root / "Links.md").unlink()

        # The name rule walks the same tree as the typography rule and did
        # not share its skip list, so a virtualenv or a populated dist/ turned
        # `make lint-docs` into a wall of errors from names nobody can rename.
        noise = root / ".venv" / "lib" / "site_packages_x"
        noise.mkdir(parents=True, exist_ok=True)
        (noise / "a_module.py").write_text("x = 1\n", encoding="utf-8")
        name_hits = []
        check_names(root, lambda f, m: name_hits.append(f))
        fired = not any(h.startswith(".venv/") for h in name_hits)
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: "
              f"generated trees are skipped by the name rule too")
        if not fired:
            missing.append(f"error: name rule walks skipped trees ({name_hits})")

        # A key set twice. The skill checker refuses this and says why; the
        # document parser kept the last one silently, on the three files that
        # are delivered into other people's repositories.
        (root / "Twice.md").write_text(
            GOOD.replace("description: 'A document that satisfies every rule "
                         "this checker enforces.'",
                         "description: 'The one a reviewer reads in the diff.'\n"
                         "description: 'The one that actually loads.'"),
            encoding="utf-8")
        _, twice, _ = check_root(root, docs_only=True)
        fired = any("a second time" in p["message"] for p in twice
                    if p["file"] == "Twice.md")
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: a second time")
        if not fired:
            missing.append("error: a second time")
        (root / "Twice.md").unlink()

        # Mojibake is diagnosed as mojibake, and not also as something else.
        ch, want, unwanted = SELF_TEST_MOJIBAKE
        (root / "Mojibake.md").write_text(
            GOOD.replace("## \U0001F4A1 Body",
                         "## \U0001F4A1 Body\n\nA mangled quote: it"
                         + ch.encode("utf-8").decode("latin-1") + "s here."),
            encoding="utf-8")
        _, moji, _ = check_root(root, docs_only=True)
        msgs = [p["message"] for p in moji if p["file"] == "Mojibake.md"]
        fired = any(want in m for m in msgs) and not any(unwanted in m for m in msgs)
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: {want}, "
              f"and not also {unwanted!r}")
        if not fired:
            missing.append(f"error: {want} diagnosed alone (got {msgs})")
        (root / "Mojibake.md").unlink()

        # The class both checkers import, one codepoint at a time.
        hidden_bad = []
        for cp, label in SELF_TEST_HIDDEN:
            if not INVISIBLE_RE.search(chr(cp)):
                hidden_bad.append(f"U+{cp:04X} ({label}) is not caught")
        for cp, label in SELF_TEST_NOT_HIDDEN:
            if INVISIBLE_RE.search(chr(cp)):
                hidden_bad.append(f"U+{cp:04X} ({label}) must NOT be caught")
        fired = not hidden_bad
        print(f"  {'fired    ' if fired else 'DID NOT  '} error: "
              f"every hidden-character family, {len(SELF_TEST_HIDDEN)} caught "
              f"and {len(SELF_TEST_NOT_HIDDEN)} deliberately not")
        if hidden_bad:
            for item in hidden_bad:
                print(f"    {item}")
            missing.append(f"error: hidden-character class: {hidden_bad}")

        # NEITHER ERRORS NOR WARNINGS. A warning on correct input is still a
        # gate crying wolf, and two of the rules fixed here reported one: a
        # heading inside a fenced example was counted as a second Heading 1,
        # and a `<details>` named in prose silenced the long-fence rule.
        noisy = [p for p in problems + warnings if p["file"] == "Good.md"]
        if noisy:
            print("::error title=Check Docs::The compliant document was REJECTED. "
                  "A gate that fails correct input trains everyone to ignore it.")
            for p in noisy:
                print(f"    {p['level']}: {p['message']}")
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
