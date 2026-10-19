---
name: develop
description: Builds, updates and improves Agent Skills, and the agents and teams they dispatch, so a skill loads and works in every coding app. Decides first whether the need is a skill at all or belongs in a rule, a hook or a script; researches before writing; reuses an agent before creating one; gates every build with a deterministic validator and independent reviewers; and learns from a skill's mistakes. Use when the user asks to build, create, write, add, package, share, fix or improve a skill, an agent, a team of agents, a slash command or a reusable procedure, or says an agent keeps getting the same multi-step task wrong, even if they never say skill.
license: MIT
metadata: { 'team': 'Development', 'version': '04.00.00' }
---

# 🏭 Develop - the skill and agent factory

Develop builds skills, the single-file agents they dispatch, and the team rosters that group those agents, in any repository and for every coding app. It is the one skill that creates other skills, and it improves them and itself after a mistake. It is lean by design: it ships the parts the evidence justifies and grows the rest by demand.

> Operating doctrine lives in `references/`. Read `references/architecture.md` before a build.

## Modes

| Mode                 | Trigger                                                                | What it does                                                                                                                                                                       |
| -------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Create** (default) | "build a skill", "create an agent", "make a team"                      | The full pipeline below.                                                                                                                                                           |
| **Update**           | "improve this skill", "/develop update PATH"                           | A scoped change to an existing skill or agent, then the gate.                                                                                                                      |
| **Recursive**        | "the skill made a mistake", "fix what it got wrong", "learn from this" | Self-improvement: a blameless postmortem to a minimal fix, applied on approval, verified independently, frozen as a regression case. Works on any skill, including develop itself. |
| **Publish**          | "package this", "get this ready to share"                              | Vendor the referenced agents into the skill and build the distributable archive.                                                                                                   |

## The architecture it serves

- **Agents are single files** in `<agent-home>/<team>/<role>.md`, grouped into folders named for the real professional team that is the agent's home (the standard: `references/agent-standard.md`, the layout: `references/architecture.md`). One capability each; the `description` is the routing key; the `title` and `name` are unique across every agent home.
- **A team is its folder.** Each team folder carries a namesake roster (`<agent-home>/<team>/<team>.md`) that lists member agents by title and stars the lead. A team owns no agents elsewhere; another team reuses one by naming it in its own roster.
- **Skills are folders** where their tier puts them: a universal skill in tannergolden/intelligence's `skills/`, a repository's in its `.agents/skills/` and `.claude/skills/`, and a skill bound for the Claude app in a `.skill` archive (`references/architecture.md`). A skill that dispatches a standing team names it in `metadata.team`, and the validator rejects a team that does not resolve to a staffed roster.
- **Reference locally, vendor on export.** Day to day a skill references its team's agents by name; only Publish copies them into the skill's `agents/` so a shipped skill is self-contained. Develop itself is published: its Development team ships inside it, in `agents/`, so it runs in any repository.

## Create pipeline

1. **Decide what it is.** Build a skill only for a procedure an agent runs on request:

   | The need                                        | Where it goes                                                                           |
   | ----------------------------------------------- | --------------------------------------------------------------------------------------- |
   | A multi-step procedure an agent runs on request | A skill                                                                                 |
   | Behaviour that must hold in every session       | A rule: `CONSTITUTION.md` in tannergolden/intelligence, or the repository's `AGENTS.md` |
   | Something that must never happen                | A hook or a CI check; prose alone is not enough                                         |
   | A deterministic transformation                  | A script, bundled in the skill that uses it, or the repository's own tooling            |
   | A fact about the setup, not an instruction      | The knowledge facts in tannergolden/intelligence                                        |

   In one published evaluation a skill was never invoked in 56% of cases, so never put anything that must always hold in a skill. If the user asked for a skill and the need is really a rule or a hook, say so and propose that instead.

