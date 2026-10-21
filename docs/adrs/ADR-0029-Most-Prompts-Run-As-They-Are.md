<!--
title: '📄 ADR-0029: MOST PROMPTS RUN AS THEY ARE'
description: 'Most universal prompts are written to run as they are, finding their details in the repository, and they cover the work any repository has, area by area, each with a scenario whose proof shows its checks can pass.'
type: record
keywords: [prompts, evals, coding-agents, guardrails]
status: 'Proposed'
date: '2026-10-20'
evidence: '[Prompts For Every Task](https://github.com/tannergolden/intelligence/blob/bb916d0a6f5c977146642985a06aa6809cfc7b99/docs/technical/research/Prompts-For-Every-Task.md)'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0029: MOST PROMPTS RUN AS THEY ARE

<a name="top"></a>

**A prompt for every kind of work, with nothing to fill in that the repository already knows.**

_Find it in the repository. Change only what is safe. Prove it._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                                  |
| :------------ | :------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                        |
| **Consulted** | Claude Code sessions: a research pass across every area of software and repository work, and the design it fed |
| **Informed**  | Every owner and collaborator who copies a universal prompt                                                     |

---

## 🎯 Context & Problem Statement

[ADR-0028](ADR-0028-Every-Prompt-Is-Linted-&-Measured.md) left six universal prompts, each with placeholders to fill in, covering a bug, a feature, a plan, a review, an explanation and a new prompt. Most of the work a repository has fell outside them: setting it up, making its checks pass, testing, keeping the code healthy, reviewing a branch, looking after issues and branches, dependencies, security, CI, releases, docs, production and the agents themselves. And each prompt asked the person for details the repository already holds, such as its commands, its default branch or its last release.

A research pass across every area, filed in the [research log](../technical/research/Prompts-For-Every-Task.md), found that a prompt can find those details for itself, and that what makes such a prompt safe is not its wording but its limits: whether it may edit at all, what it must never run, when it stops for a person, and what proves the work.

---

## 🚦 Decision Drivers

- **Nothing to fill in that the repository knows**: a prompt finds its commands, scope and history itself, and asks only for what lives in a person's head.
- **Safe in any repository**: a prompt says what it may change, never runs what leaves the machine or cannot be undone, and stops where a person decides.
- **Honest results**: a prompt offers the agent a way out, and ends with proof a stranger can re-run, never a claim.
- **Found among dozens**: a reader finds the right prompt by the kind of work, in one index.
- **Measured like the rest**: each new prompt has a scenario, and each scenario shows its own checks can pass.

---

## 🏗️ Considered Options

1. **Keep only prompts to fill in**, and add more of them.
2. **A few broad prompts**, such as one that reviews everything.
3. **Ready-to-run prompts by area**, each finding its details and carrying its area's guardrail, with prompts to fill in kept for what only a person knows.
4. **Skills or slash commands per app**, in place of prompts to paste.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, ready-to-run prompts by area

### Rationale for Selection

The universal prompts grow to 89 in 17 areas: 82 that run as they are, and the 7 that need a person's details, the six that came before and Improve A Prompt. Each ready-to-run prompt reads the repository's instruction files, build files and CI for its commands, finds the default branch and the last release itself, and runs the checks before it edits, stopping if they already fail. Each states its mode: a review, an audit or a triage changes nothing; an edit is local and only where a test, a compiler or a scanner can judge it; a push, a tag, a comment, a merge or anything against a live system is left to the person. Each names its area's signature failure and the guard against it, such as never weakening a test, never printing a secret, never writing an advisory or a hash from memory, and never claiming a speed-up without measurements.

`prompts.py --check` now asks for a **Fill in** line exactly when a prompt holds a placeholder, and for a "Find A Prompt" index that links every prompt once, by its name, and marks each one with details to fill in. A sync pull request counts a long list of added prompts instead of naming every one.

Each new prompt has a scenario in `evals/prompts/`, and every scenario now carries a proof, a script that does the asked-for work. The tests play each scenario against a stand-in app twice, side by side: its proof must pass the checks, and doing nothing must fail them, so no scenario measures nothing. A scenario's setup gains a history of branches, dated commits, tags and git commands, and stand-in tools that print canned replies, such as the issues `gh` would list, so the git, issue and audit prompts can be measured offline.

Option 1 keeps asking people for what the repository knows, and leaves most of the work uncovered. Option 2 dumps whole checklists on every repository and loses the guardrail each area needs. Option 4 serves only the apps that read one format, inside a repository, and the formats keep moving; a prompt with nothing to fill in can still be saved as a skill or a command where an app supports it.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                   |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | A prompt for each kind of work, ready to paste; each states its limits and its proof; every scenario is shown to pass the right work and fail doing nothing            |
| **Negative (-)** | `docs/Prompts.md` grows to 89 prompts, and each needs a scenario; a ready-to-run prompt needs an agent that can open the repository, so a chat app gets only the seven |
| **Neutral (~)**  | The block's hash changes, so the next release brings the new prompts to every repository as a pull request whose diff is the block alone                               |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep Only Prompts To Fill In

- ✅ Works in any app, even one that cannot see the code
- ❌ Asks the person for what the repository already knows, and covers a few tasks

### Option 2: A Few Broad Prompts

- ✅ Little to write and keep
- ❌ Dumps whole checklists, and loses the guardrail each area needs

### Option 3: Ready-To-Run Prompts By Area

- ✅ Each finds its own details and carries its area's limits and proof
- ❌ Many prompts and scenarios to write and keep current

### Option 4: Skills Or Slash Commands Per App

- ✅ One command away in the apps that read them
- ❌ One format per app, only inside a repository, and the formats keep moving

---

## 🔗 Traceability & Links

- [`docs/Prompts.md`](../Prompts.md): the universal prompts, their index and their practices, which moved there from `setup/Prompts.md` with [ADR-0031](ADR-0031-Universal-Prompts-Stay-In-The-Hub.md)
- [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py): the checks
- [`.github/scripts/evals.py`](../../.github/scripts/evals.py) and [`evals/prompts/`](../../evals/prompts/README.md): the scenarios and their proofs
- [Prompts](../technical/Prompts.md) and [Evals](../technical/Evals.md): how each works
- [Prompts For Every Task](../technical/research/Prompts-For-Every-Task.md): the research this rests on
- [ADR-0028](ADR-0028-Every-Prompt-Is-Linted-&-Measured.md): every prompt linted and measured

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
