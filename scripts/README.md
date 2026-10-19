<!--
title: '🔧 HUB SCRIPTS'
description: 'The scripts that render the Constitution and the kit, install them on a machine, guard every tool call, and deliver the rules to every repository, with their tests.'
tags: [scripts, render, home-kit, sync]
category: docs
-->

<div align="center">

# 🔧 HUB SCRIPTS

<a name="top"></a>

**Render the Constitution and the kit, install them at home, guard every tool call, deliver the rules everywhere: five scripts and their tests.**

_Standard library only, from a Mac's Python 3.9 up._

</div>

---

## 💡 What This Folder Is For

The hub's Python, standard library only, with a test beside each script. How
each part works: Article VI of [the Constitution](../CONSTITUTION.md) for
`render.py`, [The Home Kit](../docs/technical/The-Home-Kit.md) for `kit.py`,
`install.py` and `guard.py`, and [Repository Sync](../docs/technical/Repository-Sync.md)
for `sync.py`.

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
| [`render.py`](render.py)             | Render the universal rules from the Constitution into every copy this hub publishes.        |
| [`sync.py`](sync.py)                 | Deliver the universal rules to every repository the owner owns, and keep them there.        |
| [`test_develop.py`](test_develop.py) | Tests for the develop skill's validator and packager.                                       |
| [`test_guard.py`](test_guard.py)     | Tests for the guard hook.                                                                   |
| [`test_install.py`](test_install.py) | Tests for the home kit installer.                                                           |
| [`test_kit.py`](test_kit.py)         | Tests for the kit renderer.                                                                 |
| [`test_render.py`](test_render.py)   | Tests for the Constitution renderer.                                                        |
| [`test_sync.py`](test_sync.py)       | Tests for repository sync, audit, merge and apply.                                          |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**The Constitution and its kit, rendered, installed, guarded and delivered, every step under test.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
