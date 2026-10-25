<!--
title: '📄 ADR-0002: ONE ROOT AGENTS FILE PER REPOSITORY'
description: 'Each repository carries exactly one AGENTS.md, at its root, holding the managed block and the sections the repository owns, with no CLAUDE.md or per-tool files.'
type: record
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0002: ONE ROOT AGENTS FILE PER REPOSITORY

<a name="top"></a>

**One file at the root that every app reads, and nothing beside it to drift.**

_AGENTS.md, once, at the top._

</div>

> [!IMPORTANT]
> **Amended by [ADR-0020](ADR-0020-One-Constitution.md).** The hub itself keeps
> no `AGENTS.md`: it holds the source of the rules, `CONSTITUTION.md`, and every
> other repository still carries one root `AGENTS.md`.

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

The apps disagree about filenames. Claude Code has `CLAUDE.md`, Gemini CLI had `GEMINI.md`, Copilot reads `.github/copilot-instructions.md`, and Cursor has `.cursor/rules`. All six apps on the owner's list now read `AGENTS.md`. Claude Code reads it natively from v2.1.277, as long as no `CLAUDE.md` or `CLAUDE.local.md` sits beside it.

The owner asked for `AGENTS.md` over `CLAUDE.md`, for nearly identical files across tools, and for one top-level `AGENTS.md`.

The phase 0 probe confirmed the Claude Code behaviour on v2.1.302 in a Claude cloud session. A root `AGENTS.md` on its own loads. Beside a `CLAUDE.md` or a `CLAUDE.local.md` it is skipped, unless the `instructionFiles` setting says to read both.

---

## 🚦 Decision Drivers

- **One file every app reads**, so no tool needs a pointer or a copy.
- **No duplicates to drift**: per-tool files rendered from one source still disagree the moment one is edited by hand.
- **One place for a repository's agents**: the universal block and the repository's own sections side by side.
- **Nothing nested to resolve**, because apps disagree about how nested files combine.

---

## 🏗️ Considered Options

1. **One root `AGENTS.md`**, and nothing else for agents.
2. **`AGENTS.md` plus a one-line `CLAUDE.md`** containing `@AGENTS.md`, so every Claude session reads it.
3. **Per-tool files** rendered from one source, in the style of rulesync and ruler.
4. **Nested `AGENTS.md` files**, one in each folder that needs rules of its own.

---

## ✅ Decision Outcome

**Chosen Option**: Option 1, one root `AGENTS.md`

### Rationale for Selection

Every app reads it, so nothing else is needed. The cases where Claude Code skips it are narrow:

- versions before 2.1.277
- its built-in plugin turned off
- folders added with `--add-dir`
- a `CLAUDE.md` or `CLAUDE.local.md` beside it

On the owner's machines, the home setting covers the last case ([ADR-0005](ADR-0005-Home-Copies-Not-Links.md)). The first sync folds an existing `CLAUDE.md` into `AGENTS.md`, and the probe catches any regression.

The `CLAUDE.md` pointer closes a gap the owner does not have, at the cost of the second file the owner asked not to keep; revisit it only if the probe fails. Per-tool files multiply what can drift, and nested files leave each app to combine them its own way.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                           |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One file to read and review; Claude Code, Codex, Antigravity CLI, Copilot, Cursor and Grok Build all load it with no pointer                                   |
| **Negative (-)** | In a repository that keeps a `CLAUDE.md`, Claude Code skips `AGENTS.md` on machines without the home setting, which is why the first sync folds `CLAUDE.md` in |
| **Neutral (~)**  | A repository can still add nested files of its own; the hub neither manages nor forbids them                                                                   |

---

## ⚖️ Trade-off Comparative

### Option 1: One root AGENTS.md

- ✅ One file, read natively everywhere
- ❌ Relies on the home setting wherever a `CLAUDE.md` is kept

### Option 2: AGENTS.md plus a CLAUDE.md pointer

- ✅ Every Claude session reads `AGENTS.md`, whatever its settings
- ❌ A second file in every repository, which the owner ruled out

### Option 3: Per-tool files

- ✅ Each tool gets its native format
- ❌ Six files per repository that drift apart

### Option 4: Nested files

- ✅ Rules sit next to the code they govern
- ❌ Apps combine nested files differently, and the block would repeat in each

---

## 🔗 Traceability & Links

- [ADR-0001](ADR-0001-Two-Pieces-Home-&-Repository.md): why there is a repository piece at all
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the block's marker, and how the repository's sections override it
- [The Loader Probe](../technical/The-Loader-Probe.md): the Claude Code results this record cites

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**One root file, read by every app.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
