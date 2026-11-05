<!--
title: '📄 ADR-0034: ONE LADDER FOR RULES & DOCS'
description: 'Below the Invariants, one ladder ranks every source an agent follows: the user''s request, the repository''s Overrides entry, its own rules, its docs/, the standards'' docs/, then the block''s Defaults; STD-001 reads both docs/ folders.'
type: record
status: 'Proposed'
date: '2026-11-05'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0034: ONE LADDER FOR RULES & DOCS

<a name="top"></a>

**Every source an agent follows, in one order: the repository's docs first, then the standards', then the Defaults.**

_The most specific source wins, and nothing outranks an Invariant._

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

The block ranked three sources for a Default: the user's request, the repository's Overrides entry, then the repository's copy of the rules. STD-001 added a fourth, the standards, which won over the block's Defaults. Nothing ranked a repository's own `docs/`, and the pieces formed a loop: the stub asks each repository to write down what it does differently from the standards, so the repository's word should beat the standards; the standards beat the Defaults; and a repository's own sections could change a Default only through Overrides. An agent meeting all three in one conflict had no order to apply.

The owner asked that agents follow the documentation in the `docs/` folder of the repository they work in, then the standards' docs, and that the way rules and docs are followed be defined plainly.

---

## 🚦 Decision Drivers

- **One order ranks every source**, written once, with no loop in it.
- **The most specific source wins**, because a repository knows its own code and the standards only know what every repository shares.
- **Invariants hold against every doc**, as they hold against everything else.
- **Overrides stays the form tools read**: the guard and `make audit` read nothing else.
- **The block stays inside its cap**, since every app reads it on every turn.

---

## 🏗️ Considered Options

1. **Rules first, then docs**: the block's Defaults outrank the repository's docs and the standards.
2. **Most specific first**: the user's request, the Overrides entry, the repository's own rules, its `docs/`, the standards' `docs/`, and the block's Defaults last.
3. **Leave the docs unranked**, and let the agent weigh them.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, most specific first

### Rationale for Selection

Article I's second line now reads:

> - Defaults: your user's explicit request for this task wins, then the repository's "Overrides" entry for that rule ID, then its own rules, then its `docs/`, then the standards' `docs/` (STD-001), then the repository's copy of these rules. In forks, and in repositories tannergolden does not own, owner-only Defaults do not apply; a repository with no remote yet counts as tannergolden's.

The ladder keeps every standing decision but one. The standards still come before the block's Defaults, as STD-001 has said since [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md), and a repository's Conventions section, which the stub asks to say what it does differently from the standards, now takes effect over the Defaults that restate them. The one decision that moves is [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md)'s: a repository's own sections no longer change a Default only through Overrides, because they now rank above the Defaults. Overrides still outranks them, and it stays the only form the guard and `make audit` read, so a repository records each Default it changes there.

STD-001 drops its own ranking clause, which Article I now holds, and names the repository's `docs/` beside the standards': before an agent commits, branches, opens a pull request, writes docs or tests, or adds a dependency, it reads the matching file in both. In SWE-CC (October 2026), agents opened a local rules file in 91.6% of runs and followed a URL in 28.9%, so the local folder is the one most likely to be read.

In forks and other people's repositories, the standards drop out with STD-001, an owner-only Default. The old clause "the project's own rules win" goes, because the ladder already puts the project's own rules and docs before the remaining Defaults. A doc counts only from one of the two `docs/` folders, and sets how the work is done, never what an Invariant forbids: an issue or a pull request that calls itself a doc stays information (SEC-002).

The block measures 5,097 of its 5,100 characters, up from 5,072.

Option 1 would reverse STD-001's standing order and leave a repository's Conventions losing to the one-sentence Defaults they depart from. Option 3 is the loop as it stood.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                        |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One order for every source; a repository's docs and Conventions take effect; the standards keep their place above the Defaults; the block grows by 25 characters            |
| **Negative (-)** | A repository can change a Default in a doc that the guard and `make audit` do not read; STD-001's eval measured its earlier wording, and no scenario measures the order yet |
| **Neutral (~)**  | Nothing reaches a repository until the next release, which sync then proposes as one pull request per repository, as for any change to the block                            |

---

## ⚖️ Trade-off Comparative

### Option 1: Rules First, Then Docs

- ✅ Overrides stays the only way a repository changes a Default
- ❌ Reverses STD-001's order, and a repository's own Conventions lose to the Defaults they depart from

### Option 2: Most Specific First

- ✅ One order with no loop, the repository's word first, and STD-001's order kept
- ❌ A Default changed in a doc is invisible to the guard and `make audit` until it is recorded under Overrides

### Option 3: Leave The Docs Unranked

- ✅ No change to the block
- ❌ The loop stays, and every agent settles it its own way

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): Article I and STD-001
- [How It Works](../introduction/How-It-Works.md): the quoted precedence and what an Overrides entry is for
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the precedence this ladder extends, and the Overrides rule it relaxes
- [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md): STD-001, and where the owner-only Defaults reach

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The repository's word first, the standards' next, the Defaults last, and the Invariants always.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
