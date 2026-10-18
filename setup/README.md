<!--
title: '☁️ CLOUD SETUP'
description: 'The setup script that installs the universal rules into every Claude Code cloud session, pinned to one release and unable to fail the session.'
tags: [claude-code, cloud, setup-script, home-kit]
category: docs
-->

<div align="center">

# ☁️ CLOUD SETUP

<a name="top"></a>

**The universal rules in every Claude cloud session, from a pinned release, without ever stopping a session from starting.**

_Pinned at the source. Silent when it cannot help._

</div>

---

## 💡 What This Folder Is For

A Claude Code cloud session starts in a fresh container, so nothing the home
kit installed on your machines is there. Each repository's own `AGENTS.md`
still carries the rules; this script adds the home copy, so a session in a
repository with no block of its own gets them too.

It downloads the home file and the installer from one release, checks each
against its pin, and writes `~/.claude/CLAUDE.md`. **It always exits 0**:
a setup script that fails stops the session from starting, so every failure
prints a notice instead.

---

## 🚀 Installing It

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

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                            | Purpose                                                       |
| :----------------------------------------------- | :------------------------------------------------------------ |
| [`claude-cloud-setup.sh`](claude-cloud-setup.sh) | Install the universal rules into a Claude Code cloud session. |
| [`README.md`](README.md)                         | This file.                                                    |
| [`test_cloud_setup.py`](test_cloud_setup.py)     | Tests for the Claude cloud setup script.                      |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Every cloud session starts with the rules, or starts anyway.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
