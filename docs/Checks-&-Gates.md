<!--
title: '🚦 CHECKS & GATES'
description: 'Every check this repository runs on itself, what each one catches, and why the negative tests exist.'
tags: [checks, gates, verification, continuous-integration]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🚦 CHECKS & GATES

<a name="top"></a>

**Nothing downstream reviews these bytes, so everything is checked before they leave.**

_The last gate is the only gate._

</div>

---

## 🎯 Why This Repository Checks Itself Harder Than Most

A normal repository has a safety net after the commit: a pull request, a reviewer, and continuous integration in whatever consumes it. **This one has none of that.** Work lands here by direct push, the sync pulls files into a consuming repository with no pull request on their side, and a moved tag delivers to every consumer at once.

So the checks here are not a convenience. They are the only reading these bytes get before they become the instruction file an agent obeys in somebody else's repository.

---

## ⚙️ The Four Commands

Everything runs through `make`, and CI passes **no commands at all**: each stage resolves to the target of the same name. That is deliberate, and one of the four is the reason the file exists.

| Command          | Checks                                                       |
| :--------------- | :------------------------------------------------------------- |
| `make lint`      | Every skill, against the Agent Skills specification           |
| `make lint-docs` | Every document, against the published styling standard        |
| `make test`      | That both checkers still **reject** known-bad input           |
| `make build`     | That every skill still packages into an installable archive   |

> [!IMPORTANT]
> **`lint-docs` is the one stage with no input override in the shared workflow.** It resolves from a Makefile target or it does not run. Before there was a Makefile here, the documentation step reported "skipped" on every green run, so the rule `AGENTS.md` calls the one broken most often was checked by nothing, and the check was green the whole time. That failure mode is the argument for this whole document: **a gate that is not there looks exactly like a gate that passed.**

---

## 🧪 The Two Checkers

Both are standard library only. This matters more than it looks: [`actions/check-skills`](../actions/check-skills) runs in **other people's** continuous integration, where a dependency resolution would be a network call, a supply chain and a failure mode all at once.

### 📦 Skills

[`scripts/check-skills.py`](../scripts/check-skills.py) exists because every way a skill can be wrong is silent. A missing `SKILL.md` is not an error, it is a directory nothing discovers. A `name` that disagrees with its directory is found under one name and invoked under another. A body over the size guidance is not rejected, it just costs the whole session.

The full rule list, and which are errors rather than warnings, is in [Skill Authoring](Skill-Authoring.md).

### 📝 Documents

[`scripts/check-docs.py`](../scripts/check-docs.py) audits every document against the styling standard published in `standards`, followed **by link** rather than copied. It encodes only the subset a machine can decide, and it says so: where the specification calls a rule aesthetic, the rule is a warning here.

| Checks                                                                | Level     |
| :-------------------------------------------------------------------- | :-------- |
| Frontmatter in comment form, never `---` fences                       | error     |
| Exactly four kebab-case tags, and the other required keys             | error     |
| The `MD041` suppression, header block, anchor, description, tagline   | error     |
| Footer closing phrase and back-to-top link                            | error     |
| Em dashes, en dashes, curly quotes, mojibake                          | error     |
| Fence languages, shell prompt characters, image alt text              | error     |
| Relative links that resolve, and `_` as a space anywhere in the tree  | error     |
| Tagline and closing phrase uniqueness, reported against every owner   | error     |
| Fully-capped headings, `&` over `AND`, masthead length, long fences   | warning   |

`skills/` is excluded on purpose: a `SKILL.md` requires the `---` frontmatter this specification forbids. Both are correct in their own domain.

### 📏 The Delivered Budget

