# Test results: [work under test, version]

<!-- The QA Test Engineer RETURNS this (it persists nothing). It is blind: it never sees the author's or the builder's
     reasoning. The caller applies each verdict (references/verification.md): PASS stands; NEEDS-FIX goes back to the
     author on the cited item and is checked again before the work ships; FAIL blocks the ship and goes back with its
     repro. Fill every field, writing "none" rather than leaving one empty. Shape matches its Output contract. -->

| Field            | Value                                                                            |
| :--------------- | :------------------------------------------------------------------------------- |
| Work under test  | [the deliverable, or the software, skill or agent build, and its version]        |
| Made by          | [the department and seat that made it; never the tester]                         |
| Requested by     | [the Head of Quality, the research-and-development skill, the [name] skill, or the user] |
| Standard         | [the written standard, the acceptance criteria, or the locked requirements]      |
| Environment      | [where it ran, which version, which data]                                        |

## Automated checks (a build)

| Check                      | Command or suite run | Result                                  |
| :------------------------- | :------------------- | :-------------------------------------- |
| [the deterministic validator] | [as the brief names it] | [n errors, n warnings; the errors quoted] |
| [the test suite]           | [...]                | [n passed, n failed; the failures named] |

## Verdict per criterion

| #   | Criterion or requirement, quoted | Check run                    | Case types covered                              | Verdict                    | Repro, for every non-PASS          | Prescribed fix (the smallest) |
| :-- | :------------------------------- | :--------------------------- | :---------------------------------------------- | :------------------------- | :--------------------------------- | :---------------------------- |
| 1   | [R-1]                            | [the observable check]       | [main / edge / boundary / negative / error / adversarial] | [PASS / NEEDS-FIX / FAIL] | [steps; expected and actual]       | [the fix; never applied]      |

## Defects

[One line each: ID, severity (critical / major / minor / trivial), the clause, and a pointer to its
`templates/defect-report.md` entry when the Head of Quality keeps the log. "None" if clean.]

## Unconfirmed anomalies

[What was observed once and did not reproduce, with the attempts made. "None" if none.]

## Unverified scope

[What could not be tested, and the blocker (a build that would not run, a missing environment, a missing criterion).
Never silent, never passed.]

## Standard gaps routed up

[Each case the written standard is silent on, sent to the Head of Quality to define. "None" if none.]
