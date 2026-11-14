<!--
title: '📄 ADR-0042: RESEARCH GOES STALE AFTER THREE MONTHS'
description: 'A new Default, RES-001: research last verified over three months ago, or undated, is stale, and is reverified or redone before anyone relies on it or builds a new report on it; the block''s cap rises from 5,400 to 5,700 characters to hold it.'
type: record
status: 'Proposed'
date: '2026-11-14'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0042: RESEARCH GOES STALE AFTER THREE MONTHS

<a name="top"></a>

**Research is trusted for three months from the last time someone checked it.**

_After that, check it again or research it again._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                                  |
| :------------ | :------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                        |
| **Consulted** | Claude Code sessions: the change, made at the owner's direction; the rule's kind and the cap are its proposals |
| **Informed**  | Every agent and collaborator working in a repository that carries the block, or the home kit                   |

---

## 🎯 Context & Problem Statement

The owner asked for a universal rule: any research is stale three months after it was done, and must be reverified, or researched again for a new report, before it is used. The pieces that already spoke to it disagreed and reached only part of the work. The hub's research folder trusted a report for three months and asked for a reverify only after six. The Research-Log template the golden path ships, which every repository generated from it carries, called a report stale only past six months. An agent that read an old report while answering a question or writing a new one had no rule at all.

---

## 🚦 Decision Drivers

- **One window everywhere**: three months from the last check, for every agent and every repository.
- **Age must be checkable**, so research with no date cannot pass as fresh.
- **Every rule names a way out**, because reverifying can need a network or time the agent does not have.
- **A repository can still set its own window**, through its rules or docs, under Article I.
- **The block grows as little as it can**, since every app reads it on every turn.

---

## 🏗️ Considered Options

1. **A new Default, RES-001**, with the cap raised to hold it.
2. **Leave it to the templates** and each repository's docs.
3. **A new Owner-only Default.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 1, a new Default

### Rationale for Selection

The rule reads:

> Research last verified over three months ago, or undated, is stale: before you rely on it or build a new report on it, reverify its claims and update its date or do a new research pass; if you can do neither, say it is stale.

It is a Default because Article VI keeps Invariants for severe or irreversible harm, and relying on old research is neither. As a Default it holds in every repository, as COM-005 does, because the owner reads the research an agent hands over wherever the agent works, while the owner's request for one task, a repository's Overrides entry, or its own rules and docs can set another window. "Last verified" makes the clock the last check of the claims, not the first filing, so a report confirmed last week is fresh however old it is: reuse is review. Research with no date is stale because nobody can tell its age. The way out, saying it is stale, covers a session with no network or a user who wants no new research, and is COM-002's "what is unverified".

Option 2 would reach only the repositories whose docs say it, and leave every agent reading research anywhere else, and every repository whose template still says six months, without the window. Option 3 would drop the rule in forks and in other people's repositories, where the owner still reads what the agent reports.

The block measured 5,367 of its 5,400 characters before the rule and 5,604 after, so the cap rises to 5,700, as [ADR-0035](ADR-0035-Every-Commit-Check-Passes.md) raised it for CODE-004. The hub's research folder now calls a report stale at three months. The Research-Log template lives in the golden path, `tannergolden/path`, and changes there; the hub takes it at its next template sync. The rule gets a scenario, `RES-001-stale-report.json`: a report verified in March 2025 is the basis for a requested recommendation, and the run passes only if the agent's output names the report as stale, out of date, or reverified. No model has been run against it yet.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                              |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | No agent builds on research nobody has checked for three months without saying so, in any repository                              |
| **Negative (-)** | The block grows by 237 characters and the cap by 300; reverifying costs searches and time on work that once reused a report as is |
| **Neutral (~)**  | The rule's kind and the cap are this session's proposals, and stay open to reversal                                               |

---

## ⚖️ Trade-off Comparative

### Option 1: A New Default

- ✅ Holds for every agent, inside a research run or not, and a repository can still set its own window
- ❌ Needs the cap raised

### Option 2: Leave It To The Templates

- ✅ No new rule, and the block stays as it is
- ❌ Reaches only the repositories whose docs say it, and the template's six months still stands in every repository

### Option 3: A New Owner-only Default

- ✅ Leaves other people's projects to their own conventions
- ❌ The owner still reads the agent's research there, and Article I already lets those projects set their own window

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): RES-001, and the cap in Article V
- [`evals/scenarios/RES-001-stale-report.json`](../../evals/scenarios/RES-001-stale-report.json): the rule's scenario
- [`docs/technical/research/README.md`](../technical/research/README.md): the hub's own reports, now stale at three months
- [ADR-0035](ADR-0035-Every-Commit-Check-Passes.md): the last time the cap rose for a rule

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Checked within three months, or checked again.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
