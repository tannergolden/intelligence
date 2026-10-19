<!--
title: '🧪 EVALS'
description: 'Scenarios that tempt an agent to break each universal rule, run against real apps with the block and without it, and checked by code.'
type: index
keywords: [rules, measurement, scenarios]
-->

<div align="center">

# 🧪 EVALS

<a name="top"></a>

**Proof that each rule changes what an agent does, measured against the same task without it.**

_Tempt, run, check, compare._

</div>

---

## 💡 What This Folder Is For

The evals runner, a scenario for every rule in [`scenarios/`](scenarios/README.md),
and a trigger test for every skill in [`skills/`](skills/README.md). What
evals measure and how to run them: [Evals](../docs/technical/Evals.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                               | Purpose                                                                                                                      |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| [`scenarios/`](scenarios/README.md) | One JSON file per scenario: the rule it tests, the scratch repository it sets up, the prompt, and the checks that decide it. |
| [`skills/`](skills/README.md)       | One trigger test per skill: prompts that should load it, near misses that should not, and the tasks that judge its output.   |
| [`README.md`](README.md)            | This file.                                                                                                                   |
| [`run.py`](run.py)                  | Measure whether the universal rules change what agents do, one scenario per rule.                                            |
| [`test_run.py`](test_run.py)        | Tests for the eval runner.                                                                                                   |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A rule earns its place by changing what agents do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
