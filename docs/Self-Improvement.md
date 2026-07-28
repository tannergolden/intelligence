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

## 🌍 It Works Anywhere, Including Repositories That Never Heard Of This Publisher

The skill is **an optional download that assumes nothing about how it was installed.** It settles one question before it routes anything: does this repository own its instruction files, or receive them?

| Arrangement | Destinations |
| :--- | :--- |
| The repository **owns** its instruction files | One. The files are a legitimate place for a lesson |
| The files are **delivered** by a sync | Two. Local context, and a proposal upstream |

That distinction is load-bearing rather than decorative. `AGENTS.md` is a widely adopted open standard that tens of thousands of projects write by hand, so **most repositories own theirs**. In those, writing a lesson into the instruction file is exactly right. In a repository that syncs from a publisher, the same edit is destroyed by the next scheduled run with no error and no trace.

An earlier draft of the skill asserted the second case unconditionally. It would have refused to record a lesson in the one file that was the correct destination, in the majority of repositories it might ever be installed into.

---

## 🛡️ The Three Safeguards

All three are enforced by the skill. Two come from this repository being bitten by what they prevent, and the third from published measurements of what goes wrong when a loop like this is built without it.

**Nothing is recorded on a guess.** Every lesson carries the probed, documented or unverified grade that [Vendor Facts](Vendor-Facts.md) uses. Three claims in that file were wrong when first written; under an ungraded loop, all three would have become permanent instructions that every future agent obeyed.

**Every addition names a subtraction.** Instructions are read in full, in every session, forever, so an append-only loop makes agents worse at finding the rule that applies. Where a lesson could be a gate instead, the gate is the better answer: it fires every time and costs no context.

**Nothing untrusted is ever persisted.** A lesson whose origin is content the repository does not control, and which grants rather than restricts, is refused rather than graded down. Writing something down is what makes it permanent, so this step is the difference between a prompt injection that ruins an afternoon and one that becomes a rule nobody remembers agreeing to.

### 📊 What The Measurements Say

The second and third safeguards are not preferences. Both have numbers behind them, and they are the reason this loop refuses more than it records.

| Finding | Why it shapes the design |
| :--- | :--- |
| Agents on an add-all memory strategy reached 2,400 stored records at **13%** task accuracy; the same agents with selective memory held 248 records at **39%** | Accumulating is not a milder version of curating. It is worse than doing nothing, by a wide margin |
| Injection into agent memory succeeds against production systems at very high rates | A loop is a persistence mechanism, so it is the exact component an injection needs to become permanent |
| Constraint compliance measured at 73% by turn five and 33% by turn sixteen | The loop runs at the end of long tasks, so it runs when recall is least reliable. Re-establish from the artifact, never from the session |

The first row is the whole argument for a loop that treats "there is no lesson here" as the normal answer.

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
