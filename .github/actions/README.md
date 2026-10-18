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

The composite action a repository's 🔁 Intelligence Sync stub runs, through
the reusable workflow [`sync.yml`](../workflows/sync.yml). Nothing
here is called directly. How it fits: [Repository
Sync](../../docs/technical/Repository-Sync.md).

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
