<!--
title: '📄 ADR-0005: HOME COPIES, NOT LINKS'
description: 'The home kit writes byte-identical copies of the rules into each app''s own home location, checked against the release, instead of linking every app to one shared file.'
tags: [adr, dotfiles, home-kit, instructions]
category: docs
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0005: HOME COPIES, NOT LINKS

<a name="top"></a>

**Each app gets its own byte-identical copy, in the place and shape it reads, checked against the release.**

_Copied, checked, and put back on request._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                      |
| :------------ | :--------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner            |
| **Consulted** | Claude Code sessions: research, four independent reviews of the plan, and drafting |
| **Informed**  | Every agent and collaborator working in a repository that carries the block        |

---

## 🎯 Context & Problem Statement

Each app reads its user-level instructions from a different place. The first plan linked every app's file to one real copy in `~/.agents/AGENTS.md`. Links fail in too many places:

- Claude Code's desktop sessions skip linked user rule files.
- Grok Build's strict sandbox cannot follow a link into `~/.agents` and drops the file silently, and a linked hook file or `config.toml` stops it from starting.
- Copilot CLI's handling of links is unverified, since it is closed source.
- A link takes over each app's personal file, so the owner's own notes in `~/.codex/AGENTS.md` would vanish.

None of the six apps reads `~/.agents/AGENTS.md` itself, and the phase 0 probe confirmed that for Claude Code.

---

## 🚦 Decision Drivers

- **Identical text in every app.**
- **Never destroy the owner's own notes.**
- **Detect drift** against something an agent cannot rewrite.
- **Reversible**: uninstalling restores what was there before.

---

## 🏗️ Considered Options

1. **Links** from each app's file to one master copy.
2. **Byte-identical copies**, one per app, checked against the hashes in the pinned release.
3. **Settings that point each app at one shared file**, where an app has such a setting.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, copies checked against the release

### Rationale for Selection

Copies work in every sandbox and every desktop session, where links fail silently. `~/.agents/AGENTS.md` stays as the master copy: Warp, Cline, goose and Kimi Code already read it, and none of the six apps does, so it never loads twice. Each app's copy takes the shape that app requires:

| Folder        | Copy                                                                    |
| :------------ | :---------------------------------------------------------------------- |
| `~/.claude/`  | `rules/intelligence.md`; in a Claude cloud session, `CLAUDE.md` instead |
| `~/.codex/`   | A marked block in `AGENTS.md`, so the owner's text stays                |
| `~/.gemini/`  | `AGENTS.md`, which Antigravity CLI reads natively                       |
| `~/.copilot/` | `instructions/intelligence.instructions.md`, with `applyTo: "**"`       |
| `~/.grok/`    | Nothing: Grok Build reads `~/.claude` by default                        |
| `~/.cursor/`  | Nothing: the home file is pasted into Cursor's User Rules               |

Claude Code also gets `instructionFiles: claude-md-and-agents-md`, under both its current plugin ID and the one it used before v2.1.285, so `AGENTS.md` loads beside a `CLAUDE.md`. `make agents-check` compares every copy with the hashes in the pinned release, not with a local manifest an agent could rewrite, and `make agents-uninstall` restores the prior values the installer recorded.

Option 3 covers too few apps, and Gemini CLI, for one, rewrites its settings file from memory and drops keys it did not load.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                                       |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Works in every sandbox and desktop session; the owner's own text is kept; drift is caught against the release                                                                              |
| **Negative (-)** | Cursor needs the home file pasted by hand after each change to the block; Copilot in VS Code also reads `~/.claude/rules`, so it loads the rules twice, about 800 tokens, with no conflict |
| **Neutral (~)**  | The kit never writes `~/AGENTS.md` or `~/CLAUDE.md`, which apps that walk up the folder tree would load in every project beneath home                                                      |

---

## ⚖️ Trade-off Comparative

### Option 1: Links

- ✅ One real file, edited once
- ❌ Fails silently in Claude's desktop sessions and Grok's sandbox, and takes over personal files

### Option 2: Copies checked against the release

- ✅ Works everywhere, keeps personal text, and can be verified
- ❌ Several copies to keep in step, which the check automates

### Option 3: Settings that point at one file

- ✅ No duplicated text
- ❌ Only some apps have such a setting, and some rewrite their own settings files

---

## 🔗 Traceability & Links

- [ADR-0001](ADR-0001-Two-Pieces-Home-&-Repository.md): the home piece
- [Loader probe](../../probe/README.md): proves each copy loads

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Copied into every app, and checked against the release.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
