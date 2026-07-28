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

**Agent instructions and skills, authored once here and pulled at a tag you pin.**

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
| `skills/.unpackaged/<name>/`  | Skills, one canonical copy each, installed rather than synced     |

Nothing here executes on clone, and nothing is generated from anything else.

---

## 🚀 Getting Started

**To receive the agent files**, commit one workflow that checks this repository out at `ref: v1` and copies the three markdown files in. The full stub, the four ways it fails, and the removal steps are in [Installation](docs/Installation.md).

**To install a skill**, copy its directory into `.claude/skills/` for Claude Code or `.agents/skills/` for Gemini CLI. There is no directory both tools read, which is why skills are installed rather than synced.

**To write a skill**, install [`develop`](skills/.unpackaged/develop/SKILL.md), the meta skill that walks you through authoring one, and read [Skill Authoring](docs/Skill-Authoring.md) for the rules it enforces.

**To add anything to this repository**, read [Scope & Boundaries](docs/Scope-&-Boundaries.md) first. It exists to stop a second law appearing here.

---

## 🔎 What Is Checked

[`.github/actions/check-skills`](.github/actions/check-skills) validates every skill against the Agent Skills specification and the cross-vendor portability rules. It is a composite action, so any repository with skills can use it:

```yaml
- uses: tannergolden/ai/.github/actions/check-skills@v1
  with:
    path: skills/.unpackaged
```

The most important job in [`skills.yml`](.github/workflows/skills.yml) is the one asserting the checker still **rejects** known-bad input. It builds four deliberately broken skills in a temporary directory and checks that every rule fires by name, warnings included, since the rules catching the quietest defects are the advisory ones. A checker that has never rejected anything has never been tested, and one that silently stopped matching looks exactly like a clean repository.

[`scripts/check-docs.py`](scripts/check-docs.py) audits every document against the styling standard published in `standards`, followed **by link** rather than copied. It encodes only the subset a machine can decide: frontmatter shape and tag count, the header and footer blocks, banned typography, fence languages, prompt characters, alt text, and the uniqueness of every tagline and closing phrase.

[`ci.yml`](.github/workflows/ci.yml) is a stub calling the shared reusable workflow in `standards` rather than a private copy of it, so spelling, link checking and documentation linting stay in one place for the whole fleet. It passes **no commands**: every stage resolves to the `make` target of the same name.

```bash
make lint       # skills, against the Agent Skills specification
make lint-docs  # documents, against the styling standard
make test       # prove both checkers still reject known-bad input
make build      # package every skill into dist/
```

That `lint-docs` line is the reason the [`Makefile`](Makefile) exists at all. It is the one CI stage with no input override, so before there was a Makefile here the documentation step reported "skipped" on every green run, and the rule `AGENTS.md` calls the one broken most often was checked by nothing.

---

## 📚 Documentation Index

Everything above in more detail, with the reasoning attached, lives in the [Documentation Index](docs/README.md). [`AGENTS.md`](AGENTS.md) is the law itself and the only file here with rules in it.

The engineering standards this repository is built to are published in [`tannergolden/standards`](https://github.com/tannergolden/standards) and followed **by link**, never by copy. A standard copied into a repository is a standard that starts going stale the moment it is pasted.

---

<div align="center">

**One source of law. One copy of every skill. No stale duplicates anywhere.**

[↑ Back to Top](#top)

</div>
