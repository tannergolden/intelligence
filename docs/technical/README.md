<!--
title: '🛠️ TECHNICAL'
description: 'How every part of the hub works, one document each: the home kit, repository sync, the prompts, cloud setup, skills and subagents, the loader probe and evals.'
type: index
keywords: [docs, architecture]
-->

<div align="center">

# 🛠️ TECHNICAL

<a name="top"></a>

**How every part of the hub works, one document each.**

_Start with How It Works._

</div>

---

## 💡 What This Folder Is For

Every explanation of how a part of the hub works lives here, and each folder's
README in the hub links to the document for its part. Start with [How It
Works](../introduction/How-It-Works.md), in
[`../introduction/`](../introduction/README.md), which shows how the pieces
fit, and follow its links.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                            | Purpose                                                                                                                                                                                                                            |
| :----------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`research/`](research/README.md)                | Filed research reports, one per question, each dated, sourced claim by claim, and linked to the decision it fed.                                                                                                                   |
| [`Cloud-Setup.md`](Cloud-Setup.md)               | The setup script that installs the universal rules and the kit into every Claude Code cloud session, pinned to one release and unable to fail the session.                                                                         |
| [`Evals.md`](Evals.md)                           | How each universal rule and prompt is measured: scenarios run against real apps, with the block and without it or with the prompt and the hurried request it replaces, and checked by code.                                        |
| [`Prompts.md`](Prompts.md)                       | The universal prompts the hub keeps in its own docs/Prompts.md for anyone to copy, most ready to run as they are, and the empty docs/Prompts.md each repository gets for prompts of its own: how each works, and how to change it. |
| [`README.md`](README.md)                         | This file.                                                                                                                                                                                                                         |
| [`Repository-Sync.md`](Repository-Sync.md)       | How each release reaches every repository: the stub a repository carries, make sync from the hub, what a first sync does, and how make merge lands the result.                                                                     |
| [`Skills-&-Subagents.md`](Skills-&-Subagents.md) | The one skill and the Worker and Reviewer subagents the home kit installs, the rules every skill here follows, and where each app reads them.                                                                                      |
| [`The-Home-Kit.md`](The-Home-Kit.md)             | What make agents installs into each AI app's home folder, the kit that rides beside the rules, the guard hook, and how a machine gets them from a release.                                                                         |
| [`The-Loader-Probe.md`](The-Loader-Probe.md)     | How the hub proves, on the machine that runs it, which instruction files each AI coding app actually loads, what it touches, and the results so far.                                                                               |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**One document per part, and every part explained.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
