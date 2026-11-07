# Roster - the Research team wired to the pipeline

The contract that wires this skill to the standing Research team, whose specs ship in this skill's `agents/`. It is the single source of truth for who runs, on what, and what each one hands back; `dispatch.md` sets the per-tier order and the briefing shape.

**The return-based flow.** Every team agent **returns** its artifact as its final message and **persists nothing** (that is each spec's write-scope). The lead is the only one who writes a workspace file: `draft.md`, the synthesis the blind reviewers attack. So the lead collects the returns, writes `draft.md`, points the Fact-Checker and Devil's Advocate at it, and applies their returned ledgers. Never brief an agent to "write a file": that contradicts its spec and confuses it.

## Each agent: trigger, input, what it returns, and the template that shapes the return

| Agent (name) | Runs on | Input | Returns | Template |
|--------------|---------|-------|---------|----------|
| **Research Lead** | every run, as orchestrator; Step-0 before every non-quick run when the repository's instructions point to filed reports; the search approval on deep runs; the final polish when a report file ships | the user's verbatim question; the filed reports; the source strategy; the verified draft | the Step-0 verdict (canonical report reused, refreshed, or merged, or the gap); APPROVE or REVISE on the strategy; the findings-first answer, and `draft.md` for review; the polished report with an edit note | `reporting.md` Step-0 (inline); the chat shape in `reporting.md`; `report.md` when filed |
| **Information Specialist** | deep, before the fan-out | the lanes | the source strategy per lane with its self-check (sentinel check, coverage gaps, biased or low-recall queries) | `templates/source-strategy.md` |
| **All-Source Analyst** xN | standard, deep; one lane grounds locally first, only when the repository's instructions name a reference collection or offline knowledge base | one lane (the five lane fields); on the local-grounding lane, the collection's location and any search-command results the skill fetched | the lane findings brief; on the local-grounding lane, the holdings found, cited, the gaps, and any follow-up query for the skill to run | `templates/lane-brief.md` |
| **Fact-Checker** | standard, deep | `draft.md` | the claim ledger, plus the number ledger (or NONE) when load-bearing numbers carry the conclusion | `templates/verification.md` |
| **Devil's Advocate** | deep; standard when contested | `draft.md` | the objection set | `templates/critique.md` |
| **Standards Reviewer** | sensitive or external-facing output | the draft | the exposure ledger: BLOCK / REVISE / CLEAR per exposure | the ledger shape below (inline) |

## Verdict vocabularies (so the lead applies a return mechanically)

- **Research Lead, on the source strategy:** APPROVE (fan out) / REVISE (back to the Information Specialist once with the named fix; a second REVISE proceeds with the gap logged as a coverage limitation).
- **Fact-Checker, claims:** SUPPORTED / WEAK-BASIS / UNSUPPORTED / NEEDS-CITATION / CONTRADICTED. Apply: keep / soften to stated confidence / cut / add the citation / reverse the claim (CONTRADICTED, the source says the opposite).
- **Fact-Checker, load-bearing numbers:** SUPPORTED / UNSUPPORTED-NUMBER / NOT-COMPARABLE / OVERSTATED, or NONE when the draft carries no load-bearing numbers. Apply: keep / cut or source / recompute on a common basis / soften.
- **Devil's Advocate:** FATAL / MATERIAL / MINOR. Respond to every FATAL and MATERIAL: accept (adjust the conclusion) or rebut (with the citation that settles it).
- **Standards Reviewer:** BLOCK (do not ship) / REVISE (the named change) / CLEAR.

## The Standards Reviewer exposure ledger (its inline shape)

A by-demand seat with no template file; it returns one row per exposure: `exposure - the specific rule it touches - the concrete risk - disposition (BLOCK / REVISE / CLEAR) - the required change or the escalation`.

## Blind pairing

The Fact-Checker (briefed to add its quantitative review when the draft carries load-bearing numbers) and the Devil's Advocate are dispatched in one message, each reading only `draft.md`, never the lead's reasoning or each other's return. The rule and its rationale live in `dispatch.md`.
