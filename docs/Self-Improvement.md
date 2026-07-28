<!--
title: '🔁 SELF IMPROVEMENT'
description: 'Why the feedback loop ships as an optional skill rather than as law, and what it works on.'
tags: [self-improvement, feedback, skills, governance]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🔁 SELF IMPROVEMENT

<a name="top"></a>

**A mistake made once anywhere should stop being possible everywhere.**

_Optional, portable, and owned by the skill that implements it._

</div>

---

## 🎯 What It Is

The loop is the [`improve`](../skills/.unpackaged/improve/SKILL.md) skill. It decides whether a session produced a lesson at all (usually not), grades the evidence, works out where the lesson belongs, and writes or drafts it.

**Its rules live in the skill and nowhere else.** This page owns only the question the skill should not spend context answering: why it is shaped this way. For how the loop actually behaves, read the skill.

---

## 🧩 Why A Skill, Not Law

Three reasons, and each one rules out the alternative:

**It is not universal.** The law is byte-identical in every repository, so it may only hold what is true of all of them. Plenty of repositories want no feedback loop at all, and a rule they must ignore is not a rule.

**It costs context.** A loop written into the law is read in every session of every repository forever, whether or not anyone uses it. As a skill it is loaded only when invoked, which is the difference between paying always and paying on use.

**It is a capability, and capabilities are skills.** That is the second question in [Scope & Boundaries](Scope-&-Boundaries.md), and the answer routes it here without further argument.

---

## 🌍 It Works Anywhere, Because It Never Guesses About Writing

The skill is **an optional download that assumes nothing about how it was installed.** It gets that portability from one flat rule rather than from detecting anything:

> **It writes only where a sync cannot reach, and drafts everywhere else.**

| Destination | What happens |
| :--- | :--- |
| The repository's own docs and notes | **Written.** Nothing overwrites these |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | **Never written.** Drafted and handed to the user |
| Whoever publishes the instructions | **Drafted** as a proposal a person files |

An earlier version tried to work out whether the instruction files were delivered or hand-written, and edited them when it decided they were owned locally. The detection was reasonable and the trade was not, because the two failures are not equally priced: guessing "hand-written" wrongly **destroys the lesson silently and unrecoverably**, while guessing "synced" wrongly files it a folder away. A heuristic whose failure mode is silent data loss is not worth the accuracy it buys.

So the skill guesses only where being wrong is cheap. Drafting an upstream proposal in a repository with no publisher wastes a paragraph; that is allowed. Deciding it may edit a file a sync owns is not.

---

## 🛡️ The Three Safeguards

All three are enforced by the skill. Two come from this repository being bitten by what they prevent, and one from published work on what goes wrong when a loop like this is built without it.

**Nothing is recorded on a guess.** Every lesson carries the probed, documented or unverified grade that [Vendor Facts](Vendor-Facts.md) uses. Four claims in that file have been wrong, one of them because a confident correction replaced a right answer with a wrong one. Under an ungraded loop, every one of them would have become a permanent instruction that every future agent obeyed.

An unverified entry is also **shaped** differently, not just labeled differently: the grade goes in the heading and the body describes rather than instructs. The template's own argument is that a reader skims headings and takes the rules from them, and a grade line four lines below the heading does not survive that skim.

**Every addition names a subtraction.** Instructions are read in full, in every session, forever, so an append-only loop makes agents worse at finding the rule that applies. Where a lesson could be a gate instead, the gate is the better answer: it fires every time and costs no context.

**Nothing untrusted is ever persisted.** A lesson whose origin is content the repository does not control, and which grants rather than restricts, is refused rather than graded down. Writing something down is what makes it permanent, so this step is the difference between a prompt injection that ruins an afternoon and one that becomes a rule nobody remembers agreeing to.

### 📊 What The Measurements Say

The second and third safeguards are not preferences. Each rests on published work, and they are the reason this loop refuses more than it records.

**These rows are graded like every other claim this repository makes**, using the same vocabulary as [Vendor Facts](Vendor-Facts.md). A document arguing that an ungraded lesson is worse than no lesson does not get to cite ungraded numbers, and an earlier version of this table did exactly that: three figures, no source, one of which could not be found again when somebody looked.

| Finding | Grade | Why it shapes the design |
| :--- | :--- | :--- |
| On EHRAgents, an add-all memory strategy scored **13.04%** task accuracy against a fixed-memory baseline of **16.89%**, while selective addition under strict criteria scored **38.86%** | **documented**: Xiong et al., [*How Memory Management Impacts LLM Agents*](https://arxiv.org/abs/2505.16067), arXiv:2505.16067 | Accumulating is not a milder form of curating. It scores **below not learning at all**, which is the whole argument for a loop whose normal answer is "there is no lesson here" |
| Instruction adherence degrades monotonically with turn count, and faster when constraints accumulate | **documented**: consistent across recent multi-turn benchmarks, one reporting a drop from 88% to 71% between the first and third turns | The loop runs at the end of long tasks, so it runs when recall is least reliable. Re-establish from the artifact, never from the session |
| Injection into agent memory succeeds against production systems at high rates | **unverified**: the shape is widely reported, the rate is not something this repository has reproduced | A loop is a persistence mechanism, so it is the exact component an injection needs in order to become permanent. The design does not depend on the rate: one success is a rule nobody remembers agreeing to |

An earlier version of this table gave the first row as "2,400 records at 13% against 248 at 39%". The accuracy figures survived checking and the record counts did not, so they are gone. The middle row gave "73% by turn five and 33% by turn sixteen", which could not be traced to any source and has been replaced by the finding that can be. **Neither correction changes a single decision in the skill**, which is the point worth keeping: a design that only stands up with a precise number it cannot cite was never standing on the number.

---

## 📮 Where A Proposal Lands

A loop with a drafting step and nowhere to send the draft is a loop that never closes. The universal half ends at a **law proposal** on this repository, and [`.github/ISSUE_TEMPLATE/law-proposal.yml`](../.github/ISSUE_TEMPLATE/law-proposal.yml) is the form it lands on. Its fields are the same four the skill drafts, so a proposal pastes in unchanged: the rule, its grade and evidence, why it is universal, and what it costs.

**A person files it, and a person judges it.** Acceptance is a production change to every repository pinned to the moving major, so nothing about that step is automated.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

Installing it is the same as any skill, and [Installation](Installation.md) covers that.

---

<div align="center">

**Shipped as a download, not as a rule nobody asked for.**

[↑ Back to Top](#top)

</div>
