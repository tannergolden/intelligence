---
name: 'repository-standards'
title: 'Repository Standards'
kind: 'module'
description: "Where the owner's engineering standards live, what each covers and which one wins, carried by every agent that changes files in a repository: read the repository's own rules, then the matching standards document, before you branch, commit, open a pull request, write docs or tests, or add a dependency."
version: '1.0.0'
---

You change files, so you work in repositories: a venture's code, its website, the owner's knowledge vault, this workforce. Every repository the owner keeps follows one set of engineering standards. Know where they are, read the one that matches what you are about to do, and follow it.

## Where The Standards Are

1. **The repository's own rules, first.** Its root `AGENTS.md`: the universal rules between its `INTELLIGENCE` markers, synced from tannergolden/intelligence, then the repository's own rules and their Overrides. Then its `README.md`, its `.github/CONTRIBUTING.md`, its pull request template and its `docs/`.
2. **The engineering standards.** The repository tannergolden/standards on GitHub, every guide indexed in its [`docs/README.md`](https://github.com/tannergolden/standards/blob/Development/docs/README.md).
3. **Which wins.** The owner's explicit request for the task, then the repository's Overrides entry for that rule, its own rules, its `docs/`, the standards' `docs/`, then its copy of the universal rules. An Invariant in the universal rules yields to nothing.

## Read Before You Act

| Before you                             | Read in tannergolden/standards                              |
| :------------------------------------- | :---------------------------------------------------------- |
| Branch, or move work toward a release  | `docs/distribution/Branching-Strategy-&-Workflow.md`        |
| Commit                                 | `docs/distribution/Conventional-Commits.md`                 |
| Open, update or review a pull request  | `docs/distribution/Pull-Requests-&-Code-Reviews.md`         |
| Write, change or run tests             | `docs/distribution/Testing-Strategy.md`                     |
| Change CI or a workflow                | `docs/distribution/Continuous-Integration-&-Delivery.md`    |
| Cut a release or set a version         | `docs/distribution/Releases-&-Versioning.md`                |
| Write or change any document           | `docs/technical/interface/Document-Styling-&-Formatting.md` |
| Handle a secret, a key or a credential | `docs/operations/Security-&-Secrets.md`                     |
| Add or update a dependency             | `docs/operations/Dependency-Management.md`                  |
| Add, move or remove files and folders  | `docs/operations/Repository-Hygiene.md`                     |
| Set up a tool or a stack               | `docs/introduction/Environment-&-Technologies.md`           |
| Run a git command you are unsure of    | `docs/library/Git-Commands.md`                              |

Read the matching file in the repository's own `docs/` too, when it has one (STD-001).

## The Rules You Meet Every Day

The exact wording is in the repository's `AGENTS.md` and the guides above; where this list and they differ, they win.

- **Branches.** `Development` is the default branch, promoted to `Preview` and then `Release`; work goes on a `<type>/<topic>` branch, such as `feat/` or `bugfix/`, into `Development` by pull request (GIT-010). Never push to a default or protected branch, force-push except with `--force-with-lease` on a branch you created, delete a remote branch or tag, or merge a pull request (OPS-001).
- **Commits.** `type(scope): subject`, with a scope and a lowercase subject, then a body that says why (GIT-010). The owner is the author and signs off last, never an AI (GIT-001), and an AI that shaped the commit is credited with `Co-Authored-By:` above the sign-off (GIT-013).
- **Pull requests.** One intent, under 300 changed lines and at most 10 files, into `Development`, squash-merged (GIT-012); opened only when the owner asks (OPS-005), with the AI's help disclosed.
- **Checks.** Run the narrowest test that covers the change, then the repository's documented checks (CODE-001). Every hook and CI check passes by fixing its cause (CODE-004), never by weakening a test (CODE-002) or routing around a block (OPS-004).
- **Documents.** Hidden frontmatter and the styling guide's headers and footers; plain words, and never an em dash (DOC-002, DOC-003).
- **Secrets and dependencies.** No credential in any file, commit, log or message, ever (SEC-001). Only the packages the task needs, pinned, from the project's registry, and never a download piped to a shell (SEC-004).
- **What you did.** Report what you ran and its result, what failed and what you skipped, and claim done only on a check you ran (COM-002).
