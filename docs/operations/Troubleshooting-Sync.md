<!--
title: '🩺 TROUBLESHOOTING SYNC'
description: 'What each line from make audit, make sync, make merge and a repository''s 🔁 Intelligence Sync means, and what to do about it. Read it when a repository''s rules are not current, its prompts page is missing, or a sync pull request will not merge.'
type: guide
-->

<div align="center">

# 🩺 TROUBLESHOOTING SYNC

<a name="top"></a>

**Every line a sync can print, what it means, and the fix.**

_Find the line. Read the row. Make the fix._

</div>

---

## 💡 Where To Look

- **`make audit`** prints one line per repository: `<name>: current`, or each
  thing it found, joined by `;`. It exits 1 while any repository has a finding.
- **`make sync` and `make merge`** print one line per repository too. Add
  `ARGS=--dry-run` to see each line without changing anything, and
  `ARGS='--repo <name>'` to work on one repository.
- **A repository's stub** logs to that repository's Actions tab, under
  🔁 Intelligence Sync. Run it by hand with `dry-run` on to see what it would
  write.

> [!TIP]
> **Fetch the tags first.** `make audit`, `make sync` and `make merge` read the
> releases from your checkout's own tags, so a checkout that has not fetched
> the newest one delivers an older block, and calls the newest one unknown. Run
> `git fetch --tags` in the hub before anything else on this page.

Before its own lines, each command prints `<name>: skipped, <reason>` for every
repository that takes no part: an archived one, a fork, a golden path template,
one with the `no-intelligence` topic, and the hub itself. Nothing is wrong with
those.

---

## 🔎 What make audit Finds

| The line says                                                          | What it means                                                             | What to do                                                                                                                                                |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no AGENTS.md`                                                         | The repository has never been synced                                      | `make sync ARGS='--repo <name>'`, then review the first sync by hand and merge it                                                                         |
| `AGENTS.md has no block`                                               | It has its own `AGENTS.md`, without the markers                           | The same. The first sync puts the block after the file's header and keeps everything else                                                                 |
| `the block was edited by hand`                                         | The text between the markers no longer matches the hash in its marker     | Move anything the edit was for out of the block, into the repository's own sections or an Overrides entry, then sync, which puts the release's block back |
| `the block is from vX.Y.Z`                                             | An older release's block                                                  | `make sync`, or wait for the stub's Monday run                                                                                                            |
| `the block is not one the hub ever released`                           | Its hash matches no release tag in your checkout                          | `git fetch --tags` and audit again. If it stays, the block came from `--ref`, and the next sync replaces it                                               |
| `a CLAUDE.md sits beside AGENTS.md, so Claude Code may skip AGENTS.md` | Claude Code may read `CLAUDE.md` in place of `AGENTS.md` there            | `make sync`, which folds `CLAUDE.md` into `AGENTS.md` and deletes it. Review that pull request by hand                                                    |
| `Overrides names <ID>, an Invariant, which nothing waives`             | The entry changes nothing: an Invariant holds whatever a repository says  | Delete the entry. If the rule itself is wrong, change it in the Constitution                                                                              |
| `Overrides names STD-001 without a reason`                             | The entry gives no reason                                                 | Write the reason after the ID: `- STD-001: <why>`                                                                                                         |
| `sync pull request #N is open`                                         | A sync waits to be merged                                                 | `make merge`, or review and merge it by hand                                                                                                              |
| `no docs/Prompts.md`                                                   | The repository has never had its prompts page                             | `make sync`, which adds the empty page. Review that pull request by hand                                                                                  |
| `more than one INTELLIGENCE block`                                     | Sync will not choose between two blocks                                   | Delete the extra block by hand                                                                                                                            |
| `<name>/<path> is a <type>, not a file; review it by hand`             | `AGENTS.md`, `CLAUDE.md` or `docs/Prompts.md` is a folder or a link there | Make it a plain file, by hand                                                                                                                             |

