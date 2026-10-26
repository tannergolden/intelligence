<!--
title: '🤖 Agent Instructions'
description: 'How AI coding agents work in the intelligence hub: its commands, what done means, its conventions, where things live and what to ask first. The universal rules are not copied here, because this hub holds their source.'
type: standard
-->

<div align="center">

# 🤖 Agent Instructions

<a name="top"></a>

**How AI coding agents, and the people beside them, work in the hub.**

_The hub's own rules here. The universal ones from their source._

</div>

---

## Start here

This hub holds the universal rules, in [`CONSTITUTION.md`](CONSTITUTION.md), and
this file holds only the hub's own: its commands, what done means, its
conventions, where things live and what to ask first. It carries no
`INTELLIGENCE` block, because a copy of the rules beside their source would be
a second source, and sync skips the hub
([ADR-0026](docs/adrs/ADR-0026-The-Hub-Keeps-Its-Own-Rules-In-AGENTS.md)).
Agents working here get the universal rules from their home copies, which
dotfiles installs on a machine and the
[cloud setup script](docs/technical/Cloud-Setup.md) writes into a Claude cloud
session.

Everything this file does not cover follows
[tannergolden/standards](https://github.com/tannergolden/standards): branches,
commit messages, sign-offs and pull requests. The code of conduct, the
contributing guide and the security policy are the account's own, which GitHub
serves to this repository from its `.github` repository.

## Commands

- `make setup`: install PyYAML, which the repository validator in `make lint` needs. CI runs it before the checks.
- `make check`: everything CI checks, which are the repository validator, `render.py --check`, `faculties.py --check`, `prompts.py --check`, `evals.py --check` and every test.
- `make test`: the tests alone, every `test_*.py` in `.github/scripts/`.
- `make render`: rewrite `home/` from `CONSTITUTION.md`, the kit's sources in `kit/` and the installer.
- `make faculties VERSION=vX.Y.Z`: copy the five faculties, their trigger tests and their pin from that release of tannergolden/knowledge. Follow it with `make render`.
- `make probe`: prove which instruction files each installed app loads. It makes one model call per check.
- `make evals`: measure each rule with the block and without it, and each universal prompt against the hurried request it replaces. Real runs make model calls; `ARGS=--dry-run` makes none.
- `python3 kit/guard.py --command '<command>'`: see what the guard hook would say about one command.
- `make audit`, `make sync` and `make merge`: reach every repository the owner owns, through the owner's `gh` login. `make merge` also starts the checks a stub's pull request waits on.

## Definition of done

- `make check` passes, and its output is in your report.
- A change to `CONSTITUTION.md`, anything in `kit/` or `.github/scripts/install.py` is followed by `make render`, and the rendered files are committed with it.
- A new rule gets a scenario in `evals/scenarios/`, a new skill a trigger test in `evals/skills/`, and a new universal prompt a scenario in `evals/prompts/`, with a `proof` its checks pass and doing nothing fails.
- A change to the universal prompts in `docs/Prompts.md`, or to the empty page in `setup/Prompts.md`, stays as Prettier writes it, with the standards' configuration, and passes `prompts.py --check`; a reworded prompt brings its scenario in `evals/prompts/` along, and a new one gets a link in the "Find A Prompt" index.
- Every new script has tests beside it, and every folder's `README.md` logs its files, except inside a skill's folder.
- A change to how something works updates its document in `docs/` in the same commit, in the folder for its kind: `docs/technical/` for how a part works, `docs/distribution/` for how a release ships, `docs/operations/` for the controls and risks.

## Conventions

- Python uses the standard library only, with `from __future__ import annotations` and single quotes. Tests use `unittest`, are named `test_*.py`, and load the script they test with `importlib`.
- `install.py`, `loader-probe.py` and `kit/guard.py` run on the Python 3.9 that macOS ships, so none of them uses `match` or a runtime `X | Y`.
- Skill and subagent files open with the `---` frontmatter their loaders need, with no Document Styling header or footer.
- A rule is one ASCII sentence, quoted under its ID in `CONSTITUTION.md`, whose Article VI sets the format. IDs are `DOMAIN-NNN` and are never reused: its appendix lists the retired ones.
- Every explanation lives in `docs/`. A folder's `README.md` says what the folder holds in a sentence or two, links the document that explains it, and logs its files.

## Where things live

| Path                                 | What                                                                                                                                                                          |
| :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CONSTITUTION.md`](CONSTITUTION.md) | The source of every rule, and the order and budget of the block                                                                                                               |
| `kit/`                               | The kit's sources: the guard, `develop` and its team, the faculties `faculties.json` pins from tannergolden/knowledge, and the Worker and Reviewer subagents                  |
| `home/`                              | Everything a machine downloads, rendered: the home file, the kit, the installer and their hashes, which every release tag serves                                              |
| `evals/`                             | Scenarios for every rule and every universal prompt, and the skill trigger tests                                                                                              |
| `setup/`                             | The Claude cloud setup script, the stub a repository carries, and the empty prompts page every repository gets                                                                |
| `docs/Prompts.md`                    | The universal prompts, which stay in the hub: anyone copies one from here into any agent                                                                                      |
| `.github/scripts/`                   | Every script, with its test beside it: `render.py`, `kit.py`, `faculties.py`, `install.py`, `sync.py`, `prompts.py`, `evals.py`, `loader-probe.py`, and the template's checks |
| `.github/actions/`                   | The action a repository's stub runs, through `.github/workflows/sync.yml`                                                                                                     |
| `docs/introduction/`                 | Where to start: `How-It-Works.md`, which shows how the pieces fit, and the roadmap                                                                                            |
| `docs/distribution/`                 | Every step of a release, from a green `Development` to every machine and repository                                                                                           |
| `docs/technical/`                    | How every part of the hub works, one document each                                                                                                                            |
| `docs/operations/`                   | The controls and risks behind the rules, and what to do when a sync or an install goes wrong                                                                                  |
| `docs/references/`                   | Pages to look up: the glossary, the commands, the files and formats, and the eval scenario format                                                                             |
| `docs/library/`                      | Material to learn from, as the standards keep it: the prompt engineering best practices                                                                                       |
| `docs/adrs/`                         | Every decision behind the plan                                                                                                                                                |

## Gotchas

- Never edit inside `home/`. It is rendered, and `make check` fails on a hand edit.
- Never edit a faculty in `kit/skills/`, its trigger test in `evals/skills/` or `kit/faculties.json`. They are copied from a release of tannergolden/knowledge: `make check` fails on a hand edit to a copy or its trigger test, and `faculties.py --verify` on a pin that no longer holds the release it names. Change the faculty there, and pin the release that carries it.
- The guard hook denies a commit git would author as an AI. In a cloud session, pass `--author` and `--trailer 'Signed-off-by: ...'` with your user's identity, never `-s`.
- Changing `CONSTITUTION.md` changes nothing elsewhere until a release: other repositories receive the rules only through one, which their stub or `make sync` delivers.
- `sync.py`, `render.py`, `kit.py` and `prompts.py`, and `setup/Prompts.md`, also run or are read inside every repository that carries the stub, at the hub's latest release, from the archive GitHub serves. Cut Release refuses a tag without them, `.gitattributes` keeps `.github/scripts/` in that archive, and `test_stub.py` holds both.
- The universal prompts live in `docs/Prompts.md` and reach no other repository. `setup/Prompts.md` is the empty page a repository gets once; after that sync never changes a repository's page.
- Never put the `INTELLIGENCE` block in this file, and never add a `CLAUDE.md`. The hub holds the source of the rules, so a copy beside it would be a second source, and a `CLAUDE.md` would make Claude Code skip this file.

## Ask first

- Cutting a release, running `make sync` or `make merge` against real repositories, or running a repository's 🔁 Intelligence Sync.
- Adding a universal skill: the hub writes one, `develop`, and pins the five faculties from tannergolden/knowledge. A skill one repository needs lives in that repository.
- Changing a rule's wording, its kind or its ID.
- Adding, removing or rewording a universal prompt, which everyone copies from the hub, or changing the empty page in `setup/Prompts.md`, which every repository without one gets at the next release.

---

<div align="center">

**Rules for every repository, written here.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
