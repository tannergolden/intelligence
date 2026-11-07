# Review ledger (the independent check returns this)

The independent check is borrowed from the quality-assurance skill (`references/dispatch.md`): its Fact-Checker on every answer above quick, any irreversible step and every company deliverable, and its ★ Head of Quality as well on consequential work (a deep run, an irreversible step, every company deliverable before it lands). The brief hands each checker this file as the written standard. Each returns its findings in its own output contract's shape, every finding graded by the severities below, and the ★ Head of Quality reads the Fact-Checker's ledger as evidence, checks what it did not cover and does not re-run what it shows was checked. The check defaults to "not yet safe to act on" until every check below clears; it rules and never fixes, and the Chief Financial Officer applies the findings.

## What the check covers, in order

1. **Suitability.** Does the recommendation fit the user's goals, horizon, risk tolerance, liquidity needs, constraints and values, as the fact sheet records them? Were the foundations checked in order (essentials and minimum payments with none missed, the starter buffer, the match, high-interest debt, the full emergency fund), with catastrophic insurance and a will for dependents checked alongside from the first step, never left for last? For a company, were its foundations checked, and does the recommendation keep cash and runway before growth? Is any product favored for a reason other than fit and cost?
2. **The math.** Every load-bearing number traces to the fact sheet and a stated computation; totals add, dates line up, units match, and the skill's script reproduced it. A number nobody can reproduce does not ship.
3. **Currency and sourcing.** Every tax figure, limit, rate, threshold, deadline and program rule is for the right year and jurisdiction, cites an official or primary source (`assets/official-sources.json`), and carries its as-of date; the ones the decision turns on are verified at the source.
4. **The limits.** Advice only, with no step that has the team act on an account, pay, file, sign or change equity; no secret in the text; no diagnosis, treatment or medication advice; every referral trigger honored; nothing presented as legal drafting or a promised return.
5. **The risk.** Irreversible steps are flagged with their downside case; what would change the answer is stated; deadlines are dated.
6. **For a company, the completion evidence** (`references/company.md`): the books (every account reconciles to its source, nothing is plugged, the period is locked, each treatment is cited and each judgment call named); the model (every line traces to a driver or a stated assumption and none is backsolved, the actuals tie to the close, the statements tie, each scenario is labeled and flexes its own drivers, runway and its cash-zero date are stated per scenario, revenue traces to the sales-and-marketing skill's forecast and headcount to the human-resources skill's plan, or each is a marked assumption); the cap table (shares by holder and class sum to the fully diluted total, every row rests on an executed document, the pool is shown, the as-converted view states its assumptions, every open 83(b) window and the QSBS dates are flagged); and its fit (a spend recommendation names its control, and the rigor fits the stage).

Decision criteria, hardest first: suitability before cleverness; a number nobody can reproduce does not ship; for a company, books that do not tie and a cap table that does not sum never land; a current figure without a source and date is MATERIAL, and FATAL when the decision turns on it.

## The ledger

One row per finding, then one verdict.

| # | Seat | Severity | Line cited | Rule it breaks | Fix |
|---|------|----------|------------|----------------|-----|
| 1 | [Fact-Checker or ★ Head of Quality] | [FATAL, MATERIAL or MINOR] | [the plan's or the deliverable's line, quoted] | [suitability, the math, currency and sourcing, the limits, risk; for a company, the books, the model, the cap table] | [the prescribed fix] |

- **FATAL:** acting on it would harm the user or the company: an eligibility error, a horizon mismatch, a skipped foundation, a missed deadline, a math error that flips the answer, a load-bearing figure or rule that is wrong, contradicted by its source, or unverifiable when the decision turns on it, a breach of the team's limits; for a company, statements that do not tie, a cap table that does not sum or records a change no executed document shows, a backsolved number shown as built, a downside that reuses the base case's drivers when the runway call rests on it, a missed 83(b) window.
- **MATERIAL:** wrong or missing but not answer-flipping: a stale or uncited figure, a missing trade-off, a missing referral; for a company, an unexplained variance, an unlabeled scenario, an assumption used but not marked.
- **MINOR:** clarity.

**Verdict:** [SHIP with no FATAL or MATERIAL finding open and, on consequential work, a pass from the ★ Head of Quality; REVISE with MATERIAL findings only; HOLD with any FATAL finding, or a fail or an escalation from the ★ Head of Quality] - [one line of reasoning]

## Hard cases

- **A figure the checker cannot verify at the source:** mark it unverified, MATERIAL, or FATAL when the decision turns on it; never pass it. **A company document the deliverable cites that cannot be checked:** mark the row unverified, FATAL when the cap table or the runway rests on it. **A thin fact sheet:** rule on what is there and flag the gaps the decision turns on.
- **A second round:** check the cited findings and every line the fix changed, fresh, and hold if the same FATAL survives.
- **Calibration.** A sound avalanche payoff plan whose balance-transfer fee is quoted without a source: REVISE, MATERIAL, cite the card's terms and date it. A house down payment needed in 18 months placed in a stock index fund: HOLD, FATAL, against the horizon rule. A seed-stage model whose downside reuses the base case's churn while the runway call rests on it: HOLD, FATAL, the downside needs drivers of its own; its revenue line with no source is MATERIAL, traced to the sales-and-marketing skill's forecast or marked an assumption.
