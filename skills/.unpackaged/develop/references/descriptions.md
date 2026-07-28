# Writing The Description

The description is the highest-leverage text in a skill and the one most often written backwards. It is loaded for every skill in every session whether that skill is used or not, and it is the only thing an agent consults when deciding what to invoke.

## The pattern

**Frame it as an instruction to the agent, not as a label for the skill.**

Weak, because it says what the skill is:

```text
description: Processes CSV files.
```

Strong, because it says when to reach for it:

```text
description: Analyze CSV and tabular data files: compute summary statistics, add derived columns, generate charts, and clean messy data. Use this skill when the user has a CSV, TSV, or Excel file and wants to explore, transform, or visualize the data, even if they never say "CSV" or "analysis".
```

Three things changed. It names the capabilities rather than the mechanism. It broadens across the formats a user might actually have. And it covers the case where the user never uses the domain word at all, which is the case a narrow description misses.

**On one line, however long it gets.** Frontmatter here is flat `key: value` pairs, so a description wrapped onto a second line reads as nested and is rejected rather than folded.

## Third person about the user, imperative toward the agent

Write **"Use this skill when the user wants X"**, not "use me when you want X" and not "this skill provides X". The subject is the user's situation; the instruction is aimed at the agent choosing.

## Be pushier than feels natural

Agents measurably **under-trigger**. A description that reads as appropriately modest to a human is one the agent skips. Explicitly list the contexts where the skill applies, including the ones where the user describes a symptom rather than naming the domain.

The failure this prevents is silent: a skill that never fires produces no error, no log line, and no clue that it existed.

## Say what it is not for

Any skill worth writing has one neighbouring task it will wrongly claim. Naming that boundary in the description costs a clause and prevents the failure that is hardest to notice, which is a skill quietly loading in every adjacent session and crowding out the ones that should have fired.

## Length

The hard limit is 1024 characters. A few sentences to a short paragraph is the working range.

Stay well under the limit anyway. The listing that holds every skill's name and description has a budget of roughly one percent of the context window, and when it overflows, entries are shortened starting with the least-used skills. A long description does not only cost its own space; it evicts another skill's description entirely.

Where an entry is shortened, the **end** is what goes, so the key use case belongs in the first clause.

## What to leave out

**Internal mechanics.** How the skill works is the body's job, and an agent choosing between skills cannot act on it.

**Narrow keyword matching.** A description tuned to one exact phrasing fires on that phrasing and nothing else. Describe the intent and the keywords follow.

**Anything time-sensitive.** Version numbers and dates in a description are wrong later and nothing will tell you.

## A quick test

Read the description alone, with the body hidden, and write down the request you would expect to summon it. If you cannot produce one, or the one you produce is narrower than what the skill actually handles, the description is the defect, whatever the body says.
