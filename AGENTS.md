<!--
title: '🤖 AGENT INSTRUCTIONS'
description: 'The canonical instruction file every AI agent reads before doing anything here, written to hold true in any repository whatever its language or purpose.'
tags: [agent-instructions, engineering-law, conventions, universal]
category: agents
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 AGENT INSTRUCTIONS

<a name="top"></a>

**One set of rules for every AI agent, in every repository, whatever it is for.**

_One law. Every agent. Every repository._

</div>

---

## 💡 What This File Is

The canonical instruction file for every AI agent working in this repository. Whatever tool you arrived with, and whatever filename that tool discovered, the rules below are the ones that bind. Where any other file appears to conflict with this one, this one wins.

> [!IMPORTANT]
> **This file is published, not authored here.** It arrives from an upstream repository and is overwritten in full on the next sync, so a local edit is a change that will be silently reverted. The same is true of any router beside it. To change a rule for everyone, change it upstream. To change one for this repository only, write it in this repository's own context, which section 2 explains how to find.

Two properties follow from that, and both shape what may be written above this line.

It is **tool-agnostic**. A rule that only half the agents can follow is not a rule, so nothing here rests on a mechanism a single vendor ships. Tool-specific files exist only to point at this one and carry no law of their own.

It is **repository-agnostic**. This exact text sits in repositories with different languages, different toolchains, different branch models and different review policies, so it can only contain what is true across all of them. Anything that varies is delegated rather than asserted.

---

## 📝 Two Layers of Law

1. **This file: what holds everywhere.** Encoding, secret handling, how to approach a change, how to report one. None of it depends on what the repository is for.
2. **The repository's own context: everything that varies.** Architecture, stack decisions, domain rules, runbooks, branch model, review policy. No two repositories organise this the same way. Some use a `docs/` tree. Some place a set of instructions in each folder, beside the files those instructions govern. Some keep a knowledge base under a name this file has never heard of. NEVER assume a layout. Find the one actually in front of you.

> [!IMPORTANT]
> **Where this repository documents a convention that differs from any rule below, the repository wins and this file yields.** Say so in your report when it happens. A rule that cannot be overridden locally is a rule that will be wrong somewhere, and this text is identical in repositories that have nothing else in common.

Some repositories additionally follow a shared external standard by link, never by copy, because a copied standard is one that goes stale. Where a repository declares one, it outranks this file on engineering process, and this file's job is only to state the handful of rules an agent gets wrong without being told.

### 💡 Finding the Local Context

Look in this order, and stop at the first that answers the question you have:

1. **What the root `README.md` says.** A repository that organises its knowledge deliberately almost always says where, in the first screen.
2. **The folder you are about to change.** An instruction file, a README, or a rules file sitting beside the code governs that code and outranks anything further away.
3. **A repository-wide knowledge directory, under whatever name it carries.** A `docs/` tree, a notes folder, a vault, a wiki committed to the repository.

> [!IMPORTANT]
> **Nothing loads these for you, and you must not wait to be handed them.** Folder-level instructions are not a mechanism every agent tool supports: some read only from the repository root, some inject a path rather than the content, and some drop nested files partway through a long session. Treat each one as a file you are required to open and read yourself before touching what it governs. An instruction you did not read is an instruction you broke.

Read the document that governs a thing before changing the thing, and name the document you followed in your report so the reader can check the source.

---

## 🛡️ The Binding Rules

Eight rules. Rules 1, 2, 7 and 8 hold in any repository. Rules 4 and 5 apply wherever the thing they govern exists. Rules 3 and 6 tell you to go and find the answer, because asserting one here would be wrong somewhere.

