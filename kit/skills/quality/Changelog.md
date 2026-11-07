# quality Changelog

## Current Version

**`1.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `1.0.0` - 2026-11-07

Initial build of the quality skill: the company's Quality Assurance (QA) department, which the board skill's workforce held until now, becomes a skill of its own that runs in any repository or a plain conversation. It dispatches its own team (the ★ Head of Quality with the QA Test Engineer) to one standard, no pass without evidence, across the independent verification of consequential deliverables, quality standards and definitions of done, test plans and test runs, and defect triage and root cause. The board skill dispatches its ★ Head of Quality as the company's independent verifier, and every department skill names it for verification. The verdict always comes from a context that did not make the work: the Head of Quality never verifies work it made or helped make, never grades a draft from the author's seat, and is dispatched fresh whenever the conversation made the work or another skill calls from inside its run. Four verdicts (PASS, PASS WITH NOTED DEFECTS, FAIL, ESCALATE); a write-gate under which a verdict clears quality, never authority, and the skill persists only its own department's records. The roster takes develop's format with self-contained global rules, every agent points at it, the board seats it escalates to are named as the board skill's, and both specs exclude the author's reasoning from their inputs. Four references (deliverables, dispatch, verification, defects), four templates (brief, verification report, test plan, defect report) and a trigger test.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
