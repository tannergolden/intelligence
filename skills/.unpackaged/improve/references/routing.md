# Routing A Lesson

Two destinations. Sending a lesson to the wrong one either loses it silently or forces it on repositories it was never true of.

## The test

> Would this still be true in a repository with a different language, a different toolchain, a different branch model and a different review policy?

**No** makes it local. **Yes** makes it universal. Most lessons are local, and a loop that mistakes that ratio ends up rewriting the shared law every week.

| Lesson | Route | Why |
| :--- | :--- | :--- |
| "Integration tests need the database container running first" | local | A repository with no database has no use for it |
| "The deploy script must run from the repository root" | local | It describes one script |
| "Files are UTF-8 with exactly one trailing newline" | universal | True of any repository, whatever it is for |
| "A path that only resolves on the author's machine breaks for everyone else" | universal | Independent of language and toolchain |

When it is genuinely borderline, it is local. A rule that turns out to be universal can be promoted later from a repository that has been living with it. A rule pushed into the shared law wrongly is a rule that reaches every repository at once.

## Where a local lesson goes

**NEVER assume a layout.** Repositories organize their knowledge differently on purpose, and writing to a directory this one does not use creates a second place to look that nobody reads.

Look in this order and stop at the first that fits:

1. **What the root `README.md` points to.** A repository that organizes deliberately usually says where, in the first screen.
2. **Instructions beside the code the lesson concerns.** A file governing that folder outranks anything further away, and a lesson about one subsystem belongs next to it.
3. **A repository-wide knowledge directory**, under whatever name it carries: a docs tree, a notes folder, a vault, a committed wiki.

**Append to what exists** rather than starting a parallel file. Create a new one only when nothing suitable does, put it where the repository's own convention indicates, and say plainly in your report that you created it and why.

## The files that are never a destination

`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and any router beside them are **published from upstream and overwritten in full on every sync**. An edit there survives until the next scheduled run and then vanishes, taking the lesson with it and leaving no trace that anything was lost.

This is the most likely way to route a lesson wrongly, because those files are usually what the lesson is *about*. The instinct to fix the instructions where you read them is exactly the instinct to resist.

A universal lesson goes upstream as a proposal, not into the local copy of the law. See `upstream.md`.

## Two lessons that look like one

A single incident often produces both kinds, and splitting them is worth the extra minute:

> The agent hardcoded a path that only existed on one machine, and the deploy silently used a stale artifact.

- **Universal:** a machine-specific path is an instruction that fails for everyone who is not the author.
- **Local:** this deploy reports success on a stale artifact rather than failing, so it needs an explicit freshness check.

Recorded as one entry, it lands in the wrong place whichever way it goes.
