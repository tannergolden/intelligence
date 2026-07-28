#!/bin/sh
# =============================================================================
# skill-router.sh - name the installed skills before the model answers
# =============================================================================
# FIRES ON EVERY PROMPT. That makes its output the highest-frequency cost in
# this entire system: nothing else here is paid per turn. Every byte printed
# below is charged again on the next message, and the one after that, for the
# whole session. Claude Code passes hook stdout through verbatim up to 10,000
# characters and replaces anything longer with a ~2.3 KB `<persisted-output>`
# preview plus a file path (bisected on 2.1.220: 10,000 whole, 10,001 replaced).
# So the ceiling below is not about overflow, it is about a cost that recurs on
# every turn: the injection is appended per turn, not refreshed in place, so N
# turns cost N copies.
#
# Two consequences, both deliberate:
#
#   1. It prints NOTHING when no skills are installed, so a repository that
#      does not use them pays exactly zero.
#   2. It names skills rather than lecturing. The model already holds every
#      skill description; what a reminder adds is a retrieval cue, and a cue
#      is a list of names, not a paragraph of advice.
#
# `check-docs.py` enforces a byte ceiling on what this prints. Raising it is
# a commit somebody reviews.
# =============================================================================
set -eu

root="${CLAUDE_PROJECT_DIR:-.}"
found=""

for dir in "$root"/.claude/skills/*/; do
	[ -f "$dir/SKILL.md" ] || continue
	name=$(basename "$dir")
	# A directory name is attacker-controlled in any repository that takes
	# contributions, and this string goes straight into the model's context on
	# every prompt. Anything outside the specification's own name character
	# class is not a skill name and is not repeated.
	case "$name" in *[!A-Za-z0-9._-]*) continue ;; esac
	found="${found}${found:+, }${name}"
done

[ -n "$found" ] || exit 0

# The enumeration and nothing else. An imperative attached to it would assert
# more than the list supports: this sees project-level skills only, while both
# vendors also load personal, plugin and enterprise ones.
printf 'Skills installed here: %s.\n' "$found"
