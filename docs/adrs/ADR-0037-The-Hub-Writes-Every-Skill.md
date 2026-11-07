<!--
title: '📄 ADR-0037: THE HUB WRITES EVERY SKILL'
description: 'Every skill and agent the owner uses lives in the hub, written here and universal: the knowledge template keeps none, the five faculties stop being pinned copies, board and identify move in, the Agent Resources workforce becomes board''s team with at most six agents a department, and a vault supplies its layout through its AGENTS.md.'
type: record
status: 'Proposed'
date: '2026-11-07'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0037: THE HUB WRITES EVERY SKILL

<a name="top"></a>

**Every skill and every agent in one place, written for any repository.**

_No vault keeps instructions of its own; a vault says where things go._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                                              |
| :------------- | :--------------------------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                    |
| **Consulted**  | Claude Code sessions: the move, made at the owner's direction                                              |
| **Informed**   | Everyone who installs the home kit, and everyone who generates a vault from tannergolden/knowledge         |
| **Supersedes** | [ADR-0033](ADR-0033-The-Kit-Carries-The-Faculties.md), the faculties pinned from a release of the template |
| **Amends**     | [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md), which made `develop` the one skill the hub writes        |

---

## 🎯 Context & Problem Statement

The knowledge template held seven skills (`board`, `discover`, `editorial`, `finance`, `identify`, `research`, `visualize`), each with its team, plus the Agent Resources (AR) workforce of 57 agent files in `Ventures/Agent Resources (AR)/` and the Library's Librarian. Every one was written for a BRAIN vault: fixed folders such as `Profile/`, `Inbox/Reports/` and `Ventures/`, the vault's scripts, and a rule in each faculty that handed a home copy over to the vault's own. The hub carried five of them as pinned copies ([ADR-0033](ADR-0033-The-Kit-Carries-The-Faculties.md)), so a change to a faculty was made in the template, released there and pinned here.

The owner decided the knowledge repository should hold no agent instruction files at all, and that the skills and agents should be universal rather than written for one personal knowledge vault. Each department of the workforce keeps at most its six most critical agents.

---

## 🚦 Decision Drivers

- **One place for every skill and agent**, edited where it ships.
- **Universal**: a skill works in any repository, or in a conversation with no repository, and never assumes a vault's layout.
- **A vault still works**, with the skills placing their work where the vault keeps it.
- **No personal context in a repository** that was not made to hold it (SEC-003).
- **Each team stays lean**: at most six agents, its lead included.

---

## 🏗️ Considered Options

1. **Keep the pinned copies**, and only move `board`, `identify` and the workforce.
2. **Move every skill into the hub, universal**, with a vault naming its layout in its `AGENTS.md`.
3. **Move every skill into the hub, and sync vault-specific copies back** into each vault.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, every skill in the hub, universal

### Rationale for Selection

- **The hub authors every skill in `kit/skills/`.** `faculties.py`, `kit/faculties.json` and `make faculties` are gone. Each skill's trigger test in `evals/skills/` is drawn from the one it ships in `assets/trigger-evals.json` by `evals.py --draw`, and `evals.py --check` fails when the two differ; `develop`'s stays written here.
- **The skills are universal.** Where a skill persists anything is set by the repository's own instructions, which it reads first. With none, it works in the conversation and writes a file only where the user asks. Personal context goes only into a repository whose instructions say it was made to hold it.
- **`board` keeps the AR workforce as its team**, in its `agents/` folder: one roster per department, at most six agents each, its lead included. `kit.py` holds every skill, agent and team to `develop`'s validator and refuses any team over six, a skill's own team included.
- **`identify` keeps its interview** and writes the approved profile only into a repository made to hold it; anywhere else it returns the profile in the conversation.
- **Every team keeps its six most critical agents.** The `research` team drops from eleven to six and `finance` from nine to six, each retired seat's duties folded into a survivor; the vault's Librarian retires with them, and a repository's reference collection is searched by the research team's analysts.
- **The hand-over rule and the loader probe's `--handover` canary are retired**: no vault keeps a copy for a home copy to give way to.
- **A vault supplies its layout** in its own `AGENTS.md`: where ventures, reports, ideas, visuals and profile facets go, and which checks to run after a write.

Option 1 leaves five skills written for a vault and keeps a release round-trip for every change. Option 3 puts agent files back in every vault, which the owner ruled out.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                               |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One place to change any skill or agent; every skill works in every repository; departments stay lean, and a check holds them there |
| **Negative (-)** | A vault with no home kit installed has no skills; a vault's owner can no longer change a skill in the vault alone                  |
| **Neutral (~)**  | The template's releases no longer feed the hub, so nothing here pins a version of it                                               |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Pinned Copies

- ✅ The smallest change
- ❌ Five skills stay written for a vault, and every change makes a round trip through a release

### Option 2: Every Skill In The Hub, Universal

- ✅ One source, universal skills, and the vault's layout stated once, in its own `AGENTS.md`
- ❌ A vault depends on the home kit for its skills

### Option 3: Sync Copies Back Into Every Vault

- ✅ A vault works with nothing installed
- ❌ Puts agent files back in every vault, which the owner ruled out

---

## 🔗 Traceability & Links

- [Skills & Subagents](../technical/Skills-&-Subagents.md): every skill the kit carries
- [ADR-0033](ADR-0033-The-Kit-Carries-The-Faculties.md): the pinned faculties this record replaces
- [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md): `develop`, which builds and checks every skill here

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Every skill written once, here, for any repository.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
