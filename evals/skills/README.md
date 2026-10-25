<!--
title: '🎯 SKILL TRIGGER TESTS'
description: 'One trigger test per skill: prompts that should load it, near misses that should not, and the tasks that judge its output.'
type: index
-->

<div align="center">

# 🎯 SKILL TRIGGER TESTS

<a name="top"></a>

**Whether each skill loads when it should, and stays out of the way when it should not.**

_Load on the right prompt. Stay quiet on the near miss._

</div>

---

## 💡 What This Folder Is For

One trigger test per skill, named for the skill, kept here so it never ships
with it. What each test holds: [Evals](../../docs/technical/Evals.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                          | Purpose                                                                                           |
| :----------------------------- | :------------------------------------------------------------------------------------------------ |
| [`develop.json`](develop.json) | The trigger test for develop: when it should load, when it should not, and a task to judge it by. |
| [`README.md`](README.md)       | This file.                                                                                        |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A description that triggers right, proven every release.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
