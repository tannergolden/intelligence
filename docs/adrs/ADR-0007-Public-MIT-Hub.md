<!--
title: '📄 ADR-0007: PUBLIC MIT HUB'
description: 'The hub is a public repository under the MIT License, with every seeded document footer to match, because consumers fetch its releases without credentials.'
type: record
keywords: [licensing, visibility, open-source]
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0007: PUBLIC MIT HUB

<a name="top"></a>

**Public so every machine can fetch the rules, and MIT so anyone may reuse them.**

_Open by necessity, licensed to match._

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

The hub was generated from the owner's private template, which ships a proprietary `LICENSE` and a matching footer on every seeded document. The template's own README says to replace both before the first public push of anything meant to be open.

The hub has to be public:

- A public repository cannot call a private repository's reusable workflow.
- Dotfiles in a Codespace cannot download a private release without a token.

The rules are also meant to be read, copied and reused.

---

## 🚦 Decision Drivers

- **Consumers fetch releases with no credentials**, on any machine.
- **The licence matches the visibility.**
- **Every document's footer matches the licence.**

---

## 🏗️ Considered Options

1. **A private hub**, with a token on every consuming machine.
2. **A public hub under the proprietary licence.**
3. **A public hub under the MIT License**, the licence the public template uses.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, public and MIT

### Rationale for Selection

Only a public hub serves releases and reusable workflows with no token. A public repository under a proprietary licence would invite the copying its licence forbids. MIT matches the public template and states the intent plainly: reuse the rules.

`LICENSE` is the public template's MIT text, and every seeded document's footer now reads "Distributed under the MIT License." Both survive Template Sync: `LICENSE` is the owner's file and is never synced, and a sync keeps the owner's changes to the lines it merges.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                                                                                  |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Any machine fetches releases without a token; anyone may reuse the rules                                                                                                                                                              |
| **Negative (-)** | Everything committed is public for good, so no private repository name, personal context or secret may enter the hub; files Template Sync manages describe the template they come from, so check them before switching the visibility |
| **Neutral (~)**  | Switching the repository to public is a setting only the owner changes                                                                                                                                                                |

---

## ⚖️ Trade-off Comparative

### Option 1: A private hub

- ✅ Nothing is public
- ❌ A token on every machine and in every consuming workflow

### Option 2: Public, proprietary

- ✅ Keeps every right reserved
- ❌ A licence that forbids what being public invites

### Option 3: Public, MIT

- ✅ No tokens, and reuse is welcome
- ❌ Nothing private can ever be committed

---

## 🔗 Traceability & Links

- [LICENSE](../../LICENSE)
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): names fit for a public hub

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Public by need, MIT by choice.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
