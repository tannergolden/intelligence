---
name: '[skill-name]'
description: "[What it does, in one sentence. Use when the user asks to ..., with 4 to 6 concrete trigger phrases in the user's own words, even if they never say the skill's name. This line decides whether the skill ever fires.]"
license: "[the repository's licence, such as MIT]"
metadata: { 'team': '[team-name]', 'version': '1.0.0' }
---

# [emoji] [Skill Name]

<!-- Copy this file to the new skill's folder as SKILL.md (keep no t-SKILL.md there); it is named t-SKILL.md here so
     a packaged develop carries exactly one SKILL.md. Copy skill-Changelog.md to Changelog.md and skill-License.txt to
     License.txt beside it. Keep the frontmatter on one line per key: some loaders read nothing else. metadata.team
     names the team this skill dispatches; drop it for a skill with no team. Add allowed-tools only to pre-approve
     read-only tools, such as "allowed-tools: Read, Grep, Glob". The real per-complexity dispatch is the
     "Dispatch scaling" section below, in the body. -->

<!-- BODY SKELETON: every skill mirrors this spine, in this order (references/architecture.md). Title a slot for the
     skill's own domain if it helps (a Modes table may be Tiers); insert domain sections between the pipeline and
     Quality bars; never reorder the spine. Drop Conformance if the skill never writes into a repository. -->

[One paragraph: what the skill does and its one standard, the principle that wins every conflict.]

> Operating doctrine lives in `references/`. Read [the key reference] before [the key step].

## Modes

[The operational table: the axis this skill runs on. First, so the reader learns how to invoke it before anything else.]

| Mode       | Trigger   | What it does   |
| ---------- | --------- | -------------- |
| **[mode]** | [trigger] | [what it does] |

## The architecture it serves

This skill dispatches the **[team-name]** team (`<agent-home>/[team-name]/`). Agents are referenced by name and routed by their description; nothing is copied locally. On Publish, the referenced agents are vendored into this skill's `agents/` so the package is self-contained.

## [Pipeline]

[The main method, named for the skill. Numbered steps from request to delivery.]

1. [step]
2. [step]

## Dispatch scaling

- Light task: dispatch [the smallest useful subset].
- Standard task: dispatch [more of the roster].
- Full task: dispatch the whole roster, the star lead last for synthesis or the gate.

## Conformance with the repository

[Only for a skill that writes into a repository; drop this section otherwise.] Read the repository's `AGENTS.md` and the documents it names, and the rules of every folder written into; follow its rules for backups, deletes and structure; run the checks it names as the exit gate.

## Gotchas

- [What went wrong before, and the rule that prevents it.]

## Quality bars

- [The one standard, stated first.]
- No em dashes anywhere; the validator fails on the character unless the repository allows it.
- [Other non-negotiables.]

## Boundaries

- Stay within [scope]. Never [the hard limits]. [confirm-first or write rules if it writes into a repository.]
- vs [adjacent skill]: [the ruling that prevents overlap].
