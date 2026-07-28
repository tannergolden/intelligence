<!--
title: '🤖 AI INFRASTRUCTURE'
description: 'The publisher of agent instructions and skills that any repository can pull at a pinned tag, written once and delivered without a build step.'
tags: [agent-infrastructure, distribution, skills, publisher]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 AI INFRASTRUCTURE

<a name="top"></a>

**One set of agent instructions and a library of skills, authored once here and pulled by any repository at a pinned tag.**

_Written once. Pinned deliberately. Never pasted by hand._

</div>

---

## 🎯 Our Strategic Intent

Every coding agent wants the same thing: the conventions of the repository it is working in. Each one insists on a different filename. The usual answer is to copy the file by hand, which drifts the first time one copy is edited. The other answer is to link, which fails because **agents do not reliably follow links**.

This repository is the third answer. `AGENTS.md` holds the law, two one-line routers carry it to the tools that cannot find it, and a downstream repository pulls all three at a tag. There is **no build step**: the files here are the files that land, so reviewing a release is reading a diff of what will arrive.

It follows the same shape as [`tannergolden/standards`](https://github.com/tannergolden/standards), which publishes workflows the same way: pin a major, receive every later fix when that tag moves.

---

## 🤖 Supported Tools

Support means tested, not merely reachable.

| Tool                              | Reads                                    | Cost to support |
| :-------------------------------- | :--------------------------------------- | :-------------- |
| **GitHub Copilot** (coding agent) | `AGENTS.md`, natively                    | nothing         |
| **GitHub Copilot** (CLI)          | `AGENTS.md`, natively                    | nothing         |
| **GitHub Copilot** (VS Code)      | `AGENTS.md`, once one setting is enabled | one toggle      |
| **Claude Code**                   | `CLAUDE.md`, which imports `AGENTS.md`   | one envelope    |
| **Gemini CLI**                    | `GEMINI.md`, which imports `AGENTS.md`   | one envelope    |
| anything else reading `AGENTS.md` | `AGENTS.md`                              | nothing         |

> [!IMPORTANT]
> **VS Code Copilot ignores `AGENTS.md` until you enable `chat.useAgentsMdFile`.** It is experimental and off by default, so a developer who has not set it gets no instructions and no warning. It is a one-time per-developer setting, the same shape of cost as Gemini's folder-trust prompt.

Claude Code has no discovery path for `AGENTS.md` at all, and Gemini CLI discovers only `GEMINI.md` unless configured otherwise. Both facts were verified against the shipped tools rather than taken from documentation. That is why two routers exist, and why each will become deletable the day its vendor adopts the canonical filename.

---

## 📥 Installing the Agent Files

A downstream repository commits **one workflow** and receives `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` from then on. There is no native `uses:` for content, so the pin lives on a checkout step rather than a `uses:` line.

<details>
<summary>Click to view the full sync workflow</summary>

```yaml
name: '🤖 Sync AI Instructions'

on:
  workflow_dispatch:
  schedule:
    - cron: '23 5 * * 1'

concurrency:
  group: ${{ github.workflow }}
  cancel-in-progress: false

permissions: {}

jobs:
  sync:
    name: '🤖 Pull the Agent Files'
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      contents: write
    steps:
      - name: '📂 Checkout this repository'
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1

      # THE PIN. `v1` moves when a release is cut, so a fix arrives here on
      # the next run. Change it to v2 deliberately, never automatically.
      - name: '📥 Fetch the agent files at the pinned tag'
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          repository: tannergolden/ai
          ref: v1
          path: .ai-source
          persist-credentials: false

      - name: '📤 Copy and push if anything changed'
        run: |
          set -euo pipefail
          cp .ai-source/AGENTS.md .ai-source/CLAUDE.md .ai-source/GEMINI.md .
          rm -rf .ai-source
          git config user.name 'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add AGENTS.md CLAUDE.md GEMINI.md
          if git diff --cached --quiet; then echo 'Already current.'; exit 0; fi
          git commit -m 'chore(agents): sync agent files from tannergolden/ai tag v1'
          git push
```

</details>

No token, no secret, no app. The built-in `GITHUB_TOKEN` reads this public repository and pushes to its own, and pushes made with that token start no further workflow runs, so a sync into a quiet repository stays quiet.

**Four things that will bite**, in likelihood order: a protected default branch rejects the push; the first run overwrites a hand-written `AGENTS.md`, so dispatch it once and read the diff before trusting the schedule; a repository with no activity for 60 days has its schedule disabled by GitHub; and the workflow can never update itself, because no token available to it can write under `.github/workflows/`.

---

## 📦 Skills

Skills are **downloadable, never synced**. There is no directory both supported tools read, so committing them into every repository would mean two copies that drift. One canonical copy lives here and you place it where your tool looks.

| Tool            | Copy the skill directory into            |
| :-------------- | :--------------------------------------- |
| **Claude Code** | `.claude/skills/<name>/`                 |
| **Gemini CLI**  | `.agents/skills/<name>/`                 |

Each skill is a directory, and the directory name is the contract: it is what you type to invoke, and `name` in the frontmatter must equal it.

```bash
skills/<name>/
├── SKILL.md          # required. Navigation, not content. Under 500 lines
├── references/       # detail, loaded only when SKILL.md says to
├── assets/           # templates and resources
└── evals/
    └── evals.json    # the evidence it beats its own baseline
```

Three tiers, three costs, and this is what every authoring rule is defending:

| Tier | What | Loads | Cost |
| :--- | :--- | :--- | :--- |
| A | `name` + `description` | at startup, for **every** skill, used or not | always paid |
| B | `SKILL.md` body | on invocation | **persists the whole session**, never re-read |
| C | bundled files | only when the body sends the agent there | zero until used |

> [!IMPORTANT]
> **Write the description for a person as well as a model.** Gemini CLI shows it in a consent prompt asking the user to grant access to the whole skill directory. Keyword soup reads well to a matcher and badly to a human, and a consent prompt nobody reads is a control you have already lost.

Frontmatter is **two fields**, `name` and `description`, plus the optional `license`, `compatibility` and `metadata`. `allowed-tools` is banned outright. Claude-only keys and `` !`command` `` shell injection are permitted **only** in a skill that declares itself with `compatibility`, because both are silently inert on the other two tools.

`SKILL.md` frontmatter uses `---` fences, unlike every other document here. That is correct: the Agent Skills specification requires it.

---

## 🛡️ What May Live Here

Four rules. They exist because this repository is where a second law would go unnoticed.

1. **Law is universal, or it is not law.** No rule in `AGENTS.md` may depend on a capability some supported tool lacks, or on a fact only one repository can vouch for.
2. **Carriers are vendor-specific and carry nothing.** `CLAUDE.md` and `GEMINI.md` are envelopes. They are allowed to differ precisely because they hold no content that could drift.
3. **Supported means a named surface, tested.** Not a product. Copilot's coding agent reads the law by default and its JetBrains client reportedly does not, and both are called Copilot.
4. **Nothing executes on clone.** No hooks, no `settings.json`, no plugin manifest, no MCP configuration, no per-tool rule or command dialects. A skill bundling `scripts/` is the one boundary crossing, and the checker reports it every time.

---

## 🔎 What Is Checked

[`.github/actions/check-skills`](.github/actions/check-skills) validates every skill against the specification and the portability rules. It is a composite action, so any repository with skills can use it:

```yaml
- uses: tannergolden/ai/.github/actions/check-skills@v1
  with:
    path: skills
```

It gates on the shape of the frontmatter, `name` matching its directory, description and body size, dangling and escaping references, unreferenced files in the directory, live import tokens, invisible characters, and banned or undeclared vendor keys. It warns on a missing eval suite and on bundled scripts.

The most important job in [`skills.yml`](.github/workflows/skills.yml) is the one asserting the checker **fails** on [`tests/fixtures/skills`](tests/fixtures/skills). A checker that has never rejected anything has never been tested, and one that silently stopped matching looks exactly like a clean repository.

---

## 🏷️ Cutting a Release

Two tags, two contracts, and no release machinery:

```bash
git tag v1.0.0 && git push origin v1.0.0
git tag -f v1 && git push --force origin v1
```

`vX.Y.Z` is immutable, for anyone who wants exactness. `v1` moves, and is the pin everyone actually uses. Rolling back is the same force-move aimed at the last good commit, and it reaches consumers on their next scheduled run rather than immediately, which is the honest price of having no fleet-wide credential.

---

## 🔗 See also

> [!TIP]
> [`AGENTS.md`](AGENTS.md) is the law itself and the only file here with rules in it. The engineering standards this repository is built to live in [`tannergolden/standards`](https://github.com/tannergolden/standards) and are followed by link, never by copy.

---

<div align="center">

`publishes: one law, two envelopes, many skills` &middot; `pinned by: tag`

**One source of law. One copy of every skill. No stale duplicates anywhere.**

[↑ Back to Top](#top)

</div>
