<!--
title: '📏 EVALS'
description: 'How each universal rule is measured: scenarios that tempt an agent to break it, run against real apps with the block and without it, and checked by code.'
tags: [evals, rules, scenarios, skills]
category: docs
-->

<div align="center">

# 📏 EVALS

<a name="top"></a>

**A rule earns its place by changing what agents do.**

_With the block and without it. Checked by code, not by eye._

</div>

---

## 💡 What Evals Measure

The [loader probe](The-Loader-Probe.md) proves an app reads the rules. Evals
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

## 🧪 What A Scenario Holds

Each scenario in [`evals/scenarios/`](../../evals/scenarios/README.md) is named for its rule, as `<RULE-ID>-<what>.json`, and holds:

| Key      | What it says                                                                                                                                                                                                                     |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rule`   | The rule ID it tests                                                                                                                                                                                                             |
| `title`  | One line on what passing looks like                                                                                                                                                                                              |
| `prompt` | What the agent is asked; `{{FAKE_KEY}}` becomes a credential-shaped string made fresh for each run                                                                                                                               |
| `setup`  | `files`, `agents`, `commit`, `changes`, `untracked`, `remote`, `identity`, `hooks` and `shims`                                                                                                                                   |
| `checks` | Every check must pass: `remote_unchanged`, `head_unchanged`, `file_unchanged`, `file_exists`, `file_lacks`, `changed_only`, `commits_human`, `commits_match`, `shim_called`, `shim_not_called`, `output_matches`, `output_lacks` |

[`evals/run.py`](../../evals/run.py) documents each setup key and check. No scenario
holds a real-looking credential: placeholders are filled at run time and
redacted from the results.

---

## 🎯 Skill Trigger Tests

A skill is only as good as its description, because the description is all
that triggers it. Each file in [`evals/skills/`](../../evals/skills/README.md) is named for its skill and holds:

- `should_trigger`: prompts that should load the skill, in varied wording;
- `should_not_trigger`: near misses that should not;
- `runs` and `threshold`: each prompt runs at least three times, and passes
  when the skill loads in at least that share of runs;
- `quality`: real tasks to run with the skill and without it.

`make evals ARGS='--apps claude --skill <name>'` runs one. The tests live
there rather than in the skill's folder, so they never ship with it, and
`make lint` fails while a skill has none.

---

## 🔗 See Also

- [ADR-0018](../adrs/ADR-0018-Evals-Measure-The-Block.md): evals measure each rule with the block and without it
- [The Law](The-Law.md): the rules each scenario tests

---

<div align="center">

**A rule earns its place by changing what agents do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
