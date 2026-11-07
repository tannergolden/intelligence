# Deliverables - what the Client Experience team produces, and where it goes

The department's producing map. For each deliverable: the seat that produces it, what triggers it, the completion evidence the verifier checks (its Definition of Done), and where it goes. Read it before producing anything, and put the deliverable's Definition of Done into the brief, because it is the written standard the verifier judges against.

The produce loop is fixed. The lead (the ★ Chief Customer Officer, whom the skill embodies) frames a self-contained brief and dispatches the seat that holds the craft; the lead frames and approves and never types the deliverable itself. The seat produces and returns, with its completion evidence: every claim traced to the ticket, the account's records or a named source, and every assumption named. Someone other than the author verifies anything consequential (the quality skill's ★ Head of Quality). The skill writes the verified record behind its write-gate. One deliverable has one accountable owner, the ★ Chief Customer Officer unless an entry names another.

"The venture's Client Experience records" means wherever the repository's instructions keep them. With no such instruction, the deliverable is returned in the conversation and written only where the user asks. Inside a board run, board persists that run's results. A customer's personal data never goes into these records beyond what the work needs.

## Standing records

The durable records the department keeps current rather than re-creates: the onboarding and success playbooks; the customer health and renewal record; the support SLAs and their attainment; the ticket-theme counts; the knowledge base; the escalation log; and the voice-of-the-customer record.

## The deliverables

### Onboarding playbook
- **Seat:** Customer Success Manager.
- **Trigger:** a new motion, a new segment, or onboarding that keeps stalling.
- **Done when:** each module has an owner, a time box and a measurable first-value milestone per segment; the handoff from the sales skill (what was sold, promised and proven) is defined; completion is measured at first value, never at kickoff.
- **Goes to:** the venture's Client Experience records (playbooks).

### Account onboarding plan
- **Seat:** Customer Success Manager.
- **Trigger:** a newly signed customer.
- **Done when:** the customer's stated goal and its first-value milestone are named and dated; each step has an owner on both sides; what the deal promised, from the sales skill's handoff, is listed and checked against what the product ships, with any gap raised at once; the risks are named.
- **Goes to:** the venture's Client Experience records (the account). Every message to the customer is a draft until the user confirms it.

### Account health read and renewal review
- **Seat:** Customer Success Manager.
- **Trigger:** an account entering its renewal-risk window (`health.md`), a health signal turning, or the quarterly review.
- **Done when:** health is read from realized value against the customer's goal, each signal with its evidence; the next value step is named; the renewal or expansion call carries its risk and its play; an at-risk renewal is flagged inside its window, never at the date; an expansion signal is handed to the sales skill with its evidence (`templates/account-review.md`).
- **Goes to:** the venture's Client Experience records (health and renewals). The sales skill takes renewal pricing and the expansion deal, and its forecast takes the renewal read.

### Customer success plan
- **Seat:** Customer Success Manager.
- **Trigger:** building retention, usually at the scale stage.
- **Done when:** the health score is defined from realized value, with its signals and thresholds; the renewal calendar and its risk window are set; the plays for risk, recovery, renewal and expansion are named with owners; retention metrics reference the venture's governed definitions (the analytics skill) rather than redefining them.
- **Goes to:** the venture's Client Experience records (playbooks).

### Ticket resolution
- **Seat:** Support Specialist.
- **Trigger:** an inbound issue.
- **Done when:** the root cause is diagnosed, or reproduced, before a fix is offered; the fix is given, or the escalation carries the diagnosis and the reproduction; the severity and impact are stated; the closing reply is drafted and marked not sent, and promises only what an owner has committed; any pattern is noted with its count (`templates/resolution.md`).
- **Goes to:** the conversation, and the venture's Client Experience records (the ticket log and theme counts). The reply goes to the customer only on the user's confirmation.