One check in that file is **not** part of the styling standard, and is kept there because it is the only checker already reading those bytes.

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` are delivered into other repositories and read by an agent in **every session there**, invoked or not. Nothing else in this tree costs that: a `SKILL.md` costs one session, a document costs whoever opens it, and these cost everyone, always. The checker had capped a `SKILL.md` at 500 lines for being expensive while leaving the far more expensive file unbounded, which was the wrong way round.

| File | Budget | Why that ceiling |
| :--- | ---: | :--- |
| `AGENTS.md` | 14,000 bytes | The law. Every rule is paid in every session, everywhere |
| `CLAUDE.md` | 3,000 bytes | An envelope. Growth here means law is leaking into a carrier |
| `GEMINI.md` | 3,000 bytes | The same |

**The numbers are a decision, not a discovery,** and a warning fires at 80% so the conversation happens before the ceiling rather than at it. Raising one has to be a commit somebody reviews, which is what turns "every addition names a subtraction" from an aspiration into a gate. It is also the hard stop behind the [self-improvement loop](Self-Improvement.md): a proposal that would breach the budget is a proposal to add one rule and retire another.

### 🪝 The Hook Gates

The skill router in `.claude/` and `.gemini/` is the only content here that runs on somebody else's machine without being asked, and the only thing charged **per turn** rather than per session. Three checks bound it, all in the same file:

| Check | Catches |
| :--- | :--- |
| Valid POSIX shell (`sh -n`) | A broken hook does not stop a session, it silently contributes nothing. It looks installed and is not |
| Output under 256 bytes, against a three-skill fixture | A paragraph of advice added to a script that fires every prompt, billed forever |
| Output is not empty when skills exist | A router that says nothing is indistinguishable from a working one until someone measures it |

The budget is measured by **running** the hook against a fixture rather than by reading it, because what costs context is what the script prints, not what it contains. Both failure modes were confirmed by breaking the script deliberately and watching the gate catch it.

---

## 🚨 Why Both Checkers Test Themselves

`make test` runs neither checker against this repository. It builds **deliberately broken** input in a temporary directory and asserts that every rule still fires **by name**.

A bare non-zero exit would be too weak a claim: any crash satisfies it, including one meaning the rules never ran. So each rule is asserted by the phrase it reports, warnings included, because the rules catching the quietest defects are the advisory ones.

The hostile input lives **inside** each checker rather than in a fixtures directory, so a rule and the thing proving it works cannot be deleted separately or drift apart.

> [!NOTE]
> **The documentation checker also asserts that its compliant fixture still passes.** A gate that rejects correct input trains everyone to ignore it, which costs more than the gate was ever worth.

Both checkers build their own banned characters from codepoints rather than typing them, so neither file contains what it rejects. Both shipped once with the literal characters in them and failed the repository on their first run.

---

## 🌿 Where Each Check Runs

| Where                                              | Runs                                                       |
| :------------------------------------------------- | :----------------------------------------------------------- |
| [`ci.yml`](../.github/workflows/ci.yml)            | All four `make` targets, plus shared spelling and link checks |
| [`skills.yml`](../.github/workflows/skills.yml)    | The skill gate, and the negative test beside it              |
| [`release.yml`](../.github/workflows/release.yml)  | Both checkers, both negative tests, and all three delivered files present |

`ci.yml` is a stub calling the shared reusable workflow in `standards` rather than a private copy, so spelling, link checking and documentation linting stay in one place for the whole fleet.

**`skills.yml` reports, it does not gate a merge**, and that is not an oversight: work lands here by direct push, so nothing merges and a required status check would have nothing to sit in front of. What it buys is a red mark while the person who wrote it is still looking at it.

**`release.yml` is the real gate.** It is the last moment anything reads these bytes before a moved tag carries them to every consumer, so it refuses to tag when a skill fails, a document fails, either checker has stopped rejecting known-bad input, or any of the three delivered files is missing.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

What the release gate protects, and how a bad one is recalled, is in [Releases & Versioning](Releases-&-Versioning.md).

---

<div align="center">

**Checked before it ships, because nothing checks it after.**

[↑ Back to Top](#top)

</div>
