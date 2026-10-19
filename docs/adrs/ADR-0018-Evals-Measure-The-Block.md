<!--
title: '📄 ADR-0018: EVALS MEASURE THE BLOCK'
description: 'Each rule has at least one scenario that tempts an agent to break it, run headless against a real app with the block and without it and checked by code, so the difference shows what the block is worth.'
type: record
keywords: [measurement, rules]
status: 'Proposed'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0018: EVALS MEASURE THE BLOCK

<a name="top"></a>

**Prove each rule changes what an agent does, or cut it.**

_Tempt, run, check, compare._

</div>

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

The loader probe proves an app reads its copy of the rules; it says nothing about whether the agent then follows them. Research found that always-loaded rules reliably change cost and behaviour but rarely change whether a task succeeds, unless they correct a belief or add a skipped step ([ADR-0011](ADR-0011-The-Universal-Rule-Set.md)). Model-judged evals are noisy and cost money, and Anthropic advises regression suites near a 100% pass rate.

---

## 🚦 Decision Drivers

- **Deterministic checks**: the repository, its remote and the commands an agent tried, not a model's opinion.
- **A comparison, not a score**: the same scenario with the block and without it.
- **Safe to run**: nothing outside a scratch folder.
- **Every rule covered**, enforced in CI.

---

## 🏗️ Considered Options

1. **No behavioural evals**: the probe only.
2. **Model-graded evals** with an LLM judge.
3. **Scripted scenarios checked by code**, run with and without the block.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, scripted scenarios

### Rationale for Selection

`evals/scenarios/` holds twenty scenarios covering all nineteen rules: a diverged remote that tempts a force-push, a green pull request that tempts a merge, a failing hook, an AI git identity, a test that could be weakened. `evals/run.py` sets each one up in a scratch repository with a local bare remote and stand-ins for `gh` and `curl` that log their arguments, runs a real app headless, and checks the outcome with code. The summary prints each scenario's pass rate with the block and without it. A few rules can only be checked on the agent's reply, and those scenarios say so. `make lint` fails while a rule has no scenario or a skill has no trigger test, and the tests run every check against a scripted fake app.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                   |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Each rule's effect is measurable; checks are deterministic; every rule and skill is covered, in CI                     |
| **Negative (-)** | Real runs cost model calls and run agents with their own permissions; reply-only checks are approximate                |
| **Neutral (~)**  | The without condition removes the block from the repository only; a true baseline needs the home kit uninstalled first |

---

## ⚖️ Trade-off Comparative

### Option 1: The probe only

- ✅ Free
- ❌ Proves loading, not obedience

### Option 2: Model-graded evals

- ✅ Can judge open-ended replies
- ❌ Noisy, costly, and graded by a model with its own defaults

### Option 3: Scripted scenarios

- ✅ Deterministic and comparable, run by run
- ❌ Covers what code can check

---

## 🔗 Traceability & Links

- [`evals/`](../../evals/README.md), explained in [Evals](../technical/Evals.md)
- [The loader probe](../technical/The-Loader-Probe.md): proves the copies load
- [ADR-0011](ADR-0011-The-Universal-Rule-Set.md): the rules under test

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**A rule earns its place by changing what agents do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
