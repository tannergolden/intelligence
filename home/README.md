<!--
title: '🏠 HOME FILE'
description: 'Everything a machine downloads from a release, rendered: the home file, the kit and the installer the home kit runs, and the hashes a consumer pins.'
type: index
keywords: [home-kit, release, checksums, dotfiles]
-->

<div align="center">

# 🏠 HOME FILE

<a name="top"></a>

**What every machine downloads from a release: the rules between their markers, the kit around them, the installer that puts both in place, and the hashes to check all three against.**

_Rendered, never written. Pinned, never trusted blind._

</div>

---

## 💡 What This Folder Is For

What every release serves to a machine, rendered from
[`CONSTITUTION.md`](../CONSTITUTION.md), [`kit/`](../kit/README.md) and the
installer's source. **Never edit anything here by hand:** `make render`
rewrites it, and `make check` fails CI when it has drifted. How a machine gets
these files and checks them: [The Home Kit](../docs/technical/The-Home-Kit.md).

| File              | What it is                                                                       |
| :---------------- | :------------------------------------------------------------------------------- |
| `intelligence.md` | The home file: the universal block between its `INTELLIGENCE` markers            |
| `kit.json`        | The kit: the guard, the skills and the subagents, from `kit/`                    |
| `install.py`      | The installer, copied from `.github/scripts/install.py`, where its tests run     |
| `SHA256SUMS`      | The SHA-256 of the home file, the kit and the installer, for a reader            |

Each is the renderer's, so the file log below leaves them out and this table
describes them instead.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log exclude=intelligence.md,kit.json,install.py,SHA256SUMS -->

| Entry                    | Purpose    |
| :----------------------- | :--------- |
| [`README.md`](README.md) | This file. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Three files, three hashes, the same on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
