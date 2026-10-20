<!--
title: '💬 PROMPTS'
description: 'The ready-made prompts every repository gets in docs/Prompts.md: the universal ones the hub keeps current between their markers, the section each repository fills with its own, and how to change either.'
type: guide
keywords: [prompts, repository-sync, prompt-engineering]
-->

<div align="center">

# 💬 PROMPTS

<a name="top"></a>

**Ready-made prompts in every repository, so nobody has to write a good one from scratch.**

_Copy one. Fill it in. Paste it._

</div>

---

## 💡 What A Repository Gets

A prompt typed in a hurry leaves out what an agent needs: the goal, the
context it cannot see, the limits, and how to tell when it is done. So every
repository that takes part in [sync](Repository-Sync.md) gets
`docs/Prompts.md`, a page of prompts anyone can copy into any AI app, the
owner and every collaborator alike. Each prompt sits in its own fenced block,
so GitHub shows a copy button on it, and marks what changes from one use to
the next with a placeholder in double braces, such as `{{ERROR_OUTPUT}}`.

The file has two parts, split the way `AGENTS.md` is:

| Part                                             | Whose                     | What it holds                                                                                                                               |
| :----------------------------------------------- | :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| Between the `INTELLIGENCE:PROMPTS` markers       | The hub's, kept current   | How to use a prompt; five universal prompts: fix a bug, add a feature, review a change, explain code, and write a new prompt; the practices |
| "Prompts For This Repository", after the markers | The repository's, its own | The prompts its owner writes for the work that repository does                                                                              |

The last universal prompt turns a rough request into a new prompt in the same
shape and adds it to the repository's own section, so writing a good prompt
needs no study first.

---

## 🔁 How It Arrives And Stays Current

The prompts ride in the same `chore/intelligence` pull request as the rules,
by either route, the stub or `make sync`:

- a repository without `docs/Prompts.md` gets the whole file, which you review
  by hand: `make merge` leaves a pull request that adds it alone;
- after that, each sync replaces only the text between the markers, and
  leaves the rest of the file, the repository's own prompts included, as it
  was;
- the BEGIN marker carries the SHA-256 of the block's text, so a release that
  leaves the prompts as they were touches no repository, and a hand edit
  inside the markers is caught, by `make audit`, by the standards' Machined
  Block Check in each repository's CI, and by the guard hook, and repaired by
  the next sync;
- a `docs/Prompts.md` with no prompts block is the repository's own file, and
  sync never touches it;
- a `no-intelligence-prompts` topic keeps the prompts out of a repository that
  still takes the rules.

Only a release delivers them, as with the rules. A release from before the
prompts delivers none.

---

## ✍️ Changing The Universal Prompts

The source is [`setup/Prompts.md`](../../setup/Prompts.md): the file exactly as
a repository first gets it, with its markers unsealed, so it stays a file
anyone can edit. [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py)
seals the block when sync delivers it, and `make check` holds the source to
what every public repository can carry:

- exactly one `INTELLIGENCE:PROMPTS` block, with markers that carry no hash;
- no private repository named, and no en or em dash;
- every universal prompt with its **Use when** and **Fill in** lines, and every
  block of code marked `text`, which a formatter leaves alone.

Keep the file as Prettier writes it, with the standards' configuration: each
repository formats what a push touched, and a reformatted block would read as
edited. Then, in the pull request a release delivers, run `make check`. A
prompt that only one repository needs goes in that repository's own section,
never here.

---

## 🔗 See Also

- [ADR-0025](../adrs/ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): why the prompts reach every repository, and how they are split
- [Repository Sync](Repository-Sync.md): the pull request both blocks ride in
- [The Home Kit](The-Home-Kit.md): the guard hook that keeps both blocks as the hub wrote them

---

<div align="center">

**A better prompt in, better work out.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
