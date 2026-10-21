<!--
title: '📄 ADR-0022: ONLY THE GOLDEN PATH TEMPLATES SIT OUT'
description: 'Sync skips only the two golden path templates, repo and path, by name, as the standards'' stubs do; a template of any other kind, such as the vault template, takes part, so the block its generated repositories inherit stays current.'
type: record
status: 'Proposed'
date: '2026-10-19'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0022: ONLY THE GOLDEN PATH TEMPLATES SIT OUT

<a name="top"></a>

**Sync skips the two golden path templates by name, and every other template takes part.**

_A template that hands its rules on keeps them current._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                       |
| :------------ | :---------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner             |
| **Consulted** | Claude Code sessions: a comparison of the hub's stub with the standards' stubs      |
| **Informed**  | Everyone who generates a repository from a template that carries the block          |
| **Amends**    | [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md), which had sync skip every template |

---

## 🎯 Context & Problem Statement

[ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md) had sync skip every template, so that the templates stay free of agent files. Then the only templates were the two golden path templates, `repo` and `path`, and a repository generated from one starts an `AGENTS.md` of its own at its first sync.

The vault template, tannergolden/knowledge, is a template too, and it carries the block on purpose: its `AGENTS.md` holds the vault's rules, and every vault generated from it inherits them. Because sync skipped every template, nothing kept that block current. Its stub printed "skipped, a template", and `make sync` and `make audit` passed it by. At the hub's next block release the template would hold a stale block, every new vault would start a release behind, and a repair by hand would read as an edit.

---

## 🚦 Decision Drivers

- **The golden path templates stay free of agent files**, as ADR-0003 wanted.
- **A template that carries the block keeps it current**, as any repository does.
- **One answer to which templates are special**, the one the standards' upkeep stubs already give: the two golden path templates, named `repo` and `path`.

---

## 🏗️ Considered Options

1. **Keep skipping every template**, and update a template's block by hand.
2. **Skip only the golden path templates**, by name.
3. **Skip a template unless its `AGENTS.md` already carries the block.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, skip only the golden path templates

### Rationale for Selection

It is the rule the standards already apply to upkeep. Their stubs for checks, formatting, governance and maintenance sit out only in a template named `repo` or `path`, and run in any other template, the vault template among them; only a job that means nothing in any template, such as initialisation, skips them all. Keeping a block current is upkeep, so the hub now draws the line where the standards do. `left_out()` in `.github/scripts/sync.py` reads the name from the same repository settings it already reads, and its tests hold both halves: a golden path template is skipped, and a template of its own is synced and written into.

Option 3 would decide a repository's part in sync by a file it may not have yet, so sync could never adopt a template, and the decision would need every repository's `AGENTS.md` before any other check. Option 1 leaves the vault template's block to go stale at every release.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                         |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | The vault template's block stays current through its stub, `make sync` and `make audit`, so every vault starts on the latest |
| **Negative (-)** | A template renamed to `repo` or `path` would sit out too, and renaming a golden path template means changing this list       |
| **Neutral (~)**  | The golden path templates still carry no agent files                                                                         |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep Skipping Every Template

- ✅ No change to sync
- ❌ The vault template's block goes stale, and a repair by hand breaks its seal

### Option 2: Skip Only The Golden Path Templates

- ✅ The same rule as the standards' upkeep stubs, read from settings sync already has
- ❌ Two names written into the hub, which a rename must follow

### Option 3: Skip A Template Without The Block

- ✅ No names in the hub
- ❌ A template could never be adopted, and every repository's file is read before the cheaper checks

---

## 🔗 Traceability & Links

- [`.github/scripts/sync.py`](../../.github/scripts/sync.py): `left_out()` and `GOLDEN_PATH_TEMPLATES`
- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): the sync this amends
- [ADR-0019](ADR-0019-Each-Repository-Pulls-With-A-Stub.md): the stub, which applies the same rule
- [Repository Sync](../technical/Repository-Sync.md): which repositories take part

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Two templates sit out; every other one keeps its rules current.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
