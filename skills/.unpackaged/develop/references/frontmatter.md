# Frontmatter Reference

Frontmatter sits between `---` fences at the very top of `SKILL.md`. That is the one place in this ecosystem where fenced frontmatter is correct rather than forbidden, because the Agent Skills specification requires it.

## Required, and there are only two

| Field         | Rule                                                                                          |
| :------------ | :--------------------------------------------------------------------------------------------- |
| `name`        | 1 to 64 characters, matching `^[a-z0-9]+(-[a-z0-9]+)*$`, identical to the directory name       |
| `description` | 1 to 1024 characters, saying what the skill does **and** when to use it                        |

The name pattern forbids a leading hyphen, a trailing hyphen and consecutive hyphens all at once. Checking those separately is how one of them ends up missing.

## Optional and portable

`license`, `compatibility` (at most 500 characters), and `metadata`, which is a free-form mapping no runtime reads. Use `metadata` for anything you want recorded but nothing needs to act on.

## Banned

`allowed-tools`. The specification marks it experimental, and it grants tool access without a per-use prompt on a machine that is not yours. A published skill does not hand itself permissions.

## Read by one tool only

`when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`.

Every one of these is silently ignored by tools that do not implement it. Using one means the skill behaves differently depending on who loaded it, so a skill that uses any must declare that with `compatibility`.

The harmless case is an optimisation that quietly does nothing. **The dangerous case is a skill whose correctness depends on the field.** A skill relying on `disable-model-invocation` to avoid firing automatically will fire automatically everywhere that field is unknown.

## Why the description limits are what they are

**1024 characters is the hard cap.** Past it the skill is invalid.

**Aim far below it.** The listing that holds every skill's name and description has a budget of roughly one percent of the context window. When it overflows, descriptions are dropped starting with the least-used skills, so one verbose description silences another skill entirely.

**Put the key use case first.** Where a listing entry is shortened, the end is what goes.

**Write it for a person as well as a model.** At least one supported tool shows the description in a consent prompt asking a user to grant access to the whole skill directory. Keyword soup reads well to a matcher and badly to a human, and a consent prompt nobody reads has already stopped being a control. Plain, specific prose that happens to contain the natural words satisfies both readers.

## A worked description

Weak, because it says what it is and never when to use it:

```text
description: Helps with skills.
```

Better, because a request can be matched against it and a human can decide whether to approve it:

```text
description: Creates and improves Agent Skills. Use when asked to write a skill,
  fix one that never triggers, review a SKILL.md, or split an oversized skill
  into reference files.
```
