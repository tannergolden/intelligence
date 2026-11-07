# Test plan: [release, launch or set of deliverables]

<!-- The QA Test Engineer drafts a test plan in this shape and the Head of Quality approves it; the skill keeps it in
     the venture's Quality Assurance records, where the repository's instructions keep them. Fill every field, writing
     "none" rather than leaving one empty. A requirement with no testable criterion goes back to its owner; it is
     never guessed at. -->

| Field           | Value                                                     |
| :-------------- | :-------------------------------------------------------- |
| Work under test | [the deliverables and their versions]                     |
| Owner of work   | [the department and seat that made it]                    |
| Standard        | [the written standard and the acceptance criteria]        |
| Approved by     | [the Head of Quality, date; never the plan's author]      |

## Scope

- In: [what is tested]
- Out: [what is not tested, and why; named, never silent]

## Traceability

| Requirement or criterion | Check                    | Case type                                        | Slice / run by | Result            |
| :----------------------- | :----------------------- | :----------------------------------------------- | :------------- | :---------------- |
| [R-1, quoted]            | [the observable check]   | [main path / edge / boundary / negative / error] | [slice 1]      | [pass / fail / -] |

## Environment and data

[Where the checks run, the version of the work, the sample data, and how personal data in a sample is handled
(cited by where it lives, never copied).]

## Entry criteria

[What must be true before testing starts: the work is complete enough, the definition of done is agreed, the inputs
exist.]

## Exit criteria

[What must be true to stop testing and rule: every check run or its blocker named, every failure reproduced or logged
as an anomaly, no open critical or major defect.]

## Slices

[How the checks split into independent slices that run in parallel, blind to each other, and who runs each.]

## Risks to the test

[What could make the results misleading: an environment unlike the real one, missing data, a requirement read two
ways.]