2. **Requirements** (interactive, inline): develop runs this itself; mine the request, ask only the gaps, decide who should have the skill (its tier), and lock a requirements note in the run workspace.
3. **Research** (mandatory): never author from memory. Start from real work: a task an agent actually did or got wrong. Then use the repository's own research skill when it has one, or search and read primary sources with the tools at hand, depth-scaled. For a team skill, name the real-world team it mirrors.
4. **Reuse-first design**: search the existing skills and the agent homes by capability (each `description`). For each role, decide reuse, extend, or create. Reuse is advisory: take a clean fit, otherwise author the right agent in its home team folder, and do not mint a new team folder when an existing one fits. Two skills whose descriptions overlap steal each other's triggers: merge rather than duplicate. Design the team roster and the skill (its `metadata.team` and its body dispatch-scaling rule).
5. **Build**: author any new agents from `templates/agent.md` into their team folder; write or update the team's namesake roster from `templates/team.md`; write the skill from `templates/t-SKILL.md` (renamed `SKILL.md`), `templates/skill-Changelog.md` and `templates/skill-License.txt` into the folder its tier gives it, with the full mandatory structure (below). Where the repository keeps an index of its agents, refresh it with the repository's own tooling.
6. **Gate** (both, in parallel, both must pass): the deterministic validator, `python3 scripts/validate.py skill <folder>` (with `--agents <agent home>` for a team kept outside the skill), plus the checks the repository's own `AGENTS.md` names; and the Development team's fresh-context independent reviewers, the QA Engineer and the Application Security Engineer, who never touch the build (the QA Engineer runs the validator and tests; neither holds `edit`) and never review their own work. The fix loop resumes the builder on cited issues only.
7. **Trigger check + test-drive** (tiered): every build gets a light trigger check against the skill's own should-trigger and near-miss set (`assets/trigger-evals.json`; develop's own set is the worked example). Activation is proven by observing a skill tool call in a real run, never by reading the description. Reserve the full smoke test and the with-skill-versus-baseline test-drive for the Publish or complex tier; a skill that does not beat no skill is not done.
8. **Ship** by its tier: a universal skill goes into tannergolden/intelligence's `skills/` with its trigger test in `evals/skills/<name>.json`, then `make render` and `make check`, in a pull request a release delivers; a repository's skill commits both copies in one pull request; at Publish, `python3 scripts/package.py <folder> --agents <agent home>` vendors the team and builds the `.skill` archive.

## How develop runs: it dispatches the Development team

Develop builds with its Development team, whose specs ship in `agents/`, named in its `metadata.team`. When it orchestrates, develop embodies the team's ★ Engineering Lead (Maxwell). Develop runs the interactive requirements and the research itself, then dispatches the team's roles for the build, each briefed from scratch per `references/orchestration.md` with the skill-specific objective: the **Software Architect** designs the skill or agent, the **Full-Stack Engineer** writes the files, and the **QA Engineer** and **Application Security Engineer** verify it independently in a fresh context. The deterministic validator is a script, not an agent. The premium seat is that independent verification: a builder cannot honestly review its own work, so the reviewers arrive fresh, never "now check your work." The one rule that never bends, which the team's own roster also enforces, is that the reviewer is a fresh context, never the builder grading itself. Where the app cannot start a subagent, follow the fallback in `references/orchestration.md` and ask your user to review.

## Dispatch scaling

Scale the Development team to the build. A single-agent or roster edit runs the Full-Stack Engineer plus the validator, adding the QA Engineer for anything non-trivial. A full skill build runs requirements (interactive, with develop), then the Software Architect, then the Full-Stack Engineer, then the QA Engineer and Application Security Engineer and the validator in parallel, then a builder fix loop on cited issues only. The fresh-context reviewers are the premium seats; keep them whenever the result will be used unattended. Recursive mode adds the blameless postmortem, run interactively with develop.

## Self-improvement (Recursive mode)

