---
name: conventional-commit
description: Writes a Conventional Commit message for staged changes. Use when asked to commit, to write or fix a commit message, or when a commit was rejected for its format.
---

## What to do

1. Read the staged changes before writing anything. A message describing work
   you did not look at is a guess.
2. Choose one type from `references/types.md`. If two apply, the change is
   probably two commits.
3. Write the header as `type(scope): subject`. The scope names the area
   changed, lower case, no spaces.
4. Keep the subject imperative, lower case, with no trailing period, and the
   whole header at 100 characters or fewer.
5. Add a body when the change needs a reason rather than a description. Wrap
   body lines at 78 characters. Say why, not what: the diff already says what.
6. Mark a breaking change with `!` after the scope, and explain the break in
   the body.

## Rules that reject a message

- No em dash, en dash, or curly quotes anywhere in the message.
- No trailing period on the subject.
- A scope is required. Without one the log reads `docs: update the docs` a
  hundred times and answers "where?" nowhere.

## Before you commit

State the message you intend to use and what it covers, then commit. If the
staged changes span two unrelated concerns, say so and propose splitting them
rather than writing one message that covers both loosely.

## Additional resources

- `references/types.md` - the twelve types, what each one is for, and the
  distinctions people get wrong. Read it when choosing between two types that
  both seem to fit.
