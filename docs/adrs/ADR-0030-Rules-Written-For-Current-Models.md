<!--
title: '📄 ADR-0030: RULES WRITTEN FOR CURRENT MODELS'
description: 'The universal rules are revised on evidence about the mainstream models of October 2026: eleven sentences reworded, two Defaults folded, an Invariant for installing packages added, and the mechanisms the restraint rules depend on built into the home kit.'
type: record
keywords: [rules, constitution, coding-agents, guardrails, evals]
status: 'Proposed'
date: '2026-10-20'
evidence: '[Rules For Current Models](https://github.com/tannergolden/intelligence/blob/23d2b3525059f8d6ae11182a7f11eae376859922/docs/technical/research/Rules-For-Current-Models.md)'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0030: RULES WRITTEN FOR CURRENT MODELS

<a name="top"></a>

**Rules for the models that read them today, and something outside the text behind every rule that must hold.**

_Name the act. State the end. Leave a way out._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                                      |
| :------------ | :----------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                            |
| **Consulted** | Claude Code sessions: a research pass on rules for coding agents, a second on current models alone, and the change |
| **Informed**  | Every repository and machine that carries the block                                                                |

---

## 🎯 Context & Problem Statement

The rules in [`CONSTITUTION.md`](../../CONSTITUTION.md) were written from evidence that mostly measured Claude 4.x, GPT-5.x and older models. The owner asked for the best universal rules possible, judged on up-to-date research about the models mainstream tools run now. A second research pass, filed in the [research log](../technical/research/Rules-For-Current-Models.md), counted only the Claude 5 family, the GPT-6 family, Gemini 3.1 Pro and later, and the other makers' 2026 models, and found that no independent study behind the rules had tested any of them.

What the current evidence says: the newest models no longer game impossible tests or follow most injected instructions, but they still read permission as license, working around warnings and blocks in 13 to 28% of adversarial runs; they need opposite corrections, some over-checking and over-asking while others skip checks and rarely ask; a prohibition holds best with a named way to stop; and the vendors' own harnesses now open draft pull requests, push to default branches and fail open by default, against the restraint rules.

---

## 🚦 Decision Drivers

- **Rules that hold for every maker**: a repository cannot know which model reads its block, so a rule names an act and an end state, not an effort a model may overdo.
- **Current evidence only**: a reason that cites an older model says so, or goes.
- **A way out for every prohibition**: a rule never leaves an agent the choice between breaking it and failing.
- **Mechanisms behind restraint**: a rule whose failure costs more than a retry needs something outside the text, and the hub builds what it can.
- **Within the cap**: the block stays under 5,000 characters.

---

## 🏗️ Considered Options

1. **Keep the rules as they were.**
2. **Revise the sentences and build their mechanisms**, keeping the constitution's shape.
3. **A few Invariants only**, leaving the rest to the vendors' own prompts.
4. **One block per model family.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, revise the sentences and build their mechanisms

### Rationale for Selection

The constitution's shape holds: a small unwaivable tier whose rules each name an enforcer, one sentence per behavior, no emphasis, and an explicit precedence ladder whose "do the rest, skip that part and name the rule ID" is the way out the evidence asks for. The changes are in the sentences, the reasons and the mechanisms.

Eleven sentences are reworded. SEC-001 adds using a credential the agent was not given. SEC-002 keeps text that claims authority in the information it is. SEC-004 is new: install only what the task needs, from the project's own registry, after checking each package is the one intended, and never pipe a download into a shell. OPS-003 asks for the exact command with full paths, and adds permissions. OPS-005 names drafts, deploys, and messages or data sent outside. POL-001 adds the pull request template. CODE-002's way out becomes "stop and report which and why". COM-002 adds what is unverified. CODE-001 absorbs CODE-003's narrowest-test-first order, and a check that failed to start or ran nothing no longer counts. WORK-001 asks for all of the task and only the task, and a question gets an answer, not a change. WORK-002 takes the reading the request and code best support, rather than the most conservative one. DOC-003 absorbs COM-004's lead-with-the-answer, and COM-004's clause against narrating reasoning goes, since current guidance says to remove it.

