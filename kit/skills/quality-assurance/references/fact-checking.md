# Fact-checking - claims, numbers and plans against their sources

The Fact-Checker's method, in full: how a load-bearing claim is traced to its primary source, how a load-bearing number is tested for whether it can bear its weight, and how a financial plan or a company finance deliverable is reviewed before it is recorded. Read it before any fact-check or plan review, whether this skill runs it or another department's skill borrows the seat. The rule above all: **trust nothing load-bearing until its source proves it**.

## What is load-bearing

Check the claims and numbers the conclusion, the recommendation or the decision rests on, not every sentence. A decorative aside is not load-bearing; a figure the argument turns on, a fact a reader will act on, and a date or a limit a plan depends on are. When unsure, ask what would change if the claim were false: if the answer is "the conclusion", it is load-bearing.

## The source ladder

Cite and check against the highest tier available:

1. **Primary** - the thing itself: the paper, the filing, the dataset, the official document, the statute or the agency's rule, the source code, the user's own document.
2. **Institutional** - a standards body, a regulator or a peer-reviewed venue summarizing primary work.
3. **Journalistic** - established outlets with editorial standards.
4. **Aggregator or community** - forums, wikis, blogs: leads, not evidence; they cannot carry a conclusion alone.

Corroboration means tracing back to the origin, not counting echoes: two outlets citing one press release are one source. Date-check everything, and verify that every load-bearing link resolves and says what is claimed; a measurable share of machine-written citations point to sources that do not exist, and a wrong citation is worse than an honest gap.

## Claims

1. Pull every load-bearing claim.
2. Follow each citation to the primary source and locate the passage that backs the claim, so the claim-to-source link is auditable. A citation that resolves but whose passage does not support the claim fails.
3. Grade certainty on its own axis, separate from how strongly the draft asserts it: a confidently worded claim on thin evidence is still thin. Default a single-source or inferred claim to low certainty.
4. Verdict and fix:

| Verdict | Means | The fix the caller applies |
|---------|-------|----------------------------|
| **SUPPORTED** | the primary source says it, at the confidence stated | keep |
| **WEAK-BASIS** | supported only by a single, low-tier or contested source, or stated more strongly than the source allows | soften to the confidence the source supports, or find an independent primary |
| **UNSUPPORTED** | no source found that says it | cut it, or source it before it ships |
| **NEEDS-CITATION** | likely true, but the draft cites nothing checkable | add the citation |
| **CONTRADICTED** | the source says the opposite | reverse or cut the claim |

## Numbers

When numbers carry the conclusion, review each load-bearing figure in the same pass:

- **Source and computation:** it traces to a real source, and any derived figure recomputes from its inputs.
- **Sample:** its size, its population, and how it was selected.
- **Method and period:** how and over what period it was measured.
- **Effect size:** the size of the effect, as distinct from its statistical significance.
- **Base rate and denominator:** what it is a share of, and against what baseline.
- **Comparability:** figures compared share one definition, one denominator and one period.
- **Causation:** a correlation is not read as a cause, and a precise number is not taken for an accurate one.

| Verdict | Means | The fix the caller applies |
|---------|-------|----------------------------|
| **SUPPORTED** | traces to its source, computes, and bears the weight put on it | keep |
| **UNSUPPORTED-NUMBER** | no source, or it does not compute | source it or cut it; never estimate it |
| **NOT-COMPARABLE** | compared against a figure measured another way (a count against a rate, two definitions, two periods) | recompute both on one basis, or state the difference |
| **OVERSTATED** | real, but stretched beyond what its sample, method or effect size supports, or read as causal | soften to what it supports |

When the draft carries no load-bearing number, the number ledger says **NONE**; scrutiny is never manufactured.

## Plans: the review before a plan reaches the user or is recorded

