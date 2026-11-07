# Defect [ID]: [one-line summary]

<!-- The seat that found the failure returns the first half of this (most often the QA Test Engineer, one per
     failure); the Head of Quality adds the class, the root cause and the actions (references/defects.md). A finding
     in another seat's vocabulary is logged here at its severity by the crosswalk in references/defects.md. The skill
     keeps it in the venture's defect log, where the repository's instructions keep it. Fill every field, writing
     "none" rather than leaving one empty. Never copy personal data into a report: cite where it lives. -->

| Field         | Value                                                                                   |
| :------------ | :-------------------------------------------------------------------------------------- |
| Found in      | [the deliverable and its version]                                                       |
| Found by      | [the seat, and the borrowing skill if it was a borrowed run; or the user's report, through the customer-experience skill] |
| Finding       | [the seat's own verdict: FAIL, NEEDS-FIX, CONTRADICTED, NOT-COMPARABLE, FATAL, a failed accessibility gate, ...] |
| Clause broken | [the standard's clause, quoted]                                                         |
| Severity      | [critical / major / minor / trivial]                                                    |
| Priority      | [set by the owning department]                                                          |
| Status        | [new / confirmed / unconfirmed anomaly / fixed / verified closed]                       |

## Reproduce

1. [step]
2. [step]

- Expected: [what the clause requires]
- Actual: [what happened]
- Environment: [where, which version, which data]
- Reproduced: [n of m attempts]

## Class

[The kind of defect, and where else the class was searched for and found or not found.]

## Root cause

[The why-chain, ending at a cause the owning department controls, and the prediction that tested it.]

## Corrective action (this instance)

[What the author fixes, the owner, the date; the fix is checked again, fresh, on this item and every line it touched.]

## Preventive action (the class)

[What stops the class from recurring (a step, a check in the definition of done or in the borrower's brief, an
upstream validation), the owner, the date.]

## Closing check

[How and when the preventive action is shown to work: the class does not recur across the next set of deliverables of
that kind, measured.]
