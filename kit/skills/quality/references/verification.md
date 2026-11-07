# Verification - the independent check before a deliverable lands

The doctrine behind every verdict the Head of Quality gives, whoever asks for it: the board skill in a company-wide run, a department skill before it writes its own records, or the user directly. Read it before any verdict. The one standard, **no pass without evidence**, is what this file makes concrete.

## Why the verifier never made the work

A model that produces work and then checks its own work is worse off than one that does neither: the self-check launders a wrong answer into a confident one. The failure is fluency without grounds, and it is most dangerous exactly where a casual read misses it: a plausible but invented growth rate in a model, a clause that sounds standard but is not, a metric stated to two decimals with no source behind it. The context that produced an error is the worst place to catch it from, so the discipline is structural, not exhortative:

- **The verifier did not make the work and never helped make it.** A seat that drafted, shaped or approved the deliverable on the way never rules on it.
- **The verifier never sits in the author's seat.** It receives the deliverable, the brief it was made against, the definition of done, the completion evidence and the cited sources, in a fresh context; never the author's reasoning, notes or drafts, which carry the frame that produced the error.
- **The verifier cites; the author fixes.** Rewriting the work to make it pass turns the verifier into a second author and leaves nobody independent. A defect goes back with its evidence; the fix is verified like new work.
- **No co-signing.** A verdict is never softened because the author is senior, the deadline is close or the requester hopes for a pass. Pressure for a verdict is recorded as a fact about the request and changes nothing in the verdict.

## What counts as consequential

Verification costs tokens and time, so it is spent where a wrong deliverable does damage. A deliverable is **consequential**, and is verified before it lands, if it is any of these:

- **Load-bearing:** other work or decisions will rely on it: a model a budget ladders up to, a metric definition a dashboard reads, a spec a build follows, a procedure people will run, a pay band offers are drawn from.
- **External:** it leaves the company or will be read as the company's word: a press release, a customer-facing page, a proposal, an investor update, a contract or a filing.
- **Irreversible:** persisting or acting on it commits something costly or impossible to take back: it moves money, signs or sends a contract, deletes a file, or changes equity.

When in doubt, it is consequential. A cheap internal draft that is none of these (a working outline, a scratch list) gets its producing lead's own review, and the department's skill may keep it without a verdict.

## No definition of done, no verdict

