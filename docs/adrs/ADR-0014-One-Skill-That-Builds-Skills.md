<!--
title: '📄 ADR-0014: ONE SKILL, THE ONE THAT BUILDS SKILLS'
description: 'The hub ships exactly one skill for now, building-skills, which teaches an agent to decide whether a need is a skill at all and to build, test and ship one in the format every app accepts.'
type: record
status: 'Superseded'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0014: ONE SKILL, THE ONE THAT BUILDS SKILLS

<a name="top"></a>

**Start with the skill that makes every other skill right.**

_One skill now. The right shape for every one after._

</div>

> [!IMPORTANT]
> **Superseded by [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md).** The one
> skill is now `develop`, made to work in any repository, with this record's
> decision table and format rules folded into it.

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

The plan moved procedures out of the always-loaded block into skills, and drafted four of them: a pull request report, commits, a bug fix from a reproduction, and adding a dependency. Skills load only when their description matches the task, and one published evaluation found a skill was never invoked in 56% of cases. The apps disagree on where skills live: Claude Code reads only `~/.claude/skills/`, Codex, Copilot, Cursor and Grok read `~/.agents/skills/`, and Antigravity reads its own folder. The owner decided on 2026-10-18 that there should be only one skill for now: a meta skill for building other skills.

---

## 🚦 Decision Drivers

- **The owner's decision**: one skill, the one that builds skills.
- **Every future skill starts right**: the format, the description that triggers, and tests.
- **Nothing that must always hold lives in a skill.**
- **Copies where each app reads them**, never overwriting a folder the kit does not own.

---

## 🏗️ Considered Options

1. **The four procedure skills** the plan drafted.
2. **No skills** until the procedures settle.
3. **One meta skill, `building-skills`**, with the renderer enforcing the format it teaches.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, one meta skill

### Rationale for Selection

`skills/building-skills/` teaches the decision first: a procedure becomes a skill, behaviour that must always hold becomes a rule, something that must never happen becomes a hook or a check. It then covers where a skill lives, how to write it from real work, the format every app accepts, the trigger and quality tests, and how to ship it through the hub. `kit.py` refuses any skill that breaks that format, so the skill and the renderer agree. The home kit copies it into all three skills folders with a mark, and the loader probe's `--skills` canary proves each app sees exactly one copy, which was the plan's gate for shipping skills as copies. The four drafted procedures wait until the owner asks for them, and `building-skills` is how they will be built.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                          |
| :--------------- | :------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | One skill to maintain; every later skill inherits its format and tests; the renderer enforces what it teaches |
| **Negative (-)** | The drafted procedures stay prose in the standards until someone builds them                                  |
| **Neutral (~)**  | Its trigger test lives in `evals/skills/`, outside the folder, so it never ships                              |

---

## ⚖️ Trade-off Comparative

### Option 1: Four procedure skills

- ✅ Covers common procedures now
- ❌ Four skills to tune and test before the format is settled

### Option 2: No skills

- ✅ Nothing to load or test
- ❌ Every future skill starts from scratch

### Option 3: One meta skill

- ✅ Small, and multiplies into every later skill
- ❌ Delivers no procedure on its own

---

## 🔗 Traceability & Links

- `skills/building-skills/SKILL.md`, since replaced by [`develop`](../../kit/skills/develop/SKILL.md) ([ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md))
- [The loader probe](../technical/The-Loader-Probe.md): the duplicate-skill canary
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): skills are named for what they do

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The first skill is the one that makes the rest.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
