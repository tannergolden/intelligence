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

Physically nothing stops it: an installed skill is an ordinary folder, and an agent holding write access can put a file in it. Three things go wrong anyway, and the first is the one people miss.

**A skill can be installed for the user, not the project.** Claude Code resolves skills at user scope as well as project scope, so one copy of a skill can serve every repository that person works in. Data written inside it is then read in all of them: notes from one project surface in another, and anything project-specific is now wrong everywhere else.

**The directory is replaced on upgrade.** Installing a newer version copies the folder over the old one, and whatever was written inside goes with it, silently.

**An unreferenced file is a defect.** A skill directory is content the manifest names; a checker that enforces that will reject the file, and Gemini CLI puts the folder structure in context and asks the user to approve access to the whole directory, so stored data costs context and widens the grant.

Write to a path the caller provides, or to the location the host tool designates for persistent state.

## The cost side

A bundled script is executable content travelling with a document. Wherever a skill is installed, that script arrives too, and whoever installs it is trusting it. Bundle one when it earns its place, keep it small enough to read, and prefer the standard library so it runs without an install step.
