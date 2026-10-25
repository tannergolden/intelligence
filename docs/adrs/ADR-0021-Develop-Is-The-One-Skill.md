<!--
title: '📄 ADR-0021: DEVELOP IS THE ONE SKILL'
description: 'The hub''s one universal skill is develop, the skill and agent factory from the knowledge vault, made to work in any repository with its Development team and its validator inside its own folder; it replaces building-skills and takes in its decision table and format rules.'
type: record
status: 'Proposed'
date: '2026-10-19'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0021: DEVELOP IS THE ONE SKILL

<a name="top"></a>

**One skill builds every other, and carries everything it needs to do it anywhere.**

_A factory, not a pamphlet._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                          |
| :------------- | :------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                |
| **Consulted**  | Claude Code sessions: a review of the knowledge vault's skills, and drafting           |
| **Informed**   | Every agent and collaborator working in a repository that carries the block            |
| **Supersedes** | [ADR-0014](ADR-0014-One-Skill-That-Builds-Skills.md), the one skill that builds skills |

---

## 🎯 Context & Problem Statement

[ADR-0014](ADR-0014-One-Skill-That-Builds-Skills.md) made `building-skills` the hub's one skill: a guide to deciding what a need is, writing a skill and testing it. The knowledge vault had grown its own skill factory, `develop`, with four modes, a create pipeline, a standing Development team that designs, builds and verifies in separate contexts, a regression ledger, and packaging for the Claude app. It ran only inside the vault: it called the vault's engine for every check, wrote to the vault's folders, and dispatched agents that lived in the vault.

Sorting the vault's seven skills, the owner decided that only `develop` should be universal; the other six stay with the knowledge template, where their folders and personas are. Two skill builders would steal each other's triggers, so one of them had to go.

---

## 🚦 Decision Drivers

- **One universal skill**, the one that builds skills, as ADR-0014 decided.
- **The stronger factory**: independent review, a regression ledger, and packaging.
- **Nothing outside its own folder**, because the home kit installs it in every repository and every app.
- **The same structure and the same workflow** the owner already uses in the vault.

---

## 🏗️ Considered Options

1. **Keep `building-skills`**, and leave `develop` in the vault.
2. **Both**, `building-skills` in the hub and `develop` in the vault.
3. **`develop` replaces `building-skills`**, made universal, with `building-skills`' decision table, placement rules and format rules folded in.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, `develop` replaces `building-skills`

### Rationale for Selection

`kit/skills/develop/` keeps the vault skill's modes, Create pipeline, dispatch scaling, self-improvement loop, mandatory output structure and bootstrap, and drops every mention of the vault:

- **Its Development team ships inside it**, in `agents/`: the roster and five agents, with portable frontmatter and the capability names `kit.py` maps for every app. This is the published form `develop` already described, and its packager now builds it.
- **Gate 1 is its own validator**, `scripts/validate.py`, standard-library Python that checks a skill, an agent, a team or a whole agent library against the format every app accepts. A repository's own rules stay with that repository's checks, which `develop` runs beside it, so a vault keeps its engine and a code repository its CI.
- **Publish is `scripts/package.py`**, which vendors the team from its agent home into the archive and writes the same bytes on every rebuild.
- **The first step of the pipeline is `building-skills`' decision table**: a skill, a rule, a hook, a script or a fact. Skills live by tier: universal in the hub, one repository's in its `.agents/skills/` and `.claude/skills/`, the Claude app's as an archive.
- **The description says "Use when"**, the frontmatter keeps one line per key, its templates sit one level down, it pre-approves no tools, and its licence is MIT.

The scripts' tests live in `.github/scripts/test_develop.py` and its trigger test in `evals/skills/develop.json`, outside the skill, so neither ships. The vault removes its own copy and its Development team, which moved here. Option 2 would leave two skill builders fighting over every request to build a skill; Option 1 would keep the weaker factory.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                        |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every repository and every app gets independent review and a regression ledger when it builds a skill; the vault's factory and the hub's are one                            |
| **Negative (-)** | The kit grows from one small skill to a folder of about two dozen files, and a plain verb for a name needs near misses such as "develop the login page" in its trigger test |
| **Neutral (~)**  | The vault keeps its other six skills and its engine, which `develop` still calls there through the vault's own rules                                                        |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep building-skills

- ✅ The smallest skill to load
- ❌ No independent review, no regression ledger, no packaging

### Option 2: Both

- ✅ Nothing moves
- ❌ Two skills with one job, stealing each other's triggers

### Option 3: develop replaces building-skills

- ✅ One factory everywhere, with its team and its gate inside it
- ❌ A larger skill, and a name that needs careful trigger tests

---

## 🔗 Traceability & Links

- [`kit/skills/develop/SKILL.md`](../../kit/skills/develop/SKILL.md): the skill
- [ADR-0014](ADR-0014-One-Skill-That-Builds-Skills.md): the one skill this replaces
- [ADR-0015](ADR-0015-A-Worker-And-A-Reviewer.md): the Worker and Reviewer, which stay the hub's subagents
- [Skills & Subagents](../technical/Skills-&-Subagents.md): where each app reads the skill

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**One factory, and every skill built through it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
