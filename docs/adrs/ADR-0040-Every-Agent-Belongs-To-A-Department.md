<!--
title: '📄 ADR-0040: EVERY AGENT BELONGS TO A DEPARTMENT'
description: 'The kit drops its two standalone subagents, the Worker and the Reviewer, and Public Relations drops its Writer: the Chief Communications Officer drafts, the Editor reads fresh and composes the profile interview batch, and an install takes out what a release drops.'
type: record
status: 'Superseded'
date: '2026-11-07'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0040: EVERY AGENT BELONGS TO A DEPARTMENT

<a name="top"></a>

**No agent outside the twelve departments, and no seat a department does not need.**

_Every seat answers to a department._

</div>

> [!IMPORTANT]
> **Superseded by [ADR-0041](ADR-0041-The-Kit-Carries-No-Skills.md).** The
> departments, and every agent in them, are gone with the skills. An install
> still takes out what earlier releases wrote: now every skill and subagent that
> carries the kit's mark.

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                                                         |
| :------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                               |
| **Consulted**  | Claude Code sessions: the change, made at the owner's direction                                                       |
| **Informed**   | Everyone who installs the home kit, and everyone who runs the departments as Grok Bot agents                          |
| **Supersedes** | [ADR-0015](ADR-0015-A-Worker-And-A-Reviewer.md), which began the agent hierarchy with a Worker and a Reviewer         |
| **Amends**     | [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md), whose Public Relations team kept a Writer beside its Editor |

---

## 🎯 Context & Problem Statement

After [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md) the workforce was twelve departments, each one skill with a team of at most five. Two agents still sat outside every department: the Worker and the Reviewer, the standalone subagents of [ADR-0015](ADR-0015-A-Worker-And-A-Reviewer.md), installed into Claude Code, Copilot and Codex beside the skills. And Public Relations kept a Writer whose drafting its lead could do. The owner decided on 2026-11-07 to remove all three.

An install also wrote each release's skills and subagents without taking out the ones a release dropped, so a machine that installed one release and then the next kept every renamed or retired piece loaded beside the new ones.

---

## 🚦 Decision Drivers

- **Every agent belongs to a department**, reached through its skill, as the Grok Bot groups are.
- **No seat a department does not need.** The Public Relations lead can draft, and the Editor stays the fresh reader.
- **Nothing lost.** The Writer's craft, and the profile interview's separation of interviewer, composer and reviewer, survive the seat.
- **A removal reaches every machine**, not only the next install of a fresh home.

---

## 🏗️ Considered Options

1. **Keep the three agents.**
2. **Remove them, and leave earlier installs as they are.**
3. **Remove them, and have every install take out what a release dropped.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, remove them, and retire what a release drops

### Rationale for Selection

- **The Worker and the Reviewer are gone** with `kit/subagents/`. The kit ships no standalone subagent; `kit.py` can still render one, should one return.
- **Public Relations' Writer is gone.** The ★ Chief Communications Officer, which the skill embodies, drafts every piece, at every tier, in the loaded voice and the register it needs, following the Writer's craft, kept in `references/drafting.md`. The Editor still reads every piece above quick fresh, so writing and critique stay separate passes by separate agents, and the lead never gates its own draft.
- **The profile interview's composer is now the public-relations skill's Editor**, borrowed by title, composing the proposal batch from the interview ledger alone. The interviewer, the composer and the blind reviewer stay three separate seats.
- **An install retires what a release drops**: a skill folder or a subagent file the kit wrote, carrying its mark, that this release no longer ships. Nothing without the mark is touched.
- **Fifty agents remain**, Public Relations with four.

Option 1 keeps two agents outside every department and a seat Public Relations does not need. Option 2 leaves the retired agents, and every renamed skill, loaded on each machine that installed an earlier release.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Every agent sits in a department and its Grok Bot group; Public Relations' group is smaller; a machine sheds a renamed skill or a retired agent on its next install |
| **Negative (-)** | No ready-made subagent to hand a single code change or a review to; the Public Relations lead now drafts as well as orchestrates                                    |
| **Neutral (~)**  | Fifty agents, from fifty-one; the subagent renderer stays in `kit.py`, unused                                                                                       |

---

## 🔗 Traceability & Links

- [Skills & Subagents](../technical/Skills-&-Subagents.md): the twelve skills, and how their agents run as subagents
- [The Home Kit](../technical/The-Home-Kit.md): what an install writes, and what it takes out
- [ADR-0015](ADR-0015-A-Worker-And-A-Reviewer.md): the Worker and the Reviewer, which this supersedes
- [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md): twelve departments, twelve skills

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Twelve departments, and every agent in one of them.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
