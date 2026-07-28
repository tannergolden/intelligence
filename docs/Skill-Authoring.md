<!--
title: '📦 SKILL AUTHORING'
description: 'How to write a skill that works unchanged in every supported tool, what each part costs, and which rules are machine-enforced.'
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

**Optional and portable:** `license` (an SPDX identifier, or the name of a file the skill bundles), `compatibility` (1 to 500 characters), `metadata` (a mapping of string keys to string values, and the only field the specification defines as a mapping rather than a scalar).

**Banned:** `allowed-tools`. The specification marks it experimental and it grants tool access without a per-use prompt, on a machine that is not yours.

**Claude-only, permitted with a declaration:** `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`. Gemini CLI ignores every one of them.

> [!IMPORTANT]
> **A skill using any Claude-only key must set `compatibility`.** The harmless case is an optimization that quietly does nothing. The dangerous case is a skill whose **correctness** depends on the key: one relying on `disable-model-invocation: true` to avoid auto-firing will auto-fire on Gemini.

`SKILL.md` frontmatter uses `---` fences, unlike every other document in this repository. That is correct, and the specification requires it.

**What the checker parses.** Scalars, block scalars (`description: |` and `description: >`, which is how any description long enough to wrap gets written), and a mapping under `metadata`. Anything else nested is refused rather than guessed at, and a key set twice is refused outright: every YAML reader keeps the last one silently, so the value a reviewer read in the diff is not the value that loads.

---

## ✍️ The Description Decides Everything Else

It is the only part loaded for every skill whether used or not, and it alone decides whether the skill is ever invoked. **A perfect body behind a vague description runs never.** Write it first, before the body exists.

**Frame it as an instruction to the agent, not a label for the skill.** The difference is the whole rule:

| Weak                          | Strong                                                                                        |
| :---------------------------- | :---------------------------------------------------------------------------------------------- |
| `Processes CSV files`         | `Use this skill when the user needs to read, filter, or summarize tabular data, including .csv and .tsv exports` |
| `Helps with commit messages`  | `Use this skill when the user is writing a commit message, or asks why a commit was rejected`  |

The first column names a topic. The second names a **situation**, in the words someone would actually use to describe it.

Five rules, each from observed runtime behavior:

1. **Be pushier than feels natural.** Agents measurably under-trigger. A description that reads as appropriately modest to a human is one the agent skips.
2. **Name the symptom, not only the domain.** Someone with a broken skill says "it never activates", not "I need skill authoring help". List the phrasings they would really type.
3. **Say what it is not for.** The failure that costs most is over-triggering: a missed trigger costs one session, a false one costs every session.
4. **Key use case first.** Claude Code truncates the combined `description` and `when_to_use` at 1,536 characters, and truncation eats the end.
5. **Stay well under 1024.** The listing budget is roughly 1% of the context window, and on overflow Claude Code drops descriptions starting with your **least-invoked** skills. A verbose description on one skill silences another.

Gemini CLI shows this text in a consent prompt asking the user to grant access to the whole skill directory, so it has to read as prose to a person as well as matching for a model. Resolve that with plain specific sentences that happen to contain the natural words, never a keyword list.

**The test:** show the description alone to someone who has not seen the skill and ask what request would summon it. If they cannot say, the skill will not fire, whatever the body contains.

---

## 📄 The Body

State **what to do**, not how or why. The diff and the reference files carry the rest.

- Under 500 lines **and** under roughly 5,000 tokens. Those are two different caps and a body can pass one while failing the other, since 300 dense paragraphs cost more than 480 short steps.
- Write standing instructions, not one-time steps. The content is never re-read, so guidance meant to apply throughout a task must read that way.
- Name every reference file **with the condition that sends an agent to it**, not just its subject. A file listed by subject alone gets read always or never.
- Omit generic knowledge. Do not explain what a CSV is or how HTTP works. Every line spent on what the model already knows is paid again in every session.
- Compaction keeps only the first 5,000 tokens of each re-attached skill, sharing a 25,000-token budget. A long skill loses its tail.

