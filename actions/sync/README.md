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

## 💡 What It Does

It runs `scripts/sync.py apply` from the hub tree GitHub downloaded at the
tag, in the calling repository's checkout. An `AGENTS.md` with a block gets
the release's block in its place; one without gets it after its header; a
repository with none gets a new `AGENTS.md`, and any `CLAUDE.md` is folded
in and deleted. A template, a fork, an archived repository, one with the
`no-intelligence` topic and the hub itself are left alone.

It changes the working tree and nothing else: no commit, no push, no pull
request. [`sync.yml`](../../.github/workflows/sync.yml) hands its outputs to
the standards' open-pr action, which does those.

| Input     | Default  | What it is                                                                                        |
| :-------- | :------- | :------------------------------------------------------------------------------------------------ |
| `token`   | required | Reads the repository's settings, to skip what takes no part; the default `GITHUB_TOKEN` is enough |
| `dry-run` | `false`  | Print what would change, and change nothing                                                       |

| Output         | What it is                                                               |
| :------------- | :----------------------------------------------------------------------- |
| `changed`      | `'true'` when the working tree now holds a change to propose             |
| `commit-title` | The Conventional Commit title, which is also the pull request's title    |
| `commit-body`  | Why the change is made, with no sign-off: whoever commits it signs off   |
| `pr-title`     | The pull request title                                                   |
| `pr-body`      | The pull request body, which says how its checks start and who merges it |

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
