<!--
title: '🧰 SETUP'
description: 'What you copy out of the hub once: the setup script for every Claude Code cloud session, and the stub that keeps a repository''s rules current.'
tags: [claude-code, cloud, setup-script, home-kit, github-actions, sync]
category: docs
-->

<div align="center">

# 🧰 SETUP

<a name="top"></a>

**The rules in every Claude cloud session, and in every repository that asks for them, each from a pinned release.**

_Set up once. Current after every release._

</div>

---

## 💡 What This Folder Is For

Two files you copy out of the hub, each to its own place:

| File                                             | Where it goes                                  | What it does                                                    |
| :----------------------------------------------- | :--------------------------------------------- | :-------------------------------------------------------------- |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | A Claude Code cloud environment's setup script | Installs the home copy and the kit into every cloud session     |
| [`intelligence-sync.yml`](intelligence-sync.yml) | A repository's `.github/workflows/`            | Proposes each release's block as one pull request, every Monday |

---

## ☁️ The Cloud Setup Script

A Claude Code cloud session starts in a fresh container, so nothing the home
kit installed on your machines is there. Each repository's own `AGENTS.md`
still carries the rules; this script adds the home copy, so a session in a
repository with no block of its own gets them too.

It downloads the home file, the kit and the installer from one release,
checks each against its pin, and installs Claude Code's share:

- `~/.claude/CLAUDE.md`, with the rules and the knowledge facts, each between
  their own markers;
- the guard hook, registered in `~/.claude/settings.json`;
- the skills in `~/.claude/skills/` and the subagents in `~/.claude/agents/`.

A kit that cannot be downloaded or misses its pin is left out, and the rules
still install; an empty kit pin, from a release before the kit, installs the
rules alone. **It always exits 0**: a setup script that fails stops the
session from starting, so every failure prints a notice instead.

### 🚀 Installing It

1. Cut a release, then print the script with that release's pins:

   ```bash
   make cloud-setup VERSION=v0.1.0
   ```

2. Paste the output into the cloud environment's settings: open the
   environment menu in a session's title bar, choose Edit, and put it under
   Setup script. New sessions run it.
3. After each new release, print it again and replace the old one.

The copy in this folder keeps placeholders where the pins go, and refuses to
install anything until they are filled.

---

## 🔁 The Intelligence Sync Stub

A repository that carries the stub keeps its rules current by itself. Every
Monday, and whenever you run it, it calls this hub's
[`sync.yml`](../.github/workflows/sync.yml) at `@v0`, which writes the latest
release's block into the repository's checkout and opens or updates one pull
request on `chore/intelligence`. It runs on the repository's own
`GITHUB_TOKEN`, and hands over one optional secret, `BOT_ACCESS_TOKEN`, never
every secret the repository holds.

### 🚀 Adding It To A Repository

1. Copy `intelligence-sync.yml` into the repository as
   `.github/workflows/intelligence-sync.yml`.
2. Let GitHub Actions create pull requests there, under Settings, Actions,
   General. 🎯 Apply Standards turns that on with the rest of the standard
   settings.
3. Run it once from the Actions tab, or wait for Monday.

GitHub holds the checks of a pull request the default token opened until
someone with write access approves them. `make merge` in the hub approves
them for a change that is only the block, and merges it on its next run. A
first sync waits for your review, where **Approve workflows to run** starts
its checks. `test_stub.py` keeps the stub, the workflow it calls and the
release that serves them in step.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                            | Purpose                                                                                                                                                                                       |
| :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | Install the universal rules into a Claude Code cloud session.                                                                                                                                 |
| [`intelligence-sync.yml`](intelligence-sync.yml) | Keeps the universal rules for AI coding agents current in this repository's root AGENTS.md: the block between the INTELLIGENCE markers, which tannergolden/intelligence renders and releases. |
| [`README.md`](README.md)                         | This file.                                                                                                                                                                                    |
| [`test_cloud_setup.py`](test_cloud_setup.py)     | Tests for the Claude cloud setup script.                                                                                                                                                      |
| [`test_stub.py`](test_stub.py)                   | Tests for the stub a repository carries, and the workflow and action it calls.                                                                                                                |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Every cloud session and every repository starts with the rules.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
