<!--
title: '📄 ADR-0038: EACH DEPARTMENT IS A SKILL'
description: 'The company''s departments leave board and become nine skills of their own, laid out like every other skill; the three that duplicated a skill are removed, Information Security joins IT, identify gets its own team, and kit.py holds every skill to the same layout.'
type: record
status: 'Superseded'
date: '2026-11-07'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0038: EACH DEPARTMENT IS A SKILL

<a name="top"></a>

**One skill for each department, laid out like every other skill.**

_board convenes the company; each department does its own work._

</div>

> [!IMPORTANT]
> **Superseded by [ADR-0041](ADR-0041-The-Kit-Carries-No-Skills.md).** The
> department skills are gone with every other: the kit carries the guard alone.

> [!NOTE]
> **Amended by [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md).** The
> workforce is now twelve departments, each one skill named for it, with the
> general-purpose skills folded in and duplicated seats merged.

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                              |
| :------------ | :----------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                    |
| **Consulted** | Claude Code sessions: the plan and the change, made at the owner's direction               |
| **Informed**  | Everyone who installs the home kit, and everyone who runs the teams as Grok Bot agents     |
| **Amends**    | [ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md), which kept every department in `board` |

---

## 🎯 Context & Problem Statement

[ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md) moved the Agent Resources workforce into the hub as `board`'s own team: fourteen departments in one `agents/` folder, convened only through `board`. The faculties (`research`, `finance`, `discover` and the rest) are skills of their own, each with its team, and can be called directly. The owner wants the departments to work the same way, and wants the departments that duplicated a skill gone, rather than kept beside it.

---

## 🚦 Decision Drivers

- **Every skill laid out alike**: a `SKILL.md`, its own team in `agents/`, references, templates, a trigger test, a changelog and a licence.
- **One owner for each kind of work**, with no department duplicating a skill.
- **Every team at most six agents**, its lead included.
- **`board` still runs a company**, across departments.

---

## 🏗️ Considered Options

1. **Keep the departments in `board`**, called only through it.
2. **One skill for each department**, the duplicates removed, `board` keeping Administration and convening the rest.
3. **One skill for each department, duplicates kept**, beside the skill each duplicates.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, one skill for each department

### Rationale for Selection

- **Nine department skills**: `legal`, `sales`, `operations`, `people`, `systems`, `analytics`, `quality`, `customers` and `communications`, each with its department's roster and agents, built on `develop`'s template.
- **Three departments removed**: Finance & Accounting, because `finance` now covers a company's money as well as a household's, its six seats taking the books, the model, the cap table and company tax by craft; Research & Development, whose evidence work belongs to `research`, its options to `discover`, its building to `develop` and its product calls to the Chief Executive Officer; and Product Technology, whose technical direction belongs to `develop`'s Engineering Lead.
- **Information Security joins IT** in `systems`, its Chief Information Security Officer keeping the security-risk line straight to the Founder.
- **`identify` gets its own team**, Interview, led by the UX and Design Research Lead, which moved from the dissolved Research & Development department; it still borrows the Writer and the Standards Reviewer.
- **`board` keeps Administration** and convenes the department skills; within a board run it persists the results, and a department skill called on its own persists only its own department's records, behind the same write-gate.
- **`kit.py` holds every skill to the layout**: its `metadata.team` names a roster in its own `agents/`, it ships `assets/trigger-evals.json`, and its metadata holds exactly `team`, `version`, `author` and `status`.
- **The Grok Bot setup** in [`kit/skills/README.md`](../../kit/skills/README.md) builds one group for each team, and its prompt has the Chief of Staff install every skill and team in one pass.

Option 1 keeps the departments callable only through `board`, unlike every other team. Option 3 leaves two owners for a company's money and for research.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                          |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Each department is called directly or convened by `board`; one owner for each kind of work; every skill alike, and a check that keeps them so |
| **Negative (-)** | Nine more skill descriptions in every session's skill list; requests near two skills' borders need clear descriptions and trigger tests       |
| **Neutral (~)**  | Thirty-five company agents remain, plus the faculties' teams; no team tops six                                                                |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Departments In Board

- ✅ No new skills in every session's list
- ❌ The departments cannot be called on their own, unlike every other team

### Option 2: One Skill For Each Department

- ✅ Every team works the same way, and each kind of work has one owner
- ❌ More skill descriptions loaded in every session

### Option 3: Duplicates Kept

- ✅ Nothing removed
- ❌ Two owners for a company's money and for research

---

## 🔗 Traceability & Links

- [Skills & Subagents](../technical/Skills-&-Subagents.md): every skill the kit carries
- [ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md): the hub writes every skill
- [`kit/skills/README.md`](../../kit/skills/README.md): the teams as Grok Bot agents, and the setup prompt

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**One skill for each department, and every skill alike.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
