# finance Changelog

## Current Version

**`1.4.0`**

The version is SemVer, per standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver). It matches `metadata.version` in `SKILL.md`, and develop's validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** the version by standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver), and update the Current Version line with every entry.
- **4-entry cap** per section; a fifth drops the oldest.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `1.0.0` - 2026-10-22

Initial build of the finance skill: a personal and household finance skill, dispatching the new standing Finance team (the Financial Planning Lead leads the Cash Flow Analyst, the Credit & Debt Specialist, the Tax Strategist, the Investment & Retirement Analyst, the Insurance & Estate Specialist, the Equity & Benefits Specialist and the Home & Major Purchases Analyst, with the Plan Reviewer as the independent Plan Reviewer) to the standard of the Founder's interest first, with show the math as its craft rule. Three modes (ask, plan, review) and three tiers (quick, standard, deep); a fact sheet compiled before dispatch; every load-bearing number reproduced by a script before review; a blind review gate on consequential advice; and a gate that never moves money and never records a secret. Five references (doctrine, dispatch, data and writes, cadence, life events), five templates (fact sheet, brief, plan, review, checkup), and two assets (trigger tests, official US sources).

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

### `1.4.0` - 2026-11-07

The skill now covers a company's money as well as the household's: for a company or venture the user runs, the books and the monthly close, cash, burn and runway, the financial model (a driver-based forecast, scenarios, unit economics), the operating budget, the cap table and dilution, fundraising math, company tax and business insurance. The board skill's Finance & Accounting department is retired and its duties move here, so the team stays at six and each seat applies its craft to both units: the Financial Planning Lead is also the company's finance lead (capital allocation and runway calls as recommendations, the cap table, approving the model), the Cash Flow Analyst keeps the company's actuals (the books, the close, the statements, cash, burn and runway), the Investment & Retirement Analyst builds its forward model and the math of a raise, the Tax Strategist adds company tax (the entity's tax classification, payroll and sales tax basics, credits, franchise tax, the 409A beside the 83(b) and QSBS clocks), the Insurance & Estate Specialist adds business insurance and founder succession, and the Plan Reviewer verifies the model, the statements and any cap table change before they land. A new `references/company.md` carries the deliverables with their completion evidence, the stage scaling, the inputs from other skills and the metrics, and a new `templates/financial-model.md` the model's shape. The doctrine adds the company foundations, decision rules and referrals; dispatch the company tiers, routing and order; the cadence the close and the company calendar; the life events the company events; and data and writes the *company finance repository*, the only place a company's figures are written. Business decisions and strategy stay with the board skill, which convenes the lead as the company's finance function and persists its own runs; the pipeline comes from the sales skill and equity documents from the legal skill. The description, the roster and its global rules, every spec, the templates, the official sources and the trigger tests follow, and `metadata` drops its `id` key.

### `1.3.0` - 2026-11-07

The Finance team is trimmed to its six most critical agents: the Financial Planning Lead, the Cash Flow Analyst, the Tax Strategist, the Investment & Retirement Analyst, the Insurance & Estate Specialist and the Plan Reviewer. Three seats retire and their duties fold into the survivors, so every topic still has one owner: credit and debt (reports, scores and utilization, payoff order by avalanche or snowball, refinancing and consolidation, collections) and large purchases (rent or buy, mortgage affordability, cars) move to the Cash Flow Analyst; stock compensation (RSUs, ISOs and NSOs, ESPP, 83(b) elections, AMT, exercise timing) moves to the Tax Strategist; and workplace benefits (open enrollment, HSA and FSA, the 401(k) match and plan choices, job offers and leaving a job) move to the Investment & Retirement Analyst. The roster, `SKILL.md`'s team and dispatch scaling, the routing table and dependency order (`references/dispatch.md`), the life events, the cadence, the doctrine's design basis, and the official sources' domain-to-seat map follow.

### `1.2.0` - 2026-11-07

