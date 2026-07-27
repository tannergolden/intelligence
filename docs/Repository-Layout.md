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
│   ├── .claude/settings.json #    the hook wiring. MERGED, never overwritten
│   ├── .ai/ai.sh             #    verify, adopt and remove, for the consumer
│   ├── .ai/hooks/            #    hook scripts. POSIX sh only, fail open, kill switch first
│   └── .agents/skills/       #    skills, once any exist to ship. Empty in v1
│
├── actions/ai-sync/          # ⚙️ the composite action a consumer runs: the carrier
│                             #    action.yml, sync.py (the engine), check.py (the linters)
├── bootstrap/ai-sync.yml     # ⚙️ the ONE file a consumer copies, by hand, once
├── ceiling.lock              # ⚙️ the permission ceiling that stub must declare exactly
│
├── .github/workflows/        # 🌿 this repository's own CI, security scans, sync, release
├── .githooks/commit-msg      # 🌿 the only commit-message gate, installed by make setup
├── Makefile                  # 🌿 check, test, build, verify, setup. No toolchain
├── README.md                 # 🌿 what this publishes and how a consumer receives it
│
├── AGENTS.md CLAUDE.md GEMINI.md   # 🤖 GENERATED copies of payload/. See below
│
├── data/                     # ⚙️ settings and rulesets applied to THIS repository by hand
│   ├── repository-settings.json
│   └── rulesets/
├── tests/fixtures/           # 🧪 hostile inputs the checks must reject
├── docs/                     # 📝 this file, and the contracts too long for the README
└── LICENSE  LICENSES/  REUSE.toml  # 📄 see the note below
```

Three zones, and the boundary between them is the thing to keep straight:

| Zone              | Directories                                        | Leaves this repository?                                 |
| :---------------- | :------------------------------------------------- | :------------------------------------------------------ |
| **The product**   | `payload/`                                         | **Yes, verbatim.** Every byte lands in a consumer       |
| **The machinery** | `actions/`, `bootstrap/`, `.github/`, `.githooks/` | Only `actions/` runs elsewhere, and it ships no content |
| **The paperwork** | `data/`, `tests/`, `docs/`, the licence files      | Never                                                   |

`bootstrap/ai-sync.yml` is the odd one: it never runs here and is never delivered by the sync either. It is a **template a human copies once**, because the token that does the syncing provably cannot write under `.github/workflows/` in anyone's repository, including its own consumers'.

---

## 📄 Why There Are Two Licence Files

`LICENSE` at the root is what GitHub reads to show a licence on the repository page. `LICENSES/MIT.txt` is what `reuse lint` reads, and it is the one the `📄 REUSE Compliance` job in CI actually depends on: the tool resolves the `MIT` identifier against `LICENSES/` and does not look at the root file at all. Deleting either one breaks something different, so both stay.

`REUSE.toml` carries a single blanket annotation over `**`, and that shape is load-bearing rather than lazy. `payload/` is copied byte for byte into other people's repositories, so an SPDX header added to satisfy a linter would land inside always-loaded agent instruction files everywhere the sync reaches.

---

## ⚠️ The Rule That `.gitkeep` Makes Necessary

Empty directories cannot be committed to git, so a directory waiting for its first file carries a `.gitkeep`. Exactly one survives in this repository, `payload/.agents/skills/.gitkeep`, holding open the directory that receives skills in a later version.

> [!IMPORTANT]
> **`.gitkeep` files must never reach a consumer.** `payload/` is copied verbatim, so a copy that walks the tree naively will deliver `.gitkeep` into every repository that syncs, forever, in a directory the consumer never asked for. They are scaffolding for this repository, not content for anyone else's.
>
> Both engines exclude them by name, and the `🧹 Scaffolding Never Ships` job in CI drives **both** and asserts that neither would deliver one. Asserting against the emit set rather than against the tree is what makes the check meaningful: the sentinel above is correct and must stay, so a rule that simply banned the filename would be red on day one.

The rule has a second half that fires the other way. **A `.gitkeep` sitting beside a real file is dead scaffolding**, because it stopped holding anything open the moment that sibling appeared, and `check.py` reports it as a violation. That is how a stale sentinel gets swept into an emit set by hand years later.

The same logic applies to anything else added here purely to satisfy a tool. **If a file exists to serve this repository, it does not belong under `payload/`.**

---

## 🤖 Why This Repository Carries Its Own Instruction Files

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` appear at the repository root **and** under `payload/`. They are not duplicates by accident.

The copies under `payload/` are the **source**: the bytes that get delivered. The copies at the root are **this repository consuming its own output**, so the tooling that reads instruction files here reads exactly what a consumer would. A publisher that does not run its own product finds every defect second, after somebody else does.

The root copies are generated. Edit the ones under `payload/`.

---

## 📁 Naming

Directory and file names follow the canonical documentation standard in [`tannergolden/standards`](https://github.com/tannergolden/standards), under `docs/technical/interface/`, which this repository follows **by link and never by copy**. The link is to the repository rather than to a file on a branch on purpose: a branch-form URL is the shape `check.py`'s own `permalink` rule rejects, and although that rule is scoped to `payload/` and never runs over `docs/`, a document explaining this repository's naming law should not be carrying the one link shape this repository refuses to publish. The rules that bite most often here:

- Documentation filenames are Capitalized-Kebab with `&` as the conjunction, never the word `And`.
- No underscore as a word separator anywhere in the tree, except where a platform or language fixes the name.
- Paths under `payload/` are the exception that proves the rule: they are named by the **vendor** that reads them, so `.claude/`, `.agents/` and `.ai/` are correct exactly as spelled and must never be tidied.

### 🚫 Why `payload/` Carries No Chrome

`payload/AGENTS.md`, `payload/CLAUDE.md` and `payload/GEMINI.md` deliberately carry **no centred header, no `<a name="top"></a>`, no bold description, no italic tagline, no badges and no footer**. Everywhere else in this fleet those elements are mandatory. Here they are a decision, recorded so the next documentation sweep does not "fix" it:

- These files are **always-loaded bytes in six working trees**, not pages anyone browses. Every byte of chrome is context spent on decoration in every agent session in every consuming repository, forever.
- The two routers carry one import line each. The `GEMINI.md` this replaces was 1,247 bytes of frontmatter and centred chrome wrapping a single markdown link, which is the whole argument in one file.
- Hidden-comment frontmatter with exactly four kebab-case tags **is** present, because that part is machine-checked and costs four lines.

Adding chrome to these would also duplicate it, since the root copies are generated from them.

---

### 🔗 See also

> [!TIP]
> The README explains what this repository publishes and how a consumer receives it. This file only explains where things sit on disk.

---

<div align="center">

**One directory ships. The rest exists to get it there safely.**

[↑ Back to Top](#top)

</div>
