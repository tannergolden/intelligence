<!--
title: '📄 ADR-0003: PUSH SYNC & OWNER MERGE'
description: 'The hub delivers each release as one pull request per repository, opened under the owner''s own login, and the owner merges them, with no stub, secret or bot merge in any repository.'
type: record
keywords: [delivery, pull-requests, github]
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0003: PUSH SYNC & OWNER MERGE

<a name="top"></a>

**One pull request per repository, opened by the hub, merged by you, with no secret anywhere but the hub.**

_The hub proposes. You merge._

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

The first design put a workflow stub in every repository that pulled the block at a moving tag. A personal GitHub account has no account-wide Actions secrets, so the GitHub App key the stub needed would sit in every repository's secrets. Anyone with write access to a repository can read those secrets, App keys never expire, and one leaked key opens every repository the App is installed on. The stub also ran hub code with each repository's own credentials, and `secrets: inherit` would hand it every other secret there too.

Three GitHub behaviours add more failures:

- Pull requests opened with `GITHUB_TOKEN` now wait for approval before their checks run.
- GitHub disables scheduled workflows in a public repository after 60 days without activity.
- Auto-merge cannot coexist with a ruleset that lets only the owner update default branches: a bot that merges must be a bypass actor. On private repositories, auto-merge also needs Pro.

---

## 🚦 Decision Drivers

- **No secret outside the hub**, so no repository holds a key that opens the others.
- **The owner alone updates default branches**, with no bypass actor.
- **One review per release**, not one per repository.
- **Works on GitHub Free**, with nothing that stops after 60 quiet days.

---

## 🏗️ Considered Options

1. **A stub in every repository** that pulls the block at a moving tag, with an App key in each.
2. **A secret-free stub** that opens a pull request with `GITHUB_TOKEN`.
3. **Push from the hub under the owner's login**: `make sync` opens one pull request per repository, and `make merge` merges them.
4. **Push from the hub with an App key, and auto-merge.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, push from the hub, and the owner merges

### Rationale for Selection

Push keeps every credential in the hub. `make sync` uses the owner's existing `gh` login, so there is no new credential, nothing scheduled and nothing that stops after 60 quiet days. The pull requests are the owner's own, so the required checks run normally and the DCO sign-off is the owner's.

The owner reviews each release once, here. Then `make merge` merges every sync pull request whose diff is exactly the block and whose checks pass.

Every repository the owner owns takes part, except templates, forks and archived ones, and a `no-intelligence` topic opts one out. Including everything by default is safe because nothing lands until the owner merges it. Sync pull requests use the `chore/intelligence` branch, beside `chore/template-sync`.

Option 4 returns after 1.0 as the first module, without auto-merge: one App key in a protected environment of the hub, minting one token per target repository. Option 2 stays the fallback if a stub in every repository ever becomes a requirement of its own.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                             |
| :--------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | No credential in any consuming repository; consumers run no hub code; required checks and the DCO behave as for any pull request the owner opens |
| **Negative (-)** | Two commands to run after each release until the unattended module ships; the owner's login reaches every repository it syncs                    |
| **Neutral (~)**  | The templates stay free of agent files, since sync skips templates                                                                               |

---

## ⚖️ Trade-off Comparative

### Option 1: A stub with an App key in each repository

- ✅ Updates arrive with no action from the owner
- ❌ A key that opens every repository, readable in each of them

### Option 2: A secret-free stub

- ✅ No key in any repository
- ❌ Its pull requests wait for approval, and it stops after 60 quiet days in public repositories

### Option 3: Push under the owner's login

- ✅ No new credential, and one review per release
- ❌ Manual until the unattended module ships

### Option 4: Push with an App key, and auto-merge

- ✅ Fully unattended
- ❌ The merging bot must bypass the owner-only ruleset, so its key could push straight to every default branch

---

## 🔗 Traceability & Links

- [ADR-0004](ADR-0004-Precedence-Overrides-&-Hash-Marker.md): the hash marker that keeps an unchanged release quiet
- [ADR-0006](ADR-0006-Build-The-Law-Adopt-The-Plumbing.md): why sync is built on `gh`
- [Repository Sync](../technical/Repository-Sync.md): how a release reaches the repositories

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Proposed by the hub, merged by you.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
