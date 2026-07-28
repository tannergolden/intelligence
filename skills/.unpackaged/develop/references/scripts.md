# Bundling A Script

## The signal that you need one

**The agent rebuilds the same logic every run.** Read the transcripts from a few real invocations. If the agent independently wrote a similar helper each time, or took the same fiddly multi-step route to the same place, that work belongs in a tested script bundled once.

The gain is not only reliability. A script lets the agent spend its turns on composition rather than reconstruction: it stops re-deriving the mechanism and starts using it.

The second signal is fragility. When a command is complex enough to be hard to get right on the first try, a tested script is more reliable than instructions describing the command.

## Interface rules

These are not style preferences. Each one prevents a specific failure in an agent environment.

**Never prompt for input.** A script that blocks waiting for a human hangs indefinitely, because there is no human. Take everything through command-line flags, environment variables, or stdin.

**Write real `--help` output.** That is the primary way an agent learns the interface. Include a one-line description, the flags, and at least one usage example.

**Make errors actionable.** "Error: invalid input" costs a turn and teaches nothing. Say what went wrong, what was expected, and what to try instead.

**Separate data from diagnostics.** Structured results to stdout, progress and warnings to stderr. An agent parsing stdout should never have to filter your progress messages out of it.

**Prefer structured output.** JSON, CSV or TSV over free-form prose, so the result can be consumed without guessing at its shape.

**Guard destructive operations.** Anything that deletes or overwrites should require an explicit `--force` or `--confirm`, proportionate to what it can destroy.

## Invocation

Call scripts by a path relative to the skill directory root, never by an absolute path and never by a location that assumes where the skill was installed.

**List every script in `SKILL.md`.** An agent does not go looking; a script nobody mentions is a script nobody runs. Give the invocation and the condition under which to use it.

## Do not store data in the skill directory

The skill directory is replaced on upgrade, so anything written there is lost without warning. Write to a path the caller provides, or to the location the host tool designates for persistent state.

## The cost side

A bundled script is executable content travelling with a document. Wherever a skill is installed, that script arrives too, and whoever installs it is trusting it. Bundle one when it earns its place, keep it small enough to read, and prefer the standard library so it runs without an install step.
