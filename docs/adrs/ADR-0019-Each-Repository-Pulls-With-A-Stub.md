<!--
title: '📄 ADR-0019: EACH REPOSITORY PULLS WITH A STUB'
description: 'A repository that wants the rules carries a small workflow stub that pulls each release on its own GITHUB_TOKEN and proposes it as one pull request; no GitHub App, no key, and merging stays the owner''s.'
tags: [adr, sync, github-actions, workflow-stub]
category: docs
status: 'Proposed'
date: '2026-10-18'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0019: EACH REPOSITORY PULLS WITH A STUB

<a name="top"></a>

**Each repository asks for the rules itself, on its own token; you still decide what lands.**

_No App. No key. One stub._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                          |
| :------------- | :------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                |
| **Consulted**  | Claude Code sessions: the platform research behind ADR-0003, and drafting              |
| **Informed**   | Every agent and collaborator working in a repository that carries the block            |
| **Supersedes** | [ADR-0017](ADR-0017-Unattended-Sync-Through-An-App.md), unattended sync through an App |

---

## 🎯 Context & Problem Statement

[ADR-0017](ADR-0017-Unattended-Sync-Through-An-App.md) made sync unattended through a GitHub App: a key in a protected environment of the hub, one token per repository. The owner would rather not run an App, and asked for GitHub Actions and a stub instead.

[ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md) weighed exactly that as its Option 2, "a secret-free stub that opens a pull request with `GITHUB_TOKEN`", and kept it as "the fallback if a stub in every repository ever becomes a requirement of its own". It recorded two costs: such a pull request's checks wait for approval, and GitHub disables a public repository's schedules after 60 quiet days. Its objection to a stub with an App key in every repository does not apply to a stub that needs no key at all.

---

## 🚦 Decision Drivers

- **No App and no key anywhere**, and no credential in the hub that reaches another repository.
- **Merging stays the owner's**, with no bypass actor and no auto-merge.
- **One review per release**, not one per repository.
- **The hub's code runs only at a release**, never from a branch.

---

## 🏗️ Considered Options

1. **Keep the App** of ADR-0017.
2. **A stub in each repository** that calls a reusable workflow in the hub on its own `GITHUB_TOKEN`, through the standards' open-pr action.
3. **`make sync` by hand only**, as before ADR-0017.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, a stub in each repository

### Rationale for Selection

A repository that wants the rules copies `setup/intelligence-sync.yml` to `.github/workflows/intelligence-sync.yml`. Every Monday, and whenever it is run, the stub calls `.github/workflows/sync.yml` at the hub's moving major. That workflow checks out the repository's default branch, runs `actions/sync`, which runs `scripts/sync.py apply` from the hub tree at the same major, and hands the result to the standards' open-pr action. It commits as the owner, signs off as the owner, and opens or updates one pull request on `chore/intelligence`, the branch `make sync` uses. The stub grants `contents: write` and `pull-requests: write`, exactly what the workflow asks for, and hands over one optional secret, `BOT_ACCESS_TOKEN`, never `secrets: inherit`.

ADR-0003's two costs are met directly:

- **Checks that wait.** `make merge` proves the diff is the block alone first; only then does it approve the waiting runs of a pull request a bot opened, falling back to closing and reopening it as the owner, and it merges on a later run once they pass. A first sync waits for the owner's review, where **Approve workflows to run** starts its checks. A repository with a `BOT_ACCESS_TOKEN` opens the pull request as that token's owner, and its checks start at once.
- **Schedules that stop.** A quiet public repository stops pulling; `make audit` names its older block and whether it carries the stub, and `make sync` reaches every repository regardless.

`make sync`, `make merge` and `make audit` stay as they were, under the owner's own login. The templates stay free of agent configuration, as their README promises: they name the stub as one of two routes, and the owner adds it where they want it.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                         |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | No App and no key; a release reaches every repository with the stub by Monday; each repository's token reaches only that repository                          |
| **Negative (-)** | Each stub runs the hub's code at the moving major with write access, so a bad release reaches every repository that carries it, and checks wait for approval |
| **Neutral (~)**  | The stub is opt-in, per repository; repositories without it are synced by `make sync` as before                                                              |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep the App

- ✅ Pull requests start their checks at once, and nothing in a repository runs hub code
- ❌ An App to create, a key to keep and rotate, and a protected environment to maintain

### Option 2: A stub in each repository

- ✅ No credential to create or keep; it reuses the standards' open-pr action and the same branch as `make sync`
- ❌ Checks wait for approval, a quiet public repository stops pulling, and a release runs in every repository that carries the stub

### Option 3: By hand only

- ✅ Nothing runs anywhere unless the owner runs it
- ❌ A ritual after every release, and a hand edit stays until the next one

---

## 🔗 Traceability & Links

- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): the hub pushes, the owner merges, and its Option 2
- [ADR-0017](ADR-0017-Unattended-Sync-Through-An-App.md): the App this replaces
- [`setup/intelligence-sync.yml`](../../setup/intelligence-sync.yml), [`.github/workflows/sync.yml`](../../.github/workflows/sync.yml), [`actions/sync/`](../../actions/sync/README.md) and [`scripts/sync.py`](../../scripts/sync.py), explained in [Repository Sync](../technical/Repository-Sync.md)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Each repository asks, and only you merge.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