A plan review is the gate on money advice for the user's household and on a company's finance deliverables, which the finance-and-accounting skill borrows the seat for before it delivers or records anything. The seat reads the draft, the fact sheet it rests on, the skill's computation check (which numbers its script reproduced), and the user's goals, horizon, risk posture and values as recorded; for a company deliverable, also its completion evidence (the finance-and-accounting skill's `references/company.md`) and the source documents it cites. It never reads the lead's notes or the other seats' returns. Review in this order:

1. **Suitability first.** Does the recommendation fit the user's goals, horizon, risk tolerance, liquidity needs, constraints and values? Is any product favored for a reason other than fit and cost? Were the foundations checked in order, and is a gap above the question named first?
   - The household's order: essentials and every minimum payment covered with none missed; a starter buffer of about a month of essentials; the full employer match; high-interest debt; the full emergency fund; tax-advantaged retirement saving; other goals; then taxable investing. Catastrophic insurance and a will naming a guardian for dependents are checked alongside from the first step, never left for last.
   - The company's order: its money kept apart; the books closed and reconciled; payroll and tax obligations current; cash and runway known against the floor; the cap table matching its executed documents with no clock missed; the catastrophic business risks insured; controls in place. Cash and runway come before growth, and a dated clock (an 83(b) window, a payroll deposit) jumps the order.
2. **The math.** Every load-bearing number traces to the fact sheet and a stated computation; totals add, dates line up, units match; the skill's script reproduced it. A number nobody can reproduce does not ship.
3. **Currency and sourcing.** Every tax figure, limit, rate, threshold and program rule is for the right year and jurisdiction, cites its official or primary source (the tax agency, the social insurance agency, the state revenue department, the student aid office, the consumer finance regulator, the plan document), and carries its as-of date. Spot-verify at the source the ones the decision turns on; a reputable secondary may explain a rule, never supply its figure.
4. **The limits.** Advice only: no step has anyone act on an account, pay, file, sign or change equity on the user's behalf. No secret appears in the text (an account, card or routing number, a tax ID, a password, a PIN, a security answer). The household and the company stay apart: where they meet (owner pay, founder equity, a personal guarantee, a loan either way), each figure is marked by unit. Every referral trigger is honored (a tax notice, a will to draft, a lawsuit, a company return, a 409A valuation). Nothing is presented as legal drafting or a promised return.
5. **The risk.** Irreversible steps are flagged with their downside case; what would change the answer is stated; deadlines are dated.
6. **For a company, the completion evidence.**
   - The books: every account reconciles to its source, nothing is plugged, the period is locked, each treatment is cited and each judgment call named.
   - The model: every line traces to a driver or a stated assumption and none is backsolved; the actuals tie to the close; the statements tie; each scenario is labeled and flexes its own drivers; runway and its cash-zero date are stated per scenario; revenue traces to the sales-and-marketing skill's forecast and headcount to the human-resources skill's hiring plan, or each is a marked assumption.
   - The cap table: shares by holder and class sum to the fully diluted total; every row rests on an executed document; the pool is shown; the as-converted view states its assumptions; every open 83(b) window and the QSBS dates are flagged.
   - Its fit: a spend recommendation names its control, and the rigor fits the stage.

Then rule each finding and the plan:

| Severity | Means | Examples |
|----------|-------|----------|
| **FATAL** | acting on it would harm the user or the company | an eligibility error; a horizon mismatch; a skipped foundation; a missed deadline; a math error that flips the answer; a breach of the limits; statements that do not tie; a cap table that does not sum or records a change no executed document shows; a backsolved number shown as built; a downside that reuses the base case's drivers when the runway call rests on it; a missed 83(b) window |
| **MATERIAL** | wrong or missing, but not answer-flipping | a stale or uncited figure (FATAL when the decision turns on it); a missing trade-off or referral; an unexplained variance; an unlabeled scenario; an assumption used but not marked |
| **MINOR** | clarity | a figure without its unit; a step out of order with no effect |

**The verdict:** **SHIP** with no FATAL or MATERIAL finding; **REVISE** with MATERIAL findings only, which the plan is recorded only after applying; **HOLD** with any FATAL finding, which is fixed and reviewed again. A second round reviews the cited findings and every line the fix changed, fresh; a FATAL that survives two rounds goes to the user as an open question, never recorded.

## What the Fact-Checker never does

- Judges whether the conclusion is wrong: a true claim can carry a wrong conclusion, and that is the Devil's Advocate's to find.
- Rewrites the draft or the plan, or estimates a number it could not trace.
- Checks its own synthesis, or a plan it helped make.
- Acts on an account, or treats a SHIP as authority for a gated act.
