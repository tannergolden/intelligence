# Cadence - the money checkups a review run performs

What a review run checks and when, for the household and for a company the user runs. Read before a review run. Each checkup ends in the `templates/checkup.md` scorecard and leaves the next dated deadlines listed in the delivery (and, in a private money repository or a company finance repository, in its deadline list, per `data-and-writes.md`). Every date below is the usual US one: verify it each year at the source (`assets/official-sources.json`), since dates move for weekends and holidays and the rules change.

## Monthly: the cash flow review (standard tier)

- **The Cash Flow Analyst:** actual spending against the plan; the true surplus; the irregular costs due next month and the sinking funds behind them; the emergency fund against its target; progress on the payoff plan; any promotional rate ending within ninety days; statements scanned for errors or fraud.
- **The skill:** the next month's dated items, listed in the delivery and, in a private money repository, recorded in its deadline list.

## Quarterly (standard tier)

- **The Tax Strategist:** estimated tax payments when income is not fully withheld (self-employment, investment income, a large bonus or sale).
- **The Investment & Retirement Analyst:** allocation drift against the rebalancing rule; rebalance only outside the bands.
- **The Cash Flow Analyst:** a rounded net worth snapshot, offered to the financial picture where a private money repository keeps one; a subscription and recurring-cost audit twice a year.

## The annual calendar (deep tier for the annual review)

| When | Checkup | Seats |
|------|---------|-------|
| Mid-January | The prior year's fourth-quarter estimated payment | The Tax Strategist |
| Late January to mid-February | Tax forms arrive (W-2s, 1099s, brokerage statements); gather the documents | The Tax Strategist |
| February to mid-April | File, or extend; contributions to IRAs and HSAs for the prior year are due by the filing deadline, not the extension | The Tax Strategist, the Investment & Retirement Analyst |
| Mid-April | The filing deadline and the first-quarter estimated payment | The Tax Strategist |
| Mid-June | The second-quarter estimated payment | The Tax Strategist |
| Mid-September | The third-quarter estimated payment | The Tax Strategist |
| Mid-October | The extended filing deadline | The Tax Strategist |
| Autumn | Workplace open enrollment: the health plan, HSA or FSA amounts, group coverage | The Investment & Retirement Analyst, the Insurance & Estate Specialist |
| Mid-October to early December | Medicare open enrollment, when the user or a parent is on Medicare | The Insurance & Estate Specialist |
| November to mid-January | Marketplace open enrollment on HealthCare.gov, when not covered at work: enroll by mid-December for coverage from January 1; a state's own exchange sets its own dates | The Insurance & Estate Specialist |
| November and December | Year-end moves: harvest losses or gains, Roth conversions, required distributions, charitable giving, the last workplace plan deferrals, FSA balances, withholding checked against the safe harbor | The Tax Strategist, the Investment & Retirement Analyst |
| Once a year, any month | Credit reports from all three bureaus (free at the official source), insurance renewals and coverage review, every beneficiary designation, the emergency fund re-sized, the full plan refreshed | The Cash Flow Analyst, the Insurance & Estate Specialist, the lead |
| Every three to five years, and at every life event | The will, the powers of attorney and the health care directive reviewed | The Insurance & Estate Specialist |

## The company's cadence

For a company the user runs. The deliverables' shapes and their completion evidence are in `company.md`; every date is the usual US one for a calendar-year company, so verify it each year at the source and shift it for a different fiscal year.

### Monthly: the close (standard tier)

- **The Cash Flow Analyst:** the close, by a day the company sets after month-end (commonly within about ten business days): cutoff, accruals and deferrals, every account reconciled to its source, the statements, the period locked; cash, gross and net burn, runway at the trailing rate and its cash-zero date; the cash troughs over the next quarter; receivables by age.
- **The Investment & Retirement Analyst:** the variance to the budget by cause, one-time split from run-rate.
- **The Tax Strategist:** payroll tax deposits on the schedule the IRS sets for the company, and sales tax returns where it is registered.
- **The lead:** the runway read against the floor, the close package through the Plan Reviewer, and the next month's deadlines listed (and recorded, in a company finance repository).

### Quarterly (standard tier)

- **The Investment & Retirement Analyst:** the reforecast, rolling the model forward on the quarter's actuals; unit economics against their bands, from the stage at which each is load-bearing.
- **The Tax Strategist:** the company's estimated tax payments where it owes income tax (its owners' where income passes through), and the quarterly employer payroll return.
- **The lead:** the runway review and the date to start raising; the cap table reconciled to every document executed in the quarter; the finance section of the board package when the board skill runs a review.

### The company's annual calendar (deep tier for the annual budget)

| When | Checkup | Seats |
|------|---------|-------|
| End of January | Wage and contractor forms to workers and the government; the annual employer unemployment tax return; the fourth quarter's payroll return | The Tax Strategist |
| By March 1 for a Delaware corporation | The franchise tax and annual report, computed by every method the state allows; other states set their own dates | The Tax Strategist |
| Mid-March | The partnership or S corporation return, or its extension | The Tax Strategist |
| Mid-April | The C corporation return, or its extension, and its first estimated payment | The Tax Strategist |
| Every twelve months, and after a priced round or another material event | A fresh, independent 409A valuation before new option grants | The Tax Strategist, the lead |
| At each renewal | Business coverage: general liability, professional liability, D&O, cyber, workers' compensation, key person | The Insurance & Estate Specialist |
| Fourth quarter | Next year's operating budget, tied to the model's base case; the company's year-end tax moves | The Investment & Retirement Analyst, the Tax Strategist, the lead |
| Year-end | The year-end close; the cap table, the vesting schedules, and the 83(b) and QSBS dates reviewed | The Cash Flow Analyst, the lead |

## How a review run works

1. Pick the checkup from the calendar and the user's request; the annual review runs every row of the scorecard.
2. Preflight as for any run, then dispatch the seats the checkup names, each briefed on the period under review.
3. Fill the `templates/checkup.md` scorecard: each area on track, watch, or act, with its rounded evidence and its one next action and date.
4. Gate through the Plan Reviewer as for a standard run, deliver the scorecard findings-first, and list the next deadlines (recorded in the deadline list only in a private money repository).
5. In a private money repository, offer the financial-picture updates the checkup surfaced (a new rounded net worth, a changed risk posture, a new policy), line by line.
6. For a company, the monthly review is the close: the Cash Flow Analyst's close package, the variance by cause, and the lead's runway read, fill the company rows of the scorecard; once the Plan Reviewer clears it, it goes into the financials record in a company finance repository, and anywhere else it is delivered in chat.
