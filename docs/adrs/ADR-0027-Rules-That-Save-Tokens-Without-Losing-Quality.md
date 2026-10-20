<!--
title: '📄 ADR-0027: RULES THAT SAVE TOKENS WITHOUT LOSING QUALITY'
description: 'Four Defaults that cut what an agent pulls into its context, CODE-003, WORK-004, WORK-005 and WORK-006, chosen because the research found input, not output, drives cost, and rejecting the brevity rules that trade accuracy away.'
type: record
keywords: [tokens, cost, context, efficiency, defaults]
status: 'Proposed'
date: '2026-10-20'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0027: RULES THAT SAVE TOKENS WITHOUT LOSING QUALITY

<a name="top"></a>

**Four Defaults that keep waste out of an agent's context, and none that make it think less.**

_Fewer tokens in, the same work out._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                               |
| :------------ | :------------------------------------------------------------------------------------------ |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                     |
| **Consulted** | A Claude Code research run across vendor documentation, published studies and practitioners |
| **Informed**  | Every repository that carries the block                                                     |
| **Amends**    | [ADR-0011](ADR-0011-The-Universal-Rule-Set.md), the universal rule set                      |

---

## 🎯 Context & Problem Statement

The owner asked for universal rules that make agents spend fewer tokens, on one condition: saving tokens must never cost accuracy or quality. COM-004 already keeps answers sized to the question and stops whole-file reads where a section will do. The question was what else, inside the block's 5000-character cap, saves tokens at no cost to the work.

---

## 🚦 Decision Drivers

- **No loss in quality**: a rule that saves tokens by skipping verification, reasoning or reading is out.
- **Where the tokens go**: in agent sessions, input dominates. Tool output was about 84% of each turn's tokens in one SWE-agent study, file reads 67 to 76% in another, and every turn resends what came before.
- **The block's size**: every app reads the whole block on every turn, so each sentence must pay for itself.

---

## 🏗️ Considered Options

1. **Rules that keep waste out of the context**: short command output that keeps failures, parallel batches without re-reads, the narrowest test first, and no third guess at a failing fix.
2. **Brevity and reasoning-budget rules**: concise or drafted reasoning, numeric token budgets.
3. **No new rules**, leaving cost to settings: effort, model, compaction and hooks.

---

## ✅ Decision Outcome

**Chosen Option**: Option 1, rules that keep waste out of the context

### Rationale for Selection

The measured no-loss savings all come from what an agent carries, not from what it writes or thinks. Masking stale tool output halved cost with no drop in solved tasks on SWE-bench Verified, and pruning file reads to the relevant lines cut 23 to 54% of tokens at similar success. The four rules ask for that behaviour directly, each with a clause that guards quality: failures and their context stay in trimmed output, a changed file is read again, the full checks still run once, and a stuck fix gets a diagnosis rather than silence.

Option 2 fails the owner's condition. Drafted reasoning cut about 80% of tokens but lost four points on GSM8K, concise reasoning lost 28% on math for a smaller model, and budgets set too tight made models overshoot and cost more. Option 3 leaves the largest lever, what an agent chooses to read and run, untouched.

Two candidates stay out: a delegation rule, because subagents protect the main context but use more tokens overall, and a search-before-open rule, which COM-004 already covers. No study yet measures one rule in an instruction file on its own, so the four rules carry scenarios in `evals/scenarios/` to measure them here.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                    |
| :--------------- | :------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Agents carry less noise from turn to turn, which costs less and keeps the instructions that matter seen |
| **Negative (-)** | The block grows to 4884 characters, past its 4500 target and inside its 5000 cap                        |
| **Neutral (~)**  | Settings such as effort, model and compaction still decide much of the cost, and no rule reaches them   |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep Waste Out

- ✅ Matches the measured no-loss savings, and every rule guards the step it trims
- ❌ The case for each one-line rule rests on harness experiments and vendor guidance, not a test of the line itself

### Option 2: Think And Write Less

- ✅ The largest raw cuts in output tokens
- ❌ Measured accuracy losses, and budgets that backfire

### Option 3: Settings Only

- ✅ The block stays at its size
- ❌ Leaves reading and running, where most tokens go, to chance

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): CODE-003, WORK-004, WORK-005 and WORK-006, each with its reason
- [Eval scenarios](../../evals/scenarios/README.md): one scenario for each rule
- [ADR-0011](ADR-0011-The-Universal-Rule-Set.md): the universal rule set these join

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Less carried, nothing lost.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
