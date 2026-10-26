<!--
title: '📄 ADR-0033: THE KIT CARRIES THE FACULTIES'
description: 'The home kit carries the knowledge template''s five faculty skills beside develop, each copied by script from one release of the template, pinned by hash, held to its pin by make lint, and refused without the rule that hands a home copy over to a vault''s own.'
type: record
status: 'Proposed'
date: '2026-10-26'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0033: THE KIT CARRIES THE FACULTIES

<a name="top"></a>

**The template's five faculties in every repository, written once, in the template.**

_Copied by script, pinned by hash, and giving way in a vault._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                              |
| :------------ | :--------------------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                    |
| **Consulted** | Claude Code sessions: where each app reads skills, how the faculties reach a vault, and the change itself  |
| **Informed**  | Everyone who installs the home kit, and everyone who generates a vault from tannergolden/knowledge         |
| **Amends**    | [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md), which left the template's other skills with the template |

---

## 🎯 Context & Problem Statement

[ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md) made `develop` the hub's one universal skill and left the knowledge template's other skills with the template, where their folders and teams are. Five of them are faculties, each the lead of a standing team: `research`, `discover`, `editorial`, `visualize` and `finance`. None of them ever ran. The template kept them where no app reads a repository's skills, a gap the template's own ADR-0003 closes by moving them to `.agents/skills/`, with a generated copy in `.claude/skills/` for Claude Code.

The owner wants the faculties wherever they work, not only in a vault: in their dotfiles, in code repositories, in every app, installed by the home kit as every other skill is. And a vault generated from the template, by anyone, has to keep working with nothing installed. Claude Code loads a person's skill over a repository's of the same name, so a home copy of a faculty would run in a vault in place of the vault's own, which matches the vault's layout and may hold its owner's changes.

---

## 🚦 Decision Drivers

- **One source for each faculty**, in the template, beside the vault layout it names.
- **Installed like every other skill**, through the same check, bundle, installer and pin.
- **No hand edits in the hub**, so the copy every machine installs is exactly a release's.
- **Inside a vault, the vault's own copy runs**, whichever copy an app loaded.
- **Proven, not assumed**: a model following a rule is a claim the probe can test.

---

## 🏗️ Considered Options

1. **Keep `develop` the only skill the kit carries**, and leave the faculties in vaults.
2. **Move the faculties into the hub**, authored in `kit/skills/`, with Intelligence Sync writing them into every vault.
3. **Copy each faculty from a release of the template**, by script, into `kit/skills/`, pinned by hash and checked by `make lint`, with a rule in each faculty that hands a home copy over to a vault's.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, a pinned copy of each faculty

### Rationale for Selection

The template stays the one place a faculty is written, so a faculty and the layout it works in always change together, and a vault takes both through 🔄 Template Sync. The hub carries a copy for everywhere else, and treats it as it treats `home/`: generated, never edited.

- **`.github/scripts/faculties.py --pin VERSION`** downloads each faculty's `.skill` archive from that release tag of the template, or with `--from` reads it from the tag in a clone, never from what the clone has checked out, and replaces the copy in `kit/skills/<name>/`, its team in `agents/` included. It refuses a file outside the skill's folder, more than one folder deep, too large or not text, a file git would ignore, a skill with no trigger test, a name the hub already uses for a skill of its own, and a faculty that does not open with the hand-over rule. It writes everything aside before moving any of it into place, so a refused or failed release changes nothing.
- **`kit/faculties.json`** records the release, and for each faculty the SHA-256 of its archive and of its files. `faculties.py --check`, run by `make lint`, fails when a copy, or the trigger test drawn from it, differs from the pin.
- **Each faculty's trigger test** is drawn into `evals/skills/<name>.json` from the one it ships in `assets/trigger-evals.json`, so `evals.py` measures it like `develop`'s.
- **The hand-over** is one rule each faculty opens with: in a BRAIN vault, the vault's own copy runs, so a copy loaded from anywhere else reads the vault's and follows it. Outside a vault, a faculty works in the conversation and writes nothing about its user into the repository. `faculties.py` holds the rule word for word, and the loader probe's `--handover` canary plants it at home and in a scratch vault to prove each app follows the vault's copy, beside a control with no rule. Its first run, on Claude Code 2.1.310, passed both: with the rule, Claude Code followed the vault's copy, and without it, the home one.

Option 1 leaves the faculties out of every repository but a vault. Option 2 makes the hub the author of skills whose steps name the vault's folders, so a faculty and its layout would change in different repositories, and widens Intelligence Sync from one block to skill folders in every vault.

### What Changed

| Was                                         | Is now                                                                                          |
| :------------------------------------------ | :---------------------------------------------------------------------------------------------- |
| `develop`, the one skill the kit holds      | `develop`, the one the hub writes, and the five faculties copied from a release of the template |
| No faculty outside a vault                  | `kit/skills/<name>/`, written by `faculties.py --pin` and held to `kit/faculties.json`          |
| Trigger tests written in the hub            | A faculty's drawn from the one it ships, and checked with its copy                              |
| A skill canary in the probe                 | A hand-over canary beside it, `--handover`, run in a scratch vault                              |
| develop: never one skill name at two levels | The same, except a skill that opens with a rule settling which copy runs, as each faculty does  |

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                                                                   |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | The faculties reach every repository and every app on the owner's machines; each is written once; a hand edit to a copy fails CI; a vault's own copy still decides inside it                                           |
| **Negative (-)** | The kit grows by five skills and their teams, and every session in every app lists five more descriptions; a faculty change reaches a machine only through a template release, a pin here and a hub release            |
| **Neutral (~)**  | The pin names no release until the template releases its `.agents/skills/` layout, so the kit carries `develop` alone until then; dotfiles changes nothing but its pin; the hub now depends on the template's archives |

---

## ⚖️ Trade-off Comparative

### Option 1: Develop Alone

- ✅ The smallest kit, and nothing new to keep in step
- ❌ The faculties work only inside a vault

### Option 2: Author The Faculties Here

- ✅ One release carries a faculty everywhere
- ❌ A faculty and the vault layout it names change apart, and sync writes skill folders into every vault

### Option 3: A Pinned Copy Of Each

- ✅ One source, the layout's own, and a copy no one can edit by hand
- ❌ Three releases between a change and a machine, and a coupling to the template's archive path and to the rule's wording

---

## 🔗 Traceability & Links

- [`.github/scripts/faculties.py`](../../.github/scripts/faculties.py): the copier and its check, tested in [`test_faculties.py`](../../.github/scripts/test_faculties.py)
- [`kit/faculties.json`](../../kit/faculties.json): the pin
- [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md): `develop`, the one skill the hub writes
- [Skills & Subagents](../technical/Skills-&-Subagents.md#the-faculties): the faculties and the hand-over
- [The Loader Probe](../technical/The-Loader-Probe.md): the hand-over canary
- tannergolden/knowledge's ADR-0003, which keeps the skills where the apps read them

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Written once in the template, carried everywhere, and yielding in a vault.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