A line that ends in `(no stub, so only make sync updates it)` is not a fault:
the repository has no `.github/workflows/intelligence-sync.yml`, so it gets a
release only when you run `make sync`. To let it pull each release itself,
add the stub as [Repository Sync](../technical/Repository-Sync.md#-the-stub)
describes.

---

## 🔁 What make sync Says

| The line says                                                                         | What it means                                                                 | What to do                                                                                                                                |
| :------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| `the hub has no release yet: cut one, or pass --ref HEAD to deliver unreleased rules` | Your checkout has no `vX.Y.Z` tag                                             | `git fetch --tags`. If there is still none, cut a release, as [Releasing](../distribution/Releasing.md) describes                         |
| `<ref>:home/intelligence.md is not a sound home file`                                 | That ref's home file has no block, or one that does not match its marker      | With `--ref`, name another ref. For a release tag, cut a new release: Cut Release runs `make check`, which fails on a home file like that |
| `cannot list your repositories through gh: ...`                                       | `gh` is not logged in, or cannot reach GitHub; its own words follow the colon | `gh auth status`, then `gh auth login` if it asks                                                                                         |
| `<name>: current`                                                                     | The repository already carries this release's blocks                          | Nothing                                                                                                                                   |
| `<name>: would adopt (...)` or `would update (...)`                                   | A dry run, saying what a real one would write                                 | Run it without `--dry-run` when it reads right                                                                                            |
| `<name>: opened pull request #N`, or `updated pull request #N`                        | The sync is proposed                                                          | Review a first sync by hand; `make merge` lands the rest                                                                                  |
| `<name>: skipped, <branch> has no commits`                                            | The default branch is empty, so there is nothing to branch from               | Make a first commit there, then sync again                                                                                                |
| `<name>: <method> <path>: <what GitHub said>`                                         | GitHub refused a call                                                         | Read GitHub's words at the end of the line, which name the cause                                                                          |

A run with something to deliver moves `chore/intelligence` back to the
default branch's latest commit before it writes, so a commit pushed to that
branch by hand is gone after the next `make sync`. Keep other work off it.

---

## ✅ What make merge Says

`make merge` lands a pull request only when its diff is exactly the blocks,
each block is the latest release's, GitHub says it can merge, and its checks
passed. Every other case prints why:

| The line says                                                                                                | What it means                                                                                               | What to do                                                                                                                  |
| :----------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `no sync pull request`                                                                                       | Nothing is open from `chore/intelligence`                                                                   | Nothing                                                                                                                     |
| `#N changes more than the block; review it by hand`                                                          | It adds or deletes a file, touches a file other than `AGENTS.md`, or changes text outside the markers       | Review it and merge it by hand. A first sync, a folded `CLAUDE.md` and any change to `docs/Prompts.md` always land this way |
| The same, on a sync that only replaces the block                                                             | `AGENTS.md` changed outside the markers on the default branch after the pull request was opened             | `make sync ARGS='--repo <name>'`, which writes the branch again from the default branch                                     |
| `#N carries an older block; run its 🔁 Intelligence Sync, or make sync, first`                               | A newer release came out after the pull request was opened                                                  | Do as it says, then `make merge` again                                                                                      |
| `#N is not mergeable yet (<state>)`                                                                          | GitHub does not say yet that it can merge; the word in parentheses is GitHub's own                          | `make merge` again later, or open the pull request to see what holds it                                                     |
| `#N waited on its checks, so make merge approved its N waiting workflow run(s); run it again once they pass` | The stub opened it on the default `GITHUB_TOKEN`, and GitHub held its checks until someone approved them    | `make merge` again once the checks pass                                                                                     |
| `#N waited on its checks, so make merge reopened it, which starts its checks; run it again once they pass`   | Approving failed, or nothing was held, so it closed and reopened the pull request as you, which starts them | The same                                                                                                                    |
| `#N waits: checks still running: <names>`                                                                    | Its checks have not finished                                                                                | `make merge` again later                                                                                                    |
| `#N waits: checks failed: <names>`                                                                           | A check failed, and `make merge` never lands a red pull request                                             | Open the failed run in that repository and fix its cause                                                                    |
| `#N waits: commit status is <state>`                                                                         | A commit status, apart from the check runs, is not `success`                                                | The same                                                                                                                    |
| `#N waits: no checks ran, so there is nothing to trust`                                                      | No check ran, and no bot opened the pull request, so there is nothing held to start                         | A repository with no checks never merges this way: review and merge it by hand                                              |
| `would start the checks of #N`, `would merge #N`                                                             | A dry run                                                                                                   | Run it without `--dry-run`                                                                                                  |
| `merged #N`                                                                                                  | Squashed, keeping the sync commit's body and sign-off                                                       | Nothing                                                                                                                     |

---

## 🧷 When A Stub's Run Goes Wrong

| What you see                                                                                         | What it means                                                                                                                            | What to do                                                                                                                                      |
| :--------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| The run fails before any job starts, with no log                                                     | The stub grants less than the `contents: write` and `pull-requests: write` that `sync.yml` asks for: a `permissions:` block is a ceiling | Put the stub's `permissions:` back as [`setup/intelligence-sync.yml`](../../setup/intelligence-sync.yml) has them                               |
| The block is written, but the pull request step fails                                                | GitHub Actions may not create pull requests in that repository                                                                           | Allow it under Settings, Actions, General, or run 🎯 Apply Standards, which turns it on with the rest of the standard settings                  |
| The pull request is open, and its checks never start                                                 | The default `GITHUB_TOKEN` opened it, and GitHub holds its checks until someone with write access approves them                          | `make merge`, once it has proven the diff is the block alone; on a first sync, **Approve workflows to run**; or add a `BOT_ACCESS_TOKEN` secret |
| An Intelligence Sync error: `<name>: AGENTS.md is a link or a folder, not a file; review it by hand` | `apply` never writes through a link; the same goes for `CLAUDE.md` and `docs/Prompts.md`                                                 | Make it a plain file in that repository                                                                                                         |
| An Intelligence Sync error: `<name>: more than one INTELLIGENCE block`                               | Two blocks of one kind, and `apply` will not choose                                                                                      | Delete the extra block by hand                                                                                                                  |
| `<name>: skipped, <reason>`                                                                          | The repository takes no part                                                                                                             | Nothing, unless the `no-intelligence` topic is there by mistake                                                                                 |
| `<name>: current`, and no pull request                                                               | Nothing to deliver                                                                                                                       | Nothing                                                                                                                                         |
| The Monday runs stopped                                                                              | GitHub turns off scheduled workflows in a public repository after 60 days without activity                                               | Run its 🔁 Intelligence Sync by hand, or `make sync`. Until then, `make audit` names its older block                                            |

---

## 🔗 See Also

- [Repository Sync](../technical/Repository-Sync.md): how each route works, end to end
- [Files & Formats](../references/Files-&-Formats.md): the markers, the Overrides entry and the sync pull request, exactly
- [Backstops & Residual Risk](Backstops-&-Residual-Risk.md): what a stub can reach, and why it is trusted

---

<div align="center">

**Read what it printed. It already names the fix.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
