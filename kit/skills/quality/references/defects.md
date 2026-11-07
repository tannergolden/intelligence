# Defects - triage, root cause, and the fix that stops the class

How the team handles a defect, from the first report to the check that its class is gone. Read it before triaging a defect or tracing a root cause. The rule above all: **prevent over detect**. Finding defects one at a time is the cost of a quality system that is not working; tracing each to its cause and closing the cause is the point of one.

## Where defects come from

- **Verification:** a QA Test Engineer run or a Head of Quality verdict finds a condition unmet.
- **Users and customers:** a defect a user reports arrives through the customers skill, which owns the reply, the customer and the support ticket; quality takes the defect itself, reproduces it and traces its class.
- **The departments themselves:** a department that finds a recurring failure in its own work asks for a root cause.

Each is logged the same way (`templates/defect-report.md`), whatever its source.

## Triage

1. **Reproduce first.** Confirm the failure repeats and capture the exact steps, the expected and the actual result, the environment and the version. A failure that does not reproduce is logged as an **unconfirmed anomaly**, with what was observed, and is never reported as a confirmed defect or quietly dropped.
2. **Name the clause.** Every defect is a failure against a written standard or a definition of done, cited by clause. A failure no clause covers is a gap in the standard, escalated to the owning department's lead to define, not a defect graded against a rule made up for the case.
3. **Grade the severity,** by the harm if the work landed as it is:

| Severity | Meaning | Effect on the verdict |
|----------|---------|-----------------------|
| **Critical** | the work would cause harm or loss, a legal or safety exposure, a wrong external statement, or an irreversible act nobody flagged | FAIL, or ESCALATE when it rises above the deliverable |
| **Major** | a load-bearing requirement unmet, or a number or claim that does not trace | FAIL |
| **Minor** | a real defect with no load-bearing effect, or with a stated workaround | PASS WITH NOTED DEFECTS at most; the defect travels with the work |
| **Trivial** | cosmetic | noted; never blocks |

4. **Set the priority separately.** Severity is how bad the defect is; priority is how soon it is fixed, which the owning department sets against its own deadlines. A minor defect on a launch page may be urgent; a major one in a report due next quarter may wait for its fix, but it still does not land.
5. **Name the class.** Ask what kind of defect this is, not only where it is: an untraced number, a missing exception path, a placeholder left in, a definition that drifted, a step nobody owns. Search for the rest of the class in the same deliverable and its siblings; one instance found is a sample, not the whole.

## Root cause

Trace each major or critical defect, and every recurring class, to a cause its owner controls:

- **Ask why until the answer is a process, not a person.** Five whys is a habit, not a quota (Ohno, *Toyota Production System*): stop at a cause that, once fixed, stops the class from recurring. "The analyst made a typo" is a symptom; "the model has no check that the statements tie before it ships" is a cause.
- **Look across the usual categories when the chain branches.** A cause-and-effect (Ishikawa) map sorts candidate causes into method, inputs, people and roles, tools, measurement and environment, so the investigation does not stop at the first plausible one.
- **Test the cause before naming it.** A named root cause predicts something checkable: where else the class should appear, or what should change once the cause is fixed. If the prediction fails, the cause is wrong.
- **The cause lives where the work is made.** A root cause in another department's process belongs to that department; quality names it and its evidence, and the owning lead takes the fix.

## Corrective and preventive action

Every major or critical defect closes with two actions, each with an owner in the department that made the work and a date:

- **Corrective action** fixes this instance: the deliverable is repaired by its author and verified again, fresh, on the cited items and every line the fix touched.
- **Preventive action** stops the class: a step added to the procedure, a check built into the definition of done, an input validated upstream, a standard clarified.
- **The closing check** says how and when the preventive action is shown to work: the class does not recur across the next set of deliverables of that kind, measured, not assumed.

A recurring class that survives its preventive action, or spans departments, is escalated to the board skill's ★ Chief Executive Officer as a systemic finding.

## What never happens

- The verifier never fixes the defect it found; the author does.
- A defect is never closed because the author disagrees; it closes when the evidence shows the work meets the clause.
- A defect report never leaves the company (to a vendor, a customer or a regulator) without the user's explicit confirmation.
- Personal data met while reproducing a defect is cited by where it lives, never copied into the report.
