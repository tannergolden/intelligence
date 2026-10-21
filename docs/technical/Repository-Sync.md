<!--
title: '🔁 REPOSITORY SYNC'
description: 'How each release reaches every repository: the stub a repository carries, make sync from the hub, what a first sync does, and how make merge lands the result.'
type: guide
-->

<div align="center">

# 🔁 REPOSITORY SYNC

<a name="top"></a>

**Each release reaches every repository as one pull request, and only you merge it.**

_The repository asks, or you push. Either way, you merge._

</div>

---

## 💡 How A Release Reaches A Repository

Every repository carries the rules in one root `AGENTS.md`, between
`INTELLIGENCE` markers, beside sections the repository owns, as
[How It Works](../introduction/How-It-Works.md) describes, and ready-made
[prompts](Prompts.md) in `docs/Prompts.md`, whose `INTELLIGENCE:PROMPTS`
block the hub keeps current beside the repository's own prompts. A release
reaches it by either of two routes, through
[`.github/scripts/sync.py`](../../.github/scripts/sync.py):

- You review each release once, in the hub.
- **The stub.** A repository that carries it pulls each release by itself.
  Every Monday, and whenever you run it, its 🔁 Intelligence Sync opens or
  updates one pull request on `chore/intelligence`, on that repository's own
  `GITHUB_TOKEN`: no App, no key, no secret.
- **The push.** `make sync` opens the same pull request in every repository at
  once, under your own `gh` login, with or without the stub.
- `make merge` merges every sync pull request whose diff is exactly the
  blocks and whose checks pass. No bot merges anything.
- Each marker carries a hash of its block, so a release that leaves both
  blocks unchanged opens no pull requests at all.
- `make audit` reports any repository whose rules or prompts block was edited
  by hand, and whether it carries the stub; the next sync repairs the block.

Every repository you own takes part, except the two golden path templates,
`repo` and `path`, forks and archived ones, and the hub, which holds the
Constitution and carries no copy of it. A template of any other kind, such
as the vault template, takes part like the rest, since every repository
generated from it inherits its `AGENTS.md`. A `no-intelligence` topic opts
one out, and a `no-intelligence-prompts` topic keeps only the prompts out.
Both routes deliver a release, never unreleased work.

---

## 🌱 What A First Sync Does

A repository's first sync is bigger than the ones after it, so `make merge`
leaves it for you to review by hand:

- a repository with no `AGENTS.md` gets one, with the block, an admonition
  saying the repository's own rules go below it, and empty sections for its
  own commands, conventions and overrides;
- an `AGENTS.md` with no block gets the block after its header, and keeps
  everything else; a file that opens with YAML frontmatter, as an Obsidian
  note does, keeps it first and takes the block after it and its title;
- a `CLAUDE.md` is folded into `AGENTS.md` under "Folded from CLAUDE.md" and
  deleted, or just deleted when all it does is point at `AGENTS.md`, because
  Claude Code skips `AGENTS.md` beside one;
- a repository with no `docs/Prompts.md` gets one, with the universal prompts
  and a section for its own, the first time a release carries the prompts; a
  `docs/Prompts.md` with no prompts block is the repository's own, and stays
  as it is.

After that, each sync replaces only the text between the markers.

---

## 🧷 The Stub

**To add it to a repository**, copy
[`setup/intelligence-sync.yml`](../../setup/intelligence-sync.yml) into it as
`.github/workflows/intelligence-sync.yml`, and let GitHub Actions create pull
requests there, under Settings, Actions, General; 🎯 Apply Standards turns
that on with the rest of the standard settings. Then run it once from the
Actions tab, or wait for Monday. It pins `@v0`, so each release reaches it on
the Monday after:

```yaml
# Installed from tannergolden/intelligence. Edit freely: this file is YOURS.
#
# Keeps the universal rules for AI coding agents current in this
# repository's root AGENTS.md: the block between the INTELLIGENCE markers,
# which tannergolden/intelligence renders and releases. It keeps the
# universal prompts in docs/Prompts.md current the same way. Every Monday,
# and whenever you run it, it proposes the latest release's blocks as one
# pull request on `chore/intelligence`, and leaves every section this
# repository owns as it was. A first sync creates AGENTS.md and
# docs/Prompts.md. Merging stays yours.
#
# It runs on this repository's own GITHUB_TOKEN, with no App and no key, so
# two settings matter: Settings > Actions > General must allow GitHub
# Actions to create pull requests, and GitHub holds the checks of a pull
# request that token opens until you approve them. `make merge` in the hub
# approves them for a change that is only the block. A BOT_ACCESS_TOKEN
# secret, if this repository has one, opens it as you instead.
#
# `@v0` follows the hub's latest release. To stop, delete this file; the
# `no-intelligence` topic also keeps `make sync` away, and the
# `no-intelligence-prompts` topic keeps the prompts out alone.

name: '🔁 Intelligence Sync'

on:
  schedule:
    - cron: '23 6 * * 1' # Mondays: picks up a new release, and repairs a block edited by hand
  workflow_dispatch:
    inputs:
      dry-run:
        description: 'Print what would change, and change nothing'
        type: boolean
        default: false

concurrency:
  group: ${{ github.workflow }}
  cancel-in-progress: false

# ⚠️ THE `permissions:` BELOW IS A CEILING, NOT A GRANT. The called workflow
# asks for exactly these two; grant less and it fails before any job starts.
permissions: {}

jobs:
  sync:
    permissions:
      contents: write # push the sync branch (PR-only flow)
      pull-requests: write # open or update the sync pull request
    uses: tannergolden/intelligence/.github/workflows/sync.yml@v0
    with:
      dry-run: ${{ inputs.dry-run || false }}
    # Only this one secret, never `secrets: inherit`: the hub's code needs
    # nothing else this repository holds.
    secrets:
      BOT_ACCESS_TOKEN: ${{ secrets.BOT_ACCESS_TOKEN }}
```

