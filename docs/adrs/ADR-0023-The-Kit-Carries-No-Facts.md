<!--
title: '📄 ADR-0023: THE KIT CARRIES NO FACTS'
description: 'The home kit no longer installs public facts beside the rules: knowledge/ is gone, the kit carries the guard, the skills and the subagents in format 2, and an install takes out the facts an earlier release wrote.'
type: record
status: 'Proposed'
date: '2026-10-20'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0023: THE KIT CARRIES NO FACTS

<a name="top"></a>

**The rules go beside every app's home; the facts about the setup no longer do.**

_What no release maintains, no machine keeps._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute      | Specification                                                                    |
| :------------- | :------------------------------------------------------------------------------- |
| **Deciders**   | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner          |
| **Consulted**  | Claude Code sessions: what the facts fed, and how to take them out of every home |
| **Informed**   | Everyone who installs the home kit, and every cloud session that runs its setup  |
| **Supersedes** | [ADR-0016](ADR-0016-Knowledge-Starts-As-Public-Facts.md), the public facts       |

---

## 🎯 Context & Problem Statement

[ADR-0016](ADR-0016-Knowledge-Starts-As-Public-Facts.md) started knowledge as eight public facts about how the owner's setup works, kept in `knowledge/public.json` and rendered as a marked block beside every home copy of the rules and in the cloud setup. The owner decided the hub does not need them. A person's context already has its home in their knowledge vault, as [ADR-0020](ADR-0020-One-Constitution.md) records, and a fact about one repository belongs in that repository's `AGENTS.md`, which an agent reads with the task.

Taking the source away is not enough on its own. Every machine that installed a release with the facts holds them in up to six places, two of them files of their own, and nothing would ever maintain or remove that text again.

---

## 🚦 Decision Drivers

- **The owner's decision**: the facts are not needed.
- **A fact about a repository lives with that repository**, in its `AGENTS.md`.
- **No home keeps text that no release maintains**, so removing a module removes what it wrote.

---

## 🏗️ Considered Options

1. **Keep the facts.**
2. **Remove the facts**, and leave the blocks earlier releases wrote.
3. **Remove the facts**, and have the installer take out what earlier releases wrote.

---

## ✅ Decision Outcome

**Chosen Option**: Option 3, remove the facts and take out what earlier releases wrote

### Rationale for Selection

`knowledge/`, its page and its renderer go, and the kit carries the guard, the skills and the subagents. Its format moves to 2, so an installer from before reads a newer kit as the wrong format rather than as a kit missing a key.

`.github/scripts/install.py` keeps the places the facts went as `RETIRED`. An install takes out each facts block and file an earlier release wrote, puts back the separator it added, and drops the record of it; a dry run only reports what it would take out. `check` calls a block left behind stale, and an uninstall without a record removes them too. The guard protects only the `INTELLIGENCE` block, and `develop` sends a fact about the setup to the repository's `AGENTS.md`.

Option 2 would leave every machine with facts that no release keeps current. Option 1 keeps what the owner does not want.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                    |
| :--------------- | :---------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | Each app's home holds the rules and nothing else from the hub, and the next install leaves no facts behind              |
| **Negative (-)** | The facts that told an agent how this setup works are gone from its home; the guard still denies an AI sign-off         |
| **Neutral (~)**  | A machine keeps the facts until its pin moves to a release that carries this, and that release's install takes them out |

---

## ⚖️ Trade-off Comparative

### Option 1: Keep The Facts

- ✅ No change to the kit or the installer
- ❌ Text the owner does not want, beside the rules in every session

### Option 2: Remove The Facts And Leave Their Blocks

- ✅ The smallest change to the installer
- ❌ Every machine that installed them keeps them, with nothing to update or remove them

### Option 3: Remove The Facts And Take Them Out

- ✅ The source and every copy go together
- ❌ The installer keeps a list of where an earlier release wrote, and a test of taking it out

---

## 🔗 Traceability & Links

- [`.github/scripts/install.py`](../../.github/scripts/install.py): `RETIRED` and `retire()`
- [`.github/scripts/kit.py`](../../.github/scripts/kit.py): the kit, in format 2
- [ADR-0016](ADR-0016-Knowledge-Starts-As-Public-Facts.md): the facts this supersedes
- [ADR-0012](ADR-0012-One-Pinned-Kit-For-Every-Module.md): the kit this amends
- [The Home Kit](../technical/The-Home-Kit.md): what the kit installs, and where

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**The rules in every home, and nothing beside them that no one keeps.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
