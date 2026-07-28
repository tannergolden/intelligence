# Running The Checker

Every way a skill can be wrong is silent. A missing `SKILL.md` is a directory nothing discovers, a `name` that disagrees with its directory is found under one name and invoked under another, and a body over the size guidance is not rejected at all: it just costs the whole session. None of that is visible by re-reading your own work, which is why this step is a tool rather than a review.

## In a repository that already has it

Read what the repository defines before running anything. A `Makefile` with a `lint` target, a `package.json` script, a CI workflow: whichever it is, that is the command. A command that appears in none of them does not exist there.

Where this publisher's own layout is in use, it is:

```bash
make lint
```

## In a repository that has never seen it

The checker is published as a composite action, so a repository with skills can gate them without copying anything:

```yaml
- uses: tannergolden/ai/actions/check-skills@v1
  with:
    path: skills
```

Pin the moving major to receive fixes, or a full `vX.Y.Z` for exactness.

To run it once without adding a workflow, check the publisher out and invoke the script directly. It is standard library only, so there is nothing to install:

```bash
git clone --depth 1 https://github.com/tannergolden/ai /tmp/ai-checker
python3 /tmp/ai-checker/scripts/check-skills.py path/to/skills
```

## What a clean run does not prove

The checker decides what a machine can decide: field shapes, size ceilings, portability hazards, references that resolve. It cannot tell you whether the description will actually summon the skill, and that is the defect that costs the most, because a skill that never fires produces no error and no log line.

Only the eval comparison answers that. Read `evaluation.md`, and compare against not having the skill at all rather than against nothing.

## What it warns about rather than failing

A warning is a rule whose false positives would cost more than its misses. A description that never says **when**, a body over roughly 5,000 tokens, a machine-specific path, a missing eval suite, a bundled `scripts/` directory: each is usually a defect and occasionally deliberate. Read them, then decide. A warning nobody reads is a warning that should have been an error or should not exist.
