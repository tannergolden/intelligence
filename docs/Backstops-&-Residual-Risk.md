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
a change outside the prompt.

| Risk                                                                                                                                                                                           | What would close it                                                                                                                       |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code cloud sessions push with your own token.** A ruleset your account can bypass does not stop them, and with zero required approvals an agent can merge its own green pull request. | Remove the admin bypass from the integration rulesets, or give unattended work an identity with no bypass, such as Copilot's cloud agent. |
| **The DCO check counts `Signed-off-by:` lines without checking whose they are.** A commit signed off by an AI passes it.                                                                       | A rule in the standards' commit check that rejects an AI author, and a sign-off that differs from the author.                             |
| **The standards' documented fallback, `git commit -s --author=<you>`, signs off as the committer.** In an agent session the committer is the agent, so it produces an AI sign-off.             | Change the recipe to add the contributor's `Signed-off-by:` trailer explicitly.                                                           |
| **No gate reads the author field.** Nothing stops a commit authored by an AI from landing.                                                                                                     | The same commit-check rule.                                                                                                               |
| **Scheduled workflows in a public repository stop after 60 days without activity.**                                                                                                            | Nothing in this plan depends on a schedule: syncs run when you run them.                                                                  |

Until those land, treat a cloud session as yourself: use it interactively,
and review what it pushes before you merge it.

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
