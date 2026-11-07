# Plan review ledger (the Fact-Checker returns this)

<!-- The Fact-Checker returns one row per finding, then one verdict, on a financial plan or a company finance
     deliverable before the finance-and-accounting skill delivers or records it (references/fact-checking.md). It
     reads the draft, the fact sheet, the computation check and the user's recorded goals and values, blind to how
     the draft was made. It rules and never fixes; the caller applies the findings. -->

| # | Severity | Line cited | Rule it breaks | Fix |
|---|----------|------------|----------------|-----|
| 1 | [FATAL, MATERIAL or MINOR] | [the plan's or the deliverable's line, quoted] | [suitability, the math, currency and sourcing, the limits, risk; for a company, the books, the model, the cap table] | [the prescribed fix] |

- **FATAL:** acting on it would harm the user or the company: an eligibility error, a horizon mismatch, a skipped foundation, a missed deadline, a math error that flips the answer, a breach of the limits; for a company, statements that do not tie, a cap table that does not sum or records a change no executed document shows, a backsolved number shown as built, a downside that reuses the base case's drivers when the runway call rests on it, a missed 83(b) window.
- **MATERIAL:** wrong or missing but not answer-flipping: a stale or uncited figure (FATAL when the decision turns on it), a missing trade-off, a missing referral; for a company, an unexplained variance, an unlabeled scenario, an assumption used but not marked.
- **MINOR:** clarity.

**Figures spot-verified at the official source:** [each figure the decision turns on, its source, tax year and as-of date; or "none needed"]

**Verdict:** [SHIP with no FATAL or MATERIAL finding; REVISE with MATERIAL findings only, recorded only once each is applied; HOLD with any FATAL finding, fixed and reviewed again] - [one line of reasoning]
