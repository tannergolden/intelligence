# Writing The Instructions

## Degrees of freedom

Match how prescriptive you are to how fragile the task is. This is the single decision that determines whether a body reads as helpful or as noise.

| Freedom | Use when | Shape |
| :--- | :--- | :--- |
| **High** | several approaches are valid and the task tolerates variation | prose, with the reasoning stated |
| **Medium** | a preferred pattern exists but variation is acceptable | a concrete procedure or pseudocode |
| **Low** | the operation is fragile, consistency matters, or a sequence must be followed exactly | a bundled script |

The mistake in both directions is common. Prescribing an exact sequence for a task with five valid solutions makes the agent worse at it. Writing loose prose for a fragile operation produces a different result every run.

**Where the task is genuinely flexible, explaining why beats commanding.** An agent that understands the reason applies it to the case you did not anticipate; an agent following a rule it cannot see the point of abandons it the moment the situation differs.

**Where the task is genuinely fragile, be exact and say so.** A strict requirement stated plainly is not the same as a rigid style applied everywhere.

## Four patterns that work

**Gotchas.** A short list of the concrete corrections an agent will need without being told: the environment-specific fact, the API that returns 200 on failure, the flag that means the opposite of what it reads. Keep these in the body rather than a reference, because they must be read *before* the situation arrives, not after.

**Templates for output.** When the shape of the result matters, give the shape. Agents pattern-match against a concrete structure far more reliably than they follow a prose description of one. Short templates inline; long ones in `assets/`.

**Checklists for dependent steps.** Where steps have real dependencies and skipping one silently corrupts the result, a checklist keeps the agent tracking its own progress.

**Validation loops.** Tell the agent to check its own work before moving on. For batch operations, the strongest form is plan, validate, then execute: produce an intermediate structured list, check it against a source of truth, and only then act on it.

## Anti-patterns

**Vague instruction.** "Handle errors appropriately." "Follow best practices." These consume tier B space in every session and change no behavior, because they carry no information the agent did not already have.

**Overly comprehensive.** A skill that documents everything makes the agent worse at finding the part that applies. Completeness is not the goal; retrievability is.

**Options without a default.** Three approaches presented as equals makes the agent choose arbitrarily and differently each run. Pick one, justify it in a clause, mention the others briefly.

**Instructions that do not apply.** Anything in the body applies to every invocation, so a step that is only sometimes relevant gets followed when it should not be. Move it behind a condition, or into a reference the body only sends the agent to when that condition holds.

**Generic knowledge.** Explaining what a PDF is, how HTTP works, what a migration does. The agent knows, and every line costs the whole session.

**Absolute or platform-specific paths.** Backslash paths and machine-specific locations break for everyone who is not you. Reference bundled files relative to the skill directory.

**Time-sensitive facts.** Version numbers, dates, and "currently" are wrong later, and nothing reports it.

## Naming references by their condition

A resource listed by subject alone gets read always or never. Give the condition instead:

```markdown
- `references/api-errors.md` - read this if the API returns a non-200 status.
```

That is the whole difference between a reference file that costs nothing until needed and one that is either dead weight or dead text.
