<!--
title: '📄 ADR-0032: THE OWNER CAN LIFT OPS-001 FOR A SESSION'
description: 'OPS-001 keeps forbidding pushes to a default or protected branch, force-pushes, remote deletions and merges, except in a session where the repository''s owner types `override OPS-001`; the guard reads those words only from what the user typed.'
type: record
status: 'Proposed'
date: '2026-10-24'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0032: THE OWNER CAN LIFT OPS-001 FOR A SESSION

<a name="top"></a>

**The rule that keeps agents off the default branch, with one way past it that only the owner can take.**

_Two words, typed by the owner, for one session._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                |
| :------------ | :------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                      |
| **Consulted** | Claude Code sessions: the change, made at the owner's direction                              |
| **Informed**  | Every agent and collaborator working in a repository that carries the block, or the home kit |

---

## 🎯 Context & Problem Statement

OPS-001 is an Invariant, and Article I says nothing waives one. An owner who wants an agent to land finished work on the default branch, and says so in the session, gets a refusal, as the rule requires, and runs the push by hand. The owner decided that a repository's owner should be able to lift OPS-001 for the session they are in, and the guard, which denies the same pushes and merges outside the prompt, has to honor that or the exception would exist only on paper.

---

## 🚦 Decision Drivers

- **Only the owner can lift it**, and only by asking for it in so many words: a hurried "just push it" stays a no.
- **One session, nothing more**: the next session starts with the rule whole.
- **No file, tool output or summary can lift it**, since a prompt injection arrives as exactly those.
- **The other Invariants still hold** in the same command.
- **The block stays near its size**, since every app reads it on every turn.

---

## 🏗️ Considered Options

1. **Keep OPS-001 whole**: the owner runs the push or merges the pull request themselves.
2. **Move OPS-001 to the Defaults**, where any user's explicit request for the task wins.
3. **Keep it an Invariant with one exception**: the owner types `override OPS-001`, and the guard reads it from what the user typed in that session.
4. **A launch switch**: the guard stands aside when the session starts with an environment variable set.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, an Invariant with one exception the owner types

### Rationale for Selection

The sentence now opens: "Unless your user owns the repository and types `override OPS-001` in this session". The words name the rule, so an agent knows exactly what to ask for, and a person cannot lift it without meaning to. Article II's prose names this as the one exception any Invariant has, and the block's cap rises from 5000 to 5100 characters to make room for it.

The guard reads the words from the session's transcript, which Claude Code names in every hook payload. It counts a line only when the user typed it: never a tool's result, a summary written at compaction, a line Claude Code adds itself, or the agent's own text. It counts the words only in a repository tannergolden owns, judged as DOC-002 judges one, or, for a GitHub tool, the repository the tool names. When they are there, it decides the call again without OPS-001, so a command that also breaks another rule is still denied for that one. Every OPS-001 denial now ends by naming the words, so the way out is on the screen. Other apps' payloads carry no transcript in Claude Code's shape, so there the guard keeps denying, and the owner runs the push.

Option 1 left the owner typing a push the agent had already prepared. Option 2 let any user's request lift it, the vague ones included, in any repository. Option 4 cannot be turned on from inside the session the owner is already in.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                  |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | The owner can have an agent land work on the default branch, after saying so in words that cannot happen by accident  |
| **Negative (-)** | An agent that writes its own transcript could forge the words; OPS-004 forbids it, and the rulesets still hold        |
| **Neutral (~)**  | The words reach no session already running: each session starts from the copy of the rules it loaded, until a release |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep OPS-001 Whole

- ✅ No way past the rule exists, for anyone
- ❌ The owner repeats work the agent could finish

### Option 2: Move OPS-001 To The Defaults

- ✅ No exception to explain
- ❌ Any user's request lifts it, in any repository, for the whole task

### Option 3: An Invariant With One Exception The Owner Types

- ✅ Lifted only by the owner, in so many words, for one session, and the guard agrees with the rule
- ❌ The guard trusts the transcript file, which a determined agent could edit

### Option 4: A Launch Switch

- ✅ An agent cannot set it
- ❌ It cannot be turned on in the session the owner is already in

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): OPS-001, Article II and Article V
- [`kit/guard.py`](../../kit/guard.py): `lifted` and `typed`, and the second decision without OPS-001
- [ADR-0013](ADR-0013-The-Guard-Denies-Never-Allows.md): the guard denies and never allows, which still holds, since a lifted rule is only a denial left out

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The rule holds, until its owner says otherwise in so many words.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
