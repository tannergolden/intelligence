<!--
title: '🔁 SELF IMPROVEMENT'
description: 'How a lesson learned in one repository reaches the others, and what stops the loop making things worse.'
tags: [self-improvement, feedback, lessons, governance]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🔁 SELF IMPROVEMENT

<a name="top"></a>

**A mistake made once anywhere should stop being possible everywhere.**

_Two channels, one test, and nothing recorded on a guess._

</div>

---

## 🎯 The Constraint That Shapes Everything

`AGENTS.md` is **overwritten in full on every sync**. So a lesson written into the law inside a consuming repository survives until the next scheduled run and then disappears, taking itself with it and leaving no trace that anything was lost.

That single fact rules out the obvious design. "Let the agent append what it learned to the instructions" deletes itself on a weekly cron, and the deletion is silent. Any loop that works has to answer *where does the lesson go* before it answers anything else.

---

## 🔀 Two Channels

| Lesson | Goes | Reaches |
| :--- | :--- | :--- |
| True of **this** repository | its own context, wherever that lives | this repository |
| True of **any** repository | upstream, into the published law | every repository, on its next sync |

The second channel is what makes this a loop rather than note-taking. A rule learned once, in one repository, stops the same mistake in all of them.

**The routing test is the one already written into the law:** would this still be true in a repository with a different language, toolchain, branch model and review policy? When it is genuinely borderline, it is local. A local rule can be promoted later by a repository that has lived with it; a rule pushed into the shared law wrongly arrives everywhere at once.

> [!IMPORTANT]
> **The published files are never a destination.** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and any router beside them are overwritten by the sync. This is the most likely way to get routing wrong, precisely because those files are usually what the lesson is *about*.

---

## 🧪 Nothing Is Recorded On A Guess

An agent's account of why something failed is frequently wrong, and the failure is specific: the account is plausible, confident, and built from the same reasoning that produced the mistake. Written down, it becomes a permanent instruction every future agent obeys.

So every lesson carries a grade, the same three [Vendor Facts](Vendor-Facts.md) uses:

| Grade | Earns it |
| :--- | :--- |
| **probed** | Something ran and the result is reproduced in the entry |
| **documented** | A primary source says so, and the entry names it and the date |
| **unverified** | Believed from a secondary source. Recorded as a lead, never as a rule |

**An unverified lesson is allowed to exist and is not allowed to be written as a rule.** It is recorded as a question with the check that would settle it, and promoted when someone runs that check.

This is not hypothetical caution. Three claims in `Vendor-Facts.md` were wrong when first written: one recalled rather than re-measured and off by a factor of five, one describing a file that had been read through a rendering that stripped the relevant part, and one taken from a confident search summary the vendor's own documentation contradicts. Under a loop without grading, all three would have become permanent rules.

---

## ✂️ Every Addition Names A Subtraction

The law is read in full, in every session, in every repository, forever. A loop with an append path and no retirement path makes it grow without bound, and a longer instruction file makes agents **worse** at finding the rule that applies.

So an addition names either the line it replaces or the argument for a permanent seat. Retire on sight anything now false, anything a gate started enforcing, and anything only ever true of a situation that no longer exists.

**A gate beats a rule** wherever one is possible: it fires every time, it cannot be skimmed past, and it costs no context. Where a proposed lesson could be a check instead, the check is the better proposal.

---

## 🤝 Drafted, Never Filed

A universal lesson produces a **proposal shown to the user**, not an issue opened automatically.

The reason is the blast radius rather than caution for its own sake. A change accepted upstream reaches every repository pinned to the moving major on its next sync, with no pull request and no review on the receiving side. That is a production change to every consumer at once, triggered by something that happened in one of them. A person decides that.

---

## 📦 How It Is Delivered

The loop is the [`improve`](../skills/.unpackaged/improve/SKILL.md) skill: installed rather than synced, inert until invoked, and executing nothing on clone. It decides whether there is a lesson at all (usually there is not), grades it, routes it, writes local ones into the repository's own context, and drafts universal ones for a human.

Installing it is the same as any skill, and [Installation](Installation.md) covers it.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

What may enter the law at all is [Scope & Boundaries](Scope-&-Boundaries.md), and it governs any proposal this loop produces.

---

<div align="center">

**Learned once, graded before it counts, and paid for in every session it survives.**

[↑ Back to Top](#top)

</div>
