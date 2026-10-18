<!--
title: '🧰 SKILLS'
description: 'The skills the home kit installs into every AI coding app, each a folder in the open Agent Skills format.'
tags: [skills, agent-skills, home-kit, procedures]
category: docs
-->

<div align="center">

# 🧰 SKILLS

<a name="top"></a>

**Procedures an agent loads only when the task in front of it needs them.**

_One skill for now: the one that builds the rest._

</div>

---

## 💡 What This Folder Is For

A skill is a folder an agent opens only when its description matches the
task. The universal rules stay in the always-loaded block; a skill carries a
procedure. For now there is exactly one, by the owner's decision:

| Skill                                          | What it does                                                                                                                           |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| [`building-skills/`](building-skills/SKILL.md) | Builds a new skill or repairs one that misfires: decides whether it should be a skill at all, writes `SKILL.md`, tests it and ships it |

`scripts/kit.py` bundles every folder here into `home/kit.json`, and the home
kit copies each one into `~/.agents/skills/`, `~/.claude/skills/` and
Antigravity's `~/.gemini/antigravity-cli/skills/`, with a mark that lets it
replace its own folders and refuse anyone else's.

---

## 🧱 What Every Skill Here Follows

The renderer refuses a skill that breaks any of these, because each one is a
rule some app enforces by silently not loading the skill:

- The folder name is the skill's `name`: lowercase words joined by single
  hyphens, at most 64 characters, without `claude` or `anthropic`.
- `SKILL.md` opens with a `---` frontmatter fence holding only `name`,
  `description`, `license`, `compatibility`, `metadata` and `allowed-tools`.
- The description is at most 1,024 characters, has no angle brackets, and
  says when to use the skill with "Use when".
- The body stays under 500 lines, and files sit at most one level below it.

> [!NOTE]
> **Skill files are exempt from Document Styling.** Loaders read frontmatter
> only from a `---` fence on the first line, and every line of a skill is
> paid for in context, so `SKILL.md` and the files beside it carry no hidden
> comment frontmatter and no decorative header or footer. For the same
> reason a skill folder has no `README.md`: it would ship with the skill.

Each skill's trigger test lives in [`evals/skills/`](../evals/skills/README.md),
outside its folder, so it never ships.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                  | Purpose                                                       |
| :------------------------------------- | :------------------------------------------------------------ |
| [`building-skills/`](building-skills/) | The one skill: how to build, test and ship every other skill. |
| [`README.md`](README.md)               | This file.                                                    |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Load the procedure when the task calls for it, and only then.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