The hub now owns and authors the skill, made universal: the hand-over rule to a vault's own copy is gone, and it runs the same in any repository or a plain conversation. It writes the user's finances into a repository only when that repository's instructions say it is a private one made to hold them; everywhere else the plan, its deadlines and its open loops stay in the conversation (`references/data-and-writes.md`, reworked around that rule, with the vault's fixed folders replaced by the records a private repository's instructions name). The roster is in develop's format, every spec carries `title:` and is known by it alone (spoken names dropped), the namesake `Finance.md` is folded into `SKILL.md` and `references/doctrine.md` and deleted, and "the Founder" reads "the user".

### `1.1.0` - 2026-10-26

The Finance team now ships inside the skill, in `agents/`, instead of living in a separate team folder, and the skill source moved to `.agents/skills/`, where the agent apps read a repository's skills, so the vault's own sessions load it and tannergolden/intelligence's home kit can carry it to every repository. Briefs read each spec from `<skill>/agents/`, and the dispatch reference and `SKILL.md` point there too. A new **Where it runs** rule: in a vault, the vault's own copy runs, so a home copy hands over to it; anywhere else the run works only from what the user says and keeps nothing. `allowed-tools` now pre-approves read-only tools only, and the frontmatter keeps one key to a line, as the home kit's reader requires.

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

### `1.0.2` - 2026-10-23

Fixes from a second, independent audit of the team and the skill, each checked against the official sources:

- Delaying Medicare Part B now depends on who pays first: at an employer with fewer than 20 employees Medicare usually does, so Part B starts on time (the Insurance & Estate Specialist, `references/life-events.md`).
- Every income move (a Roth conversion, a gain harvest, a bonus, an extra withdrawal) is checked against the Marketplace premium tax credit, now repaid at filing with no cap, as well as IRMAA (the Tax Strategist, the Investment & Retirement Analyst, the Insurance & Estate Specialist, `references/doctrine.md`).
- The inheritance event dates its deadlines (the nine-month disclaimer, the portability election, the year-of-death distribution); a federal student loan is never left to default; the match counts once it vests; debt payoff waits only on the starter buffer; the IRA rollover limit runs per 12 months; a government money market fund is no longer called government-backed.
- Quick answers reproduce a seat's numbers with a script and lead with any foundation gap; the Plan Reviewer's inputs, severities and re-review scope read the same everywhere; the dependency order adds the Insurance & Estate Specialist before the Equity & Benefits Specialist and the Investment & Retirement Analyst before the Tax Strategist on account choice.
- One owner per topic now holds (COBRA, the dependent care FSA, self-employed retirement plans, estate tax thresholds), public benefits and Social Security disability have owners, and the brief carries each seat's sources inline.
- The official sources add the state unemployment agency, SHIP Medicare counseling, the No Surprises Act, the PBGC and the IRS child-account page.

### `1.0.1` - 2026-10-22

Fixes from an independent review of the team and the skill, each checked against the official sources:

- A windfall no longer reads as a reason to cash out an inherited IRA or workplace plan: it moves by trustee-to-trustee transfer, and cash above the deposit insurance limit is spread or held in Treasury bills (`references/doctrine.md`, `references/life-events.md`).
- Catastrophic insurance and a will for dependents run alongside the foundations from the first step, the same in the lead's spec, the fact sheet and the Plan Reviewer's check (`templates/fact-sheet.md`).
- One tier table rules, in `references/dispatch.md`: any irreversible step is standard at least, and deep is a plan, a life event, a windfall, or an irreversible decision large relative to net worth.
- The skill adds every fact a seat found to the fact sheet before the computation check, the lead sets each seat's share of the surplus, and the run workspace is deleted whether the run shipped or not.
- Routing gains owners for Medicare, medical bills, a pension's lump-sum-or-annuity choice, college aid, rental property and scam checks, and one owner each for the health plan choice, the HSA and Social Security.
- `templates/plan.md` opens with the question, the Plan Reviewer's brief includes the Profile, and the official sources add the state attorney general, the state's own health insurance exchange and the state housing finance agency.
