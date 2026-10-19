<!--
title: '🧠 HOW IT WORKS'
description: 'How one set of rules reaches every AI coding agent: the two pieces, the block every copy carries, which copy wins, and where each module fits.'
tags: [ai-agents, agents-md, architecture, precedence]
category: docs
-->

<div align="center">

# 🧠 HOW IT WORKS

<a name="top"></a>

**One block of rules, written once, reaching every agent in two pieces.**

_Home for every session. A repository copy for every clone._

</div>

---

## 💡 The Two Pieces

**Intelligence is the source of the rules every AI coding agent follows when
it works for [@tannergolden](https://github.com/tannergolden)**: Claude Code,
Codex, Antigravity CLI, Copilot (the CLI and VS Code), Cursor and Grok Build.
The rules are written once, in [the Constitution](../../CONSTITUTION.md),
rendered as one block, and reach the agents in two pieces:

| Piece               | Where the rules land                           | How they get there                                         | Read more                             |
| :------------------ | :--------------------------------------------- | :--------------------------------------------------------- | :------------------------------------ |
| **🏠 Home**         | Each app's own home folder, on every machine   | Your dotfiles run `make agents`                            | [The Home Kit](The-Home-Kit.md)       |
| **🗂️ Repositories** | One `AGENTS.md` at the root of each repository | A pull request from its stub or `make sync`, merged by you | [Repository Sync](Repository-Sync.md) |

The home copy reaches every session, including other people's repositories
and scratch folders. The repository copy travels with the code, so cloud
agents and collaborators get the same rules with nothing installed. A Claude
Code cloud session starts empty, so [the cloud setup script](Cloud-Setup.md)
installs the home copy there.

---

## 🗂️ One AGENTS.md Per Repository

**Each repository holds one `AGENTS.md`, at its root, and nothing else for
agents:** no `CLAUDE.md`, no per-tool files, nothing nested. Every app on the
list reads `AGENTS.md`, Claude Code included. The hub is the one exception: it
holds the source, `CONSTITUTION.md`, and keeps no copy. The file has a managed
block and sections the repository owns:

```markdown
# Repository Name

<!-- INTELLIGENCE:BEGIN sha256:<hash of the block> -->

The universal rules: Invariants, then Defaults, each with an ID such as SEC-001.

<!-- INTELLIGENCE:END -->

## Commands

## Definition of done

## Conventions

## Where things live

## Gotchas

## Ask first

## Overrides
```

The marker carries the SHA-256 of the block's text, so a hand edit between
the markers is plain to see: `make audit` names it, the standards' CI fails
the pull request that makes it, and the next sync puts the block back.

---

## ⚖️ Which Rule Wins

Both copies open with the same precedence text, so an agent that loads both
knows which rule wins:

> - Invariants: follow every one in every copy; nothing waives one. If a request
>   needs what one forbids, do the rest, skip that part and name the rule ID.
> - Defaults: your user's explicit request for this task wins, then the
>   repository's "Overrides" entry for that rule ID, then the repository's copy
>   of these rules. In forks, and in repositories tannergolden does not own, the
>   project's own rules win and owner-only Defaults do not apply; a repository
>   with no remote yet counts as tannergolden's.

A repository changes a Default only through an entry under its `## Overrides`
heading, one line per rule ID with the reason, such as
`- WORK-002: we ask more`. `make audit` rejects an entry that names an
Invariant, because nothing waives one.

---

## 🧩 What Rides Beside The Rules

The rules travel with a kit, one pinned file in the same release, and each
module has its own document:

| Module                                                     | What it is                                                                              | Read more                                   |
| :--------------------------------------------------------- | :-------------------------------------------------------------------------------------- | :------------------------------------------ |
| The guard hook                                             | Denies the few tool calls the Invariants forbid outright, before they run, in every app | [The Home Kit](The-Home-Kit.md)             |
| The `develop` skill, and the Worker and Reviewer subagents | A procedure loaded when the task calls for it, and two agents a session hands work to   | [Skills & Subagents](Skills-&-Subagents.md) |
| The knowledge facts                                        | Public facts about how this setup works, beside every home copy of the rules            | [Knowledge](Knowledge.md)                   |

Two tools prove the whole thing works: [the loader probe](The-Loader-Probe.md)
shows which files each app actually loads, and [evals](Evals.md) measure
whether the agent then follows each rule. Nothing reaches a machine or a
repository until [a release](../operations/Releasing.md).

---

## 🔗 See Also

- [ADR-0001](../adrs/ADR-0001-Two-Pieces-Home-&-Repository.md): the rules reach agents in two pieces
- [ADR-0002](../adrs/ADR-0002-One-Root-AGENTS-File.md): one root `AGENTS.md` per repository, and no `CLAUDE.md`
- [ADR-0004](../adrs/ADR-0004-Precedence-Overrides-&-Hash-Marker.md): which copy wins, how a repository overrides, and the hash marker

---

<div align="center">

**Written once. Loaded everywhere.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
