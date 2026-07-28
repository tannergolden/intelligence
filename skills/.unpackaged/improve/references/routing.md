# Routing A Lesson

One destination is safe to write to and the others are not, so settle that
before deciding anything else.

## What a sync can reach

`AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and any router beside them are the
files most commonly **delivered from a publisher and overwritten in full on
a schedule**. Where that is what they are, an edit survives until the next
run and then vanishes, taking the lesson with it and reporting nothing.

You cannot tell from inside the repository which kind you have. A delivered
file often announces itself, and often does not: the notice is a courtesy
its author chose to write, not a guarantee of the format. A sync workflow
may be named anything, or may live in a system that is not in the tree at
all.

**So do not try to tell.** The two errors are not equally priced:

| Guess | Wrong how | Cost |
| :--- | :--- | :--- |
| It is hand-written, so edit it | it was synced | lesson destroyed, silently, unrecoverably |
| It is synced, so write elsewhere | it was hand-written | lesson lands in the repository's notes instead |

A heuristic whose failure mode is silent data loss is not worth the accuracy
it buys. The instruction files are simply never a destination, and a lesson
that belongs in one is drafted for the user, who knows where their file
comes from.

**Everything a repository owns is safe**: its docs, its notes, instructions
sitting beside the code they govern. Nothing overwrites those, so that is
where lessons go.

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

## The instinct to resist

The instruction files are usually what the lesson is *about*, so fixing the
instructions where you read them feels like the obvious move. It is the one
move this skill exists to prevent. Draft the entry, hand it over, and let
the person who knows the file's origin decide.

## Two lessons that look like one

A single incident often produces both kinds, and splitting them is worth the extra minute:

> The agent hardcoded a path that only existed on one machine, and the deploy silently used a stale artifact.

- **Universal:** a machine-specific path is an instruction that fails for everyone who is not the author.
- **Local:** this deploy reports success on a stale artifact rather than failing, so it needs an explicit freshness check.

Recorded as one entry, it lands in the wrong place whichever way it goes.
