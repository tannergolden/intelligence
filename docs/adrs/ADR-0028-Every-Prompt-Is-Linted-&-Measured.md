<!--
title: '📄 ADR-0028: EVERY PROMPT IS LINTED & MEASURED'
description: 'The universal prompts are rewritten to the practices current research supports, held to them by prompts.py --check, and each measured by an eval scenario against the one-line request it replaces.'
type: record
status: 'Proposed'
date: '2026-10-20'
evidence: '[Prompt Engineering](https://github.com/tannergolden/intelligence/blob/dbe3e73518bb7f171b88e33299102d31882c9d36/docs/technical/research/Prompt-Engineering.md)'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0028: EVERY PROMPT IS LINTED & MEASURED

<a name="top"></a>

**The practices the prompts preach, checked by code and measured by evals.**

_Written from the evidence. Checked on every push. Measured before a release._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                           |
| :------------ | :------------------------------------------------------------------------------------------------------ |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                 |
| **Consulted** | Claude Code sessions: a research pass over vendor guidance and published studies, and the design it fed |
| **Informed**  | Every owner and collaborator who copies a universal prompt                                              |

---

## 🎯 Context & Problem Statement

[ADR-0025](ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md) gave every repository ready-made prompts, and a list of practices they follow. Nothing held the prompts to those practices: `make check` looked at the markers, private names and dashes, and the rest of the shape lived in tests that searched the source for a few strings. Nothing measured whether a prompt did better than the request it replaces, so a reworded prompt could get worse unseen and still reach every repository at the next release.

A research pass over the model makers' guidance and published studies, filed in the [research log](../technical/research/Prompt-Engineering.md), also found the practices partly out of date. Emphasis in capitals now makes current models overreact. Personas, politeness and threats show no reliable effect. Pasted material belongs in a tag of its own, marked as data. And an agent improves on its work only with feedback from a real check, such as a test that fails before the change, not from an instruction to look it over.

---

## 🚦 Decision Drivers

- **The evidence, not habit**: each practice, and each prompt, rests on what the model makers advise and what studies have measured.
- **Caught before a release**: a broken tag, a stray placeholder or a line a formatter would rewrite reaches every repository, so CI catches it first, with its line.
- **Measured like the rules**: a prompt earns its place by changing what agents do, as [ADR-0018](ADR-0018-Evals-Measure-The-Block.md) holds each rule to.
- **Standard library only**: the checks run wherever the hub's other scripts run, with nothing new to install.

---

## 🏗️ Considered Options

1. **Rewrite the prompts**, and leave the practices to review.
2. **Rewrite and lint**: `prompts.py --check` holds every prompt to the shape.
3. **Rewrite, lint and measure**: also give each prompt an eval scenario that runs it against the hurried request it replaces.
4. **Grade with a model**: a judge model scores what each prompt produces.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, rewrite, lint and measure

### Rationale for Selection

The prompts are rewritten from the research. Each opens with the context and its reason, puts anything pasted last in a tag of its own marked as data, gives a task that starts with a verb, sets limits with a way out, such as stopping when a test looks wrong, and ends with a check that proves the work and a report of what ran. Each asks the agent for any placeholder left unfilled. A sixth prompt, Plan A Change, covers the plan the research puts before any large change.

`prompts.py --check` now reads the block the way a formatter and the standards' Machined Block Check read it, and names any departure by its line: text a formatter would rewrite, a fence a fence reader would end early, a prompt without its **Use when** and **Fill in** lines, a section out of order or never closed, a placeholder that is not one, emphasis in capitals, a character outside printable ASCII, a slot an app would fill by itself, and a prompt over its cap.

`evals.py` gains prompt scenarios in `evals/prompts/`. Each sets up a repository where a hurried request tends to go wrong, keeps the rules in place, and runs the filled prompt and the one-line request against the same checks. Two checks are new: `command_succeeds`, which judges the outcome itself, and `fails_before`, which proves a test the agent wrote catches the problem on the code before the change. `make lint` fails while a universal prompt has no scenario, or a scenario fills a placeholder its prompt no longer holds.

Option 1 trusts the eye that missed two headings a reader could not tell apart in the first version of this block. Option 2 catches the form but says nothing of the effect. Option 4 needs a judge checked against labelled outcomes before its grades mean anything, and the code checks the hub already trusts cover the outcomes that matter here.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                      |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | A broken prompt fails CI with its line, and a reworded prompt's effect can be measured, run by run, against the request it replaces                       |
| **Negative (-)** | Every new universal prompt needs a scenario; the formatter rules only approximate Prettier, which runs only where installed; reply checks are approximate |
| **Neutral (~)**  | The block's hash changes, so the next release brings the new prompts to every repository as a pull request whose diff is the block alone                  |

---

## ⚖️ Trade-off Comparative

### Option 1: Rewrite The Prompts

- ✅ Nothing new to maintain
- ❌ The practices hold only as long as every reviewer remembers them

### Option 2: Rewrite And Lint

- ✅ Every departure from the shape fails CI, with its line
- ❌ A prompt can keep its shape and still do worse

### Option 3: Rewrite, Lint And Measure

- ✅ The shape is checked on every push, and the effect is measured before a release
- ❌ A scenario to write and keep for every universal prompt

### Option 4: Grade With A Model

- ✅ Judges open-ended answers that code cannot
- ❌ Its grades mean nothing until the judge is checked against labelled outcomes, and each run costs a second model call

---

## 🔗 Traceability & Links

- [`setup/Prompts.md`](../../setup/Prompts.md): the universal prompts and their practices
- [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py): the checks
- [`.github/scripts/evals.py`](../../.github/scripts/evals.py) and [`evals/prompts/`](../../evals/prompts/README.md): the measurement
- [Prompts](../technical/Prompts.md) and [Evals](../technical/Evals.md): how each works
- [Prompt Engineering](../technical/research/Prompt-Engineering.md): the research this rests on
- [ADR-0025](ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): the prompts every repository gets

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**A prompt earns its place by changing what agents do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
