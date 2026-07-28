#!/bin/sh
# =============================================================================
# skill-router.sh - name the installed skills before the model answers
# =============================================================================
# FIRES ON EVERY PROMPT. That makes its output the highest-frequency cost in
# this entire system: nothing else here is paid per turn. Every byte printed
# below is charged again on the next message, and the one after that, for the
# whole session. Claude Code does NOT truncate this stream (measured: 15,024
# characters passed through whole), so the discipline has to live here.
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
	found="${found}${found:+, }${name}"
done

[ -n "$found" ] || exit 0

printf 'Skills installed here: %s.\n' "$found"
printf 'If one fits this request, use it instead of working unaided.\n'
