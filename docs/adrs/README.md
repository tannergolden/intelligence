<!--
title: '🧭 ARCHITECTURE DECISIONS'
description: 'Architecture decision records, one file per decision, each logged with its status, date and evidence.'
tags: [adr, architecture, decisions, index]
category: docs
-->

<div align="center">

# 🧭 ARCHITECTURE DECISIONS

<a name="top"></a>

**Every significant decision this project has made, and why, one record each.**

_One decision per record. One row per decision._

</div>

---

## 💡 What This Folder Is For

An architecture decision record (ADR) captures one significant decision: the
context it was made in, the options weighed, and the consequences accepted.
Every record lives in this folder, one file per decision, and the log below is
their index.

The folder is a living record, not a fill-in form, and its records are **yours
from the first commit**: nothing upstream ever writes, moves or removes one. It
arrives with no decisions in it and gains a row each time a record is written.
Only this README is ever updated from the template - when you run
🔄 Template Sync - merged with the rows your records add.

---

## 🎯 Why Decisions Are Recorded

The _why_ matters as much as the _what_. An auditable record of how the system
evolved lets every later contributor, human or AI, see the constraints and
trade-offs that shaped it before changing it.

- **Traceability**: every major architectural pivot is documented and numbered.
- **Context**: each decision is recorded with the situation it was made in.
- **Consequences**: the benefits and the technical debt are both written down.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log fields=status,date,evidence -->

