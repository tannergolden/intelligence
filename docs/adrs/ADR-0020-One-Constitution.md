<!--
title: '📄 ADR-0020: ONE CONSTITUTION, AND NO COPY IN THE HUB'
description: 'The universal rules live in one Markdown file, CONSTITUTION.md at the hub''s root, which the renderer reads into the block every AGENTS.md carries; the hub keeps no AGENTS.md of its own, and the rule set takes in the universal rules of the knowledge vault.'
type: record
status: 'Proposed'
date: '2026-10-19'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0020: ONE CONSTITUTION, AND NO COPY IN THE HUB

<a name="top"></a>

**One file a person reads and edits, and every block an agent reads rendered from it.**

_Written once, here. Copied everywhere else._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                                                                                                                                                                          |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                                                                                                                                                                |
| **Consulted** | Claude Code sessions: a review of the hub and of the knowledge vault, and drafting                                                                                                                                                                     |
| **Informed**  | Every agent and collaborator working in a repository that carries the block                                                                                                                                                                            |
| **Amends**    | [ADR-0002](ADR-0002-One-Root-AGENTS-File.md), one root AGENTS.md; [ADR-0011](ADR-0011-The-Universal-Rule-Set.md), the universal rule set; and [ADR-0016](ADR-0016-Knowledge-Starts-As-Public-Facts.md), whose private tier becomes each person's vault |

---

## 🎯 Context & Problem Statement

The rules lived in `law/`: one JSON file per rule and `block.json` for the order, the precedence and the budget. A person had to read twenty files to read the rules, and the hub kept its own `AGENTS.md`, a copy of the block beside the source it was rendered from.

The owner asked for one `CONSTITUTION.md` in the hub, as the place every `AGENTS.md` takes its universal rules from, with no `AGENTS.md` in the hub itself. The knowledge vault, which is becoming a public template that each person generates a private vault from, kept a constitution of its own; its rules that hold in every repository were to move into the hub's. And a vault exists to hold its owner's personal context, which SEC-003 forbade in any repository.

---

## 🚦 Decision Drivers

- **One file a person reads**, with each rule's reason beside it.
- **The block stays short**, because every app reads it whole on every turn and attention fades in the middle of a long context.
- **The hub holds the source, not a copy.**
- **A private vault may hold its owner's context**, and nothing public may.
- **No new file in other repositories**: each still carries the block, in one root `AGENTS.md`.

---

## 🏗️ Considered Options

1. **Keep `law/`** and render a `CONSTITUTION.md` from it for people to read.
2. **`CONSTITUTION.md` as the source**, in a fixed Markdown shape the renderer reads.
3. **`CONSTITUTION.md` as the source, also delivered whole** into every repository beside its `AGENTS.md`.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, `CONSTITUTION.md` as the source

### Rationale for Selection

`CONSTITUTION.md` sits at the hub's root. Article I quotes the precedence, Articles II to IV hold the rules by kind, Article V sets the block's heading, source line and budget, Article VI says how the file is written and changed, and an appendix lists the retired IDs. Each rule is a `###` heading of its ID, the one sentence agents read as a quote under it, then **Why.**, **Enforced by:** and **To add:**. `.github/scripts/render.py` reads that shape and holds the file to Article VI, so a missing reason, a second quote or a rule outside an Article fails `make check` with its line number.

The block opens with a line naming its source, so a person reading any `AGENTS.md` knows where the reasons are. Option 3 would put a second managed file in every repository, which ADR-0002 rules out and the owner did not want; Option 1 keeps two forms of every rule.

The hub keeps no `AGENTS.md`. Its own commands and conventions move to `.github/CONTRIBUTING.md`, which POL-001 sends every agent to before its first commit, and agents working here read the rules from their home copies.

The rule set takes in the vault's universal rules:

- **SEC-003** allows personal context in a private repository made to hold it, and nowhere else.
- **COM-002** also grounds a claim about an earlier session in a record read in this one.
- **COM-004**, a Default: answer first, sized to the question, without repeating context or loading whole files.
- **DOC-003**, a Default: plain words, without filler or stock AI phrasing.
- **COM-005**, an owner-only Default: times of day in 12-hour form.
- **STD-001** wins over the block's Defaults only, never over an Invariant.

The cap rises from 4,000 characters to 5,000, with a target of 4,500, and each new rule has a scenario in `evals/scenarios/`.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                             |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One file to read and review; each rule's reason sits beside it; a vault can hold its owner's context; precedence between the standards and the rules is explicit |
| **Negative (-)** | An agent working in the hub reads no repository instructions and relies on its home copy; the block grows from 3,640 characters to about 4,350                   |
| **Neutral (~)**  | Every other repository's `AGENTS.md` is unchanged in shape; only the block's text moves with a release                                                           |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep law/

- ✅ JSON is the easiest form for a script to read
- ❌ Two forms of every rule, and twenty files to read the rules

### Option 2: CONSTITUTION.md as the source

- ✅ One file, read and edited by people, checked by the renderer
- ❌ The renderer depends on a Markdown shape, which Article VI and the tests pin

### Option 3: Also delivered whole

- ✅ Every repository carries each rule's reason
- ❌ A second managed file everywhere, and a longer read for every agent

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): the rules, and Article VI on how the file is written
- [ADR-0002](ADR-0002-One-Root-AGENTS-File.md): one root `AGENTS.md` per repository, now every repository but the hub
- [ADR-0011](ADR-0011-The-Universal-Rule-Set.md): the nineteen rules this set grew from
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the precedence, the Overrides entries and the hash marker, unchanged
- [ADR-0026](ADR-0026-The-Hub-Keeps-Its-Own-Rules-In-AGENTS.md): amends this record, moving the hub's own rules from `.github/CONTRIBUTING.md` into a root `AGENTS.md` without the block

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**One Constitution, and every copy rendered from it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
