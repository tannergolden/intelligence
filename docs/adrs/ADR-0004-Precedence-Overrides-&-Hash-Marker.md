<!--
title: '📄 ADR-0004: PRECEDENCE, OVERRIDES & HASH MARKER'
description: 'Invariants from every copy of the rules apply, Defaults resolve from the repository outwards with overrides by rule ID, and the managed block is marked with a hash of its content.'
tags: [adr, precedence, instructions, versioning]
category: docs
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0004: PRECEDENCE, OVERRIDES & HASH MARKER

<a name="top"></a>

**Which copy wins when an agent loads two, and how a repository changes a Default without touching the block.**

_Invariants hold everywhere. Defaults bend where a repository says so._

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

An agent can load the home copy, the repository's block and the repository's own sections in one session. The apps resolve layered instructions differently, and none of them knows these rules exist:

- Cursor ranks team rules over project rules over user rules.
- Copilot ranks personal over repository over organization.
- Codex and Grok Build let the deeper file win.
- Claude Code weighs conflicts by judgment.

So the rules must state their own precedence. The first draft said the repository's copy wins. That lets a stale block override a newer invariant: a repository still carrying an older block would tell the agent to ignore a security invariant added since. The draft marker also carried the release version, so every release would rewrite every repository's `AGENTS.md`, even a release that changed only the home kit.

---

## 🚦 Decision Drivers

- **A newer Invariant is never undone by an older copy.**
- **A repository can change a Default without editing the managed block**, which sync owns.
- **A release that leaves the block unchanged touches no repository.**
- **Drift is detectable** by a tool, not only by reading.

---

## 🏗️ Considered Options

1. **The repository's copy wins outright.**
2. **The home copy wins outright.**
3. **Invariants from every copy apply; Defaults resolve from the repository outwards, and an Overrides section replaces a Default by its ID.**

The marker had two candidates of its own: **the release version** (`INTELLIGENCE:BEGIN v0.4.0`), or **a hash of the block's content** (`INTELLIGENCE:BEGIN sha256:...`).

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, with a content-hash marker

### Rationale for Selection

Both copies carry the same precedence text. Its current draft:

> Invariants from every copy of these rules apply. For Defaults, this repository's block wins over your user-level copy, this repository's own sections win over the block, and an entry under "Overrides" in this file replaces the Default it names. Invariants cannot be overridden: if one conflicts with another instruction, stop and ask.

This record fixes the structure, not the words. The final wording ships with the law in v0.1, once the research into universal rules has tested it against how each app resolves conflicts, including what an agent does when nobody is there to answer.

Invariants only accumulate: whichever copy is newer, its invariants hold, so an old block can never undo a new one. A repository changes a Default with one line under Overrides naming its ID, and sync never touches that section. Options 1 and 2 each let one stale copy win everything.

The marker carries a hash: `<!-- INTELLIGENCE:BEGIN sha256:<hash of the block> -->`. A release that does not change the block renders the same hash, so sync opens no pull request. `make audit` maps each hash to the release that produced it, and reports a block whose content no longer matches its hash.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                               |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Invariants hold across stale copies; overrides need no edit to the block; quiet releases touch nothing; hand edits are caught by `make audit`                      |
| **Negative (-)** | Overrides are prose an agent must apply by rule ID; an Invariant that conflicts with another instruction stops the agent to ask, which can pause an unattended run |
| **Neutral (~)**  | The marker is for tools; no agent needs to read it                                                                                                                 |

---

## ⚖️ Trade-off Comparative

### Option 1: The repository's copy wins

- ✅ Simple, and local intent always wins
- ❌ A stale block silently drops newer invariants

### Option 2: The home copy wins

- ✅ The newest rules on the machine always apply
- ❌ A repository cannot adjust anything, and collaborators' agents have no home copy

### Option 3: Invariants accumulate, Defaults resolve outwards

- ✅ Safe across stale copies, and flexible where it is allowed to be
- ❌ One more sentence every agent must follow

---

## 🔗 Traceability & Links

- [ADR-0002](ADR-0002-One-Root-AGENTS-File.md): the file the marker lives in
- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): sync, which the hash keeps quiet
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): the rule IDs an Overrides entry cites

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Invariants hold everywhere, and Defaults bend by name.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