---

## 🎚️ Degrees Of Freedom

The most useful question when writing any instruction is how much latitude to leave. Match it to how fragile the task is, not to how important it feels.

| Freedom    | Form                       | Use when                                                                  |
| :--------- | :------------------------- | :------------------------------------------------------------------------- |
| **High**   | prose and principles       | several approaches work and the model's judgement is better than a rule    |
| **Medium** | a numbered procedure       | sequence matters, but the steps tolerate variation                         |
| **Low**    | a bundled script to run    | the operation is fragile, repeated, or has one correct answer              |

Getting this wrong is the most common structural defect. Prose where a script belongs makes the agent reinvent fragile logic every run and get it subtly different each time. A script where prose belongs makes the skill brittle the moment the situation shifts an inch from what the author imagined.

---

## 🧩 Four Patterns That Work

**Gotchas in the body, not a reference.** An environment-specific fact or a call that reports success on failure has to be read **before** the situation arrives. Anything a reference is only consulted after something goes wrong.

**Output templates over descriptions of output.** Give the concrete shape in a fenced block. Agents match a structure far more reliably than a paragraph describing one.

**Checklists for anything with more than about five steps.** They survive compaction better than prose and give the agent something to check itself against.

**Validation loops.** Tell the agent to verify its own work before moving on. For batch operations the strongest form is plan, validate, then execute: produce an intermediate structured list, check it against a source of truth, and only then act.

---

## 🗑️ Anti-Patterns

| Anti-pattern                | Why it fails                                                                    |
| :-------------------------- | :-------------------------------------------------------------------------------- |
| Vague filler                | "Handle errors appropriately" carries nothing the model did not have, and costs tier B in every session |
| Overly comprehensive        | A skill documenting everything makes the agent worse at finding the part that applies |
| Options without a default   | Three approaches as equals makes the agent choose arbitrarily, differently each run |
| Time-relative language      | "The new API" and "recently changed" are wrong on a schedule nobody is watching  |
| Machine-specific paths      | A path true only on the author's machine is an instruction that fails everywhere else |
| One skill for everything    | Split by triggering context, since the description is what routes the request     |

The first and the fifth are machine-checked, because both look fine in review and neither produces an error at runtime.

---

## ⚙️ Bundled Scripts

Bundle one when the agent would otherwise rebuild the same logic every run, or when the operation is deterministic enough that generated code is a liability. The signal usually comes from the transcripts: if several eval cases all show the agent writing the same helper, that helper should ship.

A bundled script is invoked by an agent, never by a person at a prompt, and that changes its interface:

- **No interactive prompts, ever.** A script waiting on stdin hangs the session with no indication why.
- **`--help` that explains itself**, since the agent may read it rather than the source.
- **Errors that say what to do next**, not just what went wrong.
- **Data on stdout, diagnostics on stderr**, so the output can be piped without being contaminated by progress messages.
- **Destructive operations guarded** behind an explicit flag.
- **Nothing written into the skill directory.** It is read-only in most installations, and on a packaged skill it may not exist on disk at all.

The cost side is real: `scripts/` is executable content in a tree whose other files are inert, so the checker warns on its presence. Deliberate is fine, accidental is not.

---

## 🌍 Two Things That Break Portability

**Live shell.** `` !`command` `` and the fenced `!` form run a command in Claude Code and are literal text in Gemini CLI. Anthropic's own first-skill example uses the backtick form to inline `git diff` output, so this is a real feature rather than a typo. It is simply not portable, and a skill using it must declare `compatibility`.

**At-tokens.** A whitespace-bounded `@token` is a live import in all three supported tools. It pulls a file into context, or on a failed resolve leaves a comment where your directive used to be. There is no declaration that makes this acceptable: rewrite the line.

