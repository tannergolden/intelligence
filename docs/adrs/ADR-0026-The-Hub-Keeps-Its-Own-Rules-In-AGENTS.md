<!--
title: '📄 ADR-0026: THE HUB KEEPS ITS OWN RULES IN AGENTS.MD'
description: 'The hub''s own commands and conventions move from .github/CONTRIBUTING.md into a root AGENTS.md that carries no copy of the universal rules, because the account now serves every derived repository its contributing guide from its .github repository.'
type: record
keywords: [agents-md, contributing, community-health, hub]
status: 'Proposed'
date: '2026-10-20'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0026: THE HUB KEEPS ITS OWN RULES IN AGENTS.MD

<a name="top"></a>

**The hub's own rules in a root `AGENTS.md`, with no copy of the universal ones.**

_Every agent's first file, and still one source of the rules._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                            |
| :------------ | :------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                  |
| **Consulted** | Claude Code sessions: the account's community health defaults, and where agents look first               |
| **Informed**  | Everyone who works in the hub, a person or an agent                                                      |
| **Amends**    | [ADR-0020](ADR-0020-One-Constitution.md), which moved the hub's own rules into `.github/CONTRIBUTING.md` |

---

## 🎯 Context & Problem Statement

ADR-0020 gave the hub no `AGENTS.md`, since a copy of the block beside its source would be a second source, and moved the hub's own commands and conventions into `.github/CONTRIBUTING.md`, where POL-001 sends every agent before its first commit. The owner then asked that every repository generated from the private template keep no community health files of its own, so that GitHub serves the account's defaults from its `.github` repository. The hub is one of them, and its contributing guide had to go, and its rules with it, unless they found another home.

---

## 🚦 Decision Drivers

- **One source of the universal rules**: nothing in the hub repeats `CONSTITUTION.md`.
- **The first file an agent reads**: the hub's own rules sit where every app looks without being told.
- **The account's defaults**: the hub carries no contributing guide, code of conduct or security policy of its own.

---

## 🏗️ Considered Options

1. **A root `AGENTS.md` holding only the hub's own rules**, with no `INTELLIGENCE` block.
2. **A page in `docs/`**, linked from the README.
3. **Keep `.github/CONTRIBUTING.md`** as the one exception to the account's defaults.

---

## ✅ Decision Outcome

**Chosen Option**: Option 1, a root `AGENTS.md` holding only the hub's own rules

### Rationale for Selection

Every app the hub supports reads a repository's root `AGENTS.md` without being told to, and none reads a page in `docs/` unless something sends it there, so Option 2 would leave an agent here with only the universal rules. Option 3 would keep the one file the owner asked every derived repository to give up.

The file carries the sections sync gives every repository's `AGENTS.md`, with the hub's commands, definition of done, conventions, layout, gotchas and Ask First list, and no block. ADR-0020's reason against an `AGENTS.md` here still holds for the block: the file never carries one, sync skips the hub, and no `CLAUDE.md` sits beside it, since Claude Code would read that in its place. Agents working here still get the universal rules from their home copies.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                        |
| :--------------- | :---------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every agent reads the hub's rules first, and the hub takes the account's community health files             |
| **Negative (-)** | An `AGENTS.md` without the block is the one exception in the account, and a reader has to be told why       |
| **Neutral (~)**  | POL-001 now meets the account's contributing guide here, and its AI policy, which sends agents to this file |

---

## ⚖️ Trade-off Comparative

### Option 1: AGENTS.md, Hub Rules Only

- ✅ Read first by every app, with no pointer needed
- ❌ An `AGENTS.md` that holds no block, unlike every other repository's

### Option 2: A Page In docs/

- ✅ The hub keeps no `AGENTS.md` at all
- ❌ An agent finds the rules only if a person or a file points it there

### Option 3: Keep CONTRIBUTING

- ✅ Nothing moves
- ❌ The one derived repository that hides the account's defaults

---

## 🔗 Traceability & Links

- [`AGENTS.md`](../../AGENTS.md): the hub's own rules
- [ADR-0020](ADR-0020-One-Constitution.md): one Constitution, and no block in the hub
- [ADR-0002](ADR-0002-One-Root-AGENTS-File.md): one root `AGENTS.md`, and no `CLAUDE.md`

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The hub's rules where every agent looks first.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
