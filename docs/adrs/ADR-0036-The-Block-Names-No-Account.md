<!--
title: '📄 ADR-0036: THE BLOCK NAMES NO ACCOUNT'
description: 'The block works in anyone''s repository: owner-only Defaults hold where the user owns the repository or its AGENTS.md carries the rules, never in forks, and a link a rule needs, such as STD-001''s to the standards, is the one place an account is named.'
type: record
status: 'Proposed'
date: '2026-11-05'
evidence: 'N/A'
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📄 ADR-0036: THE BLOCK NAMES NO ACCOUNT

<a name="top"></a>

**The same rules in anyone's repository, with the owner's repositories reached by link.**

_No name in the rules, and a direct link where a rule needs one._

</div>

---

## 📋 Meta Information

> [!NOTE]
> **Status**, **Date**, and **Evidence** live in the frontmatter above - they feed the generated [ADR index](README.md), so they are recorded once. This table records who was involved.

| Attribute     | Specification                                                                                |
| :------------ | :------------------------------------------------------------------------------------------- |
| **Deciders**  | Tanner Golden ([@tannergolden](https://github.com/tannergolden)), owner                      |
| **Consulted** | Claude Code sessions: the change, made at the owner's direction                              |
| **Informed**  | Every agent and collaborator working in a repository that carries the block, or the home kit |

---

## 🎯 Context & Problem Statement

Anyone on GitHub can take the stub and carry the block in their own repositories, for the universal rules beside their own. The block still named the hub's owner in its precedence: owner-only Defaults did not apply "in repositories tannergolden does not own", and a repository with no remote "counts as tannergolden's". In anyone else's repository that reads as someone else's rules. STD-001 named the standards as `github.com/tannergolden/standards`, a mention GitHub does not render as a link.

The owner set two requirements: the block names no account, and where a rule has to reach one of the owner's repositories, such as the standards, it links to it directly. Those links are the only exception.

---

## 🚦 Decision Drivers

- **One block for every adopter**, with nothing that only makes sense for one account.
- **The owner's conventions still reach every agent in the owner's repositories**, collaborators' included, as [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md) intended.
- **Forks and projects that never adopted the rules keep their own.**
- **A rule that needs a repository links to it**, so an agent can open it as written.

---

## 🏗️ Considered Options

1. **Owner-only Defaults hold where your user owns the repository**, and nowhere else.
2. **Where your user owns the repository, or its `AGENTS.md` carries these rules, never in forks.**
3. **A placeholder for the owner**, such as `github.com/<owner>/standards`, filled in by the agent.

---

## ✅ Decision Outcome

**Chosen Option**: Option 2, ownership or adoption

### Rationale for Selection

The second line of the precedence now ends:

> Owner-only Defaults hold in repositories your user owns or whose AGENTS.md carries these rules, never in forks; a repository with no remote yet counts as your user's.

"Your user owns" is the phrase OPS-001 already uses, so the block gains no new idea of ownership. A repository that carries the block has an owner who adopted it, so a collaborator's agent there keeps that owner's conventions, which Option 1 would lose. A fork carries the block of the repository it came from but not its owner's choice, so forks stay out, as before.

STD-001 now links `https://github.com/tannergolden/standards`, a full link GitHub renders and an agent can open as written. It is the one place the block names an account, as the owner allowed. Option 3 would name no account even there, but it asks every agent to build a link, and in a repository whose owner has no standards repository it points nowhere.

The block measures 5,367 of its 5,400 characters, up from 5,338.

---

## 📈 Consequence Matrix

| Category         | Impact / Consequence                                                                                                                              |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Positive (+)** | The block reads the same in anyone's repository; the standards are one click away; collaborators keep the owner's conventions                     |
| **Negative (-)** | An adopter's repositories get the owner-only Defaults, the standards link and `Development` among them, until an Overrides entry changes each one |
| **Neutral (~)**  | The guard still checks for the owner's account: outside the owner's repositories it denies no em dash, and `override OPS-001` lifts nothing       |

---

## ⚖️ Trade-off Comparative

### Option 1: Where Your User Owns The Repository

- ✅ The simplest test, and the same as OPS-001's
- ❌ A collaborator's agent in the owner's repository loses the owner's conventions

### Option 2: Ownership Or Adoption

- ✅ Works for owners, collaborators and adopters, and keeps forks out
- ❌ Adopters inherit the owner's conventions until they override them

### Option 3: A Placeholder For The Owner

- ✅ No account named anywhere in the block
- ❌ Every agent builds the link, and it can point at a repository that does not exist

---

## 🔗 Traceability & Links

- [`CONSTITUTION.md`](../../CONSTITUTION.md): Article I, Article IV and STD-001
- [ADR-0009](ADR-0009-Agents-Follow-The-Standards.md): where the owner-only Defaults reached before
- [ADR-0034](ADR-0034-One-Ladder-For-Rules-&-Docs.md): the ladder this line ends

### 🔗 See also

> [!TIP]
> Every canonical guide is indexed in the [&#x1F4DA; Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md). If you rename or move a file, update every reference to it across the repository to prevent link drift.

---

<div align="center">

**Rules anyone can carry, with links to the owner's where a rule needs them.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
