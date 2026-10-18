<!--
title: '⚖️ THE LAW'
description: 'The source of every universal rule: one file per rule ID, and the order, precedence text and budget of the block every agent reads.'
tags: [rules, law, agents-md, instructions]
category: docs
-->

<div align="center">

# ⚖️ THE LAW

<a name="top"></a>

**The one place the universal rules are written; every copy an agent reads is rendered from here.**

_Write a rule once. Render it everywhere._

</div>

---

## 💡 What This Folder Is For

Every rule an agent follows, in every repository and on every machine, starts
here. Nothing downstream is written by hand: `scripts/render.py` turns this
folder into the block between the `INTELLIGENCE` markers, the home file the
home kit installs, and the hashes a consumer pins.

| File                        | What it decides                                                                                     |
| :-------------------------- | :-------------------------------------------------------------------------------------------------- |
| [`block.json`](block.json)  | The heading, the precedence text, which rules sit in which section, the budget, and the retired IDs |
| [`rules/`](rules/README.md) | One JSON file per rule: its text, its kind and reach, and what enforces it                          |

---

## 📐 The Rules For Rules

`render.py --check` holds the law to these, and CI fails when one breaks:

- **An ID is `DOMAIN-NNN`**, such as `SEC-001`, and a retired ID is never
  reused. `retired` in `block.json` lists each one and where its rule went.
- **A rule is one sentence of printable ASCII, ending in a period**, at most
  300 characters. No hidden, bidirectional or look-alike characters can
  reach an agent through the law.
- **An Invariant reaches every repository and names its enforcer**, one
  that exists today or one to add. A Default reaches every repository or
  only the owner's.
- **Every rule sits in exactly one section** whose kind and reach match its
  own, and every section lists only rules that exist.
- **The block fits its cap**: 4,000 characters, against a target of 3,200.
  `--check` reports the size on every run.

---

## 🌿 Changing A Rule

1. Edit the rule's file in [`rules/`](rules/README.md), or add one and list
   its ID in `block.json`.
2. Run `make render`, which rewrites this repository's `AGENTS.md`,
   `home/intelligence.md` and `home/SHA256SUMS`.
3. Run `make check`, and commit the law and the rendered copies together.
4. Nothing leaves the hub until a release: cut one with 🏷️ Cut Release,
   then run `make sync` to deliver it.

To retire a rule, delete its file, take its ID out of `block.json`, and add
the ID to `retired` with a note on where its intent went.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                       | Purpose                                                                                                              |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| [`rules/`](rules/README.md) | One JSON file per universal rule: the sentence agents read, its kind and reach, why it exists, and what enforces it. |
| [`block.json`](block.json)  | The order, precedence text, budget and retired IDs of the block every agent reads.                                   |
| [`README.md`](README.md)    | This file.                                                                                                           |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Every rule written once, here, and nowhere else.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
