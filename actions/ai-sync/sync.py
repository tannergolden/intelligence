#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tanner Golden
# SPDX-License-Identifier: MIT
"""Copy `payload/` into a consumer repository and maintain its lockfile.

This is the whole engine. It reads `payload/` out of this repository, writes
the same bytes into a target working tree, merges the one file it is not
allowed to overwrite, records what it did in `.ai/ai.lock.json`, and stops.

IT NEVER RUNS GIT. The calling workflow owns the commit, because the job
holding `contents: write` and the job running this code are deliberately not
the same job.

Three rules carry almost all of the safety here, and each exists because of
a specific way this could destroy work it did not author:

  * REFUSE-ON-FIRST-CONTACT. A file that exists in the target, is absent
    from the lock, and does not carry the generated header is HAND WRITTEN.
    Overwriting it would be silent, unreviewed, bot-authored data loss with
    no pull request anywhere in the path. The repository this replaces holds
    tens of kilobytes of hand-written law, so this one check is the whole
    difference between a migration and an incident.

  * THE RETIRE GUARD. One bad `git rm` in `payload/` would otherwise delete
    files across every consuming repository in a single scheduled run, with
    no review gate at any point. More than two retirements needs a human and
    an explicit flag.

  * LOCK ON EVERY TERMINAL PATH. A run that refused is not a run that never
    happened, and afterwards only the lockfile can tell those two apart.

One more borrowed rule, lifted from the incumbent template engine this
replaces: a refusal suppresses ACTIONS, never BOOKKEEPING. When a run
aborts, the previous lock's `files` are carried forward verbatim rather than
dropped, because ownership records are what make a later retirement safe.
Forget this and a refused run silently orphans every path it owned.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = 1

LOCK_PATH = ".ai/ai.lock.json"
DATE_PATH = ".ai/ai.lock.date"
LOCAL_PATH = ".ai/local/agents-local.md"
SETTINGS_PATH = ".claude/settings.json"
AGENTS_PATH = "AGENTS.md"

# The command prefix that marks a hook entry in `.claude/settings.json` as
# ours. It is FROZEN for the life of v1 and `check.py` asserts the payload
# still spells it this way. Two reasons, both load bearing: it is the only
# thing distinguishing our entries from the consumer's own, and Claude Code
# has no fingerprint or re-warning mechanism for a changed hook command, so
# rotating it would execute new code in every already-trusted consumer with
# no prompt and no signal. Churn goes INSIDE the scripts, which are in the
# lock with a digest and diffable in the release notes.
HOOK_PREFIX = 'bash "$CLAUDE_PROJECT_DIR/.ai/hooks/'

# Every generated file carries this. Its absence from a file that exists in
# the target and is missing from the lock is what proves the file is a
# human's.
GENERATED_MARK = "DO NOT EDIT - Published by tannergolden/ai"

# The consumer-owned region inside AGENTS.md. Both markers must already be
# present in the payload's AGENTS.md; if they are not, that is a publisher
# defect and this run aborts rather than silently dropping local law.
LOCAL_BEGIN = "<!-- ai:local:begin -->"
LOCAL_END = "<!-- ai:local:end -->"

MAX_RETIRE = 2

OK_OUTCOMES = ("applied", "unchanged")

# `vendor` is the requirement that adding a third tool stays additive,
# expressed as data a `jq` one-liner can act on:
#
#   jq -r '.files[] | select(.vendor == "claude") | .path' .ai/ai.lock.json
#
# must list exactly the Claude-only surface and nothing else, so that
# removing one vendor is a filter rather than an archaeology exercise.
# `.ai/hooks/` is Claude-only because a hook script is reachable ONLY through
# `.claude/settings.json`; nothing in Gemini CLI ever reads it. `.agents/` is
# Gemini's workspace skills path, which other tools happen to read as well,
# but among the two supported tools it reaches exactly one.
VENDOR_RULES = (
    ("CLAUDE.md", "claude"),
    (".claude/", "claude"),
    (".ai/hooks/", "claude"),
    ("GEMINI.md", "gemini"),
    (".gemini/", "gemini"),
    (".agents/", "gemini"),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contained(target: Path, rel: str):
    """`target / rel`, but only when it provably stays inside `target`.

    Returns None otherwise, and None means REFUSE. Three ways a path escapes
    this tree and every one of them is reachable here:

      * `rel` is absolute. `pathlib` join semantics mean an absolute right
        hand side REPLACES the left, so `target / "/etc/passwd"` is not
        inside the target at all, it IS `/etc/passwd`.
      * `rel` climbs with `..`.
      * A PARENT COMPONENT is a symlink pointing out of the tree. Testing
        the leaf alone misses this entirely: when `.ai` is the link, then
        `<target>/.ai/ai.sh` is not itself a link and never was.

    The first two arrive from `.ai/ai.lock.json`, which is a bot-written
    file in a repository other people can write to, rewritten every run and
    read by no human. The third arrives from the consumer's own working
    tree. `.ai/ai.sh` already refuses the first two before its `rm`; this is
    the same guard on the side that does the writing and the deleting, which
    is the side that has a delete capability pointed at somebody else's
    filesystem.
    """
    if not rel or Path(rel).is_absolute():
        return None
    dest = target / rel
    try:
        root = target.resolve()
        # The LEAF may legitimately not exist yet, so it is the parent that
        # has to land inside the tree. `resolve()` follows every link on the
        # way there, which is what closes the symlinked-directory hole.
        parent = dest.parent.resolve()
    except OSError:
        return None
    return dest if parent == root or parent.is_relative_to(root) else None


def vendor_for(rel: str) -> str:
    for prefix, vendor in VENDOR_RULES:
        if rel == prefix or rel.startswith(prefix):
            return vendor
    return "both"


def owner_for(rel: str) -> str:
    # `shared` means the consumer also writes here, so it is merged rather
    # than overwritten and its digest covers only our own subtree.
    return "shared" if rel == SETTINGS_PATH else "ai"


def walk_payload(payload: Path) -> list:
    """Every shipped file, relative to `payload/`, sorted.

    `.gitkeep` is excluded everywhere. It exists to hold an empty directory
    open in git; delivering one would give a consumer an unexplained empty
    file plus a lock entry that outlives the directory it was holding open.
    """
    found = []
    for root, dirs, files in os.walk(payload):
        dirs.sort()
        for name in files:
            if name == ".gitkeep":
                continue
            found.append(Path(root, name).relative_to(payload).as_posix())
    return sorted(found)


def looks_generated(data: bytes) -> bool:
    """Does this file carry our provenance marker as a marker, not a mention?

    Anchored to a whole line, in one exact form, near the top. Never a
    substring search, because a substring search hands this decision to
    anyone who QUOTES the sentence: a repository documenting this very
    system, this publisher included, carries the marker inside a fenced
    example in its own hand-written AGENTS.md, and a substring test reads
    that as "we wrote this" and overwrites it with no refusal and no pull
    request anywhere. This is the check the whole difference between a
    migration and an incident rests on, so it is worth being exact.

    THE `# ` PREFIX IS REQUIRED, not optional. Every file published from
    here opens with the marker as a markdown H1 or a shell comment within
    its first few lines, and none of them writes it bare. Requiring the
    prefix is what makes a quoted mention on its own line inside a fenced
    block stop counting as provenance, which the bare form does not.
    """
    head = data[:4096].decode("utf-8", "replace").split("\n")[:12]
    return any(line.strip() == f"# {GENERATED_MARK}" for line in head)


def check_local(script_dir: Path, text: str) -> bool:
    """Run the payload's own linter over the consumer's local law.

    Consumer-supplied text goes through the SAME suite as the payload,
    because it lands in the same always-loaded file, and a live `@token` or
    an invisible character does identical damage whoever authored it.

    It is checked as STAGED BYTES in a scratch directory rather than in
    place, for two reasons: `check.py` takes a directory, and linting the
    consumer's `.ai/local/` directly would let unrelated scaffolding beside
    the file (a leftover `.gitkeep`, say) abort a sync that has nothing to
    do with it. Only the bytes about to be injected are judged.

    `--no-hatch` is the one difference from the publisher's own run, and it
    is not a detail. The `<!-- ai:allow-at -->` hatch exists so THIS
    publisher's two routers can spell the import line they exist to carry.
    Text arriving from a repository the publisher has never seen has no
    business claiming it: a hatched `@/etc/shadow` in local law is inlined
    recursively into an always-loaded context file on every Gemini session.
    The hatch is the publisher's, so it is switched off for everyone else.

    A missing checker fails closed. Unchecked content is not shipped.
    """
    checker = script_dir / "check.py"
    if not checker.is_file():
        print(f"::error title=Broken install::{checker} is missing, refusing to inject unchecked content.")
        return False
    with tempfile.TemporaryDirectory() as scratch:
        staged = Path(scratch) / Path(LOCAL_PATH).name
        staged.write_text(text, encoding="utf-8")
        print(f"[check] {LOCAL_PATH} (staged as {staged}, escape hatch disabled)")
        command = [sys.executable, str(checker), scratch, "--no-hatch", "--any-path"]
        return subprocess.run(command, check=False).returncode == 0


def inject_local(agents: bytes, local_text: str) -> bytes:
    """Splice the consumer's local law into the marked region of AGENTS.md.

    The provenance line names the source file so that an agent reading the
    delivered instructions can tell which half of them is repository-local,
    and so a human who wants to change that half knows where to go.
    """
    text = agents.decode("utf-8")
    start, end = text.find(LOCAL_BEGIN), text.find(LOCAL_END)
    if start < 0 or end < start:
        raise ValueError(f"AGENTS.md is missing the {LOCAL_BEGIN} / {LOCAL_END} region")
    note = f"<!-- Injected by tannergolden/ai from {LOCAL_PATH}. Edit that file, never this region. -->"
    body = local_text.strip("\n")
    region = f"{LOCAL_BEGIN}\n\n{note}\n\n{body}\n\n" if body else f"{LOCAL_BEGIN}\n\n{note}\n\n"
    return (text[:start] + region + text[end:]).encode("utf-8")


def strip_ours(groups: list) -> list:
    """Drop our hook commands from one event's matcher groups.

    Filtering happens at the innermost level, not at the group level: a
    consumer who added their own command beside ours inside one matcher
    group keeps it. A group left holding nothing was ours alone and goes.

    A GROUP shaped in a way this does not recognise is passed through
    untouched, because the safe answer to an unfamiliar structure in someone
    else's config file is to leave it exactly as it was found. That is safe
    here and only here: a group travels inside a list, so passing one
    through re-emits it in the same list. An unfamiliar value one level up,
    where the list itself should be, is NOT passed through: see
    `unmergeable`, which refuses the whole file instead.
    """
    kept_groups = []
    for group in groups:
        if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
            kept_groups.append(group)
            continue
        kept = [
            hook
            for hook in group["hooks"]
            if not str((hook or {}).get("command", "")).startswith(HOOK_PREFIX)
        ]
        if len(kept) == len(group["hooks"]):
            kept_groups.append(group)
        elif kept:
            replacement = dict(group)
            replacement["hooks"] = kept
            kept_groups.append(replacement)
    return kept_groups


def unmergeable(existing: dict):
    """Why this settings file cannot be merged into, or None when it can.

    THIS GUARD EXISTS BECAUSE COERCION HERE IS SILENT DESTRUCTION. The merge
    rebuilds the `hooks` object, and rebuilding anything requires knowing its
    shape. An unrecognised value there is not something to coerce: `list()`
    of a dict yields its KEYS, so a consumer's

        "hooks": {"SessionStart": {"hooks": [{"command": "..."}]}}

    (a missing array wrapper, the most plausible hand-edit there is) would
    come back as `["hooks", {ours}]` and their command would be gone. Not
    quarantined and not reported: replaced by the string "hooks". Claude Code
    then rejects the WHOLE file on the invalid value, which takes the
    repository's own hooks down with it, and this publisher pushes that to
    their default branch with no pull request and no reviewer.

    So: refuse, do not repair. The run goes red with a readable reason and
    the consumer's file is not touched. That is the one outcome which cannot
    destroy work this publisher did not author, and it is the failure the
    rest of this design is organised around preventing.
    """
    hooks = existing.get("hooks")
    if hooks is None:
        return None
    if not isinstance(hooks, dict):
        return f"has a 'hooks' key that is a {type(hooks).__name__}, not an object"
    for event, groups in hooks.items():
        if not isinstance(groups, list):
            return f"has a 'hooks.{event}' value that is a {type(groups).__name__}, not a list"
    return None


def merge_settings(existing: dict, ours: dict) -> dict:
    """Return `existing` with our hook entries replaced by `ours`.

    `.claude/settings.json` is the consumer's ONLY committed, team-shared
    Claude configuration file, and Claude Code has no drop-in directory, no
    include and no merge file. Overwriting it would seize `permissions`,
    `env` and every hook the consumer wired themselves. So we own hook
    entries carrying our command prefix and nothing else: every other
    top-level key and every foreign hook entry survives byte for byte.

    Passing an empty `ours` is how the path is retired: our entries leave,
    the consumer's file stays.

    `unmergeable` has already run and returned None, so every value under
    `hooks` here is known to be a list. Nothing below coerces anything.
    """
    merged = {key: value for key, value in existing.items() if key != "hooks"}
    hooks = {}
    for event, groups in (existing.get("hooks") or {}).items():
        kept = strip_ours(groups)
        if kept:
            hooks[event] = kept
    for event, groups in ours.items():
        hooks[event] = hooks.get(event, []) + list(groups)
    if hooks or "hooks" in existing:
        merged["hooks"] = hooks
    return merged


def dump_settings(obj: dict) -> bytes:
    # Stable key ordering, so a consumer who hand-sorts their file differently
    # gets one reordering diff and never a second.
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_lock(target: Path) -> dict:
    """Read the previous lock. An unreadable one is treated as absent.

    Failing open here is the safe direction: with no ownership record every
    pre-existing file becomes a first-contact refusal, which stops the run
    loudly instead of overwriting anything.
    """
    path = target / LOCK_PATH
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (ValueError, OSError):
        print(
            f"[warn] {LOCK_PATH} is unreadable, treating this as a first sync. "
            "Ownership goes with it: any path an earlier release delivered here and "
            "this one no longer ships is now unowned and can never be retired."
        )
        return {}


def owned_entries(previous: dict) -> list:
    """The lock's `files` array, with everything unusable dropped.

    Shape checked per entry, never assumed. The lockfile is an ordinary
    committed file in a repository other people edit, and `.ai/ai.sh` tells
    humans to read it, so a `files` holding a string, a number or a bare
    array is reachable. An entry this cannot understand is not an entry to
    guess at: it is dropped, which costs its bookkeeping and nothing else,
    and the alternative is a traceback in somebody else's CI.
    """
    return [
        entry
        for entry in (previous.get("files") or [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str) and entry["path"]
    ]


def resolved_tag(requested: str) -> str:
    """The concrete release tag, when it is honestly knowable.

    A caller that knows it exports `AI_RESOLVED_TAG`. Otherwise a consumer
    pinned to a full version is its own answer, and a consumer pinned to a
    moving major leaves this empty rather than guessing, because the only
    job this field has is to reveal a consumer sitting on an old tag.
    """
    explicit = os.environ.get("AI_RESOLVED_TAG", "").strip()
    if explicit:
        return explicit
    return requested if re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", requested) else ""


def write_lock(target: Path, outcome: str, files: list, contested: list) -> None:
    requested = os.environ.get("AI_REQUESTED", "").strip()
    lock = {
        "schema": SCHEMA,
        "requested": requested,
        "resolved_tag": resolved_tag(requested),
        "resolved_sha": os.environ.get("AI_RESOLVED_SHA", "").strip(),
        "run_url": os.environ.get("AI_RUN_URL", "").strip(),
        "emitted_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "outcome": outcome,
        "files": sorted(files, key=lambda entry: entry["path"]),
        "contested": sorted(contested),
    }
    # The receipts live under `.ai/` like everything else, so they escape
    # through a symlinked `.ai` exactly the way the payload would. Refusing
    # to write a lock is the lesser harm: a missing lock reads as a first
    # sync, which refuses everything, and a lock written outside the tree
    # would be a receipt for a delivery that never happened.
    path = contained(target, LOCK_PATH)
    if path is None:
        print(f"::error title=Receipt escapes the tree::{LOCK_PATH} resolves outside the target repository, so a parent directory is a link out of it. No lockfile was written.")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    # Insertion order, not sorted keys: the schema reads top to bottom in the
    # order a human wants to read it, and this side of the file is ours.
    path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")


def write_date(target: Path) -> None:
    """One ISO-8601 date, one line, nothing else.

    This sidecar exists so the session hook can check staleness with `date`
    and `test` alone. The hook ships to machines that may have no `python3`,
    no `jq` and no `node`, and the interpreter is the one dependency that
    cannot be fixed remotely.

    It advances only on a successful run. A run that refused delivered
    nothing, and advancing the date would erase the very staleness signal
    the human needs.
    """
    path = contained(target, DATE_PATH)
    if path is None:
        print(f"::error title=Receipt escapes the tree::{DATE_PATH} resolves outside the target repository. No date stamp was written.")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(datetime.now(timezone.utc).strftime("%Y-%m-%d") + "\n", encoding="utf-8")


def emit_outputs(outcome: str, changed: bool) -> None:
    """Publish step outputs BEFORE any non-zero exit.

    A refusing run still has something to say, and a workflow that wants to
    commit the lockfile of a failed sync needs to know which failure it was.
    """
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"outcome={outcome}\n")
        handle.write(f"changed={'true' if changed else 'false'}\n")


def sync(args) -> int:
    payload = Path(args.payload).resolve()
    target = Path(args.target).resolve()
    script_dir = Path(__file__).resolve().parent
    apply_mode = args.mode == "apply"
    tag = "apply" if apply_mode else "plan"

    carried = owned_entries(load_lock(target))
    contested = []

    def finish(outcome: str, changed: bool, files=None) -> int:
        if apply_mode:
            write_lock(target, outcome, carried if files is None else files, contested)
            if outcome in OK_OUTCOMES:
                write_date(target)
        emit_outputs(outcome, changed)
        print(f"[{tag}] outcome={outcome} changed={'true' if changed else 'false'}")
        return 0 if outcome in OK_OUTCOMES else 1

    # 1. The emit set.
    emit = walk_payload(payload)

    # 2. The guards. An empty payload means something upstream deleted the
    #    product, and applying it would retire every delivered file in every
    #    consumer at once.
    if not emit:
        print(f"::error title=Empty payload::{payload} contains no deliverable files. Refusing to run.")
        return finish("check-failed", False)

    emit_set = set(emit)
    to_delete, to_unmerge, stale = plan_retirements(target, carried, emit_set)
    if len(to_delete) + len(to_unmerge) > MAX_RETIRE and not args.allow_large_retire:
        for entry in [pair[0] for pair in to_delete] + to_unmerge:
            print(f"  [would retire] {entry['path']}")
        # THE REMEDY NAMED HERE IS THE ONE A CONSUMER CAN ACTUALLY REACH.
        # `--allow-large-retire` is a local flag for a maintainer running
        # this engine by hand; the reusable workflow takes no inputs, on
        # purpose, so the stub stays the entire consumer-side surface and
        # there is nothing to keep in sync but the ceiling. Naming a flag a
        # consumer cannot pass would turn one careless deletion into a
        # fleet-wide sync outage with a remedy that does not exist.
        print(
            f"::error title=Too many retirements::{len(to_delete) + len(to_unmerge)} paths would be "
            f"removed in one run (limit {MAX_RETIRE}). This is what a deletion inside payload/ looks "
            f"like, and it reaches every consuming repository on their next scheduled run. Nothing "
            f"was changed. FIX IT AT THE PUBLISHER: retire at most {MAX_RETIRE} paths per release "
            f"and cut one release per batch. docs/Retirement-Contract.md says why the floor is a "
            f"count rather than a proportion."
        )
        return finish("check-failed", False)

    # 3. Refuse-on-first-contact, over EVERY emit path. The settings file is
    #    the one exception, and only because it is merged rather than
    #    overwritten, so there is nothing there to lose.
    known = {entry["path"] for entry in carried}
    refused = []
    dests = {}
    for rel in emit:
        if rel == SETTINGS_PATH:
            continue
        dest = contained(target, rel)
        if dest is None:
            # A parent component is a link out of the tree. Refusing rather
            # than unlinking it: that link is the consumer's file, and the
            # damage a write does here lands somewhere nobody will look.
            refused.append((rel, "resolves outside the repository, so a parent directory is a link out of it"))
            continue
        dests[rel] = dest
        if dest.is_symlink() or dest.is_dir():
            # Writing through a link can escape the target tree entirely, and
            # writing onto a directory would silently create a file inside it.
            refused.append((rel, "is a symlink or a directory where a file is published"))
        elif dest.is_file() and rel not in known and not looks_generated(dest.read_bytes()):
            refused.append((rel, "already exists, is not in the lock, and carries no generated header"))
    if refused:
        for rel, why in refused:
            print(f"  [refused] {rel}: {why}")
        print(
            "::error title=First contact refused::The files above look hand written and this sync "
            "will not overwrite them. Nothing was changed. To go ahead, either run "
            "`sh .ai/ai.sh adopt`, which MOVES a hand-written AGENTS.md to "
            f"`{LOCAL_PATH}` so its law survives and is folded back into every delivered "
            "AGENTS.md from now on, or copy out what you want to keep and delete the file. "
            "On a genuine first contact nothing has been delivered yet, so `.ai/ai.sh` does not "
            "exist here; move the file by hand to the path above and re-run."
        )
        return finish("first-contact-refused", False)

    # 4. Produce the delivered bytes, then write them. The transform happens
    #    before the comparison so the digest in the lock is the digest of
    #    what actually landed. Note what this does NOT claim: the emit set is
    #    sorted, so a settings file that turns out to be unmergeable is met
    #    after the earlier paths are already on disk. In the workflow that
    #    costs nothing, because the whole checkout is discarded and nothing
    #    is committed. Running the engine by hand can leave files a lock
    #    written on the same terminal path does not list.
    local_file = target / LOCAL_PATH
    local_text = ""
    if local_file.is_file():
        # Consumer-owned. Read, checked, never written.
        try:
            local_text = local_file.read_bytes().decode("utf-8")
        except ValueError as error:
            print(f"::error title=Local law unreadable::{LOCAL_PATH} is not valid UTF-8: {error}")
            return finish("check-failed", False)
        if not check_local(script_dir, local_text):
            print(f"::error title=Local law rejected::{LOCAL_PATH} failed the payload checks and was not injected.")
            return finish("check-failed", False)
        if LOCAL_BEGIN in local_text or LOCAL_END in local_text:
            print(f"::error title=Nested markers::{LOCAL_PATH} contains the injection markers, which would corrupt the region.")
            return finish("check-failed", False)

    entries = []
    changed = False
    for rel in emit:
        source = (payload / rel).read_bytes()
        if rel == SETTINGS_PATH:
            status, digest, ok = apply_settings(target, source, apply_mode, tag)
            if not ok:
                return finish("check-failed", changed)
        else:
            if rel == AGENTS_PATH and local_file.is_file():
                try:
                    source = inject_local(source, local_text)
                except ValueError as error:
                    print(f"::error title=Broken payload::{error}. Local law would have been dropped silently.")
                    return finish("check-failed", changed)
            # `dests[rel]` rather than a second join: the containment check
            # in step 3 is the only place a destination is computed, so no
            # write can reach a path that check did not clear.
            status = write_file(dests[rel], source, apply_mode, tag, rel)
            digest = sha256(source)
        changed = changed or status != "unchanged"
        entries.append(
            {
                "path": rel,
                "sha256": digest,
                "vendor": vendor_for(rel),
                "owner": owner_for(rel),
                "status": status,
            }
        )

    # 5. Retire. A path goes only when the lock says we put it there, the
    #    payload no longer ships it, and its recorded digest still matches
    #    what is on disk. A mismatch means the consumer edited it, so the
    #    delete is refused and the entry is kept as `contested` rather than
    #    dropped: dropping it would silently skip the file forever, and the
    #    next sync would have no record that anything was ever owed here.
    for entry, dest in to_delete:
        print(f"  [{tag}] retire: {entry['path']}")
        if apply_mode:
            dest.unlink()
        changed = True
    if to_unmerge:
        # At most one path can be here, and retiring it means removing our
        # hook entries from a file that stays.
        status, _digest, ok = apply_settings(target, None, apply_mode, tag)
        if not ok:
            return finish("check-failed", changed)
        changed = changed or status != "unchanged"
    for entry in stale:
        rel = entry["path"]
        print(f"  [contested] {rel}: edited since it was delivered, refusing to retire it.")
        contested.append(rel)
        kept = dict(entry)
        kept["status"] = "contested"
        entries.append(kept)

    outcome = "applied" if changed else "unchanged"
    return finish(outcome, changed, entries)


def plan_retirements(target: Path, carried: list, emit_set: set):
    """Work out what would be removed, before anything is written.

    Computed early because the retire guard has to see the whole picture to
    be worth anything: catching a mass deletion after half of it has already
    happened is not a guard.

    `to_delete` carries the resolved destination beside each entry, so the
    path that gets unlinked is the same object `contained` cleared and there
    is no second join between the check and the delete.
    """
    to_delete, to_unmerge, stale = [], [], []
    for entry in carried:
        rel = entry["path"]
        if rel in emit_set:
            continue
        if rel == SETTINGS_PATH:
            to_unmerge.append(entry)
            continue
        dest = contained(target, rel)
        if dest is None:
            # Every path here comes from the lockfile, which is bot written,
            # rewritten on every run and reviewed by nobody. An absolute or
            # climbing path in it would carry this `unlink` out of the tree,
            # where `git add -A` would never see it and the run would go
            # green over a file destroyed somewhere else on the runner.
            print(f"::warning title=Suspicious lock path::{rel} does not resolve inside the target repository. Not retiring it. Remove the entry from .ai/ai.lock.json by hand.")
            continue
        if dest.is_symlink():
            stale.append(entry)
        elif not dest.is_file():
            continue  # already gone: the bookkeeping goes with it
        elif sha256(dest.read_bytes()) == entry.get("sha256"):
            to_delete.append((entry, dest))
        else:
            stale.append(entry)
    return to_delete, to_unmerge, stale


def write_file(dest: Path, data: bytes, apply_mode: bool, tag: str, rel: str) -> str:
    if dest.is_file() and dest.read_bytes() == data:
        return "unchanged"
    verb = "update" if dest.exists() else "add"
    print(f"  [{tag}] {verb}: {rel}")
    if apply_mode:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return "written"


def apply_settings(target: Path, source: bytes, apply_mode: bool, tag: str):
    """Merge our hook entries into the consumer's settings file.

    `source` is the payload copy, or None to retire our entries. Returns
    (status, digest, ok). The digest covers OUR subtree canonically
    serialised, not the whole file: the rest of that file is the consumer's
    and its bytes are none of our business.
    """
    ours = {}
    if source is not None:
        try:
            # Only `hooks` is read. Anything else in the payload copy cannot
            # reach a consumer by construction, which is the cheapest
            # possible enforcement of the ban on shipping settings keys whose
            # value schema is version gated: an invalid value on a KNOWN key
            # silently voids the consumer's entire settings file.
            ours = json.loads(source.decode("utf-8")).get("hooks") or {}
        except ValueError as error:
            print(f"::error title=Broken payload::payload/{SETTINGS_PATH} is not valid JSON: {error}")
            return "contested", "", False

    existing, raw = {}, b""
    dest = contained(target, SETTINGS_PATH)
    if dest is None:
        print(f"::error title=Settings escapes the tree::{SETTINGS_PATH} resolves outside the target repository, so a parent directory is a link out of it. Refusing.")
        return "contested", "", False
    if dest.is_symlink():
        print(f"::error title=Settings is a symlink::{SETTINGS_PATH} is a link. Writing through it could leave the repository. Refusing.")
        return "contested", "", False
    if dest.is_dir():
        print(f"::error title=Settings is a directory::{SETTINGS_PATH} is a directory, not a file. Refusing.")
        return "contested", "", False
    if dest.is_file():
        raw = dest.read_bytes()
        try:
            existing = json.loads(raw.decode("utf-8"))
        except ValueError as error:
            # Never clobber. A file we cannot parse is a file whose contents
            # we cannot preserve, and this one holds the consumer's own
            # permissions, env and hooks.
            print(
                f"::error title=Unparseable settings::{SETTINGS_PATH} is not valid JSON ({error}). "
                "Refusing to touch it. Fix the file, then re-run."
            )
            return "contested", "", False
        if not isinstance(existing, dict):
            print(f"::error title=Unexpected settings::{SETTINGS_PATH} is not a JSON object. Refusing to touch it.")
            return "contested", "", False
        problem = unmergeable(existing)
        if problem:
            print(
                f"::error title=Unexpected settings::{SETTINGS_PATH} {problem}. This merge "
                "recognises `hooks` only as an object of event names to lists, and rebuilding "
                "a shape it does not recognise would rewrite hook wiring this publisher did "
                "not author. Refusing to touch the file. Fix that key, then re-run."
            )
            return "contested", "", False

    merged = dump_settings(merge_settings(existing, ours))
    digest = sha256(json.dumps(ours, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    if merged == raw:
        return "unchanged", digest, True
    print(f"  [{tag}] merge: {SETTINGS_PATH}")
    if apply_mode:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(merged)
    return "merged", digest, True


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Copy payload/ into a repository and maintain .ai/ai.lock.json.")
    parser.add_argument("--target", default=".", help="Target repository working tree (default: the current directory).")
    parser.add_argument("--payload", default=str(Path(__file__).resolve().parents[2] / "payload"), help="Payload directory to deliver.")
    parser.add_argument("--plan", dest="mode", action="store_const", const="plan", default="plan", help="Print what would happen and write nothing (default).")
    parser.add_argument("--apply", dest="mode", action="store_const", const="apply", help="Write the files.")
    parser.add_argument(
        "--allow-large-retire",
        action="store_true",
        help=f"Permit more than {MAX_RETIRE} retirements in one run. Requires a human who has read the list.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if not Path(args.payload).is_dir():
        print(f"::error title=No payload::{args.payload} is not a directory.")
        return 1
    if not Path(args.target).is_dir():
        print(f"::error title=No target::{args.target} is not a directory.")
        return 1
    try:
        return sync(args)
    except Exception as error:  # noqa: BLE001 - the point is that nothing escapes
        # THE PATH NOBODY ANTICIPATED STILL LEAVES A RECEIPT. Every expected
        # failure above reports itself and writes a lock; an unexpected one
        # would otherwise hand a consumer a Python traceback in their own CI
        # and leave delivered files on disk that no lock records. Both halves
        # matter: the annotation is the only readable thing in that run's
        # log, and the lock is what keeps ownership of already-delivered
        # paths from being orphaned by a crash.
        print(f"::error title=Engine fault::{type(error).__name__}: {error}. Nothing further was written.")
        if args.mode == "apply":
            try:
                target = Path(args.target).resolve()
                write_lock(target, "check-failed", owned_entries(load_lock(target)), [])
            except Exception as second:  # noqa: BLE001
                print(f"::error title=Engine fault::the lockfile could not be written either: {second}")
        emit_outputs("check-failed", False)
        return 1


if __name__ == "__main__":
    sys.exit(main())
