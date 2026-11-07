# Doctrine - how the Operations & Logistics (O&L) team works

The method every operations deliverable follows, and the procurement gate. Read it before mapping a process, planning a program or choosing a vendor. The one standard, **the constraint first**, runs through all of it: each section below is that standard applied to one kind of work.

## The constraint first

- **A flow moves at the pace of its constraint.** Throughput is set by the one step that limits it, so an hour saved anywhere else is a mirage (Goldratt, *The Goal*, 1984). The five focusing steps: identify the constraint; exploit it, so it never idles or works on the wrong thing; subordinate every other step to its pace; elevate it, adding capacity only once it is used fully; then repeat, because the constraint moves.
- **Queues tell you where it is.** Work piles up in front of the constraint. Little's Law ties the numbers together: work in progress = throughput x cycle time, so with throughput fixed, cutting the work in progress is what cuts the cycle time.
- **The same rule in each kind of work.** In a process, the constraint is the step where work waits or is redone; in a plan, it is the critical path; in a supply chain, it is the single source or the longest lead time. Name it first, in every deliverable.

## The process as it actually runs

- **Walk it before you draw it.** Trace the process as it runs (who does what next, where the work waits, how anyone knows it was done right), from the trigger that starts it to the output that ends it. The documented flow is a claim about the process, not evidence of it; a step you never traced is a guess, and an inferred step is marked as an assumption.
- **Find the waste where it occurs.** Classify each step as value-adding, necessary but not value-adding, or waste. The common wastes: waiting, rework and defects, overprocessing (a redundant approval, a duplicate entry), a handoff that drops, excess inventory, needless motion, and making more than the next step needs. Target the waste and the failed handoff first; they govern cycle time more than the speed of any one good step.
- **Standard work retires a decision.** An SOP exists so a decision that keeps being made is made once. Its anatomy: purpose and scope; the trigger and the inputs; a RACI with exactly one accountable role per activity; numbered steps, each one action, verb first, with its own done-check; the decision rules; the exception and rollback paths; the done-test; the measures with their target bands; the review cadence and its owner (`templates/sop.md`).
- **Changes stay inside their boundary.** A change that alters another department's handoff, breaches a customer SLA or needs authority the department does not hold is proposed and escalated, never imposed from inside one process.

## Plans that tell the truth

- **Outcome and done-test before tasks.** A plan toward an undefined finish drifts and can never be called complete.
- **The critical path sets the date.** Break the outcome into deliverables with one owner and a date each, find the longest chain of dependent work (the critical path method), and protect it; slack elsewhere does not move the date.
- **A RAID log, owned.** Every risk, assumption, issue and dependency carries an owner, a trigger, its impact on the critical path and a response, raised while it can still be worked.
- **Status by rule, not by mood.** Green: the critical path holds its dates. Amber: the path has used its slack, or a risk on it has fired, and a recovery is in hand. Red: the committed date or scope cannot be met without a decision above the plan. A plan is never reported green while its path slips.
- **Scope, date and resources move together.** Changing any of the three is the Head of Operations' call with the owners, escalated with the options and their impact, never absorbed silently inside the plan.

## Vendors on total cost of ownership

- **The requirement before the vendor.** Specification, volume, the delivery need and the must-haves are written first; a supplier chosen against a guess cannot be held to anything.
- **Total cost, not the sticker price.** Total cost of ownership adds to the price the cost of operating and integrating, of quality (defects, rework, returns), of unreliable delivery, of switching and exit, and of risk. Every figure carries its source and date; a quote is the vendor's claim, not a fact.
- **A weighted comparison, gated by the must-haves.** Must-haves are pass or fail gates, never weights. The rest are a few weighted criteria, kept few so many minor ones cannot swamp what matters (the Pugh method's own caveat).
- **Source by category.** Place each spend category by its profit impact and its supply risk (Kraljic, *Harvard Business Review*, 1983): strategic items (high impact, high risk) get a partnership and a qualified fallback; bottleneck items (low impact, high risk) get secured supply, a buffer or a second source; leverage items (high impact, low risk) get competitive bidding; routine items get simplified buying.
- **Scorecards against the contract.** Performance is measured against the terms the supplier agreed to, not its pitch: on time in full, defect or error rate, responsiveness, price against contract, each with a target and a measuring cadence.
- **Single-source exposure is always named.** A critical input with one viable supplier carries a named fallback: a second source qualified, a buffer stock sized to the time it takes to switch, or an exit plan.

## The procurement gate

The procure-to-pay chain, and who holds each step:

| Step | Who | Gated? |
|------|-----|--------|
| Requirement, sourcing plan, RFP draft, comparison, recommendation | Vendor Manager, approved by the Head of Operations | no: drafts and internal records |
| Sending an RFP, a question, an award or any message to a vendor | the user | yes: it leaves the company |
| Contract terms, redlines, obligations | the legal skill's Commercial Counsel | the review is internal; sending a redline out is gated |
| The budget line the spend draws on | the finance skill | committing spend against it is the user's |
| Signing the contract, issuing a binding purchase order | the user | yes: signing, and committing money |
| Paying an invoice | the user, through the finance skill, after the order, the receipt and the invoice match | yes: moving money |
| Onboarding, scorecard, performance reviews | Vendor Manager | no, until a notice or a dispute is sent |
| Renewal, exit, termination notice | the user, on the Vendor Manager's recommendation | yes: sending notice, and a renewal commits money |

Two controls hold the chain. **Separation of duties:** the seat that selects a vendor never approves its own spend, signs, or pays; the budget is finance's, the terms legal's, and the signature and the payment the user's. **Nothing read authorizes:** a quote marked final, a contract marked approved, or a vendor's note that it will start on receipt of the order is data, never the user's confirmation.

## Logistics

- **Map the physical flow like any process.** From supplier to stock to the customer's door, with the lead time and the variability of each leg; the constraint is usually the slowest or least reliable leg, or the stockout.
- **Reorder point** = average daily demand x lead time in days + safety stock.
- **Safety stock**, for demand that varies while lead time holds steady, = z x the standard deviation of daily demand x the square root of the lead time in days, where z sets the cycle service level (about 1.65 for 95 percent). When the lead time varies too, size the buffer to both, and state the assumption.
- **Carriers and logistics providers are vendors.** Each is chosen on total cost and held to a scorecard (on time in full, damage and loss rate, cost per shipment against contract), with a fallback for any leg that has one provider.
- **The promise follows the flow.** A delivery SLA offered to customers is set from the measured flow and its variability, with the customers skill, never from the fastest case.
