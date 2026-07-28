#!/bin/sh
# =============================================================================
# skill-router.sh - name the installed skills before the model answers
# =============================================================================
# FIRES ON EVERY PROMPT, at the BeforeAgent event. That makes its output the
# highest-frequency cost in this entire system: nothing else here is paid per
# turn. Every byte printed below is charged again on the next message, and the
# one after that, for the whole session.
#
# Two consequences, both deliberate:
#
#   1. It prints NOTHING when no skills are installed, so a repository that
#      does not use them pays exactly zero.
#   2. It names skills rather than lecturing. The model already holds every
#      skill description; what a reminder adds is a retrieval cue, and a cue
#      is a list of names, not a paragraph of advice.
#
# TWO DIRECTORIES, NOT ONE. Gemini CLI discovers skills under `.gemini/skills`
# and under `.agents/skills`, the second being an official alias. A router
# reading only the vendor path silently misses every skill installed to the
# shared one, which is the path this publisher's own guidance recommends.
#
# `check-docs.py` enforces a byte ceiling on what this prints. Raising it is
# a commit somebody reviews.
# =============================================================================
set -eu

root="${GEMINI_PROJECT_DIR:-.}"
found=""

for base in .gemini/skills .agents/skills; do
	for dir in "$root"/"$base"/*/; do
		[ -f "$dir/SKILL.md" ] || continue
		name=$(basename "$dir")
		# The same skill can sit in both directories. Name it once.
		case ", $found," in *", $name,"*) continue ;; esac
		found="${found}${found:+, }${name}"
	done
done

[ -n "$found" ] || exit 0

printf 'Skills installed here: %s.\n' "$found"
printf 'If one fits this request, use it instead of working unaided.\n'
