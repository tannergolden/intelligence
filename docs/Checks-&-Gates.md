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
| `make test`      | That both checkers, and the packager, still **reject** known-bad input |
| `make build`     | That every skill still packages into an installable archive   |

> [!IMPORTANT]
> **`lint-docs` is the one stage with no input override in the shared workflow.** It resolves from a Makefile target or it does not run. Before there was a Makefile here, the documentation step reported "skipped" on every green run, so the rule `AGENTS.md` calls the one broken most often was checked by nothing, and the check was green the whole time. That failure mode is the argument for this whole document: **a gate that is not there looks exactly like a gate that passed.**

---

## 🧪 The Two Checkers, And The Packager

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
| Em dashes, en dashes, curly quotes, mojibake, invisible characters    | error     |
| British spellings, from a curated list of pairs                       | error     |
| Fence languages, shell prompt characters, image alt text              | error     |
| Relative links that resolve, and `_` as a space anywhere in the tree  | error     |
| Tagline and closing phrase uniqueness, reported against every owner   | error     |
| Fully-capped headings, `&` over `AND`, masthead length, long fences   | warning   |

`skills/` is excluded from the **document** rules on purpose: a `SKILL.md` requires the `---` frontmatter this specification forbids. Both are correct in their own domain.

**Two boundaries decide which rules see what, and they are not the same boundary.** Rules about rendered meaning skip code spans and fenced blocks, both kinds, because a document demonstrating Markdown is not a document making a claim: a fenced `# TITLE` is not a second heading, a `![](x.png)` shown as an example of bad alt text is not bad alt text, and a fenced link resolves to nothing on purpose. Rules about bytes skip nothing. A banned dash, a mojibake sequence and an invisible character are hazards wherever they sit, and those run over **every** file in the tree rather than the documents: a hook script, a workflow, a Makefile, a Python comment. The law says the ban covers everything you write, and until that gate existed it covered Markdown.

Link targets are read as URLs rather than paths, so `Scope-%26-Boundaries.md` and `Scope-&amp;-Boundaries.md` both resolve to the file whose name contains `&`.

Exempt from the tree scan: submodules, `dist/`, anything that is not valid UTF-8, and the verbatim third-party text the law itself exempts, which is license files and lockfiles.

**Spelling is a pairs list, not a dictionary.** Both spellings are correct English, so the shared workflow's spell check sees nothing wrong; what is wrong is the inconsistency with the sibling publisher, and only a list can judge that. The list omits every word with an American reading, `analyses` and `towards` among them, because a rule that fires on correct text is a rule somebody switches off. It runs in **both** checkers, since `skills/` is outside the document scan and nothing else ever reads a skill's prose for this.

### 🗜️ The Packager

[`skills/.unpackaged/develop/scripts/package.py`](../skills/.unpackaged/develop/scripts/package.py) builds the `.skill` archives attached to each release, and it is bundled inside the `develop` skill rather than sitting in `scripts/` because a skill author in another repository needs it and this repository's `scripts/` does not travel.

`make test` runs its self-test alongside the two checkers, because it is the one piece of machinery whose output is a file somebody downloads rather than a message somebody reads. Seven invariants, each of which produced a broken or unverifiable archive when it did not hold:

| Invariant | Why |
| :--- | :--- |
| The skill **folder** is the archive root, never `SKILL.md` | Unzipping the other shape scatters a skill across the current directory |
| `evals/` is excluded by default | Read by tooling, never by an agent, so it is weight in every download |
| Packing unchanged source twice is byte-identical | A build whose output changes without its input changing cannot be verified by anyone |
| Every entry records a **fixed** creating system | `zipfile` takes that field from the host, so the same source packed on Windows differed from the same source packed anywhere else |
| `--include-evals` ships them | The exclusion has to be an option rather than a rule, or the evidence is unshippable |
| A name and directory mismatch is refused | The same defect the skill checker fails on, caught before it is sealed in an archive |
| A directory with no `SKILL.md` is refused | It is not a skill, and an archive of it is a download that installs nothing |

The fourth is the one the third could not see. Two runs on the same machine agree whatever the host-derived fields say, so a repeat-build check passes on every platform while the archives still differ across them. Only reading the field answers the question, and determinism that holds on the platform you happened to test on is a property nobody can check from the other side.

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

## 🌐 Two Gates `make` Cannot Run

