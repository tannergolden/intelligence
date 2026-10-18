<!--
title: '🎯 SKILL TRIGGER TESTS'
description: 'One trigger test per skill: prompts that should load it, near misses that should not, and the tasks that judge its output.'
tags: [evals, skills, triggers, descriptions]
category: docs
-->

<div align="center">

# 🎯 SKILL TRIGGER TESTS

<a name="top"></a>

**Whether each skill loads when it should, and stays out of the way when it should not.**

_Load on the right prompt. Stay quiet on the near miss._

</div>

---

## 💡 What This Folder Is For

A skill is only as good as its description, because the description is all
that triggers it. Each file here is named for its skill and holds:

- `should_trigger`: prompts that should load the skill, in varied wording;
- `should_not_trigger`: near misses that should not;
- `runs` and `threshold`: each prompt runs at least three times, and passes
  when the skill loads in at least that share of runs;
- `quality`: real tasks to run with the skill and without it.

`make evals ARGS='--apps claude --skill <name>'` runs one. The tests live
here rather than in the skill's folder, so they never ship with it, and
`make lint` fails while a skill has none.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                          | Purpose                                                                                                   |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| [`building-skills.json`](building-skills.json) | The trigger test for building-skills: when it should load, when it should not, and a task to judge it by. |
| [`README.md`](README.md)                       | This file.                                                                                                |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A description that triggers right, proven every release.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
