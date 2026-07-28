<!--
title: '🤖 VENDOR FACTS'
description: 'What each supported tool actually does with an instruction file and a skill, how each claim was checked, and when.'
tags: [vendors, verification, evidence, compatibility]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 VENDOR FACTS

<a name="top"></a>

**Nearly every structural decision in this repository traces to one row below, so the rows carry how they were checked rather than only what they say.**

_A dated measurement beats a confident sentence._

</div>

---

## 🎯 Why This File Exists

Three claims in this table were wrong when first written, and each was believed until something ran. One was off by a factor of five. One described a hazard in a file type where it does not occur. One came from a confident search summary that the vendor's own documentation contradicts.

So each row says **how it was established**, and the grades mean exactly this:

| Grade          | Means                                                              |
| :------------- | :------------------------------------------------------------------ |
| **probed**     | Executed against the installed tool, and the result is reproduced below |
| **documented** | The vendor's own documentation says so. Not executed                |
| **unverified** | Believed, from a secondary source. Treat as a lead, not a fact      |

Everything below was established on 2026-07-28 against **Claude Code 2.1.220**. No Gemini CLI or Copilot binary was available, so every row for those two is documentation at best.

---

## 📄 Instruction Files

| Claim                                                              | Grade          | How                                                                                                     |
| :----------------------------------------------------------------- | :------------- | :------------------------------------------------------------------------------------------------------ |
| Claude Code does **not** discover `AGENTS.md`                      | **probed**     | A directory holding only `AGENTS.md` returned `UNKNOWN`; the same directory with `CLAUDE.md` returned the codeword |
| Claude Code reads `CLAUDE.md`                                      | **probed**     | Control case above                                                                                      |
| An import line in a router resolves                                | **probed**     | `CLAUDE.md` containing only the import returned the codeword held in `AGENTS.md`                        |
| A large law loads whole, and its middle is retrievable             | **probed**     | A 113 KB imported file returned markers at byte 36, 56,359 and 112,895                                  |
| Gemini CLI discovers only `GEMINI.md` by default                   | **documented** | Its docs: the default filename is `GEMINI.md`, and reading `AGENTS.md` needs `context.fileName` in settings |
| Copilot's coding agent and CLI read `AGENTS.md` natively           | **documented** | Announced August 2025, alongside `.github/copilot-instructions.md` and `.github/instructions/**`         |
| VS Code Copilot ignores `AGENTS.md` unless `chat.useAgentsMdFile`  | **documented** | Experimental, off by default. Several independent sources agree                                         |

---

## 📦 Skills

| Claim                                                             | Grade          | How                                                                                          |
| :---------------------------------------------------------------- | :------------- | :-------------------------------------------------------------------------------------------- |
| Claude Code loads `.claude/skills/` only                          | **probed**     | A skill there appeared in the listing; an identical one in `.agents/skills/` did not          |
| Gemini CLI reads `.gemini/skills/` or `.agents/skills/`           | **documented** | The second is an official alias, named as compatible with the Agent Skills standard           |
| `name` and `description` are the only required fields             | **documented** | The specification. `name` is 1 to 64 characters and must match the parent directory           |
| `description` is capped at 1024 characters                        | **documented** | The specification                                                                             |
| A skill body persists for the whole session and is never re-read  | **documented** | Claude Code's docs. Compaction keeps the first 5,000 tokens each, sharing a 25,000-token budget |
| Gemini CLI prompts for consent, naming the directory it will access | **documented** | Its docs. It also adds the folder structure to context                                        |
| There is **no `.skill` package format**                           | **probed**     | Every `.skill` string in the binary is a property accessor. `skill package` and `unpackaged` return zero hits. Uploading to claude.ai uses a `.zip` |

---

## ⚠️ Content Hazards

| Claim                                                     | Grade      | How                                                                                              |
| :-------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------ |
| A whitespace-bounded at-token is a live import            | **probed** | It is the mechanism the routers use, so it is live by demonstration                               |
| `` !`command` `` is **inert** in `CLAUDE.md`              | **probed** | A router carrying one returned the literal source text, not command output                        |
| `` !`command` `` is **live** in `SKILL.md`               | **documented** | Anthropic's own first-skill example uses it to inline `git diff` output before the model sees the file |
| A SessionStart hook's output is truncated at about 2 KB   | **probed** | A 2,034-byte payload survived whole; a 15,480-byte one was cut between markers at 1,806 and 2,064 |

> [!IMPORTANT]
> **That last row was first recorded as 10,000 characters, and was wrong by a factor of five in the direction that made a rejected design look better than it was.** It is the reason this file grades its rows.

---

## 🔁 What Would Change The Design

Three of these rows are load-bearing enough that a change makes a file deletable or a rule unnecessary:

- **Gemini CLI adopting `AGENTS.md` by default** deletes `GEMINI.md`. There is an open upstream request for exactly this.
- **Claude Code adopting `AGENTS.md`** deletes `CLAUDE.md`, though its documentation frames the current behaviour as a position rather than a gap.
- **VS Code Copilot enabling `chat.useAgentsMdFile` by default** removes the one manual step in installation.

Every one of those makes this repository smaller. The churn runs in the right direction.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

Where these facts become rules is [Scope & Boundaries](Scope-&-Boundaries.md). If a row above changes, that is the document to re-read.

---

<div align="center">

**Graded, dated, and reproducible. Anything ungraded is a rumour.**

[↑ Back to Top](#top)

</div>
