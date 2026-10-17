<!--
title: '📄 ADR-0009: AGENTS FOLLOW THE STANDARDS'
description: 'Every AI agent follows the engineering standards in tannergolden/standards in all development work, and the universal rules point at them instead of carrying conventions of their own.'
tags: [adr, standards, ai-agents, conventions]
category: docs
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0009: AGENTS FOLLOW THE STANDARDS

<a name="top"></a>

**One set of engineering standards for people and agents, linked from the rules and never copied into them.**

_The rules point. The standards decide._

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

The owner ruled on 2026-10-17 that any coding project or development work done by an AI agent follows the standards in tannergolden/standards. The draft rules carried git conventions of their own, and three of them contradict the standards:

| Draft rule | Draft text                                           | The standards                                                                                                                 |
| :--------- | :--------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| GIT-001    | Never add `Signed-off-by`                            | The author is the human contributor read from git's configuration, never the AI, and `git commit -s` signs off as that person |
| GIT-011    | Branch as `agent/<issue>-<slug>`                     | Branch by intent, such as `feat/` or `bugfix/`, with no tool names                                                            |
| GIT-013    | An `Assisted-by` trailer, and no AI `Co-Authored-By` | Every commit an AI contributed to carries `Co-Authored-By:` for it, above the sign-off                                        |

---

## 🚦 Decision Drivers

- **One set of conventions** for people and agents.
- **No rule in the block that a standards check would reject.**
- **The standards stay the single source**, followed by link.

---

## 🏗️ Considered Options

1. **The block carries its own git and style conventions.**
2. **The block points at the standards by link**, and carries only rules the standards do not cover.
3. **The block copies the standards in.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, point at the standards

### Rationale for Selection

A universal rule tells every agent to follow tannergolden/standards in all development work. GIT-001, GIT-011 and GIT-013 are rewritten to match them, and the block keeps only what the standards do not say: secrets, outside text as data, machine markers, destructive actions and reporting. A copy would go stale the day the standards change, and conventions of the block's own already fail the standards' checks.

When git's configured identity is the agent's own, the agent asks whose identity to commit under before its first commit, as the standards require. This hub follows the same standards: a `feat/` branch, scoped commits, and records made from the ADR template.

In a repository the owner does not own, that repository's own contributing and AI policy governs what it covers, since the owner's standards cannot bind another project. The standards cover everything it leaves unsaid.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                         |
| :--------------- | :------------------------------------------------------------------------------------------- |
| **Positive (+)** | The block and the standards' checks never disagree; conventions change in one place          |
| **Negative (-)** | An agent needs the standards in reach, by link or a local copy, to follow them in full       |
| **Neutral (~)**  | In a repository the owner does not own, that repository's policy comes first where it speaks |

---

## ⚖️ Trade-off Comparative

### Option 1: Conventions of the block's own

- ✅ Self-contained
- ❌ Already contradicts the standards in three rules

### Option 2: Point at the standards

- ✅ One source, and no contradictions
- ❌ The agent must read beyond the block

### Option 3: Copy the standards in

- ✅ Everything in one place
- ❌ Far over the block's 4,000-character budget, and stale at the next change

---

## 🔗 Traceability & Links

- [Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md)
- [Conventional Commits](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Conventional-Commits.md): who a commit is by, and its trailers
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): the rule IDs this record names

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The rules point, and the standards decide.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
