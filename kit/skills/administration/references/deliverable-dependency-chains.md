# Deliverable dependency chains

*The producing order and handoffs across the departments: what must exist before what, so a deliverable is never built on a missing input. Many chains cross from one department skill to another, which is exactly the sequencing administration owns.*

A deliverable rarely stands alone. Build in dependency order, and when a request asks for a downstream artifact whose upstream input is missing, produce or flag the input first. The chains below are the common ones; the skill that owns each link is in `routing.md`, and each department skill's references name its own files.

## Product
Evidence about users and markets (the research-and-development skill) to the options worth weighing (the research-and-development skill) to the product decision (the CEO, recorded in `Administration/Decisions.md`) to the roadmap and the requirements (the research-and-development skill's `Roadmap.md`) to the architecture and the build (the research-and-development skill) to the release plan to the test plan and the requirements-traceability matrix (the quality-assurance skill). The CEO cannot decide what the evidence has not validated; the research-and-development skill cannot build what the requirements have not defined.

## Finance
Strategy and OKRs (administration) to the operating budget to the monthly close (actuals) to the forward model (the finance-and-accounting skill), which administration's review cadence reads into the board deck. The model's assumptions trace to the strategy; the board deck reconciles plan against actuals.

## Go-to-market
Positioning and ICP to the GTM plan to the demand-gen campaign and content to sales enablement to the pipeline and forecast (all the sales-and-marketing skill's), then onboarding and success (the customer-experience skill), with the public-relations skill's brand-voice gate on anything published. Sales cannot enable what marketing has not positioned, and cannot sell on terms the legal-and-compliance skill has not cleared.

## Legal and the founding clocks
The entity and its formation pack (the legal-and-compliance skill) before the cap table, the founder stock, and the 83(b) and QSBS clocks (the finance-and-accounting skill, every change Founder-gated); the contract terms (the legal-and-compliance skill) before the sales motion sells on them; the privacy obligations (the legal-and-compliance skill) before the systems and the product handle personal data.

## Data
Metric definitions (the business-intelligence skill's semantic layer) to the data model and pipelines to the dashboards and the scorecard. A dashboard built before the metric definitions are agreed reports numbers no one trusts.

## People and operations
Org design to the hiring plan and comp bands (the human-resources skill, the plan costed against the finance-and-accounting skill's runway) to onboarding to the SOPs and runbooks (the operations-and-logistics skill). Hiring without the comp bands creates the very inconsistency the bands exist to prevent.

## A personal decision and what follows it
The Founder's goals and values (what they say, or the human-resources skill's profile where a private repository holds it) to each convened department's view (finance-and-accounting on the money, legal-and-compliance on the lease or contract, operations-and-logistics on the logistics, human-resources on career and wellbeing, sales-and-marketing on the negotiation) to the Founder's call to the work that carries it out: for a move, the budget (finance-and-accounting) and the lease review (legal-and-compliance) before the move plan (operations-and-logistics), and the plan before the messages telling people (public-relations). Nothing is signed, paid or sent before the Founder confirms it.

## The rule
Before producing a downstream artifact, confirm its upstream input exists and is current; if not, the lead produces or flags it first (see `specialist-dispatch.md`). Across departments, administration sequences the parts, and a department's part does not start on another department's missing input. The independent verifier (`verification.md`) checks that a deliverable's inputs were real, not assumed.
