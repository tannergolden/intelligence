<!--
title: '🛡️ OPERATIONS & SECURITY'
description: 'Keeping the hub and everything it reaches healthy: the server-side backstops behind the rules, the risks that remain, and what to do when a sync, an install or the guard reports a problem.'
type: index
keywords: [docs, risk, security, troubleshooting]
-->

<div align="center">

# 🛡️ OPERATIONS & SECURITY

<a name="top"></a>

**Keeping the hub healthy and safe.**

_The backstops, the risks, and the fixes._

</div>

---

## 💡 What This Folder Is For

The documents here are about keeping the hub safe once it runs, rather than how
it works: the controls behind the rules, the risks that remain with every one
of them on, and what to do when a sync, a merge, an install or the guard
reports a problem. How a release ships lives in
[`../distribution/`](../distribution/README.md), and how each part works in
[`../technical/`](../technical/README.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                                                | Purpose                                                                                                                                                                                                                                                                                                            |
| :------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`Backstops-&-Residual-Risk.md`](Backstops-&-Residual-Risk.md)       | The server-side controls behind the universal rules, how to apply them to each repository, and the risks that remain once they are on.                                                                                                                                                                             |
| [`README.md`](README.md)                                             | This file.                                                                                                                                                                                                                                                                                                         |
| [`Troubleshooting-Sync.md`](Troubleshooting-Sync.md)                 | What each line from make audit, make sync, make merge and a repository's &#x1F501; Intelligence Sync means, and what to do about it. Read it when a repository's rules are not current, its prompts page is missing, or a sync pull request will not merge.                                                        |
| [`Troubleshooting-The-Home-Kit.md`](Troubleshooting-The-Home-Kit.md) | What the installer, its check, the Claude cloud setup script and the guard hook print when something on a machine is wrong, and what to do about each. Read it when make agents-check is not all current, a cloud session starts without the rules, the guard blocks a call, or Claude Code asks before an action. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Say what it cannot stop.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
