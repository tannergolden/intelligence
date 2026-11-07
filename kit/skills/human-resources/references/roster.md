# Roster - the seats wired to the profile interview

The contract that wires the profile interview to its people. Three seats, all borrowed by title from other departments and constant across every run regardless of facet or sensitivity: the skill **embodies the research-and-development skill's UX and Design Research Lead** as the interviewer, **dispatches the public-relations skill's Editor** to compose, and **dispatches the legal-and-compliance skill's Privacy & Data Protection Counsel** to review blind. This file is the single source of truth for who runs in the profile mode, on what, and what each hands back; `interviewing.md` and `question-maps.md` shape the interview itself, `provenance.md` governs every line composed. The department's own team, its lead and its other seats, is in `agents/Human Resources (HR).md`; of them, only the HRIS and People Operations Analyst joins this mode, for the uniqueness check on an approved record offer.

**The single-writer flow.** The dispatched seats **return** their artifact as their final message and **persist nothing** (that is each spec's write-scope). The skill's own top-level context, embodied as the UX and Design Research Lead, is the sole writer: it holds the interview ledger, it dispatches the Editor and the Privacy & Data Protection Counsel, and it alone keeps the approved batch at pipeline step 10, writing it only into a profile repository (`SKILL.md`, Where it runs). Never brief a dispatched seat to "write a file": that contradicts its spec and confuses it.

## Each seat: how it runs, its input, what it returns, and the template that shapes the return

| Seat | How it runs | Input | Returns | Template |
|------|-------------|-------|---------|----------|
| **UX and Design Research Lead** (the research-and-development skill's) | **embodied** as the top-level context, every run | the target facet, its current content and section gaps (from the repository's coverage command when it names one), and the running interview ledger | the interview ledger and the kept batch; it is the only converser and the only writer | `templates/interview-plan.md` |
| **Editor** (the public-relations skill's), as the composer | **dispatched**, every run that produces a batch | the interview ledger inline, the facet's current content (its file paths in a profile repository, or the profile the user shared), `references/provenance.md`, `templates/proposal-batch.md` | the composed proposal batch, markers already applied per `provenance.md` | `templates/proposal-batch.md` |
| **Privacy & Data Protection Counsel** (the legal-and-compliance skill's) | **dispatched blind**, every batch, always | the batch, the profile rules and marker grammar in `references/provenance.md` plus a profile repository's own rules, SEC-003; never the ledger, the plan or the Editor's brief | one review ledger row per proposal | the review ledger shape below (inline) |
| **HRIS and People Operations Analyst** (this team's) | **dispatched** only when an approved record offer is to be written as new in a profile repository | the approved record offers, and where the repository's instructions keep such records | the uniqueness verdict per offer: clear, or the colliding record named | its output contract |

## The seats in full

**The UX and Design Research Lead** (the research-and-development skill's `agents/UX and Design Research Lead.md`, where it does user and customer research). Its craft is the profile interview's spine: instrument design, non-leading questions, and the observed-versus-stated-versus-assumed evidence discipline that keeps the ledger honest. The skill runs *as* it in the profile mode: the top-level context announces as the UX and Design Research Lead embodied (no handoff ceremony), converses, calls the question tool, keeps the session-only ledger, dispatches the other seats, applies verdicts, and keeps the approved batch. It is embodied rather than dispatched precisely because only the top-level context can hold the conversation and call the question tool. While it works for this team it follows the global rules in `agents/Human Resources (HR).md`.

**The Editor** (the public-relations skill's `agents/Editor.md`, that department's fresh reader, borrowed here as the composer). It composes the proposal batch from the ledger in the user's own voice: one construct per line, stated rows to unmarked lines, observed rows to fully-marked `unconfirmed` lines, the Snapshot composed last. Its sole factual input is the ledger passed in the brief: if it is not in the ledger, it does not exist to it. It returns the batch in the `templates/proposal-batch.md` shape and persists nothing. It composes the batch and never reviews it: reading drafts fresh is its craft elsewhere, but here the review is the Privacy & Data Protection Counsel's.

**The Privacy & Data Protection Counsel** (the legal-and-compliance skill's `agents/Privacy & Data Protection Counsel.md`). It audits the batch blind against the profile rules (`provenance.md`, plus a profile repository's own) and SEC-003: every proposed line traceable to a stated answer or correctly marked, no record-shaped fact smuggled into a profile line (the records boundary), no sensitive line beyond the minimum needed to be considerate (the sensitive categories), and nothing headed for a repository not made to hold it. It receives the batch and the law only, never the interview reasoning or the Editor's brief, so its eyes are fresh. It returns one ledger row per proposal and persists nothing.

**The HRIS and People Operations Analyst** (this skill's `agents/HRIS and People Operations Analyst.md`). It never sees the ledger or the batch: it receives only the approved record offers and checks each against the records the profile repository already keeps, by name and alias, so a person, an event, a date or a decision is never written twice. A collision is shown to the user, never merged silently.

## The verdict vocabulary (so the interviewer applies a return mechanically)

The Privacy & Data Protection Counsel classifies each proposal exactly one of:

- **BLOCK** - do not write this line as proposed. Applied: drop it, or re-mark it (a line asserted as stated but only observed becomes a marked `unconfirmed` line, or is cut).
- **REVISE** - the named change makes it safe. Applied: make exactly that edit, then the line stands.
- **CLEAR** - no exposure; the line stands as written.

Verdicts apply mechanically and in **one round only**. REVISE is applied, BLOCK is dropped or re-marked, CLEAR passes through; there is no argue-back loop and no second review pass. A BLOCK never becomes an approval by re-running the review.

## The review ledger (the reviewer's inline shape)

A blind seat with no template file; it returns one row per proposal:

```
[proposal N] · disposition (BLOCK / REVISE / CLEAR) · the specific rule it touches (read-only / propose first / facts not guesses / sensitive categories / records boundary / provenance grammar / SEC-003) · the concrete risk · the required change (REVISE) or the reason (BLOCK)
```

## The briefs

Each dispatched seat gets a self-contained brief in the `templates/brief.md` shape, with these specifics:

- **The Editor.** ROLE reads the public-relations skill's `agents/Editor.md` and this skill's `agents/Human Resources (HR).md`. OBJECTIVE: compose the proposal batch, the duty the profile interview borrows the seat for, not its fresh read of a draft. INPUTS: the interview ledger inline (stated and observed rows, never the skipped ids), the facet's current content, `references/provenance.md`, `templates/proposal-batch.md`. OUTPUT: the batch in that template's shape, markers applied. BOUNDARIES: compose from the ledger alone; mark every inference; no skip, refusal or record-shaped fact in a profile line; never review the batch; persist nothing.
- **The Privacy & Data Protection Counsel.** ROLE reads the legal-and-compliance skill's `agents/Privacy & Data Protection Counsel.md` and this skill's `agents/Human Resources (HR).md`. INPUTS: the batch, the profile rules and marker grammar in `references/provenance.md`, a profile repository's own profile rules, and SEC-003; nothing else. OUTPUT: one review ledger row per proposal, in the shape above. BOUNDARIES: review blind; never rewrite the batch beyond a REVISE's named change; persist nothing.
- **The HRIS and People Operations Analyst.** ROLE reads this skill's `agents/HRIS and People Operations Analyst.md` and `agents/Human Resources (HR).md`. INPUTS: the approved record offers, and the path where the profile repository's instructions keep such records. OUTPUT: the uniqueness verdict per offer. BOUNDARIES: read only; persist nothing.

## Blind pairing

The Privacy & Data Protection Counsel reviews the batch and the law, never the ledger, the plan, or the Editor's brief. That separation is the quality lever: a reviewer who saw how the batch was assembled cannot audit whether each line is truly traceable. The rule is non-negotiable on sensitive facets and holds on every run; there is no batch too small to review (`SKILL.md`, Dispatch scaling). When the subagent tool is unavailable, run the Editor's and the reviewer's specs sequentially in the one context with role headers, and tell the user the blind-review guarantee is weakened: a single context cannot give the reviewer fresh eyes.

## The cross-home reference convention

`metadata.team` in `SKILL.md` names **Human Resources (HR)**, this skill's own team, whose roster is `agents/Human Resources (HR).md`. The profile interview's three seats are borrowed by title: the roster names them in its body, never in its `members`, and their specs stay in their own skills, the UX and Design Research Lead in the research-and-development skill's `agents/`, the Editor in the public-relations skill's and the Privacy & Data Protection Counsel in the legal-and-compliance skill's, which remain their source of truth. Nothing is copied into this skill.

## Rejected alternatives

- **A dedicated interviewer sub-agent.** Rejected: only the top-level context can converse and call the question tool, so the interviewer is embodied, not dispatched. A dispatched interviewer would need the conversation relayed to it turn by turn, which no brief can carry.
- **The department's lead as the interviewer.** Rejected: the Chief Human Resources Officer's craft is roles, pay and a company's people; drawing a true self-report out of someone without leading them is user research, the UX and Design Research Lead's craft, so the skill embodies that seat for this mode.
- **The Compliance Officer as the reviewer.** Rejected: it holds the standards and ethics gate on external-facing output, and a profile batch is never external-facing. Its risks (an unmarked inference, a sensitive line beyond the minimum, a record smuggled into the profile, personal context headed for the wrong repository) are privacy and data-minimization risks, the Privacy & Data Protection Counsel's craft.
- **A second reviewer, or the quality-assurance skill's ★ Head of Quality on top.** Rejected: the blind privacy review against the profile rules and SEC-003 already covers what the batch can expose, and the user's line-by-line approval is the final gate; a second reviewer adds coordination cost without a fresh angle. The lever is blindness, not headcount.
- **Letting the Editor check its own composition.** Rejected: reviewing is the Editor's craft, but never of a batch it composed; "now review your own work" collapses the independence that makes the review worth running. Composition and review are always two contexts.
- **Skipping review on a one-line batch.** Rejected: there is no batch too small to review; even a single proposed line can carry an unmarked inference or a records-boundary violation.
