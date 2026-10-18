<!--
title: '🧠 INTELLIGENCE'
description: 'One set of rules for every AI coding agent, installed at home by dotfiles and delivered to every repository as one AGENTS.md.'
tags: [ai-agents, agents-md, instructions, standards]
category: docs
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
collaborators get the same rules with nothing installed.

> [!IMPORTANT]
> **Status: built, not yet released.** The law, the renderer, the home kit,
> repository sync and the backstop notes are all here: phases v0.1 to v0.4.
> Nothing reaches a machine or another repository until the first release is
> cut, and phase 0 still needs the probe run on your own machine. See
> [Releasing](docs/operations/Releasing.md).

---

## 📖 Documentation

Everything the hub does is explained in [`docs/`](docs/README.md), one document
per part. Start with How It Works.

| Document                                                                  | What it explains                                                                                  |
| :------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------ |
| [How It Works](docs/technical/How-It-Works.md)                            | The two pieces, the block every copy carries, which copy wins, and how a repository overrides one |
| [The Law](docs/technical/The-Law.md)                                      | Where every rule is written, the rules the rules follow, and how to change one                    |
| [The Home Kit](docs/technical/The-Home-Kit.md)                            | What `make agents` installs into each app, the kit beside the rules, and the guard hook           |
| [Repository Sync](docs/technical/Repository-Sync.md)                      | How a release reaches every repository: the stub, `make sync`, `make merge` and `make audit`      |
| [Cloud Setup](docs/technical/Cloud-Setup.md)                              | The rules and the kit in every Claude Code cloud session                                          |
| [Skills & Subagents](docs/technical/Skills-&-Subagents.md)                | The one skill, the Worker and the Reviewer, and where each app reads them                         |
| [Knowledge](docs/technical/Knowledge.md)                                  | The public facts installed beside the rules, and what may go in                                   |
| [The Loader Probe](docs/technical/The-Loader-Probe.md)                    | How the hub proves which files each app actually loads, and the results so far                    |
| [Evals](docs/technical/Evals.md)                                          | How each rule is measured, with the block and without it                                          |
| [Releasing](docs/operations/Releasing.md)                                 | Every step from a green `Development` to the rules on every machine and in every repository       |
| [Roadmap](docs/operations/Roadmap.md)                                     | Each phase and module, what finishes it, and where it stands                                      |
| [Backstops & Residual Risk](docs/operations/Backstops-&-Residual-Risk.md) | The server-side controls behind the rules, and the risks that remain                              |
| [Decisions](docs/adrs/README.md)                                          | Every decision behind the plan, with the options it was weighed against                           |

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

| Entry                                       | Purpose                                                                                                                                                     |
| :------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`.devcontainer/`](.devcontainer/README.md) | The language-neutral development container this repository ships, and how to give it the toolchain your project needs.                                      |
| [`.github/`](.github/)                      | CODEOWNERS, Dependabot, release notes config, Template Sync's list, scripts and workflows - logged below                                                    |
| [`.vscode/`](.vscode/README.md)             | The VS Code settings and extension recommendations this repository shares, and why every other file in this folder stays out of git.                        |
| [`actions/`](actions/README.md)             | The composite action that carries the hub's own code into every repository whose stub asks for it, at the hub's latest release.                             |
| [`assets/`](assets/README.md)               | Where this project keeps what presents it: four folders to start, a name ready for every other kind, and the rules every file follows.                      |
| [`docs/`](docs/README.md)                   | Where this project keeps its own documents, and where the engineering standards it follows actually live.                                                   |
| [`evals/`](evals/README.md)                 | Scenarios that tempt an agent to break each universal rule, run against real apps with the block and without it, and checked by code.                       |
| [`home/`](home/README.md)                   | The rendered home file and kit the home kit installs, and the hashes a consumer pins, served from every release tag.                                        |
| [`knowledge/`](knowledge/README.md)         | The public facts about tannergolden's setup that the home kit installs beside the rules: facts, never rules, and never personal context.                    |
| [`law/`](law/README.md)                     | The source of every universal rule: one file per rule ID, and the order, precedence text and budget of the block every agent reads.                         |
| [`probe/`](probe/README.md)                 | Proves, on the machine that runs it, which instruction files each AI coding app actually loads.                                                             |
| [`scripts/`](scripts/README.md)             | The scripts that render the law and the kit, install them on a machine, guard every tool call, and deliver the rules to every repository, with their tests. |
| [`setup/`](setup/README.md)                 | What you copy out of the hub once: the setup script for every Claude Code cloud session, and the stub that keeps a repository's rules current.              |
| [`skills/`](skills/README.md)               | The skills the home kit installs into every AI coding app, each a folder in the open Agent Skills format.                                                   |
| [`subagents/`](subagents/README.md)         | The Worker and Reviewer subagents the home kit installs, each one source rendered for Claude Code, Copilot and Codex.                                       |
| [`.editorconfig`](.editorconfig)            | Editor defaults every editor honours: UTF-8, LF, a final newline, and indentation per language                                                              |
| [`.env.example`](.env.example)              | Environment variable template for this project.                                                                                                             |
| [`.gitattributes`](.gitattributes)          | Git attributes - line endings, diffs, and what counts as binary                                                                                             |
| [`.gitignore`](.gitignore)                  | &#x1F5C4;&#xFE0F; Universal Ignore Patterns                                                                                                                 |
| [`.markdownlint.json`](.markdownlint.json)  | Repository-wide markdownlint rules. Discovered by mechanism, which is why this lives at the root.                                                           |
| [`AGENTS.md`](AGENTS.md)                    | How AI coding agents work in the intelligence hub: the universal rules it publishes, then its own commands, conventions and limits.                         |
| [`LICENSE`](LICENSE)                        | MIT License                                                                                                                                                 |
| [`Makefile`](Makefile)                      | The hub's commands. Each one is plain Python from the standard library, so the same targets run on a Mac, in CI and in a cloud session.                     |
| [`README.md`](README.md)                    | This file.                                                                                                                                                  |

<!-- AUTO-INDEX:END -->

**Every folder carries a `README.md` that logs each file inside it**, with one
exception. GitHub shows a README in `.github/` in place of this page, so that
folder's own files are logged here instead. 🗂️ Machined Indexes redraws both
tables after every push:

<!-- AUTO-INDEX:BEGIN dir=./.github style=log -->

| Entry                                              | Purpose                                                                                                                             |
| :------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| [`scripts/`](.github/scripts/README.md)            | The checks this repository runs on its own configuration, and the tests that guard them.                                            |
| [`workflows/`](.github/workflows/README.md)        | Every workflow in this repository: the name it shows in the Actions tab, what triggers it, and what it does.                        |
| [`CODEOWNERS`](.github/CODEOWNERS)                 | CODEOWNERS - review ownership                                                                                                       |
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
