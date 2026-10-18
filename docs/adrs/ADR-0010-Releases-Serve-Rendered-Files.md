<!--
title: '📄 ADR-0010: RELEASES SERVE RENDERED FILES'
description: 'A release is a tag whose committed home file and installer every consumer downloads and checks against a pinned SHA-256, instead of assets built and attached after the tag.'
tags: [adr, releases, pinning, supply-chain]
category: docs
status: 'Proposed'
date: '2026-10-17'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0010: RELEASES SERVE RENDERED FILES

<a name="top"></a>

**A release is a tag, and the tag serves exactly the files CI checked, each one verified against a pin.**

_Tagged, rendered, pinned._

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

The plan gave each release three attached assets: the block, the home file and `SHA256SUMS`. The standards' release machinery does not deliver that:

- 🏷️ Cut Release publishes a release with `GITHUB_TOKEN`, and a release created with `GITHUB_TOKEN` does not trigger `on: release`, so the publish job that builds and attaches assets never runs.
- When that job does run, it packages one tarball of a build folder, not individual files a machine can fetch by name.

Building assets inside Cut Release would mean a new job with its own permissions, upload steps and failure modes, all to publish files the hub already renders and commits.

---

## 🚦 Decision Drivers

- **One URL per file**, fetched with no token on any machine.
- **The file a machine installs is the file CI checked**, byte for byte.
- **Integrity from a pin**, never from a hash served beside the download.
- **Few moving parts** for one maintainer.

---

## 🏗️ Considered Options

1. **Assets built and uploaded by a job added to Cut Release.**
2. **The standards' publish tarball**, triggered by hand after each release.
3. **Rendered files committed and served from the tag**, each fetched by its raw URL and checked against a pinned SHA-256.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, serve the rendered files from the tag

### Rationale for Selection

`home/intelligence.md` and `scripts/install.py` are committed, and `make check`, which CI runs and Cut Release runs as its `check-command`, fails while the rendered copies differ from the law. So the file at a tag is always the file the law produced. A public repository serves any file at a tag with no token, at a URL that never changes:

```text
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/home/intelligence.md
```

The trust anchor is the pin: dotfiles' pin file and the cloud setup script each carry the SHA-256 of both files for one version, computed with `make pins VERSION=...` from the tag itself. `SHA256SUMS` stays in `home/` for a reader, and is never used to check a download it came with. Releases are never pruned, so a pinned version keeps resolving.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                       |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One stable URL per file; no upload job and no extra permissions; what a machine installs is exactly what CI checked        |
| **Negative (-)** | The rendered files must be re-rendered whenever the law or the installer changes, which `make render` does and CI enforces |
| **Neutral (~)**  | The release page carries notes only; the files live in the tagged tree                                                     |

---

## ⚖️ Trade-off Comparative

### Option 1: Assets built by a new job

- ✅ Matches the original plan
- ❌ A new job, new permissions and an upload that can fail after the tag exists

### Option 2: The publish tarball

- ✅ Reuses the standards as they are
- ❌ A manual step after every release, and a tarball instead of files

### Option 3: Rendered files from the tag

- ✅ Simple, token-free, and checked by CI before the tag exists
- ❌ Rendered copies are committed beside their source

---

## 🔗 Traceability & Links

- [ADR-0005](ADR-0005-Home-Copies-Not-Links.md): what the home kit does with the home file
- [ADR-0003](ADR-0003-Push-Sync-&-Owner-Merge.md): sync delivers the latest tag's block
- [The Home Kit](../technical/The-Home-Kit.md) and [Cloud Setup](../technical/Cloud-Setup.md)

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**What CI checked is what every machine installs.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
