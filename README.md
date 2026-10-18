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

| Piece               | Where the rules land                           | How they get there                             |
| :------------------ | :--------------------------------------------- | :--------------------------------------------- |
| **🏠 Home**         | Each app's own home folder, on every machine   | Your dotfiles run `make agents`                |
| **🗂️ Repositories** | One `AGENTS.md` at the root of each repository | A pull request from `make sync`, merged by you |

The home copy reaches every session, including other people's repositories and
scratch folders. The repository copy travels with the code, so cloud agents and
collaborators get the same rules with nothing installed.

> [!IMPORTANT]
> **Status: built, not yet released.** The law, the renderer, the home kit,
> repository sync and the backstop notes are all here: phases v0.1 to v0.4.
> Nothing reaches a machine or another repository until the first release is
> cut, and phase 0 still needs the probe run on your own machine. See
> [🚀 Releasing](#-releasing).

---

## 🏠 Piece 1: Home

`make agents`, in your dotfiles, downloads the pinned release's home file,
kit and [`scripts/install.py`](scripts/README.md), checks each against its
SHA-256, and runs the installer, which writes byte-identical copies, one per
app, in the shape each app reads:

| Folder        | Universal rules                                                              | Setting                                                                            |
| :------------ | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `~/.agents/`  | `AGENTS.md`, the master copy every other copy is checked against             | none                                                                               |
| `~/.claude/`  | `rules/intelligence.md`; in a Claude cloud session, `CLAUDE.md` instead      | `instructionFiles: claude-md-and-agents-md`, so AGENTS.md loads beside a CLAUDE.md |
| `~/.codex/`   | A marked block in `AGENTS.md`, so your own text stays                        | none                                                                               |
| `~/.gemini/`  | `AGENTS.md`, which Antigravity CLI reads natively                            | none                                                                               |
| `~/.copilot/` | `instructions/intelligence.instructions.md`, with `applyTo: "**"`            | none                                                                               |
| `~/.grok/`    | Nothing: Grok Build reads `~/.claude` by default, so a copy would load twice | none                                                                               |
| `~/.cursor/`  | Nothing to write: paste the home file into Cursor's User Rules once          | none                                                                               |

Copies, not links: links fail silently in Claude's desktop sessions and Grok's
sandbox, and would take over files you keep notes in. `make agents-check`
compares every copy with the release, and `make agents-uninstall` puts back
what was there before. In a Claude cloud session, the
[setup script](setup/README.md) does the same from a pinned release, and can
never stop the session from starting.

**The kit** rides beside the rules in the same release, as one pinned file,
[`home/kit.json`](home/README.md), and the installer puts each piece where
its app reads it:

| Module                                     | What it is                                                                                         | Where it lands                                                                                                                                     |
| :----------------------------------------- | :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Guard hook](scripts/guard.py)             | Denies force-pushes, merges, `--no-verify`, AI sign-offs and irreversible commands before they run | `~/.agents/hooks/`, registered in Claude Code's settings (read by Grok and Cursor), Codex's and Antigravity's `hooks.json`, and Copilot's `hooks/` |
| [`building-skills`](skills/README.md)      | The one skill: how to build, test and ship every other skill                                       | `~/.agents/skills/`, `~/.claude/skills/` and Antigravity's skills folder                                                                           |
| [Worker and Reviewer](subagents/README.md) | Subagents that make one change, and check one without editing                                      | `~/.claude/agents/`, `~/.copilot/agents/` and `~/.codex/agents/`                                                                                   |
| [Knowledge facts](knowledge/README.md)     | Public facts about how this setup works                                                            | Beside every home copy of the rules, between their own markers                                                                                     |

Everything the kit writes carries its mark, so it replaces only its own
files and `make agents-uninstall` takes back exactly what it added.

---

## 🗂️ Piece 2: Repositories

**Each repository holds one `AGENTS.md`, at its root, and nothing else for
agents:** no `CLAUDE.md`, no per-tool files, nothing nested. Every app on the
list reads `AGENTS.md`, Claude Code included. The file has a managed block and
sections the repository owns:

```markdown
# Repository Name

<!-- INTELLIGENCE:BEGIN sha256:<hash of the block> -->

The universal rules: Invariants, then Defaults, each with an ID such as SEC-001.

<!-- INTELLIGENCE:END -->

## Commands

## Definition of done

## Conventions

## Where things live

## Gotchas

## Ask first

## Overrides
```

Both copies open with the same precedence text, so an agent that loads both
knows which rule wins:

> - Invariants: follow every one in every copy; nothing waives one. If a request
>   needs what one forbids, do the rest, skip that part and name the rule ID.
> - Defaults: your user's explicit request for this task wins, then the
>   repository's "Overrides" entry for that rule ID, then the repository's copy
>   of these rules. In forks, and in repositories tannergolden does not own, the
>   project's own rules win and owner-only Defaults do not apply; a repository
>   with no remote yet counts as tannergolden's.

