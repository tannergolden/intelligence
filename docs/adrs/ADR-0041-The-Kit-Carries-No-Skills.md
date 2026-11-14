<!--
title: '📄 ADR-0041: THE KIT CARRIES NO SKILLS'
description: 'The hub stops writing skills: the twelve department skills, their trigger tests and the probe''s skill canary are gone, the kit carries the guard alone in format 3, and every install takes out the skills and subagents earlier releases wrote.'
type: record
status: 'Proposed'
date: '2026-11-14'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0041: THE KIT CARRIES NO SKILLS

<a name="top"></a>

**The hub keeps the rules, the `AGENTS.md` they ride in and the sync that carries them. The skills leave.**

_What no release maintains, no machine keeps._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                                                                                                                                                                                                                                                  |
| :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                                                                                                                                                                                                                                        |
| **Consulted**  | Claude Code sessions: what the skills reached, and how to take them out of every home                                                                                                                                                                                                                          |
| **Informed**   | Everyone who installs the home kit, every cloud session that runs its setup, and everyone who ran the departments as skills or as Grok Bot agents                                                                                                                                                              |
| **Supersedes** | [ADR-0021](ADR-0021-Develop-Is-The-One-Skill.md), [ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md), [ADR-0038](ADR-0038-Each-Department-Is-A-Skill.md), [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md) and [ADR-0040](ADR-0040-Every-Agent-Belongs-To-A-Department.md): the skills and their teams |
| **Amends**     | [ADR-0012](ADR-0012-One-Pinned-Kit-For-Every-Module.md), whose one pinned kit now carries the guard alone                                                                                                                                                                                                      |

---

## 🎯 Context & Problem Statement

By [ADR-0040](ADR-0040-Every-Agent-Belongs-To-A-Department.md) the kit carried twelve department skills, each with a team of at most five, written in the hub ([ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md), [ADR-0039](ADR-0039-Twelve-Departments-Twelve-Skills.md)), beside the guard hook. They were almost all of `home/kit.json`, about 2.5 MB of its 2.7 MB, and machinery grew around them that served nothing else: the team and layout checks in `kit.py`, the validator and packager `research-and-development` carried and their tests, the trigger tests in `evals/skills/`, the loader probe's skill canary, and the installer's skill folders in three apps.

The owner decided on 2026-11-14 to take every skill out of the hub, for now, and keep it to the universal rules, the `AGENTS.md` every repository carries them in, and the sync that delivers them. The rules never named a skill, so the block, and every repository's copy of it, stay as they are, byte for byte.

Taking the sources away is not enough on its own. Releases v0.5.0 to v0.9.0 installed skills into `~/.agents/skills/`, `~/.claude/skills/` and Antigravity's skills folder, and v0.5.0 to v0.8.0 installed subagents for Claude Code, Copilot and Codex, on every machine that ran `make agents`. Nothing would ever update or remove those again. A cloud session starts fresh each time, so its setup script installs skills only while it stays pinned to one of those releases.

---

## 🚦 Decision Drivers

- **The owner's decision**: the hub keeps the rules, `AGENTS.md` and the sync, and no skills, for now.
- **No home keeps text that no release maintains**, so removing a module removes what it wrote, as [ADR-0023](ADR-0023-The-Kit-Carries-No-Facts.md) did for the facts.
- **The guard stays.** It is no skill: the Constitution names it as what enforces several Invariants and Defaults, from SEC-001 to DOC-002.
- **Nothing is lost.** The `v0.9.0` tag keeps every skill exactly as it last shipped.

---

## 🏗️ Considered Options

1. **Keep the skills.**
2. **Ship an empty set of skills**, and keep the machinery for when skills return.
3. **Remove the skills and the machinery around them**, and have every install take out what earlier releases wrote.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, remove the skills and their machinery, and take out what earlier releases wrote

### Rationale for Selection

- **`kit/skills/` is gone**, with the validator and packager `research-and-development` carried and their tests in `test_develop.py`. `kit.py` bundles the guard alone, and the kit's format moves to 3, so an installer from before reads a newer kit as the wrong format rather than as a kit missing its skills, as format 2 did for the facts.
- **The skill trigger tests are gone**: `evals/skills/`, and `evals.py`'s `--draw`, `--skill` and `--seen`. Every rule and every universal prompt keeps its scenario.
- **The loader probe's skill canary is gone**, with `--skills`. Its loader checks and controls stand.
- **Every install takes out each skill folder and subagent file an earlier release wrote**, with a kit or without, and the record of them; a folder the kit made for them goes too, once it is empty. Only what carries the kit's mark goes, so a skill or an agent of your own stays, whatever its name. `check` calls one left behind stale, and `uninstall` takes them out as it always has.
- **`.typos.toml` is gone**: every word on it was one only the skills carried.
- **`AGENTS.md` asks first** before any skill or subagent is added to the kit again.

Option 2 keeps code shaped around one design of skills, teams of five sized for a Grok Bot group of six and one skill's validator, that a future set would likely not share, and git history keeps it either way. Option 1 keeps what the owner does not want.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                                                                                     |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | `home/kit.json` shrinks from about 2.7 MB to about 120 KB; the hub holds only what serves the rules, `AGENTS.md` and the sync; a machine sheds every skill and subagent on its next install                                              |
| **Negative (-)** | No department skills on any machine after its next install, a knowledge vault's included, since it keeps none of its own ([ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md)); bringing skills back means building their machinery again |
| **Neutral (~)**  | No repository's `AGENTS.md` changes; the installer keeps a sweep for what earlier releases wrote, which a later release can drop once every machine has run it                                                                           |

---

## 🔗 Traceability & Links

- [The Home Kit](../technical/The-Home-Kit.md): what an install writes, and what it takes out
- [Files & Formats](../references/Files-&-Formats.md#-the-kit): the kit in format 3
- [ADR-0012](ADR-0012-One-Pinned-Kit-For-Every-Module.md): one pinned kit for every module, which this amends
- [ADR-0023](ADR-0023-The-Kit-Carries-No-Facts.md): the knowledge facts, taken out the same way
- [ADR-0040](ADR-0040-Every-Agent-Belongs-To-A-Department.md): the last shape of the skills and their teams, which this supersedes with ADR-0021, ADR-0037, ADR-0038 and ADR-0039
- [The skills as they last shipped](https://github.com/tannergolden/intelligence/tree/v0.9.0/kit/skills), in the `v0.9.0` release

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The rules, and the guard that enforces them.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
