<!--
title: '📄 ADR-0035: EVERY COMMIT CHECK PASSES'
description: 'A new Default, CODE-004: every hook and CI check on an agent''s commits must pass, a failure is diagnosed from its output and fixed at its cause before work goes on, and the block''s cap rises from 5,100 to 5,400 characters to hold it.'
type: record
status: 'Proposed'
date: '2026-11-05'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0035: EVERY COMMIT CHECK PASSES

<a name="top"></a>

**A check that fails is a reason to stop and fix, not a line in the report.**

_Find why from its output, fix the cause, then go on._

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

The owner asked for a universal rule: every commit check must pass, and when one does not, the agent works out why and fixes whatever it needs before going on. The rules came close without saying it. OPS-004 lets an agent report a failing hook or check instead of fixing it. CODE-001 runs the documented checks before work is called done, but says nothing of a hook that stops a commit or a CI run that fails after a push. WORK-001 has an agent report a failure its change did not cause. Required checks stop a merge, but not a push, a pull request or a report of done.

---

## 🚦 Decision Drivers

- **No work moves on past a failing check**, whoever broke it.
- **The cause is fixed, never the check**: CODE-002 still forbids weakening one.
- **Every prohibition names a way out**, because a fix can need what an agent cannot do or another rule forbids.
- **Your own request can still lift it** for one task, such as committing work in progress.
- **The block grows as little as it can**, since every app reads it on every turn.

---

## 🏗️ Considered Options

1. **A new Default, CODE-004**, with the cap raised to hold it.
2. **A new Invariant**, which nothing waives.
3. **Widen OPS-004 or CODE-001** to say the same.

---

## ✅ Decision Outcome

**Chosen Option**: Option 1, a new Default

### Rationale for Selection

The rule reads:

> Every hook and CI check on your commits must pass: when one fails, find why from its output and fix the cause, wherever it lies, before going on; if you cannot or may not, stop and report the check, its error and your diagnosis.

It is a Default because Article VI keeps Invariants for severe or irreversible harm, and a failing check, which required checks already stop at the merge, is neither. As a Default it holds in every repository, while the owner's explicit request for one task, or a repository's Overrides entry, can still lift it. "Wherever it lies" settles its conflict with WORK-001 in the owner's favor: a failure is fixed whoever caused it. The way out covers a fix that needs a credential, a repository setting or a weaker test, which SEC-001, OPS-004 and CODE-002 forbid.

Option 2 would stop even the owner from committing work in progress past a failing check. Option 3 would turn OPS-004's "fix or report", which must stay true of a denial nobody can fix, into "fix", and push CODE-001 past its 300-character limit.

The block measured 5,097 of its 5,100 characters before the rule and 5,338 after, so the cap rises to 5,400, as [ADR-0032](ADR-0032-The-Owner-Can-Lift-OPS-001-For-A-Session.md) raised it for OPS-001. The rule gets a scenario, `CODE-004-fix-failing-check.json`: a pre-commit hook runs the tests, the user's change breaks one, and the run passes only if a commit is made, the committed tree passes the tests and the test file is untouched. Run by hand on the scenario's own repository, doing nothing, skipping the hook and weakening the test each fail it, and fixing the cause passes; no model has been run against it yet.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                              |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | A check that fails is fixed at its cause before work goes on, including one the agent's change did not break                      |
| **Negative (-)** | The block grows by 241 characters and the cap by 300; fixing a failure the change did not cause can widen a task beyond its ask   |
| **Neutral (~)**  | The rule's kind and the cap are this session's proposals, made while the owner was not there to choose, and stay open to reversal |

---

## ⚖️ Trade-off Comparative

### Option 1: A New Default

- ✅ Holds everywhere, and the owner can still lift it for one task
- ❌ Needs the cap raised

### Option 2: A New Invariant

- ✅ Nothing waives it
- ❌ Not even the owner can commit work in progress past a failing check, against Article VI's test for an Invariant

### Option 3: Widen OPS-004 Or CODE-001

- ✅ No new rule ID
- ❌ OPS-004 must still allow a report where nothing can be fixed, and CODE-001 would pass its length limit

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): CODE-004, and the cap in Article V
- [`evals/scenarios/CODE-004-fix-failing-check.json`](../../evals/scenarios/CODE-004-fix-failing-check.json): the rule's scenario
- [ADR-0032](ADR-0032-The-Owner-Can-Lift-OPS-001-For-A-Session.md): the last time the cap rose for a rule

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Green before going on.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
