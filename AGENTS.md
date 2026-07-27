<!--
title: '🤖 AGENT INSTRUCTIONS'
description: 'The canonical instruction file every AI agent reads before doing anything in this repository, whichever tool it arrived with.'
tags: [agent-instructions, engineering-law, conventions, universal]
category: agents
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 AGENT INSTRUCTIONS

<a name="top"></a>

**One set of rules for every AI agent working here, written so that no rule depends on a feature only one vendor ships.**

_One law. Every agent. No exceptions per vendor._

</div>

---

## 💡 What This File Is

The canonical instruction file for every AI agent working in this repository. Whatever tool you arrived with, and whatever filename that tool discovered, the rules below are the ones that bind. Where any other file appears to conflict with this one, this one wins.

It is deliberately **tool-agnostic**. A rule that only half the agents can follow is not a rule, so nothing here rests on a mechanism a single vendor ships. Tool-specific files exist only to point at this one and carry no law of their own.

---

## 📝 Two Layers of Law

1. **The shared engineering standards.** Branching, commits, security, testing, dependencies and documentation style are defined once in [tannergolden/standards](https://github.com/tannergolden/standards) and followed **by link, never by copy**. A copied standard is a standard that goes stale. This file states the handful of rules an agent gets wrong without being told, and leaves the long form upstream.
2. **This repository's own `docs/`.** Architecture, stack decisions, domain rules and runbooks live locally. On engineering process the shared standards win. On this repository's own specifics the local docs win.

Read the document that governs a thing before changing the thing, and name the document you followed in your report so the reader can check the source.

---

## 🛡️ The Binding Rules

Eight rules. They bind every agent, every change, and every file you write.

1. **Commit messages are Conventional Commits.** `type(scope): subject`, imperative mood, lower-case subject, no trailing period. Types in use: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `security`, `revert`.
2. **The em dash (U+2014) is banned in everything you write**: prose, code, comments, configuration, commit messages, issue text and release notes alike. Use a comma, a colon, parentheses, or a spaced hyphen (" - "). En dashes (U+2013) and curly quotes are banned on the same terms. Verbatim third-party text is exempt: license files, vendored assets, lockfiles.
3. **Work lands by direct push to `Development`.** `Development` is trunk and the default branch, not a stage in a promotion ladder. NEVER open a pull request to deliver a change. The only exceptions exist because the automation token provably cannot write them: Dependabot's own bumps, and changes under `.github/workflows/`.
4. **Every third-party GitHub Action is pinned to a full 40-character commit SHA**, with its human-readable version as a trailing comment on the same line. NEVER pin a third-party action to a tag or a branch, and NEVER write a SHA you have not read from a real source. A guessed SHA is a broken workflow at best.
5. **Every workflow opens with `permissions: {}` at the top level**, and each job grants itself only the permissions it actually uses. A workflow-level block is a ceiling, not a grant: a job cannot hold a permission the workflow did not allow, and it does not receive one just because the workflow listed it.
6. **Documentation follows the shared styling specification.** The parts that get missed: frontmatter is wrapped in an HTML comment so it stays hidden, never a `---` fence, because a fence renders as a block of metadata at the top of the page on GitHub; it carries exactly four kebab-case `tags`; filenames under `docs/` are Capitalized-Kebab with `&` as the conjunction and no underscores; every code fence declares a language; shell blocks carry no leading prompt character.
7. **Files are UTF-8 with no byte order mark and end with exactly one trailing newline.**
8. **Secrets never enter the tree.** No key, token or credential in a file, a fixture, a comment, a test or a commit message, not even an expired one. Read them from the environment or from repository secrets.

---

## ⚙️ Commands: Read Them, Do Not Guess Them

Repositories do not share one toolchain. Before running a build, a test or a lint, read what this repository actually defines: its `Makefile`, its `package.json` scripts, its `pyproject.toml`, and the workflows under `.github/workflows/`. A command that appears in none of those does not exist here. Inventing one burns a turn and teaches the reader to distrust the next claim you make.

The same discipline applies to what a job may assume is installed. GitHub's runners provide a standard-library Python 3, POSIX `sh`, `jq` and `gh`. Anything else arrives only because a step installs it, so a script that reaches for a third-party package is adding a dependency, and that is a decision to state rather than a convenience to take.

---

## 📦 What Never to Edit by Hand

| Path                                      | Why                                                                       |
| :---------------------------------------- | :------------------------------------------------------------------------ |
| Any file carrying a do-not-edit header    | It says so on its first line. Change the source and republish.            |
| Content between `AUTO-INDEX` markers      | Regenerated from the tree. Edit the prose around the markers instead.     |
| Lockfiles and vendored third-party files  | Regenerated, or verbatim upstream. A hand edit is undone on the next run. |
| Machine-written receipts and state files  | They record what happened. Editing one rewrites history, not behaviour.   |

If you believe one of these is wrong, fix what generates it and say so. Editing the output hides the defect and reintroduces it on the next run.

---

## 🚀 How to Make a Change

1. **Scope first.** Name the files and the lines the task touches, and what stays untouched, then work only there. A narrow scope beats a wide crawl, and reading the ranges a decision needs beats reading whole files by reflex.
2. **Plan before anything non-trivial.** A multi-file change, a refactor, a workflow change, or a new capability gets its plan stated and agreed before it gets built. A typo needs no plan.
3. **Simplest solution that fully works.** Reach for abstraction, tooling, or extra machinery only when the simple path demonstrably fails. Complexity is a cost every future reader pays.
4. **Reproduce, then fix the cause.** NEVER suppress, mask, or catch-and-ignore an error to make a check pass. A hidden failure is a deferred outage, and a fallback that swallows the real error is worse than the error it hid.
5. **Separate making from checking.** You rate your own work generously, so trust an independent signal: a test, a gate, a pass that never watched the code being written. "It should work" is a hypothesis; only what ran is a result.
6. **Least privilege, reversible first.** The narrowest scope, the fewest permissions, the most reversible action that does the job. Confirm before anything destructive.
7. **Documentation lands with the change.** A workflow, a script, a configuration knob, or a convention is unfinished until the document explaining it lands in the same commit, and the root `README.md` names every major feature with a link to the page that explains it.

---

## 🌿 After You Push

A push is a claim. The checks are the proof.

1. Watch every run the push triggered until none is queued or in progress, then confirm each one concluded green. ALWAYS finish this loop before reporting done, ending the turn, or starting unrelated work.
2. Red means fix forward. Pull the failing job's log, fix the cause, push, and watch the new runs the same way. Red inherited from an earlier commit is yours too: fix it, or name it out loud.
3. Sweep what the runs produced: opened issues, code scanning, secret scanning and dependency alerts, pre-existing ones included. Resolve what you can and name the rest.
4. Report the commit, the checks that concluded green, and anything you surfaced instead of fixing.

The only forbidden outcomes are silence and the unwatched push.

---

## 🔗 See also

> [!TIP]
> The long form of every rule above lives in [tannergolden/standards](https://github.com/tannergolden/standards). Read its documentation styling specification before writing any Markdown here, because that is the rule broken most often and the one a reader notices first.

---

<div align="center">

`scope: every agent, every session` &middot; `authority: highest in this repository`

**Written for every agent, owed by every agent, waived for none.**

[↑ Back to Top](#top)

</div>
