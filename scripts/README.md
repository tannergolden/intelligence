<!--
title: '🔧 HUB SCRIPTS'
description: 'The scripts that render the law, install it on a machine, and deliver it to every repository, with the tests that guard them.'
tags: [scripts, render, home-kit, sync]
category: docs
-->

<div align="center">

# 🔧 HUB SCRIPTS

<a name="top"></a>

**Render the law, install it at home, deliver it to every repository: three scripts and their tests.**

_Standard library only, from a Mac's Python 3.9 up._

</div>

---

## 💡 What This Folder Is For

| Script                     | What it does                                                                                     | Run by                                  |
| :------------------------- | :----------------------------------------------------------------------------------------------- | :-------------------------------------- |
| [`render.py`](render.py)   | Checks the law and renders every copy of the block: `AGENTS.md`, the home file and its hashes    | `make render`, `make lint`, CI          |
| [`install.py`](install.py) | Installs the home file into each app's folder, checks it, and uninstalls it to the byte          | dotfiles' `make agents`, cloud setup    |
| [`sync.py`](sync.py)       | Audits every repository, opens one sync pull request each, and merges the green, block-only ones | `make audit`, `make sync`, `make merge` |

`install.py` runs on its own after a machine downloads it from a release, so
it imports nothing from the hub. `sync.py` reaches GitHub only through the
owner's `gh` login.

---

## 🚀 Running Them

From the root of the repository:

```bash
make render                    # rewrite every copy from the law
make audit                     # what every repository carries now
make sync ARGS=--dry-run       # what a sync would change
make sync                      # open or update one pull request per repository
make merge                     # merge the green ones whose diff is only the block
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`make sync` delivers the latest release's block. To deliver unreleased rules
on purpose, pass `ARGS='--ref HEAD'`.

> [!NOTE]
> **The tests keep their underscores on purpose.** `unittest` imports each
> `test_*.py` as a module, and a module name cannot contain a hyphen.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                | Purpose                                                                                     |
| :----------------------------------- | :------------------------------------------------------------------------------------------ |
| [`install.py`](install.py)           | Install the universal rules into every AI app's home folder, check them, and take them out. |
| [`README.md`](README.md)             | This file.                                                                                  |
| [`render.py`](render.py)             | Render the universal rules from the law into every copy this hub publishes.                 |
| [`sync.py`](sync.py)                 | Deliver the universal rules to every repository the owner owns, and keep them there.        |
| [`test_install.py`](test_install.py) | Tests for the home kit installer.                                                           |
| [`test_render.py`](test_render.py)   | Tests for the law renderer.                                                                 |
| [`test_sync.py`](test_sync.py)       | Tests for repository sync, audit and merge.                                                 |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**The law, rendered, installed and delivered, every step under test.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