Develop improves other skills and itself. The loop: capture the failure from the transcript and notes; run a blameless postmortem to the root cause, not the symptom; design the minimal corrective diff; **propose, then apply only on approval**; verify independently (re-run `scripts/validate.py` and the repository's own checks, a scoped re-audit by a fresh QA Engineer, joined by the Application Security Engineer where the change is security-relevant, and a trigger check if the description changed); and append a frozen case to the skill's `assets/regression-cases.jsonl` that every future self-edit must re-pass. Self-correction is trusted only against an oracle (the validator, a test, a golden example), never on the model's own say-so, and the no-self-grading rule holds even when develop edits develop.

## Mandatory output structure (every skill develop builds)

```
<skill>/
  SKILL.md          frontmatter (name, description, license, metadata) + body; from templates/t-SKILL.md
  License.txt       the licence text; the repository's licence by default
  Changelog.md      version history from templates/skill-Changelog.md, starting at 01.00.00
  assets/           static files the skill ships, including assets/trigger-evals.json
  references/       domain knowledge loaded on demand
  templates/        output scaffolds the skill fills in
  scripts/          only for helpers no repository engine provides, so the skill runs anywhere
  agents/           only in a published skill: its team, vendored
```

Every file sits at most one folder below `SKILL.md`, and the skill holds exactly one file named `SKILL.md`. The `SKILL.md` **body** follows the canonical skeleton in `references/architecture.md` (Modes, the architecture it serves, the pipeline, dispatch scaling, conformance with the repository, quality bars, boundaries), scaffolded by `templates/t-SKILL.md`. Every skill mirrors it and never reorders the spine. The frontmatter keeps one line per key, `metadata` included as a one-line map, because some loaders read nothing else. A repository may ask for more beside it, such as a folder note or a file log; follow its rules.

## Conformance with the repository

A repository's rules change: its frontmatter, its naming, its layout. So develop never freezes a copy of a repository rule inside a skill or a reference, because a frozen copy drifts the moment the rule changes. For any repository rule, develop reads the live rules (the root `AGENTS.md`, the documents it names, and the rules of every folder it writes into) and runs the checks the repository names, which already track its current rules. `scripts/validate.py` checks only what is true of a skill in every repository. Every skill develop builds, and develop itself, is held to the repository as it is now, not as it was when the skill was written.

## Gotchas

- A skill named in the user's request but never triggered in tests is not finished; fix the description first.
- In the apps that read it, `allowed-tools` pre-approves the tools it lists while the skill runs. List read-only tools at most; a skill that writes or runs commands goes through the session's own permissions.
- A skill that fetches from the network or installs packages when it loads will fail in sandboxed apps; bundle what it needs or document the requirement in `compatibility`.
- A universal skill is never copied into a home folder by hand: the home kit installs it, and replaces only the folders it owns.

## Quality bars

- **Agents** follow `references/agent-standard.md` (single file, header plus bracketed body, cut decorative persona, comprehensive by coverage).
- **No em dashes** anywhere in a generated skill or agent; the validator fails on the character unless the repository allows it.
- **Tools declared with least privilege**: an agent's `tools` hold only the capabilities its role needs, and a skill pre-approves read-only tools at most.
- **Descriptions** are written to trigger: `references/descriptions.md`.
- **Repository-resident skills** honor the repository's own contract (its instructions, its checks, its rules for writing and deleting).

## Boundaries

- Stay within building, updating, and improving skills, agents, and teams. Never rename an existing skill's `name` or its directory; installed users lose it on a rename.
- Apply a self-improvement diff only on explicit approval, and never self-grade a fix; verification is the validator, a fresh reviewer, and the regression ledger.
- Inside a repository, follow its rules: confirm before any delete or structural change, and back up where its rules ask. Reference agents from the agent home; vendor them into a skill's `agents/` only at Publish.

## Bootstrap

Develop began as a hand-authored v0, because the first factory cannot build itself (the self-hosting problem). It now dispatches its Development team for design, build, and independent verification. Before its output is trusted, it is checked against the golden set in `assets/golden-set.md` with a person as the fresh reviewer. From here, develop builds the other skills and rebuilds later versions of itself, each gated by the validator, the team's independent reviewers, and the regression ledger.
