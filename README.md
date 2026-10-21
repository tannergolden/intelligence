<!--
title: '🧠 INTELLIGENCE'
description: 'One set of rules for every AI coding agent, installed at home by dotfiles and delivered to every repository as one AGENTS.md.'
type: index
keywords: [ai-agents, agents-md, instructions, standards]
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🧠 INTELLIGENCE

<a name="top"></a>

**One set of rules for every AI coding agent, on every machine and in every repository.**

_Written once. Loaded everywhere. Proven before it is trusted._

</div>

---

## 💡 What This Is

**Intelligence is the source of the rules every AI coding agent follows when it
works for [@tannergolden](https://github.com/tannergolden)**: Claude Code,
Codex, Antigravity CLI, Copilot (the CLI and VS Code), Cursor and Grok Build.
The rules are written once, as one block, and reach the agents in two pieces:

| Piece               | Where the rules land                           | How they get there                                         |
| :------------------ | :--------------------------------------------- | :--------------------------------------------------------- |
| **🏠 Home**         | Each app's own home folder, on every machine   | Your dotfiles run `make agents`                            |
| **🗂️ Repositories** | One `AGENTS.md` at the root of each repository | A pull request from its stub or `make sync`, merged by you |

The home copy reaches every session, including other people's repositories and
scratch folders. The repository copy travels with the code, so cloud agents and
collaborators get the same rules with nothing installed. Ready-made prompts
for any repository stay here, in [`docs/Prompts.md`](docs/Prompts.md), for
anyone to copy into an AI agent: one for each kind of work, from a first look
at the code to a release, most of them ready to run as they are. Each
repository gets a `docs/Prompts.md` of its own, empty, for the prompts only it
needs.

> [!IMPORTANT]
> **Status: built, not yet released.** The Constitution, the renderer, the home kit,
> repository sync and the backstop notes are all here: phases v0.1 to v0.4.
> Nothing reaches a machine or another repository until the first release is
> cut, and phase 0 still needs the probe run on your own machine. See
> [Releasing](docs/distribution/Releasing.md).

---

## 📖 Documentation

Everything the hub does is explained in [`docs/`](docs/README.md), one document
per part. Start with How It Works.

| Document                                                                        | What it explains                                                                                            |
| :------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------- |
| [How It Works](docs/introduction/How-It-Works.md)                               | The two pieces, the block every copy carries, which copy wins, and how a repository overrides one           |
| [The Constitution](CONSTITUTION.md)                                             | Every rule, why it exists, what enforces it, and how to change one                                          |
| [The Home Kit](docs/technical/The-Home-Kit.md)                                  | What `make agents` installs into each app, the kit beside the rules, and the guard hook                     |
| [Repository Sync](docs/technical/Repository-Sync.md)                            | How a release reaches every repository: the stub, `make sync`, `make merge` and `make audit`                |
| [Cloud Setup](docs/technical/Cloud-Setup.md)                                    | The rules and the kit in every Claude Code cloud session                                                    |
| [Prompts](docs/technical/Prompts.md)                                            | The universal prompts the hub keeps, the empty page each repository gets, and how to change each            |
| [Skills & Subagents](docs/technical/Skills-&-Subagents.md)                      | The one skill, the Worker and the Reviewer, and where each app reads them                                   |
| [The Loader Probe](docs/technical/The-Loader-Probe.md)                          | How the hub proves which files each app actually loads, and the results so far                              |
| [Evals](docs/technical/Evals.md)                                                | How each rule is measured, with the block and without it                                                    |
| [Releasing](docs/distribution/Releasing.md)                                     | Every step from a green `Development` to the rules on every machine and in every repository                 |
| [Roadmap](docs/introduction/Roadmap.md)                                         | Each phase and module, what finishes it, and where it stands                                                |
| [Backstops & Residual Risk](docs/operations/Backstops-&-Residual-Risk.md)       | The server-side controls behind the rules, and the risks that remain                                        |
| [Troubleshooting Sync](docs/operations/Troubleshooting-Sync.md)                 | What each line from `make audit`, `make sync`, `make merge` and a stub's run means, and the fix             |
| [Troubleshooting The Home Kit](docs/operations/Troubleshooting-The-Home-Kit.md) | What the installer, its check, the cloud setup script and the guard print, and the fix                      |
| [Glossary](docs/references/Glossary.md)                                         | The hub's own terms, from block, marker and stub to pin and override                                        |
| [Commands](docs/references/Commands.md)                                         | Every make target and script option, and what each one reaches                                              |
| [Files & Formats](docs/references/Files-&-Formats.md)                           | The exact shape of the markers, the pins, the kit, an Overrides entry and what the tools leave on a machine |
| [Eval Scenario Format](docs/references/Eval-Scenario-Format.md)                 | Every key a scenario and a trigger test can hold, and how to add a scenario                                 |
| [Decisions](docs/adrs/README.md)                                                | Every decision behind the plan, with the options it was weighed against                                     |

---

## 📚 The Standards

**All development work here, by a person or an agent, follows
[tannergolden/standards](https://github.com/tannergolden/standards/blob/Development/docs/README.md)**,
by link: how to branch, commit, review, release, test and write documents. The
rules this hub publishes point agents at the same standards, so the work an
agent does in any repository you own meets them too, a new one included. Forks
and other people's repositories follow their own rules.

---

## 📦 What's Inside

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                       | Purpose                                                                                                                                                                                                                   |
| :------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`.devcontainer/`](.devcontainer/README.md) | The language-neutral development container this repository ships, and how to give it the toolchain your project needs.                                                                                                    |
| [`.github/`](.github/)                      | CODEOWNERS, Dependabot, release notes config, Template Sync's list, actions, scripts and workflows - logged below                                                                                                         |
| [`.vscode/`](.vscode/README.md)             | The VS Code settings and extension recommendations this repository shares, and why every other file in this folder stays out of git.                                                                                      |
| [`assets/`](assets/README.md)               | Where this project keeps what presents it: four folders to start, a name ready for every other kind, and the rules every file follows.                                                                                    |
| [`docs/`](docs/README.md)                   | Where this project keeps its own documents, and where the engineering standards it follows actually live.                                                                                                                 |
| [`evals/`](evals/README.md)                 | Scenarios that tempt an agent to break each universal rule, or measure each universal prompt against the hurried request it replaces, run against real apps and checked by code.                                          |
| [`home/`](home/README.md)                   | Everything a machine downloads from a release, rendered: the home file, the kit and the installer the home kit runs, and the hashes a consumer pins.                                                                      |
| [`kit/`](kit/README.md)                     | The sources of everything the home kit installs besides the rules: the guard hook, the skills and the subagents, rendered into home/kit.json.                                                                             |
| [`setup/`](setup/README.md)                 | What leaves the hub for somewhere else: the setup script for every Claude Code cloud session, the stub that keeps a repository's rules current, and the empty prompts page every repository gets.                         |
| [`.editorconfig`](.editorconfig)            | Editor defaults every editor honours: UTF-8, LF, a final newline, and indentation per language                                                                                                                            |
| [`.env.example`](.env.example)              | Environment variable template for this project.                                                                                                                                                                           |
| [`.gitattributes`](.gitattributes)          | Git attributes - line endings, diffs, and what counts as binary                                                                                                                                                           |
| [`.gitignore`](.gitignore)                  | &#x1F5C4;&#xFE0F; Universal Ignore Patterns                                                                                                                                                                               |
| [`.markdownlint.json`](.markdownlint.json)  | Repository-wide markdownlint rules. Discovered by mechanism, which is why this lives at the root.                                                                                                                         |
| [`AGENTS.md`](AGENTS.md)                    | How AI coding agents work in the intelligence hub: its commands, what done means, its conventions, where things live and what to ask first. The universal rules are not copied here, because this hub holds their source. |
| [`CONSTITUTION.md`](CONSTITUTION.md)        | The universal rules every AI agent follows in every repository and on every machine: written once here, rendered into the block every AGENTS.md carries.                                                                  |
| [`LICENSE`](LICENSE)                        | MIT License                                                                                                                                                                                                               |
| [`Makefile`](Makefile)                      | The hub's commands. Each one is plain Python from the standard library, so the same targets run on a Mac, in CI and in a cloud session.                                                                                   |
| [`README.md`](README.md)                    | This file.                                                                                                                                                                                                                |

<!-- AUTO-INDEX:END -->

**Every folder carries a `README.md` that logs each file inside it**, with one
exception. GitHub shows a README in `.github/` in place of this page, so that
folder's own files are logged here instead. 🗂️ Machined Indexes redraws both
tables after every push:

<!-- AUTO-INDEX:BEGIN dir=./.github style=log -->

| Entry                                              | Purpose                                                                                                                             |
| :------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| [`actions/`](.github/actions/README.md)            | The composite actions this repository keeps for its own workflows, and for any other repository that calls them.                    |
| [`scripts/`](.github/scripts/README.md)            | The checks this repository runs on its own configuration, and the tests that guard them.                                            |
| [`workflows/`](.github/workflows/README.md)        | Every workflow in this repository: the name it shows in the Actions tab, what triggers it, and what it does.                        |
| [`CODEOWNERS`](.github/CODEOWNERS)                 | Review ownership                                                                                                                    |
| [`dependabot.yml`](.github/dependabot.yml)         | Dependabot - automated dependency updates                                                                                           |
| [`release.yml`](.github/release.yml)               | GitHub auto-generated release notes configuration.                                                                                  |
| [`template-sync`](.github/template-sync)           | Every path tannergolden/repo ships, and whether &#x1F504; Template Sync, when you run it, keeps it current in this repository.      |
| [`template-sync.lock`](.github/template-sync.lock) | Where each file here was last synced from.                                                                                          |
| [`template-sync.md`](.github/template-sync.md)     | How this repository takes its template's later fixes when you run &#x1F504; Template Sync, what you control, and what waits on you. |

<!-- AUTO-INDEX:END -->

---

## 🌿 The Workflows

| Workflow                   | Gives you                                                             |
| :------------------------- | :-------------------------------------------------------------------- |
| `checks.yml`               | Lint, test and build; secret scan; CodeQL; workflow lint              |
| `governance.yml`           | Pull request title and DCO checks, triage, stale sweep, commands      |
| `release.yml`              | Draft notes, publish assets, prune superseded releases                |
| `maintenance.yml`          | Prunes stale deployments and draft releases                           |
| `lifecycle.yml`            | Claims this repository once; flags a new major                        |
| `dependabot-automerge.yml` | Approves and queues patch and minor updates                           |
| `ci-failure-alert.yml`     | Opens an issue when a watched workflow fails                          |
| `apply-standards.yml`      | Dispatch-only: the label taxonomy, settings and rulesets              |
| `auto-format.yml`          | Formats what a push touched                                           |
| `preview-deploy.yml`       | Deploys pushes to a preview target, once configured                   |
| `prune-runs.yml`           | Deletes old workflow runs, with their logs and artifacts              |
| `verify-stubs.yml`         | Proves every stub's permission ceiling matches its called workflow    |
| `auto-index.yml`           | Redraws every folder log after a push                                 |
| `template-sync.yml`        | Proposes the template's later fixes as one pull request, when run     |
| `cut-release.yml`          | Cuts the hub's releases, and refuses one whose rendered files drifted |
| `sync.yml`                 | Called by each repository's stub to sync it; never runs here          |

**Do not rename the job ids** `ci` and `secrets` (in `checks.yml`) or `pr` (in
`governance.yml`): branch protection names them. **Sign your commits off** with
`git commit -s`; the DCO check is a required status check once the rulesets are
on.

> [!NOTE]
> **GitHub disables scheduled workflows in a public repository after 60 days
> without activity.** The one schedule the plan leans on is each stub's Monday
> run, in the repository that carries it. A public repository that goes quiet
> stops pulling until you run its sync or `make sync`, and `make audit` names
> its older block meanwhile.

---

## 🔒 Licence

**MIT.** See [LICENSE](LICENSE). Anyone may copy, adapt and reuse these rules.
The shared workflows this repository calls from
[tannergolden/standards](https://github.com/tannergolden/standards) are
published separately under their own licence.

---

<div align="center">

**Write the rules once. Prove every app reads them.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by [@tannergolden](https://github.com/tannergolden). Distributed under the MIT License.

</div>
