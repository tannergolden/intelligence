<!--
title: '📚 KNOWLEDGE'
description: 'The public facts about tannergolden''s setup that the home kit installs beside the rules: facts, never rules, and never personal context.'
tags: [knowledge, facts, home-kit, privacy]
category: docs
-->

<div align="center">

# 📚 KNOWLEDGE

<a name="top"></a>

**What an agent cannot infer about this setup, in a few public sentences.**

_Facts beside the rules. Nothing personal anywhere._

</div>

---

## 💡 What This Folder Is For

The rules say what to do. These facts say how the setup works, so the rules
can be followed without guessing: where work integrates, who merges, what
the guard does, and why `git commit -s` misbehaves in a cloud session.

[`public.json`](public.json) holds them. `scripts/kit.py` renders them as
their own block, between `INTELLIGENCE:KNOWLEDGE` markers, and the home kit
installs it beside every home copy of the rules:

| App                   | Where the facts land                                             |
| :-------------------- | :--------------------------------------------------------------- |
| Claude Code           | `~/.claude/rules/intelligence-knowledge.md`                      |
| Claude cloud sessions | A second block in `~/.claude/CLAUDE.md`, from the setup script   |
| Codex and Antigravity | A second block in `~/.codex/AGENTS.md` and `~/.gemini/AGENTS.md` |
| Copilot               | `~/.copilot/instructions/intelligence-knowledge.instructions.md` |

Repositories never receive them: the block in each `AGENTS.md` stays the
rules alone.

---

## 🔒 What May Go In

**Everything here is public**, because the home copies load in public
repositories too. The renderer refuses a fact that:

- is not one printable ASCII sentence ending in a period, or runs past 300
  characters;
- names a tannergolden repository that is not public;
- pushes the facts past their 2,000-character cap.

Personal context, preferences and anything private wait for a private tier,
which the public tannergolden/knowledge repository is set aside for.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                        | Purpose                                                                                                                                            |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`public.json`](public.json) | The public tier of knowledge: facts about tannergolden's setup that an agent cannot infer, installed into each app's home folder beside the rules. |
| [`README.md`](README.md)     | This file.                                                                                                                                         |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**What the setup is, never who the person is.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
