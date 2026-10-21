<!--
title: '📄 ADR-0025: EVERY REPOSITORY GETS READY-MADE PROMPTS'
description: 'Sync gives every repository docs/Prompts.md: a sealed block of universal prompts and the practices behind them, which the hub keeps current, and a section of the repository''s own, which sync never touches.'
type: record
status: 'Superseded'
date: '2026-10-20'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0025: EVERY REPOSITORY GETS READY-MADE PROMPTS

<a name="top"></a>

**A page of prompts in every repository, the universal ones kept current and the rest the repository's own.**

_Copy one. Fill it in. Paste it._

</div>

> [!NOTE]
> **Superseded by [ADR-0031](ADR-0031-Universal-Prompts-Stay-In-The-Hub.md).** The universal
> prompts now stay in the hub's own `docs/Prompts.md`, and a repository gets an
> empty `docs/Prompts.md` of its own instead. `setup/Prompts.md`, which this
> record calls the source, is now that empty page.

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                     |
| :------------ | :-------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner           |
| **Consulted** | Claude Code sessions: a design talked through with the owner before it was built  |
| **Informed**  | Every owner and collaborator who works with an AI agent in a repository of theirs |

---

## 🎯 Context & Problem Statement

The universal rules decide how an agent behaves, but not what it is asked. A request typed in a hurry leaves out the goal, the context the agent cannot see, the limits, and how to tell when the work is done, and the agent fills the gaps with guesses. The owner wanted every repository to carry ready-made prompts, written the way a good prompt is written, that the owner and every collaborator can copy and paste into an AI app, alongside prompts each repository writes for its own work.

---

## 🚦 Decision Drivers

- **Any app, no setup**: a prompt is text anyone can copy, into any AI app, with nothing installed.
- **Better prompts reach everyone**: when the hub improves a universal prompt, every repository gets it.
- **A repository's own prompts are its own**: no delivery ever changes them.
- **The layout rules hold**: the file sits where the standards keep a repository's documents, and passes their checks.

---

## 🏗️ Considered Options

1. **Add the file once**, and hand all of it to the repository.
2. **Split it as `AGENTS.md` is**: a sealed block of universal prompts that sync keeps current, and a section of the repository's own.
3. **Slash commands for each app**, rendered from one source the way the subagents are.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, the same split as `AGENTS.md`

### Rationale for Selection

Every repository that takes part in sync gets `docs/Prompts.md`, in the same `chore/intelligence` pull request as the rules. Between its `INTELLIGENCE:PROMPTS` markers sit how to use a prompt, five universal prompts and the practices they follow; after them sits "Prompts For This Repository", which is the repository's own. The last universal prompt writes a new prompt from a rough request, in the same shape, into that section.

The source is `setup/Prompts.md`, the file as a repository first gets it, with its markers unsealed. `prompts.py` seals the block with the SHA-256 of its text, the way the rules block is sealed, so an unchanged release touches nothing and a hand edit is repaired. `make audit`, the guard hook and the standards' Machined Block Check each catch an edit inside the block; the check now hashes a block's own lines, code fences included. A file of that name without the block is never touched, and a `no-intelligence-prompts` topic keeps the prompts out of one repository. A pull request that adds the file waits for review by hand, and one that only moves a block forward merges with `make merge`.

Option 1 would leave every repository with the first release's prompts forever. Option 3 makes each prompt one `/name` away, but in some apps and not others, and only where the repository is open; it stays a later step that can render from the same source.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                         |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every repository starts with well-made prompts, keeps them current, and has a set place for its own                          |
| **Negative (-)** | A second block to deliver, audit and merge; the source has to stay as Prettier writes it, or every repository reformats it   |
| **Neutral (~)**  | It needs a release of the standards whose Machined Block Check hashes code fences, before the release that ships the prompts |

---

## ⚖️ Trade-off Comparative

### Option 1: Add The File Once

- ✅ No block to maintain, and the owner may change every line
- ❌ No improvement ever reaches a repository that has the file

### Option 2: Split It As AGENTS.md Is

- ✅ The universal prompts stay current, and a repository's own stay untouched
- ❌ A second sealed block in every repository's sync, audit and merge

### Option 3: Slash Commands For Each App

- ✅ Each prompt is one command away, with no copying
- ❌ Only in the apps that read a command folder, and only inside the repository

---

## 🔗 Traceability & Links

- [`setup/Prompts.md`](../../setup/Prompts.md): the source
- [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py) and [`.github/scripts/sync.py`](../../.github/scripts/sync.py): sealing and delivery
- [Prompts](../technical/Prompts.md): what a repository gets, and how to change the universal prompts
- [ADR-0019](ADR-0019-Each-Repository-Pulls-With-A-Stub.md): the stub that delivers both blocks

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The universal prompts from the hub, the rest from the people who do the work.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