1. **Commit messages are Conventional Commits.** `type(scope): subject`, imperative mood, lower-case subject, no trailing period. Types in use: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `security`, `revert`.
2. **The em dash (U+2014) is banned in everything you write**: prose, code, comments, configuration, commit messages, issue text and release notes alike. Use a comma, a colon, parentheses, or a spaced hyphen (" - "). En dashes (U+2013) and curly quotes are banned on the same terms. Verbatim third-party text is exempt: license files, vendored assets, lockfiles.
3. **Find out how work lands here before you land any.** NEVER assume a trunk name, and NEVER assume whether a pull request is required, optional or forbidden. Some repositories take direct pushes to their default branch and open no pull requests at all; others require one for every change. Read this repository's own context first, then its contributing guide if it has one, then how recent commits actually arrived on the default branch. Guessing wrong fails loudly, and it fails after the work is done.
4. **Every third-party CI action or job template is pinned to an immutable revision**, a full 40-character commit SHA on GitHub Actions, with its human-readable version as a trailing comment on the same line. NEVER pin to a tag or a branch, and NEVER write a revision you have not read from a real source. A guessed SHA is a broken pipeline at best.
5. **Every CI job holds the narrowest permissions it can do its work with.** On GitHub Actions that means `permissions: {}` at the top of the workflow, with each job granting itself only what it uses. A workflow-level block is a ceiling, not a grant: a job cannot hold a permission the workflow did not allow, and it does not receive one just because the workflow listed it.
6. **Documentation matches what this repository already does.** Where it publishes or links a styling specification, read that before writing any Markdown, because it is the rule broken most often and the one a reader notices first. Where it does not, match the files already there rather than importing a house style from elsewhere. Two things hold either way: every code fence declares a language, and shell blocks carry no leading prompt character.
7. **Files are UTF-8 with no byte order mark and end with exactly one trailing newline.**
8. **Secrets never enter the tree.** No key, token or credential in a file, a fixture, a comment, a test or a commit message, not even an expired one. Read them from the environment or from a secret store.

---

## ⚙️ Commands: Read Them, Do Not Guess Them

Repositories do not share one toolchain. Before running a build, a test or a lint, read what this repository actually defines: its `Makefile`, its `package.json` scripts, its `pyproject.toml`, its `Cargo.toml`, its CI configuration, whatever it happens to use. A command that appears in none of those does not exist here. Inventing one burns a turn and teaches the reader to distrust the next claim you make.

The same discipline applies to what a CI job may assume is installed. A hosted runner provides a documented base image and nothing else; anything beyond it arrives only because a step installs it. So a script that reaches for a third-party package is adding a dependency, and that is a decision to state rather than a convenience to take.

---

## 📦 What Never to Edit by Hand

| Path                                     | Why                                                                       |
| :--------------------------------------- | :------------------------------------------------------------------------ |
| This file, and any router beside it      | Published from upstream. Overwritten in full on the next sync.            |
| Any file carrying a do-not-edit header   | It says so on its first line. Change the source and republish.            |
| Content between generated-region markers | Regenerated from the tree. Edit the prose around the markers instead.     |
| Lockfiles and vendored third-party files | Regenerated, or verbatim upstream. A hand edit is undone on the next run. |
| Machine-written receipts and state files | They record what happened. Editing one rewrites history, not behaviour.   |

If you believe one of these is wrong, fix what generates it and say so. Editing the output hides the defect and reintroduces it on the next run.

---

## 🚀 How to Make a Change

1. **Scope first.** Name the files and the lines the task touches, and what stays untouched, then work only there. A narrow scope beats a wide crawl, and reading the ranges a decision needs beats reading whole files by reflex.
2. **Plan before anything non-trivial.** A multi-file change, a refactor, a pipeline change, or a new capability gets its plan stated and agreed before it gets built. A typo needs no plan.
3. **Simplest solution that fully works.** Reach for abstraction, tooling, or extra machinery only when the simple path demonstrably fails. Complexity is a cost every future reader pays.
4. **Reproduce, then fix the cause.** NEVER suppress, mask, or catch-and-ignore an error to make a check pass. A hidden failure is a deferred outage, and a fallback that swallows the real error is worse than the error it hid.
5. **Separate making from checking.** You rate your own work generously, so trust an independent signal: a test, a gate, a pass that never watched the code being written. "It should work" is a hypothesis; only what ran is a result.
6. **Least privilege, reversible first.** The narrowest scope, the fewest permissions, the most reversible action that does the job. Confirm before anything destructive.
7. **Documentation lands with the change.** A pipeline, a script, a configuration knob, or a convention is unfinished until the document explaining it lands in the same commit, wherever this repository keeps such documents.

---

## 🌿 After You Push

A push is a claim. Whatever can check it is the proof.

1. Where the push triggers automated checks, watch every run until none is queued or in progress, then confirm each one concluded green. ALWAYS finish that loop before reporting done, ending the turn, or starting unrelated work.
2. Red means fix forward. Pull the failing job's log, fix the cause, push, and watch the new runs the same way. Red inherited from an earlier commit is yours too: fix it, or name it out loud.
3. Sweep what the push produced: opened issues, code scanning, secret scanning and dependency alerts, pre-existing ones included. Resolve what you can and name the rest.
4. Report the commit, what concluded green, and anything you surfaced instead of fixing.

A repository with no automated checks does not make this optional, it makes it manual. Say plainly what you verified by hand and what nobody verified at all.

The only forbidden outcomes are silence and the unwatched push.

---

<div align="center">

**Written for every agent, owed by every agent, waived for none.**

[↑ Back to Top](#top)

</div>