A deliverable does not arrive as done; it arrives with the evidence that it is done, and the verifier checks the evidence, not the claim. The bar is the deliverable's **definition of done**: the concrete, checkable conditions it must meet, which each department's `references/deliverables.md` (or the board skill's catalog, in a board run) sets for its own deliverables. A brief with no definition of done is itself the first finding: it goes back to the owning department's lead to define done before anything is graded, and the Head of Quality may draft one with that lead. The verifier never invents the rule to fit the work in front of it.

## Completion evidence, by kind of deliverable

The evidence is specific to the artifact and stated in checkable terms:

- **A financial model:** the statements tie out (the balance sheet balances, cash agrees across statements, net income flows to retained earnings); every assumption is labeled with its source; the scenarios are present, labeled and internally consistent.
- **A metric definition:** the formula is explicit; each input names its source system; the definition is the only one of its metric; a cited benchmark names its origin and vintage.
- **A contract or a policy:** every required clause from the playbook is present; party names and entities match the venture's record; no placeholder or bracketed term survives; any non-standard term is flagged, not buried. Whether a clause is sound law is the legal skill's call, not the verifier's.
- **An SOP or runbook:** every step is executable as written; the RACI names real owners; the exception and rollback paths exist.
- **A program plan:** the outcome has a done-test; every deliverable has an owner and a date; the critical path is named; the status matches the path.
- **A vendor selection:** the requirement predates the choice; the total-cost basis is shown with its sources; single-source exposure is named.
- **A go-to-market or brand piece:** the positioning matches the strategy on file; every claim is supportable; nothing contradicts a published artifact of the venture's.

## Ground every number and claim

Every number, named fact and external claim in a consequential deliverable traces to a tool call, a venture record or a cited source; nothing load-bearing rests on recall. In practice:

- **The venture's figures trace to the venture.** Revenue, runway, headcount and customer counts come from the venture's own records or a system of record read at run time, never from a guess or a remembered earlier run.
- **Benchmarks name their source and vintage,** so a current number is not judged against a remembered old band.
- **Computed numbers are recomputed, not recalled.** A ratio, a total, a growth rate or a projection is arithmetic the verifier redoes from the inputs; with the inputs missing, the number is unverified.
- **External facts carry a citation,** and the verifier checks that the cited source says what the deliverable claims. A fact that is contested or turns on events after the model's knowledge goes to the research skill, whose Fact-Checker establishes it; the verifier never asserts it.

Financial and legal output gets default suspicion: a number is assumed invented until its source is shown, and a clause non-standard until the playbook confirms it.

## The four verdicts

| Verdict | When | What happens next |
|---------|------|-------------------|
| **PASS** | every definition-of-done condition met, every load-bearing number traced, no material defect | the deliverable goes on to the write-gate; an external or irreversible act it enables still waits for the user |
| **PASS WITH NOTED DEFECTS** | sound, with known gaps, stated assumptions or open questions a reader must see | it goes on, and the noted defects travel with it into the record and the delivery; it is never silently upgraded to a clean pass |
| **FAIL** | a condition unmet, a number that does not trace, an unsupported claim, an internal contradiction, a critical or major defect | it goes back to its producer through whoever asked, with each defect cited; it does not land as it stands, and the fix is verified again |
| **ESCALATE** | something above the deliverable: a contradiction with the venture's own record, a material risk, an irreversible act the brief assumed but never flagged, a systemic defect class, a standard silent on the case | it goes to the user, or in a board run to the board skill, with what rose and why |

A caller's records may name these cleared, cleared with noted defects, returned and escalated; the meaning is the same.

## The anti-self-deception battery

Run on every consequential deliverable, aimed at the ways produced work flatters itself:

1. **Does it answer the brief?** Compare it to the brief it was made against, not to a nearby question it answers well. A polished answer to the wrong question is a defect.
2. **Trace three numbers at random.** Follow each load-bearing figure to its source. If one does not trace, trace them all.
3. **Find the seam the author skated over.** The assumption with no basis, the edge case the procedure ignores, the clause quietly softened, the cohort the model excludes. Name it.
4. **Read it as the person who acts on it.** The customer, the counterparty, the operator on the night shift, the engineer who builds from it: what goes wrong when they rely on it?
5. **Check it against the venture's own record.** A new number that contradicts the books, a positioning that contradicts the strategy, a claim that contradicts the log is resolved before the deliverable lands.
6. **Check nothing was bent toward a wished-for answer.** A result suspiciously close to what someone hoped for gets its assumptions checked for having been chosen to get there.

## Verification is not authorization

A verdict clears quality; it never authorizes an act. A press release can be verified line by line and still does not go out without the user's explicit confirmation, because sending it is irreversible. Moving money, signing or sending a contract, sending anything outside the company, deleting a file, changing equity and sharing personal data stop at the user however clean the verdict. When the deliverable enables such an act, the verdict says so, so the user confirms with the consequence in view.

## What the verifier returns

The verdict is itself a checkable artifact, in the `templates/verification-report.md` shape:

1. **The verdict,** one of the four, with one line on why.
2. **The definition-of-done check:** each condition marked met or unmet, with the evidence checked.
3. **The grounding check:** which numbers and claims were traced or recomputed, to what, and anything that did not trace.
4. **The defects:** each stated specifically enough for its producer to act on, by class, with the clause it breaks and its severity (`defects.md`), and the noted defects that travel with a pass.
5. **The escalation, if any:** what rose above the deliverable, to whom, and whether it touches a gated act.
