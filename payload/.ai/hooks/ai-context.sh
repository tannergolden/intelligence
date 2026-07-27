#!/bin/sh
[ -f "${CLAUDE_PROJECT_DIR:-.}/.ai/hooks/.disabled" ] && exit 0
# =============================================================================
# DO NOT EDIT - Published by tannergolden/ai
# SessionStart hook: report a stale sync, and do nothing else
# =============================================================================
# WHY A HOOK LAYER EXISTS AT ALL: the owner requires it. This script is the
# smallest safe first occupant of that layer, not its justification. Read the
# next hook's cost as new cost to be argued for, never as cost already paid.
#
# WHY THE KILL SWITCH IS THE FIRST LINE, ABOVE EVEN THIS COMMENT: it is the
# only consumer-side recall that exists. Moving the major tag back at the
# publisher fixes future runs; it does not reach a machine that already has
# these bytes. Until a sync actually runs here, a bad hook keeps executing on
# every agent session, in every clone, and the stub's schedule is weekly.
# Creating an empty `.ai/hooks/.disabled` from the GitHub web UI takes thirty
# seconds, needs no token, needs no local checkout and needs nobody at the
# publisher. Nothing may ever be added above that line.
#
# WHY IT IS INVOKED AS `bash "<path>"`: the transport that delivers this file
# writes contents and paths only, with no file mode, so this script cannot be
# relied on to arrive executable. The command string in `.claude/settings.json`
# names an interpreter for that reason, and it is frozen for the life of v1:
# Claude Code has no fingerprint and no re-warning for a changed hook command,
# so rotating one would execute new code in every already-trusted repository
# with no prompt and no signal. All churn belongs inside this file, which is
# recorded in the lockfile with a digest and shows up in a release diff.
#
# WHAT THIS MAY USE: `sh` builtins, `date` and `test`. Nothing else, ever. The
# interpreter is the one dependency that cannot be fixed remotely: a hook that
# reaches for a helper program missing on this machine fails on every session
# forever, and there is no channel back here except another sync. That is also
# why the sync writes a plain one-line date beside the lockfile. Reading a date
# is `read` and arithmetic; reading the JSON lockfile would not be.
#
# WHY IT FAILS OPEN, ON EVERY PATH: this hook is informational and must never
# stand between a person and their session. Only exit 2 blocks, and every path
# here reaches exit 0, including every path that meets something it did not
# expect. The repository this publisher takes its hook patterns from ships two
# hooks that fail CLOSED when an interpreter is absent, one of them on a
# matcher some clients ignore, so a machine that is merely configured
# differently has all of its tool calls blocked. Do not reproduce that here.
#
# WHY THE WARNING GOES TO BOTH CHANNELS: SessionStart stdout is injected into
# the model's context and is never shown to the person, while stderr reaches
# the transcript the person reads and never the model. A warning on one channel
# reaches one audience, and this one is for both of them.
# =============================================================================

ROOT="${CLAUDE_PROJECT_DIR:-.}"
STAMP="$ROOT/.ai/ai.lock.date"

# Four missed weekly syncs. The number is set against the failure actually
# being watched for: GitHub disables a scheduled workflow after 60 days
# without repository activity and says so once, by email, to one person. A
# repository whose schedule quietly died is the case nothing else reports.
MAX_AGE_DAYS=30

# One line, both channels, then out. Warning twice would be worse than not
# warning at all: this text lands in the model's context on every session.
warn() {
  printf '%s\n' "$1"
  printf '%s\n' "$1" >&2
  exit 0
}

# Splits YYYY-MM-DD into PY, PM, PD. Leading zeros are stripped because shell
# arithmetic reads 08 and 09 as malformed octal, which is a hard error in some
# shells and a wrong answer in others. `local` is not POSIX, so the working
# names are prefixed and deliberately global.
parse_date() {
  PY=${1%%-*}
  _rest=${1#*-}
  PM=${_rest%%-*}
  PD=${_rest#*-}
  PD=${PD%%[!0-9]*}
  PM=${PM#0}
  PD=${PD#0}
  [ -z "$PM" ] && PM=0
  [ -z "$PD" ] && PD=0
  # Explicit, because the guard above returns 1 in the ordinary case and a
  # later editor should not inherit a function that reports failure on success.
  return 0
}

# Days since 1970-01-01, by the standard civil-to-days algorithm, in shell
# arithmetic. Written out because the portable alternatives are not portable:
# GNU `date` spells relative dates `-d`, BSD `date` spells them `-v`, and a
# hook that guesses wrong either says nothing or states a number that is false.
days_from_civil() {
  _y=$1
  _m=$2
  _d=$3
  [ "$_m" -le 2 ] && _y=$((_y - 1))
  _era=$((_y / 400))
  _yoe=$((_y - _era * 400))
  if [ "$_m" -gt 2 ]; then
    _mp=$((_m - 3))
  else
    _mp=$((_m + 9))
  fi
  _doy=$(((153 * _mp + 2) / 5 + _d - 1))
  _doe=$((_yoe * 365 + _yoe / 4 - _yoe / 100 + _doy))
  DAYS=$((_era * 146097 + _doe - 719468))
}

STAMPED=""
[ -r "$STAMP" ] && IFS= read -r STAMPED < "$STAMP" 2>/dev/null

# A missing stamp is a repository condition, not an environment problem, and
# it is worth saying: either no sync has ever completed here, or something
# removed the file. Both are the same instruction to the reader.
[ -n "$STAMPED" ] || warn "tannergolden/ai: this repository has no .ai/ai.lock.date, so nothing here records its agent instructions ever being synced. If .github/workflows/ai-sync.yml exists, run it from the Actions tab."

# Trailing junk is tolerated (a carriage return from a checkout on another
# platform is the realistic case); a stamp that is not a date at all is not,
# and there is nothing true to say about it, so say nothing.
case "$STAMPED" in
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*) ;;
  *) exit 0 ;;
esac
# Then drop the tolerated junk, because the stamp is quoted back to the reader
# and a stray carriage return inside a message returns the cursor to the start
# of the line, overwriting the half of the warning already printed.
STAMPED=${STAMPED%%[!0-9-]*}

# An unusable `date` is an environment problem. Fail open and stay silent:
# the person cannot act on it and the model does not need it.
NOW=$(date +%Y-%m-%d 2>/dev/null) || exit 0
case "$NOW" in
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]) ;;
  *) exit 0 ;;
esac

parse_date "$STAMPED"
days_from_civil "$PY" "$PM" "$PD"
SYNCED_DAY=$DAYS

parse_date "$NOW"
days_from_civil "$PY" "$PM" "$PD"
TODAY=$DAYS

AGE=$((TODAY - SYNCED_DAY))
# A negative age means a clock disagreement, not a stale repository.
[ "$AGE" -gt "$MAX_AGE_DAYS" ] && warn "tannergolden/ai: the agent instructions in this repository were last synced on $STAMPED, $AGE days ago. Run the 'Sync AI Instructions' workflow from the Actions tab, and check that its weekly schedule is still enabled: GitHub disables scheduled workflows after 60 days without repository activity."

exit 0
