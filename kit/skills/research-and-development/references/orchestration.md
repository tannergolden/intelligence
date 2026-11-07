# Orchestration - the build mode's dispatch

How the build mode dispatches without misfires. The skill, as the ★ Head of Research & Development, briefs the R&D team's **Full-Stack Engineer** (its design pass, then its build pass) and, for a product-shaped build whose scope is open, the **UX and Design Research Lead**, as fresh-context subagents per build, handing each its spec in this skill's `agents/` as its role. The independent reviewers are **borrowed seats, not members**: the quality-assurance skill's **QA Test Engineer** (correctness) and **Design Critic** (a user-facing interface), and the information-technology skill's **Security Engineer** (security), each read from its own skill's `agents/` folder, installed beside this one, and never copied here. Dispatch scaling (who runs at which complexity) is in `SKILL.md`, the lead's method in `lead-build.md`; this is the contract for how each dispatch is shaped. Read it before the first dispatch of a build.

## The self-contained brief

A subagent sees none of this conversation. Every dispatch brief restates, in full: the **objective** (the one job and the success test), the **output contract** (the exact artifact shape, and the absolute path to write it to when the seat writes one), the **inputs** (every path to read), the **tools and sources** to use, and the **boundaries** (what not to do, what to flag and stop on). An incomplete brief is the single most common dispatch failure: the worker improvises the gap.

Fill every field on every dispatch; an omitted field is precisely the gap that gets improvised:

```
ROLE: read <agent spec path>. You are the <title>.
OBJECTIVE: <the one job> - you are done when <success test>.
INPUTS: read <absolute paths>. Assume <X>; flag and stop if <Y> is missing.
OUTPUT: write <artifact> to <absolute path>, or return it; return a summary of at most <N> lines.
TOOLS / SOURCES: <what to use, what to prefer>.
BOUNDARIES: never <forbidden action>. Write-scope: <what it may write>.
```

A borrowed reviewer is briefed in its own skill's brief shape, which names its spec and that skill's roster: the QA Test Engineer and the Design Critic in the quality-assurance skill's `templates/brief.md` shape, the Security Engineer in the information-technology skill's `templates/brief.md` shape. Each gets the build (its checkout by absolute path, or the diff), the locked requirements and the definition of done, the run instructions and the test suite, and the validator's output; never the builder's notes or reasoning.

## What each seat returns

| Seat | Runs on | Returns | Shape |
|------|---------|---------|-------|
| **Full-Stack Engineer**, design pass | every full build, before any code | the build plan: structure, stack, interfaces and data shapes, the file plan, the named risks, the one resolved hard tradeoff, what was left undecided | its output contract |
| **Full-Stack Engineer**, build pass | after the lead checks the plan; again on each fix-loop round | the build, written where the brief names, and the build notes: what was built, deviations and why, how to run it | its output contract |
| **UX and Design Research Lead** | a product-shaped build whose scope is open | the design intent and the usability criteria, each traced to a user need | its output contract |
| **QA Test Engineer** (borrowed) | every build that will be used unattended, and every non-trivial edit | the test results: per criterion PASS / NEEDS-FIX / FAIL, each defect with its severity and repro | the quality-assurance skill's `templates/test-results.md` |
| **Design Critic** (borrowed) | a build with a user-facing interface | the design review: issues FATAL / MATERIAL / MINOR, the accessibility gate PASS / FAIL, one call SHIP / HOLD | the quality-assurance skill's `templates/design-review.md` |
| **Security Engineer** (borrowed) | every build | the security ledger: findings ranked by exploitability and blast radius, ending in ship or block | the information-technology skill's `templates/security-ledger.md` |

The lead applies each verdict mechanically: the QA Test Engineer's and the Design Critic's by the rule in the quality-assurance skill's `references/verification.md`, the Security Engineer's by the information-technology skill's `references/security.md`. A NEEDS-FIX, a FAIL, a HOLD or a block goes back to the builder on the cited items only. A reachable high-severity exploit blocks the ship until it is fixed and re-reviewed; a request to ship past a security block goes to the information-technology skill, never through this one.

## Only the orchestrator spawns

The skill, as the lead, is the only one that dispatches. Subagents never spawn subagents; all fan-out happens at the top, where the full picture lives. A worker that needs more work done returns a flag, and the lead dispatches the follow-up.

## The filesystem is the artifact bus

Each phase writes its artifact to a run workspace (a scratch folder outside the repository's tracked files, or wherever the repository's rules put work in progress); the next phase reads it from disk. Workers return a short summary (status, artifact path, key decisions, flags), never a file dump. Passing artifacts inside chat messages loses detail in transit; the file is the source of truth. The Full-Stack Engineer is the one seat that writes, and only where its brief names; the reviewers return their ledgers and persist nothing.

## Scale the dispatch, and parallelize only the independent

A multi-agent run costs about 15x a single agent, so dispatch is scaled to the build, not reflexive. Parallelize genuinely independent work (separate reviewers, separate dimension reviews); keep interdependent authoring sequential, because parallel generation does not suit work where each part depends on the others. The design pass and the build pass run in sequence, in one seat, so the build never improvises what the design resolved.

## The fix loop

A validator error, a NEEDS-FIX, a FAIL, a HOLD or a security block resumes the builder on the cited issues only. Re-run `scripts/validate.py` always, with the repository's own checks; re-audit only the cited items, and every line the fix touched, with a fresh reviewer. If the same error survives two rounds, stop and surface a likely requirement-level conflict to the user rather than looping.

## Independence is structural, not requested

The reviewers are fresh-context seats that never touch the build and never read the builder's notes, so no reviewer can fix-and-rubber-stamp its own work, and no reviewer holds an edit tool. The validator and the tests are run by the skill, or by the QA Test Engineer where its tools let it execute checks, and their output travels to the reviewers as evidence. Never "now check your work"; always a separate, fresh-context invocation. That separation is the main quality lever and must not be collapsed for speed.

## When a seat or a subagent is unavailable

When a borrowed reviewer's skill is not installed beside this one, brief a fresh subagent with that reviewer's job from the table above (its objective, what it checks and its verdict vocabulary), and tell the user the check ran without its spec. Where the app offers no way to start a subagent at all, run the same role specs sequentially in this one context with role headers, and tell the user the independent-review guarantee is weakened: a single context cannot give the reviewer fresh eyes. Ask the user to review the result before anything relies on it. This single-context mode is the fallback, never the default.
