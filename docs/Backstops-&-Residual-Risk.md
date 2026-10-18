<!--
title: '🛡️ BACKSTOPS & RESIDUAL RISK'
description: 'The server-side controls behind the universal rules, how to apply them to each repository, and the risks that remain once they are on.'
tags: [security, rulesets, github, risk]
category: docs
-->

<div align="center">

# 🛡️ BACKSTOPS & RESIDUAL RISK

<a name="top"></a>

**What stops an agent when the rules do not, how to switch it on, and what it still cannot stop.**

_Prose asks. Rulesets refuse._

</div>

---

## 💡 What This Covers

The universal rules tell an agent what not to do, and the evidence is plain
that prose cannot reliably make an agent stop. So every Invariant that can
be enforced outside the prompt names its enforcer in its file under
[`law/rules/`](../law/rules/README.md), and this page covers the ones that
live on GitHub's side. Phase v0.4 is done when, in a repository with these
on:

- a direct push to `Development` is refused;
- a force-push is refused;
- a commit carrying a test token fails the `secrets` check.

---

## 🛡️ Switching The Rulesets On

🎯 Apply Standards, a workflow every repository from the templates already
carries, writes the rulesets: a pull request required, force-pushes and
deletion blocked, and the required checks `ci`, `secrets` and `pr`. Run it in
each repository:

1. Add an `ADMIN_TOKEN` secret: a fine-grained token scoped to your
   repositories, with **Administration: Read and write** and nothing else.
2. Run 🎯 Apply Standards from the Actions tab with `dry-run` on, and read
   the plan it prints.
3. Run it again with `dry-run` off.

| Repository visibility | On GitHub Free                         | On GitHub Pro       |
| :-------------------- | :------------------------------------- | :------------------ |
| Public                | Rulesets and push protection both work | Same                |
| Private               | No rulesets and no required checks     | Rulesets and checks |

Private repositories on a personal account get no GitHub secret scanning on
any plan, so `gitleaks` in the `secrets` check is their only secret gate.

---

## ⚠️ What Remains

These hold even with every ruleset on. None is fixed by wording; each needs
a change outside the prompt, and the right-hand column says how far that
change has come.

| Risk                                                                                                                                                                                                            | What closes it, and where it stands                                                                                                                                                                                                                                                                                      |
| :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code cloud sessions push with your own token.** A ruleset your account can bypass does not stop them, and with zero required approvals an agent can merge its own green pull request.                  | **Narrowed:** the cloud setup script installs the guard hook, which denies pushes to protected branches, force-pushes without a lease, and merges by `gh`, the REST API or a GitHub MCP tool. **Still open:** remove the admin bypass from the integration rulesets, or give unattended work an identity with no bypass. |
| **The DCO check counts `Signed-off-by:` lines without checking whose they are.** A commit signed off by an AI passes it.                                                                                        | **Closed in the standards:** the commit check rejects an AI author and a sign-off that is not the author's; it reaches a repository with the standards' next release. Locally, the guard denies such a commit before it is made.                                                                                         |
| **The standards' documented fallback, `git commit -s --author=<you>`, signs off as the committer.** In an agent session the committer is the agent, so it produces an AI sign-off.                              | **Closed:** the standards now add the contributor's `Signed-off-by:` trailer explicitly, and the guard denies `-s` whenever git's identity is an AI's.                                                                                                                                                                   |
| **No gate reads the author field.** Nothing stops a commit authored by an AI from landing.                                                                                                                      | **Closed** by the same commit-check rule, and by the guard before the commit exists.                                                                                                                                                                                                                                     |
| **The guard reads commands the way a reviewer would, not the way a shell does.** A command built to hide its intent gets past it, and in Codex and Antigravity a guard that cannot start lets the call through. | Nothing in the prompt can close this. The rulesets and CI stay the real gates; the guard catches the honest mistake first, and `make agents-check` reports a guard whose Python is gone.                                                                                                                                 |
| **Scheduled workflows in a public repository stop after 60 days without activity.**                                                                                                                             | Only the weekly repair in `sync.yml` is scheduled. Releases still reach every repository, because Cut Release calls the sync itself.                                                                                                                                                                                     |

Until the open row closes, treat a cloud session as yourself: use it
interactively, and review what it pushes before you merge it.

---

## 🔗 See Also

- [The law](../law/README.md): every rule, with what enforces it today and what is still to add
- [ADR-0011](adrs/ADR-0011-The-Universal-Rule-Set.md): why the rule set looks the way it does
- [Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md)

---

<div align="center">

**Where the prompt ends, the server takes over.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
