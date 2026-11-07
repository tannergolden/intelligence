# Verification - the independent check before work goes out

The doctrine behind every verdict the team gives, whoever asks for it: the administration skill in a company-wide run, a department skill before it writes its own records or borrows a seat, or the user directly, about a company they run or about their own life. Read it before any verdict. The one standard, **no pass without evidence**, is what this file makes concrete.

## Why the verifier never made the work

A model that produces work and then checks its own work is worse off than one that does neither: the self-check launders a wrong answer into a confident one. The failure is fluency without grounds, and it is most dangerous exactly where a casual read misses it: a plausible but invented growth rate in a model, a clause that sounds standard but is not, a metric stated to two decimals with no source behind it, a chart whose axis quietly starts at 90. The context that produced an error is the worst place to catch it from, so the discipline is structural, not exhortative:

- **The verdict comes from a seat that did not make the work and never helped make it.** A seat that drafted, shaped or approved the work on the way never rules on it; this holds for every seat on the team, and for every borrowed run.
- **No seat sits in the author's seat.** Each receives the work, the brief it was made against, the standard or definition of done, the completion evidence and the cited sources, in a fresh context; never the author's reasoning, notes or drafts, which carry the frame that produced the error.
- **Seats checked together stay blind to each other.** The Fact-Checker never sees the Devil's Advocate's return and the reverse; a seat that has read another's finding checks toward it.
- **The verifier cites; the author fixes.** Rewriting the work to make it pass turns the verifier into a second author and leaves nobody independent. A defect goes back with its evidence; the fix is checked like new work.
- **No co-signing.** A verdict is never softened because the author is senior, the deadline is close or the requester hopes for a pass. Pressure for a verdict is recorded as a fact about the request and changes nothing in the verdict.

## What counts as consequential

Verification costs tokens and time, so it is spent where wrong work does damage. Work is **consequential**, and is checked before it lands or goes out, if it is any of these:

- **Load-bearing:** other work or decisions will rely on it: a model a budget ladders up to, a metric definition a dashboard reads, a spec a build follows, a procedure people will run, a pay band offers are drawn from, a plan the user will act on.
- **External:** it leaves the company or the user's hands, or will be read as their word: a press release, a customer-facing page, a proposal, an investor update, a contract or a filing; for the user's own life, a job, school, grant, visa or loan application, a public post or a speech.
- **Irreversible:** persisting or acting on it commits something costly or impossible to take back: it moves money, signs or sends a contract, submits an application, deletes a file, or changes equity.

When in doubt, it is consequential. A cheap internal draft that is none of these (a working outline, a scratch list) gets its producing lead's own review, and the department's skill may keep it without a verdict.

## No definition of done, no verdict

