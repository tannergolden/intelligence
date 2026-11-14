<!--
title: '📄 ADR-0044: THE WORKFORCE LIVES BESIDE THE KIT'
description: 'The hub holds an agent workforce in workforce/: a Chief of Staff, a Knowledge Vault Manager and the venture template''s twelve departments of at most five agents, one Markdown file each, rendered for local apps, API orchestrators and Grok by workforce.py, and installed only on request, never by the home kit.'
type: record
status: 'Proposed'
date: '2026-11-14'
evidence: '[Portable Agent Workforce](https://github.com/tannergolden/intelligence/blob/99c43fd892b2fddaec1b9a01705878110f1ee54c/docs/technical/research/Portable-Agent-Workforce.md)'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0044: THE WORKFORCE LIVES BESIDE THE KIT

<a name="top"></a>

**Forty-five agents, written once in the hub, installed only where someone asks for them.**

_Beside the kit, never inside it._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                   |
| :------------ | :---------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                         |
| **Consulted** | Claude Code sessions: the research, the design and the build, made at the owner's direction     |
| **Informed**  | Anyone who installs the workforce, in a local app, a cloud session, an API orchestrator or Grok |

---

## 🎯 Context & Problem Statement

[ADR-0041](ADR-0041-The-Kit-Carries-No-Skills.md) took the twelve department skills and their teams out of the kit, and with them every agent the owner used, leaving the hub to the rules, `AGENTS.md` and the sync. The owner then asked for a workforce of agents stored in the hub and laid out like the departments of the venture template in tannergolden/knowledge: one Chief of Staff orchestrating every department, a ⭐ Director and up to four specialists in each, a Knowledge Vault Manager for the owner's vault, a mesh inside each department and a hub between them, every agent serving the ventures and the owner's own life, and the whole workforce installable by the Chief of Staff locally, in the cloud and on Grok.

`AGENTS.md` asks first before any skill or subagent joins the kit, because the kit installs into every app on every machine, and ADR-0041 gave the reason: about 2.5 MB of skills that every install carried, and machinery that served nothing else.

---

## 🚦 Decision Drivers

- **The owner's request**: the agent files live in the hub, mirror the venture template's departments, carry the names the owner reads, and install in three environments.
- **The kit stays the guard alone**: nothing reaches a machine that did not ask for it, and `make agents` neither installs nor removes an agent.
- **One source**: each agent written once, every environment's copy rendered from it and checked.
- **Each seat earns its place**: the fewest agents that cover every function of each department, with one owner for each function.
- **Rules held in code where an app allows it**: who may message whom, and which acts wait on the owner.

---

## 🏗️ Considered Options

1. **Put the workforce back in the kit**, rendered into `home/kit.json` and installed into every app by `make agents`.
2. **Keep it in the hub beside the kit**, in `workforce/`, rendered and installed only by `workforce.py`, on request.
3. **Keep it out of the hub**, in the owner's vault or a repository of its own.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, the workforce lives beside the kit

### Rationale for Selection

- **`workforce/` mirrors `Ventures/.template/`**: the twelve department folders under the template's own names, `Miscellaneous/` with no team, and the Chief of Staff and the Knowledge Vault Manager at the root.
- **One Markdown file per agent**, its file named for the role with spaces, a Director's led by the star U+2B50. Its frontmatter's `name` is the ASCII id every app calls it by, and `title` the persona's name. Its prompt is composed of the agent, its department's charter and `Protocol.md`, so no rule is written twice.
- **Forty-five agents**: the two at the root and forty-three in the departments, a seat added beside the Director only for independence, expertise with a high cost of error, or a cadence of its own. Only Finance & Accounting fills five seats.
- **Hub and spoke between departments, a mesh inside each**: the Chief of Staff carries every message between departments, word for word on the way back, and is the only way to the Knowledge Vault Manager, the vault's one writer. Money, contracts, outside messages, deletions, equity, live systems and the owner's profile wait on the owner's yes for the exact act.
- **`.github/scripts/workforce.py` checks and renders it** for Claude Code (whose folder VS Code and Cursor also read), Grok Build, Copilot, Codex, Antigravity, an API bundle for OpenAI, xAI, Anthropic and local servers, Ollama, plain text, and Grok Bot's first messages. `make lint` runs its check. Every copy carries a mark of its own, not the kit's, so the kit's sweep never touches it, and `install` never overwrites a file it did not write.
- **The Chief of Staff installs it**, from a bootstrap prompt for a terminal and one for Grok Bot, in [The Workforce](../technical/The-Workforce.md).

Option 1 brings back what ADR-0041 removed: every agent in every app on every machine, whether or not the owner works with the workforce there. Option 3 contradicts the request, and puts agent instruction files in the vault, which [ADR-0037](ADR-0037-The-Hub-Writes-Every-Skill.md) ruled out.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                                                        |
| :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Positive (+)** | One source for every environment; the kit and every machine unchanged until someone installs; names and schemas checked before anything renders                             |
| **Negative (-)** | A pull request holding the whole workforce runs far past the 300 lines and 10 files a pull request may hold, so it lands in parts; Grok Bot's rules are partly undocumented |
| **Neutral (~)**  | No repository's `AGENTS.md` changes; the knowledge vault keeps no agent files, as before                                                                                    |

---

## ⚖️ Trade-off Comparative

### Option 1: Back In The Kit

- ✅ Every machine has the workforce with nothing more to run
- ❌ Every app on every machine loads forty-five agents, and the kit grows back the machinery ADR-0041 removed

### Option 2: Beside The Kit

- ✅ The workforce installs where it is wanted, in any of nine forms, and the kit stays the guard alone
- ❌ One more command to run, or one more prompt to give the Chief of Staff

### Option 3: Outside The Hub

- ✅ The hub stays the rules alone
- ❌ Not what the owner asked for, and in the vault it breaks ADR-0037

---

## 🔗 Traceability & Links

- [The Workforce](../technical/The-Workforce.md): the layout, the agent file, the seats, the protocol and the installs
- [Portable Agent Workforce](../technical/research/Portable-Agent-Workforce.md): the research behind the format, the names and the Grok setup
- [ADR-0041](ADR-0041-The-Kit-Carries-No-Skills.md): the kit carries no skills, which this leaves as it is
- [ADR-0040](ADR-0040-Every-Agent-Belongs-To-A-Department.md): the last workforce, whose seats this one was measured against

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Written once, beside the kit, installed where it is asked for.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
