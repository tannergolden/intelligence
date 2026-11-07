<!--
title: '📄 ADR-0039: TWELVE DEPARTMENTS, TWELVE SKILLS'
description: 'The workforce is twelve departments that cover every area of a company and of the owner''s own life, each one skill named for the department with a team of at most five; the general-purpose skills fold into the departments, eighteen agents merge into others, and the Chief of Staff''s Grok Bot setup starts by asking for GitHub and the owner''s vault.'
type: record
status: 'Proposed'
date: '2026-11-07'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0039: TWELVE DEPARTMENTS, TWELVE SKILLS

<a name="top"></a>

**One skill for each department, and one department for every area of work and of life.**

_Fewer seats, each doing more, none duplicated._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                |
| :------------ | :------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                      |
| **Consulted** | Claude Code sessions: the plan, its audit and the change, made at the owner's direction      |
| **Informed**  | Everyone who installs the home kit, and everyone who runs the departments as Grok Bot agents |
| **Amends**    | [ADR-0038](ADR-0038-Each-Department-Is-A-Skill.md), which kept seven general-purpose skills  |

---

## 🎯 Context & Problem Statement

After [ADR-0038](ADR-0038-Each-Department-Is-A-Skill.md) the kit carried seventeen skills and teams: ten for a company and seven general-purpose ones (`research`, `discover`, `develop`, `editorial`, `visualize`, `finance`, `identify`). The owner wants the workforce to be the twelve departments every company has, Administration, Finance & Accounting, Legal & Compliance, Sales & Marketing, Operations & Logistics, Human Resources, Information Technology, Research & Development, Business Intelligence, Quality Assurance, Customer Experience and Public Relations, covering every area of any business and of the owner's personal life, each skill named for its department.

---

## 🚦 Decision Drivers

- **Twelve departments, no other teams**, each one skill named for it.
- **Every area covered**, a company's and the owner's own.
- **No duplicated seat**: two agents that did one job become one.
- **Every team at most five**, so a Grok Bot group of six holds a department and the Chief of Staff.

---

## 🏗️ Considered Options

1. **Keep the general-purpose skills beside the departments**, borrowing department seats.
2. **Fold every skill and team into the twelve departments.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, twelve departments

### Rationale for Selection

- **The skills**: `administration` (was `board`), `finance-and-accounting` (was `finance`), `legal-and-compliance`, `sales-and-marketing`, `operations-and-logistics`, `human-resources` (with `identify`'s profile interview), `information-technology`, `research-and-development` (with `research`, `discover` and `develop`, its validator and packager among them), `business-intelligence` (with `visualize`), `quality-assurance`, `customer-experience` and `public-relations` (with `editorial`).
- **Eighteen agents merge into others**: the Research, Creative and Engineering leads and the Tournament Ranker into one Head of Research & Development; the Information Specialist into the All-Source Analyst; the Idea Curator into the Idea Generator; the Software Architect into the Full-Stack Engineer; the Idea Critic into the Devil's Advocate; develop's QA Engineer into the QA Test Engineer; the Plan Reviewer into the Fact-Checker; the Standards Reviewer into the Compliance Officer; the Portfolio Manager into the Chief Operating Officer; the Editorial Lead into the Chief Communications Officer; the Long-Form and Technical Writers into the Writer; the Line and Developmental Editors into one Editor; the Design Lead into the Chief Data Officer; the Application Security Engineer into the Security Engineer; and the Product Marketing and Demand Generation managers into one Marketing Manager. The Financial Planning Lead becomes the Chief Financial Officer, and Human Resources gains a Wellbeing Specialist, which never diagnoses or prescribes. Fifty-one agents remain.
- **Quality Assurance is the one independent check**, its Fact-Checker, Devil's Advocate, Design Critic and QA Test Engineer borrowed by the departments whose work they verify.
- **Every department covers the owner's own life**, from Administration's goals and decisions to Customer Experience's complaints and returns, and every skill keeps the owner's personal context only in a repository made to hold it.
- **Renames**: Sales & Revenue becomes Sales & Marketing, and Client Experience becomes Customer Experience, matching the knowledge template's venture folders.
- **The Chief of Staff's Grok Bot setup** first asks whether GitHub is connected and which repository holds the owner's vault, tests the app's group rules before it builds, and forms a temporary working group when a job needs several departments.

Option 1 keeps seventeen teams and the duplicated seats.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                        |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Twelve teams, one per department; no duplicated seat; every area of work and life has an owner; every Grok Bot group fits six               |
| **Negative (-)** | Merged skills carry several procedures in one description, so their triggers need the model trigger tests; the old skill names stop working |
| **Neutral (~)**  | Fifty-one agents, from sixty-eight                                                                                                          |

---

## 🔗 Traceability & Links

- [Skills & Subagents](../technical/Skills-&-Subagents.md): the twelve skills
- [`kit/skills/README.md`](../../kit/skills/README.md): the departments as Grok Bot agents, and the setup prompt
- [ADR-0038](ADR-0038-Each-Department-Is-A-Skill.md): each department is a skill

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Twelve departments, and every area has one.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
