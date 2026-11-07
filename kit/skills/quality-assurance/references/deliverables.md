# Deliverables - what the Quality Assurance (QA) team produces

What the department produces, for a company or venture the user runs and for the user's own life: each deliverable, the seat that produces it, what calls for it, the evidence that it is done, and where it goes. Read it before framing a standard or a deep run. The team's main product is the verdict on other work; its own deliverables are checked too, by the seat that did not author them.

## Where the work goes

The team's own records land in the venture's **Quality Assurance records**, wherever the repository's instructions keep a venture's department records (a department folder inside the venture's record, a repository of its own, or a location they name). With no such instruction, they are returned in the conversation, and a file is written only where the user asks. A check of the user's own document stays in the conversation unless a private repository made to hold the user's context says where it goes (the Constitution's SEC-003).

A verdict or a ledger has two homes. It **travels with the work it judged**: the caller (the administration skill, or the department skill that asked or borrowed the seat) persists the work and its report or ledger together, in its own records. When the quality-assurance skill runs on its own, it also keeps the report in the venture's verification record, where the repository's instructions allow.

The department keeps four standing assets, updated rather than re-created run to run:

- **The quality standards and definitions of done** - the bar each kind of deliverable is judged against, owned with the department that makes it.
- **The test strategy and plans** - what is tested, how, by whom, and when the testing is done.
- **The verification record** - every verdict and ledger on file from the department's own runs, so a pass can be reproduced and a recurring failure seen.
- **The defect log** - every defect and anomaly, whichever seat found it, its class, its root cause and its corrective and preventive actions.

## The deliverables

### Verification report - ★ Head of Quality

- **Trigger:** every consequential deliverable (load-bearing, external or irreversible) before it lands, whichever department made it; any work the user asks to have checked.
- **Done when:** the verdict is one of the four (`verification.md`); every definition-of-done condition is marked met or unmet with the evidence checked, not a general thumbs-up; the load-bearing numbers and claims traced are named with their sources, and anything that did not trace is named too; each seat that ran is listed with its verdicts and how each was weighed; each defect is stated specifically enough for its producer to act on, by class, with the clause it breaks and its severity; noted defects are listed to travel with a pass; any escalation names what rose and whether it touches a gated act; no seat made the work or saw the author's reasoning; and the verdict is on record with the caller before the deliverable is written, so a FAIL is never written.
- **Needs from other departments:** the deliverable, the brief it was made against, its definition of done and its completion evidence, all from the department that made it.
- **Shape:** `templates/verification-report.md`.

### Quality standard, definition of done or quality management plan - ★ Head of Quality, with the owning department's lead

- **Trigger:** a deliverable that arrives with no definition of done, a new kind of deliverable, a recurring defect class, a stage change.
- **Done when:** every clause is testable (an observable check a stranger could run, with its pass condition); each clause names what it protects; the owning department's lead agrees it is the bar; the QA Test Engineer has checked every clause for testability; a standard the whole company will hold itself to is accepted by the user.
- **Needs from other departments:** the owning department's knowledge of the work; a metric's definition from the business-intelligence skill when a clause measures one.

### Test plan - QA Test Engineer