The stub calls the hub's reusable workflow,
[`sync.yml`](../../.github/workflows/sync.yml), at the moving major. That
workflow checks out the repository's default branch, runs the action in
[`.github/actions/sync/`](../../.github/actions/sync/README.md), which runs
`sync.py apply` from the hub tree at the same major, and hands the result to
the standards' open-pr action. That commits as the owner, signs off as the
owner, and opens or updates the pull request. The stub grants exactly the two
permissions the workflow asks for, and passes one optional secret,
`BOT_ACCESS_TOKEN`, never every secret the repository holds.

The action changes the working tree and nothing else:

| Input     | Default  | What it is                                                                                        |
| :-------- | :------- | :------------------------------------------------------------------------------------------------ |
| `token`   | required | Reads the repository's settings, to skip what takes no part; the default `GITHUB_TOKEN` is enough |
| `dry-run` | `false`  | Print what would change, and change nothing                                                       |

| Output         | What it is                                                               |
| :------------- | :----------------------------------------------------------------------- |
| `changed`      | `'true'` when the working tree now holds a change to propose             |
| `commit-title` | The Conventional Commit title, which is also the pull request's title    |
| `commit-body`  | Why the change is made, with no sign-off: whoever commits it signs off   |
| `pr-title`     | The pull request title                                                   |
| `pr-body`      | The pull request body, which says how its checks start and who merges it |

`@v0` is written out in the workflow too, because a reusable workflow cannot
name the ref it was called at. Moving `v0` delivers a release to both at once,
so the code that writes into a repository is always a released one, and a stub
pinned to a full version still runs the action at the moving major.

---

## 🚀 From The Hub

From the root of the hub, under your own `gh` login:

```bash
make audit                     # what every repository carries now
make sync ARGS=--dry-run       # what a sync would change
make sync                      # open or update one pull request per repository
make merge ARGS=--dry-run      # what would merge
make merge                     # merge the green ones whose diff is only the blocks
```

`make sync` delivers the latest release's blocks. To deliver unreleased rules
on purpose, pass `ARGS='--ref HEAD'`. To see what a repository's stub would
write, run `apply` in its checkout:

```bash
GITHUB_REPOSITORY=tannergolden/<name> python3 /path/to/intelligence/.github/scripts/sync.py apply --dry-run
```

---

## ✅ How Merging Works

`make merge` lands a sync pull request only when its diff is exactly the
blocks, in `AGENTS.md`, `docs/Prompts.md` or both, each block is the latest
release's, GitHub says it can merge, and its checks passed. A first sync, a
pull request that adds `docs/Prompts.md`, or anything bigger, waits for you.

GitHub holds the checks of a pull request the default `GITHUB_TOKEN` opened
until someone with write access approves them. Once `make merge` has proven
the diff is the block alone, it approves those waiting runs, falling back to
closing and reopening the pull request as you where approval fails, and it
merges on its next run once they pass. A first sync's checks start when you
select **Approve workflows to run** on it. A repository with a
`BOT_ACCESS_TOKEN` opens the pull request as that token's owner, and its checks
start at once.

The squash keeps the sync commit's body, sign-off included, so history still
says who certified the change.

---

## 🔗 See Also

- [ADR-0003](../adrs/ADR-0003-Push-Sync-&-Owner-Merge.md): the hub pushes, and the owner merges
- [ADR-0019](../adrs/ADR-0019-Each-Repository-Pulls-With-A-Stub.md): each repository pulls with a stub, on its own token
- [ADR-0025](../adrs/ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): every repository gets ready-made prompts beside the rules
- [Backstops & Residual Risk](../operations/Backstops-&-Residual-Risk.md): what a stub can reach, and the schedules GitHub stops
- [Troubleshooting Sync](../operations/Troubleshooting-Sync.md): what each line from `make audit`, `make sync`, `make merge` and a stub's run means

---

<div align="center">

**Each repository asks, and only you merge.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
