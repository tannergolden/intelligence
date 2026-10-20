<!--
title: '⌨️ COMMANDS'
description: 'Every make target and script option, and what each one reaches: your gh login, model calls, your home folder or nothing beyond the checkout. Read it before running a command for the first time, or to find an option to pass through ARGS.'
type: reference
keywords: [makefile, scripts, options, flags, exit-codes, environment]
-->

<div align="center">

# ⌨️ COMMANDS

<a name="top"></a>

**Every command the hub offers, with what it touches before you run it.**

_Know what it reaches before you press enter._

</div>

---

## 💡 How To Read This Page

Run every command from the hub's root. Each one is plain Python from the
standard library, except that the repository validator also needs PyYAML,
which `make setup` installs. The **Reaches** column says what a command touches
beyond the checkout: GitHub through your own `gh` login, model calls on your
own subscriptions, or the files in your home folder.

> [!IMPORTANT]
> **`make sync` and `make merge` change other repositories.** Running them
> against real repositories, like cutting a release, is on the
> [Ask first](../../AGENTS.md#ask-first) list for an agent.

---

## ⚙️ The Make Targets

| Target             | Runs                                                                                    | Reaches                                                                                              |
| :----------------- | :-------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| `make help`        | Lists every target with its summary                                                     | Nothing                                                                                              |
| `make setup`       | `pip install pyyaml==6.0.3`, for the repository validator; CI runs it first             | The Python package index                                                                             |
| `make check`       | `make lint`, then `make test`: everything CI checks                                     | Nothing                                                                                              |
| `make lint`        | `validate-repository.py`, `render.py --check`, `prompts.py --check`, `evals.py --check` | Nothing                                                                                              |
| `make test`        | Every `test_*.py` in `.github/scripts/`, through `unittest`                             | Nothing: GitHub and the apps are stand-ins                                                           |
| `make render`      | `render.py --write`, which rewrites `home/`                                             | Nothing                                                                                              |
| `make probe`       | `loader-probe.py` with `ARGS`                                                           | Every installed app, one model call per check, and your home folder, which it restores               |
| `make evals`       | `evals.py` with `ARGS`, which must name `--apps` unless it holds `--check`              | The apps named, one model call per run; nothing with `--check` or `--dry-run`                        |
| `make audit`       | `sync.py audit` with `ARGS`                                                             | Every repository you own, read only                                                                  |
| `make sync`        | `sync.py sync` with `ARGS`                                                              | Every repository you own: moves `chore/intelligence`, commits to it, opens or updates a pull request |
| `make merge`       | `sync.py merge` with `ARGS`                                                             | Every sync pull request: approves or reopens to start held checks, and merges the green ones         |
| `make pins`        | `render.py --pins` for `VERSION`, or for this checkout without it                       | Nothing: it reads the tag from your checkout                                                         |
| `make cloud-setup` | `render.py --setup` for `VERSION`, which it requires                                    | Nothing: it reads the tag from your checkout                                                         |

Four variables change what a target runs:

| Variable         | Default   | What it is                                                              |
| :--------------- | :-------- | :---------------------------------------------------------------------- |
| `ARGS`           | empty     | Options for the script, such as `ARGS='--repo dotfiles --dry-run'`      |
| `VERSION`        | empty     | A release tag, such as `v0.2.0`, for `make pins` and `make cloud-setup` |
| `PYTHON`         | `python3` | The interpreter every target runs                                       |
| `PYYAML_VERSION` | `6.0.3`   | The PyYAML that `make setup` installs                                   |

---

## 🔁 sync.py

`make audit`, `make sync` and `make merge` run its first three commands; the
stub's action runs the fourth. [Repository Sync](../technical/Repository-Sync.md)
explains each.

```bash
python3 .github/scripts/sync.py audit|sync|merge|apply [options]
```

| Option             | With               | What it does                                                                                      |
| :----------------- | :----------------- | :------------------------------------------------------------------------------------------------ |
| `--repo NAME`      | audit, sync, merge | Only this repository; repeat it for more                                                          |
| `--ref REF`        | audit, sync, merge | Use the block of this hub ref, such as `HEAD`, instead of the latest release tag in your checkout |
| `--dry-run`        | sync, merge, apply | Print what would change, and change nothing                                                       |
| `--path DIR`       | apply              | The checkout to write into; the current folder by default                                         |
| `--release REF`    | apply              | The hub ref the tree came from, such as `v0`, named in the pull request's text                    |
| `--hub OWNER/NAME` | apply              | The hub, to find the full version a moving tag points at; `tannergolden/intelligence` by default  |

`apply` refuses to start without `GITHUB_REPOSITORY` set to `owner/name`, which
GitHub Actions sets. It exits 1 when `audit` finds anything in any repository,
when any repository fails during `sync` or `merge`, and when `gh` cannot list
your repositories.

---

## 🏠 install.py

The installer every machine runs from a release: dotfiles' `make agents`,
`make agents-check` and `make agents-uninstall` run its three commands, and the
cloud setup script runs `install --cloud`. To run it by hand, download the
release's files and check them against their pins first, as
[The Home Kit](../technical/The-Home-Kit.md) describes.

```bash
python3 install.py install --home-file intelligence.md --kit-file kit.json
python3 install.py check --home-file intelligence.md --kit-file kit.json
python3 install.py uninstall --dry-run
```

| Option             | With               | What it does                                                                             |
| :----------------- | :----------------- | :--------------------------------------------------------------------------------------- |
| `--home-file FILE` | install, check     | The release's home file; required                                                        |
| `--kit-file FILE`  | install, check     | The release's `kit.json`; without it, the rules alone are installed or checked           |
| `--cloud`          | install, check     | A Claude Code cloud session: Claude Code's files only, and no `instructionFiles` setting |
| `--home DIR`       | every command      | The home folder to work in; yours by default                                             |
| `--dry-run`        | install, uninstall | Print the plan, and change nothing                                                       |

`install` exits 1 when it refused anything, and `check` when anything is not
`current`. What each status means:
[Troubleshooting The Home Kit](../operations/Troubleshooting-The-Home-Kit.md).

---

## 🧪 evals.py

`make evals` runs it. [Evals](../technical/Evals.md) shows the usual runs, and
[Eval Scenario Format](Eval-Scenario-Format.md) what a scenario holds.

| Option                          | What it does                                                                                                                                        |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--check`                       | Validate every scenario and trigger test, then stop, with no model calls                                                                            |
| `--apps LIST`                   | Comma-separated: `claude`, `codex`, `copilot`, or any app given a `--command`. Required to run                                                      |
| `--rules IDS`                   | Comma-separated rule IDs to run; all of them by default                                                                                             |
| `--skill NAME`                  | Run that skill's trigger test instead of the scenarios                                                                                              |
| `--prompts [NAMES]`             | Run the prompt scenarios instead: all of them, or comma-separated names such as `fix-a-bug`; `with` is the prompt and `without` the hurried request |
| `--condition both/with/without` | Which conditions to run; `both` by default                                                                                                          |
| `--runs N`                      | Runs per scenario and condition, 1 by default; a trigger test runs each prompt at least 3 times                                                     |
| `--timeout SECONDS`             | Time allowed per model call; 600 by default                                                                                                         |
| `--command 'APP=ARGV'`          | An app's headless command, holding `{prompt}`; repeat it for more apps                                                                              |
| `--seen 'APP=REGEX'`            | How an app's output shows it loaded a skill, with `{name}` for the skill's name                                                                     |
| `--dry-run`                     | Print the plan and the number of model calls, and call none                                                                                         |
| `--keep`                        | Keep each scratch folder, and print where it is                                                                                                     |
| `--out FILE`                    | Where the results go; `~/.cache/intelligence-evals/results-<time>.json` by default                                                                  |

A scenario run exits 1 when any run with the block fails, and a prompt
scenario run when any run with the prompt fails; the runs without them never
fail the command. A trigger test exits 1 when any prompt fails.

---

## 🔬 loader-probe.py

`make probe` runs it. [The Loader Probe](../technical/The-Loader-Probe.md)
explains each check and what it touches.

| Option                 | What it does                                                                                                           |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `--apps LIST`          | Comma-separated, from `claude`, `codex`, `antigravity`, `copilot`, `grok` and `cursor`; every installed one by default |
| `--dry-run`            | Print the plan, and change nothing                                                                                     |
| `--skills`             | Add the skill canary: one more model call per app                                                                      |
| `--keep`               | Write the files and fixtures for a check by hand, and leave them until `--cleanup`                                     |
| `--cleanup`            | Restore what `--keep`, or a run that died, left behind                                                                 |
| `--command 'APP=ARGV'` | Replace an app's command; it must keep `{prompt}`                                                                      |
| `--timeout SECONDS`    | Time allowed per model call; 240 by default                                                                            |
| `--home DIR`           | The home folder to probe; yours by default                                                                             |
| `--state DIR`          | Where the manifest and the results go; `~/.cache/intelligence-probe/` by default                                       |

It exits 1 when a check fails or none of the apps is installed, and 2 when an
earlier run's manifest is still there, until `--cleanup` replays it.

---

## ⚖️ render.py, kit.py & prompts.py

The scripts that build what the hub ships. `make render` runs
`render.py --write`, `make lint` runs `render.py --check` and
`prompts.py --check`, and `render.py` calls `kit.py` itself.

| Command                  | What it does                                                                                                                        |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `render.py`              | Print the block                                                                                                                     |
| `render.py --write`      | Rewrite every file in `home/` that differs from what the sources render, unless `--check` would fail on the Constitution or the kit |
| `render.py --check`      | Fail on a Constitution that breaks its Article VI, a kit problem, or a stale file in `home/`, and print the block's size            |
| `render.py --pins [REF]` | Print the four pin lines for a tag, or for this checkout without one                                                                |
| `render.py --setup REF`  | Print the cloud setup script with the pins of that tag filled in                                                                    |
| `kit.py`                 | Print the bundle `home/kit.json` would hold                                                                                         |
| `kit.py --check`         | List every problem in `kit/`                                                                                                        |
| `prompts.py`             | Print `docs/Prompts.md` as a repository first gets it, sealed                                                                       |
| `prompts.py --check`     | Fail on a broken `setup/Prompts.md`                                                                                                 |

Each is `python3 .github/scripts/<name>`, and each exits 1 on a problem.

---

## 🛡️ guard.py

Every app's pre-tool hook pipes its call to the guard as JSON, naming itself
with `--app`. To see what it says about one command, run it by hand: in the hub
as `kit/guard.py`, or on a machine with the kit as
`~/.agents/hooks/intelligence-guard.py`.

```bash
python3 kit/guard.py --command 'git push --force origin main'
python3 kit/guard.py --remind
```

| Option           | What it does                                                                                                                                                                    |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--app NAME`     | The app whose hook calls it: `claude`, `codex`, `copilot` or `antigravity`                                                                                                      |
| `--command TEXT` | Check one shell command by hand. It prints `allowed`, or the denial on stderr with exit 2                                                                                       |
| `--remind`       | Print the Invariants from Claude Code's home copy of the rules, as the compaction hook does; nothing when that copy is missing, or when the payload names another session start |

---

## 🧰 The develop Skill's Scripts

The skill carries its own validator and packager, which work from any
repository; their docstrings give every option.

```bash
python3 kit/skills/develop/scripts/validate.py skill kit/skills/develop
python3 kit/skills/develop/scripts/package.py kit/skills/develop --dry-run
```

`validate.py` checks a `skill`, an `agent`, a `team` or a `library`, and exits
1 on an error and 2 on bad usage. `package.py` builds `<name>.skill` in the
folder `--out` names, the current one by default, and exits 1 when the skill
fails validation or its team cannot be found.

---

## 🌿 Environment Variables

| Variable            | Read by                             | What it changes                                                                                                                                       |
| :------------------ | :---------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GITHUB_REPOSITORY` | `sync.py apply`                     | The repository it writes for, as `owner/name`; required                                                                                               |
| `GH_TOKEN`          | `gh`, in the sync action            | The token `gh` uses in a stub's run; the action sets it from its `token` input                                                                        |
| `XDG_STATE_HOME`    | `install.py`                        | Where the install record goes, in place of `~/.local/state`                                                                                           |
| `XDG_CACHE_HOME`    | `loader-probe.py`, `evals.py`       | Where the probe's manifest and results, and the eval results, go, in place of `~/.cache`                                                              |
| `CODEX_HOME`        | `install.py`, `kit/guard.py`        | Where Codex keeps its files, in place of `~/.codex`                                                                                                   |
| `INTELLIGENCE_BASE` | `setup/claude-cloud-setup.sh`       | Where the release is downloaded from, in place of `https://raw.githubusercontent.com/tannergolden/intelligence`; the tests point it at a local folder |
| `GITHUB_OUTPUT`     | `sync.py apply`                     | Set by GitHub Actions: where `apply` hands its outputs to the workflow                                                                                |
| `GITHUB_ACTIONS`    | `sync.py`, `validate-repository.py` | Set by GitHub Actions: problems print as annotations, which the validator places on the file and line                                                 |

---

## 🔗 See Also

- [Agent Instructions](../../AGENTS.md): which commands a change needs before it is done
- [Releasing](../distribution/Releasing.md): the commands of a release, in order
- [Glossary](Glossary.md): the terms these commands use

---

<div align="center">

**Read the row, then run the command.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
