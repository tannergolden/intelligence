<!--
title: '🧰 SKILLS & SUBAGENTS'
description: 'The skills the home kit installs, every one written here and universal, the Agent Resources workforce board dispatches, the Worker and Reviewer subagents, the rules every skill here follows, and where each app reads them.'
type: guide
-->

<div align="center">

# 🧰 SKILLS & SUBAGENTS

<a name="top"></a>

**A procedure an agent opens only when the task calls for it, and two agents it can hand work to.**

_Loaded on demand. Rendered for every app._

</div>

---

## 💡 Skills

A skill is a folder an agent opens only when its description matches the
task. The universal rules stay in the always-loaded block; a skill carries a
procedure. The hub writes every skill the kit carries, and each one works in
any repository, or in a conversation with no repository at all:

| Skill                                              | What it does                                                                                                                                                                                                                                                     |
| :------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`develop`](../../kit/skills/develop/SKILL.md)     | Builds, updates and improves skills and the agents and teams they dispatch: decides whether the need is a skill at all, researches, reuses before it creates, gates every build with its validator and independent reviewers, and learns from a skill's mistakes |
| [`research`](../../kit/skills/research/SKILL.md)   | Runs multi-source, fact-checked research scaled to the question, with cited synthesis                                                                                                                                                                            |
| [`discover`](../../kit/skills/discover/SKILL.md)   | Generates ideas wide from distinct lenses, then converges to a ranked shortlist                                                                                                                                                                                  |
| [`editorial`](../../kit/skills/editorial/SKILL.md) | Writes, edits and formats any prose a person will read, from a message to a book                                                                                                                                                                                 |
| [`visualize`](../../kit/skills/visualize/SKILL.md) | Makes the chart, diagram, timeline or interactive visual that lands better seen than read                                                                                                                                                                        |
| [`finance`](../../kit/skills/finance/SKILL.md)     | Advises on personal and household money: budgets, debt, taxes, investing, insurance, benefits and homes                                                                                                                                                          |
| [`board`](../../kit/skills/board/SKILL.md)         | Founds, runs, scales and maintains a company with the Agent Resources (AR) workforce, scaled to its stage, behind a write-gate                                                                                                                                   |
| [`identify`](../../kit/skills/identify/SKILL.md)   | Interviews the user about themselves with validated frameworks and turns the answers into a profile they approve line by line                                                                                                                                    |

Each skill carries everything it needs in its own folder: its team in
`agents/`, a roster and the agents it dispatches, its references, templates
and assets. `develop` also carries two standard-library scripts in
`scripts/`: `validate.py` checks a skill, an agent, a team or a library
against the format every app accepts, and `package.py` builds a `.skill`
archive for the Claude app, with the team vendored and the same bytes on
every rebuild. Their tests live in
[`.github/scripts/test_develop.py`](../../.github/scripts/test_develop.py),
outside the skill, so they never ship. A skill only one repository needs
lives in that repository's `.agents/skills/` and `.claude/skills/`, never
here.

### Universal, not tied to one repository

No skill names a repository's folders or scripts. Where a skill keeps
anything it makes, a report, an idea, a venture's files, a profile, is set by
the repository's own instructions, its `AGENTS.md` and folder rules, which
the skill reads first, along with the checks those instructions name. With
none, it works in the conversation and writes a file only where the user
asks. A skill writes the user's personal context only into a repository
whose instructions say it was made to hold it (SEC-003); anywhere else that
stays in the conversation. So a repository with a layout of its own, such as
a vault generated from tannergolden/knowledge, states it once in its
`AGENTS.md`, and every skill follows it.

### The Agent Resources (AR) workforce

`board` dispatches the AR workforce, a company's departments as named
agents, each with a star lead, kept as `board`'s own team in
[`kit/skills/board/agents/`](../../kit/skills/board/agents/): one roster for
each department and one file for each agent. **A department keeps at most
its six most critical agents, its lead included**, and `kit.py` refuses a
roster with more. Deeper specialists are not kept on disk: a present chief
stands in for them. `identify` embodies the R&D department's interviewer, and
`research` keeps the Librarian, dispatched only where a repository keeps a
reference collection.

