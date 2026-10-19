<!--
title: '📄 ADR-0006: BUILD THE LAW, ADOPT THE PLUMBING'
description: 'The hub builds its own renderer and installer in the Python standard library, and adopts existing tools for the plumbing around them, with set triggers to revisit.'
type: record
keywords: [tooling, build-vs-adopt, python]
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0006: BUILD THE LAW, ADOPT THE PLUMBING

<a name="top"></a>

**Write the small part nobody else does, and borrow everything around it.**

_Standard library for the law. Existing tools for the pipes._

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

Several tools render one source of rules into many tools' files: Microsoft APM, rulesync, ruler, Vercel's `skills` CLI and skillshare. Each misses most of what this plan needs:

- Grok Build's compatibility settings
- Claude Code's `instructionFiles` setting
- release attestation checks
- running on the system Python 3.9 that macOS ships

The two closest are moving fast. APM 0.33.0 refuses symlinked destinations, has no Grok hooks or MCP, needs Python 3.10 or later, and logged six breaking changes in four weeks. rulesync went from 17.0.0 to 37.0.0 in 26 days.

---

## 🚦 Decision Drivers

- **Few moving parts** for one maintainer.
- **Standard library only**, so the installer runs on any machine with the system Python.
- **Stable formats**: what the hub writes must not change because a dependency shipped a major.

---

## 🏗️ Considered Options

1. **Adopt APM** as the renderer and installer.
2. **Adopt rulesync or ruler.**
3. **Build `render.py` and `install.py`** in the standard library, and adopt the plumbing: the owner's `gh` login, or multi-gitter, for sync, and `actions/create-github-app-token` for the unattended module.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, build the law and adopt the plumbing

### Rationale for Selection

The renderer and installer are small, and the plan's specifics are exactly what the existing tools lack. Building them in the standard library keeps the installer runnable on Python 3.9, with golden tests pinning every byte it writes. The plumbing around them is not specific to this plan, so it is adopted: `gh` already holds the owner's login, and GitHub's own action mints App tokens.

Two triggers reopen the decision:

- APM reaches 1.0 with Grok hooks and a settings passthrough.
- rulesync's major releases slow down.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                             |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | No external runtime or package to install; exact control over every byte written; formats change only when this hub changes them |
| **Negative (-)** | Code to maintain and test here, which the golden tests and the probe keep honest                                                 |
| **Neutral (~)**  | Two named triggers to revisit adopting APM or rulesync                                                                           |

---

## ⚖️ Trade-off Comparative

### Option 1: Adopt APM

- ✅ A maintained tool with a growing set of targets
- ❌ No Grok hooks, Python 3.10 or later, and frequent breaking changes

### Option 2: Adopt rulesync or ruler

- ✅ Many targets out of the box
- ❌ Majors every few days, and gaps this plan depends on

### Option 3: Build the law, adopt the plumbing

- ✅ Small, exact and stable
- ❌ The renderer and installer are this hub's to maintain

---

## 🔗 Traceability & Links

- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): sync, built on `gh`
- [ADR-0005](ADR-0005-Home-Copies-Not-Links.md): what the installer writes
- [multi-gitter](https://github.com/lindell/multi-gitter)
- [actions/create-github-app-token](https://github.com/actions/create-github-app-token)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Build what is ours, borrow what is not.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
