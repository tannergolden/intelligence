<!--
title: '📘 GLOSSARY'
description: 'What the hub''s own words mean: the rules and their kinds, blocks and markers, releases and pins, the home kit, sync, and the tools that prove it works. Read it when a term in another document here is unclear.'
type: reference
-->

<div align="center">

# 📘 GLOSSARY

<a name="top"></a>

**Every word the hub uses in a sense of its own, defined once.**

_One meaning per word, in every document._

</div>

---

## 💡 How To Use This Page

These are the hub's own terms, grouped by the part of the hub they belong to,
most with a link to the document that explains them. Engineering, git and
automation terms shared by every repository are in the standards'
[Glossary](https://github.com/tannergolden/standards/blob/Development/docs/references/Glossary.md).

---

## ⚖️ The Rules

| Term                   | What it means here                                                                                                                                                                                    |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Constitution**       | [`CONSTITUTION.md`](../../CONSTITUTION.md), at the hub's root: every rule, why it exists and what enforces it, and the size the block may grow to. Every copy an agent reads is rendered from it      |
| **Rule**               | One sentence of printable ASCII, at most 300 characters and ending in a period, quoted under its ID in the Constitution. Agents read only that sentence; the reason and the enforcers stay in the hub |
| **Rule ID**            | `DOMAIN-NNN`, such as `SEC-001`: two to five capital letters and three digits. An ID appears once, and a retired one is listed in the Constitution's appendix and never used again                    |
| **Invariant**          | A rule nothing waives. It holds from every copy that loads, in every repository, and names what enforces it outside the prompt                                                                        |
| **Default**            | A rule that holds until the user's explicit request for the task, or the repository's Overrides entry for its ID, says otherwise                                                                      |
| **Owner-only Default** | A Default that holds only in repositories tannergolden owns, a repository with no remote yet included, and never in a fork or someone else's project                                                  |
| **Precedence**         | The two lines from the Constitution's Article I that open every copy of the block and say which rule wins when several copies load at once. [How It Works](../introduction/How-It-Works.md)           |
| **Overrides entry**    | One line under the `## Overrides` heading of a repository's `AGENTS.md`, such as `- WORK-002: we ask more`, that changes one Default for that repository. One naming an Invariant changes nothing     |
| **Enforcer**           | What stops a behaviour outside the prompt: a ruleset, a required check, a sandbox or the guard. The Constitution lists each rule's under **Enforced by:** and **To add:**                             |
| **Backstop**           | An enforcer on GitHub's side, such as a ruleset or push protection. [Backstops & Residual Risk](../operations/Backstops-&-Residual-Risk.md)                                                           |

---

## 📝 Blocks & Markers

| Term                     | What it means here                                                                                                                                                                                                                                   |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| **Block**                | The rules as every agent reads them: a `## Constitution` heading, the precedence, then `### Invariants`, `### Defaults` and `### Owner-only Defaults`, one `- ID: sentence` line per rule. Capped at 5,000 characters                                |
| **Prompts block**        | The universal prompts release v0.3.0 sealed into a repository's `docs/Prompts.md`, which sync now takes out. The universal prompts stay in the hub's `docs/Prompts.md`, and a repository's page is its own. [Prompts](../technical/Prompts.md)       |
| **Ready-to-run prompt**  | A universal prompt with nothing to fill in: the agent finds what it needs, such as the commands, the default branch or the last release, in the repository. One with a **Fill in** line asks for what only a person knows, and the index marks it ✏️ |     |
| **Marker**               | One of the two comment lines around a block, such as `<!-- INTELLIGENCE:BEGIN sha256:<hash> -->` and `<!-- INTELLIGENCE:END -->`. The hash in the BEGIN marker is the SHA-256 of the block's text. [Files & Formats](Files-&-Formats.md)             |
| **Sealed, unsealed**     | A sealed BEGIN marker carries the hash; an unsealed one does not. Only a block sync delivers is sealed: the rules in `AGENTS.md`, and the prompts block v0.3.0 delivered                                                                             |
| **Edited block**         | A block whose text no longer matches the hash in its marker. `make audit` names it, the guard denies an agent's edit inside one, and the next sync puts the release's block back                                                                     |
| **Machined Block Check** | The standards' check, in every repository's CI, that each block's hash matches its text                                                                                                                                                              |
| **Render**               | Rebuild a copy from its source. `make render` rewrites everything in `home/` from `CONSTITUTION.md`, `kit/` and `.github/scripts/install.py`, and nothing there is edited by hand                                                                    |
| **Stale**                | Behind its source: a file in `home/` that `make render` would change, which fails `make check`, or a copy of the block, in a repository or a home folder, from a release other than the one it is checked against                                    |

---

## 📦 Releases & Pins

| Term             | What it means here                                                                                                                                                                                                                                                                 |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hub**          | This repository. It holds the source of the rules and keeps no copy of them, so it has no `AGENTS.md`, and sync skips it                                                                                                                                                           |
| **Release**      | A tag `vX.Y.Z`, cut by 🏷️ Cut Release. Dotfiles and the cloud setup script pin one, and the stub follows the newest through the moving major. Nothing reaches a machine or another repository until one is cut, and every version stays. [Releasing](../distribution/Releasing.md) |
| **Moving major** | The tag `vX` that Cut Release moves to each new release. The stub calls the hub's workflow at `@v0`, which calls its action at `@v0`, so moving the tag delivers the release to every repository that carries the stub                                                             |
| **Home file**    | `home/intelligence.md`: the block between its markers and nothing else. The home kit copies it into each app's folder, and sync delivers the same block to every repository                                                                                                        |
| **Kit**          | `home/kit.json`: the guard, the skills and the subagents in one file, rendered by `kit.py` from `kit/`, so a consumer pins one hash for all of them                                                                                                                                |
| **Kit format**   | The `format` number in `home/kit.json`, which the installer checks before it reads anything else. It is 2 since the kit stopped carrying the knowledge facts                                                                                                                       |
| **Pin**          | The SHA-256 a consumer records for a file before downloading it from a release, and checks the download against: never a hash from the same download. `make pins VERSION=vX.Y.Z` prints one each for the home file, the installer and the kit                                      |

---

## 🏠 The Home Kit

| Term                   | What it means here                                                                                                                                                                                                                                                                                                                                   |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Home kit**           | What dotfiles' `make agents` installs on a machine: a copy of the rules where each app reads them, and the kit beside them. [The Home Kit](../technical/The-Home-Kit.md)                                                                                                                                                                             |
| **Home copy**          | One app's copy of the block in its home folder, such as `~/.claude/rules/intelligence.md`, or a marked block in `~/.codex/AGENTS.md`                                                                                                                                                                                                                 |
| **Master copy**        | `~/.agents/AGENTS.md`, which every other home copy is checked against. None of the apps the hub serves reads it, so the copies never load twice                                                                                                                                                                                                      |
| **Installer**          | `install.py`, served as `home/install.py`, with three commands: `install`, `check` and `uninstall`. It makes no network calls                                                                                                                                                                                                                        |
| **Install record**     | `install.json` in `$XDG_STATE_HOME/intelligence/`, or `~/.local/state/intelligence/` without that variable: what `uninstall` needs to put each file back, such as whether the kit created it, the earlier value of Claude Code's `instructionFiles` setting, and the ask rules the kit added                                                         |
| **Kit's mark**         | The line `Part of tannergolden/intelligence's home kit, which replaces this file on every install.`, which the guard and every subagent file carry, and every installed skill folder holds in a `.intelligence-kit` file. The installer replaces only what it can tell is its own: a file with the mark, or a copy of the rules with its block       |
| **Guard**              | `kit/guard.py`, installed as `~/.agents/hooks/intelligence-guard.py` and run by every app's pre-tool hook. It denies the few calls the Invariants forbid outright, with exit 2 and one line saying why, or stays silent; it never allows and never asks. Claude Code also runs it after a compaction, with `--remind`, to print the Invariants again |
| **Shadow**             | A file the installer warns about because it would hide a home copy or load the rules a second time: `~/.codex/AGENTS.override.md`, `~/AGENTS.md` or `~/CLAUDE.md`                                                                                                                                                                                    |
| **Cloud setup script** | `setup/claude-cloud-setup.sh`, printed with a release's pins by `make cloud-setup`, which installs Claude Code's share of the home kit in every Claude Code cloud session and always exits 0. [Cloud Setup](../technical/Cloud-Setup.md)                                                                                                             |
| **Skill**              | A folder in the open Agent Skills format that an agent opens only when its description matches the task. The hub ships one, `develop`. [Skills & Subagents](../technical/Skills-&-Subagents.md)                                                                                                                                                      |
| **Subagent**           | An agent a session hands work to. The kit ships two, the Worker and the Reviewer, each one source rendered for Claude Code, Copilot and Codex                                                                                                                                                                                                        |

---

## 🔁 Sync

| Term                      | What it means here                                                                                                                                                                                                                                                                                                                                     |
| :------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sync**                  | Delivering a release's blocks to a repository as one pull request that only the owner merges, by the stub or by `make sync`. [Repository Sync](../technical/Repository-Sync.md)                                                                                                                                                                        |
| **Stub**                  | `setup/intelligence-sync.yml`, copied into a repository as `.github/workflows/intelligence-sync.yml`, which pulls each release every Monday on that repository's own `GITHUB_TOKEN`. The standards' stubs are a different thing: the workflows every repository from the templates carries, each calling a reusable workflow in the standards at `@v1` |
| **Sync branch**           | `chore/intelligence`, the head of every sync pull request. `make sync` moves it to the default branch's latest commit before it writes, so no other work belongs on it                                                                                                                                                                                 |
| **First sync**            | A repository's first sync, which may create `AGENTS.md`, put the block into one that has none, fold a `CLAUDE.md` into it, or add the empty `docs/Prompts.md`. It is bigger than the syncs after it, so `make merge` leaves it to be reviewed by hand                                                                                                  |
| **Fold**                  | What sync does with a `CLAUDE.md` that holds text of its own: moves it into `AGENTS.md` under `## Folded from CLAUDE.md`, every heading one level down, and deletes the file. A `CLAUDE.md` that only points at `AGENTS.md` is just deleted                                                                                                            |
| **Apply**                 | `sync.py apply`, the command the stub's action runs in a repository's checkout. It writes the release's blocks into the working tree and changes nothing else                                                                                                                                                                                          |
| **Opt-out topic**         | A GitHub topic on a repository: `no-intelligence` keeps it out of sync, and `no-intelligence-prompts` keeps its prompts page out while the rules still arrive                                                                                                                                                                                          |
| **Golden path templates** | The two templates new repositories start from. Sync skips both, so they carry no agent files and a repository generated from one starts an `AGENTS.md` of its own                                                                                                                                                                                      |
| **`BOT_ACCESS_TOKEN`**    | An optional secret a repository may hold. With it, the stub opens the pull request as the token's owner and its checks start at once; without it, the default `GITHUB_TOKEN` opens it and GitHub holds its checks until someone approves them                                                                                                          |

---

## 🧪 Proof

| Term                 | What it means here                                                                                                                                                                                                        |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- |
| **Loader probe**     | `loader-probe.py`, which proves on one machine which instruction files each app loads: it plants a random code in each file and asks the app which codes it can see. [The Loader Probe](../technical/The-Loader-Probe.md) |
| **Probe code**       | A random twelve-character code the probe plants: `PROBE_REPO` in a scratch repository's `AGENTS.md`, `PROBE_HOME` in each home copy, and `PROBE_MASTER` in the master copy                                                |
| **Control**          | A probe check that expects an app to skip `AGENTS.md` in a documented case, such as Claude Code beside a `CLAUDE.md`                                                                                                      |
| **Skill canary**     | The probe's `--skills` check: one skill name planted in three skills folders, to prove each app sees exactly one copy                                                                                                     |
| **Scenario**         | A JSON file in `evals/scenarios/` that sets up a scratch repository tempting an agent to break one rule, and the checks that decide whether it did. [Eval Scenario Format](Eval-Scenario-Format.md)                       |
| **With and without** | The two conditions every scenario runs in: with the block in the scratch repository's `AGENTS.md`, and without it. The difference between the two pass rates is what the block is worth for that rule                     |
| **Shim**             | A stand-in for a command such as `gh` or `curl`, first on a scenario's `PATH`, which logs its arguments and reaches nothing                                                                                               |
| **Trigger test**     | A JSON file in `evals/skills/` holding prompts that should load a skill and near misses that should not. [Evals](../technical/Evals.md)                                                                                   |
| **Prompt scenario**  | A JSON file in `evals/prompts/` that measures one universal prompt against the hurried request it replaces, in a scratch repository, with checks that decide each run. [Eval Scenario Format](Eval-Scenario-Format.md)    |
| **Hurried request**  | The one-line request a person in a hurry would type in place of a universal prompt. Its scenario runs both, and the difference between the two pass rates is what the prompt is worth                                     |
| **Proof**            | A prompt scenario's script that does the asked-for work. The tests run it, and then nothing, against a stand-in app, to show the scenario's checks pass the work and fail doing nothing                                   |     |

---

## 🔗 See Also

- [How It Works](../introduction/How-It-Works.md): how these pieces fit together
- [Commands](Commands.md): every command these terms turn up in
- [Glossary](https://github.com/tannergolden/standards/blob/Development/docs/references/Glossary.md): the terms every repository on the standards shares

---

<div align="center">

**Say it the same way in every document.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