**The checks.** `.github/scripts/kit.py` holds every skill, every agent and
every team to `develop`'s own `validate.py`, and every name and title is
unique across all of `kit/skills/*/agents/`. Each skill's trigger test in
`evals/skills/` is drawn from the one it ships in
`assets/trigger-evals.json` by `evals.py --draw`, and `make lint` fails when
the two differ; `develop`'s is written in `evals/skills/` by hand.

`.github/scripts/kit.py` bundles every folder in [`kit/skills/`](../../kit/skills/README.md)
into `home/kit.json`, and the home kit copies each one into
`~/.agents/skills/`, `~/.claude/skills/` and Antigravity's
`~/.gemini/antigravity-cli/skills/`, with a mark that lets it replace its own
folders and refuse anyone else's. The loader probe's `--skills` canary proves
each app sees exactly one copy.

---

## 🧱 What Every Skill Here Follows

The renderer refuses a skill that breaks any of these, because each one is a
rule some app enforces by silently not loading the skill:

- The folder name is the skill's `name`: lowercase words joined by single
  hyphens, at most 64 characters, without `claude` or `anthropic`.
- `SKILL.md` opens with a `---` frontmatter fence holding only `name`,
  `description`, `license`, `compatibility`, `metadata` and `allowed-tools`.
- The description is at most 1,024 characters, has no angle brackets, and
  says when to use the skill with "Use when".
- The body stays under 500 lines, and files sit at most one level below it.

> [!NOTE]
> **Skill files are exempt from Document Styling.** Loaders read frontmatter
> only from a `---` fence on the first line, and every line of a skill is
> paid for in context, so `SKILL.md` and the files beside it carry no hidden
> comment frontmatter and no decorative header or footer. For the same
> reason a skill folder has no `README.md`: it would ship with the skill.

Each skill's trigger test lives in `evals/skills/`, outside its folder, so the
hub's own never ships. Each is drawn from the one the skill keeps in its own
`assets/`, which ships with it, as the template keeps it. [Evals](Evals.md)
describes them.

---

## 👥 Subagents

The agent hierarchy starts with two subagents a session can hand work to, in
[`kit/subagents/`](../../kit/subagents/README.md):

| Subagent                                         | What it does                                                                                         | Tools                       |
| :----------------------------------------------- | :--------------------------------------------------------------------------------------------------- | :-------------------------- |
| [`worker.md`](../../kit/subagents/worker.md)     | Makes one well-defined change, runs the checks that cover it, never pushes, and reports the evidence | read, search, edit, execute |
| [`reviewer.md`](../../kit/subagents/reviewer.md) | Reviews a change before it ships, runs the checks itself, and reports verified findings by severity  | read, search, execute       |

Each source holds a `name`, a `description` and a list of abstract tools.
`.github/scripts/kit.py` renders it three ways, and the home kit installs each:

| App                   | Where                | Form                                         |
| :-------------------- | :------------------- | :------------------------------------------- |
| Claude Code           | `~/.claude/agents/`  | Markdown, tools as Claude Code names them    |
| Copilot               | `~/.copilot/agents/` | `.agent.md`, tools as Copilot's aliases      |
| Codex                 | `~/.codex/agents/`   | TOML, the prompt as `developer_instructions` |
| Grok Build and Cursor | Claude Code's folder | read from there, so no copy of their own     |

> [!NOTE]
> **These files are exempt from Document Styling.** Each app reads them as a
> prompt with `---` frontmatter, so they carry no hidden comment frontmatter
> and no decorative header or footer.

The Reviewer has no edit tools where an app lets that be enforced. Codex has
no tool list, so there it is read-only by instruction.

---

## 🔗 See Also

- [ADR-0021](../adrs/ADR-0021-Develop-Is-The-One-Skill.md): develop is the one skill the hub writes
- [ADR-0037](../adrs/ADR-0037-The-Hub-Writes-Every-Skill.md): the hub writes every skill, universal, and the knowledge template keeps none
- [ADR-0015](../adrs/ADR-0015-A-Worker-And-A-Reviewer.md): the hierarchy starts with a Worker and a Reviewer
- [The Home Kit](The-Home-Kit.md): how the kit reaches each app

---

<div align="center">

**Load the procedure when the task calls for it, and give every change a second look.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