- **Trigger:** a release or launch, a batch of deliverables, a process change to prove before it goes live, a software or skill build large enough to need one.
- **Done when:** every requirement or acceptance criterion maps to at least one check (the traceability matrix); the checks include edge, boundary, negative, error-path and, for a build, adversarial cases, not only the main path; the entry and exit criteria are stated; the environment and data are named; what is out of scope is named, not silent; the Head of Quality has approved it.
- **Needs from other departments:** the requirements and acceptance criteria, from the department that owns the work (for a build, the research-and-development skill's locked requirements). A requirement with no testable criterion is returned to its owner.
- **Shape:** `templates/test-plan.md`.

### Test results and defect reports - QA Test Engineer

- **Trigger:** each run of a test plan or a verification's checks; every build the research-and-development skill borrows the seat for, and every scoped re-audit of a fix.
- **Done when:** every criterion carries PASS, NEEDS-FIX or FAIL against its clause, with the check run; for a build, the validator's and the test suite's output is attached; every non-PASS is reproducible (steps, expected and actual, environment) with a severity read and the smallest prescribed fix; an anomaly that did not reproduce is reported as one; the unverified scope and its blocker are named.
- **Shape:** `templates/test-results.md`, with `templates/defect-report.md` for each defect the log keeps.

### Claim and number ledgers - Fact-Checker

- **Trigger:** any draft whose claims or numbers will be relied on or go out: a research draft the research-and-development skill borrows the seat for, a press release, a pitch, an investor update, a proposal, the user's own speech, post or application.
- **Done when:** every load-bearing claim carries a verdict (SUPPORTED, WEAK-BASIS, UNSUPPORTED, NEEDS-CITATION, CONTRADICTED), the primary source and the passage that backs it (or "not found"), and a fix; every load-bearing number carries a verdict (SUPPORTED, UNSUPPORTED-NUMBER, NOT-COMPARABLE, OVERSTATED) with its source and basis, or the ledger says NONE; two outlets citing one release counted as one source.
- **Shape:** `templates/fact-check-ledger.md`; the method is `fact-checking.md`.

### Plan review ledger - Fact-Checker

- **Trigger:** a money recommendation above a quick answer, any irreversible money step, and every company finance deliverable, before the finance-and-accounting skill delivers or records it; a personal financial plan the user brings to be checked.
- **Done when:** suitability, the math, currency and sourcing, the limits, the risk and, for a company, the completion evidence have each been checked in that order; every finding carries a severity (FATAL, MATERIAL, MINOR), the line it cites, the rule it breaks and the fix; every tax figure, limit and rule the decision turns on was spot-verified at its official source for the right year; one verdict is given (SHIP, REVISE, HOLD) by the rule in `fact-checking.md`.
- **Needs from other departments:** the draft, the fact sheet, the computation check, the user's recorded goals and values, and for a company the completion evidence in the finance-and-accounting skill's `references/company.md`, all from that skill.
- **Shape:** `templates/plan-review.md`.

### Objection set - Devil's Advocate

- **Trigger:** a conclusion, a recommendation, a plan or a decision case before it ships or is acted on: a research draft (always on a deep research run), a strategy memo, a business case, the user's own plan for a big step.
- **Done when:** the framing was attacked first; the strongest alternative was built before any strike; the load-bearing assumptions are listed with where each would break; every objection is classed FATAL, MATERIAL or MINOR, marked stands or answered (with the settling citation), and every FATAL and MATERIAL names its falsifier.
- **Shape:** `templates/critique-ledger.md`; the method is `critique.md`.

### Idea verdict ledger - Devil's Advocate

- **Trigger:** a deduplicated pool of ideas to narrow, before it is ranked; the research-and-development skill borrows the seat for its standard and deep idea runs.
- **Done when:** every idea was steelmanned before it was tested; each carries KEEP, FLAW or KILL on novelty, feasibility and a fatal flaw; each KEEP and FLAW carries its evolution potential, high or low; each FLAW names the fixable flaw to evolve and each KILL the fatal flaw.
- **Shape:** `templates/critique-ledger.md`.

### Design review - Design Critic

- **Trigger:** a visual that ships, is load-bearing or will be saved, and every interactive; the business-intelligence skill borrows the seat for its visuals, and any department for a chart in its deliverable.
- **Done when:** form-fit, integrity, the enumerated accessibility gate and clarity were checked in that order; the gate is explicitly PASS or FAIL with each failing check named; every issue is classed FATAL, MATERIAL or MINOR with the mark it concerns and the rule it breaks; the call is SHIP or HOLD.
- **Shape:** `templates/design-review.md`; the checklist is `critique.md`.

### Root cause and corrective action - ★ Head of Quality, with the QA Test Engineer reproducing

- **Trigger:** a major or critical defect, a recurring class (in the department's own runs or in a borrower's), a defect a user reports through the customer-experience skill.
- **Done when:** the defect is reproduced or logged as an unconfirmed anomaly; its class is named and searched for beyond the one instance; the root cause is traced to a cause the owning department controls and tested against a prediction; the corrective and the preventive action each have an owner in that department and a date; the closing check is defined (`defects.md`).
- **Needs from other departments:** the owning department's process and records; the customer-experience skill's report of the user's experience.
- **Shape:** `templates/defect-report.md`.

### Audit or assessment report - ★ Head of Quality

- **Trigger:** a review cycle, a stage change, a pattern of failures, a request from a customer or a regulator.
- **Done when:** the scope and the standard audited against are named; every finding cites its evidence and the clause; findings are graded by severity; each feeds a corrective action with an owner; sending the report outside the company is listed as the user's gated act.

### A pre-send check of the user's own document - ★ Head of Quality, with the seats it needs

- **Trigger:** the user asks to have an important document, application or plan of their own checked before it goes out: a job, school, grant, visa or loan application, a resume, a form, a personal financial plan, a speech, a big personal plan.
- **Done when:** the standard is named (the form's instructions, the posting's requirements, the program's published rules, read at their source); every requirement is marked met or unmet with what was checked; every fact, date and figure matches the user's own documents, and every outside claim its source (the Fact-Checker); a plan's case is attacked when it argues for a step (the Devil's Advocate); the deadline and the submission route are stated; personal data is cited by where it lives, never copied; and submitting is named as the user's own act.
- **Shape:** `templates/verification-report.md`, returned in the conversation.

## The producing chain

- **The definition of done comes first.** Nothing is graded before its bar exists; work that arrives without one goes back to its owner first.
- **Requirements before tests.** In the product chain (evidence, requirements, design, build, release), the test plan and its traceability matrix come last and can only test what the requirements defined: an untestable requirement is returned to its owner, never guessed at.
- **Inputs were real, not assumed.** Every chain ends here: the verifier checks that the work's upstream inputs existed and were current when it was made, and work built on an assumed input fails on that alone.
- **The fix belongs to the maker.** A root cause in another department's process goes to that department as a corrective action; the team checks the fix and never makes it.

## Stage scales the slice

When the administration skill's record names the venture's stage, scale the work to it:

- **found** (idea to seed): verify what is load-bearing or external (the numbers in a pitch, the first contracts' completeness, and above all whether the metric that reads an experiment actually measures its hypothesis rather than the founder's hope). No standards library yet.
- **scale** (Series A to C): a definition of done for each recurring kind of deliverable, test plans for releases, a defect log with root causes.
- **maintain** (established to mature): audits on a cadence, recurring classes prevented at their cause, standards reviewed as the work changes.
