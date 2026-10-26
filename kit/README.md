<!--
title: '🧩 KIT'
description: 'The sources of everything the home kit installs besides the rules: the guard hook, the skills and the subagents, rendered into home/kit.json.'
type: index
-->

<div align="center">

# 🧩 KIT

<a name="top"></a>

**Everything the home kit puts beside the rules, kept here as readable sources and shipped as one pinned file.**

_Written here. Rendered once. Installed everywhere._

</div>

---

## 💡 What This Folder Is For

The kit's sources, one entry for each part of `home/kit.json`:
[`guard.py`](guard.py), the hook every app runs before a tool call;
[`skills/`](skills/README.md), `develop` and the faculties, which
[`faculties.json`](faculties.json) pins to a release of the knowledge
template; and [`subagents/`](subagents/README.md), the Worker and the
Reviewer.
`.github/scripts/kit.py` checks each one and bundles them, and `make render`
writes the bundle. What each part does and where it lands: [The Home
Kit](../docs/technical/The-Home-Kit.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                               | Purpose                                                                                                                                                          |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`skills/`](skills/README.md)       | The skills the home kit installs into every AI coding app, each a folder in the open Agent Skills format.                                                        |
| [`subagents/`](subagents/README.md) | The Worker and Reviewer subagents the home kit installs, each one source rendered for Claude Code, Copilot and Codex.                                            |
| [`faculties.json`](faculties.json)  | The faculty skills the home kit carries, each copied from one release of tannergolden/knowledge with its trigger test, and the hashes that hold each copy to it. |
| [`guard.py`](guard.py)              | Block the few tool calls the universal rules forbid outright, before they run.                                                                                   |
| [`README.md`](README.md)            | This file.                                                                                                                                                       |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**One folder of sources, one pinned file on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
