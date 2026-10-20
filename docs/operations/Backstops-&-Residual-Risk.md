<!--
title: '🛡️ BACKSTOPS & RESIDUAL RISK'
description: 'The server-side controls behind the universal rules, how to apply them to each repository, and the risks that remain once they are on.'
type: guide
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
be enforced outside the prompt names its enforcer under its ID in
[`CONSTITUTION.md`](../../CONSTITUTION.md), and this page covers the ones that
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

| Risk                                                                                                                                                                                                                                                                                                                                                             | What closes it, and where it stands                                                                                                                                                                                                                                                                                      |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code cloud sessions push with your own token.** A ruleset your account can bypass does not stop them, and with zero required approvals an agent can merge its own green pull request.                                                                                                                                                                   | **Narrowed:** the cloud setup script installs the guard hook, which denies pushes to protected branches, force-pushes without a lease, and merges by `gh`, the REST API or a GitHub MCP tool. **Still open:** remove the admin bypass from the integration rulesets, or give unattended work an identity with no bypass. |
| **The DCO check counts `Signed-off-by:` lines without checking whose they are.** A commit signed off by an AI passes it.                                                                                                                                                                                                                                         | **Closed in the standards:** the commit check rejects an AI author and a sign-off that is not the author's; it reaches a repository with the standards' next release. Locally, the guard denies such a commit before it is made.                                                                                         |
| **The standards' documented fallback, `git commit -s --author=<you>`, signs off as the committer.** In an agent session the committer is the agent, so it produces an AI sign-off.                                                                                                                                                                               | **Closed:** the standards now add the contributor's `Signed-off-by:` trailer explicitly, and the guard denies `-s` whenever git's identity is an AI's.                                                                                                                                                                   |
| **No gate reads the author field.** Nothing stops a commit authored by an AI from landing.                                                                                                                                                                                                                                                                       | **Closed** by the same commit-check rule, and by the guard before the commit exists.                                                                                                                                                                                                                                     |
| **The guard reads commands the way a reviewer would, not the way a shell does.** A command built to hide its intent gets past it, and in Codex and Antigravity a guard that cannot start lets the call through. It sees Claude Code's `Read` calls but not `Grep` or `Glob`, so a search can still print a line from a credential store.                         | Nothing in the prompt can close this. The rulesets and CI stay the real gates; the guard catches the honest mistake first, and `make agents-check` reports a guard whose Python is gone.                                                                                                                                 |
| **Cursor runs the guard from Claude Code's settings, and Cursor's hooks fail open.** A guard that cannot start, crashes or times out lets Cursor's call through, where Claude Code's own registration blocks it.                                                                                                                                                 | **Open:** Cursor documents `failClosed` only for hooks in its own `hooks.json`, and nothing shows it reads the field from Claude Code's settings, so the kit does not set it there. A registration in Cursor's own `hooks.json` would close it.                                                                          |
| **Claude Code's ask rules match a command as it is usually typed.** `git -C . push`, `bash -c 'git push'`, or a GitHub MCP server added under a name other than `github`, gets past them, and they reach only a machine's own install, not a cloud session.                                                                                                      | The guard still denies the pushes, merges and deletions OPS-001 forbids, in any spelling. The rest is left to OPS-005 itself and to the rulesets.                                                                                                                                                                        |
| **Scheduled workflows in a public repository stop after 60 days without activity.**                                                                                                                                                                                                                                                                              | Each stub's Monday run is the only schedule. A public repository that goes quiet stops pulling; `make audit` names its older block, and `make sync`, or running its sync by hand, brings it current.                                                                                                                     |
| **A stub runs the hub's code with write access.** Every repository that carries it runs `.github/actions/sync` at the moving `v0` with `contents: write` and `pull-requests: write`. A bad release could push a branch or open a pull request in each of them, and in a private repository on GitHub Free, where no ruleset applies, push to its default branch. | Only you cut releases, from 🏷️ Cut Release, and a release is the unit of trust: a stub pinned to a full version still runs the action at the moving major. The stub hands over no secret but an optional `BOT_ACCESS_TOKEN`, and its token reaches that one repository for one run.                                      |

Until the open row closes, treat a cloud session as yourself: use it
interactively, and review what it pushes before you merge it.

---

## 🔗 See Also

- [The Constitution](../../CONSTITUTION.md): every rule, with what enforces it today and what is still to add
- [ADR-0011](../adrs/ADR-0011-The-Universal-Rule-Set.md): why the rule set looks the way it does
- [Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md)

---

<div align="center">

**Where the prompt ends, the server takes over.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
