# Company money - the close, the model, the cap table and runway

How the Finance team works as the finance function of a company the user runs. Read before any company run, with `doctrine.md` (the company foundations, the decision rules and the referrals) and `data-and-writes.md` (where a company's figures may be kept). Each seat applies its craft to the company as well as the household; this file names the company deliverables, who produces each, the evidence each must carry, and where it goes.

## When it applies

- A company or venture the user runs or co-founds, at any stage, from an idea with a bank account to a scaled business. The user's employer is not one: equity in the user's pay is personal stock compensation, and the household runs as usual.
- The unit is pinned on every run: the household or the company, never both in one record. Where the two meet (owner pay, founder equity, a personal guarantee, a loan either way, self-employment tax), both sides are worked on one fact sheet, each figure marked by unit, and each side's answer goes to its own records.
- Business decisions and strategy are the board skill's. Called on its own, this skill does the company's finance work and persists only its finance records. Inside a board run, the board skill convenes the ★ Financial Planning Lead as the company's finance function, the finance work returns to the board skill, and the board skill persists that run's results.

## Who does what

| Seat | For the company |
|------|-----------------|
| ★ Financial Planning Lead | frames the company's finance work; makes the capital allocation and runway calls as recommendations; keeps the cap table; approves the model |
| Cash Flow Analyst | the actuals: bookkeeping, the monthly close, the statements, cash position, net burn and runway at the trailing rate, the cash troughs ahead, receivables and payables |
| Investment & Retirement Analyst | the forward model: the driver-based forecast, scenarios and sensitivities, the operating budget and its variance, unit economics, fundraising and dilution math |
| Tax Strategist | company tax: the entity's tax classification and elections, estimated payments, payroll and sales tax basics, credits, franchise tax, the 409A, the 83(b) and QSBS clocks |
| Insurance & Estate Specialist | business insurance and founder succession |
| Plan Reviewer | verifies every deliverable below against its completion evidence before it lands |

## The stage scales the work

Stages as the board skill's lifecycle names them; the user may say pre-seed, seed or Series A instead.

- **found** (an idea to early revenue): the survival set. The books kept from day one, cash, net burn and runway, a one-page driver-based monthly cash projection through the next raise plus a buffer, and the cap table with its 83(b) and QSBS clocks. Metrics that are not yet load-bearing (the Rule of 40, the magic number, the burn multiple) are not reported as if they were.
- **scale** (a repeatable revenue motion): the monthly close package, the three statements tied in the model, unit economics, and the annual operating budget.
- **maintain** (a durable business): the durability view (free cash flow and its margin, the Rule of 40) and the finance section of the board package, through the board skill.

## The deliverables

Each names its producing seat, its trigger, its shape, the completion evidence the Plan Reviewer checks, and where it goes. "Its record" means the record a company finance repository's instructions name for it (`data-and-writes.md`); with none, the deliverable is returned in chat.

### The monthly close and reporting package

- **Seat:** the Cash Flow Analyst; the variance by cause from the Investment & Retirement Analyst; the runway read from the lead.
- **Trigger:** month-end, a review run, or "close the books for October".
- **Shape:** the period and the accounting basis; each reconciliation (every bank and card account, receivables, payables, payroll) with its status; the entries booked (accruals, deferrals, revenue recognized) with each treatment cited; the income statement, balance sheet and cash flow statement; the variance to budget by cause; cash on hand, gross and net burn over the trailing three months with one-time items split out, and runway in months with its cash-zero date; receivables by age and days to collect; the judgment calls for the lead; the next month's deadlines.
- **Completion evidence:** every account reconciles to its source document and nothing is plugged; the period is locked, and any correction to a closed period is booked forward; the variance is explained by cause, not just shown; cash and runway are current as of the close date.
- **Goes to:** the company's financials record.

### The financial model

- **Seat:** the Investment & Retirement Analyst, on the Cash Flow Analyst's closed actuals; the lead approves.
- **Trigger:** a planning cycle, a raise, a major spend or hire, or "build our financial model".
- **Shape:** `templates/financial-model.md`.
- **Completion evidence:** every number traces to a source or a stated assumption, and none is backsolved; the actuals tie to the close; at scale, the three statements tie (the balance sheet balances, and the cash flow ends at the balance sheet's cash); each scenario is labeled and flexes its own drivers; runway is stated in months with its cash-zero date for each scenario; revenue traces to the sales skill's forecast and headcount to the people skill's plan, or each is a marked assumption.
- **Goes to:** the company's model record.

### The operating budget

- **Seat:** the Investment & Retirement Analyst; the lead approves.
- **Trigger:** the annual planning cycle, or a raise that resets the plan.
- **Shape:** spending by department and month and headcount by role and start month, tied to the model's base case; the plan each monthly close is measured against.
- **Completion evidence:** it ties to the base case; every line has an owning department; the headcount matches the people skill's hiring plan, or the gap is named.
- **Goes to:** with the model.

### The cap table

- **Seat:** the ★ Financial Planning Lead keeps it; the round and dilution math come from the Investment & Retirement Analyst and the clocks from the Tax Strategist.
- **Trigger:** incorporation, a round, a grant, a repurchase or a transfer, or "update the cap table after the seed round".
- **Shape:** one row per holder and class: the shares or units, the instrument (common, preferred by series, options, a SAFE, a note), vesting, the executed document it rests on and its date, the 83(b) filing date for restricted stock, and the QSBS issuance date; the option pool, granted and available; every SAFE and note outstanding, with an as-converted view on stated assumptions; the fully diluted total and each holder's percentage.
- **Completion evidence:** shares by holder and class sum to the fully diluted total; every row rests on an executed document; the pool is shown; the as-converted view states its assumptions; every open 83(b) window and the QSBS dates are flagged.
- **Goes to:** the company's cap table record, only on the user's yes and only once the documents behind the change are executed. Modeling a round is a draft; recording ownership is the user's call, and issuing, granting or transferring equity is the user's act on the legal skill's documents.

### A round's model (the fundraising math)

- **Seat:** the Investment & Retirement Analyst; the lead recommends.
- **Trigger:** a planned raise, a term sheet, a SAFE or note on offer, or "how much should we raise".
- **Shape:** the round sized to the milestone it buys (the months of runway at the model's burn, commonly 18 to 24, plus a buffer); the pre- and post-money valuation and the price per share; the option pool's top-up and whom it dilutes; every SAFE and note converted by its own terms (the cap, the discount, pre- or post-money, a note's interest) at the round; each holder's dilution; the pro forma cap table.
- **Completion evidence:** the pro forma sums to its fully diluted total; every term comes from the term sheet or the documents, or is marked as an assumption; stacked caps are shown converting together.
- **Goes to:** chat, or with the model; the instruments are the legal skill's to draft and the user's to sign.

### The runway call

- **Seat:** the ★ Financial Planning Lead, from the actuals and the model.
- **Trigger:** "how much runway do we have", a spend or hire decision, or a close that moves runway toward the floor.
- **Shape:** runway now (at the trailing net burn) and per scenario, the floor, the date to start raising, and the ranked moves (cut, raise, extend, grow revenue), each with its runway effect and its reversibility; a recommendation, never a decision made.
- **Completion evidence:** both runways reproduced by the skill's script; the floor named; each move's effect computed.
- **Goes to:** chat; a decision the user makes may become a finance decision record.

### The company tax plan and calendar

- **Seat:** the Tax Strategist.
- **Shape:** the entity's tax classification and why; the year's obligations with their dates (estimates, payroll deposits and returns, the year-end wage and contractor forms, sales tax where registered, franchise tax and the annual report, the return); the credits worth claiming; the open clocks (each 83(b) window, the QSBS dates, the 409A's date); and every point a licensed professional must prepare or sign.
- **Goes to:** the company's deadline list, where its records keep one; otherwise chat.

### The business coverage map and founder succession

- **Seat:** the Insurance & Estate Specialist.
- **Shape:** each business risk with its coverage, gap, recommendation and any contract or legal floor (general liability, professional liability, D&O, cyber, workers' compensation, key person, property, employment practices); the buy-sell agreement and its funding; who acts if a founder cannot; the founder's shares in their estate plan.
- **Goes to:** chat, or the company's records where its instructions keep coverage.

## Inputs from other skills

- **The sales skill:** the pipeline, the bookings and the revenue forecast the model's revenue line rests on. Finance converts bookings to recognized revenue and to cash by the billing and collection terms; it never builds the pipeline.
- **The people skill:** the hiring plan by role and start month, and the pay bands; finance adds the fully loaded cost.
- **The legal skill:** the executed documents the cap table rests on (the formation, founder stock agreements, SAFEs and notes, stock purchase and option agreements, board consents), and contracts with payment terms.
- **The analytics skill:** the company's governed metric definitions, where it keeps them; finance reports on those definitions and never redefines them.
- **The board skill:** the strategy and goals the model's assumptions trace to, and every business decision.

A missing input is flagged in the delivery, and the model carries a bounded, marked assumption in its place, naming the skill that owns it.

## The producing order

Strategy and goals (the board skill) come first, then the operating budget, then the monthly close (the actuals), then the forward model and the board package. A deliverable is never built on a missing input: produce or flag the input first. The model's assumptions trace to the strategy, and each close reconciles the plan against the actuals.

## The metrics

Report each on the company's own definitions where it keeps them, and only from the stage at which it becomes load-bearing. A band is a reference point for B2B software (2025/26), never a measurement of this company; adjust it for the industry and the stage.

| Metric | Formula | Load-bearing from | Reference band |
|--------|---------|-------------------|----------------|
| Net burn | cash out minus cash in, per month | found | |
| Runway | cash on hand / net monthly burn, in months, with the cash-zero date | found | start raising with about 12 months left |
| CAC | fully loaded sales and marketing spend / new customers, same period | late found | |
| Gross margin | (revenue - cost of revenue) / revenue | scale | over 75% strong, under 60% weak (software; goods differ) |
| Burn multiple | net burn / net new ARR, same period | scale | under 1 strong, over 2 weak |
| LTV | (average revenue per account x gross margin) / customer churn rate | scale | |
| LTV to CAC | LTV / CAC | scale | over 3 healthy, under 1 destroys value |
| CAC payback | CAC / (monthly recurring revenue per customer x gross margin), in months | scale | under 12 strong, over 18 weak |
| Days to collect | (receivables / revenue) x days in the period | scale | about 30 to 45 on net-30 terms |
| Magic number | net new ARR / prior period's sales and marketing spend | scale | over 0.75 efficient, under 0.5 fix first |
| Rule of 40 | revenue growth % + profit margin % | scale, the headline above about $5M to $10M ARR | 40 or more |
| Free cash flow margin | (operating cash flow - capital spending) / revenue | maintain | |

## Who decides

- The lead recommends; the user decides. A spend recommendation is checked against its budget line and the runway it consumes; an unbudgeted or irreversible spend is put to the user with its runway cost and its reversibility framed, and names the standing control that governs its category.
- Approval thresholds are the user's to set for each company; with none set, every spend is the user's call.
- A decision across departments, or a conflict with another department, goes to the board skill's ★ Chief Executive Officer; the board skill's Chief of Staff carries messages between departments.