To write one literally, put it in backticks. Claude Code documents that import parsing skips code spans and fenced code blocks, so a skill teaching the syntax can show it, and the checker follows the same boundary. Everywhere else on the line it still fails.

---

## 🧪 Evidence, Not Craft

> [!IMPORTANT]
> **Seeing a skill trigger tells you it was found, not that it did what you intended.** Two things fail separately and must be measured separately: whether it is invoked on the prompts it should be, and whether the output is right when it is.

`evals/evals.json` holds the cases. Anthropic's `skill-creator` plugin reads that path, runs each case in an isolated subagent, and writes a benchmark comparing pass rate, time and tokens **with the skill against without it**.

```json
{
  "skill_name": "the directory name",
  "evals": [
    {
      "id": 1,
      "prompt": "a realistic request, in the words a user would type",
      "expected_output": "what a correct response looks like",
      "files": ["optional input files the case needs"],
      "assertions": ["a checkable claim about the output"]
    }
  ]
}
```

Three things decide whether the suite is worth running:

1. **Start with two or three cases**, not twenty. The first run usually shows that the description, not the body, is what needs work, and twenty speculative prompts written beforehand are twenty prompts written against the wrong problem.
2. **Run each in a fresh session.** Context left over from writing the skill hides gaps in what the skill actually says.
3. **Cover the adjacent request you are most afraid of.** Every skill has one neighboring task it will wrongly claim, and that should-not-trigger case is worth writing before any of the happy paths.

That baseline comparison is the bar. A skill that does not beat it should not ship, however well written, and the overhead is real: published research finds context files often fail to improve task success while adding over 20% inference cost.

---

## 🔎 What Is Machine-Enforced

[`actions/check-skills`](../actions/check-skills) gates on all of the following, because every one of them fails silently otherwise:

Missing `SKILL.md`; frontmatter that is malformed, nested outside `metadata`, or sets one key twice; missing or empty `name` or `description`; `name` failing its pattern, exceeding 64 characters, or disagreeing with the directory; `description` over 1024; `compatibility` over 500; `metadata` written as a scalar; unknown, banned or undeclared vendor keys; a body over 500 lines; a reference that does not exist or escapes the directory; a file in the directory that `SKILL.md` never references; a live import token; an invisible character; undeclared live shell; a byte order mark; a missing or doubled trailing newline; and an `evals.json` that is unreadable, misattributed, empty, missing a prompt or assertions, or reusing a case id.

It warns on a description that never says **when** to use the skill, a description over 500 characters, a body over roughly 5,000 tokens, vague filler, a machine-specific path, a missing eval suite, a reference more than one level deep, and a bundled `scripts/` directory.

Two of those deserve their reasoning stated. The unreferenced-file rule is a gate rather than a warning for a Gemini-specific reason: it adds the **folder structure** to context and grants the model access to the **whole directory**, so a stray file costs context and widens what the user is asked to approve. And the eval file is checked as strictly as the skill because a malformed one looks like evidence right up until somebody tries to run it, which is usually the moment the skill is being changed and the evidence is most needed.

The content rules run over **every** bundled Markdown file, not only `SKILL.md`, since a reference enters context the moment the body sends an agent to it. Filler and anti-patterns quoted inside backticks or quotation marks are exempt, so a skill that teaches an anti-pattern can still name it, and import tokens follow the same boundary the vendors do. A file the `license` field names counts as referenced: the frontmatter is what points at it, so the body never will.

Run the checker locally with `make lint`, and prove the checker itself still rejects known-bad input with `--self-test`.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

The reference implementation is [`develop`](../skills/.unpackaged/develop/SKILL.md), the meta skill for authoring skills, which passes every gate above. The measurements these rules rest on are in [Vendor Facts](Vendor-Facts.md).

---

<div align="center">

**Cheap to ignore, expensive to load, and proven before it ships.**

[↑ Back to Top](#top)

</div>
