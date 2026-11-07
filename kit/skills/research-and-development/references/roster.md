# Roster - the research mode's seats wired to its pipeline

The contract that wires the research mode to its seats: the R&D team's own, whose specs ship in this skill's `agents/` (the team's roster is `agents/Research & Development (R&D).md`), and the seats it borrows from other departments by title. It is the single source of truth for who runs, on what, and what each one hands back; `research-dispatch.md` sets the per-tier order and the briefing shape, and `lead-research.md` the lead's own method.

**The return-based flow.** Every seat **returns** its artifact as its final message and **persists nothing** (that is each spec's write-scope). The lead is the only one who writes a workspace file: `draft.md`, the synthesis the blind reviewers attack. So the lead collects the returns, writes `draft.md`, points the Fact-Checker and the Devil's Advocate at it, and applies their returned ledgers. Never brief a seat to "write a file": that contradicts its spec and confuses it.

## Each seat: trigger, input, what it returns, and the template that shapes the return

| Seat | Runs on | Input | Returns | Template |
|------|---------|-------|---------|----------|
| **★ Head of Research & Development** (the lead) | every run, as orchestrator; Step 0 before every non-quick run when the repository's instructions point to filed reports; the search approval on deep runs; the final polish when a report file ships | the user's verbatim question; the filed reports; the source strategy; the verified draft | the Step-0 verdict (canonical report reused, refreshed, or merged, or the gap); APPROVE or REVISE on the strategy; the findings-first answer, and `draft.md` for review; the polished report with an edit note | `reporting.md` Step 0 (inline); the chat shape in `reporting.md`; `templates/report.md` when filed |
| **All-Source Analyst**, strategy pass | deep, before the fan-out | the lanes | the source strategy per lane with its self-check (sentinel check, coverage gaps, biased or low-recall queries, dissent-seeking queries) | `templates/source-strategy.md` |
| **All-Source Analyst** xN, lane pass | standard, deep; one lane grounds locally first, only when the repository's instructions name a reference collection or offline knowledge base | one lane (the five lane fields); on the local-grounding lane, the collection's location and any search-command results the skill fetched | the lane findings brief; on the local-grounding lane, the holdings found, cited, the gaps, and any follow-up query for the skill to run | `templates/lane-brief.md` |
| **UX and Design Research Lead** | standard, deep; only on a lane about users or customers | the lane's research question, and any notes, transcripts or survey results the user supplies | the study plan (screener and guide), or the insights, each with its verbatim evidence and count, and the gaps | inline, in its output contract |
| **Fact-Checker** (borrowed from the quality-assurance skill) | standard, deep | `draft.md` | the claim ledger, plus the number ledger (or NONE) when load-bearing numbers carry the conclusion | the quality-assurance skill's `templates/fact-check-ledger.md` |
| **Devil's Advocate** (borrowed from the quality-assurance skill) | deep; standard when contested | `draft.md` | the objection set | the quality-assurance skill's `templates/critique-ledger.md` (the objection set) |
| **Compliance Officer** (borrowed from the legal-and-compliance skill) | sensitive or external-facing output | the draft and its intended audience and channel | the exposure ledger: BLOCK / REVISE / CLEAR per exposure | the ledger shape below (inline) |
| **Editor** (borrowed from the public-relations skill) | by demand, when a report file ships and the lead hands over the prose polish | the verified report | the polished prose, substance untouched, with an edit note | inline |

## Verdict vocabularies (so the lead applies a return mechanically)

- **The lead, on the source strategy:** APPROVE (fan out) / REVISE (back to the All-Source Analyst's strategy pass once with the named fix; a second REVISE proceeds with the gap logged as a coverage limitation).
- **Fact-Checker, claims:** SUPPORTED / WEAK-BASIS / UNSUPPORTED / NEEDS-CITATION / CONTRADICTED. Apply: keep / soften to the confidence the source supports / cut or source / add the citation / reverse or cut the claim (CONTRADICTED, the source says the opposite).
- **Fact-Checker, load-bearing numbers:** SUPPORTED / UNSUPPORTED-NUMBER / NOT-COMPARABLE / OVERSTATED, or NONE when the draft carries no load-bearing numbers. Apply: keep / source or cut / recompute on a common basis / soften.
- **Devil's Advocate:** FATAL / MATERIAL / MINOR. Respond to every FATAL and MATERIAL: accept (adjust the conclusion) or rebut (with the citation that settles it); MINOR is noted.
- **Compliance Officer:** BLOCK (do not ship) / REVISE (the named change) / CLEAR.

The quality-assurance skill's `references/verification.md` is the canonical statement of how a borrower applies its seats' verdicts; these lines restate it for the research draft.

## The Compliance Officer's exposure ledger (its inline shape)

A by-demand seat with no template here; it returns one row per exposure: `exposure - the specific rule it touches (libel, privacy, intellectual property and licensing, a regulated claim, a disclosure standard) - the concrete risk - disposition (BLOCK / REVISE / CLEAR) - the required change or the escalation`. It advises on risk, not law: anything that needs legal advice goes to the legal-and-compliance skill, which says when a licensed lawyer must review it.

## Blind pairing

The Fact-Checker (briefed to add its quantitative review when the draft carries load-bearing numbers) and the Devil's Advocate are dispatched in one message, each reading only `draft.md`, never the lead's reasoning or each other's return. The rule and its rationale live in `research-dispatch.md`.
