<!--
title: '📜 THE LAW'
description: 'Where every universal rule is written, what each rule file holds, the rules the rules themselves follow, and how to change, add or retire one.'
tags: [rules, law, invariants, defaults, render]
category: docs
-->

<div align="center">

# 📜 THE LAW

<a name="top"></a>

**Every rule an agent follows, written once, in one place, and rendered everywhere else.**

_One sentence each. Every one with a reason._

</div>

---

## 💡 What The Law Is

Every rule an agent follows, in every repository and on every machine, starts
in [`law/`](../../law/README.md). Nothing downstream is written by hand:
[`scripts/render.py`](../../scripts/render.py) turns that folder into the block
between the `INTELLIGENCE` markers, the home file the home kit installs, and
the hashes a consumer pins.

| File                                  | What it decides                                                                                     |
| :------------------------------------ | :-------------------------------------------------------------------------------------------------- |
| [`block.json`](../../law/block.json)  | The heading, the precedence text, which rules sit in which section, the budget, and the retired IDs |
| [`rules/`](../../law/rules/README.md) | One JSON file per rule, named for its ID                                                            |

---

## 📄 What Each Rule File Holds

| Field         | What it is                                                                                        |
| :------------ | :------------------------------------------------------------------------------------------------ |
| `//`          | The line the folder's file log shows, as `ID: kind for reach.`; `render.py --check` keeps it true |
| `id`          | `DOMAIN-NNN`, the same as the file's name                                                         |
| `kind`        | `invariant`, which nothing waives, or `default`, which a repository may override by ID            |
| `reach`       | `every` repository, or `owner` for the owner's repositories only                                  |
| `text`        | The one sentence agents read, exactly as it appears in the block                                  |
| `why`         | What the rule prevents, and the evidence for it                                                   |
| `enforced_by` | What enforces it today, outside the prompt                                                        |
| `to_add`      | The enforcement still to build                                                                    |

An Invariant without any enforcement listed is refused, because prose alone
cannot make an agent stop. `block.json` decides the order the rules appear in;
the rule files themselves are listed alphabetically.

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

1. Edit the rule's file in [`law/rules/`](../../law/rules/README.md), or add
   one and list its ID in `block.json`.
2. Run `make render`, which rewrites the hub's own `AGENTS.md`,
   `home/intelligence.md`, `home/kit.json` and `home/SHA256SUMS`.
3. Run `make check`, and commit the law and the rendered copies together.
4. Nothing leaves the hub until a release: cut one with 🏷️ Cut Release, as
   [Releasing](../operations/Releasing.md) describes. Every repository's stub
   picks it up on Monday, and `make sync` delivers it to every repository now.

To retire a rule, delete its file, take its ID out of `block.json`, and add
the ID to `retired` with a note on where its intent went. A new rule also gets
a scenario in `evals/scenarios/`, as [Evals](Evals.md) describes.

```bash
make render                    # rewrite every copy from the law
make check                     # the validator, render --check, evals --check and every test
```

---

## 🔗 See Also

- [ADR-0011](../adrs/ADR-0011-The-Universal-Rule-Set.md): the nineteen rules, and the evidence for each addition and cut
- [ADR-0008](../adrs/ADR-0008-Names-Without-Prefixes.md): rule IDs are `DOMAIN-NNN`, with no owner prefix
- [Backstops & Residual Risk](../operations/Backstops-&-Residual-Risk.md): the controls behind each Invariant, outside the prompt

---

<div align="center">

**Every rule written once, here, and nowhere else.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
