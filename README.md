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

Claude Code has no discovery path for `AGENTS.md` at all, and Gemini CLI discovers only `GEMINI.md` unless configured otherwise. Both were verified against the shipped tools rather than taken from documentation, and both routers become deletable the day their vendor adopts the canonical filename. See [Vendor Facts](docs/Vendor-Facts.md).

---

## 📦 What Is Published

| Path                          | What it is                                                        |
| :---------------------------- | :---------------------------------------------------------------- |
| `AGENTS.md`                   | The law. The only file in this repository with rules in it        |
| `CLAUDE.md`, `GEMINI.md`      | Envelopes. One import line each, carrying no law of their own     |
| `skills/<name>/`              | Skills, one canonical copy each, installed rather than synced     |

Nothing here executes on clone, and nothing is generated from anything else.

---

## 🚀 Getting Started

**To receive the agent files**, commit one workflow that checks this repository out at `ref: v1` and copies the three markdown files in. The full stub, the four ways it fails, and the removal steps are in [Installation](docs/Installation.md).

**To install a skill**, copy its directory into `.claude/skills/` for Claude Code or `.agents/skills/` for Gemini CLI. There is no directory both tools read, which is why skills are installed rather than synced.

**To write a skill**, read [Skill Authoring](docs/Skill-Authoring.md) and then [`skills/conventional-commit/`](skills/conventional-commit/SKILL.md), which is the reference implementation and passes every gate.

**To add anything to this repository**, read [Scope & Boundaries](docs/Scope-&-Boundaries.md) first. It exists to stop a second law appearing here.

---

## 🔎 What Is Checked

[`.github/actions/check-skills`](.github/actions/check-skills) validates every skill against the Agent Skills specification and the cross-vendor portability rules. It is a composite action, so any repository with skills can use it:

```yaml
- uses: tannergolden/ai/.github/actions/check-skills@v1
  with:
    path: skills
```

The most important job in [`skills.yml`](.github/workflows/skills.yml) is the one asserting the checker **fails** on [`tests/fixtures/skills`](tests/fixtures/skills). A checker that has never rejected anything has never been tested, and one that silently stopped matching looks exactly like a clean repository.

[`ci.yml`](.github/workflows/ci.yml) is a stub calling the shared reusable workflow in `standards` rather than a private copy of it, so spelling, link checking and documentation linting stay in one place for the whole fleet.

---

## 🔗 See also

> [!TIP]
> [`docs/`](docs/README.md) is the index of everything above, in more detail and with the reasoning attached. [`AGENTS.md`](AGENTS.md) is the law itself. The engineering standards this repository is built to live in [`tannergolden/standards`](https://github.com/tannergolden/standards) and are followed by link, never by copy.

---

<div align="center">

`publishes: one law, two envelopes, many skills` &middot; `pinned by: tag`

**One source of law. One copy of every skill. No stale duplicates anywhere.**

[↑ Back to Top](#top)

</div>
