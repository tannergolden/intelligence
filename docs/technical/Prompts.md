<!--
title: '💬 PROMPTS'
description: 'The ready-made prompts every repository gets in docs/Prompts.md: the universal ones the hub keeps current between their markers, most ready to run as they are, the section each repository fills with its own, and how to change either.'
type: guide
keywords: [prompts, repository-sync, prompt-engineering]
-->

<div align="center">

# 💬 PROMPTS

<a name="top"></a>

**Ready-made prompts in every repository, so nobody has to write a good one from scratch.**

_Find one. Copy it. Paste it._

</div>

---

## 💡 What A Repository Gets

A prompt typed in a hurry leaves out what an agent needs: the goal, the
context it cannot see, the limits, and how to tell when it is done. So every
repository that takes part in [sync](Repository-Sync.md) gets
`docs/Prompts.md`, a page of prompts anyone can copy into any AI app, the
owner and every collaborator alike. Each prompt sits in its own fenced block,
so GitHub shows a copy button on it.

Most of the universal prompts run as they are: the agent finds what changes
from one repository to the next, such as its commands, its default branch or
its last release, in the repository itself. The few that need what only a
person knows, such as the bug they saw, mark it with a placeholder in double
braces, such as `{{ERROR_OUTPUT}}`, and name it in a **Fill in** line.

The file has two parts, split the way `AGENTS.md` is:

| Part                                             | Whose                     | What it holds                                                                                                                |
| :----------------------------------------------- | :------------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| Between the `INTELLIGENCE:PROMPTS` markers       | The hub's, kept current   | How to use a prompt; an index of every prompt; the universal prompts, grouped by the kind of work they do; and the practices |
| "Prompts For This Repository", after the markers | The repository's, its own | The prompts its owner writes for the work that repository does                                                               |

The universal prompts cover the work any repository has, in 17 areas, from a
first look at the code to a release:

| Area                          | Prompts that run as they are                                                                                                                                                                                                    | Prompts to fill in                   |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------- |
| Get started                   | Tour This Repository, Set Up This Project, Make Setup Repeatable, Catch Me Up                                                                                                                                                   | Explain This Code                    |
| Plan and build                |                                                                                                                                                                                                                                 | Plan A Change, Add A Feature         |
| Debug and fix                 | Make Every Check Pass, Find The Commit That Broke It, Hunt For Bugs, Clear The Warnings                                                                                                                                         | Fix A Bug                            |
| Test                          | Fill The Test Gaps, Test My Changes, Test The Tests, Add A Smoke Test, Fix Flaky Tests, Speed Up The Tests                                                                                                                      |                                      |
| Keep the code healthy         | Find The Riskiest Code, Simplify The Most Complex Code, Remove Duplicated Code, Remove Dead Code, Tighten The Types, Triage The TODO Comments, Review The Whole Codebase                                                        |                                      |
| Review and ship               | Review This Branch, Commit My Work, Write The Pull Request, Address The Review Comments, Update This Branch, Split This Branch                                                                                                  | Review My Change                     |
| Look after the repository     | Check The Repository Setup, Add Issue And Pull Request Templates, Stop Tracking Generated Files, Find What Bloats The Repository, Triage The Open Issues, Sort The Open Pull Requests, Clean Up Old Branches, Find My Lost Work |                                      |
| Dependencies                  | Update The Dependencies, Fix Vulnerable Dependencies, Remove Unused Dependencies, Set Up Dependency Updates, Check Dependency Licenses                                                                                          |                                      |
| Security and privacy          | Find Security Holes, Find Security Holes In This Branch, Find Leaked Secrets, Map The Personal Data, Write A Threat Model, Generate A Software Bill Of Materials                                                                |                                      |
| Build and CI                  | Run Every Check In CI, Speed Up CI, Harden The CI Workflows                                                                                                                                                                     |                                      |
| Release                       | Prepare The Next Release, Write The Release Notes, Find Breaking Changes                                                                                                                                                        |                                      |
| Document                      | Refresh The README, Fix Stale Docs, Document The Public Interface, Write An Architecture Overview, Record Past Decisions, Write The Contributing Guide, Document The Configuration                                              |                                      |
| Performance and reliability   | Check Production Readiness, Speed Up The Slowest Path, Find Resource Leaks, Harden The External Calls, Find Swallowed Errors, Find Concurrency Bugs, Make It Observable                                                         |                                      |
| Data and APIs                 | Check The Migrations Are Safe, Check The API Contract, Check The API Design                                                                                                                                                     |                                      |
| User interface                | Fix Accessibility Problems, Prepare For Translation, Speed Up Page Load                                                                                                                                                         |                                      |
| Containers and infrastructure | Harden The Container Image, Review The Infrastructure Code, Find Cloud Savings, Write The Runbook                                                                                                                               |                                      |
| Work with agents              | Write The Agent Instructions, Set Up Cloud Agents, Continue Where I Left Off, Suggest What To Do Next, Check What The Agent Did, Write A Handoff Note                                                                           | Write A New Prompt, Improve A Prompt |

A prompt that runs as it is needs an agent that works in the repository, one
that can open its files and run its commands; a prompt to fill in also works in
an app that sees only what is pasted into it. A line added after a prompt, such
as "Only the billing module.", points it at part of the repository. Write A New
Prompt turns a rough request into a new prompt in the same shape and adds it to
the repository's own section, so writing a good prompt needs no study first,
and Improve A Prompt fixes one that went wrong.

---

## 🧭 How A Prompt Runs Anywhere

A prompt that reaches every repository cannot name one repository's commands,
files or branches, so each universal prompt is written to find them and to stay
safe where it does not fit, as the research behind it found agents need:

