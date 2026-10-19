<!--
title: '📚 KNOWLEDGE'
description: 'The public facts about tannergolden''s setup that the home kit installs beside the rules, where they land, and what may go in: facts, never rules, and never personal context.'
type: guide
keywords: [facts, home-kit, privacy]
-->

<div align="center">

# 📚 KNOWLEDGE

<a name="top"></a>

**What the setup is, so the rules can be followed without guessing.**

_Facts, never rules. Public, never personal._

</div>

---

## 💡 What It Is

The rules say what to do. These facts say how the setup works, so the rules
can be followed without guessing: where work integrates, who merges, what the
guard does, and why `git commit -s` misbehaves in a cloud session.

[`knowledge/public.json`](../../knowledge/public.json) holds them.
`scripts/kit.py` renders them as their own block, between
`INTELLIGENCE:KNOWLEDGE` markers, and the [home kit](The-Home-Kit.md) installs
it beside every home copy of the rules:

| App                   | Where the facts land                                             |
| :-------------------- | :--------------------------------------------------------------- |
| Claude Code           | `~/.claude/rules/intelligence-knowledge.md`                      |
| Claude cloud sessions | A second block in `~/.claude/CLAUDE.md`, from the setup script   |
| Codex and Antigravity | A second block in `~/.codex/AGENTS.md` and `~/.gemini/AGENTS.md` |
| Copilot               | `~/.copilot/instructions/intelligence-knowledge.instructions.md` |

Repositories never receive them: the block in each `AGENTS.md` stays the rules
alone.

---

## 🔒 What May Go In

**Everything in it is public**, because the home copies load in public
repositories too. The renderer refuses a fact that:

- is not one printable ASCII sentence ending in a period, or runs past 300
  characters;
- names a tannergolden repository that is not public;
- pushes the facts past their 2,000-character cap.

Personal context, preferences and anything private wait for a private tier,
which the public tannergolden/knowledge repository is set aside for.

---

## 🔗 See Also

- [ADR-0016](../adrs/ADR-0016-Knowledge-Starts-As-Public-Facts.md): knowledge starts as public facts beside the rules

---

<div align="center">

**What the setup is, never who the person is.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
