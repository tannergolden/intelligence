# Deliverables - what the Sales & Revenue team produces, and where it goes

The department's producing map. For each deliverable: the seat that produces it, what triggers it, the completion evidence the verifier checks (its Definition of Done), and where it goes. Read it before producing anything, and put the deliverable's Definition of Done into the brief, because it is the written standard the verifier judges against.

The produce loop is fixed. The lead (the ★ Chief Revenue Officer, whom the skill embodies) frames a self-contained brief and dispatches the seat that holds the craft; the lead frames and approves and never types the deliverable itself. The seat produces and returns, with its completion evidence: every figure traced to a record, a system of record or a named source, and every assumption named. Someone other than the author verifies anything consequential (the quality skill's ★ Head of Quality). The skill writes the verified record behind its write-gate. One deliverable has one accountable owner, the ★ Chief Revenue Officer unless an entry names another.

"The venture's Sales & Revenue records" means wherever the repository's instructions keep them. With no such instruction, the deliverable is returned in the conversation and written only where the user asks. Inside a board run, board persists that run's results.

## Standing records

The durable records the department keeps current rather than re-creates: the stage definitions and the funnel; the pipeline and the committed forecast, with its accuracy history; the revenue plan; the sales plan and playbook (stages, territory, quota); the positioning and messaging; the go-to-market surface for each product; the demand plan; and the pricing exception log. The pricing policy itself is a company decision, kept wherever board's decisions are kept; sales administers it (`deal-desk.md`).

## The deliverables

### Positioning and messaging
- **Seat:** Product Marketing Manager.
- **Trigger:** a launch, a new segment, a rebrand, or a run of lost deals that points at the message.
- **Done when:** the positioning is one sentence a stranger can repeat; it names the buyer, the alternative the buyer compares against, and a true, material differentiation; the messaging maps to the buyer's jobs and drops the claims every competitor could make; every claim traces to evidence or to shipped capability.
- **Goes to:** the venture's Sales & Revenue records (positioning). A published asset waits for the user, after the communications skill checks its brand voice.
- **Needs:** market and competitor facts from the research skill.

### Go-to-market (launch) plan
- **Seat:** Product Marketing Manager, with the Demand Generation Manager for the channel plan.
- **Trigger:** a launch or a new market.
- **Done when:** the ideal customer profile is specific (never "everyone"); the why-now is evidenced; the launch tiers have owners and dates; the pipeline target and the channel mix trace to a number; the readiness gate includes sales enablement (the message, the objections, the technical answers); every external asset is flagged as needing the user's confirmation (`templates/gtm-plan.md`).
- **Goes to:** the venture's Sales & Revenue records (the go-to-market surface).
- **Needs:** the positioning above, and the shipped capability the Sales Engineer confirms.

### Demand and campaign plan
- **Seat:** Demand Generation Manager.
- **Trigger:** a quarter, a launch, or a pipeline gap.
- **Done when:** the funnel math runs backward from the pipeline target to the lead volume each channel must carry; each program names its channel, its budget fit, its attribution path, and the leads, pipeline and CAC it returns; spend sits inside the CAC and payback ceiling; every spend, send and contact-list upload is flagged as needing the user's confirmation.
- **Goes to:** the venture's Sales & Revenue records (the demand plan).
- **Needs:** the budget and the CAC ceiling from the company's plan (the finance skill), and the positioning.

### Deal call
- **Seat:** Account Executive, with the Sales Engineer when the deal turns on what the product can do.
- **Trigger:** a deal at a decision point, a pipeline review, or a request for a discount.
- **Done when:** the stage is named with its exit criteria met; qualification is read on need, budget, authority and timeline (or the venture's own framework); the next step and its blocker are named and dated; the offer sits inside the latitude or the exception request is framed; the close probability is weighted on evidence.
- **Goes to:** the venture's Sales & Revenue records (the pipeline), and into the forecast.

### Technical sales design and proof-of-concept plan
- **Seat:** Sales Engineer.
- **Trigger:** a buyer's technical requirements, an integration or security questionnaire, or a requested proof.
- **Done when:** each requirement maps to shipped capability or is marked a roadmap dependency; each gap is named with its workaround; the proof has success criteria, test data and steps, and can fail; a proof plan for the buyer is flagged as needing the user's confirmation before it is shared.
- **Goes to:** the venture's Sales & Revenue records (the deal).
- **Needs:** the develop skill's ★ Engineering Lead when the records do not settle what the product does; the systems skill for a security questionnaire's answers about how the company runs its systems.

### Pricing exception
- **Seat:** the Account Executive raises it; the ★ Chief Revenue Officer decides inside the exception band; board decides beyond it (`deal-desk.md`).
- **Trigger:** a deal that only closes outside the pricing latitude.
- **Done when:** the request carries the deal, its value and stage, the ask beside the standard offer, the give-get, the effect on price, margin and the forecast, and the precedent; the decision, its owner and its date are recorded.
- **Goes to:** the venture's Sales & Revenue records (the exception log); a decision beyond the band goes wherever board records its decisions.

### Pipeline review and forecast
- **Seat:** the Revenue Operations Manager (the stage definitions and the stage-weighted count) and the Account Executive (the deal-by-deal call), reconciled by the ★ Chief Revenue Officer (`forecast.md`, `templates/forecast.md`).
- **Trigger:** the forecast cadence the venture sets (weekly or monthly is common), a quarter, or a review run.
- **Done when:** coverage and the forecast trace to named opportunities and stated win rates from the system of record; the pipeline is dated and stage-weighted; every deal sits in a category on its evidence; the two reads are reconciled and their difference explained; the gap to target is named stage by stage, never rounded; the customers skill's renewal read is included; each computed figure lists the inputs it can be recomputed from.
- **Goes to:** the venture's Sales & Revenue records (the pipeline and forecast). The committed number is the input the finance skill takes for the revenue line.

### Revenue plan
- **Seat:** ★ Chief Revenue Officer, with the Revenue Operations Manager.
- **Trigger:** a planning cycle.
- **Done when:** the single revenue number is reconciled across demand, the close and renewal; the stage that binds it is named; the bookings-to-revenue bridge states its timing assumptions, for the finance skill to apply its recognition rules; every metric references the venture's governed definitions (the analytics skill) rather than redefining them.
- **Goes to:** the venture's Sales & Revenue records (the revenue plan), and to the finance skill for the financial model.
- **Needs:** the customers skill's renewal and expansion read; the company's targets from board.

### Sales plan and playbook
- **Seat:** ★ Chief Revenue Officer, with the Account Executive (the close motion) and the Revenue Operations Manager (territory, quota, the process).
- **Trigger:** building a repeatable motion, usually at the scale stage.
- **Done when:** the close motion has named stages with exit criteria; quota is sized to demonstrated capacity and costed against the forecast; territories are balanced; the process is repeatable by someone other than the founder.
- **Goes to:** the venture's Sales & Revenue records (the sales plan).

### Revenue operations plan
- **Seat:** Revenue Operations Manager.
- **Trigger:** two tools that count the funnel differently, a new revenue tool, or a planning cycle.
- **Done when:** the stages are defined with entry and exit criteria; each figure traces to the system of record; one funnel counts each lead once across demand, sales and success; the territory and quota design and the forecast mechanics are stated with their assumptions.
- **Goes to:** the venture's Sales & Revenue records (revenue operations). A change to the systems themselves (access, integrations, security) goes to the systems skill.

## The producing order

Build in dependency order. When a request asks for a downstream deliverable whose upstream input is missing or stale, produce or flag the input first, and the verifier checks that the inputs were real, not assumed.

- **Go-to-market:** positioning and the ideal customer profile -> the go-to-market plan -> demand programs and content -> sales enablement -> the pipeline and the forecast -> (after the sale) the customers skill's onboarding. Sales cannot enable what has not been positioned.
- **Measurement:** the venture's governed metric definitions (the analytics skill) -> the stage definitions -> the pipeline -> the forecast. A forecast built before the stages are agreed reports numbers no one trusts.
- **Deal:** qualification -> solution fit and proof -> the offer inside policy, or the exception decided -> the close -> the handoff to the customers skill (what was sold, promised and proven).

## What the department needs from its neighbours

| Need | From |
|------|------|
| Market size, competitor facts, pricing benchmarks | the research skill |
| Governed metric definitions (win rate, coverage, CAC, churn) | the analytics skill |
| The renewal and expansion read, account health | the customers skill |
| The budget, the CAC ceiling, the revenue line in the financial model | the finance skill |
| Pricing strategy, the price list, revenue targets, a call across departments | the board skill's ★ Chief Executive Officer |
| A non-standard contract term; consent rules for marketing email | the legal skill (its Commercial Counsel; its Privacy & Data Protection Counsel) |
| A published asset's brand voice, press for a launch | the communications skill |
| What the product does, and what a build would take | the develop skill's ★ Engineering Lead |
| The revenue tools' access, integrations and security | the systems skill |
| Polished copy, a chart | the editorial skill, the visualize skill |

Another department's input is read from its records where the repository's instructions keep them, or asked of the user; it is never invented. A disagreement with another department's figure goes to the board skill's ★ Chief Executive Officer with both answers.

## Stage scaling

- **found:** a lean positioning statement, a founder-led go-to-market note, a named-deal pipeline with next steps and dates, and the evidence of willingness to pay; no weighted forecast that pretends to precision the business does not have.
- **scale:** the repeatable set: the sales plan and playbook, the full forecast discipline, revenue operations, quota and territory, and channel-level CAC.
- **maintain:** the durability set: renewal and expansion forecast with the customers skill, net revenue retention read with the finance skill, and the positioning defended against new alternatives.
