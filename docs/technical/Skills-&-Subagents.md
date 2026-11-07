<!--
title: '🧰 SKILLS & SUBAGENTS'
description: 'The skills the home kit installs, twelve, one for each department, each written here, universal and laid out alike, the Worker and Reviewer subagents, the rules every skill here follows, and where each app reads them.'
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
any repository, or in a conversation with no repository at all.

There are **twelve skills, one for each department**, each named for its
department. Together they cover every area of a company the user runs and
of the user's own life:

| Skill                                                                            | Department                   | A company's work                                                        | The user's own life                                         |
| :------------------------------------------------------------------------------- | :--------------------------- | :---------------------------------------------------------------------- | :---------------------------------------------------------- |
| [`administration`](../../kit/skills/administration/SKILL.md)                     | Administration               | Founding, strategy, decisions across departments, the operating cadence | Goals, priorities, decisions, calendar and commitments      |
| [`finance-and-accounting`](../../kit/skills/finance-and-accounting/SKILL.md)     | Finance & Accounting (F&A)   | The books, the model, the cap table, company tax                        | Budget, debt, taxes, investing, insurance, estate           |
| [`legal-and-compliance`](../../kit/skills/legal-and-compliance/SKILL.md)         | Legal & Compliance (L&C)     | Formation, contracts, intellectual property, compliance, privacy        | Leases, contracts, disputes, wills, privacy                 |
| [`sales-and-marketing`](../../kit/skills/sales-and-marketing/SKILL.md)           | Sales & Marketing (S&M)      | Pipeline, deals, positioning, demand                                    | Personal brand, job search, networking, negotiation         |
| [`operations-and-logistics`](../../kit/skills/operations-and-logistics/SKILL.md) | Operations & Logistics (O&L) | Processes, programs, vendors                                            | Household, routines, travel, moves, contractors             |
| [`human-resources`](../../kit/skills/human-resources/SKILL.md)                   | Human Resources (HR)         | Roles, hiring, pay, onboarding, people records                          | The user's profile, career and skills, health and wellbeing |
| [`information-technology`](../../kit/skills/information-technology/SKILL.md)     | Information Technology (IT)  | Internal systems and their security                                     | Devices, accounts, digital security                         |
| [`research-and-development`](../../kit/skills/research-and-development/SKILL.md) | Research & Development (R&D) | Research, ideas, and building products, skills and software             | Researching anything, learning, ideas, side projects        |
| [`business-intelligence`](../../kit/skills/business-intelligence/SKILL.md)       | Business Intelligence (BI)   | Metrics, data, dashboards, any chart or diagram                         | Habit and metric tracking, visuals                          |
| [`quality-assurance`](../../kit/skills/quality-assurance/SKILL.md)               | Quality Assurance (QA)       | The independent check of consequential work                             | Checking important documents and plans                      |
| [`customer-experience`](../../kit/skills/customer-experience/SKILL.md)           | Customer Experience (CX)     | Onboarding, customer success, support                                   | The user as a customer: complaints, returns, warranties     |
| [`public-relations`](../../kit/skills/public-relations/SKILL.md)                 | Public Relations (PR)        | Announcements, press, crises                                            | All of the user's writing and email, reputation             |

**Every skill is laid out alike**: a `SKILL.md`, the department's team in its
own `agents/` (a roster and one file for each agent), its `references/`,
`templates/` and `assets/`, a `Changelog.md` and a `License.txt`.
`research-and-development` also carries two standard-library scripts in
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
the repository itself: its agent instructions where it has them, its
`AGENTS.md` and folder rules, and otherwise its `README.md` files, the root
one and the one in each folder written into, which the skill reads first,
along with the checks they name. With neither, it works in the conversation
and writes a file only where the user asks. Every skill writes the user's
personal context only into a repository that says it was made to hold it
(SEC-003); anywhere else that stays in the conversation. So a vault
generated from tannergolden/knowledge, which holds no AI instructions,
explains each folder in its README, and every skill follows it.

### The departments' teams

`administration` keeps the executive office, the Chief Executive Officer,
the Chief Operating Officer, the Corporate Secretary and the Chief of Staff,
and convenes the other departments from their own skills. Called on its
own, a department skill does its function's work and keeps only its own
records; inside an `administration` run, `administration` keeps the
results. Agents are known by their role titles alone, and each team's lead
carries a star. `quality-assurance` is the one independent check: its
Fact-Checker, Devil's Advocate, Design Critic, QA Test Engineer and Head of
Quality verify the other departments' work, and a verdict always comes from
a seat that did not make it.

**Every team keeps at most its five most critical agents, its lead
included**, so a Grok Bot group of six holds a department and the Chief of
Staff, and `kit.py` refuses a roster with more. Deeper specialists are not kept on disk: a present lead stands in
for them.

**The checks.** `.github/scripts/kit.py` holds every skill, every agent and
every team to the validator in `research-and-development/scripts/`, every
title is unique across all of `kit/skills/*/agents/`, and every skill is
laid out alike: its `metadata.team` names a roster in its own `agents/`, it
ships `assets/trigger-evals.json`, and its metadata holds exactly `team`,
`version`, `author` and `status`. Each skill's trigger test in
`evals/skills/` is drawn from the one it ships by `evals.py --draw`, and
`make lint` fails when the two differ.

`.github/scripts/kit.py` bundles every folder in [`kit/skills/`](../../kit/skills/README.md)
into `home/kit.json`, and the home kit copies each one into
`~/.agents/skills/`, `~/.claude/skills/` and Antigravity's
`~/.gemini/antigravity-cli/skills/`, with a mark that lets it replace its own
folders and refuse anyone else's. The loader probe's `--skills` canary proves
each app sees exactly one copy. To run the departments as Grok Bot agents
instead, see [`kit/skills/README.md`](../../kit/skills/README.md).

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

- [ADR-0021](../adrs/ADR-0021-Develop-Is-The-One-Skill.md): develop, the skill builder, now the build mode of `research-and-development`
- [ADR-0037](../adrs/ADR-0037-The-Hub-Writes-Every-Skill.md): the hub writes every skill, universal, and the knowledge template keeps none
- [ADR-0038](../adrs/ADR-0038-Each-Department-Is-A-Skill.md): each department is a skill, laid out like every other
- [ADR-0039](../adrs/ADR-0039-Twelve-Departments-Twelve-Skills.md): twelve departments, twelve skills, covering a company and the user's own life
- [ADR-0015](../adrs/ADR-0015-A-Worker-And-A-Reviewer.md): the hierarchy starts with a Worker and a Reviewer
- [The Home Kit](The-Home-Kit.md): how the kit reaches each app

---

<div align="center">

**Load the procedure when the task calls for it, and give every change a second look.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
