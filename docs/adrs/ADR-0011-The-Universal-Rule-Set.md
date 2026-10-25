<!--
title: '📄 ADR-0011: THE UNIVERSAL RULE SET'
description: 'The block holds nineteen rules, eleven Invariants and three Defaults for every repository and five Defaults for the owner''s repositories, each one sentence with a reason and an enforcer.'
type: record
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0011: THE UNIVERSAL RULE SET

<a name="top"></a>

**Nineteen rules, each one there because an agent would otherwise get it wrong.**

_Short enough to obey. Specific enough to check._

</div>

> [!IMPORTANT]
> **Amended by [ADR-0020](ADR-0020-One-Constitution.md).** The rules now live in
> `CONSTITUTION.md` at the hub's root, and the set has grown to 22: SEC-003
> allows a private vault, COM-002 covers earlier sessions, STD-001 yields to the
> Invariants, and COM-004, DOC-003 and COM-005 are new.

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

The draft block had twenty-two rules, ten Invariants and twelve Defaults, plus POL-001 in the home copy. Research across five strands tested it: empirical studies of instruction files, incidents and failure modes, vendor guidance, the best public rule sets, and wording and precedence. It found that always-loaded rules reliably change cost and behaviour but rarely change whether a task succeeds, unless they correct what a model believes or add a step it skips. The owner's ruling that every agent follows the standards also contradicted three draft rules.

---

## 🚦 Decision Drivers

- **Every rule earns its tokens**: it states a fact the agent cannot infer, opposes a documented default, or adds a cheap step agents skip.
- **The block fits its cap**: 4,000 characters, read by every app on every session.
- **Every rule is one checkable sentence**, worded for 2026 models: no capitals, no MUST, each "never" paired with what to do instead.
- **No rule contradicts the standards' gates.**

---

## 🏗️ Considered Options

1. **Keep the draft block** as it was.
2. **An exhaustive block** that names every failure mode the research found.
3. **The researched set**: nineteen rules, with additions, merges and cuts each traced to evidence.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, the researched nineteen-rule set

### Rationale for Selection

The set adds what the draft lacked:

- CODE-002: never pass a check by weakening it, with explicit permission to stop, the wording that nearly eliminated test gaming.
- OPS-005: push, open pull requests or publish only when asked for that specific action.
- STD-001: the pointer to the standards, tied to the moments an agent should read them.

POL-001 becomes an Invariant in the shared block, with a clause that discloses AI help where a project's policy says nothing. MEM-001 folds into SEC-003, WORK-003 into CODE-001, GIT-011 into GIT-010 and DOC-001 into STD-001. COM-001, COM-003 and OPS-002 are cut: the precedence text, harness prompts and `make audit` cover them. GIT-001 and GIT-013 follow the standards: the human authors and signs, and the AI is credited with `Co-Authored-By:`. An exhaustive block would blow the cap, and joint compliance falls as rules accumulate.

The owner settled the open questions on 2026-10-17: STD-001 stays a Default, forks count as outside repositories, and a repository with no remote yet counts as the owner's. The law in `law/` is this set, and `render.py --check` holds it to the cap and to the rules for rules.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                        |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Every rule traces to evidence; the block agrees with the standards' gates; it measures 3,640 of 4,000 characters            |
| **Negative (-)** | The block runs 440 characters over its 3,200 target; SEC-003 and POL-001 have no enforcement today, only enforcement to add |
| **Neutral (~)**  | Each release should test rules with and without them, and drop any that shows no effect                                     |

---

## ⚖️ Trade-off Comparative

### Option 1: The draft block

- ✅ Already written
- ❌ Three rules contradict the standards, and test integrity and outward actions go unaddressed

### Option 2: An exhaustive block

- ✅ Nothing left unsaid
- ❌ Over the cap, and every added rule lowers compliance with the rest

### Option 3: The researched set

- ✅ Short, checkable, and aligned with the standards
- ❌ Some Invariants wait on enforcement still to build

---

## 🔗 Traceability & Links

- The Law, the nineteen rules as files with each one's reason and enforcer, since gathered into [the Constitution](../../CONSTITUTION.md) ([ADR-0020](ADR-0020-One-Constitution.md))
- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the precedence text that opens the block
- [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md): why the git rules follow the standards

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Nineteen rules, every one with a reason.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
