---
name: develop
description: Creates and improves Agent Skills. Use when asked to write a skill, fix one that never triggers or triggers too often, review a SKILL.md, or split an oversized skill into reference files.
---

## Decide whether it should be a skill at all

A skill earns its place when guidance is **reused** and **conditional**. Guidance that applies to every task in the repository belongs in the always-loaded instruction file instead, because a skill that is always relevant is an instruction file with extra steps.

Do not create a skill for a one-off task, and do not create one whose whole body is a sentence you could have said directly.

## Write it in this order

**The description comes first, always.** It is the only part of a skill loaded into every session whether the skill is used or not, and it alone decides whether the skill is ever invoked. A perfect body behind a vague description runs never.

1. **Name it.** The directory name and the frontmatter `name` must be identical: 1 to 64 characters, lowercase letters, digits and single hyphens. Discovery uses the directory and the listing uses the field, so a mismatch means the skill is found under one name and invoked under another.
2. **Write the description.** What it does and when to use it, in the words a person would actually type. Put the key use case first, because truncation eats the end.
3. **Write the body as navigation, not as content.** Once invoked it stays in context for the whole session and is never re-read, so every line is a recurring cost. State what to do; leave out how and why.
4. **Push detail into `references/`.** Anything long, conditional, or rarely needed costs nothing until the body sends the agent to it.
5. **Write the evals before believing it works.** Triggering is not the same as being correct, and they fail separately.
6. **Check portability**, then run the checker.

## Three tiers, three costs

| Tier | What | Loads | Cost |
| :--- | :--- | :--- | :--- |
| A | `name` and `description` | at startup, for every skill, used or not | always paid |
| B | the `SKILL.md` body | on invocation | persists the whole session |
| C | files under `references/` and `assets/` | only when the body sends the agent there | zero until used |

Every rule worth following comes from this table. Keep tier A short so a skill nobody uses costs nothing. Keep tier B navigational so an invoked skill does not crowd out the work. Put everything else in tier C.

## Diagnosing a skill that misbehaves

**It never triggers.** The description is missing the words a user actually says. Rewrite it around real phrasings, not internal vocabulary. Check the name matches the directory.

**It triggers on everything.** The description is too broad. Narrow it to the cases you want, and name what it is *not* for.

**It triggers and then gets ignored.** The body is guidance rather than instruction, or it has been pushed out by later work. Make the steps imperative and standing, not one-time.

**It works for you and not for a colleague.** Something in it is vendor-specific. See `references/portability.md`.

## Reviewing someone else's skill

Read the description alone and ask what request would summon it. If you cannot tell, that is the defect, whatever else the body says. Then check the body for anything a reference file should hold, and check that every bundled file is actually referenced.

## Packaging one for distribution

A packaged skill is a ZIP archive holding the skill **folder** at its root. There is no bespoke format, no manifest header and no signature. The command-line tools do not read archives at all: they read directories, so a skill is installed by copying its folder into whichever directory the tool discovers. Packaging is for the web upload and for handing someone a single file.

Run `scripts/package.py <skill-dir>` to build one. It writes a `.zip`, because every documented upload path asks for that and installing is the point. It refuses to package a skill whose frontmatter name disagrees with its directory, excludes `evals/` because no agent reads it, and produces byte-identical output from unchanged input so a rebuilt package differs only when the content did.

## Additional resources

- `references/frontmatter.md` - every field, which are required, which are portable, which are banned, and the limits with the reason behind each. Read before writing frontmatter.
- `references/portability.md` - what differs between the supported tools, and the two content forms that behave differently in each. Read before using anything beyond the two required fields.
- `references/evaluation.md` - how to prove a skill beats not having it, and what to measure. Read at step 5, before shipping.
- `assets/skill-template.md` - a starting `SKILL.md` that passes every gate. Copy it rather than starting from a blank file.
- `scripts/package.py` - builds the archive for web upload. Run it only when someone needs a single file; the command-line tools read directories and need no packaging step at all.
