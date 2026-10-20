<!--
title: '🤝 CONTRIBUTING'
description: 'How to work in the intelligence hub, for people and AI agents alike: its commands, what done means, its conventions, where things live and what to ask first.'
type: guide
keywords: [agents, commands, conventions]
-->

<div align="center">

# 🤝 CONTRIBUTING

<a name="top"></a>

**How to work in the hub that writes the rules for every other repository.**

_Read this before your first commit here._

</div>

---

## 💡 Before You Start

This hub holds the universal rules, in [`CONSTITUTION.md`](../CONSTITUTION.md),
and keeps no `AGENTS.md` of its own: every other repository carries a copy of
the rules, and this one carries the source. Agents working here get the rules
from their home copies, which dotfiles installs on a machine and the
[cloud setup script](../docs/technical/Cloud-Setup.md) writes into a Claude
cloud session, and get this page through POL-001 before their first commit.

Everything this page does not cover follows
[tannergolden/standards](https://github.com/tannergolden/standards): branches,
commit messages, sign-offs and pull requests.

---

## 🛠️ Commands

- `make setup`: install PyYAML, which the repository validator in `make lint` needs. CI runs it before the checks.
- `make check`: everything CI checks, which are the repository validator, `render.py --check`, `prompts.py --check`, `evals.py --check` and every test.
- `make test`: the tests alone, every `test_*.py` in `.github/scripts/`.
- `make render`: rewrite `home/` from `CONSTITUTION.md`, the kit's sources in `kit/` and the installer.
- `make probe`: prove which instruction files each installed app loads. It makes one model call per check.
- `make evals`: measure each rule with the block and without it, and each universal prompt against the hurried request it replaces. Real runs make model calls; `ARGS=--dry-run` makes none.
- `python3 kit/guard.py --command '<command>'`: see what the guard hook would say about one command.
- `make audit`, `make sync` and `make merge`: reach every repository the owner owns, through the owner's `gh` login. `make merge` also starts the checks a stub's pull request waits on.

---

## ✅ Definition Of Done

- `make check` passes, and its output is in your report.
- A change to `CONSTITUTION.md`, anything in `kit/` or `.github/scripts/install.py` is followed by `make render`, and the rendered files are committed with it.
- A new rule gets a scenario in `evals/scenarios/`, a new skill a trigger test in `evals/skills/`, and a new universal prompt a scenario in `evals/prompts/`.
- A change to `setup/Prompts.md` stays as Prettier writes it, with the standards' configuration, and passes `prompts.py --check`; a reworded prompt brings its scenario in `evals/prompts/` along.
- Every new script has tests beside it, and every folder's `README.md` logs its files, except inside a skill's folder.
- A change to how something works updates its document in `docs/` in the same commit, in the folder for its kind: `docs/technical/` for how a part works, `docs/distribution/` for how a release ships, `docs/operations/` for the controls and risks.

---

## 📐 Conventions

- Python uses the standard library only, with `from __future__ import annotations` and single quotes. Tests use `unittest`, are named `test_*.py`, and load the script they test with `importlib`.
- `install.py`, `loader-probe.py` and `kit/guard.py` run on the Python 3.9 that macOS ships, so none of them uses `match` or a runtime `X | Y`.
- Skill and subagent files open with the `---` frontmatter their loaders need, with no Document Styling header or footer.
- A rule is one ASCII sentence, quoted under its ID in `CONSTITUTION.md`, whose Article VI sets the format. IDs are `DOMAIN-NNN` and are never reused: its appendix lists the retired ones.
- Every explanation lives in `docs/`. A folder's `README.md` says what the folder holds in a sentence or two, links the document that explains it, and logs its files.

---

## 🗂️ Where Things Live

| Path                                    | What                                                                                                                                            |
| :-------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CONSTITUTION.md`](../CONSTITUTION.md) | The source of every rule, and the order and budget of the block                                                                                 |
| `kit/`                                  | The kit's sources: the guard, the one skill `develop` and its team, and the Worker and Reviewer subagents                                       |
| `home/`                                 | Everything a machine downloads, rendered: the home file, the kit, the installer and their hashes, which every release tag serves                |
| `evals/`                                | Scenarios for every rule and every universal prompt, and the skill trigger tests                                                                |
| `setup/`                                | The Claude cloud setup script, the stub a repository carries, and the prompts every repository gets                                             |
| `.github/scripts/`                      | Every script, with its test beside it: `render.py`, `kit.py`, `install.py`, `sync.py`, `evals.py`, `loader-probe.py`, and the template's checks |
| `.github/actions/`                      | The action a repository's stub runs, through `.github/workflows/sync.yml`                                                                       |
| `docs/introduction/`                    | Where to start: `How-It-Works.md`, which shows how the pieces fit, and the roadmap                                                              |
| `docs/distribution/`                    | Every step of a release, from a green `Development` to every machine and repository                                                             |
| `docs/technical/`                       | How every part of the hub works, one document each                                                                                              |
| `docs/operations/`                      | The controls and risks behind the rules                                                                                                         |
| `docs/references/`, `docs/library/`     | Pages to look up, and material to learn from, as the standards keep them; empty so far                                                          |
| `docs/adrs/`                            | Every decision behind the plan                                                                                                                  |

---

## ⚠️ Gotchas

- Never edit inside `home/`. It is rendered, and `make check` fails on a hand edit.
- The guard hook denies a commit git would author as an AI. In a cloud session, pass `--author` and `--trailer 'Signed-off-by: ...'` with your user's identity, never `-s`.
- Changing `CONSTITUTION.md` changes nothing elsewhere until a release: other repositories receive the rules only through one, which their stub or `make sync` delivers.
- `sync.py`, `render.py`, `kit.py` and `prompts.py`, and `setup/Prompts.md`, also run or are read inside every repository that carries the stub, at the hub's latest release, from the archive GitHub serves. Cut Release refuses a tag without them, `.gitattributes` keeps `.github/scripts/` in that archive, and `test_stub.py` holds both.
- `setup/Prompts.md` keeps its `INTELLIGENCE:PROMPTS` markers unsealed: sync seals them as it delivers the file, and a hash in the source fails `make check`.
- Never add an `AGENTS.md` or a `CLAUDE.md` here. The hub holds the source of the rules; a copy beside it would be a second source.

---

## ✋ Ask First

- Cutting a release, running `make sync` or `make merge` against real repositories, or running a repository's 🔁 Intelligence Sync.
- Adding a universal skill: the owner keeps one, `develop`. A skill one repository needs lives in that repository.
- Changing a rule's wording, its kind or its ID.
- Adding, removing or rewording a universal prompt: it reaches every repository at the next release.

---

<div align="center">

**Rules for every repository, written here.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
