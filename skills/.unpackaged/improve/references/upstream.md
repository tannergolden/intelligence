# Proposing A Change To The Shared Law

A universal lesson is beyond one repository's authority, so it goes to
whoever owns the instructions. It never goes into the local copy of them:
see `routing.md` for why that copy is not a destination.

Where no publisher exists, a drafted proposal simply goes unused, which
costs a paragraph. That is the whole risk of guessing wrong here, and it is
why this step is allowed to guess at all.

## Draft it, do not file it

**Produce the proposal and show it to the user.** Do not open an issue, a pull request or a discussion on another repository on your own initiative.

Where the publisher offers a proposal form, fill its fields rather than
inventing a shape: the sections below are the ones such a form asks for, so a
draft written this way pastes in without being reshaped. Filing it is still
the user's action.

The reason is not caution for its own sake. A change accepted upstream reaches every repository pinned to the moving major tag on its next sync, with no pull request and no review on the receiving side. That is a production change to every consumer at once, triggered by a lesson learned in one of them. A human decides that.

## What makes a proposal actionable

A maintainer needs to judge it without the session it came from. Four things, and a proposal missing any of them will sit unread.

1. **The rule, in one sentence**, written as an instruction rather than a story.
2. **The evidence and its grade**, per `evidence.md`. An ungraded proposal is a request to take your word for it.
3. **Why it is universal**, answering the routing test explicitly: what makes it true regardless of language, toolchain and branch model.
4. **What it costs**, because the law is read in full in every session in every repository. Name the line it replaces, or argue for the seat.

## The shape

```markdown
## Proposed rule

<One sentence, imperative, no story.>

## Evidence

**Grade:** probed | documented | unverified
<What ran and what it returned, or the primary source and the date read.>

## Why it is universal

<Why it holds in a repository with a different language, toolchain, branch
model and review policy. If it does not, it is local and belongs elsewhere.>

## Cost

<The line it replaces, or the argument for adding one. "It seemed useful"
is not an argument.>
```

## What gets rejected upstream, so check first

- **Anything a tool could enforce instead.** A gate beats a rule: it fires every time, it cannot be skimmed past, and it costs no context. If the lesson could be a check, propose the check.
- **Anything that varies by repository.** It failed the routing test and belongs local.
- **Anything restating what the model already knows.** Generic engineering advice consumes context in every session and changes no behavior.
- **Anything time-sensitive.** A version number or a current vendor behavior is wrong later, and the law has no expiry mechanism.

## When the same local lesson appears in several repositories

That is the strongest possible case for promotion, and it is worth saying so explicitly in the proposal. A rule independently discovered in three unrelated repositories has already passed the universality test by experiment rather than by argument.
