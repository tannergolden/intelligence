<!--
HOSTILE FIXTURE. This file exists to FAIL `actions/ai-sync/check.py`.

The invisible rule is the only check in the suite that catches a defect class
a human provably cannot catch by reading a diff. Every other rule guards
something a careful reviewer could in principle spot; a zero-width space and a
bidi override render as nothing and as ordinary text respectively, in the
diff, in the review UI, and in the terminal.

Expected result: exactly NINE invisible violations, one per marked line. This
file carries no at sign and no branch-form permalink, so any other rule firing
here means that rule has a false positive.

The last seven were added after a review found the rule stopping one codepoint
short of U+200E and U+200F. A widened regex with an unwidened fixture proves
nothing: CI asserts only that the rule FIRED, so every codepoint the rule
claims to cover needs a line here that would pass without it.

The two lines below LOOK ordinary. That is the entire point, and it is why
this fixture has to exist rather than being described in a comment: the only
honest way to prove the rule works is to hand it bytes a reviewer would pass.
-->

# invisible fixture

HAZARD 1, zero-width space (U+200B). It sits inside the word "config" on the
next line, splitting a token that a reader, a grep and a spellchecker all see
as one word.

The confi​g file is loaded on every session.

HAZARD 2, right-to-left override (U+202E). It sits before the word "reverse"
on the next line and flips the rendering of everything after it, so what a
reviewer reads and what the model receives are different sentences.

Never run ‮reverse this command.

HAZARD 3, left-to-right mark (U+200E). One codepoint past where this rule used
to stop, and a directional control of the same class as HAZARD 2.

Never‎ run this command.

HAZARD 4, right-to-left mark (U+200F). The other half of the pair.

Never‏ run this command.

HAZARD 5, word joiner (U+2060). Zero width, and specified as non-breaking, so
it is a zero-width space by another name.

Never⁠ run this command.

HAZARD 6, soft hyphen (U+00AD). Renders as nothing until a line breaks there.

Never­ run this command.

HAZARD 7, combining grapheme joiner (U+034F). Renders as nothing anywhere.

Never͏ run this command.

HAZARD 8, hangul filler (U+3164). A letter with no glyph, so it reads as a
space and is not one.

Neverㅤ run this command.

HAZARD 9, halfwidth hangul filler (U+FFA0). The same trick, in a different
block, which is why the rule names both.

Neverﾠ run this command.
