# Deliverables - what the Quality Assurance (QA) team produces

What the department produces for a company or venture the user runs: each deliverable, the seat that produces it, what calls for it, the evidence that it is done, and where it goes. Read it before framing a standard or deep run. The team's main product is the verdict on other departments' work; its own deliverables are verified too, by the seat that did not author them.

## Where the work goes

The team's own records land in the venture's **Quality Assurance records**, wherever the repository's instructions keep a venture's department records (a department folder inside the venture's record, a repository of its own, or a location they name). With no such instruction, they are returned in the conversation, and a file is written only where the user asks.

A verification report has two homes. It **travels with the deliverable it judged**: the caller (the board skill, or the department skill that asked) persists the deliverable and its report together, in its own records. When the quality skill runs on its own, it also keeps the report in the venture's verification record, where the repository's instructions allow.

The department keeps four standing assets, updated rather than re-created run to run:

- **The quality standards and definitions of done** - the bar each kind of deliverable is judged against, owned with the department that makes it.
- **The test strategy and plans** - what is tested, how, by whom, and when the testing is done.
- **The verification record** - every verdict on file, so a pass can be reproduced and a recurring failure seen.
- **The defect log** - every defect and anomaly, its class, its root cause and its corrective and preventive actions.

## The deliverables

### Verification report - ★ Head of Quality

- **Trigger:** every consequential deliverable (load-bearing, external or irreversible) before it lands, whichever department made it; any work the user asks to have checked.
- **Done when:** the verdict is one of the four (`verification.md`); every definition-of-done condition is marked met or unmet with the evidence checked, not a general thumbs-up; the load-bearing numbers and claims traced are named with their sources, and anything that did not trace is named too; each defect is stated specifically enough for its producer to act on, by class, with the clause it breaks and its severity; noted defects are listed to travel with a pass; any escalation names what rose and whether it touches a gated act; the verifier did not make the work and never saw the author's reasoning; and the verdict is on record with the caller before the deliverable is written, so a FAIL is never written.
- **Needs from other departments:** the deliverable, the brief it was made against, its definition of done and its completion evidence, all from the department that made it.
- **Shape:** `templates/verification-report.md`.

### Quality standard, definition of done or quality management plan - ★ Head of Quality, with the owning department's lead

- **Trigger:** a deliverable that arrives with no definition of done, a new kind of deliverable, a recurring defect class, a stage change.
- **Done when:** every clause is testable (an observable check a stranger could run, with its pass condition); each clause names what it protects; the owning department's lead agrees it is the bar; the QA Test Engineer has checked every clause for testability; a standard the whole company will hold itself to is accepted by the user.
- **Needs from other departments:** the owning department's knowledge of the work; a metric's definition from the analytics skill when a clause measures one.

### Test plan - QA Test Engineer

- **Trigger:** a release or launch, a batch of deliverables, a process change to prove before it goes live.
- **Done when:** every requirement or acceptance criterion maps to at least one check (the traceability matrix); the checks include edge, boundary, negative and error-path cases, not only the main path; the entry and exit criteria are stated; the environment and data are named; what is out of scope is named, not silent; the Head of Quality has approved it.
- **Needs from other departments:** the requirements and acceptance criteria, from the department that owns the work. A requirement with no testable criterion is returned to its owner.
- **Shape:** `templates/test-plan.md`.

### Test results and defect reports - QA Test Engineer

- **Trigger:** each run of a test plan or a verification's checks.
- **Done when:** pass or fail is given per criterion, against its clause; every defect is reproducible (steps, expected and actual, environment) with a severity read; an anomaly that did not reproduce is reported as one; the unverified scope and its blocker are named.
- **Shape:** `templates/defect-report.md`, one per defect.

### Root cause and corrective action - ★ Head of Quality, with the QA Test Engineer reproducing

- **Trigger:** a major or critical defect, a recurring class, a defect a user reports through the customers skill.
- **Done when:** the defect is reproduced or logged as an unconfirmed anomaly; its class is named and searched for beyond the one instance; the root cause is traced to a cause the owning department controls and tested against a prediction; the corrective and the preventive action each have an owner in that department and a date; the closing check is defined (`defects.md`).
- **Needs from other departments:** the owning department's process and records; the customers skill's report of the user's experience.

### Audit or assessment report - ★ Head of Quality

- **Trigger:** a review cycle, a stage change, a pattern of failures, a request from a customer or a regulator.
- **Done when:** the scope and the standard audited against are named; every finding cites its evidence and the clause; findings are graded by severity; each feeds a corrective action with an owner; sending the report outside the company is listed as the user's gated act.

## The producing chain

- **The definition of done comes first.** Nothing is graded before its bar exists; a deliverable that arrives without one goes back to its owner first.
- **Requirements before tests.** In the product chain (evidence, requirements, design, build, release), the test plan and its traceability matrix come last and can only test what the requirements defined: an untestable requirement is returned to its owner, never guessed at.
- **Inputs were real, not assumed.** Every chain ends here: the verifier checks that a deliverable's upstream inputs existed and were current when it was made, and a deliverable built on an assumed input fails on that alone.
- **The fix belongs to the maker.** A root cause in another department's process goes to that department as a corrective action; quality verifies the fix and never makes it.

## Stage scales the slice

When the board skill's record names the venture's stage, scale the work to it:

- **found** (idea to seed): verify what is load-bearing or external (the numbers in a pitch, the first contracts' completeness, and above all whether the metric that reads an experiment actually measures its hypothesis rather than the founder's hope). No standards library yet.
- **scale** (Series A to C): a definition of done for each recurring kind of deliverable, test plans for releases, a defect log with root causes.
- **maintain** (established to mature): audits on a cadence, recurring classes prevented at their cause, standards reviewed as the work changes.
