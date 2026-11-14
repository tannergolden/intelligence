<!--
title: '🧩 KIT'
description: 'The source of everything the home kit installs besides the rules: the guard hook, rendered into home/kit.json.'
type: index
-->

<div align="center">

# 🧩 KIT

<a name="top"></a>

**Everything the home kit puts beside the rules, kept here as a readable source and shipped as one pinned file.**

_Written here. Rendered once. Installed everywhere._

</div>

---

## 💡 What This Folder Is For

The kit's source: [`guard.py`](guard.py), the hook every app runs before a
tool call. The kit carries no skills and no subagents
([ADR-0041](../docs/adrs/ADR-0041-The-Kit-Carries-No-Skills.md)).
`.github/scripts/kit.py` checks the guard and bundles it, and `make render`
writes the bundle. What it does and where it lands: [The Home
Kit](../docs/technical/The-Home-Kit.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                    | Purpose                                                                        |
| :----------------------- | :----------------------------------------------------------------------------- |
| [`guard.py`](guard.py)   | Block the few tool calls the universal rules forbid outright, before they run. |
| [`README.md`](README.md) | This file.                                                                     |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**One folder of sources, one pinned file on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
