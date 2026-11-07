# Roster - the three seats wired to the interview

The contract that wires this skill to its people. Three seats, all reuse, constant across every run regardless of facet or sensitivity: the skill **embodies the UX and Design Research Lead** as the interviewer, **dispatches the Writer** to compose, and **dispatches the Standards Reviewer** to review blind. This file is the single source of truth for who runs, on what, and what each hands back; `interviewing.md` and `question-maps.md` shape the interview itself, `provenance.md` governs every line composed.

**The single-writer flow.** The two dispatched seats **return** their artifact as their final message and **persist nothing** (that is each spec's write-scope). The skill's own top-level context, embodied as the UX and Design Research Lead, is the sole writer: it holds the interview ledger, it dispatches the Writer and the Standards Reviewer, and it alone keeps the approved batch at pipeline step 10, writing it only into a profile repository (SKILL.md, Where the profile lives). Never brief a dispatched seat to "write a file": that contradicts its spec and confuses it.

## Each seat: how it runs, its input, what it returns, and the template that shapes the return

| Seat (name) | How it runs | Input | Returns | Template |
|-------------|-------------|-------|---------|----------|
| **UX and Design Research Lead** | **embodied** as the top-level context, every run | the target facet, its current content and section gaps (from the repository's coverage command when it names one), and the running interview ledger | the interview ledger and the kept batch; it is the only converser and the only writer | `templates/interview-plan.md` |
| **Writer** | **dispatched**, every run that produces a batch | the interview ledger inline, the facet's current content (its file paths in a profile repository, or the profile the user shared), `references/provenance.md`, `templates/proposal-batch.md` | the composed proposal batch, markers already applied per `provenance.md` | `templates/proposal-batch.md` |
| **Standards Reviewer** | **dispatched blind**, every batch, always | the batch, the profile rules and marker grammar in `references/provenance.md` plus a profile repository's own rules, SEC-003; never the ledger or the Writer's brief | one review ledger row per proposal | the review ledger shape below (inline) |

## The seats in full

**The UX and Design Research Lead** (the board skill's `agents/UX and Design Research Lead.md`, in the Research & Development (R&D) department). Its craft is the skill's spine: instrument design, non-leading questions, and the observed-versus-stated-versus-assumed evidence discipline that keeps the ledger honest. The skill runs *as* it: the top-level context announces as the UX and Design Research Lead embodied (no handoff ceremony), converses, calls the question tool, keeps the session-only ledger, dispatches the other two, applies verdicts, and keeps the approved batch. It is embodied rather than dispatched precisely because only the top-level context can hold the conversation and call the question tool.

**The Writer** (the editorial skill's `agents/Writer.md`). It composes the proposal batch from the ledger in the user's own voice: one construct per line, stated rows to unmarked lines, observed rows to fully-marked `unconfirmed` lines, the Snapshot composed last. Its sole factual input is the ledger passed in the brief: if it is not in the ledger, it does not exist to it. It returns the batch in the `templates/proposal-batch.md` shape and persists nothing.

**The Standards Reviewer** (the research skill's `agents/Standards Reviewer.md`). It audits the batch blind against the profile rules (`provenance.md`, plus a profile repository's own) and SEC-003: every proposed line traceable to a stated answer or correctly marked, no record-shaped fact smuggled into a profile line (the records boundary), no sensitive line beyond the minimum needed to be considerate (the sensitive categories). It receives the batch and the law only, never the interview reasoning or the Writer's brief, so its eyes are fresh. It returns one ledger row per proposal and persists nothing.

## The verdict vocabulary (so the lead applies a return mechanically)

The Standards Reviewer classifies each proposal exactly one of:

- **BLOCK** - do not write this line as proposed. Applied: drop it, or re-mark it (a line asserted as stated but only observed becomes a marked `unconfirmed` line, or is cut).
- **REVISE** - the named change makes it safe. Applied: make exactly that edit, then the line stands.
- **CLEAR** - no exposure; the line stands as written.

Verdicts apply mechanically and in **one round only**. REVISE is applied, BLOCK is dropped or re-marked, CLEAR passes through; there is no argue-back loop and no second review pass. A BLOCK never becomes an approval by re-running the review.

## The review ledger (the Standards Reviewer's inline shape)

A blind seat with no template file; it returns one row per proposal:

```
[proposal N] · disposition (BLOCK / REVISE / CLEAR) · the specific rule it touches (read-only / propose first / facts not guesses / sensitive categories / records boundary / provenance grammar) · the concrete risk · the required change (REVISE) or the reason (BLOCK)
```

## Blind pairing

The Standards Reviewer reviews the batch and the law, never the ledger, the plan, or the Writer's brief. That separation is the quality lever: a reviewer who saw how the batch was assembled cannot audit whether each line is truly traceable. The rule is non-negotiable on sensitive facets and holds on every run; there is no batch too small to review (SKILL.md, dispatch scaling). When the Agent tool is unavailable, run the Writer's and the Standards Reviewer's specs sequentially in the one context with role headers, and tell the user the blind-review guarantee is weakened: a single context cannot give the reviewer fresh eyes.

## The cross-home reference convention

The research skill's convention for a borrowed seat. `metadata.team` in SKILL.md names **Research & Development (R&D)**, the board workforce's department that is home to the embodied lead. The two dispatched seats are referenced by name from their own skills: the Writer from the editorial skill's `agents/`, the Standards Reviewer from the research skill's `agents/`. Nothing is copied into this skill: it carries no `agents/` folder and reads all three specs, by the skill-relative locations above, from the sibling skills installed beside it (board, editorial, research), which stay their source of truth.

## Rejected alternatives

- **A dedicated interviewer sub-agent.** Rejected: only the top-level context can converse and call the question tool, so the interviewer is embodied, not dispatched. A dispatched interviewer would need the conversation relayed to it turn by turn, which no brief can carry.
- **A second reviewer or a standalone privacy seat.** Rejected: the Standards Reviewer's blind audit against the profile rules and SEC-003 already covers privacy and sensitive-category exposure; a second reviewer adds coordination cost without adding a fresh angle. The lever is blindness, not headcount.
- **Letting the Writer check its own composition.** Rejected: "now review your own work" collapses the independence that makes the review worth running. Composition and review are always two contexts.
- **Skipping review on a one-line batch.** Rejected: there is no batch too small to review; even a single proposed line can carry an unmarked inference or a records-boundary violation.
