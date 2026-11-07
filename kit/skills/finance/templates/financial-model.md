# Financial model (the shape of a company's model)

The Investment & Retirement Analyst builds it on the Cash Flow Analyst's closed actuals, the ★ Financial Planning Lead approves it at its seam, and the Plan Reviewer verifies it against the completion evidence below before it lands (`references/company.md`). It is also the brief's output contract for the model: every field is filled, or marked as missing with the skill that owns it. Scale it to the stage: at found, the projection is a driver-based monthly cash view through the next raise plus a buffer; at scale, it adds the three tied statements and unit economics; at maintain, the durability view.

- **Company and unit:** [a pointer to the company; its entity and stage]
- **The question it serves:** [a planning cycle, a raise, a major spend or hire, a runway question]
- **Basis and periods:** [cash or accrual; the fiscal year; monthly for at least the first 12 to 24 months, then by year]
- **Actuals base:** [the last closed month and its close date, tied to the close package]
- **Horizon:** [through the next raise plus a buffer, at least]

## Bottom line

- **Runway:** [base: N months, cash-zero date; downside: N months, cash-zero date]
- **When to raise:** [the month runway reaches about twelve months in the downside]
- **The driver that moves it most:** [the driver, and how far the runway moves for a stated change in it]

## Drivers

| Driver | Value | Source or assumption | Owner | Sensitivity |
|--------|-------|----------------------|-------|-------------|
| [new bookings per month] | [value] | [the sales skill's forecast, dated; or a marked assumption] | [the sales skill] | [high, medium or low] |
| [churn, price, gross margin, billing and collection terms] | | | | |
| [headcount by role and start month, fully loaded cost] | | [the people skill's hiring plan, dated; or a marked assumption] | [the people skill] | |
| [other spending by driver or contract] | | | | |

## Projection

| Period | Revenue | Gross margin | Operating spending | Net burn | Cash at period end |
|--------|---------|--------------|--------------------|----------|--------------------|
| [month] | | | | | |

At scale, attach the income statement, the balance sheet and the cash flow statement for each period, tied to each other.

## Scenarios

| Scenario | Drivers flexed, with their own values | Runway | Cash-zero date | Breakeven month |
|----------|---------------------------------------|--------|----------------|-----------------|
| Base | [the drivers above] | | | |
| Downside | [its own churn, bookings and hiring pace, never the base case's] | | | |
| Upside, where it informs the call | | | | |

## Unit economics (from the stage at which each is load-bearing)

| Metric | Value | Definition used | Reference band |
|--------|-------|-----------------|----------------|
| [CAC, LTV on a gross-margin basis, LTV to CAC, CAC payback, gross margin, burn multiple] | | [the company's governed definition, or the one in `references/company.md`] | |

## Variance to the last model or budget

| Line | Plan | Actual | Variance | Cause (volume, price, timing, mix) | One-time or run-rate |
|------|------|--------|----------|------------------------------------|----------------------|
| [line] | | | | | |

## A round, when one is in play

- **Size and milestone:** [the months of runway it buys at the model's burn, the buffer, the milestone it reaches]
- **Valuation:** [pre-money, post-money, the price per share]
- **Pool and instruments:** [the option pool's top-up and whom it dilutes; each SAFE and note converted by its own terms]
- **Dilution:** [each holder's percentage before and after; the pro forma cap table, for the lead]

## Completion evidence

- [ ] Every number traces to a source or a stated assumption, and none is backsolved.
- [ ] The actuals tie to the close.
- [ ] At scale, the statements tie: the balance sheet balances, and the cash flow ends at the balance sheet's cash.
- [ ] Each scenario is labeled and flexes its own drivers.
- [ ] Runway is stated in months with its cash-zero date for each scenario.
- [ ] Revenue traces to the sales skill's forecast and headcount to the people skill's plan, or each is a marked assumption.
- [ ] The skill's script reproduced every load-bearing number (the ties, the runways, the unit economics, the round's math).

## Review and saved

- **Lead's approval:** [approved at the seam, with any seam fixed]
- **Plan Reviewer:** [SHIP, REVISE or HOLD, and the findings applied]
- **Saved:** [where a company finance repository's instructions keep the model; otherwise "nothing", delivered in chat; in a board run, "returned to the board skill"]
