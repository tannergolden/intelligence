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

**Every structural decision here traces to one row below, graded by how it was checked.**

_A dated measurement beats a confident sentence._

</div>

---

## 🎯 Why This File Exists

Four claims in this table have been wrong, and each was believed until something ran. One described a hazard in a file type where it does not occur. One came from a confident search summary the vendor's own documentation contradicts. One was a row this file **corrected in the wrong direction**, replacing a right number with a wrong one. And one was a probe that measured the wrong thing, because the model under test could reach for a file it should not have been able to open.

That last pair is why the grades below are not enough on their own. A probe is only worth its grade if it could have failed.

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
| Gemini CLI discovers only `GEMINI.md` by default                   | **documented** | Its docs: the default filename is `GEMINI.md`, and reading `AGENTS.md` needs `context.fileName` in settings. Re-verified 2026-07-28 |
| Copilot's coding agent and CLI read `AGENTS.md` natively           | **documented** | Announced August 2025, alongside `.github/copilot-instructions.md` and `.github/instructions/**`         |
| VS Code Copilot ignores `AGENTS.md` unless `chat.useAgentsMdFile`  | **documented** | Still experimental and still off by default. Re-verified 2026-07-28, because this is the row whose change removes the one manual step in installation |
| `AGENTS.md` is an Agentic AI Foundation project under the Linux Foundation | **documented** | Contributed by OpenAI at the AAIF's formation, beside MCP. Reported at 60,000+ adopting projects |
| A `CLAUDE.md` symlink to `AGENTS.md` is an alternative to the import | **documented** | Anthropic's memory docs give `ln -s AGENTS.md CLAUDE.md`. Rejected here: a symlink does not survive `core.symlinks=false`, and this repository delivers into trees it does not control |

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
| There is **no `.skill` package format**                           | **probed**     | Every `.skill` string in the binary is a property accessor. `skill package` and `unpackaged` return zero hits |
| A `.skill` file is a ZIP under another name | **probed** | The packager writes one with `zipfile` and reads it back with `zipfile`. The extension is a label on ZIP bytes |
| The claude.ai upload wants the `.zip` extension | **unverified** | Circulating advice rather than a primary source, and not reproducible from here: it is a web interface no probe in this repository can reach. Graded rather than promoted. Recorded 2026-07-28 |
| The ZIP is the only install path that needs packaging at all      | **documented** | The command-line tools read directories. Packaging exists for the web upload and for handing someone one file |

---

## ⚠️ Content Hazards

| Claim                                                     | Grade      | How                                                                                              |
| :-------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------ |
| A whitespace-bounded at-token is a live import            | **probed** | It is the mechanism the routers use, so it is live by demonstration                               |
| `` !`command` `` is **inert** in `CLAUDE.md`              | **probed** | A router carrying one returned the literal source text, not command output                        |
| `` !`command` `` is **live** in `SKILL.md`               | **documented** | Anthropic's own first-skill example uses it to inline `git diff` output before the model sees the file |
| Hook stdout passes through **whole up to 10,000 characters** | **probed** | Bisected on 2.1.220 with tools disabled: 9,999 and 10,000 arrived complete, 10,001 did not |
| Beyond that it is **replaced**, not trimmed                | **probed** | 10,001 and 15,024 both returned a `<persisted-output>` block: "Output too large (14.7KB)", a file path, and a 2 KB preview |

> [!IMPORTANT]
> **That pair of rows has been wrong twice, in both directions, and the second time was the worse one.** It was first recorded as 10,000 characters, which is correct. It was then "corrected" to about 2 KB, because the 2 KB preview *inside* the replacement block was read as the threshold itself. A confident correction that replaces a right answer with a wrong one is harder to catch than an original error, because it arrives wearing the clothes of a fix.
>
> The re-probe that settled it ran with the Read, Bash, Glob and Grep tools disabled. Without that, the model reads the persisted file the notice points at and reports the full payload as though it had arrived in context, which is how "15,024 characters passed through untruncated" was recorded elsewhere in this repository. **The probe has to be unable to cheat, or it measures the wrong thing and says so confidently.**

---

## 🔁 What Would Change The Design

Three of these rows are load-bearing enough that a change makes a file deletable or a rule unnecessary:

- **Gemini CLI adopting `AGENTS.md` by default** deletes `GEMINI.md`. There is an open upstream request for exactly this.
- **Claude Code adopting `AGENTS.md`** deletes `CLAUDE.md`, though its documentation frames the current behavior as a position rather than a gap.
- **VS Code Copilot enabling `chat.useAgentsMdFile` by default** removes the one manual step in installation.

Every one of those makes this repository smaller. The churn runs in the right direction.

> [!NOTE]
> **Both router files were re-checked on 2026-07-28 and both are still needed.** A widely repeated summary lists Gemini CLI among the tools that read `AGENTS.md`, which is true of the ecosystem and false of the default configuration: the filename still has to be named in `context.fileName`, and the upstream request to change that is still open. This is the second time that particular summary has been believed here, which is why the row above now carries a re-verification date rather than only an original one.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

Where these facts become rules is [Scope & Boundaries](Scope-&-Boundaries.md). If a row above changes, that is the document to re-read.

---

<div align="center">

**Graded, dated, and reproducible. Anything ungraded is a rumor.**

[↑ Back to Top](#top)

</div>