`ci.yml` calls the shared reusable workflow, which runs **spelling** and **link checking** in addition to the four `make` targets. Neither has a local equivalent, and that asymmetry is worth knowing before it costs a red build: a clean `make lint-docs` is not the same claim as a clean CI run.

| Gate | Tool | Configuration |
| :--- | :--- | :--- |
| Spelling | `typos` | The shared `_typos.toml` in `standards`, an accept-list of terms its dictionary does not know |
| Links | `lychee` | The shared `lychee.toml`, which accepts 403 and 429 so a host that blocks robots is not read as a broken link |

**Both configurations are upstream on purpose**, so an accepted term or an excluded URL is decided once for every repository rather than per repository. The cost is that a word this repository is entitled to use can still fail here, and the fix is upstream rather than a local override: a local `_typos.toml` replaces the shared one outright, which forks a standard followed by link.

That happened, and the cheaper answer was available. A citation naming a benchmark whose acronym `typos` reads as a transposition failed the build twice; the sentence was rewritten to name the benchmark by what it is, and the link already carried the identity. **Reword before overriding.** Add the term upstream only when it is a word this fleet will keep using.

To run either gate before pushing, fetch the same pinned tool version and the shared configuration and run it against the tree. That is one command more than `make`, and it is the difference between finding this on your machine and finding it on the default branch.

---

## 🌿 Where Each Check Runs

| Where                                              | Runs                                                       |
| :------------------------------------------------- | :----------------------------------------------------------- |
| [`ci.yml`](../.github/workflows/ci.yml)            | All four `make` targets, plus shared spelling and link checks |
| [`skills.yml`](../.github/workflows/skills.yml)    | The skill gate, and the negative test beside it              |
| [`lint-workflows.yml`](../.github/workflows/lint-workflows.yml) | actionlint and zizmor, on any change under `.github/workflows/` or `actions/` |
| [`release.yml`](../.github/workflows/release.yml)  | Both checkers, both negative tests, the packager's invariants, and every file the sync stub copies |

`ci.yml` is a stub calling the shared reusable workflow in `standards` rather than a private copy, so spelling, link checking and documentation linting stay in one place for the whole fleet.

**`lint-workflows.yml` is the gate for rules 4 and 5 of this repository's own law.** Until it existed, nothing here checked that third-party actions were pinned to a full SHA or that jobs held the narrowest permissions they could, so the repository published a law about continuous integration and exempted its own from it. actionlint validates Actions semantics and runs shellcheck over every `run:` block; zizmor audits for template injection, credential persistence, dangerous triggers and cache poisoning. Both are consumed by link from the sibling publisher rather than installed here. It caught its own first defect on its first run, an `ls` whose output was being parsed.

**`skills.yml` reports, it does not gate a merge**, and that is not an oversight: work lands here by direct push, so nothing merges and a required status check would have nothing to sit in front of. What it buys is a red mark while the person who wrote it is still looking at it.

**`release.yml` is the real gate.** It is the last moment anything reads these bytes before a moved tag carries them to every consumer, so it refuses to tag when a skill fails, a document fails, either checker has stopped rejecting known-bad input, the packager has stopped holding its invariants, or any file the sync stub copies is missing. That last list is all seven, the two hook scripts and two settings files included, not only the three documents: one missing at the tag is a `cp` that fails in every consuming repository at once, on a schedule, with nobody watching.

Four things it also refuses, each of which is about the tag rather than the bytes:

| Refusal | Because |
| :--- | :--- |
| A version tag that already exists | A published `vX.Y.Z` is immutable. The checkout fetches tags so the question can actually be answered locally rather than by the remote after every gate has reported success |
| A commit not reachable from the default branch | `workflow_dispatch` offers every ref, so nothing else stops a release being cut from unmerged work. An ancestor test rather than an equality test, so recutting from a known-good older commit still works |
| An empty `dist/` | An unmatched glob is itself, so the release would attach a path that does not exist |
| Publishing the release after moving the major | The release carries the skill archives. A failed upload used to leave the moving tag pointing at a version whose downloads do not exist, with the run reporting success. The pointer every consumer resolves is now the last thing to change |

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

What the release gate protects, and how a bad one is recalled, is in [Releases & Versioning](Releases-&-Versioning.md).

---

<div align="center">

**Checked before it ships, because nothing checks it after.**

[↑ Back to Top](#top)

</div>
