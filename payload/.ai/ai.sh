#!/bin/sh
# =============================================================================
# DO NOT EDIT - Published by tannergolden/ai
# .ai/ai.sh: the three things a person needs to do to this installation
# =============================================================================
#   sh .ai/ai.sh verify            exercise the hook and report the sync state
#   sh .ai/ai.sh adopt             hand a hand-written AGENTS.md to the sync
#   sh .ai/ai.sh remove [--force]  uninstall, using the lockfile as the manifest
#
# WHY THIS SHIPS AS A SCRIPT INSTEAD OF AS DOCUMENTATION: this repository
# commits ONE file, the workflow stub. There is no second committed file to
# hang commands off, and appending targets to a repository's own Makefile is
# exactly the merge problem this publisher refuses to have. So the commands
# arrive with the payload, live in the payload's directory, and leave with it.
#
# POSIX sh, and only utilities POSIX guarantees. Same reason as the hook: the
# interpreter is the one dependency that cannot be fixed remotely. Output goes
# through `printf` and never `echo`, because `echo` expands backslash escapes
# in some shells and not others, and this script prints back JSON that is full
# of them.
# =============================================================================

GENERATED_MARK='DO NOT EDIT - Published by tannergolden/ai'
STUB='.github/workflows/ai-sync.yml'
PROBE='reply with the single word OK'

# The repository root is derived from this script's own location, never from
# the working directory, so every command below behaves the same whether it
# was started from the root or from three directories down.
ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd) || exit 1
LOCK="$ROOT/.ai/ai.lock.json"
STAMP="$ROOT/.ai/ai.lock.date"
LOCAL_LAW="$ROOT/.ai/local/agents-local.md"
DISABLED="$ROOT/.ai/hooks/.disabled"

say() {
  printf '%s\n' "$1"
}

usage() {
  cat <<'EOF'
tannergolden/ai

  sh .ai/ai.sh verify            Exercise the SessionStart hook through Claude
                                 Code and report what this installation is.
  sh .ai/ai.sh adopt             Move a pre-existing hand-written AGENTS.md to
                                 .ai/local/agents-local.md so the sync can run.
  sh .ai/ai.sh remove [--force]  Uninstall. Without --force it prints the plan
                                 and deletes nothing.
EOF
}

# Reads one string value out of the lockfile. That file is written by this
# publisher with a fixed serialisation, so a line-oriented read is safe here,
# and it is what buys the whole script its freedom from a JSON tool.
lock_value() {
  [ -f "$LOCK" ] || return 1
  sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$LOCK" | head -n 1
}

