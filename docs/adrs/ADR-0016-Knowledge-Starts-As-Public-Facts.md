<!--
title: '📄 ADR-0016: KNOWLEDGE STARTS AS PUBLIC FACTS'
description: 'Knowledge begins as a short, public list of facts about how the owner''s setup works, rendered as its own marked block beside every home copy of the rules and in the cloud setup, and never personal context.'
type: record
status: 'Superseded'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0016: KNOWLEDGE STARTS AS PUBLIC FACTS

<a name="top"></a>

**Tell agents how the setup works, and nothing about the person.**

_Facts beside the rules. Nothing personal anywhere._

</div>

> [!IMPORTANT]
> **Superseded by [ADR-0023](ADR-0023-The-Kit-Carries-No-Facts.md).** The kit
> carries no facts: `knowledge/` is gone, and an install takes out the blocks
> earlier releases wrote.

> [!NOTE]
> **Amended by [ADR-0020](ADR-0020-One-Constitution.md).** A private tier now
> exists outside the hub: each person's knowledge vault, a private repository
> generated from the public knowledge template, holds that person's context,
> and SEC-003 allows it there and nowhere else. The facts here stay public.

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

Rules say what to do; agents also lack facts about this setup that make the rules easy to follow: that repositories integrate on `Development`, that the guard explains its denials, that `git commit -s` in a cloud session signs as an AI. The Workforce design had a private knowledge instance with a Librarian, digests and SessionStart injection. The plan cut it back: "public tier first, delivered as a file the setup script writes, because user hooks never run in cloud sessions. Personal context never goes into the universal home file." The home copies load in public repositories too.

---

## 🚦 Decision Drivers

- **Public only**: everything here may appear in any repository.
- **Facts, not rules**, short enough to cost little on every session.
- **Delivered where the rules are**, including cloud sessions, with no hook.
- **Kept apart from the block**, which has its own budget and its own sync.

---

## 🏗️ Considered Options

1. **The private knowledge instance** with a Librarian and SessionStart digests.
2. **Facts added to the block.**
3. **Public facts as their own marked block**, installed beside each home copy of the rules.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, public facts beside the rules

### Rationale for Selection

`knowledge/public.json` holds eight facts under a 2,000-character cap, each one printable ASCII, one sentence and at most 300 characters. `kit.py` renders them between `INTELLIGENCE:KNOWLEDGE` markers and refuses any that names a tannergolden repository that is not public. The installer writes the block as a file of its own where an app loads a folder of rules (Claude Code, Copilot) and as a second marked block in the single files Codex and Antigravity read; the cloud setup adds it to `~/.claude/CLAUDE.md`. Repositories never receive it: the block in each `AGENTS.md` stays the rules alone. The public tannergolden/knowledge repository is kept for the private tier, when it comes.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                              |
| :--------------- | :------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Agents learn how the setup works in every session and every app, with no hook and nothing private |
| **Negative (-)** | Another 1,400 characters in every home session; facts must be kept true by hand                   |
| **Neutral (~)**  | A private tier can follow without changing this one                                               |

---

## ⚖️ Trade-off Comparative

### Option 1: The private instance

- ✅ Rich, personal context
- ❌ A project of its own, and hooks that never run in cloud sessions

### Option 2: Facts in the block

- ✅ One block to deliver
- ❌ Over the block's cap, and pushed into every repository

### Option 3: Public facts beside the rules

- ✅ Small, public, delivered everywhere the rules are
- ❌ No personal context at all, by design

---

## 🔗 Traceability & Links

- `knowledge/` and `docs/technical/Knowledge.md`, both removed by [ADR-0023](ADR-0023-The-Kit-Carries-No-Facts.md)
- [ADR-0005](ADR-0005-Home-Copies-Not-Links.md): home copies, checked against the release

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**What the setup is, never who the person is.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
