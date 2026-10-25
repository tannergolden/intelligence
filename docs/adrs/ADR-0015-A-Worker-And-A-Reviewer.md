<!--
title: '📄 ADR-0015: A WORKER AND A REVIEWER'
description: 'The agent hierarchy begins with two subagents, a Worker that makes one change and proves it and a Reviewer that checks a change without editing it, rendered for Claude Code, Copilot and Codex.'
type: record
status: 'Proposed'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0015: A WORKER AND A REVIEWER

<a name="top"></a>

**One agent to do the work, another to doubt it.**

_Do, then doubt, before anything ships._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                      |
| :------------ | :--------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner            |
| **Consulted** | Claude Code sessions: research, four independent reviews of the plan, and drafting |
| **Informed**  | Every agent and collaborator working in a repository that carries the block        |

---

## 🎯 Context & Problem Statement

The Workforce design put agents in tiers with an App for each, and the plan deferred all of it: "The hierarchy: beginning with Worker and Reviewer subagents." On a solo account no second person reviews a pull request, so a fresh-context check before a push has real value. The apps define subagents differently: Claude Code and Copilot read Markdown with frontmatter, in `~/.claude/agents/` and `~/.copilot/agents/`, and Codex reads TOML roles in `~/.codex/agents/` whose prompt is `developer_instructions`. Only a name, a description and the prompt are portable.

---

## 🚦 Decision Drivers

- **Short prompts** that lean on the universal rules instead of repeating them.
- **The Reviewer never edits**, wherever the app lets that be enforced.
- **One source per subagent**, rendered for each app.
- **No new identity, App or token.**

---

## 🏗️ Considered Options

1. **The full tiered hierarchy**, with an App per tier.
2. **No subagents.**
3. **A Worker and a Reviewer**, each one Markdown source rendered for three apps.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, a Worker and a Reviewer

### Rationale for Selection

`kit/subagents/worker.md` makes the smallest change that does the task, runs the checks that cover it, never pushes, and reports what changed, what ran, what failed and what it assumed. `kit/subagents/reviewer.md` reads the diff, runs the checks itself, looks for the failures the rules name, verifies every finding and reports them ranked. The source names abstract tools, which `kit.py` maps to Claude Code's names and Copilot's aliases; the Reviewer gets no edit tools in either. Codex has no tool list, so its Reviewer is read-only by instruction. Grok Build and Cursor read Claude's folder.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                      |
| :--------------- | :-------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | A fresh-context review before every push, in three apps, from two short files                             |
| **Negative (-)** | Codex enforces the Reviewer's read-only promise by instruction only; VS Code may list each subagent twice |
| **Neutral (~)**  | Subagents run as the session that calls them, with its permissions and its guard                          |

---

## ⚖️ Trade-off Comparative

### Option 1: The full hierarchy

- ✅ Separation by identity
- ❌ Apps, tokens and orchestration well beyond the goal

### Option 2: No subagents

- ✅ Nothing to maintain
- ❌ No second look before a push on an account with one person

### Option 3: A Worker and a Reviewer

- ✅ Most of the value, almost none of the machinery
- ❌ Separation by instruction, not identity

---

## 🔗 Traceability & Links

- [`kit/subagents/`](../../kit/subagents/README.md), explained in [Skills & Subagents](../technical/Skills-&-Subagents.md)
- [ADR-0012](ADR-0012-One-Pinned-Kit-For-Every-Module.md): how they ship

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Every change gets a second look before it leaves.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
