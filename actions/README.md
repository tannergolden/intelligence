<!--
title: '🎬 ACTIONS'
description: 'The composite action that carries the hub''s own code into every repository whose stub asks for it, at the hub''s latest release.'
tags: [github-actions, composite-action, sync, intelligence]
category: docs
-->

<div align="center">

# 🎬 ACTIONS

<a name="top"></a>

**The hub's code, carried into each repository that asks for it, at the latest release.**

_Called, never copied._

</div>

---

## 💡 What This Folder Is For

A workflow step runs only code its repository already has. A repository's
🔁 Intelligence Sync stub needs the hub's code, so the reusable workflow
[`sync.yml`](../.github/workflows/sync.yml) calls the action here, and GitHub
downloads the hub at its moving major tag. The action runs
`scripts/sync.py` from that download against the repository's own checkout,
so the code that writes the block is always a released one, the same that
`make sync` runs.

Nothing here is meant to be called directly. A repository calls the
workflow, through the stub in [`setup/`](../setup/README.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                     | Purpose                                                                                                                                                          |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`sync/`](sync/README.md) | Writes the universal rules of the release it is called at into the calling repository's AGENTS.md, for &#x1F501; Intelligence Sync to propose as a pull request. |
| [`README.md`](README.md)  | This file.                                                                                                                                                       |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**One copy of the code, reaching every repository at its release.**

[↑ Back to Top](#top)

</div>
