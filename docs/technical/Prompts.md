<!--
title: '💬 PROMPTS'
description: 'The universal prompts the hub keeps in its own docs/Prompts.md for anyone to copy, most ready to run as they are, and the empty docs/Prompts.md each repository gets for prompts of its own: how each works, and how to change it.'
type: guide
-->

<div align="center">

# 💬 PROMPTS

<a name="top"></a>

**Universal prompts in the hub, and a page of its own in every repository.**

_Find one. Copy it. Paste it._

</div>

---

## 💡 Two Places For Prompts

A prompt typed in a hurry leaves out what an agent needs: the goal, the
context it cannot see, the limits, and how to tell when it is done. So the hub
keeps ready-made prompts anyone can copy into any AI app, the owner and every
collaborator alike, and every repository keeps the prompts only it needs.
Each prompt sits in its own fenced block, so GitHub shows a copy button on it.

| Where                                                        | Whose                     | What it holds                                                                                                                |
| :----------------------------------------------------------- | :------------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| [`docs/Prompts.md`](../Prompts.md) in the hub                | The hub's                 | How to use a prompt; an index of every prompt; the universal prompts, grouped by the kind of work they do; and the practices |
| `docs/Prompts.md` in each repository that takes part in sync | The repository's, its own | The prompts its owner writes for that repository alone: for using it, changing it and understanding it                       |

The universal prompts stay in the hub. A repository gets its own page once,
empty, from [`setup/Prompts.md`](../../setup/Prompts.md), and sync never
changes it after that.

Most of the universal prompts run as they are: the agent finds what changes
from one repository to the next, such as its commands, its default branch or
its last release, in the repository itself. The few that need what only a
person knows, such as the bug they saw, mark it with a placeholder in double
braces, such as `{{ERROR_OUTPUT}}`, and name it in a **Fill in** line.

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
the repository's own `docs/Prompts.md`, so writing a good prompt needs no study
first, and Improve A Prompt fixes one that went wrong.

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

## 🔁 How A Repository Gets Its Page

The page rides in the same `chore/intelligence` pull request as the rules, by
either route, the stub or `make sync`:

- a repository without `docs/Prompts.md` gets the empty page, with a section
  each for using, changing and understanding the repository and a link to the
  universal prompts. You review it by hand: `make merge` leaves any change to
  `docs/Prompts.md` alone;
- after that the page is the repository's own, and sync never touches it;
- release v0.3.0 delivered the universal prompts into each repository's
  `docs/Prompts.md`, between sealed `INTELLIGENCE:PROMPTS` markers. Sync takes
  that block out again, in the same pull request, and leaves everything
  else in the file, the repository's own prompts included. A file nobody
  touched since that release becomes the empty page, and `make audit` names
  each repository whose page still holds the block;
- a `no-intelligence-prompts` topic keeps sync from adding or changing the
  page in a repository that still takes the rules.

Only a release delivers the page, as with the rules. A release from before
it, v0.3.0 among them, delivers no prompts at all.

---

## ✍️ Changing The Universal Prompts

They live in the hub's [`docs/Prompts.md`](../Prompts.md), and everyone
copies them from there, so a change reaches people as soon as it lands, with
no release. [`.github/scripts/prompts.py`](../../.github/scripts/prompts.py)
holds the file to the shape its own practices describe, and `make check`
fails on any problem. `prompts.py --check` names each with its line:

- no `INTELLIGENCE:PROMPTS` marker, since nothing seals or delivers them now,
  and no private repository named or en or em dash;
- text a formatter leaves as it is, between the header and the footer: no
  trailing whitespace, tab or second blank line, a blank line around each
  heading, list and block of code, `-` bullets, and every block of code fenced
  as `text` and closed, with no fence inside it;
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

Where Prettier is installed, `make test` also runs it over both prompts files
with the standards' configuration, and fails on any line it would change.

Every universal prompt also has a scenario in
[`evals/prompts/`](../../evals/prompts/README.md) that measures it against the
one-line request it replaces, as [Evals](Evals.md) describes. `make lint`
fails while a prompt has none, or while a scenario fills a placeholder the
prompt no longer holds, so a reworded prompt brings its scenario along, and
`make test` runs each scenario's proof, a script that does the work, to show
its checks pass the work done right and fail when nothing is done. Before a
release carries a changed prompt, run its scenario at least seven times each
way:

```bash
make evals ARGS='--apps claude --prompts fix-a-bug --runs 7'
```

Keep a change only if the prompt does at least as well as before, and run
the scenarios again when a new model ships, since advice that helps one model
can hurt the next. A prompt that only one repository needs goes in that
repository's own `docs/Prompts.md`, never here.

---

## 📄 Changing The Page A Repository Gets

[`setup/Prompts.md`](../../setup/Prompts.md) is the page a repository first
gets, exactly as it lands. `prompts.py --check` holds it to what any
repository can carry: no prompt, since the page is the repository's to fill,
no `INTELLIGENCE:PROMPTS` marker, no private repository named and no en or em
dash. A change reaches only the repositories that get a page after the next
release; one that already has a page keeps its own.

---

## 🔗 See Also

- [ADR-0031](../adrs/ADR-0031-Universal-Prompts-Stay-In-The-Hub.md): why the universal prompts stay in the hub, and each repository gets an empty page of its own
- [ADR-0025](../adrs/ADR-0025-Every-Repository-Gets-Ready-Made-Prompts.md): the earlier decision to seal the universal prompts into every repository, which ADR-0031 supersedes
- [ADR-0028](../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md): why each universal prompt is checked by `make check` and measured by evals
- [ADR-0029](../adrs/ADR-0029-Most-Prompts-Run-As-They-Are.md): why most universal prompts need nothing filled in, and how they cover every kind of work
- [Prompt Engineering](research/Prompt-Engineering.md): the research the prompts and their practices rest on
- [Prompts For Every Task](research/Prompts-For-Every-Task.md): the research behind the areas the prompts cover and what each must hold
- [Evals](Evals.md): how a prompt scenario measures a universal prompt
- [Repository Sync](Repository-Sync.md): the pull request the rules and the page ride in

---

<div align="center">

**A better prompt in, better work out.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
