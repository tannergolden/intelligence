<!--
title: '🗺️ ROADMAP'
description: 'Each phase of the plan and each module held back until after 1.0: what it delivers, what finishes it, and where it stands.'
type: record
keywords: [phases, modules, status]
-->

<div align="center">

# 🗺️ ROADMAP

<a name="top"></a>

**Every phase and module, what finishes it, and where it stands.**

_Built is not proven. A release and a probe run prove it._

</div>

---

## 🧭 The Phases

| Phase                     | Delivers                                                                                                       | Done when                                                                                                         | Status                                                 |
| :------------------------ | :------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| **0. Prove the loaders**  | The [loader probe](../technical/The-Loader-Probe.md)                                                           | Every app you use reads its home copy and a repository's AGENTS.md, headless and by hand, and every control holds | Claude Code passes; the other apps run on your machine |
| **v0.1. The rules**       | The rules, in [the Constitution](../../CONSTITUTION.md); `render.py`; its tests                                | Two renders are byte-identical, and the block stays under its cap                                                 | Built                                                  |
| **v0.2. The home kit**    | `install.py`; dotfiles' `make agents`, `make agents-check` and `make agents-uninstall`; the cloud setup script | The probe passes on macOS, Linux, a Codespace and a Claude cloud session, and uninstalling restores every file    | Built; proven on a machine after the first release     |
| **v0.3. Repository sync** | `make audit`, `make sync` and `make merge`                                                                     | One release reaches every repository as one pull request each, merged by one command                              | Built; the first sync is yours to run                  |
| **v0.4. Backstops**       | Rulesets through 🎯 Apply Standards, and the [risks that remain](Backstops-&-Residual-Risk.md)                 | A direct push and a force-push to `Development` are both refused                                                  | Written up; the rulesets need your `ADMIN_TOKEN`       |
| **v1.0. Freeze**          | Rule IDs, the marker format and file paths, frozen once two releases pass v0.2 to v0.4                         | One release ships with one review, one `make sync`, one `make merge` and a green probe                            | After two releases                                     |

---

## 🧩 The Modules

The modules the plan held back until after 1.0 are built, each with its own
passing tests and a record in [`docs/adrs/`](../adrs/README.md):

| Module                    | Delivers                                                                                 | Status                                                   |
| :------------------------ | :--------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| **Guard hooks**           | The [guard](../technical/The-Home-Kit.md), registered for every app by the installer     | Built; first loads with the release that carries the kit |
| **Skills**                | One skill, [`develop`](../technical/Skills-&-Subagents.md), and the probe's skill canary | Built; run `make probe ARGS=--skills` on your machine    |
| **The hierarchy**         | The [Worker and Reviewer](../technical/Skills-&-Subagents.md) subagents                  | Built                                                    |
| **Knowledge**             | The [public facts](../technical/Knowledge.md), beside every home copy of the rules       | Built; the private tier waits                            |
| **Evals**                 | [Scenarios for every rule](../technical/Evals.md), run with the block and without it     | Built; real runs are yours, `make evals`                 |
| **Unattended sync**       | A [stub](../technical/Repository-Sync.md) in each repository, on its own token           | Built; copy the stub in after the first release          |
| **Machined-region check** | The standards' check that a block's hash matches its text, in every repository's CI      | Built in tannergolden/standards                          |

---

## 🔗 See Also

- [Releasing](Releasing.md): the steps each release takes
- [Decisions](../adrs/README.md): every decision behind the plan

---

<div align="center">

**Every phase finished by proof, not by assertion.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
