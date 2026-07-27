<!--
title: 'AGENTS.md - Canonical Agent Instructions'
description: 'The canonical instruction file every AI agent loads and follows in this repository.'
tags: [agent-instructions, engineering-law, conventions, sync-owned]
category: agents
-->

# DO NOT EDIT - Published by tannergolden/ai

This file is copied into this repository by an automated sync from
[tannergolden/ai](https://github.com/tannergolden/ai). Local edits to it are reverted on the next
sync, silently, with no pull request and no warning. To change the law, change it there and cut a
release; every repository in the fleet receives it. To add law that is true of **this** repository
only, edit `.ai/local/agents-local.md`, which the sync injects into the last section below and
never overwrites.

---

## 1. What This File Is

The canonical instruction file for every AI agent working in this repository. `CLAUDE.md` and
`GEMINI.md` are one-line routers that import it and carry no law of their own. Where any other file
appears to conflict with this one, this one wins.

Two agent tools are supported here, meaning tested and budgeted: **Claude Code** and **Gemini CLI**.
Anything else that happens to read `AGENTS.md` receives the same law as a side effect, which is
welcome but is not a promise.

---

## 2. Two Layers of Law

1. **The shared engineering standards.** Branching, commits, security, testing, dependencies and
   documentation style are defined once in
   [tannergolden/standards](https://github.com/tannergolden/standards) and followed **by link, never
   by copy**. A copied standard is a standard that goes stale. That is why this file states the
   handful of rules an agent gets wrong without being told, and leaves the long form upstream.
2. **This repository's own `docs/`.** Architecture, stack decisions, domain rules and runbooks live
   locally, under `docs/`; if there is a `docs/Documentation.md`, start there. On engineering
   process the shared standards win. On this repository's own specifics the local docs win.

Read the document that governs a thing before changing the thing. When you follow one, name it in
your report so the user can check the source.

---

## 3. The Binding Rules

These bind every repository in this fleet, every agent, and every file you write.

1. **Commit messages are Conventional Commits.** `type(scope): subject`, imperative mood, lower-case
   subject, no trailing period. Types in use: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`,
   `test`, `build`, `ci`, `chore`, `security`, `revert`.
2. **The em dash (U+2014) is banned in everything you write**: prose, code, comments, configuration,
   commit messages, issue text, release notes. Use a comma, a colon, parentheses, or a spaced hyphen
   (" - "). En dashes (U+2013) and curly quotes are banned on the same terms. Verbatim third-party
   text is exempt: license files, vendored assets, lockfiles.
3. **Work lands by direct push to `Development`.** `Development` is trunk and the default branch, not
   a stage in a promotion ladder. NEVER open a pull request to deliver a change. Two narrow
   exceptions exist only because the automation token provably cannot write them: Dependabot's own
   bumps, and changes under `.github/workflows/`.
4. **Every third-party GitHub Action is pinned to a full 40-character commit SHA**, with its
   human-readable version as a trailing comment on the same line. NEVER pin a third-party action to a
   tag or a branch, and NEVER write a SHA you have not read from a real source. A guessed SHA is a
   broken workflow at best.
5. **Every workflow opens with `permissions: {}` at the top level**, and each job grants itself only
   the permissions it actually uses. A workflow-level block is a ceiling, not a grant: a job cannot
   hold a permission the workflow did not allow, and it does not receive one just because the
   workflow listed it.
6. **Documentation follows the shared styling specification.** The parts that get missed: frontmatter
   is wrapped in an HTML comment so it stays hidden, never a `---` fence, because a fence renders as
   a block of metadata at the top of the page on GitHub; it carries exactly four kebab-case `tags`;
   filenames under `docs/` are Capitalized-Kebab with `&` as the conjunction and no underscores;
   every code fence declares a language; shell blocks carry no leading prompt character.
7. **Files are UTF-8 with no byte order mark and end with exactly one trailing newline.**
8. **Secrets never enter the tree.** No key, token, or credential in a file, a fixture, a comment, a
   test, or a commit message, not even an expired one. Read them from the environment or from
   repository secrets.

---

## 4. Commands: Read Them, Do Not Guess Them

Repositories in this fleet do not share one toolchain. Before running a build, a test, or a lint,
read what this repository actually defines: its `Makefile`, its `package.json` scripts, its
`pyproject.toml`, and the workflows under `.github/workflows/`. A command that appears in none of
those does not exist here. Inventing one burns a turn and teaches the user to distrust the next
claim you make.

The same discipline applies to what a CI job may assume is installed. GitHub's runners provide a
standard-library Python 3, POSIX `sh`, `jq`, and `gh`. Anything else arrives only because a step
installs it, so a script in `.github/` or `scripts/` that reaches for a third-party package is
adding a dependency, and that is a decision to state rather than a convenience to take.

---

## 5. What Never to Edit by Hand

| Path                                     | Why                                                                                       |
| :--------------------------------------- | :---------------------------------------------------------------------------------------- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`    | Published by tannergolden/ai. Overwritten on the next sync.                               |
| `.ai/`                                   | The same, except `.ai/local/` and `.ai/hooks/.disabled`, which belong to this repository. |
| `.ai/ai.lock.json`, `.ai/ai.lock.date`   | Machine-written receipts of the last sync.                                                |
| Content between `AUTO-INDEX` markers     | Regenerated from the tree. Edit the prose around the markers instead.                     |
| Lockfiles and vendored third-party files | Regenerated, or verbatim upstream.                                                        |

Two mechanical facts about the sync, because neither is discoverable by reading the tree:

- It pushes directly, with no pull request and no review step. It refuses to overwrite any file it
  has not written before, so a hand-written `AGENTS.md` is safe until a human adopts it on purpose.
- If this repository carries `.ai/hooks/`, those scripts run on every agent session. To switch them
  off, create an empty file at `.ai/hooks/.disabled`. The sync never creates or deletes that file,
  which makes it a kill switch that survives every release.

---

## 6. How to Make a Change

1. **Scope first.** Name the files and the lines the task touches, and what stays untouched, then
   work only there. A narrow scope beats a wide crawl, and reading the ranges a decision needs beats
   reading whole files by reflex.
2. **Plan before anything non-trivial.** A multi-file change, a refactor, a workflow change, or a new
   capability gets its plan stated to the user and agreed before it gets built. A typo needs no plan.
3. **Simplest solution that fully works.** Reach for abstraction, tooling, or extra machinery only
   when the simple path demonstrably fails. Complexity is a cost every future reader pays.
4. **Reproduce, then fix the cause.** NEVER suppress, mask, or catch-and-ignore an error to make a
   check pass. A hidden failure is a deferred outage, and a fallback that swallows the real error is
   worse than the error it hid.
5. **Separate making from checking.** You rate your own work generously, so trust an independent
   signal: a test, a gate, a pass that never watched the code being written. "It should work" is a
   hypothesis; only what ran is a result.
6. **Least privilege, reversible first.** The narrowest scope, the fewest permissions, the most
   reversible action that does the job. Confirm with the user before anything destructive.
7. **Documentation lands with the change.** A workflow, a script, a configuration knob, or a
   convention is unfinished until the document explaining it lands in the same commit, and the root
   `README.md` names every major feature with a link to the page that explains it.

---

## 7. After You Push

A push is a claim. The checks are the proof.

1. Watch every run the push triggered until none is queued or in progress, then confirm each one
   concluded green. ALWAYS finish this loop before reporting done, ending the turn, or starting
   unrelated work.
2. Red means fix forward. Pull the failing job's log, fix the cause, push, and watch the new runs the
   same way. Red inherited from an earlier commit is yours too: fix it, or name it out loud.
3. Sweep what the runs produced: opened issues, code scanning, secret scanning, and dependency
   alerts, pre-existing ones included. Resolve what you can and name the rest.
4. Report the commit, the checks that concluded green, and anything you surfaced instead of fixing.

The only forbidden outcomes are silence and the unwatched push.

---

## 8. Local Law

Everything between the markers below is written by this repository, in `.ai/local/agents-local.md`,
and injected here by the sync. It extends this file: on this repository's own specifics it is
authoritative, and where it appears to contradict a rule above, the rule above holds and the
contradiction is a defect worth reporting.

<!-- ai:local:begin -->
<!-- ai:local:end -->
