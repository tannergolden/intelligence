<!--
title: '👥 SUBAGENTS'
description: 'The Worker and Reviewer subagents the home kit installs, each one source rendered for Claude Code, Copilot and Codex.'
type: index
keywords: [hierarchy, review, home-kit]
-->

<div align="center">

# 👥 SUBAGENTS

<a name="top"></a>

**One agent to make a change, another to check it, in every app that runs subagents.**

_Do the work. Then doubt it._

</div>

---

## 💡 What This Folder Is For

The Worker and Reviewer subagents, one source each, which `scripts/kit.py`
renders for Claude Code, Copilot and Codex. What each does and where it lands:
[Skills & Subagents](../docs/technical/Skills-&-Subagents.md).

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
