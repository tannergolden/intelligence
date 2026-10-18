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

| Entry                                                                                              | Status   | Date       | Evidence | Purpose                                                                                                                                                                                                                                                  |
| :------------------------------------------------------------------------------------------------- | :------- | :--------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ADR-0001-Two-Pieces-Home-&-Repository.md`](ADR-0001-Two-Pieces-Home-&-Repository.md)             | Proposed | 2026-10-17 | N/A      | The universal rules reach agents in two pieces, a copy in each app's home folder and a managed block in every repository, both rendered from one source.                                                                                                 |
| [`ADR-0002-One-Root-AGENTS-File.md`](ADR-0002-One-Root-AGENTS-File.md)                             | Proposed | 2026-10-17 | N/A      | Each repository carries exactly one AGENTS.md, at its root, holding the managed block and the sections the repository owns, with no CLAUDE.md or per-tool files.                                                                                         |
| [`ADR-0003-Push-Sync-&-Owner-Merge.md`](ADR-0003-Push-Sync-&-Owner-Merge.md)                       | Proposed | 2026-10-17 | N/A      | The hub delivers each release as one pull request per repository, opened under the owner's own login, and the owner merges them, with no stub, secret or bot merge in any repository.                                                                    |
| [`ADR-0004-Precedence-Overrides-&-Hash-Marker.md`](ADR-0004-Precedence-Overrides-&-Hash-Marker.md) | Proposed | 2026-10-17 | N/A      | Invariants from every copy of the rules apply and nothing waives one, Defaults yield to the user's request and then to an Overrides entry by rule ID, and the managed block is marked with a hash of its content.                                        |
| [`ADR-0005-Home-Copies-Not-Links.md`](ADR-0005-Home-Copies-Not-Links.md)                           | Proposed | 2026-10-17 | N/A      | The home kit writes byte-identical copies of the rules into each app's own home location, checked against the release, instead of linking every app to one shared file.                                                                                  |
| [`ADR-0006-Build-The-Law-Adopt-The-Plumbing.md`](ADR-0006-Build-The-Law-Adopt-The-Plumbing.md)     | Proposed | 2026-10-17 | N/A      | The hub builds its own renderer and installer in the Python standard library, and adopts existing tools for the plumbing around them, with set triggers to revisit.                                                                                      |
| [`ADR-0007-Public-MIT-Hub.md`](ADR-0007-Public-MIT-Hub.md)                                         | Proposed | 2026-10-17 | N/A      | The hub is a public repository under the MIT License, with every seeded document footer to match, because consumers fetch its releases without credentials.                                                                                              |
| [`ADR-0008-Names-Without-Prefixes.md`](ADR-0008-Names-Without-Prefixes.md)                         | Proposed | 2026-10-17 | N/A      | Rule IDs take the form DOMAIN-NNN and every file and skill is named for what it does, with no owner prefix on either.                                                                                                                                    |
| [`ADR-0009-Agents-Follow-The-Standards.md`](ADR-0009-Agents-Follow-The-Standards.md)               | Proposed | 2026-10-17 | N/A      | Every AI agent follows the engineering standards in tannergolden/standards in every repository the owner owns, new ones included, through an owner-only Default that points at them, while forks and other people's repositories follow their own rules. |
| [`ADR-0010-Releases-Serve-Rendered-Files.md`](ADR-0010-Releases-Serve-Rendered-Files.md)           | Proposed | 2026-10-17 | N/A      | A release is a tag whose committed home file and installer every consumer downloads and checks against a pinned SHA-256, instead of assets built and attached after the tag.                                                                             |
| [`ADR-0011-The-Universal-Rule-Set.md`](ADR-0011-The-Universal-Rule-Set.md)                         | Proposed | 2026-10-17 | N/A      | The block holds nineteen rules, eleven Invariants and three Defaults for every repository and five Defaults for the owner's repositories, each one sentence with a reason and an enforcer.                                                               |
| [`README.md`](README.md)                                                                           | -        | -          | -        | This file.                                                                                                                                                                                                                                               |

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
