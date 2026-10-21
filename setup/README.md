<!--
title: '🧰 SETUP'
description: 'What leaves the hub for somewhere else: the setup script for every Claude Code cloud session, the stub that keeps a repository''s rules current, and the empty prompts page every repository gets.'
type: index
keywords: [claude-code, cloud, setup-script, home-kit, github-actions, sync]
-->

<div align="center">

# 🧰 SETUP

<a name="top"></a>

**The rules in every Claude cloud session, and in every repository that asks for them, each from a pinned release.**

_Set up once. Current after every release._

</div>

---

## 💡 What This Folder Is For

Three files that leave the hub, each for its own place: two you copy out
once, and one sync delivers:

| File                                             | Where it goes                                                           | Read more                                               |
| :----------------------------------------------- | :---------------------------------------------------------------------- | :------------------------------------------------------ |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | A Claude Code cloud environment's setup script, copied by you           | [Cloud Setup](../docs/technical/Cloud-Setup.md)         |
| [`intelligence-sync.yml`](intelligence-sync.yml) | A repository's `.github/workflows/`, as `intelligence-sync.yml`, by you | [Repository Sync](../docs/technical/Repository-Sync.md) |
| [`Prompts.md`](Prompts.md)                       | Every repository's `docs/`, written once by sync, then the repository's | [Prompts](../docs/technical/Prompts.md)                 |

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                            | Purpose                                                                                                                                                                                       |
| :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | Install the universal rules into a Claude Code cloud session.                                                                                                                                 |
| [`intelligence-sync.yml`](intelligence-sync.yml) | Keeps the universal rules for AI coding agents current in this repository's root AGENTS.md: the block between the INTELLIGENCE markers, which tannergolden/intelligence renders and releases. |
| [`Prompts.md`](Prompts.md)                       | Prompts for working in this repository with an AI agent, written for it. Copy one, fill in any details it asks for, and paste it into your agent.                                             |
| [`README.md`](README.md)                         | This file.                                                                                                                                                                                    |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Every cloud session and every repository starts with the rules.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
