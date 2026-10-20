<!--
title: '📄 ADR-0009: AGENTS FOLLOW THE STANDARDS'
description: 'Every AI agent follows the engineering standards in tannergolden/standards in every repository the owner owns, new ones included, through an owner-only Default that points at them, while forks and other people''s repositories follow their own rules.'
type: record
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0009: AGENTS FOLLOW THE STANDARDS

<a name="top"></a>

**One set of engineering standards for people and agents, linked from the rules and never copied into them.**

_The rules point. The standards decide._

</div>

> [!NOTE]
> **Corrected by [ADR-0030](ADR-0030-Rules-Written-For-Current-Models.md).** No
> source could be found for the rise in doc reading from 11% to 75% cited below:
> summaries of Vercel's published evaluation give pass rates of 53%, 53%, 79%
> and 100% instead. STD-001's reason now rests on SWE-CC, where agents tried a
> URL in 28.9% of runs and opened a local rules file in 91.6%.

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

The owner ruled on 2026-10-17 that any coding project or development work done by an AI agent follows the standards in tannergolden/standards. The draft rules carried git conventions of their own, and three of them contradict the standards:

| Draft rule | Draft text                                           | The standards                                                                                                            |
| :--------- | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| GIT-001    | Never add `Signed-off-by`                            | The author is the human contributor read from git's configuration, never the AI, and the sign-off names that same person |
| GIT-011    | Branch as `agent/<issue>-<slug>`                     | Branch by intent, such as `feat/` or `bugfix/`, with no tool names                                                       |
| GIT-013    | An `Assisted-by` trailer, and no AI `Co-Authored-By` | Every commit an AI contributed to carries `Co-Authored-By:` for it, above the sign-off                                   |

Agents rarely open a policy file they are only pointed at, and other projects publish contributing and AI policies of their own, some of which reject exactly what the standards require.

---

## 🚦 Decision Drivers

- **One set of conventions** for people and agents.
- **No rule in the block that a standards check would reject.**
- **The standards stay the single source**, followed by link.
- **Other projects' rules are respected**: the owner's conventions must not break a policy in someone else's repository.

---

## 🏗️ Considered Options

1. **The block carries its own git and style conventions.**
2. **The block points at the standards with an owner-only Default**, STD-001, and gives one line each to the standards no gate checks.
3. **The block copies the standards in.**

Two questions came with the choice: whether the pointer is an Invariant or a Default, and whether the standards reach every repository or only the owner's.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, an owner-only pointer that stays a Default

### Rationale for Selection

STD-001 sends every agent to the standards before it commits, branches, opens a pull request, writes docs or tests, or adds a dependency, and says the standards differ from the agent's defaults and win over the block. A bare link is rarely followed. A pointer tied to specific moments that says the agent's defaults are wrong is the pattern that raised doc reading from 11% to 75% in Vercel's published agent evaluations. The standards no gate checks also get one line each:

- GIT-001: the human author and sign-off
- GIT-010: branch and commit names
- GIT-012: pull request size
- GIT-013: `Co-Authored-By:` for the AI
- DOC-002: no em dash

A copy of the standards would go stale the day they change, and conventions of the block's own already contradict them in three rules.

GIT-001 states the result, not the command: the author and the sign-off are the user's git identity, never an AI's, and the agent asks whose identity to use when `user.email` is unset or an AI's. The standards' own fallback, `git commit -s --author=<contributor>`, signs off as the committer. In a Claude Code cloud session, where the committer is the agent, it produced `Signed-off-by: Claude`.

STD-001 stays a Default, as decided on 2026-10-17. An Overrides entry naming it is the owner's own recorded exception for one repository, and `make audit` asks for a reason. Invariants stay limited to safety and honesty, where nothing should waive them.

The standards and the other owner-only Defaults reach every repository the owner owns, including a new one with no remote yet, so a new project follows them from its first commit. Forks and other people's repositories follow their own rules: there, the project's contributing and AI policy wins over the remaining Defaults, and every Invariant still holds. POL-001 makes the agent read that policy before its first commit or post. If it bars AI contributions, the agent publishes nothing; if it says nothing about AI, the agent discloses AI help in the pull request. Carrying the owner's conventions further would break real policies: some projects reject an AI `Co-Authored-By:`, and the Linux kernel forbids AI sign-offs.

This hub follows the same standards: a `feat/` branch, scoped commits, records made from the ADR template, and commits authored and signed off by the owner with `Co-Authored-By:` for the agent.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                     |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | The block and the standards' checks never disagree; conventions change in one place; a new project follows the standards from its first commit           |
| **Negative (-)** | A pointer still misses some runs, which is why the standards no gate checks also get a line each in the block                                            |
| **Neutral (~)**  | In forks and other people's repositories, only the Invariants and the three everyday Defaults apply, and the project's own rules win over those Defaults |

---

## ⚖️ Trade-off Comparative

### Option 1: Conventions of the block's own

- ✅ Self-contained
- ❌ Already contradicts the standards in three rules

### Option 2: An owner-only pointer

- ✅ One source, followed wherever it applies
- ❌ A pointer is followed less reliably than a rule written in the block

### Option 3: Copy the standards in

- ✅ Everything in one place
- ❌ Far over the block's 4,000-character budget, and stale at the next change

---

## 🔗 Traceability & Links

- [Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md)
- [Conventional Commits](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Conventional-Commits.md): who a commit is by, and its trailers
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the precedence text, and where owner-only Defaults reach
- [ADR-0008](ADR-0008-Names-Without-Prefixes.md): the rule IDs this record names

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The rules point, and the standards decide.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
