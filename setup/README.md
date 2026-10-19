<!--
title: '🧰 SETUP'
description: 'What you copy out of the hub once: the setup script for every Claude Code cloud session, and the stub that keeps a repository''s rules current.'
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

Two files you copy out of the hub, each to its own place:

| File                                             | Where it goes                                                   | Read more                                               |
| :----------------------------------------------- | :-------------------------------------------------------------- | :------------------------------------------------------ |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | A Claude Code cloud environment's setup script                  | [Cloud Setup](../docs/technical/Cloud-Setup.md)         |
| [`intelligence-sync.yml`](intelligence-sync.yml) | A repository's `.github/workflows/`, as `intelligence-sync.yml` | [Repository Sync](../docs/technical/Repository-Sync.md) |

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
