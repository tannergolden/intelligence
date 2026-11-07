# Deliverable dependency chains

*The producing order and handoffs across the departments: what must exist before what, so a deliverable is never built on a missing input. Many chains cross from one department skill to another, which is exactly the sequencing board owns.*

A deliverable rarely stands alone. Build in dependency order, and when a request asks for a downstream artifact whose upstream input is missing, produce or flag the input first. The chains below are the common ones; the skill that owns each link is in `routing.md`, and each department skill's `references/deliverables.md` names its own files.

## Product
Evidence about users and markets (the research skill) to the options worth weighing (the discover skill) to the product decision and the requirements (the CEO, recorded in `Administration/Roadmap.md`) to the architecture and the build (the develop skill) to the release plan to the test plan and the requirements-traceability matrix (the quality skill). The CEO cannot decide what the evidence has not validated; the develop skill cannot build what the requirements have not defined.

## Finance
Strategy and OKRs (board) to the operating budget to the monthly close (actuals) to the forward model (the finance skill), which board's review cadence reads into the board deck. The model's assumptions trace to the strategy; the board deck reconciles plan against actuals.

## Go-to-market
Positioning and ICP to the GTM plan to the demand-gen campaign and content to sales enablement to the pipeline and forecast (all the sales skill's), then onboarding and success (the customers skill), with the communications skill's brand-voice gate on anything published. Sales cannot enable what marketing has not positioned, and cannot sell on terms the legal skill has not cleared.

## Legal and the founding clocks
The entity and its formation pack (the legal skill) before the cap table, the founder stock, and the 83(b) and QSBS clocks (the finance skill, every change Founder-gated); the contract terms (the legal skill) before the sales motion sells on them; the privacy obligations (the legal skill) before the systems and the product handle personal data.

## Data
Metric definitions (the analytics skill's semantic layer) to the data model and pipelines to the dashboards and the scorecard. A dashboard built before the metric definitions are agreed reports numbers no one trusts.

## People and operations
Org design to the hiring plan and comp bands (the people skill, the plan costed against the finance skill's runway) to onboarding to the SOPs and runbooks (the operations skill). Hiring without the comp bands creates the very inconsistency the bands exist to prevent.

## The rule
Before producing a downstream artifact, confirm its upstream input exists and is current; if not, the lead produces or flags it first (see `specialist-dispatch.md`). Across departments, board sequences the parts, and a department's part does not start on another department's missing input. The independent verifier (`verification.md`) checks that a deliverable's inputs were real, not assumed.
