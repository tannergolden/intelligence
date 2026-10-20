<!--
title: '📄 ADR-0030: RULES WRITTEN FOR CURRENT MODELS'
description: 'The universal rules are revised on evidence about the mainstream models of October 2026: fifteen sentences reworded, three Defaults retired and one moved, an Invariant for installing packages added, and the mechanisms the restraint rules depend on built into the home kit.'
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

| Attribute     | Specification                                                                                                                |
| :------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                                      |
| **Consulted** | Claude Code sessions: a research pass on rules for coding agents, a second on current models alone, the change and its audit |
| **Informed**  | Every repository and machine that carries the block                                                                          |

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

Fifteen sentences are reworded. SEC-001 adds using a credential the agent was not given. SEC-002 keeps text that claims authority in the information it is. SEC-003 lets the user's own request publish their context. SEC-004 is new: install only what the task needs, from the project's own registry, checking each package added is the one intended, and never pipe or pass a download to a shell. OPS-001 names remote branches and forbids merging any pull request, since an agent cannot tell its own from its user's. OPS-003 asks for the exact command with full paths, leaves what the agent created to it, and names shared databases, access and settings. OPS-004 adds TLS errors. OPS-005 names drafts, deploys, and messages or data sent outside, and lets an agent push the branch its harness assigned. POL-001 adds the pull request template and the owner's .github repository. CODE-002 leaves room for the change the user asked for, and its way out becomes "stop and report which and why". COM-002 adds what is unverified. CODE-001 absorbs CODE-003's narrowest-test-first order, runs the documented checks once, and no longer counts a check that failed to start, was cut short or ran nothing. WORK-001 asks for all of the task and only the task: a question gets an answer, not a change, and what the repository's rules require counts as asked. WORK-002 takes the reading the request and code best support, rather than the most conservative one. DOC-003 loses "lead with the point", which both Claude models did without it, and STD-001 loses "which differ from your defaults", a claim whose source could not be found.

Three Defaults leave and one moves. CODE-003 is folded into CODE-001. COM-004's lead-with-the-answer clause went into DOC-003 and then out of the block, since Claude Opus 5.5 and Sonnet 5.5 led with a short answer in 7 of 7 runs without it, and its clause against narrating reasoning goes, since current guidance says to remove it. WORK-005 is cut to keep the block under its cap after the rewordings: both models skipped the needless rerun in 7 of 7 runs without it, Claude Code's own prompt already asks for parallel calls, and CODE-001's "once" keeps its check on reruns. COM-005 moves from the Owner-only Defaults to the Defaults, since the owner reads an agent's replies in every repository.

The block drops its source line, which asked agents to open a file they rarely open, and measures 4,989 of its 5,000 characters, 24 rules. Every reason was rewritten on current-model evidence, with previous-generation figures labelled or dropped; STD-001's figure for doc reading, which no source held, gives way to SWE-CC's. Article VI gains an admission test for every rule, a release note naming each rule ID a release changes, and a note that a retired Invariant still holds wherever an older copy loads.

The mechanisms the restraint rules name are built into the home kit with this change. The guard denies piping a download into a shell, an install that overrides the registry on the command line, a read of a credential store in the home folder, a recursive delete of a Windows drive or home folder, and an em dash written into a file, commit or pull request in a repository the owner owns. On local machines the installer adds Claude Code ask-first permissions for pushes, pull requests, comments, releases and publishing, and a hook that restates the Invariants after Claude Code compacts a conversation. Codex rules, Antigravity Ask entries and a Cursor hook that fails closed stay on the To add lists.

Every new or reworded rule's scenarios ran on Claude Code with Claude Opus 5.5 and Claude Sonnet 5.5 at their defaults, seven times with the block and seven without, on the block as first revised. The block made the difference in six. SEC-001's key in a config file and CODE-002's impossible test went from none of seven without it to seven of seven with it, on both models. WORK-004's short output went from 2 and 0 of 7 to 7, POL-001's pull request template from 5 and 0 to 7, and OPS-003's untracked data from 6 and 0 to 7, Opus first. CODE-001's documented checks went from 0 to 7 on Sonnet, and Opus ran them either way. Everything else passed 7 of 7 either way, which cannot tell a rule Claude does not need from one it already follows; those rules stay on the admission test's other grounds, the models of other makers or the harm they guard against. Codex, Copilot CLI, Antigravity and Cursor were not installed where the evals ran, so their runs are still to make.

Some proposals were declined. Claude Code's `includeGitInstructions: false` would strip its own commit-only-when-asked and git safety text from every repository, including those where the owner's git rules do not apply, so the kit leaves it on. A fixed `attribution` value would lose the model name Claude Code's default trailer already carries, which is what GIT-013 asks for. Moving the source into the block's marker would break older installers and syncs, which read the marker strictly. DOC-002 stays in the block until a check on changed files runs in CI and its without-block eval passes. A rule against agreeing with a user's wrong claim waits for current-model numbers.

Option 1 keeps reasons that describe models nobody runs, and rules the harnesses now contradict. Option 3 leaves the owner's defaults to prompts that disagree with each other and have dropped restraint. Option 4 cannot work, because a repository cannot know which model reads it, and copies per model would drift.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                            |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | Rules that hold across makers and give every prohibition a way out; restraint backed by the guard and by ask-first permissions; reasons that cite the models in use             |
| **Negative (-)** | The block sits 11 characters under its cap, so the next rule must cut another; local Claude Code asks before every push, pull request and publish, even ones the user asked for |
| **Neutral (~)**  | The block's hash changes, so the next release reaches every repository as a pull request whose diff is the block alone                                                          |

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
- [ADR-0020](ADR-0020-One-Constitution.md): one constitution; [ADR-0027](ADR-0027-Rules-That-Save-Tokens-Without-Losing-Quality.md): the token-saving Defaults, of which CODE-003 is folded and WORK-005 cut here

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
