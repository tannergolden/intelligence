<!--
title: '📄 ADR-0043: THE PATH TEMPLATE TAKES THE SYNC'
description: 'The path golden path template now takes part in sync, so its AGENTS.md comes from 🔁 Intelligence Sync like any repository''s, and the research section it keeps there reaches every repository built from it through 🔄 Template Sync; the repo template still sits out.'
type: record
status: 'Proposed'
date: '2026-11-14'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0043: THE PATH TEMPLATE TAKES THE SYNC

<a name="top"></a>

**The golden path template gets its AGENTS.md the way every repository does.**

_The block from the hub. Its research section from the template._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                                          |
| :------------ | :--------------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                                |
| **Consulted** | Claude Code sessions: the change, made at the owner's direction; the markers and the section's place are its proposals |
| **Informed**  | Every repository generated from `tannergolden/path`, and every owner who runs 🔄 Template Sync in one                  |

---

## 🎯 Context & Problem Statement

[ADR-0022](ADR-0022-Only-The-Golden-Path-Templates-Sit-Out.md) had sync skip both golden path templates, `repo` and `path`, so that they stayed free of agent files and every repository generated from one started an `AGENTS.md` of its own. The owner now wants every repository built from `path` to know where its research reports go, and that a research request is done only when its report is filed from the Research-Log template. That belongs in `AGENTS.md`, the one file every agent loads, and the owner wants `path`'s `AGENTS.md` to come from 🔁 Intelligence Sync rather than be written by hand. Two things stood in the way: sync skipped `path` by name, and its stub was silent there. A third would have stopped the section reaching anyone already built from `path`: their `AGENTS.md` was written by their own sync, so 🔄 Template Sync had no baseline to merge `path`'s into, and could only report a conflict.

---

## 🚦 Decision Drivers

- **One way to get an `AGENTS.md`**: from the sync, with the block between its markers and the owner's sections below it.
- **The research section reaches every repository built from `path`**, those generated before it included.
- **Nothing an owner wrote is taken from them**: their own sections, the block their sync keeps, and any change they made to the template's section.
- **The block names no repository's folders**, so the research section is the template's, not the hub's.

---

## 🏗️ Considered Options

1. **`path` takes part in sync, and its research section is a block 🔄 Template Sync keeps.**
2. **`path` keeps sitting out, and ships a hand-written `AGENTS.md`.**
3. **The research rule goes into the block**, for every repository.

---

## ✅ Decision Outcome

**Chosen Option**: Option 1

### Rationale for Selection

`left_out()` in `.github/scripts/sync.py` now skips only `repo`, so `make sync` and the stub's own run both write into `path`, and `path`'s stub loses the guard that kept it silent. `path`'s `AGENTS.md` is the one the sync writes, with its block, and holds one section of its own, between `<!-- TEMPLATE-SYNC:BEGIN -->` and `<!-- TEMPLATE-SYNC:END -->`: where research reports go, and that a research request is done only when its report is filed. The template sync engine in `tannergolden/standards` syncs a Markdown file that holds such a block one block at a time: it puts the section into a repository's own `AGENTS.md` under the heading it follows in the template, keeps it current while the owner leaves it alone, and never touches the rest of the file. The block the repository's own sync keeps was already masked from every merge, so a release of either never conflicts with the other.

A template's `AGENTS.md` is inherited, so the skeleton the sync writes no longer names the repository in its description, which in every repository built from `path` would have named `path`.

Option 2 would make a second source for the shape of an `AGENTS.md`, beside the skeleton in `sync.py`, and still leave every repository built before it without the section. Option 3 would put one template's folder into the block every repository reads, against [ADR-0036](ADR-0036-The-Block-Names-No-Account.md)'s reasoning, at a cap RES-001 has just raised.

`repo` still sits out: nothing asked for a change there. The hub is itself built from `path`, so its next 🔄 Template Sync puts the research section into this repository's `AGENTS.md` too, under **Where things live**, which describes the hub's own research folder truly; the hub keeps its own `docs/technical/research/README.md` with a rule in `.github/template-sync`, as it does for its `technical/` and `operations/` READMEs.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                              |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every repository built from `path` carries its research section, kept current, and `path`'s own `AGENTS.md` keeps its block current like any repository's         |
| **Negative (-)** | `path` is no longer free of agent files, and a repository generated from it now starts with an `AGENTS.md` and a block rather than adopting one at its first sync |
| **Neutral (~)**  | Nothing reaches a repository until releases: the hub's for sync, `tannergolden/standards`' for the engine, then `path`'s for the section                          |

---

## ⚖️ Trade-off Comparative

### Option 1: `path` Takes Part, And Template Sync Keeps Its Section

- ✅ One way to get an `AGENTS.md`, and the section reaches repositories built before it
- ❌ Needs the engine to sync part of a file, which `tannergolden/standards` now does

### Option 2: A Hand-Written `AGENTS.md`

- ✅ No change to sync
- ❌ A second source for the file's shape, and nothing for repositories built before it

### Option 3: The Rule In The Block

- ✅ Reaches every repository
- ❌ Names one template's folders in the block every repository reads, at its cap

---

## 🔗 Traceability & Links

- [`.github/scripts/sync.py`](../../.github/scripts/sync.py): `TEMPLATES_THAT_SIT_OUT`, read by `left_out()`
- [ADR-0022](ADR-0022-Only-The-Golden-Path-Templates-Sit-Out.md): the rule this narrows, which still holds for `repo`
- [ADR-0042](ADR-0042-Research-Goes-Stale-After-Three-Months.md): RES-001, which the research section's reports are held to
- [Repository Sync](../technical/Repository-Sync.md): which repositories take part

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**One way in, for every AGENTS.md.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
