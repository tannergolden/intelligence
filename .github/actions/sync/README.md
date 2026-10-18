<!--
title: '🔁 INTELLIGENCE SYNC ACTION'
description: 'Writes the universal rules of the release it is called at into the calling repository''s AGENTS.md, for 🔁 Intelligence Sync to propose as a pull request.'
tags: [github-actions, composite-action, sync, agents-md]
category: docs
-->

<div align="center">

# 🔁 INTELLIGENCE SYNC ACTION

<a name="top"></a>

**The release's block, written into one repository's checkout, and nothing else.**

_It writes. The workflow proposes. You merge._

</div>

---

## 💡 What This Folder Is For

`action.yml` runs `scripts/sync.py apply` from the hub tree GitHub downloads
at the tag, in the calling repository's checkout, and changes the working tree
and nothing else. Its inputs and outputs, and how the workflow uses them:
[Repository Sync](../../../docs/technical/Repository-Sync.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                      | Purpose                                                                                      |
| :------------------------- | :------------------------------------------------------------------------------------------- |
| [`action.yml`](action.yml) | Writes the universal rules of this action's release into the calling repository's AGENTS.md. |
| [`README.md`](README.md)   | This file.                                                                                   |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Written by the release, proposed by the workflow, merged by you.**

[↑ Back to Top](#top)

</div>