Work does not arrive as done; it arrives with the evidence that it is done, and the verifier checks the evidence, not the claim. The bar is the work's **definition of done**: the concrete, checkable conditions it must meet, which each department's `references/deliverables.md` (or the administration skill's catalog, in an administration run) sets for its own deliverables. A brief with no definition of done is itself the first finding: it goes back to the owning department's lead to define done before anything is graded, and the Head of Quality may draft one with that lead. For the user's own document, the standard is the requirements it must meet: the form's own instructions, the posting's requirements, the program's published rules, read at their source. The verifier never invents the rule to fit the work in front of it.

## Completion evidence, by kind of work

The evidence is specific to the artifact and stated in checkable terms:

- **A financial model:** the statements tie out (the balance sheet balances, cash agrees across statements, net income flows to retained earnings); every assumption is labeled with its source; the scenarios are present, labeled and each flexes its own drivers (the Fact-Checker's plan review, `fact-checking.md`).
- **A metric definition:** the formula is explicit; each input names its source system; the definition is the only one of its metric; a cited benchmark names its origin and vintage.
- **A contract or a policy:** every required clause from the playbook is present; party names and entities match the venture's record; no placeholder or bracketed term survives; any non-standard term is flagged, not buried. Whether a clause is sound law is the legal-and-compliance skill's call, not the verifier's.
- **An SOP or runbook:** every step is executable as written; the RACI names real owners; the exception and rollback paths exist.
- **A program plan:** the outcome has a done-test; every deliverable has an owner and a date; the critical path is named; the status matches the path.
- **A vendor selection:** the requirement predates the choice; the total-cost basis is shown with its sources; single-source exposure is named.
- **A go-to-market or brand piece:** the positioning matches the strategy on file; every claim is supportable (the Fact-Checker); nothing contradicts a published artifact of the venture's.
- **A software, skill or agent build:** every locked requirement maps to a check that passed; the deterministic validator and the test suite ran clean; the adversarial and edge cases held (the QA Test Engineer); its security review is the information-technology skill's.
- **A chart, diagram or dashboard:** the form fits the question; the encoding is honest; the accessibility gate passed (the Design Critic, `critique.md`).
- **The user's own application or form:** every required field and attachment is present; every fact and date matches the user's own documents; every requirement in the instructions is met; nothing contradicts another part of the submission; the deadline and the submission route are stated.

## Ground every number and claim

Every number, named fact and external claim in consequential work traces to a tool call, a record or a cited source; nothing load-bearing rests on recall. In practice:

- **The venture's figures trace to the venture.** Revenue, runway, headcount and customer counts come from the venture's own records or a system of record read at run time, never from a guess or a remembered earlier run. The user's own figures trace to the user's own documents.
- **Benchmarks name their source and vintage,** so a current number is not judged against a remembered old band.
- **Computed numbers are recomputed, not recalled.** A ratio, a total, a growth rate or a projection is arithmetic the verifier redoes from the inputs; with the inputs missing, the number is unverified.
- **External facts carry a citation,** and the Fact-Checker checks that the cited source says what the work claims, at the primary source. A current figure (a tax limit, a rate, a program rule, a deadline) is checked at its official source for the right year and jurisdiction. An open evidence question beyond checking a cited claim goes to the research-and-development skill; the verifier never asserts the answer.

Financial and legal output gets default suspicion: a number is assumed invented until its source is shown, and a clause non-standard until the playbook confirms it.

## The four verdicts

The Head of Quality rules on a whole deliverable with one of four verdicts:

| Verdict | When | What happens next |
|---------|------|-------------------|
| **PASS** | every definition-of-done condition met, every load-bearing number traced, no material defect | the work goes on to the write-gate; an external or irreversible act it enables still waits for the user |
| **PASS WITH NOTED DEFECTS** | sound, with known gaps, stated assumptions or open questions a reader must see | it goes on, and the noted defects travel with it into the record and the delivery; it is never silently upgraded to a clean pass |
| **FAIL** | a condition unmet, a number that does not trace, an unsupported claim, an internal contradiction, a critical or major defect | it goes back to its producer through whoever asked, with each defect cited; it does not land as it stands, and the fix is checked again |
| **ESCALATE** | something above the work: a contradiction with the venture's own record, a material risk, an irreversible act the brief assumed but never flagged, a systemic defect class, a standard silent on the case | it goes to the user, or in an administration run to the administration skill, with what rose and why |

A caller's records may name these cleared, cleared with noted defects, returned and escalated; the meaning is the same.

## Every seat's verdict, and how its caller applies it

Each specialist returns its own ledger in its own vocabulary. A borrowing skill applies the ledger mechanically, by the rule in the third column; in a verify run the Head of Quality weighs it as evidence, by the rule in the fourth. A seat's return is never the Head of Quality's verdict by itself.

| Seat and ledger | Its verdicts | How the caller applies them | In the Head of Quality's verdict |
|-----------------|--------------|-----------------------------|----------------------------------|
| **QA Test Engineer**, test results (`templates/test-results.md`) | per criterion PASS / NEEDS-FIX / FAIL; each defect critical, major, minor or trivial | PASS stands; NEEDS-FIX goes back to the author on the cited item and is checked again before the work ships; FAIL blocks the ship and goes back with its repro | any FAIL fails the work; an open NEEDS-FIX allows PASS WITH NOTED DEFECTS at most |
| **Fact-Checker**, claim ledger (`templates/fact-check-ledger.md`) | SUPPORTED / WEAK-BASIS / UNSUPPORTED / NEEDS-CITATION / CONTRADICTED | keep / soften to the confidence the source supports / cut or source / add the citation / reverse or cut the claim | an UNSUPPORTED or CONTRADICTED load-bearing claim fails the work; a WEAK-BASIS or NEEDS-CITATION one fails it until fixed when the conclusion rests on it, and is otherwise a noted defect |
| **Fact-Checker**, number ledger (same template), or NONE | SUPPORTED / UNSUPPORTED-NUMBER / NOT-COMPARABLE / OVERSTATED | keep / source or cut / recompute on a common basis / soften | an UNSUPPORTED-NUMBER or NOT-COMPARABLE load-bearing figure fails the work; OVERSTATED fails it when the conclusion rests on it |
| **Fact-Checker**, plan review ledger (`templates/plan-review.md`) | findings FATAL / MATERIAL / MINOR; one verdict SHIP / REVISE / HOLD | SHIP may be recorded; REVISE is recorded only once every MATERIAL finding is applied; HOLD is fixed and reviewed again, and a FATAL that survives two rounds goes to the user as an open question, never recorded | HOLD fails the work; REVISE fails it until applied; SHIP with MINOR notes allows PASS or PASS WITH NOTED DEFECTS |
| **Devil's Advocate**, objection set (`templates/critique-ledger.md`) | FATAL / MATERIAL / MINOR; each stands or is answered | respond to every FATAL and MATERIAL: accept (change the conclusion) or rebut with the citation that settles it; MINOR is noted | a FATAL that stands fails the work, or escalates it when it attacks the frame of a company-level decision; a MATERIAL that stands fails it until addressed |
| **Devil's Advocate**, idea verdict ledger (same template) | KEEP / FLAW / KILL; evolution potential high or low | KEEP enters the ranking; FLAW goes to the research-and-development skill's Idea Generator to evolve on the named flaw, then re-enters; KILL leaves the pool and stays recorded as killed, so it is never re-trodden | ideas are options, not deliverables: they are not given one of the four verdicts |
| **Design Critic**, design review (`templates/design-review.md`) | issues FATAL / MATERIAL / MINOR; accessibility gate PASS / FAIL; one call SHIP / HOLD | SHIP may render or be saved; HOLD goes back to the maker on the cited issues only, then a fresh re-review; a blocking issue that survives two rounds goes to the user | HOLD, or a failed accessibility gate, fails the work; SHIP with MINOR notes allows PASS or PASS WITH NOTED DEFECTS |

Every seat's finding also carries over into the defect log by the crosswalk in `defects.md`, so a class found in a borrowed run can be traced to its cause like any other.

## The anti-self-deception battery

Run on every consequential deliverable, aimed at the ways produced work flatters itself:

1. **Does it answer the brief?** Compare it to the brief it was made against, not to a nearby question it answers well. A polished answer to the wrong question is a defect.
2. **Trace three numbers at random.** Follow each load-bearing figure to its source. If one does not trace, trace them all.
3. **Find the seam the author skated over.** The assumption with no basis, the edge case the procedure ignores, the clause quietly softened, the cohort the model excludes. Name it.
4. **Read it as the person who acts on it.** The customer, the counterparty, the operator on the night shift, the engineer who builds from it, the admissions reader or the visa officer: what goes wrong when they rely on it?
5. **Check it against the record.** A new number that contradicts the books, a positioning that contradicts the strategy, a date that contradicts the user's own documents is resolved before the work lands.
6. **Check nothing was bent toward a wished-for answer.** A result suspiciously close to what someone hoped for gets its assumptions checked for having been chosen to get there.

## Verification is not authorization

A verdict clears quality; it never authorizes an act. A press release can be verified line by line and still does not go out without the user's explicit confirmation, because sending it is irreversible; an application can pass every check and the user still submits it. Moving money, signing or sending a contract, sending or submitting anything outside the company, deleting a file, changing equity and sharing personal data stop at the user however clean the verdict. When the work enables such an act, the verdict says so, so the user confirms with the consequence in view.

## What the verifier returns

The verdict is itself a checkable artifact, in the `templates/verification-report.md` shape:

1. **The verdict,** one of the four, with one line on why.
2. **The definition-of-done check:** each condition marked met or unmet, with the evidence checked.
3. **The grounding check:** which numbers and claims were traced or recomputed, to what, and anything that did not trace.
4. **The seats' returns:** which seats ran, each one's verdicts in its own vocabulary, and how each was weighed.
5. **The defects:** each stated specifically enough for its producer to act on, by class, with the clause it breaks and its severity (`defects.md`), and the noted defects that travel with a pass.
6. **The escalation, if any:** what rose above the work, to whom, and whether it touches a gated act.
