<!--
title: '📄 ADR-0013: THE GUARD DENIES, NEVER ALLOWS'
description: 'One standard-library script, called by every app''s pre-tool hook, denies the few tool calls the Invariants forbid outright with exit 2 and a reason, and never allows or asks.'
type: record
status: 'Proposed'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0013: THE GUARD DENIES, NEVER ALLOWS

<a name="top"></a>

**A seatbelt in every app, built from the one verdict every app honours.**

_Silent when right. Specific when wrong._

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

Several Invariants guard against damage nobody can take back: a force-push, an agent merging its own pull request, a dropped working tree, a credential in a commit, a sign-off in an AI's name. Prose is followed most of the time, and the plan listed hooks as the second layer. Every target app now has pre-tool hooks, but they differ: Claude Code, Codex, Copilot and Antigravity name events and fields differently, only exit 2 with a reason blocks in all of them, `ask` fails open in Codex, and a bare `allow` is an error there. Copilot CLI never runs a user's Claude hooks; Grok Build and Cursor do.

---

## 🚦 Decision Drivers

- **One verdict that blocks everywhere**: exit 2, the reason on stderr.
- **No false alarms in daily work**: `git commit -s` with a person's identity, `--force-with-lease` on a feature branch and ordinary pushes all pass.
- **Every app the kit serves**, from one script.
- **Never the only layer**: rulesets and CI still decide.

---

## 🏗️ Considered Options

1. **No hooks**: prose, rulesets and CI only.
2. **Per-app hooks**, each written in its app's own protocol, allowing and asking where the app supports it.
3. **One deny-only script behind every app's hook**, registered where each app reads hooks.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, one deny-only guard

### Rationale for Selection

`kit/guard.py` normalises each app's payload, reads a shell command the way a careful reviewer would, and denies with the rule it enforces:

- OPS-001: force-pushes without a lease, pushes to protected branches, deleted refs, tag pushes and merges, through git, gh or a GitHub MCP tool
- OPS-003: what git cannot undo, when there is something to lose
- OPS-004: `--no-verify` and edits that would remove the guard
- GIT-001: commits git would author or sign off as an AI, which settles the old conflict with `git commit -s` by checking the identity instead of the flag
- SEC-001: credential-shaped strings
- the machine-written blocks

The installer registers it in Claude Code's settings (which Grok Build and Cursor read), in Codex's `hooks.json` (appended last and replaced in place, because Codex trusts a hook by its position), in a file of its own for Copilot, and under a named key in Antigravity's `hooks.json`. Claude Code's entry sets `onFailure: block`. A bug inside the guard lets the call through and says so, because a guard that blocks every call gets switched off.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                                    |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | The commonest irreversible mistakes are stopped before they run, in every app, with a reason that names the rule                                                                        |
| **Negative (-)** | It reads commands heuristically, so a determined workaround passes; Codex and Antigravity hooks fail open if the script cannot start; Antigravity's schema comes from secondary sources |
| **Neutral (~)**  | Codex asks once to trust the hook, and keeps that trust while the command stays the same                                                                                                |

---

## ⚖️ Trade-off Comparative

### Option 1: No hooks

- ✅ Nothing to maintain
- ❌ The first warning comes after the damage, from the server

### Option 2: Per-app hooks

- ✅ Each app's full protocol, including ask
- ❌ Six implementations, and ask fails open in Codex

### Option 3: One deny-only guard

- ✅ One tested script, one verdict that blocks everywhere
- ❌ Cannot ask; an approved irreversible step is run by the user

---

## 🔗 Traceability & Links

- [ADR-0011](ADR-0011-The-Universal-Rule-Set.md): the Invariants it enforces
- [Backstops & residual risk](../operations/Backstops-&-Residual-Risk.md): what still gets past it
- [`kit/guard.py`](../../kit/guard.py)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Deny the irreversible, say why, and stay quiet otherwise.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
