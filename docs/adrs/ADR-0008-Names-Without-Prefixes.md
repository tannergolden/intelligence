<!--
title: '📄 ADR-0008: NAMES WITHOUT PREFIXES'
description: 'Rule IDs take the form DOMAIN-NNN and every file and skill is named for what it does, with no owner prefix on either.'
type: record
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0008: NAMES WITHOUT PREFIXES

<a name="top"></a>

**Rule IDs and file names that say what they are, not whose they are.**

_SEC-001, not anyone's initials._

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

Earlier drafts prefixed every rule ID and every file with the owner's initials, as in `TG-SEC-001` and `tg-*` skill folders, to avoid collisions with other people's rules and skills. The owner ruled on 2026-10-17 that no rule or file carries a prefix.

---

## 🚦 Decision Drivers

- **Names say what a thing does**, read in any repository.
- **Short IDs** that a repository's Overrides section can cite.
- **No collisions**, now carried by distinctive names instead of a prefix.

---

## 🏗️ Considered Options

1. **An owner prefix** on every rule ID and file.
2. **`DOMAIN-NNN` rule IDs, and names that say what a thing does.**
3. **A namespace folder only**, with bare names inside it.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, `DOMAIN-NNN` IDs and descriptive names

### Rationale for Selection

A rule ID is a domain and a number, such as `SEC-001` for secrets or `OPS-001` for operations, and an ID is never reused once 1.0 freezes them. Files the kit writes are named for the hub, as in `intelligence.md` and `intelligence.instructions.md`, which says what they hold. Skills get distinctive names, such as `pull-request-report`, and the installer never overwrites a skill folder it did not install, which carries the collision protection the prefix used to give.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                 |
| :--------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Shorter IDs, and names that read naturally in any repository                                                         |
| **Negative (-)** | A bare name can collide with someone else's skill, so the installer refuses to overwrite anything it did not install |
| **Neutral (~)**  | The block's marker names the hub, `INTELLIGENCE`, not its owner                                                      |

---

## ⚖️ Trade-off Comparative

### Option 1: An owner prefix

- ✅ Collisions are impossible
- ❌ Every name carries its owner instead of its purpose, which the owner ruled out

### Option 2: DOMAIN-NNN and descriptive names

- ✅ Plain, short and citable
- ❌ Collision protection moves into the installer

### Option 3: A namespace folder only

- ✅ Bare names grouped in one place
- ❌ Not every app reads from a folder of its choosing

---

## 🔗 Traceability & Links

- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): an Overrides entry cites a Default by its ID

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Named for what it does.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
