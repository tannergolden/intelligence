<!--
title: '📄 ADR-0017: UNATTENDED SYNC THROUGH AN APP'
description: 'A GitHub App, with one token per repository and a key kept in a protected environment, opens each release''s sync pull requests unattended, while merging stays the owner''s, under the owner''s own login.'
type: record
keywords: [github-app, automation]
status: 'Superseded'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0017: UNATTENDED SYNC THROUGH AN APP

<a name="top"></a>

**The hub proposes every release by itself; you still decide what lands.**

_Opened by a bot. Merged by you._

</div>

> [!IMPORTANT]
> **Superseded by [ADR-0019](ADR-0019-Each-Repository-Pulls-With-A-Stub.md).**
> Each repository now pulls the rules with a stub, on its own token, and the
> App this record describes was never created.

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

Version 1 runs `make sync` under the owner's own `gh` login after each release ([ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md)). That is a ritual to remember, and a block edited by hand stays edited until the next run. Pull requests opened with `GITHUB_TOKEN` start no workflows, and a release published with it starts no `on: release` workflow. The plan named the module: "One App key in a protected environment of the public hub, limited to main and release tags, with Contents and Pull requests write and no Workflows, Administration, Checks or Statuses permission ... Mint one token per target repository so a leaked token reaches one repository."

---

## 🚦 Decision Drivers

- **No ritual**: every release reaches every repository by itself.
- **Merging stays the owner's.**
- **The smallest blast radius**: a leaked token reaches one repository for an hour.
- **Nothing to set up in any target repository.**

---

## 🏗️ Considered Options

1. **Keep `make sync` by hand.**
2. **A personal access token** in the hub, used by a scheduled workflow.
3. **A GitHub App** with a key in a protected environment, one token per repository, chained after Cut Release and run weekly.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, a GitHub App

### Rationale for Selection

`.github/workflows/sync.yml` runs after 🏷️ Cut Release, every Monday and on demand. Its plan job mints a token that can only read metadata and lists the repositories with `sync.py targets --app`; each matrix job mints a token for its one repository, with Contents and Pull requests write, and runs `sync.py sync --app`. App mode lists the installation's repositories, writes commits with no sign-off, because a bot certifies nothing and the DCO check exempts bots, and refuses `merge` outright. The key lives in the `intelligence-sync` environment, limited to the default branch and `v*` tags. Every job is skipped until the `INTELLIGENCE_APP_CLIENT_ID` variable exists, so the workflow is inert until the owner creates the App.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                              |
| :--------------- | :---------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Releases and repairs reach every repository unattended; no repository holds a key; a token reaches one repository |
| **Negative (-)** | An App to create and a key to rotate; the App's pull requests are authored by a bot, not the owner                |
| **Neutral (~)**  | `make sync` under the owner's login still works, for a first sync or a repository the App cannot reach            |

---

## ⚖️ Trade-off Comparative

### Option 1: By hand

- ✅ No new credential
- ❌ A ritual after every release, and drift until the next one

### Option 2: A personal access token

- ✅ Simple to set up
- ❌ One long-lived token that reaches every repository

### Option 3: A GitHub App

- ✅ Short-lived tokens, one repository each
- ❌ An App to create and a key to rotate

---

## 🔗 Traceability & Links

- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): the hub pushes, the owner merges
- [ADR-0019](ADR-0019-Each-Repository-Pulls-With-A-Stub.md): the stub that supersedes this record
- [`.github/workflows/sync.yml`](../../.github/workflows/sync.yml) and [`scripts/sync.py`](../../scripts/sync.py)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**A bot proposes, and only you merge.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
