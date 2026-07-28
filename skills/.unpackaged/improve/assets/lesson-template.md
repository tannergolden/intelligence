# Lesson Entry Template

Copy the block below into wherever this repository already keeps its context.
Match the surrounding formatting rather than importing this one: a heading
level that fits the file it lands in beats a heading level that fits this
template.

```markdown
### <The rule, as an instruction rather than a topic>

<What to do, in one or two sentences. Present tense, imperative, no narrative
of how it was discovered.>

**Trigger:** <the situation a future agent will actually be in when this
applies. Without this, the entry is read always or never.>

**Grade:** probed | documented | unverified - <the command and what it
returned, or the primary source and the date it was read.>

**Recorded:** <YYYY-MM-DD>
```

## Worked example

```markdown
### Generate fixtures before running the test suite

Run `make fixtures` once after cloning. The suite does not generate them and
does not say that is what is missing.

**Trigger:** `make test` fails with `fixtures/ not found`.

**Grade:** probed - `make test` on a clean clone exits 1 with that message;
it passes after `make fixtures`.

**Recorded:** 2026-07-28
```

## What each field is defending

**The heading is the rule**, so a reader skimming headings gets the
instructions without reading the bodies. A heading that names a topic
("Fixtures") rather than an instruction makes the skim useless.

**The trigger is what makes it retrievable.** An entry without one is
either read on every task or on none, and both are failures.

**The grade is what stops a guess becoming permanent.** See
`evidence.md` for why an ungraded entry is worse than no entry.

**The date is what lets a reader judge staleness.** An undated claim is
trusted forever by default, including long after it stopped being true.