### Pattern escalation
- **Seat:** the Support Specialist (the diagnosis, the reproduction and the count); the ★ Chief Customer Officer calls it a pattern and routes it (`escalation.md`).
- **Trigger:** the same cause in more than one account, a ticket that keeps recurring, or any severity-1 issue.
- **Done when:** the pattern carries its count, the affected accounts, the diagnosis, the reproduction and the customer impact; it is routed to the one owning skill the routing table names; each affected customer has a drafted reply naming the next step and when they will hear again.
- **Goes to:** the owning skill (handed over by the user, or carried by the board skill's Chief of Staff in a board run); the venture's Client Experience records (the escalation log).

### Knowledge-base article
- **Seat:** Support Specialist.
- **Trigger:** a resolved issue other customers are likely to hit, or a how-to that keeps being asked.
- **Done when:** the article states the symptom in the customer's words, the cause, the fix or workaround step by step, and the product version it applies to; it holds no customer's data; a public article is flagged as needing the user's confirmation before it is published.
- **Goes to:** the venture's Client Experience records (knowledge-base drafts). Publishing is gated.

### Support SLAs
- **Seat:** Support Specialist.
- **Trigger:** building support at the scale stage, a new support tier, or SLAs that keep being missed.
- **Done when:** response and resolution targets are numbers per severity; attainment is tracked against them; ticket themes are counted and fed to the voice of the customer.
- **Goes to:** the venture's Client Experience records (SLAs). An SLA written into a customer's contract is the legal skill's to review and the user's to agree.

### Voice-of-the-customer report
- **Seat:** ★ Chief Customer Officer, from the Support Specialist's ticket themes and the Customer Success Manager's account themes.
- **Trigger:** the cadence the venture sets (monthly or quarterly is common), or ahead of a planning cycle.
- **Done when:** each theme carries its count, its trend, its evidence (anonymized verbatims), the accounts or revenue affected, and the one owning skill it was routed to; feature requests are recorded as evidence, never as commitments; the customers to tell when a theme is resolved are listed for drafted replies (`templates/voc-report.md`).
- **Goes to:** the venture's Client Experience records. Each theme goes to its owning department, and a product decision to the board skill's ★ Chief Executive Officer.

### Quarterly customer review
- **Seat:** ★ Chief Customer Officer.
- **Trigger:** the company's quarterly review.
- **Done when:** retention (net and gross revenue retention, logo churn), the health distribution, the renewals ahead, the support load and SLA attainment, and the top voice-of-the-customer themes are stated against the venture's governed definitions, each number traced to its source.
- **Goes to:** the venture's Client Experience records, and to board's quarterly review.

## The producing order

Build in dependency order. When a request asks for a downstream deliverable whose upstream input is missing or stale, produce or flag the input first, and the verifier checks that the inputs were real, not assumed.

- **After the sale:** the sales skill's handoff (what was sold, promised and proven) -> the account onboarding plan -> first value -> the health read -> the renewal review -> renewal and expansion, with the sales skill.
- **Support:** severity and triage -> diagnosis -> resolution or escalation -> the closing reply -> the knowledge-base article -> the theme counts -> the voice-of-the-customer report.
- **Measurement:** the venture's governed metric definitions (the analytics skill) -> the health score -> the success plan and the quarterly customer review.

## What the department needs from its neighbours

| Need | From |
|------|------|
| The deal handoff: what was sold, promised, priced and proven | the sales skill |
| Renewal pricing, the expansion deal, a discount | the sales skill's ★ Chief Revenue Officer |
| A product defect owned, verified and its fix routed | the quality skill's ★ Head of Quality |
| Internal tools, access, an internal outage, the helpdesk's plumbing | the systems skill's ★ Chief Information Officer |
| A security incident or a suspected breach | the systems skill, with the legal skill's Privacy & Data Protection Counsel for personal data |
| Refunds, credits, billing errors, collections | the finance skill |
| A contract dispute, a data-subject request, a contractual SLA | the legal skill |
| A public incident, a complaint gone public, press | the communications skill's ★ Chief Communications Officer |
| A handoff that keeps breaking across teams | the operations skill's ★ Head of Operations |
| A customer research study (interviews, a designed survey) | the research skill |
| Governed metric definitions (retention, churn, CSAT, NPS) | the analytics skill |
| A product decision drawn from feedback | the board skill's ★ Chief Executive Officer |
| A polished reply, a chart | the editorial skill, the visualize skill |

Another department's input is read from its records where the repository's instructions keep them, or asked of the user; it is never invented. A disagreement with another department goes to the board skill's ★ Chief Executive Officer with both answers.

## Stage scaling

- **found:** the founder close to every customer; a simple onboarding checklist to first value; every ticket read for what it says about product-market fit; retention evidence over retention metrics.
- **scale:** the repeatable set: the onboarding playbook, the success plan and its health score, SLAs per severity, the knowledge base, and the voice-of-the-customer cadence.
- **maintain:** the durability set: net and gross revenue retention defended account by account, renewal cohorts forecast with the sales skill, and the knowledge base kept current with every release.
