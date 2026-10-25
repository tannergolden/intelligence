<!--
title: '📄 ADR-0004: PRECEDENCE, OVERRIDES & HASH MARKER'
description: 'Invariants from every copy of the rules apply and nothing waives one, Defaults yield to the user''s request and then to an Overrides entry by rule ID, and the managed block is marked with a hash of its content.'
type: record
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

So the rules must state their own precedence. The first draft said the repository's copy wins. That lets a stale block override a newer invariant: a repository still carrying an older block would tell the agent to ignore a security invariant added since. Its fallback, "stop and ask", strands an unattended run that nobody is there to answer, and its trigger, "another instruction", would let a comment injected into an issue halt the agent. The draft marker also carried the release version, so every release would rewrite every repository's `AGENTS.md`, even a release that changed only the home kit.

---

## 🚦 Decision Drivers

- **A newer Invariant is never undone by an older copy.**
- **A conflict never strands a run**, attended or not, and outside text cannot trigger one.
- **A repository can change a Default without editing the managed block**, which sync owns.
- **A release that leaves the block unchanged touches no repository.**
- **Drift is detectable** by a tool, not only by reading.

---

## 🏗️ Considered Options

1. **The repository's copy wins outright.**
2. **The home copy wins outright.**
3. **Invariants from every copy apply; Defaults follow one ladder: the user's explicit request, then an Overrides entry naming the rule ID, then the repository's copy.**

The marker had two candidates of its own: **the release version** (`INTELLIGENCE:BEGIN v0.4.0`), or **a hash of the block's content** (`INTELLIGENCE:BEGIN sha256:...`).

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, with a content-hash marker

### Rationale for Selection

The precedence text is the first two lines of the block, word for word the same in the home copy and the repository copy:

> - Invariants: follow every one in every copy; nothing waives one. If a request needs what one forbids, do the rest, skip that part and name the rule ID.
> - Defaults: your user's explicit request for this task wins, then the repository's "Overrides" entry for that rule ID, then the repository's copy of these rules. In forks, and in repositories tannergolden does not own, the project's own rules win and owner-only Defaults do not apply; a repository with no remote yet counts as tannergolden's.

Invariants only accumulate: whichever copy is newer, its invariants hold, so an old block can never undo a new one. When a request needs what an Invariant forbids, the agent does the rest, skips that part and names the rule ID, so an unattended run still finishes and outside text cannot halt it.

A repository changes a Default only with an entry under Overrides naming its ID, and sync never touches that section. `make audit` rejects an entry that names an Invariant, and asks for a reason on one that names STD-001, the pointer to the standards. Because both copies carry the same words, an agent that loads both reads one text twice, never two paraphrases that could look like a conflict. Options 1 and 2 each let one stale copy win everything.

The marker carries a hash: `<!-- INTELLIGENCE:BEGIN sha256:<hash of the block> -->`. A release that does not change the block renders the same hash, so sync opens no pull request. `make audit` maps each hash to the release that produced it, and reports a block whose content no longer matches its hash.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                          |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Invariants hold across stale copies; a conflict never strands a run; overrides need no edit to the block; quiet releases touch nothing; hand edits are caught by `make audit` |
| **Negative (-)** | Overrides are prose an agent must apply by rule ID; a request that needs what an Invariant forbids is done only in part, with the skipped part named                          |
| **Neutral (~)**  | The marker is for tools; no agent needs to read it                                                                                                                            |

---

## ⚖️ Trade-off Comparative

### Option 1: The repository's copy wins

- ✅ Simple, and local intent always wins
- ❌ A stale block silently drops newer invariants

### Option 2: The home copy wins

- ✅ The newest rules on the machine always apply
- ❌ A repository cannot adjust anything, and collaborators' agents have no home copy

### Option 3: Invariants accumulate, Defaults follow one ladder

- ✅ Safe across stale copies, and every run can finish
- ❌ Two lines of precedence every agent must follow

---

## 🔗 Traceability & Links

- [ADR-0002](ADR-0002-One-Root-AGENTS-File.md): the file the marker lives in
- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): sync, which the hash keeps quiet
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): the rule IDs an Overrides entry cites
- [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md): STD-001, and where the owner-only Defaults reach

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Invariants hold everywhere, and Defaults bend by name.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
