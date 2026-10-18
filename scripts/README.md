<!--
title: '🔧 HUB SCRIPTS'
description: 'The scripts that render the law and the kit, install them on a machine, guard every tool call, and deliver the rules to every repository, with their tests.'
tags: [scripts, render, home-kit, sync]
category: docs
-->

<div align="center">

# 🔧 HUB SCRIPTS

<a name="top"></a>

**Render the law and the kit, install them at home, guard every tool call, deliver the rules everywhere: five scripts and their tests.**

_Standard library only, from a Mac's Python 3.9 up._

</div>

---

## 💡 What This Folder Is For

| Script                     | What it does                                                                                       | Run by                                              |
| :------------------------- | :------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| [`render.py`](render.py)   | Checks the law and renders every copy of the block, the kit and the hashes                         | `make render`, `make lint`, CI                      |
| [`kit.py`](kit.py)         | Checks the guard, skills, subagents and knowledge facts, and bundles them into `home/kit.json`     | `render.py`                                         |
| [`install.py`](install.py) | Installs the home file and the kit into each app's folder, checks them, and uninstalls to the byte | dotfiles' `make agents`, cloud setup                |
| [`guard.py`](guard.py)     | Denies the tool calls the Invariants forbid outright, before they run, in every app                | each app's pre-tool hook, once installed            |
| [`sync.py`](sync.py)       | Audits every repository, opens one sync pull request each, and merges the green, block-only ones   | `make audit`, `make sync`, `make merge`, `sync.yml` |

`install.py` and `guard.py` run on their own on a machine, after a release
delivers them, so they import nothing from the hub. `sync.py` reaches GitHub
only through `gh`: under the owner's login for `audit`, `sync` and `merge`,
and, for `apply`, under the `GITHUB_TOKEN` of a repository whose stub runs
it. That run uses the hub tree GitHub downloads at the moving major tag, so
`sync.py`, `render.py` and `kit.py` must all be in every release.

---

## 🚀 Running Them

From the root of the repository:

```bash
make render                    # rewrite every copy from the law
make audit                     # what every repository carries now
make sync ARGS=--dry-run       # what a sync would change
make sync                      # open or update one pull request per repository
make merge                     # merge the green ones whose diff is only the block
python3 scripts/guard.py --command 'git push --force'   # try the guard on a command
python3 -m unittest discover -s scripts -p 'test_*.py'
```

`make sync` delivers the latest release's block. To deliver unreleased rules
on purpose, pass `ARGS='--ref HEAD'`. To see what a repository's stub would
write, run `apply` in its checkout:

```bash
GITHUB_REPOSITORY=tannergolden/<name> python3 /path/to/intelligence/scripts/sync.py apply --dry-run
```

> [!NOTE]
> **The tests keep their underscores on purpose.** `unittest` imports each
> `test_*.py` as a module, and a module name cannot contain a hyphen.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                | Purpose                                                                                     |
| :----------------------------------- | :------------------------------------------------------------------------------------------ |
| [`guard.py`](guard.py)               | Block the few tool calls the universal rules forbid outright, before they run.              |
| [`install.py`](install.py)           | Install the universal rules into every AI app's home folder, check them, and take them out. |
| [`kit.py`](kit.py)                   | Render everything the home kit installs besides the rules into one bundle, `home/kit.json`. |
| [`README.md`](README.md)             | This file.                                                                                  |
| [`render.py`](render.py)             | Render the universal rules from the law into every copy this hub publishes.                 |
| [`sync.py`](sync.py)                 | Deliver the universal rules to every repository the owner owns, and keep them there.        |
| [`test_guard.py`](test_guard.py)     | Tests for the guard hook.                                                                   |
| [`test_install.py`](test_install.py) | Tests for the home kit installer.                                                           |
| [`test_kit.py`](test_kit.py)         | Tests for the kit renderer.                                                                 |
| [`test_render.py`](test_render.py)   | Tests for the law renderer.                                                                 |
| [`test_sync.py`](test_sync.py)       | Tests for repository sync, audit, merge and apply.                                          |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**The law and its kit, rendered, installed, guarded and delivered, every step under test.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
