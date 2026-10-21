<!--
title: '📄 ADR-0012: ONE PINNED KIT FOR EVERY MODULE'
description: 'Every module around the rules, the guard hook, the skills, the subagents and the knowledge facts, ships in one rendered file, home/kit.json, pinned by one SHA-256 beside the home file and the installer.'
type: record
status: 'Proposed'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0012: ONE PINNED KIT FOR EVERY MODULE

<a name="top"></a>

**Four modules, one file, one more pin.**

_Many sources, one bundle, one hash._

</div>

> [!IMPORTANT]
> **Amended by [ADR-0023](ADR-0023-The-Kit-Carries-No-Facts.md).** The kit
> carries three modules now, the guard hook, the skills and the subagents: the
> knowledge facts are gone, and the kit's format is 2.

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

After 1.0 the plan brings back the modules it deferred: the guard hook, skills, knowledge, the agent hierarchy and evals. Each one adds files a machine must install, in formats that differ per app: a Python script, folders of Markdown, subagents that Claude Code and Copilot read as Markdown and Codex reads as TOML, and a block of facts. Releases already serve the home file and the installer from the tag, each checked against a pin ([ADR-0010](ADR-0010-Releases-Serve-Rendered-Files.md)). One pin per new file would multiply what dotfiles and the cloud setup script must carry.

---

## 🚦 Decision Drivers

- **One more pin, not one per file**, for dotfiles and the cloud setup script.
- **The installer converts nothing**: every app's form is rendered and reviewed in the hub.
- **Readable sources** that a person edits, separate from what a machine installs.
- **The installer stays one standard-library file** on a Mac's Python 3.9.

---

## 🏗️ Considered Options

1. **One pinned download per module file**, fetched by its raw URL like the home file.
2. **A tarball attached to each release**, unpacked by the installer.
3. **One rendered JSON bundle, `home/kit.json`**, committed beside the home file, served from the tag and pinned by one SHA-256.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, one rendered bundle

### Rationale for Selection

`.github/scripts/kit.py` renders the bundle from the sources: `kit/guard.py`, `kit/skills/`, `kit/subagents/` and `knowledge/public.json`. It holds each source to the strictest rule any target app enforces, so a skill with a bad name or a subagent with an unknown tool stops `make check` rather than failing silently on a machine. `render.py` writes the bundle with the other rendered files, lists it in `home/SHA256SUMS`, and prints `kit_sha256` with the other pins. The installer takes it with `--kit-file`; a pin with no kit hash, from a release before the kit, installs the rules alone. Everything the kit writes carries its mark, so the installer replaces only what is its own and `uninstall` takes back exactly what it added.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                              |
| :--------------- | :---------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One more pin covers every module; each app's form is reviewed in the hub; a broken source fails CI, not a machine |
| **Negative (-)** | Every change to a module needs `make render`, and the bundle's diffs are JSON-escaped text                        |
| **Neutral (~)**  | The bundle is committed and served from the tag, like the home file                                               |

---

## ⚖️ Trade-off Comparative

### Option 1: One download per file

- ✅ Each file readable at its own URL
- ❌ A pin per file, in two places, for every module

### Option 2: A release tarball

- ✅ Familiar packaging
- ❌ A publish job that never runs under GITHUB_TOKEN, and an unpacker in the installer

### Option 3: One rendered bundle

- ✅ One pin, no conversion on the machine, validated in CI
- ❌ Re-rendered on every module change

---

## 🔗 Traceability & Links

- [ADR-0010](ADR-0010-Releases-Serve-Rendered-Files.md): releases serve rendered files, checked against pins
- [`.github/scripts/kit.py`](../../.github/scripts/kit.py) and [`home/`](../../home/README.md), explained in [The Home Kit](../technical/The-Home-Kit.md)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Every module ships the way the rules do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
