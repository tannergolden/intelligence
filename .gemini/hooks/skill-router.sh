#!/bin/sh
# =============================================================================
# skill-router.sh - name the installed skills before the model answers
# =============================================================================
# FIRES ON EVERY PROMPT, at the BeforeAgent event. That makes its output the
# highest-frequency cost in this entire system: nothing else here is paid per
# turn. Every byte printed below is charged again on the next message, and the
# one after that, for the whole session.
#
# THE OUTPUT IS JSON, AND THAT IS NOT COSMETIC. Gemini CLI parses hook stdout
# as JSON. Plain text does not fail loudly: it is converted to a `systemMessage`
# that is shown to the USER in transcript mode and never reaches the model at
# all. The only path into the request is `hookSpecificOutput.additionalContext`.
# An earlier version of this file printed prose, so it injected nothing and put
# a line in the operator's terminal on every prompt, and every gate here passed
# it: valid shell, non-empty, under budget, and completely inert.
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
		# A directory name is attacker-controlled in any repository that takes
		# contributions, and it is interpolated into a JSON string below. A
		# quote or backslash would emit invalid JSON, which by the same vendor
		# rule degrades to a user-facing message and reaches the model not at
		# all. Anything outside the specification's name class is not a skill.
		case "$name" in *[!A-Za-z0-9._-]*) continue ;; esac
		# The same skill can sit in both directories. Name it once.
		case ", $found," in *", $name,"*) continue ;; esac
		found="${found}${found:+, }${name}"
	done
done

[ -n "$found" ] || exit 0

# The enumeration and nothing else, wrapped in the only envelope the model
# ever sees. An imperative attached to it would assert more than the list
# supports: this sees workspace skills only, while Gemini also loads personal
# and extension ones.
printf '{"hookSpecificOutput":{"hookEventName":"BeforeAgent","additionalContext":"Skills installed here: %s."}}\n' "$found"
