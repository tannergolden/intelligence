<!--
title: '🌿 STANDARDS OFFLINE'
description: 'How a repository vendors the engineering standards on disk so an agent can read them without following a link.'
tags: [submodule, standards, offline, vendoring]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🌿 STANDARDS OFFLINE

<a name="top"></a>

**Agents do not follow links, so the standard has to be on disk to be followed.**

_A pin, never a paste._

</div>

---

## 🎯 The Problem This Solves

This whole publisher exists because **agents do not reliably follow links**. That is the founding complaint in the README, and the agent files exist to put the law *in the tree* rather than one hop away.

The standards themselves were left out of that. Rule 6 of the law tells every agent to read the styling specification before writing any Markdown, and that specification lives in another repository, reachable only by a link the agent will probably not follow. So the rule most often broken is the rule whose source is hardest to reach.

A submodule closes that gap: the specification becomes a file on disk, at a path an agent can open.

---

## 🧷 A Submodule Is A Pin, Not A Copy

This repository says everywhere that standards are followed **by link, never by copy**, because a copied standard starts going stale the moment it is pasted. A submodule does not contradict that, and the distinction is exact:

| | Stores | Goes stale | Updated by |
| :--- | :--- | :--- | :--- |
| **A copy** | the bytes | silently, from the first edit upstream | nothing |
| **A submodule** | a URL and one commit SHA | never, because it holds no content | a deliberate commit |

Nothing can drift, because nothing is in your tree except a pointer. It is the same shape as pinning `@v1` on a checkout step, and it resolves to bytes on disk instead of to a URL.

---

## 📥 Installing It

```bash
git submodule add https://github.com/tannergolden/standards.git standards
cd standards && git checkout v1 && cd ..
git add .gitmodules standards
git commit -m 'build(standards): vendor the engineering standards at v1'
```

That records the SHA `v1` currently points at. Then **tell your agents it is there**, in whatever your repository uses for its own context, because the law tells them to find that context rather than to guess a path.

> [!IMPORTANT]
> **Do not pass `--depth 1`.** A shallow submodule cannot fetch tags: `git fetch --tags` reports `rejected refs/tags/v1 because shallow roots are not allowed to be updated`, and the `git checkout v1` above then fails with `pathspec 'v1' did not match`. The shallow clone saves a couple of megabytes and costs you the ability to pin to a release.

---

## 🧯 The Failure That Matters

**A plain `git clone` leaves the directory present and empty.**

```bash
git clone <your-repo>
ls -A standards/   # 0 entries
```

This is worse than not installing it at all. The path exists, so an agent looking for the specification finds a directory, finds nothing in it, and may reasonably conclude the standards are empty rather than uninitialized.

Two ways to be right:

```bash
git clone --recurse-submodules <your-repo>   # when cloning
git submodule update --init                  # to recover an existing clone
```

**And your CI must opt in**, or every workflow sees the empty directory:

```yaml
- uses: actions/checkout@<sha> # <version>
  with:
    submodules: true
```

> [!WARNING]
> **The shared reusable CI in `standards` does not check out submodules**, and exposes no input to make it. Its checkout steps pass `persist-credentials: false` and nothing else, so a job running there sees the empty directory whatever you do in your stub.
>
> This is usually harmless: the vendored standards are for agents to read, not for a build to consume, and no stage of that workflow needs them. It matters only if you write a check that reads the specification, and that check has to live in a job you control.

---

## 🔄 Updating The Pin

```bash
cd standards && git fetch --tags && git checkout v1 && cd ..
git add standards
git commit -m 'build(standards): move the pin to the current v1'
```

> [!NOTE]
> **`git submodule update --remote` does not work with a tag.** It resolves `refs/remotes/origin/<name>`, which exists for a branch and never for a tag, so it fails with `Unable to find refs/remotes/origin/v1 revision`. Setting `submodule.<name>.branch` to a branch makes `--remote` work, but then you are tracking unreleased work rather than a release. Pin to the tag and move it deliberately.

Because `v1` moves when a release is cut, re-running the checkout above is how a fix reaches you. The pin in your tree is a SHA, so nothing changes underneath you until you run it.

---

## 💰 What It Costs

**About 2.5 MB of clone**, of which the documentation is roughly 356 KB across 32 files.

It costs **nothing in context**. The files sit on disk and are read only when an agent opens one, which is the same economics as a skill's bundled references: free until used. That is the whole reason this beats pasting the specification into an instruction file, where it would be paid in every session forever.

If the clone size matters, a local trim is possible, though it is **per-clone and does not propagate**, because sparse-checkout settings are not committed:

```bash
cd standards
git sparse-checkout init --cone
git sparse-checkout set docs
```

---

## 🗑️ Removing It

```bash
git submodule deinit -f standards
git rm -f standards
rm -rf .git/modules/standards
git commit -m 'build(standards): stop vendoring the standards'
```

Nothing else was installed and nothing executed, so there is nothing further to undo.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

The agent files themselves arrive by a different mechanism, described in [Installation](Installation.md), because three root files want copying and a whole repository wants pinning.

---

<div align="center">

**Vendored by pin, read from disk, deletable in one command.**

[↑ Back to Top](#top)

</div>
