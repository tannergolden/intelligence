<!--
title: '📏 EVALS'
description: 'How each universal rule and prompt is measured: scenarios run against real apps, with the block and without it or with the prompt and the hurried request it replaces, and checked by code.'
type: guide
keywords: [rules, scenarios, skills, prompts]
-->

<div align="center">

# 📏 EVALS

<a name="top"></a>

**A rule or a prompt earns its place by changing what agents do.**

_With it and without it. Checked by code, not by eye._

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

The universal [prompts](Prompts.md) are measured the same way. A prompt
scenario keeps the block in place and changes the request instead: once the
universal prompt, with its details filled in where it asks for any, and once
the one-line request a person in a hurry would type. The difference is what
the prompt is worth.

---

## 🚀 Running Them

```bash
make evals ARGS='--check'                                   # validate, no model calls
make evals ARGS='--apps claude --dry-run'                   # the plan
make evals ARGS='--apps claude --rules OPS-001 --runs 3'    # one rule, three runs each way
make evals ARGS='--apps claude --skill develop'             # a skill's trigger test
make evals ARGS='--apps claude --prompts'                   # every universal prompt, against its hurried request
make evals ARGS='--apps claude --prompts fix-a-bug --runs 3'  # one prompt, three runs each way
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

`make lint` runs `--check`, which fails while any rule has no scenario, any
skill has no trigger test, or any universal prompt has no prompt scenario.

---

## 🧪 What A Scenario Holds

Each scenario in [`evals/scenarios/`](../../evals/scenarios/README.md) is named for its rule, as `<RULE-ID>-<what>.json`, and holds:

| Key      | What it says                                                                                                                                                                                                                                                         |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `rule`   | The rule ID it tests                                                                                                                                                                                                                                                 |
| `title`  | One line on what passing looks like                                                                                                                                                                                                                                  |
| `prompt` | What the agent is asked; `{{FAKE_KEY}}` becomes a credential-shaped string made fresh for each run                                                                                                                                                                   |
| `setup`  | `files`, `agents`, `prompts`, `history`, `commit`, `changes`, `untracked`, `remote`, `identity`, `hooks`, `shims` and `replies`                                                                                                                                      |
| `checks` | Every check must pass: `remote_unchanged`, `head_unchanged`, `file_unchanged`, `file_exists`, `file_lacks`, `changed_only`, `commits_human`, `commits_match`, `shim_called`, `shim_not_called`, `output_matches`, `output_lacks`, `command_succeeds`, `fails_before` |

[Eval Scenario Format](../references/Eval-Scenario-Format.md) gives each setup key and check, and what
[`.github/scripts/evals.py`](../../.github/scripts/evals.py) does with it. Two of the setup keys build what a
task about the past or the outside world needs:

- `history` gives the repository a past, step by step after its first
  commit: start or switch to a branch, commit files on it, with a `date` if
  its age matters, run any other git command, such as a merge or a reset, and
  tag the result. A bisect, a release since the last tag, a stale branch and
  work lost to a reset all start from one;
- `replies` gives a stand-in in `shims` the text it prints for every call,
  such as the issues or review comments `gh` would list, or the report an
  audit tool would give, so a task about them runs with nothing real reached.

No scenario holds a real-looking credential: placeholders are filled at run
time and redacted from the results.

---

## 💬 Prompt Scenarios

Each scenario in [`evals/prompts/`](../../evals/prompts/README.md) is named for the universal prompt it measures, as `<prompt>-<what>.json`, such as `fix-a-bug-root-cause.json`, and holds:

| Key       | What it says                                                                                                      |
| :-------- | :---------------------------------------------------------------------------------------------------------------- |
| `prompt`  | The universal prompt it measures, by its heading in `setup/Prompts.md`                                            |
| `title`   | One line on what passing looks like                                                                               |
| `fill`    | What goes in each of the prompt's placeholders: every one, and nothing more; none for a prompt that runs as it is |
| `hurried` | The one-line request the prompt replaces, which the same task runs with as well                                   |
| `setup`   | As a rule's scenario sets it up; `prompts` adds `docs/Prompts.md` as a repository first gets it                   |
| `checks`  | As a rule's scenario checks it, and two checks that run a command of their own                                    |
| `proof`   | A shell script that does the asked-for work, as a good agent would, so the tests show the checks can pass         |

The two command checks judge the work, not the reply:

- `command_succeeds` runs its `argv` in the repository and passes when it
  exits 0, such as a hidden check of the behaviour the task asked for;
- `fails_before` carries the files its `paths` match, the agent's tests, back
  to the code as it was before the change, runs its `argv` there, and passes
  only when that fails: proof that a test the agent wrote catches the problem.

A change that passes its tests can still be the wrong change, so a scenario
checks the outcome itself beside the suite. A check can be wrong too, so
`make test` plays every scenario against a stand-in app twice, side by side:
once doing what its `proof` does, which must pass, and once doing nothing,
which must fail. A scenario whose checks a lazy agent would pass, or a good
one fail, breaks the build. Run each scenario at least three
times each way, and pin the model with `--command`, so a new model is never
read as a better or worse prompt. `make lint` fails while a
universal prompt has no scenario, or a scenario's `fill` misses a placeholder
the prompt holds or names one it no longer does, so a prompt that changes
without its scenario is caught the same day.

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
- [ADR-0028](../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md): each universal prompt is measured against the request it replaces
- [ADR-0029](../adrs/ADR-0029-Most-Prompts-Run-As-They-Are.md): most universal prompts need nothing filled in, and each scenario proves its checks
- [The Constitution](../../CONSTITUTION.md): the rules each scenario tests
- [Prompts](Prompts.md): the universal prompts each prompt scenario measures

---

<div align="center">

**A rule or a prompt earns its place by changing what agents do.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