The block drops its source line, which asked agents to open a file they rarely open, and measures 4,997 of its 5,000 characters, 25 rules. Every reason was rewritten on current-model evidence, with previous-generation figures labelled or dropped; STD-001's figure for doc reading, which no source held, gives way to SWE-CC's. Article VI gains an admission test for every rule, a release note naming each rule ID a release changes, and a note that a retired Invariant still holds wherever an older copy loads.

The mechanisms the restraint rules name are built into the home kit with this change. The guard denies piping a download into a shell, an install that overrides the registry on the command line, a read of a credential store in the home folder, a recursive delete of a Windows drive or home folder, and an em dash written into a file, commit or pull request in a repository the owner owns. On local machines the installer adds Claude Code ask-first permissions for pushes, pull requests, comments, releases and publishing, and a hook that restates the Invariants after Claude Code compacts a conversation. Codex rules, Antigravity Ask entries and a Cursor hook that fails closed stay on the To add lists.

Every new or reworded rule's scenarios, nineteen in all and six of them new, run on Claude Code with Claude Opus 5.5, seven times with the block and seven without. Codex, Copilot CLI, Antigravity and Cursor were not installed where the evals ran, so their runs are still to make.

Some proposals were declined. Claude Code's `includeGitInstructions: false` would strip its own commit-only-when-asked and git safety text from every repository, including those where the owner's git rules do not apply, so the kit leaves it on. A fixed `attribution` value would lose the model name Claude Code's default trailer already carries, which is what GIT-013 asks for. Moving the source into the block's marker would break older installers and syncs, which read the marker strictly. DOC-002 stays in the block until a check on changed files runs in CI and its without-block eval passes. A rule against agreeing with a user's wrong claim waits for current-model numbers.

Option 1 keeps reasons that describe models nobody runs, and rules the harnesses now contradict. Option 3 leaves the owner's defaults to prompts that disagree with each other and have dropped restraint. Option 4 cannot work, because a repository cannot know which model reads it, and copies per model would drift.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                           |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Rules that hold across makers and give every prohibition a way out; restraint backed by the guard and by ask-first permissions; reasons that cite the models in use            |
| **Negative (-)** | The block sits 3 characters under its cap, so the next rule must cut another; local Claude Code asks before every push, pull request and publish, even ones the user asked for |
| **Neutral (~)**  | The block's hash changes, so the next release reaches every repository as a pull request whose diff is the block alone                                                         |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Rules As They Were

- ✅ No churn for any repository
- ❌ Reasons cite models nobody runs, and the harnesses contradict several rules

### Option 2: Revise The Sentences And Build Their Mechanisms

- ✅ Rules that hold across makers, each with a way out and something behind it
- ❌ The block nears its cap, and every app needs its own mechanism

### Option 3: A Few Invariants Only

- ✅ A much shorter block
- ❌ The owner's defaults would rest on vendor prompts that disagree and have dropped restraint

### Option 4: One Block Per Model Family

- ✅ Each model gets the correction it needs
- ❌ A repository cannot know which model reads it, and the copies would drift

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): the rules, their reasons and their enforcement
- [`kit/guard.py`](../../kit/guard.py) and [`.github/scripts/install.py`](../../.github/scripts/install.py): the guard and the installer
- [`evals/scenarios/`](../../evals/scenarios/README.md): the scenarios for every rule
- [The Home Kit](../technical/The-Home-Kit.md) and [Evals](../technical/Evals.md): how each works
- [Rules For Current Models](../technical/research/Rules-For-Current-Models.md): the research this rests on
- [ADR-0020](ADR-0020-One-Constitution.md): one constitution; [ADR-0027](ADR-0027-Rules-That-Save-Tokens-Without-Losing-Quality.md): the token-saving Defaults, of which CODE-003 is folded here

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**A rule earns its place by changing what the models in use do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
