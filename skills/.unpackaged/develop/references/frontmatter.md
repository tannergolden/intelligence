# Frontmatter Reference

Frontmatter sits between `---` fences at the very top of `SKILL.md`. That is the one place in this ecosystem where fenced frontmatter is correct rather than forbidden, because the Agent Skills specification requires it.

For how to *write* the description, which is a craft question rather than a field question, see `descriptions.md`.

## Required, and there are only two

| Field         | Rule                                                                                    |
| :------------ | :--------------------------------------------------------------------------------------- |
| `name`        | 1 to 64 characters, matching `^[a-z0-9]+(-[a-z0-9]+)*$`, identical to the directory name |
| `description` | 1 to 1024 characters, saying what the skill does **and** when to use it                  |

The name pattern forbids a leading hyphen, a trailing hyphen and consecutive hyphens all at once. Checking those separately is how one of them ends up missing.

## Optional and portable

`license`, which is either an SPDX identifier or the name of a file the skill bundles; `compatibility`, at most 500 characters; and `metadata`, a mapping of string keys to string values with no keys the specification requires. Use `metadata` for anything worth recording that nothing needs to act on.

A file named by `license` counts as referenced even though the body never mentions it. The frontmatter is what points at it.

## Banned

`allowed-tools`. The specification marks it experimental, and it grants tool access without a per-use prompt on a machine that is not yours. A published skill does not hand itself permissions.

## Read by one tool only

`when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`.

Every one of these is silently ignored by tools that do not implement it, so a skill using any of them behaves differently depending on who loaded it. Declare that with `compatibility`.

The harmless case is an optimization that quietly does nothing. **The dangerous case is a skill whose correctness depends on the field.** One relying on `disable-model-invocation` to avoid firing automatically will fire automatically everywhere that field is unknown.

## What shapes are allowed

Scalars, block scalars, and a mapping under `metadata`. A description long enough to wrap is normally written as a block scalar, and that is ordinary YAML:

```yaml
description: >
  Use this skill when the user is doing the thing, or when they describe
  the symptom without naming the thing.
metadata:
  author: your name
```

Anything else nested is refused rather than half-read, because a parser that quietly drops what it cannot understand would pass a skill whose real frontmatter says something else. A key written twice is refused too: every YAML reader keeps the last one silently, so the value a reviewer read in the diff is not the value that loads.
