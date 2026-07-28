# Routing A Lesson

How many destinations exist depends on who owns the instruction files, so
settle that first. Getting it wrong either destroys the lesson or refuses to
record it anywhere useful.

## Owned here, or published from elsewhere

Open the instruction file the repository uses and read its opening. A file
delivered by a sync **says so**, usually in its first paragraphs, because
being silently overwritten is precisely what its author had to warn about.
A workflow under `.github/workflows/` that checks out another repository and
copies files in is the other reliable signal.

| Signal | Arrangement | Destinations |
| :--- | :--- | :--- |
| Declares itself published, synced or generated | **Published** | Two: local context, and upstream |
| Declares nothing, and nothing fetches it | **Owned here** | One: this repository |
| No instruction file exists at all | **Owned here** | One: this repository |

**Most repositories in the world are the owned-here case.** `AGENTS.md` is a
widely adopted open standard that tens of thousands of projects write by
hand. Assuming every one of them is a published copy is the mistake this
section exists to prevent: it would refuse to write a lesson into the one
file that is exactly the right place for it.

**When the files are owned here, the instruction file is a normal
destination.** There is no upstream, no sync to destroy the edit, and no
proposal to draft. A lesson that sounds universal is still just a lesson;
record it and move on.

Everything below applies to the **published** arrangement, where the local
copies are delivered and a second destination exists.

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

## The files that are never a destination, when they are published

In a published arrangement, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and any
router beside them are **delivered copies, overwritten in full on every
sync**. An edit there survives until the next scheduled run and then
vanishes, taking the lesson with it and leaving no trace that anything was
lost.

This is the most likely way to route a lesson wrongly, because those files are usually what the lesson is *about*. The instinct to fix the instructions where you read them is exactly the instinct to resist.

A universal lesson goes upstream as a proposal, not into the local copy of the law. See `upstream.md`.

## Two lessons that look like one

A single incident often produces both kinds, and splitting them is worth the extra minute:

> The agent hardcoded a path that only existed on one machine, and the deploy silently used a stale artifact.

- **Universal:** a machine-specific path is an instruction that fails for everyone who is not the author.
- **Local:** this deploy reports success on a stale artifact rather than failing, so it needs an explicit freshness check.

Recorded as one entry, it lands in the wrong place whichever way it goes.
