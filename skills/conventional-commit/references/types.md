# Commit Types

Twelve types. Pick the one describing what the change *is*, not the area it
touched: a fix to a workflow file is `fix`, not `ci`, if it repairs broken
behaviour.

| Type       | For                                                                     |
| :--------- | :---------------------------------------------------------------------- |
| `feat`     | A capability that did not exist before.                                 |
| `fix`      | Behaviour that was wrong and now is not.                                |
| `docs`     | Documentation only. No behaviour change anywhere.                       |
| `style`    | Formatting, whitespace, quotes. No behaviour change and no logic moved. |
| `refactor` | Restructuring that leaves behaviour identical.                          |
| `perf`     | A change whose point is that it is faster.                              |
| `test`     | Tests and fixtures only.                                                |
| `build`    | Build system, packaging, dependency versions.                           |
| `ci`       | Pipeline configuration, as configuration rather than as a bug.          |
| `chore`    | Housekeeping with no product effect and no better home.                 |
| `security` | A change whose point is to close an exposure.                           |
| `revert`   | Undoing an earlier commit. Name it in the body.                         |

## The distinctions people get wrong

**`fix` against `refactor`.** If behaviour changed, it is `fix`. If it did not,
it is `refactor`. "Cleaner and also correct now" is two commits.

**`ci` against `fix`.** Editing a pipeline because you want it to do something
different is `ci`. Editing it because it was doing the wrong thing is `fix`.

**`chore` against everything.** `chore` is the type people reach for when they
have not decided what the change is. Try the other eleven first.

**`style` against `refactor`.** `style` moves no code. If a function moved, it
is `refactor`, however small.

**`security` against `fix`.** Both repair something. Use `security` when the
thing repaired was an exposure, so it lands in the security section of the
release notes rather than among ordinary bugs.
