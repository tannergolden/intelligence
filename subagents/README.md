<!--
title: '👥 SUBAGENTS'
description: 'The Worker and Reviewer subagents the home kit installs, each one source rendered for Claude Code, Copilot and Codex.'
tags: [subagents, hierarchy, review, home-kit]
category: docs
-->

<div align="center">

# 👥 SUBAGENTS

<a name="top"></a>

**One agent to make a change, another to check it, in every app that runs subagents.**

_Do the work. Then doubt it._

</div>

---

## 💡 What This Folder Is For

The agent hierarchy starts here, with two subagents a session can hand work
to:

| Subagent                     | What it does                                                                                         | Tools                       |
| :--------------------------- | :--------------------------------------------------------------------------------------------------- | :-------------------------- |
| [`worker.md`](worker.md)     | Makes one well-defined change, runs the checks that cover it, never pushes, and reports the evidence | read, search, edit, execute |
| [`reviewer.md`](reviewer.md) | Reviews a change before it ships, runs the checks itself, and reports verified findings by severity  | read, search, execute       |

Each source holds a `name`, a `description` and a list of abstract tools.
`scripts/kit.py` renders it three ways, and the home kit installs each:

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

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                        | Purpose                                                                                                                                                                                                                                                                                                                                                             |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`README.md`](README.md)     | This file.                                                                                                                                                                                                                                                                                                                                                          |
| [`reviewer.md`](reviewer.md) | Reviews a change before it is pushed or merged. Checks the diff against its task, the repository's AGENTS.md and the universal rules, runs the checks itself, and returns verified findings ranked by severity with file and line evidence. Use after a Worker or the main session finishes a change, or whenever the user asks for a review. It never edits files. |
| [`worker.md`](worker.md)     | Implements one well-defined change in the current repository and reports back with evidence. Use for a self-contained coding task that fits in a few sentences with its acceptance check, when the main session wants it done in a fresh context and reviewed before anything is pushed.                                                                            |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Every change gets a second look before it leaves.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
