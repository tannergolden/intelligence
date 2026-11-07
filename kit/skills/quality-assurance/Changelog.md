# quality-assurance Changelog

## Current Version

**`2.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

Renamed and merged into the company's whole independent check, one of the twelve department skills. Renamed: the skill `quality` becomes `quality-assurance` (its team stays Quality Assurance (QA)), and every reference to a renamed skill follows (board becomes administration, finance becomes finance-and-accounting, analytics becomes business-intelligence, customers becomes customer-experience, and so on). Merged: the team grows from two seats to five, at the cap. Three seats move in with their duties: the Fact-Checker and the Devil's Advocate from research's Research team, and the Design Critic from visualize's Design team, each losing its old team's references and lead and pointing at this roster. Absorbed, with every duty kept: develop's QA Engineer into the QA Test Engineer, which now also tests the software, skills and agents the research-and-development skill builds (it runs their validator and test suite, tries adversarial cases, and rules PASS, NEEDS-FIX or FAIL per criterion, so it gains Bash to run checks and never edits); finance's Plan Reviewer into the Fact-Checker, which now also reviews a financial plan or a company finance deliverable before the finance-and-accounting skill records it (suitability, the math reproduced, every figure and rule current and cited to its official source, the limits, the risk and the completion evidence; FATAL, MATERIAL or MINOR findings and SHIP, REVISE or HOLD); and discover's Idea Critic into the Devil's Advocate, which now also steelmans then stress-tests ideas (KEEP, FLAW or KILL with evolution potential). Every department borrows these seats by dispatching them directly (research-and-development for its research drafts, idea pools and builds; business-intelligence for its visuals; finance-and-accounting for its plans; any department for the check its work needs), and a verdict always comes from a seat that did not make the work. The skill gains modes (verify, define, test, defects, fact-check, critique, design review), the user's own life (checking any important document, application or plan before it goes out), the personal context rule and the health line, and WebSearch and WebFetch in `allowed-tools` for checking sources. References: `verification.md` gains every seat's verdict vocabulary, how a borrower applies each and how the Head of Quality weighs it; `dispatch.md` gains which seat checks what and the borrowing rules; `deliverables.md` gains each seat's deliverables and the pre-send check of the user's own document; `defects.md` gains the crosswalk from every seat's findings to one severity scale; new `fact-checking.md` (claims, numbers and the plan review) and `critique.md` (conclusions, ideas and the design review checklist). Templates: carried from HEAD and renamed, research's verification ledger as `fact-check-ledger.md`, research's critique as `critique-ledger.md` (with the idea verdict ledger added) and finance's review as `plan-review.md`; new `test-results.md` and `design-review.md`; the brief, the verification report, the test plan and the defect report updated for five seats and for borrowers.

### `1.0.0` - 2026-11-07

Initial build of the quality skill: the company's Quality Assurance (QA) department, which the board skill's workforce held until now, becomes a skill of its own that runs in any repository or a plain conversation. It dispatches its own team (the ★ Head of Quality with the QA Test Engineer) to one standard, no pass without evidence, across the independent verification of consequential deliverables, quality standards and definitions of done, test plans and test runs, and defect triage and root cause. The board skill dispatches its ★ Head of Quality as the company's independent verifier, and every department skill names it for verification. The verdict always comes from a context that did not make the work: the Head of Quality never verifies work it made or helped make, never grades a draft from the author's seat, and is dispatched fresh whenever the conversation made the work or another skill calls from inside its run. Four verdicts (PASS, PASS WITH NOTED DEFECTS, FAIL, ESCALATE); a write-gate under which a verdict clears quality, never authority, and the skill persists only its own department's records. The roster takes develop's format with self-contained global rules, every agent points at it, the board seats it escalates to are named as the board skill's, and both specs exclude the author's reasoning from their inputs. Four references (deliverables, dispatch, verification, defects), four templates (brief, verification report, test plan, defect report) and a trigger test.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
