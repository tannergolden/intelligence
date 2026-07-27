<!--
HOSTILE FIXTURE. This file exists to FAIL `actions/ai-sync/check.py`.

A linter that has never failed is not a linter, and the at-strict rule is the
one rule whose failure mode is invisible in a diff: Gemini CLI substitutes an
HTML comment over a failed import token, deleting the directive that shared
the line, and the source bytes and the emitted bytes stay identical.

Expected result: exactly FOUR at-strict violations, on the four lines marked
HAZARD below, and NONE on the two lines marked SAFE. This file is a fixture,
not a document; it is deliberately exempt from the repository's markdown
styling rules and is never published.
-->

# at-strict fixture

HAZARD 1, bare version pin. The commonest accident: a human writes a pin in
prose and Gemini reads it as an import of a file named `v1.2.3`.
Pin the release to @v1.2.3 before cutting it.

HAZARD 2, mention style. Reads to a human as a person and to Gemini as a
path.
Ask @tannergolden to confirm the ruleset.

HAZARD 3, scoped package. The leading at sign is part of the package name and
is not optional, which is why this shape keeps reappearing.
Install @anthropic-ai/claude-code from npm.

HAZARD 4, inside a code span. Backticks are NOT an exemption: strict mode
rejects the token wherever it appears, because porting Gemini's own
backtick-region scan was the most intricate piece in the system and deleting
it costs an author one comment.
The import line is written `as @./AGENTS.md` in the router.

SAFE 1, an email address. There is no whitespace before the at sign, so it is
not a candidate token at all. This is the shape that would break if the rule
were relaxed to a bare search for the character.
Mail tanner@example.invalid to request access.

SAFE 2, the escape hatch. The literal comment on the preceding line permits an
at sign on the next line ONLY, so an author pays one comment per genuine
import and the rule never has to guess.

<!-- ai:allow-at -->
@./AGENTS.md

That trailing line is the end of the fixture; anything added below it is
outside the hatch and will be rejected.