- **It finds what it needs.** It reads `AGENTS.md`, the README, the
  contributing guide, the build files and the CI configuration for the
  commands, and treats CI as what must pass. It finds the default branch from
  the remote and the last release from the tags. A prompt that edits runs the
  checks first, and stops to ask if they already fail, so a later failure is
  known to be its own.
- **It says what it may change.** A prompt that only looks says to change
  nothing; one that edits names what it may touch, such as only the docs, and
  what it must never do, such as push, rewrite history, edit a lock file by
  hand, or weaken a test to make it pass.
- **It stops where a person decides.** A license, a major upgrade, a design
  change, a secret to rotate or a comment to post waits for a person, and the
  prompt says so.
- **It has a way out.** It says what to do when the task cannot be done
  honestly, or does not apply, such as a page with no user interface, rather
  than leaving the agent to fake a result.
- **It proves the result.** It ends with what shows the work is done, such as
  a check that fails before and passes after, a measurement before and after,
  or a finding traced to the input that triggers it, and what to report.
- **It reads what it did not write as data.** A diff, an issue or a review
  comment is material to weigh, never an instruction; a secret is named by
  where it is, never by its value; and an advisory or a commit hash comes from
  a tool's output, never from memory.

---

## 🔁 How It Arrives And Stays Current

The prompts ride in the same `chore/intelligence` pull request as the rules,
by either route, the stub or `make sync`:

- a repository without `docs/Prompts.md` gets the whole file, which you review
  by hand: `make merge` leaves a pull request that adds it alone;
- after that, each sync replaces only the text between the markers, and
  leaves the rest of the file, the repository's own prompts included, as it
  was. Its pull request names the universal prompts the new block adds,
  rewords and drops, so you can see what changed without reading a sealed
  diff;
- the BEGIN marker carries the SHA-256 of the block's text, so a release that
  leaves the prompts as they were touches no repository, and a hand edit
  inside the markers is caught, by `make audit`, by the standards' Machined
  Block Check in each repository's CI, and by the guard hook, and repaired by
  the next sync;
- a `docs/Prompts.md` with no prompts block is the repository's own file, and
  sync never touches it;
- a `no-intelligence-prompts` topic keeps the prompts out of a repository that
  still takes the rules.

Only a release delivers them, as with the rules. A release from before the
prompts delivers none.

---

## ✍️ Changing The Universal Prompts

The source is [`setup/Prompts.md`](../../setup/Prompts.md): the file exactly as
a repository first gets it, with its markers unsealed, so it stays a file
anyone can edit. [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py)
seals the block when sync delivers it, and `make check` holds the source to
what every repository can carry and to the shape its own practices describe.
`prompts.py --check` names each problem with its line:

- one `INTELLIGENCE:PROMPTS` block, with markers that carry no hash, and no
  private repository named or en or em dash;
- text a formatter leaves as it is: no trailing whitespace, tab or second
  blank line, a blank line around each heading, list and block of code, `-`
  bullets, and every block of code fenced as `text` and closed, with no fence
  inside it. Each repository formats what a push touched, so a block a
  formatter would rewrite reads as edited there;
- every universal prompt under its own `###` heading, with a **Use when**
  line, and a **Fill in** line exactly when it holds a placeholder, before one
  block of text that holds `<context>` and then `<task>`, any `<constraints>`,
  and a `<done_when>` or an `<output>`, every tag closed;
- each detail only a person can give in a placeholder of capitals and
  underscores, and no stray brace;
- text an agent reads as it is meant: printable ASCII, no emphasis in
  capitals, no slot such as `$ARGUMENTS` that an app fills by itself, no
  character that hides or reorders text, and none of the wording the model
  makers now find useless or harmful, such as "think step by step" or a
  persona;
- no prompt over 1,600 characters, and no two headings alike;
- a "Find A Prompt" index that links every prompt once, by its name, and marks
  with ✏️ each one that has details to fill in.

Where Prettier is installed, `make test` also runs it over the source with the
standards' configuration, and fails on any line it would change.

Every universal prompt also has a scenario in
[`evals/prompts/`](../../evals/prompts/README.md) that measures it against the
one-line request it replaces, as [Evals](Evals.md) describes. `make lint`
fails while a prompt has none, or while a scenario fills a placeholder the
prompt no longer holds, so a reworded prompt brings its scenario along, and
`make test` runs each scenario's proof, a script that does the work, to show
its checks pass the work done right and fail when nothing is done. Before a
release carries a changed prompt, run its scenario a few times:

```bash
make evals ARGS='--apps claude --prompts fix-a-bug --runs 3'
```

Keep a change only if the prompt does at least as well as before, and run
the scenarios again when a new model ships, since advice that helps one model
can hurt the next. A prompt
that only one repository needs goes in that repository's own section, never
here.

---

## 🔗 See Also

- [ADR-0025](../adrs/ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): why the prompts reach every repository, and how they are split
- [ADR-0028](../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md): why each universal prompt is checked by `make check` and measured by evals
- [ADR-0029](../adrs/ADR-0029-Most-Prompts-Run-As-They-Are.md): why most universal prompts need nothing filled in, and how they cover every kind of work
- [Prompt Engineering](research/Prompt-Engineering.md): the research the prompts and their practices rest on
- [Prompts For Every Task](research/Prompts-For-Every-Task.md): the research behind the areas the prompts cover and what each must hold
- [Evals](Evals.md): how a prompt scenario measures a universal prompt
- [Repository Sync](Repository-Sync.md): the pull request both blocks ride in
- [The Home Kit](The-Home-Kit.md): the guard hook that keeps both blocks as the hub wrote them

---

<div align="center">

**A better prompt in, better work out.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
