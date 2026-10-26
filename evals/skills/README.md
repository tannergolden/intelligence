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

| Entry                              | Purpose                                                                                                   |
| :--------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| [`develop.json`](develop.json)     | The trigger test for develop: when it should load, when it should not, and a task to judge it by.         |
| [`discover.json`](discover.json)   | The trigger test for discover, taken from its assets/trigger-evals.json by .github/scripts/faculties.py.  |
| [`editorial.json`](editorial.json) | The trigger test for editorial, taken from its assets/trigger-evals.json by .github/scripts/faculties.py. |
| [`finance.json`](finance.json)     | The trigger test for finance, taken from its assets/trigger-evals.json by .github/scripts/faculties.py.   |
| [`README.md`](README.md)           | This file.                                                                                                |
| [`research.json`](research.json)   | The trigger test for research, taken from its assets/trigger-evals.json by .github/scripts/faculties.py.  |
| [`visualize.json`](visualize.json) | The trigger test for visualize, taken from its assets/trigger-evals.json by .github/scripts/faculties.py. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A description that triggers right, proven every release.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
