<!--
title: '🧪 EVALS'
description: 'Scenarios that tempt an agent to break each universal rule, run against real apps with the block and without it, and checked by code.'
tags: [evals, rules, measurement, scenarios]
category: docs
-->

<div align="center">

# 🧪 EVALS

<a name="top"></a>

**Proof that each rule changes what an agent does, measured against the same task without it.**

_Tempt, run, check, compare._

</div>

---

## 💡 What This Folder Is For

The [loader probe](../probe/README.md) proves an app reads the rules. Evals
measure whether the agent then follows them. Each scenario sets up a scratch
git repository that tempts an agent to break one rule, gives a real app the
prompt headless, and checks the outcome with code:

- the repository and its files, and a local bare remote standing in for
  GitHub;
- what `gh` and `curl` were asked to do, through stand-ins that log their
  arguments and reach nothing;
- for the few rules only a reply can show, the agent's reply, which those
  scenarios mark as approximate.

Every scenario runs **with** the INTELLIGENCE block in the repository's
`AGENTS.md` and **without** it, and the summary prints both pass rates and
the difference.

---

## 🚀 Running Them

```bash
make evals ARGS='--check'                                   # validate, no model calls
make evals ARGS='--apps claude --dry-run'                   # the plan
make evals ARGS='--apps claude --rules OPS-001 --runs 3'    # one rule, three runs each way
make evals ARGS='--apps claude --skill building-skills'     # a skill's trigger test
```

Claude Code, Codex and Copilot CLI have commands built in; give any other
app one with `--command 'APP=argv with {prompt}'`.

> [!WARNING]
> **Agents run with the permissions their command gives them.** Scenarios
> stay inside their scratch folder, but run evals on a machine where the
> home kit's guard hook is installed, and read a scenario before you run it.

Each scenario's own `//` line says what it tests, and `--keep` leaves its
scratch folder in place to inspect afterwards.

> [!NOTE]
> **The without runs remove the block from the repository only.** Home
> copies installed by the kit still load. For a true baseline, run
> `make agents-uninstall` in dotfiles first; the runner warns when it finds
> them.

`make lint` runs `--check`, which fails while any rule has no scenario or
any skill has no trigger test.

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
