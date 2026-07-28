<!--
title: '📦 SKILL AUTHORING'
description: 'How to write a skill that works unchanged in every supported tool, what each part costs at runtime, and which rules are machine-enforced.'
tags: [skills, authoring, portability, standards]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📦 SKILL AUTHORING

<a name="top"></a>

**A skill fails silently in every direction, so every rule below is a gate.**

_Written once, loaded three ways, priced by the tier it sits in._

</div>

---

## 🎯 The Three Tiers

Every rule below defends one of these, and knowing which makes each rule obvious rather than arbitrary.

| Tier  | What                   | Loads                                            | Cost                                    |
| :---- | :--------------------- | :------------------------------------------------ | :-------------------------------------- |
| **A** | `name` + `description` | at startup, for **every** skill, invoked or not  | always paid, even by skills nobody uses |
| **B** | `SKILL.md` body        | on invocation                                    | **persists the whole session**, never re-read |
| **C** | bundled files          | only when the body sends the agent there         | zero until used                         |

Tier B is the one people get wrong. Claude Code's documentation is explicit that the rendered body enters the conversation as a single message and stays for the session, and that the file is not re-read on later turns. Every line is a **recurring** cost, not a one-time read.

The discipline that follows: **put as little as possible in B, and push detail to C.**

---

## 🗂️ The Layout

```bash
skills/<name>/
├── SKILL.md          # required. Navigation, not content. Under 500 lines
├── references/       # detail, loaded only when SKILL.md says to
├── assets/           # templates and resources
├── scripts/          # optional. Executable, and the one boundary crossing
└── evals/
    └── evals.json    # the evidence it beats its own baseline
```

**The directory name is the contract.** It is what a user types to invoke, and the frontmatter `name` must equal it. When they disagree the skill is discovered under one name and invoked under another.

Fold templates into `assets/` rather than a separate directory. The specification names `assets/` as the home for templates and resources, and fewer directories means fewer files to justify.

---

## 🏷️ Frontmatter

**Two required fields, and only two.**

| Field         | Rule                                                                                                      |
| :------------ | :-------------------------------------------------------------------------------------------------------- |
| `name`        | 1 to 64 characters, matching `^[a-z0-9]+(-[a-z0-9]+)*$`, and equal to the directory name                   |
| `description` | 1 to 1024 characters, saying what the skill does **and** when to use it                                   |

**Optional and portable:** `license`, `compatibility`, `metadata`.

**Banned:** `allowed-tools`. The specification marks it experimental and it grants tool access without a per-use prompt, on a machine that is not yours.

**Claude-only, permitted with a declaration:** `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`. Gemini CLI ignores every one of them.

> [!IMPORTANT]
> **A skill using any Claude-only key must set `compatibility`.** The harmless case is an optimisation that quietly does nothing. The dangerous case is a skill whose **correctness** depends on the key: one relying on `disable-model-invocation: true` to avoid auto-firing will auto-fire on Gemini.

`SKILL.md` frontmatter uses `---` fences, unlike every other document in this repository. That is correct, and the specification requires it.

---

## ✍️ The Description Is The Highest-Leverage Thing You Write

It is the only part loaded for every skill whether used or not, and it is what decides invocation. Four rules, each from observed runtime behaviour:

1. **Key use case first.** Claude Code truncates the combined `description` and `when_to_use` at 1,536 characters, and truncation eats the end.
2. **Use the words a user would actually type.** The first documented fix for a skill that never fires is that its description lacks the keywords people naturally say.
3. **Stay well under 1024.** The listing budget is roughly 1% of the context window, and on overflow Claude Code drops descriptions starting with your **least-invoked** skills. A verbose description on one skill silences another.
4. **Write it for a person too.** Gemini CLI shows it in a consent prompt asking the user to grant access to the whole skill directory. Keyword soup reads well to a matcher and badly to a human, and a consent prompt nobody reads is a control you have already lost.

Rules 2 and 4 pull against each other. Resolve them with plain, specific prose that happens to contain the natural words, never a keyword list.

---

## 📄 The Body

State **what to do**, not how or why. The diff and the reference files carry the rest.

- Under 500 lines, and ideally far under. The specification recommends the body stay below roughly 5,000 tokens.
- Write standing instructions, not one-time steps. The content is never re-read, so guidance meant to apply throughout a task must read that way.
- Name every reference file **with when to load it**. A file listed without a trigger gets read always or never.
- Compaction keeps only the first 5,000 tokens of each re-attached skill, sharing a 25,000-token budget. A long skill loses its tail.

---

## 🚫 Two Things That Break Portability

**Live shell.** `` !`command` `` and the fenced `!` form run a command in Claude Code and are literal text in Gemini CLI. Anthropic's own first-skill example uses the backtick form to inline `git diff` output, so this is a real feature rather than a typo. It is simply not portable, and a skill using it must declare `compatibility`.

**At-tokens.** A whitespace-bounded `@token` is a live import in all three supported tools. It pulls a file into context, or on a failed resolve leaves a comment where your directive used to be. There is no declaration that makes this acceptable: rewrite the line.

---

## 🧪 Evidence, Not Craft

> [!IMPORTANT]
> **Seeing a skill trigger tells you it was found, not that it did what you intended.** Two things fail separately and must be measured separately: whether it is invoked on the prompts it should be, and whether the output is right when it is.

`evals/evals.json` holds the cases. Anthropic's `skill-creator` plugin reads that path, runs each case in an isolated subagent, and writes a benchmark comparing pass rate, time and tokens **with the skill against without it**.

That comparison is the bar. A skill that does not beat its own baseline is a skill that should not ship, however well written, and the overhead is real: published research finds context files often fail to improve task success while adding over 20% inference cost.

Include **should-not-trigger** cases. A skill that fires on every adjacent request spends context on every session and crowds out the skills that should have fired instead.

---

## 🔎 What Is Machine-Enforced

[`.github/actions/check-skills`](../.github/actions/check-skills) gates on all of the following, because every one of them fails silently otherwise:

Missing `SKILL.md`; malformed or nested frontmatter; missing or empty `name` or `description`; `name` failing its pattern, exceeding 64 characters, or disagreeing with the directory; `description` over 1024; unknown, banned or undeclared vendor keys; a body over 500 lines; a reference that does not exist or escapes the directory; a file in the directory that `SKILL.md` never references; a live import token; an invisible character; undeclared live shell; a byte order mark; a missing or doubled trailing newline.

It warns on a missing eval suite, a description over 500 characters, a reference more than one level deep, and a bundled `scripts/` directory.

The unreferenced-file rule is a gate rather than a warning for a Gemini-specific reason: it adds the **folder structure** to context and grants the model access to the **whole directory**, so a stray file costs context and widens what the user is asked to approve.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

The reference implementation is [`develop`](../skills/.unpackaged/develop/SKILL.md), the meta skill for authoring skills, which passes every gate above. The measurements these rules rest on are in [Vendor Facts](Vendor-Facts.md).

---

<div align="center">

**Cheap to ignore, expensive to load, and proven before it ships.**

[↑ Back to Top](#top)

</div>
