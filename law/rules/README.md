<!--
title: '📜 RULES'
description: 'One JSON file per universal rule: the sentence agents read, its kind and reach, why it exists, and what enforces it.'
tags: [rules, law, invariants, defaults]
category: docs
-->

<div align="center">

# 📜 RULES

<a name="top"></a>

**One file per rule, named for its ID, holding the sentence every agent reads and the reason behind it.**

_One sentence each. Every one with a reason._

</div>

---

## 💡 What Each File Holds

| Field         | What it is                                                                                     |
| :------------ | :--------------------------------------------------------------------------------------------- |
| `//`          | The line the file log below shows, as `ID: kind for reach.`; `render.py --check` keeps it true |
| `id`          | `DOMAIN-NNN`, the same as the file's name                                                      |
| `kind`        | `invariant`, which nothing waives, or `default`, which a repository may override by ID         |
| `reach`       | `every` repository, or `owner` for the owner's repositories only                               |
| `text`        | The one sentence agents read, exactly as it appears in the block                               |
| `why`         | What the rule prevents, and the evidence for it                                                |
| `enforced_by` | What enforces it today, outside the prompt                                                     |
| `to_add`      | The enforcement still to build                                                                 |

An Invariant without any enforcement listed is refused, because prose alone
cannot make an agent stop. `law/block.json` decides the order the rules
appear in; the files themselves are listed below alphabetically.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                            | Purpose                                          |
| :------------------------------- | :----------------------------------------------- |
| [`CODE-001.json`](CODE-001.json) | CODE-001: a Default for every repository.        |
| [`CODE-002.json`](CODE-002.json) | CODE-002: an Invariant for every repository.     |
| [`COM-002.json`](COM-002.json)   | COM-002: an Invariant for every repository.      |
| [`DOC-002.json`](DOC-002.json)   | DOC-002: a Default for the owner's repositories. |
| [`GIT-001.json`](GIT-001.json)   | GIT-001: an Invariant for every repository.      |
| [`GIT-010.json`](GIT-010.json)   | GIT-010: a Default for the owner's repositories. |
| [`GIT-012.json`](GIT-012.json)   | GIT-012: a Default for the owner's repositories. |
| [`GIT-013.json`](GIT-013.json)   | GIT-013: a Default for the owner's repositories. |
| [`OPS-001.json`](OPS-001.json)   | OPS-001: an Invariant for every repository.      |
| [`OPS-003.json`](OPS-003.json)   | OPS-003: an Invariant for every repository.      |
| [`OPS-004.json`](OPS-004.json)   | OPS-004: an Invariant for every repository.      |
| [`OPS-005.json`](OPS-005.json)   | OPS-005: an Invariant for every repository.      |
| [`POL-001.json`](POL-001.json)   | POL-001: an Invariant for every repository.      |
| [`README.md`](README.md)         | This file.                                       |
| [`SEC-001.json`](SEC-001.json)   | SEC-001: an Invariant for every repository.      |
| [`SEC-002.json`](SEC-002.json)   | SEC-002: an Invariant for every repository.      |
| [`SEC-003.json`](SEC-003.json)   | SEC-003: an Invariant for every repository.      |
| [`STD-001.json`](STD-001.json)   | STD-001: a Default for the owner's repositories. |
| [`WORK-001.json`](WORK-001.json) | WORK-001: a Default for every repository.        |
| [`WORK-002.json`](WORK-002.json) | WORK-002: a Default for every repository.        |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Nineteen sentences, each one earning its place.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