| Entry                                                                                              | Status     | Date       | Evidence | Purpose                                                                                                                                                                                                                                                         |
| :------------------------------------------------------------------------------------------------- | :--------- | :--------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ADR-0001-Two-Pieces-Home-&-Repository.md`](ADR-0001-Two-Pieces-Home-&-Repository.md)             | Proposed   | 2026-10-17 | N/A      | The universal rules reach agents in two pieces, a copy in each app's home folder and a managed block in every repository, both rendered from one source.                                                                                                        |
| [`ADR-0002-One-Root-AGENTS-File.md`](ADR-0002-One-Root-AGENTS-File.md)                             | Proposed   | 2026-10-17 | N/A      | Each repository carries exactly one AGENTS.md, at its root, holding the managed block and the sections the repository owns, with no CLAUDE.md or per-tool files.                                                                                                |
| [`ADR-0003-Push-Sync-&-Owner-Merge.md`](ADR-0003-Push-Sync-&-Owner-Merge.md)                       | Proposed   | 2026-10-17 | N/A      | The hub delivers each release as one pull request per repository, opened under the owner's own login, and the owner merges them, with no stub, secret or bot merge in any repository.                                                                           |
| [`ADR-0004-Precedence-Overrides-&-Hash-Marker.md`](ADR-0004-Precedence-Overrides-&-Hash-Marker.md) | Proposed   | 2026-10-17 | N/A      | Invariants from every copy of the rules apply and nothing waives one, Defaults yield to the user's request and then to an Overrides entry by rule ID, and the managed block is marked with a hash of its content.                                               |
| [`ADR-0005-Home-Copies-Not-Links.md`](ADR-0005-Home-Copies-Not-Links.md)                           | Proposed   | 2026-10-17 | N/A      | The home kit writes byte-identical copies of the rules into each app's own home location, checked against the release, instead of linking every app to one shared file.                                                                                         |
| [`ADR-0006-Build-The-Law-Adopt-The-Plumbing.md`](ADR-0006-Build-The-Law-Adopt-The-Plumbing.md)     | Proposed   | 2026-10-17 | N/A      | The hub builds its own renderer and installer in the Python standard library, and adopts existing tools for the plumbing around them, with set triggers to revisit.                                                                                             |
| [`ADR-0007-Public-MIT-Hub.md`](ADR-0007-Public-MIT-Hub.md)                                         | Proposed   | 2026-10-17 | N/A      | The hub is a public repository under the MIT License, with every seeded document footer to match, because consumers fetch its releases without credentials.                                                                                                     |
| [`ADR-0008-Names-Without-Prefixes.md`](ADR-0008-Names-Without-Prefixes.md)                         | Proposed   | 2026-10-17 | N/A      | Rule IDs take the form DOMAIN-NNN and every file and skill is named for what it does, with no owner prefix on either.                                                                                                                                           |
| [`ADR-0009-Agents-Follow-The-Standards.md`](ADR-0009-Agents-Follow-The-Standards.md)               | Proposed   | 2026-10-17 | N/A      | Every AI agent follows the engineering standards in tannergolden/standards in every repository the owner owns, new ones included, through an owner-only Default that points at them, while forks and other people's repositories follow their own rules.        |
| [`ADR-0010-Releases-Serve-Rendered-Files.md`](ADR-0010-Releases-Serve-Rendered-Files.md)           | Proposed   | 2026-10-17 | N/A      | A release is a tag whose committed home file and installer every consumer downloads and checks against a pinned SHA-256, instead of assets built and attached after the tag.                                                                                    |
| [`ADR-0011-The-Universal-Rule-Set.md`](ADR-0011-The-Universal-Rule-Set.md)                         | Proposed   | 2026-10-17 | N/A      | The block holds nineteen rules, eleven Invariants and three Defaults for every repository and five Defaults for the owner's repositories, each one sentence with a reason and an enforcer.                                                                      |
| [`ADR-0012-One-Pinned-Kit-For-Every-Module.md`](ADR-0012-One-Pinned-Kit-For-Every-Module.md)       | Proposed   | 2026-10-18 | N/A      | Every module around the rules, the guard hook, the skills, the subagents and the knowledge facts, ships in one rendered file, home/kit.json, pinned by one SHA-256 beside the home file and the installer.                                                      |
| [`ADR-0013-The-Guard-Denies-Never-Allows.md`](ADR-0013-The-Guard-Denies-Never-Allows.md)           | Proposed   | 2026-10-18 | N/A      | One standard-library script, called by every app's pre-tool hook, denies the few tool calls the Invariants forbid outright with exit 2 and a reason, and never allows or asks.                                                                                  |
| [`ADR-0014-One-Skill-That-Builds-Skills.md`](ADR-0014-One-Skill-That-Builds-Skills.md)             | Proposed   | 2026-10-18 | N/A      | The hub ships exactly one skill for now, building-skills, which teaches an agent to decide whether a need is a skill at all and to build, test and ship one in the format every app accepts.                                                                    |
| [`ADR-0015-A-Worker-And-A-Reviewer.md`](ADR-0015-A-Worker-And-A-Reviewer.md)                       | Proposed   | 2026-10-18 | N/A      | The agent hierarchy begins with two subagents, a Worker that makes one change and proves it and a Reviewer that checks a change without editing it, rendered for Claude Code, Copilot and Codex.                                                                |
| [`ADR-0016-Knowledge-Starts-As-Public-Facts.md`](ADR-0016-Knowledge-Starts-As-Public-Facts.md)     | Proposed   | 2026-10-18 | N/A      | Knowledge begins as a short, public list of facts about how the owner's setup works, rendered as its own marked block beside every home copy of the rules and in the cloud setup, and never personal context.                                                   |
| [`ADR-0017-Unattended-Sync-Through-An-App.md`](ADR-0017-Unattended-Sync-Through-An-App.md)         | Superseded | 2026-10-18 | N/A      | A GitHub App, with one token per repository and a key kept in a protected environment, opens each release's sync pull requests unattended, while merging stays the owner's, under the owner's own login.                                                        |
| [`ADR-0018-Evals-Measure-The-Block.md`](ADR-0018-Evals-Measure-The-Block.md)                       | Proposed   | 2026-10-18 | N/A      | Each rule has at least one scenario that tempts an agent to break it, run headless against a real app with the block and without it and checked by code, so the difference shows what the block is worth.                                                       |
| [`ADR-0019-Each-Repository-Pulls-With-A-Stub.md`](ADR-0019-Each-Repository-Pulls-With-A-Stub.md)   | Proposed   | 2026-10-18 | N/A      | A repository that wants the rules carries a small workflow stub that pulls each release on its own GITHUB_TOKEN and proposes it as one pull request; no GitHub App, no key, and merging stays the owner's.                                                      |
| [`ADR-0020-One-Constitution.md`](ADR-0020-One-Constitution.md)                                     | Proposed   | 2026-10-19 | N/A      | The universal rules live in one Markdown file, CONSTITUTION.md at the hub's root, which the renderer reads into the block every AGENTS.md carries; the hub keeps no AGENTS.md of its own, and the rule set takes in the universal rules of the knowledge vault. |
| [`README.md`](README.md)                                                                           | -          | -          | -        | This file.                                                                                                                                                                                                                                                      |

<!-- AUTO-INDEX:END -->

**This log is the decision index, and nobody types its rows.** 🗂️ Machined
Indexes redraws it after every push from each record's own frontmatter.
**Status** is Proposed, Accepted, Superseded, or Deprecated; **Date** is when
the decision was made; **Evidence** links the research report(s) that informed
it, or reads N/A.

---

## 🌿 Adding A Decision

- [ ] Copy the [ADR template](../templates/ADR.md) into this folder as
      `ADR-NNNN-Short-Slug.md`, taking the next number.
- [ ] Set `status`, `date`, and `evidence` in its frontmatter, and write every
      section.
- [ ] Propose it in a pull request. Once merged, it is **Accepted**.

A later decision supersedes an earlier one rather than rewriting it: mark the
old record **Superseded** and link the new one.

---

## 🔗 See also

- [Documentation index](../README.md) - every document this project keeps
- [Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md) - the canonical engineering standards

---

<div align="center">

**Write the decision down while the reasons are still fresh.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the MIT License.

</div>
