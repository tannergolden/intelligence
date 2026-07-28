---
name: develop
description: Use this skill when the user is writing, fixing, reviewing, or packaging an Agent Skill, or when they describe a skill that never triggers, fires on the wrong requests, has grown too long, or behaves differently in one tool than another. Applies whenever a SKILL.md is being created or edited, even when the user does not call it a skill. Not for using an installed skill or for writing an agent instruction file; this is for authoring the skill itself.
---

## Decide whether it should be a skill

A skill earns its place when guidance is **reused** and **conditional**. Guidance that applies to every task in the repository belongs in the always-loaded instruction file instead, because a skill that is always relevant is an instruction file with extra steps.

Do not create one for a single task, and do not create one whose whole body is a sentence you could have said directly.

## Write it in this order

**The description comes first, always.** It is the only part loaded into every session whether the skill is used or not, and it alone decides whether the skill is ever invoked. A perfect body behind a vague description runs never.

1. **Name it.** The directory name and the frontmatter `name` must be identical: 1 to 64 characters, lowercase letters, digits and single hyphens.
2. **Write the description**, framed as an instruction to the agent and slightly pushier than feels natural. Agents under-trigger. Read `references/descriptions.md` before writing it; it is the highest-leverage text in the skill.
3. **Choose the degree of freedom** for each instruction: prose where several approaches work, a concrete procedure where sequence matters, a bundled script where the operation is fragile. Read `references/instructions.md` when deciding how prescriptive to be.
4. **Write the body as navigation.** It stays in context for the whole session once invoked and is never re-read, so every line is a recurring cost. Under 500 lines.
5. **Push detail into `references/`**, and name each one with the **condition** that should send an agent to it, not just its subject.
6. **Bundle a script** if the agent would otherwise rebuild the same logic every run. Read `references/scripts.md` before writing one.
7. **Write the evals** and compare against not having the skill at all. Read `references/evaluation.md` before believing it works.
8. **Check portability**, then run a checker over the skill directory. Read `references/checking.md` for what to run, in this repository and in one that has never seen this skill.

## Three tiers, three costs

| Tier | What | Loads | Cost |
| :--- | :--- | :--- | :--- |
| A | `name` and `description` | at startup, for every skill, used or not | always paid |
| B | the `SKILL.md` body | on invocation | persists the whole session |
| C | files under `references/`, `assets/`, `scripts/` | only when the body sends the agent there | zero until used |

Keep tier A short so a skill nobody uses costs nothing. Keep tier B navigational so an invoked skill does not crowd out the work. Everything else belongs in tier C.

## What belongs in the body, and what does not

**Include** the project's own conventions, the domain procedures an agent cannot infer, the non-obvious edge cases, and the specific tools or APIs to reach for.

**Omit generic knowledge.** Do not explain what a CSV is, how HTTP works, or what a migration does. The agent knows. Every line spent on it is paid again in every session.

**Prefer a default to a menu.** Presenting three equal options makes the agent choose badly. Pick one, say why in a clause, and mention the alternatives briefly.

## Diagnosing a skill that misbehaves

**It never triggers.** Almost always the description, not the body. It is written as what the skill *is* rather than when to *use* it, or it lacks the words a user would actually type. See `references/descriptions.md`.

**It fires on the wrong requests.** The description is too broad, or it names a domain that overlaps a common task. Narrow it and say what the skill is not for.

**It triggers and then gets ignored.** The body is background rather than instruction. Make the steps imperative and standing, and add a validation step so the agent checks its own work before moving on.

**It works for you and not for a colleague.** Something in it is tool-specific. See `references/portability.md`.

**It is right but slow, or costs more than it saves.** That is a real failure and only the eval comparison will show it. See `references/evaluation.md`.

## Reviewing someone else's skill

Read the description alone and ask what request would summon it. If you cannot tell, that is the defect, whatever the body says. Then check that the body carries no generic knowledge, that every bundled file is referenced with a condition attached, and that anything fragile is a script rather than a paragraph of prose.

## Packaging one for distribution

A packaged skill is a ZIP archive holding the skill **folder** at its root. There is no bespoke format. The command-line tools do not read archives at all: they read directories, so a skill is installed by copying its folder into whichever directory the tool discovers. Packaging is only for the web upload and for handing someone a single file.

Run `scripts/package.py <skill-dir>` to build one.

## Additional resources

Each of these is loaded only when its condition applies. Read the one that matches, not all of them.

- `references/descriptions.md` - read **before writing or changing any description**, and first when a skill triggers wrongly. Carries the phrasing pattern, the pushiness rule, and worked examples.
- `references/instructions.md` - read **when deciding how prescriptive to be**, or when a body has grown long and vague. Carries degrees of freedom, the four instruction patterns that work, and the documented anti-patterns.
- `references/scripts.md` - read **before bundling any script**. Carries the signal that one is needed and the interface rules that keep an agent from hanging on it.
- `references/evaluation.md` - read **before shipping**, and whenever a skill is suspected of costing more than it buys. Carries the eval file format and the baseline comparison.
- `references/portability.md` - read **before using any frontmatter field beyond `name` and `description`**, or when a skill behaves differently for different people.
- `references/frontmatter.md` - read **when a field is rejected or you are unsure whether one is portable**. Carries every field, its limit, its allowed shapes, and which tools read it.
- `references/checking.md` - read **before running the checker**, and when a repository has none. Carries the command here, the published action, and what a clean run still does not prove.
- `assets/skill-template.md` - copy this **when starting a new skill**, rather than beginning from a blank file.
- `scripts/package.py` - run this **only when someone needs a single downloadable file**. Installing from the directory needs no packaging step.
