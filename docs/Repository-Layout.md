<!--
title: '📦 REPOSITORY LAYOUT'
description: 'What each directory in this repository holds, which of them is copied verbatim into consumers, and the one rule that keeps scaffolding out of that copy.'
tags: [layout, structure, publishing, conventions]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📦 REPOSITORY LAYOUT

<a name="top"></a>

**Nine directories, three jobs: the bytes that get published, the machinery that publishes them, and the paperwork that governs both.**

_Know which directory you are in before you edit anything._

</div>

---

## 🎯 Our Strategic Intent

Most publishers keep a template language, a renderer, and a pile of emitters that turn one into the other. This one does not. **`payload/` holds the delivered files as literal bytes**, arranged exactly as they will sit in a consuming repository.

That single decision is what makes the rest small. Measuring a delivered file is `wc -c payload/AGENTS.md`. Reviewing a release is reading a diff of the bytes that will actually land, rather than reading a generator and imagining its output. There is no template language to learn and no rendering step to debug, because there is no rendering step.

Everything else here exists to move that directory safely.

---

## 🗂️ The Tree

```bash
.
├── payload/                  # 📦 THE PRODUCT. Mirrors a consumer's tree, byte for byte
│   ├── AGENTS.md             #    the instruction body: the only file carrying content
│   ├── CLAUDE.md             #    router, one import line
│   ├── GEMINI.md             #    router, one import line
│   ├── .claude/              #    settings that wire the hook. MERGED, never overwritten
│   ├── .ai/hooks/            #    hook scripts. POSIX sh only, fail open, kill switch first
│   └── .agents/skills/       #    skills, once any exist to ship
│
├── actions/ai-sync/          # ⚙️ the composite action a consumer runs: the carrier
├── .github/workflows/        # 🌿 this repository's own CI, sync and release workflows
├── .githooks/                # 🌿 local commit-message enforcement, installed by make setup
│
├── data/                     # ⚙️ settings and rulesets applied to THIS repository by hand
│   └── rulesets/
├── tests/fixtures/           # 🧪 hostile inputs the checks must reject
└── docs/                     # 📝 this file, and the contracts too long for the README
```

Three zones, and the boundary between them is the thing to keep straight:

| Zone              | Directories                          | Leaves this repository?                                 |
| :---------------- | :----------------------------------- | :------------------------------------------------------ |
| **The product**   | `payload/`                           | **Yes, verbatim.** Every byte lands in a consumer       |
| **The machinery** | `actions/`, `.github/`, `.githooks/` | Only `actions/` runs elsewhere, and it ships no content |
| **The paperwork** | `data/`, `tests/`, `docs/`           | Never                                                   |

---

## ⚠️ The Rule That `.gitkeep` Makes Necessary

Empty directories cannot be committed to git, so the ones waiting for their first file carry a `.gitkeep`. Three of those sit **inside `payload/`**.

> [!IMPORTANT]
> **`.gitkeep` files must never reach a consumer.** `payload/` is copied verbatim, so a copy that walks the tree naively will deliver `.gitkeep` into every repository that syncs, forever, in a directory the consumer never asked for. They are scaffolding for this repository, not content for anyone else's.
>
> The sync excludes them by name, and a check asserts that no emitted path is named `.gitkeep`. That assertion is cheap, and the failure it prevents is the kind nobody notices until it is in six repositories.

The same logic applies to anything else added here purely to satisfy a tool. **If a file exists to serve this repository, it does not belong under `payload/`.**

---

## 🤖 Why This Repository Carries Its Own Instruction Files

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` appear at the repository root **and** under `payload/`. They are not duplicates by accident.

The copies under `payload/` are the **source**: the bytes that get delivered. The copies at the root are **this repository consuming its own output**, so the tooling that reads instruction files here reads exactly what a consumer would. A publisher that does not run its own product finds every defect second, after somebody else does.

The root copies are generated. Edit the ones under `payload/`.

---

## 📁 Naming

Directory and file names follow the [canonical documentation standard](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-%26-Formatting.md), which this repository follows **by link and never by copy**. The rules that bite most often here:

- Documentation filenames are Capitalized-Kebab with `&` as the conjunction, never the word `And`.
- No underscore as a word separator anywhere in the tree, except where a platform or language fixes the name.
- Paths under `payload/` are the exception that proves the rule: they are named by the **vendor** that reads them, so `.claude/`, `.agents/` and `.ai/` are correct exactly as spelled and must never be tidied.

---

### 🔗 See also

> [!TIP]
> The README explains what this repository publishes and how a consumer receives it. This file only explains where things sit on disk.

---

<div align="center">

**One directory ships. The rest exists to get it there safely.**

[↑ Back to Top](#top)

</div>
