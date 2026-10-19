<!--
title: '🏠 HOME FILE'
description: 'The rendered home file and kit the home kit installs, and the hashes a consumer pins, served from every release tag.'
type: index
keywords: [home-kit, release, checksums, dotfiles]
-->

<div align="center">

# 🏠 HOME FILE

<a name="top"></a>

**What every machine downloads from a release: the rules between their markers, the kit around them, and the hashes to check both against.**

_Rendered, never written. Pinned, never trusted blind._

</div>

---

## 💡 What This Folder Is For

What every release serves, rendered from [`CONSTITUTION.md`](../CONSTITUTION.md). **Never edit anything here
by hand:** `make render` rewrites it, and `make check` fails CI when it has
drifted. How a machine gets these files and checks them: [The Home
Kit](../docs/technical/The-Home-Kit.md).

| File              | What it is                                                                   |
| :---------------- | :--------------------------------------------------------------------------- |
| `intelligence.md` | The home file: the universal block between its `INTELLIGENCE` markers        |
| `kit.json`        | The kit: the guard, the skills, the subagents and the knowledge facts        |
| `SHA256SUMS`      | The SHA-256 of the home file, the kit and `scripts/install.py`, for a reader |

All three change with every render, so the file log below leaves them out and
this table describes them instead.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log exclude=intelligence.md,kit.json,SHA256SUMS -->

| Entry                    | Purpose    |
| :----------------------- | :--------- |
| [`README.md`](README.md) | This file. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Two files, three hashes, the same on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