# Every path in the lock whose owner is this engine, one per line. THE LOCK
# INVENTORY IS THE UNINSTALL MANIFEST: it is the only record of what was
# delivered here, and complete removal is possible for no other reason.
# Entries owned by `shared` (the settings file) are deliberately absent. Those
# are the repository's own files and are reported for a person to edit.
owned_paths() {
  [ -f "$LOCK" ] || return 1
  _path=""
  while IFS= read -r _line; do
    case "$_line" in
      *'"path":'*)
        _path=${_line#*:}
        _path=${_path#*\"}
        _path=${_path%\"*}
        ;;
      *'"owner": "ai"'*)
        [ -n "$_path" ] && printf '%s\n' "$_path"
        _path=""
        ;;
    esac
  done < "$LOCK"
}

# --- verify ------------------------------------------------------------------
# THE ONLY COMMAND THAT CAN SEE A BROKEN HOOK. A plain `claude -p` run prints
# its answer and exits 0 whether or not the hook fired, and `--output-format
# json` carries no hook field of any kind, so a hook that cannot even be found
# is invisible in both. The failure surfaces in exactly one place: a
# `hook_response` event on the stream, which needs `stream-json` AND
# `--verbose` together. That is the whole reason this subcommand exists, and
# it is why a green sync is not evidence that the hook works.
cmd_verify() {
  say "tannergolden/ai: verify"
  say ""
  say "  root         $ROOT"

  if [ -f "$LOCK" ]; then
    _tag=$(lock_value resolved_tag)
    [ -n "$_tag" ] || _tag="(none recorded)"
    _sha=$(lock_value resolved_sha)
    [ -n "$_sha" ] || _sha="(none recorded)"
    say "  requested    $(lock_value requested)"
    say "  resolved     $_tag"
    say "  commit       $_sha"
    say "  emitted at   $(lock_value emitted_at)"
    say "  outcome      $(lock_value outcome)"
  else
    say "  lockfile     MISSING. No sync has completed in this repository."
  fi

  if [ -f "$STAMP" ]; then
    say "  synced       $(cat "$STAMP")"
  else
    say "  synced       unknown (.ai/ai.lock.date is missing)"
  fi

  # Staleness is not recomputed here. The hook is run instead, so the
  # installation has one threshold rather than two that can disagree.
  if [ -f "$DISABLED" ]; then
    say "  kill switch  PRESENT (.ai/hooks/.disabled). Every shipped hook exits"
    say "               immediately, so no staleness warning can appear."
  elif [ -f "$ROOT/.ai/hooks/ai-context.sh" ]; then
    _msg=$(CLAUDE_PROJECT_DIR="$ROOT" sh "$ROOT/.ai/hooks/ai-context.sh" 2>/dev/null)
    if [ -n "$_msg" ]; then
      say "  staleness    $_msg"
    else
      say "  staleness    current"
    fi
  else
    say "  staleness    unknown (.ai/hooks/ai-context.sh is missing)"
  fi
  say ""

  if ! command -v claude >/dev/null 2>&1; then
    cat <<'EOF'
  hook         SKIPPED: Claude Code is not on PATH here, so the hook was not
               exercised. THIS IS NOT A PASS. Run this again on a machine
               that has it before trusting the installation.
EOF
    return 0
  fi

  _out=$(claude -p "$PROBE" --output-format stream-json --verbose </dev/null 2>/dev/null)
  _status=$?
  _line=$(printf '%s\n' "$_out" \
    | grep -E '"subtype"[[:space:]]*:[[:space:]]*"hook_response"' \
    | grep -E '"hook_name"[[:space:]]*:[[:space:]]*"SessionStart' \
    | head -n 1)

  if [ -z "$_line" ]; then
    if [ "$_status" -ne 0 ]; then
      say "  hook         UNKNOWN: Claude Code exited $_status and reported no"
      say "               hook event at all. Run the probe by hand to see why:"
      say "                 claude -p '$PROBE' --output-format stream-json --verbose"
      return 1
    fi
    cat <<'EOF'
  hook         FAIL: Claude Code ran and reported no SessionStart hook.
               In order of likelihood: .claude/settings.json has lost this
               publisher's entry; or that file carries an invalid VALUE on a
               known key, which voids the WHOLE file silently and takes the
               repository's own hooks down with it; or this is not the
               directory Claude Code treats as the project root.
EOF
    return 1
  fi

  _ok=yes
  printf '%s\n' "$_line" | grep -qE '"outcome"[[:space:]]*:[[:space:]]*"success"' || _ok=no
  printf '%s\n' "$_line" | grep -qE '"exit_code"[[:space:]]*:[[:space:]]*0([^0-9]|$)' || _ok=no

  if [ "$_ok" = yes ]; then
    say "  hook         PASS: the SessionStart hook ran and exited 0."
    return 0
  fi
  say "  hook         FAIL: the SessionStart hook ran and did not succeed."
  say "               $_line"
  return 1
}

# --- adopt -------------------------------------------------------------------
# The sync refuses, once, when it finds a file it did not write. That refusal
# is the only thing standing between a repository's hand-written law and a bot
# overwriting it with no pull request and no review anywhere. This command
# answers the refusal by MOVING the file into the region the sync injects and
# never overwrites, so the law survives the installation instead of being
# traded for it.
cmd_adopt() {
  if [ ! -f "$ROOT/AGENTS.md" ]; then
    say "No AGENTS.md here, so there is nothing to adopt. The next sync writes one."
    return 0
  fi
  if grep -q "$GENERATED_MARK" "$ROOT/AGENTS.md" 2>/dev/null; then
    say "AGENTS.md here was published by the sync already, so there is nothing to adopt."
    say "Law that is true of this repository only belongs in .ai/local/agents-local.md,"
    say "which the sync folds into AGENTS.md and never writes over."
    return 0
  fi
  if [ -e "$LOCAL_LAW" ]; then
    say "Refusing: both of these already exist."
    say "    AGENTS.md"
    say "    .ai/local/agents-local.md"
    say "Merging them is a judgement call, so it stays with you. Fold AGENTS.md into"
    say ".ai/local/agents-local.md by hand, delete AGENTS.md, then run the sync."
    return 1
  fi

  mkdir -p "$ROOT/.ai/local" || return 1
  mv "$ROOT/AGENTS.md" "$LOCAL_LAW" || return 1
  say "Moved:"
  say "    AGENTS.md  ->  .ai/local/agents-local.md"
  say ""
  say "That file is yours now and permanently. Every sync reads it, folds it into the"
  say "AGENTS.md it delivers, and never writes to it. Commit the move, then run the"
  say "sync: it will stop refusing, because the path it was refusing is free."

  # CLAUDE.md and GEMINI.md are refused on the same terms and are deliberately
  # not moved here. Handling them would mean merging three files into one, and
  # the shape of that merge is the author's decision, not a script's.
  for _router in CLAUDE.md GEMINI.md; do
    if [ -f "$ROOT/$_router" ] && ! grep -q "$GENERATED_MARK" "$ROOT/$_router" 2>/dev/null; then
      say ""
      say "$_router is hand written too, and the sync will refuse it as well. It is"
      say "replaced by a one-line router that imports AGENTS.md, so move anything worth"
      say "keeping into .ai/local/agents-local.md and delete $_router."
    fi
  done
  return 0
}

# --- remove ------------------------------------------------------------------
# The hook entries are described, never edited. `.claude/settings.json` is the
# repository's only committed, team-shared Claude Code configuration; an
# invalid value left in it voids the whole file silently, and the hooks that
# would take down are the repository's own.
print_settings_note() {
  cat <<'EOF'
Still to do by hand, in .claude/settings.json: delete every hook entry whose
command begins with

    bash "$CLAUDE_PROJECT_DIR/.ai/hooks/

and leave every other key, and every other hook, exactly as it is. If that empties
the file of hooks and it had no other keys, the file itself is safe to delete.
EOF
}

cmd_remove() {
  _force=no
  for _arg in "$@"; do
    case "$_arg" in
      --force) _force=yes ;;
      *) say "remove: unknown option: $_arg" >&2; return 2 ;;
    esac
  done

  if [ ! -f "$LOCK" ]; then
    say "No .ai/ai.lock.json here, so there is no manifest and this will not guess."
    say "By hand: delete $STUB, delete .ai/, and remove the hook entries below."
    say ""
    print_settings_note
    return 1
  fi

  say "tannergolden/ai: remove"
  say ""
  say "  The lockfile records these as this publisher's:"
  owned_paths | while IFS= read -r _rel; do say "    $_rel"; done
  say "    (plus the rest of .ai/, which goes with the directory)"
  say "  And the stub that fetches them: $STUB"
  say ""

  if [ "$_force" = no ]; then
    say "  Everything listed above is deleted, including the instruction files. Copy"
    say "  out anything you mean to keep before running this with --force."
    say ""
    if [ -f "$LOCAL_LAW" ]; then
      say "  ONE OF YOUR OWN FILES SITS INSIDE THE DIRECTORY THIS DELETES:"
      say "      .ai/local/agents-local.md"
      say "  Every sync read it and none of them ever wrote it, so --force MOVES it to"
      say "      ./agents-local.md"
      say "  rather than deleting it. Nothing else in .ai/ survives."
      say ""
    fi
    say "  Nothing has been deleted. To go ahead:"
    say "      sh .ai/ai.sh remove --force"
    return 1
  fi

  # The stub goes first. No stub, no sync, so nothing can be re-delivered
  # underneath a half-finished uninstall.
  if [ -f "$ROOT/$STUB" ]; then
    rm -f "$ROOT/$STUB" && say "  removed $STUB"
  else
    say "  $STUB was already gone"
  fi

  # By manifest before directory, so anything delivered outside `.ai/` goes
  # too, and so it is visibly the manifest that does the work.
  owned_paths | while IFS= read -r _rel; do
    # The lockfile is an ordinary file in a repository other people can write
    # to. An absolute path or a `..` in it would carry this `rm` out of the
    # tree, so those are reported and skipped rather than followed.
    case "$_rel" in
      ''|/*|*..*)
        say "  skipped suspicious lock path: $_rel" >&2
        continue
        ;;
    esac
    if [ -e "$ROOT/$_rel" ]; then
      rm -f "$ROOT/$_rel" && say "  removed $_rel"
    fi
  done

  # YOUR LAW LEAVES WITH YOU, NOT WITH THE PUBLISHER. `.ai/local/agents-local.md`
  # sits inside the directory below and was never written by any sync: it is
  # read, folded into the delivered AGENTS.md, and left alone. Uninstalling a
  # publisher must not be able to destroy a file that publisher never wrote,
  # and the dry run's warning is not enough on its own, because the whole
  # point of `--force` is that somebody runs it later from memory. So it is
  # MOVED out first, which is the mirror of what `adopt` does on the way in.
  if [ -f "$LOCAL_LAW" ]; then
    if [ -e "$ROOT/agents-local.md" ]; then
      say "  kept your local law where it is: ./agents-local.md already exists, so"
      say "  .ai/local/agents-local.md was NOT moved and is about to go with .ai/."
      say "  Copy it out now if you want it, then re-run."
      return 1
    fi
    mv "$LOCAL_LAW" "$ROOT/agents-local.md" \
      && say "  kept your local law: .ai/local/agents-local.md -> ./agents-local.md"
  fi

  rm -rf "$ROOT/.ai" && say "  removed .ai/"
  say ""
  print_settings_note
  say ""
  say "The manifest is spent, and everything on it is gone, the published AGENTS.md,"
  say "CLAUDE.md and GEMINI.md included. Nothing here will be written from outside"
  say "this repository again. Recover anything you wanted from git history."

  # Exit from inside the function on purpose: `.ai/` has just been deleted and
  # this script was in it. Returning to the dispatcher would leave the shell
  # reading the rest of a file that no longer has a name.
  exit 0
}

case "${1:-}" in
  verify) shift; cmd_verify "$@" ;;
  adopt) shift; cmd_adopt "$@" ;;
  remove) shift; cmd_remove "$@" ;;
  -h|--help|help) usage ;;
  '') usage >&2; exit 2 ;;
  *) say "unknown command: $1" >&2; say "" >&2; usage >&2; exit 2 ;;
esac
