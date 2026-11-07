# information-technology Changelog

## Current Version

**`2.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The `systems` skill is renamed `information-technology`, named for its department, one of the twelve that cover every area of a company the user runs and of the user's own life; the team keeps its title, Information Technology (IT), and its four seats. Absorbed: the `develop` skill's Application Security Engineer merges into the Security Engineer, which takes over every duty it held: the threat model and security review of anything built (an app, a tool, a script, a skill, an agent, a pull request), every build the research-and-development skill makes included, run fresh and blind to the builder's reasoning, findings ranked by exploitability and blast radius, each with its severity, exploit path and fix, and a reachable high-severity exploit blocking the ship until it is fixed and re-reviewed; it cites the fix and never rewrites the build, and gains `Bash` for read-only checks in a build's own checkout (a dependency audit, a secret scan, the build's tests). The research-and-development skill borrows the seat for every build, as departments borrow the quality-assurance skill's ★ Head of Quality, and a request to ship past a block goes to the Chief Information Security Officer and, if refused, the Founder. New: `templates/security-ledger.md`, a build-review tier row and routing, and the security review of a build in `references/security.md`. The department now runs the user's own digital life too: devices, accounts, backups and digital security, a security checkup, a scam read and a hacked account's recovery, never recording a password or any secret, only where it lives (SEC-001), with personal deliverables, the user's own section in the systems register, personal gated acts, the personal context and health rules in `SKILL.md` and the roster's Global rules, and personal triggers in the description and the trigger test. Every mention of another department follows the renames (board to administration, develop to research-and-development, operations to operations-and-logistics, legal to legal-and-compliance, quality to quality-assurance, people to human-resources, communications to public-relations, visualize to business-intelligence, research to research-and-development), and seats in other departments are named as the new skill's.

### `1.0.0` - 2026-11-07

Initial build of the systems skill: the company's Information Technology (IT) department, which board convened as part of its workforce, becomes a skill of its own that runs a company's internal systems (the tools and platforms it works on, accounts and access, internal tooling and automations, and their security), to the standard secure by default, reversible by design. The separate Information Security department merges into IT: the Chief Information Security Officer joins the team as an unstarred member and keeps its security-risk line straight to the Founder, so it can hold or refuse a change on unaccepted security risk regardless of the Chief Information Officer. The skill embodies the ★ Chief Information Officer and dispatches the Platform Engineer, the Security Engineer and the Chief Information Security Officer by tier; it persists its own department's records behind its write-gate, where rotating or revoking a credential, changing a real person's access, deleting data and disabling a security control wait for the user's yes, and no secret is ever written down. Ships `references/deliverables.md`, `dispatch.md`, `security.md` and `gated-acts.md`, the brief, change-review, incident-record and systems-register templates, and its trigger test.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
