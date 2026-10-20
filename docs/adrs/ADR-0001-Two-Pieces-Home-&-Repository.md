<!--
title: '📄 ADR-0001: TWO PIECES, HOME & REPOSITORY'
description: 'The universal rules reach agents in two pieces, a copy in each app''s home folder and a managed block in every repository, both rendered from one source.'
type: record
keywords: [ai-agents, delivery, instructions]
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0001: TWO PIECES, HOME & REPOSITORY

<a name="top"></a>

**Every session gets the rules, whether the agent runs on your machine or in someone else's cloud.**

_Home for the sessions you start. The repository for the ones you do not._

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

The owner works with six AI coding apps: Claude Code, Codex, Antigravity CLI, Copilot (the CLI and VS Code), Cursor and Grok Build. They run on a Mac, on Linux, in Codespaces and in Claude cloud sessions, across many repositories, some of them other people's. Each app loads always-on instructions from two kinds of place: a user-level file in its home folder, and files in the repository it works in.

A rule kept in only one of those places misses sessions. A rule kept only at home never reaches a cloud agent or a collaborator's agent, which see only the repository. A rule kept only in repositories never reaches scratch folders or repositories the owner does not control.

The first design also carried an agent hierarchy, a knowledge layer and behaviour evals, which made version 1 several projects at once.

---

## 🚦 Decision Drivers

- **Reach**: every session the owner starts, on any machine, in any folder.
- **Agents the owner does not run**: cloud agents and collaborators' agents get the rules from the repository, with nothing installed.
- **One source**: both pieces are rendered from the same law, never copied by hand.
- **Scope**: version 1 is exactly this goal; everything else waits for a module after 1.0.

---

## 🏗️ Considered Options

1. **Home only**: install the rules into each app's home folder on every machine.
2. **Repository only**: ship the rules in every repository, and nothing at home.
3. **Two pieces**: home copies installed by dotfiles, plus a managed block in every repository, both rendered from one law.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, two pieces

### Rationale for Selection

Each piece covers sessions the other cannot. The home copy is the only thing that reaches scratch folders and repositories the owner does not control. The repository block is the only thing that reaches a cloud agent or a collaborator's agent, which run with nothing installed. Rendering both from one law keeps them identical, and the precedence text ([ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md)) settles which copy wins when an agent loads both.

Repository only was a close second, since every cloud agent already relies on the repository block. It loses because the owner asked for the home layer, and only that layer reaches repositories nobody can add a block to.

The hierarchy, knowledge, evals, skills and hooks each return after 1.0 as a module with its own exit test, so version 1 is this goal and nothing else.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                        |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every session sees the rules, on any machine and in any repository; a cloud session works with nothing installed                                            |
| **Negative (-)** | An agent that loads both copies holds the rules twice, about 800 tokens; two delivery paths to keep working, the home kit (v0.2) and repository sync (v0.3) |
| **Neutral (~)**  | The agent hierarchy, knowledge, evals, skills and hooks move to modules after 1.0                                                                           |

---

## ⚖️ Trade-off Comparative

### Option 1: Home only

- ✅ One install per machine, and nothing in any repository
- ❌ Cloud agents and collaborators never see the rules

### Option 2: Repository only

- ✅ Travels with the code, so every agent working in it sees the rules
- ❌ Scratch folders and other people's repositories get nothing

### Option 3: Two pieces

- ✅ Covers every session either piece alone would miss
- ❌ Two delivery paths, and a duplicate copy in some sessions

---

## 🔗 Traceability & Links

- [ADR-0002](ADR-0002-One-Root-AGENTS-File.md): the shape of the repository piece
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): which copy wins when an agent loads both
- [ADR-0005](ADR-0005-Home-Copies-Not-Links.md): how the home piece is installed
- [How It Works](../introduction/How-It-Works.md): the two pieces, side by side

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Two pieces, one law, every session.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