A repository changes a Default only through an Overrides entry naming its rule
ID, and `make audit` rejects one that names an Invariant.

**How a release reaches the repositories**, through
[`scripts/sync.py`](scripts/README.md):

- You review each release once, here.
- `make sync` opens or updates one pull request per repository on
  `chore/intelligence`, under your own `gh` login: no new credential, no
  schedule, no secret in any repository.
- `make merge` merges every sync pull request whose diff is exactly the block
  and whose checks pass. No bot merges anything.
- The marker carries a hash of the block, so a release that leaves the block
  unchanged opens no pull requests at all.
- `make audit` reports any repository whose block was edited by hand, and the
  next `make sync` repairs it.

Every repository you own takes part, except templates, forks and archived
ones, and this hub, which renders its own copy from the law. A
`no-intelligence` topic opts one out. Sync always delivers the latest
release, never unreleased work.

---

## 🗺️ Roadmap

| Phase                     | Delivers                                                                                                       | Done when                                                                                                         | Status                                                 |
| :------------------------ | :------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| **0. Prove the loaders**  | The [loader probe](probe/README.md)                                                                            | Every app you use reads its home copy and a repository's AGENTS.md, headless and by hand, and every control holds | Claude Code passes; the other apps run on your machine |
| **v0.1. The law**         | The rules, one file per ID, in [`law/`](law/README.md); `render.py`; its tests                                 | Two renders are byte-identical, and the block stays under 4,000 characters                                        | Built                                                  |
| **v0.2. The home kit**    | `install.py`; dotfiles' `make agents`, `make agents-check` and `make agents-uninstall`; the cloud setup script | The probe passes on macOS, Linux, a Codespace and a Claude cloud session, and uninstalling restores every file    | Built; proven on a machine after the first release     |
| **v0.3. Repository sync** | `make audit`, `make sync` and `make merge`; this hub's own `AGENTS.md`                                         | One release reaches every repository as one pull request each, merged by one command                              | Built; the first sync is yours to run                  |
| **v0.4. Backstops**       | Rulesets through 🎯 Apply Standards, and the [risks that remain](docs/Backstops-&-Residual-Risk.md)            | A direct push and a force-push to `Development` are both refused                                                  | Written up; the rulesets need your `ADMIN_TOKEN`       |
| **v1.0. Freeze**          | Rule IDs, the marker format and file paths, frozen once two releases pass v0.2 to v0.4                         | One release ships with one review, one `make sync`, one `make merge` and a green probe                            | After two releases                                     |

The modules the plan held back until after 1.0 are built, each with its own
passing tests and a record in [`docs/adrs/`](docs/adrs/README.md):

| Module                    | Delivers                                                                                 | Status                                                   |
| :------------------------ | :--------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| **Guard hooks**           | [`scripts/guard.py`](scripts/README.md), registered for every app by the installer       | Built; first loads with the release that carries the kit |
| **Skills**                | One skill, [`building-skills`](skills/README.md), and the probe's duplicate-skill canary | Built; run `make probe ARGS=--skills` on your machine    |
| **The hierarchy**         | The [Worker and Reviewer](subagents/README.md) subagents                                 | Built                                                    |
| **Knowledge**             | The [public facts](knowledge/README.md), beside every home copy of the rules             | Built; the private tier waits                            |
| **Evals**                 | [Scenarios for every rule](evals/README.md), run with the block and without it           | Built; real runs are yours, `make evals`                 |
| **Unattended sync**       | [`sync.yml`](.github/workflows/sync.yml), through a GitHub App, one token per repository | Built; inert until you create the App                    |
| **Machined-region check** | The standards' check that a block's hash matches its text, in every repository's CI      | Built in tannergolden/standards                          |

---

## 🚀 Releasing

Each release is a tag, and every step after it is one command. `make help`
lists them all.

1. On `Development`, `make check` passes.
2. Run 🏷️ Cut Release with the next version, such as `v0.1.0`. It runs
   `make check` again, and refuses a release whose rendered files have
   drifted from the law.
3. `make pins VERSION=v0.1.0` prints the hashes to pin: the home file, the
   installer and the kit. Put them in dotfiles' `agents/intelligence.pin`,
   then run `make agents` on each machine.
4. `make cloud-setup VERSION=v0.1.0` prints the Claude cloud setup script,
   pinned. Paste it into the cloud environment's setup script.
5. `make audit`, then `make sync ARGS=--dry-run`, then `make sync`: one pull
   request per repository. Once the intelligence App is set up, as
   [`sync.yml`](.github/workflows/sync.yml) describes, Cut Release does this
   step by itself.
6. Review each first sync by hand. After that, `make merge` lands every sync
   whose diff is only the block and whose checks passed.

---

## 🧪 Phase 0: The Loader Probe

[`probe/loader-probe.py`](probe/README.md) plants a random code in every file
an app should read, and another in `~/.agents/AGENTS.md`, which no app should
read. It asks each installed app, headless, which codes its instructions
define, and then restores every byte it touched.

