# Architecture - the model the build mode builds into

Read this before any build. It is the shape of the system the build mode produces; everything else serves it.

## Three kinds of thing

- **Agent**: one Markdown file in `<agent-home>/<team>/<role>.md`, living in its home team folder. One capability. Its `description` is the routing key; its `title` (the role) is its identity, unique across every agent home; an agent carries no personal name. The folder groups by real professional team; it is cosmetic to invocation (the model routes by title and description) but is the human-browsable org chart.
- **Team**: a folder named for a real professional team, carrying a namesake roster `<agent-home>/<team>/<team>.md`. The roster lists `members` (agent titles) and a `lead`. A team owns no agents elsewhere; it references them, and a roster may name a member whose home is another team folder. The body holds dispatch order and conflict rules.
- **Skill**: a folder whose name is the skill's `name`, holding a `SKILL.md`. It names its team in `metadata.team` and scales dispatch in its body. Where it lives depends on who should have it (below).

## Four rules that govern the model

1. **Reference locally, vendor on export.** Day to day, a skill references its team's agents by name and routes by description; nothing is copied. Only at Publish are the referenced agents copied into the skill's `agents/`, making a shipped skill self-contained. The library is always present locally, so local copying would only create drift. Where a skill's own `agents/` is its team's agent home, as in tannergolden/intelligence, the team is always inside the skill and Publish has nothing to vendor.
2. **Parameterized capability.** An agent spec encodes a broad capability. The skill-specific objective, inputs, and boundaries are injected by the dispatch brief at call time. One agent serves many skills; each call is anchored by its brief. Capability in the spec, objective in the brief.
3. **Rule of Three, repointed.** Every agent is born in an agent home, so there is no skill-local stage to promote from. It survives in three forms: placement (assign each agent a home team at birth, the real profession that owns its capability), consumption (reuse only on a clean capability fit, else author the right one, never force-fit), and team restraint (do not mint a new team folder when an existing one fits). The library grows by demand, not up front.
4. **The lead is marked with a star.** In any roster the lead's title carries the black-star character before its role name. Never a word-label like (lead), never a different glyph.

## Where things live

Decide who should have the skill before writing it, because that decides where it lives and how it ships.

| Who should have it                      | Where it lives                                                                                                                                                                   | How it ships                                                                                                                                                                                                                                                 |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Every repository, every app             | `kit/skills/<name>/` in tannergolden/intelligence, with its team in its own `agents/` and its trigger test in its own `assets/trigger-evals.json`                              | The next release carries it; the home kit copies it into each app's skills folder on every machine, and the cloud setup script into cloud sessions. Never copy it into a home folder by hand: the kit replaces folders it owns and refuses ones it does not. |
| Every repository made from one template | The template's `.agents/skills/<name>/` and `.claude/skills/<name>/`                                                                                                             | The template ships it to each repository generated from it, and its sync keeps it current.                                                                                                                                                                   |
| One repository                          | `.agents/skills/<name>/` for Codex, Copilot, Cursor, Gemini and Antigravity, and the same folder at `.claude/skills/<name>/`, because Claude Code reads nothing under `.agents/` | Commit both copies in one pull request, or let the repository's own engine write them from one source when its rules say so.                                                                                                                                 |
| The Claude app                          | A `.skill` archive built at Publish                                                                                                                                              | Upload it in the app. An uploaded skill is on in all your chats there, so only a skill meant for every conversation belongs in the app.                                                                                                                      |

Never ship the same skill name at two levels: two copies leave it to the app which one runs. A repository adjusts a universal skill through its own rules, never through a second copy; tannergolden/intelligence writes every universal skill, and a repository made from the knowledge template keeps none of its own (tannergolden/intelligence ADR-0037).

The **agent home** is where a repository keeps agent specs: the folders its rules name, such as a knowledge vault's team folders. A repository with none keeps a skill's team inside the published skill, in `agents/`, as this skill does. In tannergolden/intelligence every universal skill keeps its own team in its own `agents/`, which `.github/scripts/kit.py` requires, and a seat another department needs is borrowed by title from the skill it lives in, never copied. A subagent every repository should have lives in tannergolden/intelligence's `kit/subagents/`, which renders it for each app.

## Where the build mode writes

| Artifact        | Path                                     | When                                                                       |
| --------------- | ---------------------------------------- | -------------------------------------------------------------------------- |
| New agent       | `<agent-home>/<team>/<role>.md`          | authored on a clean-fit miss, into its home team folder                    |
| Team roster     | `<agent-home>/<team>/<team>.md`          | the team folder's namesake, per team                                       |
| Skill source    | the folder its tier gives it, above      | every build                                                                |
| Derived index   | wherever the repository's rules keep one | refreshed by the repository's own tooling after an agent or roster changes |
| Vendored agents | `<skill>/agents/`                        | only at Publish                                                            |

## The canonical SKILL.md skeleton

Every skill's `SKILL.md` body follows one skeleton, so all skills read the same and a reader learns the shape once. This skill's own `SKILL.md` is the exemplar; `templates/t-SKILL.md` scaffolds it. The spine order is fixed: a skill may title a slot for its own domain (a `## Modes` table may be `## Tiers`, the run may be named for its pipeline) and may insert domain sections between the run and `## Quality bars`, but it never reorders the spine.

1. `# <emoji> <Name> - <identity>`, then a one-paragraph intro (what it does, for whom, and its one standard), then `> Operating doctrine lives in references/...` when the skill has references.
2. `## Where it runs` - read the repository's own instructions first (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files, and the documents they name); they decide what the skill reads and where it keeps anything, and the user's personal context goes only into a repository made to hold it.
3. `## Modes` - the operational table: the axis the skill runs on (modes, tiers). Early, so the reader sees how to invoke it before anything else.
4. `## The team it dispatches` - the architecture the skill serves: the team its `metadata.team` names, its lead and members, any seat it borrows from another skill, and the reference-then-vendor rule.
5. `## How a run works` - the main method, named for the skill (a Create pipeline, an intake-to-ship flow).
6. `## Dispatch scaling` - the smallest-sufficient dispatch, scaled to the task.
7. `## The write-gate` - for a skill that writes into a repository: the preflight, conformance with the repository's live rules and the checks it names (never a frozen copy of them), what is written once verified, and what waits for the user's explicit confirmation.
8. `## Quality bars` - the non-negotiable quality rules, as a bulleted list.
9. `## Boundaries` - the scope limits and the vs-other-skills rulings.

A skill without a team folds slots 4 and 6 into its method; a skill that never writes into a repository drops slot 7. Everything else is present and in order. This skill's own `SKILL.md` closes with a `## Bootstrap` origin note: that section is research-and-development's alone, the skill builder's self-hosting story, which the validator rejects in any other skill.

## Write it from real work

1. Start from a task an agent actually did or got wrong. Capture the steps that worked, the corrections it needed, and its exact inputs and outputs.
2. Cut every line the agent would get right without being told. The body stays loaded for the rest of the session, so each line costs every turn.
3. Give one default, not a menu. Match freedom to fragility: prose where several approaches work, an exact command where one mistake breaks things.
4. Write standing instructions ("run the tests after every edit"), and put the most important ones first: after compaction only the opening 5,000 tokens survive.
5. Keep a `## Gotchas` section in `SKILL.md` itself, where the agent will see it.
