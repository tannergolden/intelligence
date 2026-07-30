<!--
title: '📥 INSTALLATION'
description: 'How another repository receives the agent files at a pinned tag, how a skill is installed, and every way the sync fails.'
tags: [installation, distribution, sync, adoption]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 📥 INSTALLATION

<a name="top"></a>

**One committed workflow, seven files delivered, two of which execute unprompted.**

_Pin it once, receive every fix, edit nothing._

</div>

---

## 🎯 The Shape

GitHub resolves `owner/repo/path@ref` natively for actions and reusable workflows, and for nothing else. There is **no `uses:` for content**, so the pin lives on a checkout step instead of a `uses:` line. Everything else works exactly like [`tannergolden/standards`](https://github.com/tannergolden/standards): pin a major, receive every later fix when that tag moves.

---

## 📄 The Agent Files

A consuming repository commits **one workflow** and receives `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` from then on.

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
          repository: tannergolden/intelligence
          ref: v1
          path: .ai-source
          persist-credentials: false

      - name: '📤 Copy and push if anything changed'
        run: |
          set -euo pipefail
          cp .ai-source/AGENTS.md .ai-source/CLAUDE.md .ai-source/GEMINI.md .
          git config user.name 'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add AGENTS.md CLAUDE.md GEMINI.md

          # ---- THE SKILL ROUTER. Delete this whole block, through its own
          # ---- `git add`, to take the instruction files and no executable
          # ---- content at all.
          mkdir -p .claude/hooks .gemini/hooks
          cp .ai-source/.claude/hooks/skill-router.sh .claude/hooks/
          cp .ai-source/.gemini/hooks/skill-router.sh .gemini/hooks/
          # NEVER overwrite a settings file this repository already owns: it is
          # where `permissions.deny` and this team's own hooks live. The scripts
          # above still update on every sync, so fixes still reach you; only the
          # registration is written once.
          [ -f .claude/settings.json ] || cp .ai-source/.claude/settings.json .claude/
          [ -f .gemini/settings.json ] || cp .ai-source/.gemini/settings.json .gemini/
          for d in .claude .gemini; do
            if git check-ignore -q "$d"; then
              echo "::error::$d is gitignored here, so the router cannot be committed. Un-ignore it, or delete this block."
              exit 1
            fi
            git add -A -- "$d"
          done
          # ---- end of the skill router block

          rm -rf .ai-source
          if git diff --cached --quiet; then echo 'Already current.'; exit 0; fi
          git commit -m 'chore(agents): sync agent files from tannergolden/intelligence tag v1'
          git push
```

</details>

> [!WARNING]
> **That block delivers executable content.** `.claude/` and `.gemini/` carry a skill router that runs unprompted on every prompt, and a hook in a project directory executes with no approval step in a headless session. It is bounded (it prints nothing unless skills are installed, and its output is gated in CI), and it is still code arriving on a schedule. **Delete that block to receive the instruction files alone**, which is the whole feature set this repository had before the router existed.
>
> Expect one extra consequence on Gemini: it fingerprints project hooks, so a sync that changes the hook command marks it new and untrusted and asks the user to approve it again.

No token, no secret, no app. The built-in `GITHUB_TOKEN` reads this public repository and pushes to its own, and **pushes made with that token start no further workflow runs**, so a sync into a quiet repository stays quiet.

Pin `@v1` to receive fixes, or a full `@v1.4.2` for exactness that no publisher-side change can reach.

---

## 🧯 The Ways It Fails

In likelihood order, because the first is common and the last is structural. There were four before the router shipped; there are six now, and that growth is part of what the router costs.

| Failure                                | What you see                                       | Fix                                                                        |
| :------------------------------------- | :------------------------------------------------- | :-------------------------------------------------------------------------- |
| **Protected default branch**           | the push is rejected by a ruleset                  | Check with `gh api repos/OWNER/REPO/rulesets`. A `pull_request` rule whose only bypass is the admin role rejects `github-actions[bot]` |
| **First run overwrites hand-written law** | your `AGENTS.md` is replaced by a bot commit    | Dispatch it once by hand and read the diff before trusting the schedule     |
| **Schedule silently disabled**         | nothing runs, no error anywhere                    | GitHub disables scheduled workflows after 60 days of repository inactivity and emails once. `workflow_dispatch` is the recovery |
| **The stub cannot update itself**      | a change to the workflow needs a human             | No token available to it can write under `.github/workflows/`. Budget one announced edit per major version |
| **Gemini asks about the hook again**   | a trust prompt after a routine sync                | Gemini fingerprints project hooks, so a changed command is a new one. Expected, not a fault |
| **You already had a settings file**    | the router never registers, and silently does nothing | The sync will not overwrite your `settings.json`. Copy the router block out of `.ai-source` into yours once, by hand |
| **`.claude/` is gitignored here**      | the sync fails with an error naming the directory  | Deliberate: forcing past a gitignore would commit files your repository chose to exclude. Un-ignore it, or delete the router block |

> [!IMPORTANT]
> **The three documents become owned by this publisher.** There is no ownership engine, no lockfile and no merge: they are overwritten in full on every sync. Repository-specific law belongs in that repository's own context, which the law itself tells every agent to go and find.

---

## 📦 Skills

Skills are **installed, never synced**. No directory both supported tools read exists, so committing them into a repository would mean two copies that drift.

| Tool            | Copy the skill directory into |
| :-------------- | :---------------------------- |
| **Claude Code** | `.claude/skills/<name>/`      |
| **Gemini CLI**  | `.agents/skills/<name>/`      |

Copy the whole directory, including `references/` and `assets/`. Leave `evals/` behind if you like: it is read by tooling, never by an agent.

---

## 🤖 One Manual Step, For Copilot In VS Code

Copilot's coding agent and its CLI read `AGENTS.md` with no setup. **VS Code does not**, until `chat.useAgentsMdFile` is enabled. It is experimental and off by default, so a developer who has not set it gets no instructions and no warning that anything is missing.

This is a per-developer setting rather than a per-repository file, which is why no file here fixes it. It is the same shape of cost as Gemini CLI's folder-trust prompt.

---

## 🗑️ Removing It

1. Delete `.github/workflows/ai-sync.yml`. Nothing further arrives, and no credential needs revoking because none was ever issued.
2. **Remove the executable content**, which step 1 does not do. Delete `.claude/hooks/skill-router.sh` and `.gemini/hooks/skill-router.sh`, then remove the `UserPromptSubmit` block from `.claude/settings.json` and the `BeforeAgent` block from `.gemini/settings.json`. Delete a settings file outright only if the router block is the whole of it; if you had your own `permissions` or hooks in there, edit rather than delete.
3. Delete `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`, or keep them. Once step 1 is done they are ordinary files nobody will touch again.
4. Delete any skill directories you copied in.

Nothing was installed outside the working tree, and once step 2 is done nothing from this publisher executes.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

The other half of this page is [Releases & Versioning](Releases-&-Versioning.md), which explains what moving `v1` actually does to every repository pinned to it.

---

<div align="center">

**One workflow in, seven files out, and a delete that finishes the job.**

[↑ Back to Top](#top)

</div>