| App         | Version | Where                       | Result             |
| :---------- | :------ | :-------------------------- | :----------------- |
| Claude Code | 2.1.302 | Linux, Claude cloud session | 5 of 5 checks pass |

Codex, Antigravity CLI, Copilot, Cursor and Grok Build run on your own machine:

```bash
python3 probe/loader-probe.py
```

---

## 🧭 Decisions

Every decision behind the plan has a record in [`docs/adrs/`](docs/adrs/README.md),
with the options it was weighed against:

- [ADR-0001](docs/adrs/ADR-0001-Two-Pieces-Home-&-Repository.md): the rules reach agents in two pieces, home and repository
- [ADR-0002](docs/adrs/ADR-0002-One-Root-AGENTS-File.md): one root `AGENTS.md` per repository, and no `CLAUDE.md`
- [ADR-0003](docs/adrs/ADR-0003-Push-Sync-&-Owner-Merge.md): the hub pushes one pull request per repository, and you merge
- [ADR-0004](docs/adrs/ADR-0004-Precedence-Overrides-&-Hash-Marker.md): which copy wins, how a repository overrides, and the hash marker
- [ADR-0005](docs/adrs/ADR-0005-Home-Copies-Not-Links.md): home files are copies, checked against the release
- [ADR-0006](docs/adrs/ADR-0006-Build-The-Law-Adopt-The-Plumbing.md): build the law, adopt the plumbing
- [ADR-0007](docs/adrs/ADR-0007-Public-MIT-Hub.md): this hub is public and MIT-licensed
- [ADR-0008](docs/adrs/ADR-0008-Names-Without-Prefixes.md): rule IDs are `DOMAIN-NNN`, and nothing carries an owner prefix
- [ADR-0009](docs/adrs/ADR-0009-Agents-Follow-The-Standards.md): every agent follows the engineering standards in every repository you own
- [ADR-0010](docs/adrs/ADR-0010-Releases-Serve-Rendered-Files.md): a release tag serves the rendered home file and installer, checked against pins
- [ADR-0011](docs/adrs/ADR-0011-The-Universal-Rule-Set.md): the nineteen rules, and the evidence for each addition and cut
- [ADR-0012](docs/adrs/ADR-0012-One-Pinned-Kit-For-Every-Module.md): every module ships in one pinned kit beside the rules
- [ADR-0013](docs/adrs/ADR-0013-The-Guard-Denies-Never-Allows.md): one guard behind every app's hook, which only ever denies
- [ADR-0014](docs/adrs/ADR-0014-One-Skill-That-Builds-Skills.md): one skill for now, the one that builds skills
- [ADR-0015](docs/adrs/ADR-0015-A-Worker-And-A-Reviewer.md): the hierarchy starts with a Worker and a Reviewer
- [ADR-0016](docs/adrs/ADR-0016-Knowledge-Starts-As-Public-Facts.md): knowledge starts as public facts beside the rules
- [ADR-0017](docs/adrs/ADR-0017-Unattended-Sync-Through-An-App.md): a GitHub App opens the sync pull requests, and you still merge
- [ADR-0018](docs/adrs/ADR-0018-Evals-Measure-The-Block.md): evals measure each rule with the block and without it

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
| [`assets/`](assets/README.md)               | Where this project keeps what presents it: four folders to start, a name ready for every other kind, and the rules every file follows.                      |
| [`docs/`](docs/README.md)                   | Where this project keeps its own documents, and where the engineering standards it follows actually live.                                                   |
| [`evals/`](evals/README.md)                 | Scenarios that tempt an agent to break each universal rule, run against real apps with the block and without it, and checked by code.                       |
| [`home/`](home/README.md)                   | The rendered home file and kit the home kit installs, and the hashes a consumer pins, served from every release tag.                                        |
| [`knowledge/`](knowledge/README.md)         | The public facts about tannergolden's setup that the home kit installs beside the rules: facts, never rules, and never personal context.                    |
| [`law/`](law/README.md)                     | The source of every universal rule: one file per rule ID, and the order, precedence text and budget of the block every agent reads.                         |
| [`probe/`](probe/README.md)                 | Proves, on the machine that runs it, which instruction files each AI coding app actually loads.                                                             |
| [`scripts/`](scripts/README.md)             | The scripts that render the law and the kit, install them on a machine, guard every tool call, and deliver the rules to every repository, with their tests. |
| [`setup/`](setup/README.md)                 | The setup script that installs the universal rules and the kit into every Claude Code cloud session, pinned to one release and unable to fail the session.  |
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
| `sync.yml`                 | Opens each release's sync pull requests through the intelligence App  |

**Do not rename the job ids** `ci` and `secrets` (in `checks.yml`) or `pr` (in
`governance.yml`): branch protection names them. **Sign your commits off** with
`git commit -s`; the DCO check is a required status check once the rulesets are
on.

> [!NOTE]
> **GitHub disables scheduled workflows in a public repository after 60 days
> without activity.** Nothing in the plan depends on a schedule here: syncs run
> when you run them.

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
