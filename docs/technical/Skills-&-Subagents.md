<!--
title: '🧰 SKILLS & SUBAGENTS'
description: 'The one skill and the Worker and Reviewer subagents the home kit installs, the rules every skill here follows, and where each app reads them.'
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
procedure. There is exactly one, by the owner's decision:

| Skill                                          | What it does                                                                                                                                                                                                                                                     |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`develop`](../../kit/skills/develop/SKILL.md) | Builds, updates and improves skills and the agents and teams they dispatch: decides whether the need is a skill at all, researches, reuses before it creates, gates every build with its validator and independent reviewers, and learns from a skill's mistakes |

`develop` carries everything it needs in its own folder, so it works in any
repository: its Development team in `agents/`, five agents and their roster,
and two standard-library scripts in `scripts/`. `validate.py` checks a skill,
an agent, a team or a library against the format every app accepts, and
`package.py` builds a `.skill` archive for the Claude app, with the team
vendored and the same bytes on every rebuild. Their tests live in
[`.github/scripts/test_develop.py`](../../.github/scripts/test_develop.py), outside the
skill, so they never ship. A skill only one repository needs lives in that
repository's `.agents/skills/` and `.claude/skills/`, never here.

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

Each skill's trigger test lives in `evals/skills/`, outside its folder, so it
never ships; [Evals](Evals.md) describes them.

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

- [ADR-0014](../adrs/ADR-0014-One-Skill-That-Builds-Skills.md): one skill for now, the one that builds skills
- [ADR-0015](../adrs/ADR-0015-A-Worker-And-A-Reviewer.md): the hierarchy starts with a Worker and a Reviewer
- [The Home Kit](The-Home-Kit.md): how the kit reaches each app

---

<div align="center">

**Load the procedure when the task calls for it, and give every change a second look.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
