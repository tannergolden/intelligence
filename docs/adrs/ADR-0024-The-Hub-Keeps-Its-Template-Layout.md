<!--
title: '📄 ADR-0024: THE HUB KEEPS ITS TEMPLATE''S LAYOUT'
description: 'The hub follows the layout of the template it was generated from: every script and its test in .github/scripts/, the kit''s sources in kit/, and everything a machine downloads in home/, the installer included.'
type: record
keywords: [repository-layout, home-kit, release, migration]
status: 'Proposed'
date: '2026-10-20'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0024: THE HUB KEEPS ITS TEMPLATE'S LAYOUT

<a name="top"></a>

**Every script in `.github/scripts/`, the kit's sources in `kit/`, and everything a machine downloads in `home/`.**

_The template's shape, and no consumer broken on the way._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                   |
| :------------ | :---------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                         |
| **Consulted** | Claude Code sessions: a comparison with tannergolden/repo and the standards' layout rule        |
| **Informed**  | Everyone who installs the home kit, and every repository that carries the stub                  |
| **Amends**    | [ADR-0010](ADR-0010-Releases-Serve-Rendered-Files.md), which served the installer from scripts/ |

---

## 🎯 Context & Problem Statement

The hub was generated from tannergolden/repo, whose root holds only its scaffold: a repository's own composite actions live in `.github/actions/` and its scripts in `.github/scripts/`. The standards' [Repository Hygiene](https://github.com/tannergolden/standards/blob/Development/docs/operations/Repository-Hygiene.md) makes that the rule: every helper lives in `.github/scripts/`, whoever runs it.

The hub grew seven folders beside the template's. Its scripts and their tests sat in four places, `scripts/`, `probe/`, `setup/` and `evals/`, with `make test` running five test suites. The kit's sources sat in three, `scripts/guard.py`, `skills/` and `subagents/`. And a machine downloaded the installer from `scripts/`, beside everything else it downloads from `home/`.

Two things constrain any move. A consumer fetches each file by its path at a tag: dotfiles' home kit and the cloud setup script. And every repository's stub runs the hub's action from the archive GitHub serves at the tag, which the template's `.gitattributes` strips of everything in `.github/` except `.github/actions/`.

---

## 🚦 Decision Drivers

- **The template's layout**, and the standards' rule that every script lives in `.github/scripts/`.
- **One folder for each kind of thing**: the scripts, the kit's sources, and what a machine downloads.
- **No consumer broken**: a pinned release keeps installing, and every stub keeps finding its code.

---

## 🏗️ Considered Options

1. **Keep the layout.**
2. **Move the scripts and their tests into `.github/scripts/`**, and nothing else.
3. **Move the scripts into `.github/scripts/`, gather the kit's sources in `kit/`, and serve everything a machine downloads from `home/`.**

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, the template's layout, with one folder for each kind of thing

### Rationale for Selection

| Was                                                                    | Is now                                                                             |
| :--------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `scripts/render.py`, `kit.py`, `sync.py`, `install.py` and their tests | `.github/scripts/`, beside the template's checks                                   |
| `evals/run.py` and `evals/test_run.py`                                 | `.github/scripts/evals.py` and `test_evals.py`; the scenarios stay in `evals/`     |
| `probe/loader-probe.py` and its test                                   | `.github/scripts/`                                                                 |
| `setup/test_cloud_setup.py` and `setup/test_stub.py`                   | `.github/scripts/`; the two files a consumer copies stay in `setup/`               |
| `scripts/guard.py`, `skills/` and `subagents/`                         | `kit/guard.py`, `kit/skills/` and `kit/subagents/`, the sources of `home/kit.json` |
| `scripts/install.py`, as a release serves it                           | `home/install.py`, which `make render` copies from `.github/scripts/install.py`    |

The root now holds the template's scaffold, `CONSTITUTION.md`, the Makefile and four folders of the hub's own: `evals/`, `home/`, `kit/` and `setup/`. `make test` is one test run, and every `make` target keeps its name.

`home/` is now the whole of what a machine downloads, so the hub's scripts can move again without moving a consumer. A release from before this one serves the installer at `scripts/install.py`: dotfiles, the cloud setup script and `make pins` look there when `home/install.py` is missing, and the pinned hash decides either way. The stub's action finds `sync.py` at `$GITHUB_ACTION_PATH/../../scripts/`, and the hub's `.gitattributes` keeps `.github/scripts/` in the archive, below the template's lines so that it wins. `test_stub.py` proves both.

Option 2 leaves the kit's sources in three places and ties the installer's public address to the hub's tooling. Option 1 keeps the hub out of the template's shape and the standards' rule.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                        |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | The root reads like the template's, one test run covers the hub, and a machine downloads from one folder                                    |
| **Negative (-)** | The installer is in the tree twice, its source and the copy a release serves, which `make check` keeps identical; consumers keep a fallback |
| **Neutral (~)**  | A path typed by hand changes, such as `python3 kit/guard.py`; `make` targets and the stub's address stay as they were                       |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Layout

- ✅ No change to any path
- ❌ Seven root folders the template does not have, and scripts in four places

### Option 2: Move Only The Scripts

- ✅ The standards' rule kept, with the smallest move
- ❌ The kit's sources stay scattered, and the installer's address moves with the tooling

### Option 3: The Template's Layout, One Folder Each

- ✅ Each folder holds one kind of thing, and the address a machine downloads from stays put from now on
- ❌ A one-time move of every consumer to `home/install.py`, with a fallback for earlier releases

---

## 🔗 Traceability & Links

- [`.github/scripts/`](../../.github/scripts/README.md): every script, with its test beside it
- [`kit/`](../../kit/README.md): the kit's sources
- [`home/`](../../home/README.md): everything a machine downloads
- [ADR-0010](ADR-0010-Releases-Serve-Rendered-Files.md): the served files this amends
- [The Home Kit](../technical/The-Home-Kit.md): how a machine gets the files, and the fallback

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The template's shape, with the hub's own parts in plain sight.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
