---
name: improve
description: Use this skill when an agent got something wrong and the correction should outlive the session, when the user says to remember something or stop repeating a mistake, or when a task ends and something was learned worth keeping. Applies whenever agent instructions are being changed for any reason. It is NOT for improving code: a request to refactor, optimize or clean something up is ordinary work.
---

## First, decide whether there is a lesson at all

**Most sessions produce none, and that is the normal outcome.** A lesson is a correction that would change what a future agent does on a different day. Recording anything less makes the instructions longer without making them better, and every line of an instruction file is paid in every session forever.

Not a lesson: a one-off typo, a thing the model already knows, a preference nobody has to follow, anything true only today.

A lesson: an environment fact an agent cannot infer, a call that reports success on failure, a convention that was broken because nothing stated it, a belief that turned out false.

If there is no lesson, say so and stop. Stopping is the common case.

## Grade it before you record it

**An unverified lesson is worse than no lesson**, because it is wrong forever and carries the authority of a written rule. An agent's account of why something failed is frequently mistaken, and the mistake is invisible once it is written down as fact.

Every recorded lesson carries one of three grades:

| Grade | Means |
| :--- | :--- |
| **probed** | Something ran and the result is reproduced in the entry |
| **documented** | A primary source says so, and the entry names it |
| **unverified** | Believed from a secondary source. Recorded as a lead, never as a rule |

Read `references/evidence.md` before grading anything, and always when the lesson came from a search result, a summary, or your own recollection of what happened earlier in the session.

## Then find out who owns the instruction files here

**Do this before deciding where anything goes.** Two arrangements exist and they route lessons in opposite directions, so guessing wrong either destroys the lesson or refuses to record it.

Open the instruction file this repository actually uses and read the top of it.

| What you find | The arrangement | What follows |
| :--- | :--- | :--- |
| It says it is **published, synced, or generated** from somewhere else, or a workflow in the tree fetches it | **Published.** The file is a delivered copy | Never edit it. Two destinations, below |
| It says nothing of the kind, and nothing fetches it | **Owned here.** The file is this repository's own | It is a normal destination. One destination |
| There is no instruction file at all | **Owned here**, trivially | Use the repository's own context |

A published file usually announces itself in its first paragraphs, because being overwritten silently is exactly what its author needed to warn about. A sync workflow under `.github/workflows/` naming another repository is the other reliable signal.

> [!IMPORTANT]
> **In a published arrangement, NEVER write a lesson into the instruction files.** They are overwritten in full on the next sync, so the edit is deleted without warning and the lesson is lost with no trace that anything was there. This is the single most likely way to get this wrong, because those files are usually what the lesson is *about*.

## Route it

**When the files are owned here**, there is one destination: this repository. A lesson about how this repository works goes into its own context, and the instruction file is a legitimate part of that context. Keep it in the file whose subject it matches.

**When the files are published**, there are two, and the test is:

> Would this lesson still be true in a repository with a different language, toolchain, branch model and review policy?

- **No, it is local.** It belongs in this repository's own context, which is somewhere other than the published files.
- **Yes, it is universal.** It belongs upstream with whoever publishes the law, from where it reaches every repository on the next sync.

Read `references/routing.md` when the call is not obvious, and always before creating any new file.

## Writing a local lesson

Find the repository's own context first: what its root `README.md` points to, then instructions sitting beside the code the lesson concerns, then a repository-wide knowledge directory under whatever name it carries.

**Append to what exists.** Create a new file only when nothing suitable does, and say plainly that you created it and why. A repository that already keeps decisions somewhere does not want a second place to keep them.

Copy `assets/lesson-template.md` for the entry shape.

## Drafting an upstream proposal

This applies **only in a published arrangement**. Where the instruction files are owned here, there is no upstream and a universal-sounding lesson is simply a lesson, recorded locally.

A universal lesson is **drafted, never filed automatically.** The law reaches every repository at once with no review on the receiving side, so a human decides what enters it.

Produce the proposal, show it to the user, and let them decide. Read `references/upstream.md` for what a proposal has to contain to be actionable.

## Every addition needs a subtraction, or a reason it does not

The instructions are read in full, in every session, forever. A loop with an append path and no retirement path makes them grow without bound, which makes agents worse at finding the rule that applies.

So when you add a lesson, name either the line it replaces or why it earns a permanent seat. "It seemed useful" is not a reason.

Retire on sight: anything now false, anything the tooling started enforcing (a gate replaces a rule), anything that was only ever true of a situation that no longer exists.

## Additional resources

Each is loaded only when its condition applies. Read the one that matches.

- `references/evidence.md` - read this **before grading any lesson**, and always when it came from a search summary or from memory rather than from something that ran.
- `references/routing.md` - read this **when the local-or-universal call is not obvious**, before creating any new file to hold a lesson, or when you cannot tell who owns the instruction files.
- `references/upstream.md` - read this **when drafting a proposal in a published arrangement**, for the shape that makes one actionable.
- `assets/lesson-template.md` - copy this **when writing a local entry**, rather than inventing a format the repository does not use.
