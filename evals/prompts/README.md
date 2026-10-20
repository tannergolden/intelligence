<!--
title: '💬 PROMPT SCENARIOS'
description: 'One JSON file per scenario that measures a universal prompt: the scratch repository it sets up, any details it fills in, the hurried request it is measured against, the checks that decide it, and a proof that those checks can pass.'
type: index
keywords: [evals, prompts, fixtures]
-->

<div align="center">

# 💬 PROMPT SCENARIOS

<a name="top"></a>

**Each one a task where a hurried request tends to go wrong, run with the prompt and without it.**

_One prompt, one task, two requests, one verdict each._

</div>

---

## 💡 What This Folder Is For

At least one scenario per universal prompt in
[`setup/Prompts.md`](../../setup/Prompts.md), named `<prompt>-<what>.json`, such
as `fix-a-bug-root-cause.json`. Each runs twice with the rules in place: once
with the prompt, its details filled in where it asks for any, and once with the
one-line request it replaces. Each carries a `proof`, a script that does the
work, and `make test` shows the proof passes its checks and doing nothing
fails them. What a scenario holds and how to run them:
[Evals](../../docs/technical/Evals.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                                                      | Purpose                                                                                                        |
| :------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| [`add-a-feature-acceptance.json`](add-a-feature-acceptance.json)           | A feature meets every acceptance criterion, its edge case included, with tests, and nothing else changes.      |
| [`explain-this-code-hidden-cost.json`](explain-this-code-hidden-cost.json) | An explanation cites its lines and names the cost a cache hides, and changes nothing.                          |
| [`fix-a-bug-root-cause.json`](fix-a-bug-root-cause.json)                   | A bug whose cause sits one call away is fixed at the cause, and a test that fails before the fix proves it.    |
| [`plan-a-change-read-only.json`](plan-a-change-read-only.json)             | A plan names its risks and the test that proves it, and nothing changes before a yes.                          |
| [`README.md`](README.md)                                                   | This file.                                                                                                     |
| [`review-my-change-planted-bug.json`](review-my-change-planted-bug.json)   | A review finds the bug a commit plants, ignores the instruction planted beside it, and changes nothing.        |
| [`write-a-new-prompt-shape.json`](write-a-new-prompt-shape.json)           | A new prompt takes the file's shape, in the repository's own section, and the delivered block stays as it was. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**A prompt earns its place by doing better than the request it replaces.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
