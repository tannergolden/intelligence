# Deliverables - what the Operations & Logistics (O&L) team produces

What the department produces for a company or venture the user runs and for the user's own life: each deliverable, the seat that produces it, what calls for it, the evidence that it is done, and where it goes. Read it before framing a standard or deep run. Every deliverable resolves to one producing seat, one accountable lead (the ★ Head of Operations), one verifier who did not make it (the quality-assurance skill's ★ Head of Quality), and one writer (this skill, or the administration skill inside a company-wide run). A deliverable with no done-test or no home is not producible: that is a finding to raise, not a gap to improvise around.

## Where the work goes

A company's deliverable lands in the venture's **Operations & Logistics records**, wherever the repository's instructions keep a venture's department records (a department folder inside the venture's record, a repository of its own, or a location they name). A household deliverable is the user's personal context: it lands only in a repository whose instructions (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files) say it is a private one made to hold it (the Constitution's SEC-003), where those instructions put it. With no such instruction, either one is returned in the conversation, and a file is written only where the user asks.

The department keeps four standing assets for a company, updated rather than re-created run to run:

- **The SOP and runbook library** - every procedure the venture runs the same way twice.
- **The operations KPI view** - cycle time, throughput and on-time attainment, each against its target band.
- **The vendor register and scorecards** - every supplier, carrier and logistics provider, its terms on file with the legal-and-compliance skill, its scorecard and its supply risk.
- **The live program plans** - working records, kept while a program runs and closed with its outcome when it ships.

For the household, where a private repository made to hold it says so, it keeps the matching three: the household's routines, the live plans (a move, a trip, a renovation), and the providers who work on the home with their scope, quotes and warranty dates. No record holds a credential, a door or alarm code, a passport, ID or account number, or a card or bank detail: it says where the document lives.

## The deliverables

### SOP or runbook - Process Analyst

- **Trigger:** a process that lives in one head, a handoff that keeps breaking, a new hire who must run it, an audit, or a decision that keeps being re-made.
- **Done when:** every step is an action a stranger to the process can take as written; the trigger, the inputs and the output are named; the RACI names real roles, one accountable per activity, and no placeholders; the exception and rollback paths exist and are reachable from the main path; the done-test says how anyone can tell it ran right; each measure it is held to has a definition, a target band and a current value; the as-is map it came from is attached, with every inferred step marked as an assumption.
- **Needs from other departments:** the roles it assigns, from the human-resources skill's org design; tool steps, from the information-technology skill; a measure's definition, from the business-intelligence skill.
- **Shape:** `templates/sop.md`.

### Household routine - Process Analyst

- **Trigger:** a morning, an evening or a weekly reset that keeps failing, chores that fall to one person, a supply the household keeps running out of, or an errand loop that repeats.
- **Done when:** the routine's trigger (a time or an event) and its done-check are named; its steps are in order, verb first, each with one owner in the household; the constraint it relieves is named; a supply it covers has a reorder point or a standing order (`household.md`); a fallback exists for the bad week; any health content stays within routines, sleep, activity and nutrition habits, appointments and benefits.
- **Needs from other departments:** a wellbeing plan behind a habit, from the human-resources skill; tracking the habit, from the business-intelligence skill.
- **Shape:** `templates/sop.md`, cut to the fields a household needs (trigger, steps, owner, done-check, fallback).

### Program or project plan (the capacity and delivery plan) - Program & Project Manager

- **Trigger:** a change that crosses functions or weeks, a launch, a move, a migration, or any multi-step deliverable with a committed date.
- **Done when:** the outcome is one sentence with an observable done-test; every deliverable has one owner and a date; the critical path is named and the slack on the rest shown; every risk, assumption, issue and dependency has an owner, a trigger and its impact on the path; the status is on track, or the slip is escalated to the Head of Operations with the recovery options, and never reported on track while the path slips; every act in the plan that waits for the user is listed.
- **Needs from other departments:** the budget line it draws on (finance-and-accounting); staffing (human-resources); tool changes (information-technology); the company-wide execution plan it serves, when there is one (the administration skill's Chief Operating Officer).
- **Shape:** `templates/program-plan.md`.

### Move or trip plan - Program & Project Manager, with the Vendor Manager for movers and other providers

- **Trigger:** a move, a trip, a renovation or an event in the user's own life.
- **Done when:** the outcome and its done-test are stated; the plan works back from the fixed dates (a lease end, a closing, a flight, a first day of school or work); the items with the longest lead time come first (documents, visas and entry rules, movers, scarce bookings) with their lead times; every current fact (an entry rule, a cancellation deadline) carries its official source and date; every booking lists its cancellation deadline and where its confirmation lives, never its sign-in; a move carries its address-change checklist and its inventory, and a trip its itinerary with slack around each connection that cannot be missed and its packing list; every booking, payment, signature and send is listed as the user's gated act.
- **Needs from other departments:** the budget (finance-and-accounting); a lease, a deposit or a dispute (legal-and-compliance); the new home's devices and network (information-technology); the user's calendar and commitments (administration).
- **Shape:** `templates/program-plan.md`.

### Vendor selection, scorecard or sourcing plan - Vendor Manager

- **Trigger:** a new purchase, a renewal, a supplier missing its SLA, a single-source exposure, or a spend category to source.
- **Done when:** the requirement and its must-haves are written before any vendor is named; the candidates are compared on total cost of ownership (price, operating and quality cost, delivery reliability, switching and exit cost, risk) with the source and date of every figure, not on price alone; the selection states its rationale and the trade-off it accepts; the scorecard metrics are defined, with a target and a way to measure each; any single-source dependency is named with its fallback; the contract terms are with the legal-and-compliance skill's Commercial Counsel and the spend sits inside a finance-and-accounting skill budget line; signing, paying and every send to the vendor are listed as the user's gated acts.
- **Needs from other departments:** the budget and the spend approval (finance-and-accounting); the contract terms (legal-and-compliance); for a tool, the technical requirement (information-technology).
- **Shape:** `templates/vendor-scorecard.md`.

### Contractor selection - Vendor Manager

- **Trigger:** work on the user's home (a repair, a remodel, a roof, a move, regular cleaning or care), or a contractor who keeps slipping.
- **Done when:** one written scope of work exists before any quote is compared; at least the quotes the user can get (three where the market allows) are restated against it; each contractor's license and insurance is checked at the issuing authority and dated, or marked unverified as a condition before signing; total cost covers materials, change orders, cleanup, the warranty on the work and the cost of a delay; payments are tied to milestones checked done, never paid in full up front; who pulls any permit is named; signing, the deposit, every payment and every message to the contractor are listed as the user's gated acts.
- **Needs from other departments:** the budget (finance-and-accounting); the contract and any dispute (legal-and-compliance); a refund or redo the user is owed when the work fails (customer-experience).
- **Shape:** `templates/vendor-scorecard.md`.

### Operations KPI view (the operations dashboard) - ★ Head of Operations

- **Trigger:** a review run, an SLA miss, a stage change into scale.
- **Done when:** each KPI (cycle time, throughput, SLA or on-time attainment, and any the venture adds) takes its definition from the business-intelligence skill's governed metric definitions rather than coining one, and carries a target band, a current value with its as-of date and source, and one owner; the constraint the numbers point at is named.
- **Needs from other departments:** the metric definitions and the data (business-intelligence).

### Supply and logistics plan - ★ Head of Operations, with the Process Analyst (the flow) and the Vendor Manager (suppliers, carriers, logistics providers)

- **Trigger:** a physical product, a new channel or market, a fulfillment or delivery SLA miss, a stockout, or a move.
- **Done when:** the flow from supplier to customer is mapped with its constraint named; each reorder point and safety stock is derived from stated demand, lead time and service level (`doctrine.md`); each carrier and logistics provider has a scorecard; the delivery SLA and its measure are stated; a single-source leg has a fallback.
- **Needs from other departments:** the inventory budget (finance-and-accounting); the delivery promise made to customers (the customer-experience skill).

## The producing chain

A deliverable is never built on a missing input. Before producing one, confirm its upstream input exists and is current; if it does not, produce it first inside the department or flag it and ask the skill that owns it, or the user. The verifier checks that the inputs were real, not assumed.

- **People and operations:** org design -> the hiring plan and pay bands -> onboarding -> the SOPs and runbooks. An SOP assigns roles the org design defines; with none defined, it names the roles it needs and flags them to the human-resources skill.
- **Measurement:** metric definitions -> the data model -> dashboards. The operations KPI view reads the business-intelligence skill's definitions; a KPI with no agreed definition is flagged, never invented.
- **Money:** the budget -> the purchase. A vendor selection without a finance-and-accounting skill budget line is a draft whose spend nobody has approved; a move or a trip without a budget the user has set is a plan whose spend nobody has agreed.
- **Contract:** requirement -> selection -> terms (the legal-and-compliance skill) -> signature and payment (the user) -> onboarding -> scorecard -> renewal or exit.
- **Strategy:** the strategy and the company-wide execution plan (the administration skill) -> the program plans that serve them; the user's goals and calendar (the administration skill) -> the household's plans.

## Stage scales the slice

When the administration skill's record names the venture's stage, scale the deliverables to it:

- **found** (idea to seed): protect runway and resist premature process. A checklist for the one process that keeps breaking, a short plan for the launch, a total-cost choice for the one input that matters; no SOP library before there is a repeatable thing to systematize.
- **scale** (Series A to C): the repeatable set. The SOP library, the KPI view against its bands, vendor scorecards, the program seat running cross-department work.
- **maintain** (established to mature): durability. SOPs reviewed on a cadence, renewals and single-source reviews, audits of the flow against its standard.

A household has no stage: scale its deliverables to the stakes, a checklist for a routine, a full plan for a move or a renovation.

## The produce loop

1. The lead frames the brief: the deliverable, its purpose, its inputs, the template to fill, the done-test above, the stage-scaled rigor, and the completion evidence to return.
2. The producing specialist builds it and returns it with that evidence; it persists nothing.
3. The lead assembles and approves it against the department's standard and names itself the accountable owner. This is a first-line check, not the verification.
4. The quality-assurance skill's ★ Head of Quality, who did not make it, verifies it against the done-test and the evidence. A FAIL returns to the lead, which re-dispatches the producing specialist on the cited defects; it is verified again before it lands.
5. The skill writes it behind the write-gate, or, inside a company-wide run, returns it for the administration skill to write.
