<!--
title: '📄 ADR-0031: UNIVERSAL PROMPTS STAY IN THE HUB'
description: 'The universal prompts move to the hub''s own docs/Prompts.md and reach no other repository; sync gives each repository an empty docs/Prompts.md of its own once, where its owner makes the sections and prompts.'
type: record
status: 'Proposed'
date: '2026-10-21'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0031: UNIVERSAL PROMPTS STAY IN THE HUB

<a name="top"></a>

**One place for the prompts that work anywhere, and a page in each repository for the ones that work only there.**

_Copy the universal ones from the hub. Write your own where you work._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                                              |
| :------------- | :--------------------------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                    |
| **Consulted**  | Claude Code sessions: the change, made at the owner's direction                                            |
| **Informed**   | Every owner and collaborator who works with an AI agent in a repository of theirs                          |
| **Supersedes** | [ADR-0025](ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md), every repository gets ready-made prompts |

---

## 🎯 Context & Problem Statement

[ADR-0025](ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md) sealed the universal prompts into every repository's `docs/Prompts.md`, beside a section of the repository's own, and release v0.3.0 shipped them, before any repository had taken a release through its stub. The owner decided the universal prompts belong in the hub alone. Each repository that carries the stub should instead get its own `docs/Prompts.md`, empty, where its owner writes the prompts that only make sense there, such as ones for using it, changing it or understanding it, in sections of the owner's own making.

---

## 🚦 Decision Drivers

- **One copy of the universal prompts**: nearly 90 prompts and their guide in every repository is a copy that adds nothing the hub cannot serve.
- **A repository's page is its own**: after it arrives, no delivery ever changes it.
- **The layout rules hold**: the page sits where the standards keep a repository's documents, and passes their checks.

---

## 🏗️ Considered Options

1. **Keep the sealed block in every repository**, as ADR-0025 chose.
2. **Universal prompts in the hub only**, and an empty page of its own in each repository, added once.
3. **Universal prompts in the hub only**, and nothing in a repository until its owner adds a page.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, universal prompts in the hub only, and an empty page in each repository

### Rationale for Selection

The universal prompts move from `setup/Prompts.md` to the hub's own [`docs/Prompts.md`](../Prompts.md), the same path every repository keeps its prompts at. Their markers go, since nothing seals or delivers them, and the guide and the **Use when** lines now speak to a reader who copies a prompt into another repository. Write A New Prompt adds a prompt to the repository's own page, creating it if there is none, and Improve A Prompt names a prompt from the hub as one to send back here. `prompts.py --check` holds the file to the same shape and lint as before.

[`setup/Prompts.md`](../../setup/Prompts.md) becomes the page a repository first gets: the standard header and footer, and a note on what goes there, such as prompts for using, changing or understanding the repository, with a link to the universal prompts. It holds no section and no prompt: the owner makes both. Sync adds it to a repository without `docs/Prompts.md`, in the same `chore/intelligence` pull request as the rules, and never changes it after that. The `no-intelligence-prompts` topic still keeps it out.

`make audit` names a repository with no page, and `make merge` leaves a pull request that adds one for the owner to review. The guard no longer protects a prompts block, since a repository's page is all its own. No repository took v0.3.0 through its stub, so none holds the universal prompts to take out, and a release from before the page, v0.3.0 among them, delivers no prompts at all.

Option 1 keeps a second sealed block in every repository's sync, audit and merge, for prompts anyone can copy from one place. Option 3 leaves a repository's own prompts with no set place, so they end up in a README or nowhere.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                  |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | One copy of the universal prompts, current as soon as it lands; each repository has a set place for its own, and sync leaves it alone |
| **Negative (-)** | Copying a universal prompt means opening the hub                                                                                      |
| **Neutral (~)**  | The page a repository first gets changes only with a release; a repository that already has one keeps its own                         |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Sealed Block In Every Repository

- ✅ Every prompt is in the repository where it runs
- ❌ A second block in every sync, audit and merge, and nearly 90 prompts copied into every repository

### Option 2: Universal Prompts In The Hub, An Empty Page In Each Repository

- ✅ One copy of the universal prompts, and a page each repository owns outright
- ❌ The universal prompts are one link away, not in the repository

### Option 3: Universal Prompts In The Hub, Nothing In A Repository

- ✅ Sync delivers one file fewer
- ❌ A repository's own prompts have no set place to live

---

## 🔗 Traceability & Links

- [`docs/Prompts.md`](../Prompts.md): the universal prompts
- [`setup/Prompts.md`](../../setup/Prompts.md): the page a repository first gets
- [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py) and [`.github/scripts/sync.py`](../../.github/scripts/sync.py): the checks and the delivery
- [Prompts](../technical/Prompts.md): how both work, and how to change each
- [ADR-0025](ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): the decision this supersedes

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The universal prompts in one place, and each repository's own where it works.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
