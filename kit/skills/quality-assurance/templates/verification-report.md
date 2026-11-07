# Verification report: [deliverable]

<!-- The Head of Quality returns a verdict in this shape (references/verification.md). The caller persists it with the
     work it judged; when the quality-assurance skill runs on its own, it also keeps it in the venture's verification
     record, where the repository's instructions allow, and a check of the user's own document stays in the
     conversation unless a private repository made to hold it says otherwise. Fill every field, writing "none" rather
     than leaving one empty. Name the evidence actually checked, never a general thumbs-up. -->

| Field        | Value                                                                                           |
| :----------- | :---------------------------------------------------------------------------------------------- |
| Deliverable  | [the named artifact and its version]                                                            |
| Made by      | [the department and seat that made it, or the user; never the verifier]                         |
| Requested by | [the administration skill, the [name] skill, or the user]                                        |
| Standard     | [the written standard and the definition of done it was judged against; for the user's own document, the requirements it must meet and where they come from] |
| Stakes       | [load-bearing, external, irreversible]                                                          |
| Verifier     | the quality-assurance skill's ★ Head of Quality, in a context that did not make the work and never saw how it was made |
| Date         | [YYYY-MM-DD]                                                                                    |

## Verdict

**[PASS | PASS WITH NOTED DEFECTS | FAIL | ESCALATE]** - [one line on why]

## Definition-of-done check

| #   | Condition   | Met?       | Evidence checked                  |
| :-- | :---------- | :--------- | :-------------------------------- |
| 1   | [condition] | [yes / no] | [what was looked at, and where]   |

## Grounding check

| Number or claim | Traced to                          | Result                                  |
| :-------------- | :--------------------------------- | :-------------------------------------- |
| [figure]        | [source, record or recomputation]  | [traced / recomputed / did not trace]   |

## Seats' returns weighed

| Seat               | Ran on                     | Its verdicts, in its own vocabulary                              | How it was weighed                    |
| :----------------- | :------------------------- | :--------------------------------------------------------------- | :------------------------------------ |
| [QA Test Engineer] | [the criteria or the build] | [n PASS, n NEEDS-FIX, n FAIL]                                    | [which clause each finding touches]   |
| [Fact-Checker]     | [the claims and numbers]   | [n SUPPORTED, n WEAK-BASIS, ... / NONE; or SHIP, REVISE, HOLD]  | [...]                                 |
| [Devil's Advocate] | [the conclusion]           | [n FATAL, n MATERIAL, n MINOR; which stand]                      | [...]                                 |
| [Design Critic]    | [each visual]              | [SHIP or HOLD; accessibility gate PASS or FAIL]                  | [...]                                 |

## Defects

| ID     | Severity                             | Class   | Clause broken | Found by | Evidence (steps, expected and actual) | Fix owner |
| :----- | :----------------------------------- | :------ | :------------ | :------- | :------------------------------------ | :-------- |
| [D-1]  | [critical / major / minor / trivial] | [class] | [clause]      | [seat]   | [...]                                 | [role]    |

## Noted defects that travel with it

[The gaps, assumptions and open questions a reader must see with a PASS WITH NOTED DEFECTS. "None" if clean.]

## Escalation

[What rose above the work, to whom it goes, and whether it touches a gated act. "None" if none.]

## Gated act it enables

[None; or the act (a payment, a signature, a send or a submission outside the company, a delete, an equity change),
and that it still waits for the user's explicit confirmation: a pass clears quality, never authority.]
