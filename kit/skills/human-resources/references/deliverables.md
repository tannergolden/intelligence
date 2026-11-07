# Deliverables - what the Human Resources team produces, and where it goes

The department's producing map: each deliverable, the seat that produces it, what triggers it, the completion evidence its verifier checks before it lands, and where it goes. Every deliverable resolves to one producing seat and one accountable lead, the Chief Human Resources Officer. A deliverable with no completion evidence cannot be verified and does not land. The verifier is the quality-assurance skill's ★ Head of Quality, except for a profile batch, which the legal-and-compliance skill's Privacy & Data Protection Counsel reviews blind.

**Where it goes.** The company's Human Resources records live wherever the repository's instructions keep the company's department records: the org chart, the bands, the hiring plan, the open roles with their role cards and interview kits, the onboarding plans, the review cycle, the wellbeing program, and the people records. A person's record goes only into a private repository made to hold the company's people records (`doctrine.md`). The user's profile goes only into a profile repository, and the user's career and wellbeing plans only into a repository made to hold the user's personal context (SEC-003). With no such instruction, a company deliverable is returned in the conversation and filed only where the user asks, and the user's personal context stays in the conversation. Inside an administration run, the administration skill persists that run's results.

**Every deliverable, always.** Each market figure carries its named source and date, each rule its official source and date, and each health figure its official public-health source and date; each fact about a person or a role traces to the records or the user; no sensitive identifier appears; no real person's pay, promotion or exit is decided in it (those are recommended, and the user decides); and no diagnosis, treatment or medication advice appears in it.

## The company's deliverables

### Org design and org chart
- **Seat:** ★ Chief Human Resources Officer; the analyst supplies the current records.
- **Trigger:** a reorg, a funding round, a stage change, a new team.
- **Completion evidence:** every role has one manager and a charter; spans are stated; the next-hire sequence ties to the strategy; every current person is placed, reconciled against the records.
- **Goes to:** the org chart. **Needs:** the administration skill for the strategy, and for any reorg as a company decision.

### Hiring plan
- **Seat:** ★ Chief Human Resources Officer.
- **Trigger:** a planning cycle, a raise, a new goal.
- **Completion evidence:** each hire names the bottleneck or goal it serves; headcount by quarter, with each role's level and band; costed by the finance-and-accounting skill against the company's model and runway; inside the headcount the administration skill approved, or marked as a request for it.
- **Goes to:** the hiring plan. **Needs:** the finance-and-accounting skill for payroll cost; the administration skill for a headcount call across the company.

### Role card and job description
- **Seat:** ★ Chief Human Resources Officer (`templates/role-card.md`).
- **Trigger:** an approved seat.
- **Completion evidence:** the outcomes are specific and measurable; the must-haves are few, and each is tested in the loop; the level and band are attached with the band's source; the posting carries the pay range where the work location's law requires one, checked and dated; no requirement screens people out without a job-related reason.
- **Goes to:** the open roles. **Needs:** the hiring plan or an approved seat, and the bands.

### Interview loop and scorecard
- **Seat:** ★ Chief Human Resources Officer (`templates/interview-loop.md`).
- **Trigger:** a role opens.
- **Completion evidence:** every competency maps to a must-have on the role card, and every must-have is tested; every stage has its owner, its core questions and an anchored scale; the same core questions go to every candidate; no question touches a protected characteristic or, where the location bars it, pay history; the debrief rule requires written scores first.
- **Goes to:** the open roles, with the role card.

### Compensation bands
- **Seat:** ★ Chief Human Resources Officer sets the ranges; the HRIS and People Operations Analyst places the current people in them.
- **Trigger:** a hiring wave, an annual review, a new level or location.
- **Completion evidence:** each band is a range by level and function, naming its benchmark source and date and its location differential; the ranges were set before current pay was seen; every current person is placed, with each outlier flagged; the equity guidelines by level are stated; the cost is checked by the finance-and-accounting skill.
- **Goes to:** the bands. **Gated:** a band change is framed by the administration skill's ★ Chief Executive Officer and decided by the user.

### Offer
- **Seat:** ★ Chief Human Resources Officer; the analyst places it against the band and peers (`templates/offer.md`).
- **Trigger:** a candidate chosen.
- **Completion evidence:** the base sits inside the band, or the exception is named and escalated; internal equity is checked against peers at the level without naming them; every number in the letter matches the band, the plan and the summary; the contingencies and the expiry are stated; an equity grant is marked for the company's board and the cap table; no placeholder survives; the offer is marked unsent.
- **Goes to:** the conversation until the user sends it; the person's record once accepted. **Needs:** the legal-and-compliance skill for the employment agreement and the IP and confidentiality agreement; the finance-and-accounting skill for the cost and the grant.

### Onboarding plan
- **Seat:** ★ Chief Human Resources Officer (`templates/onboarding.md`).
- **Trigger:** an accepted offer.
- **Completion evidence:** every task has an owner and a date; the work-authorization check carries the deadline the location's law sets, checked and dated; accounts, devices and access are requested from the information-technology skill; the 30, 60 and 90-day goals are drawn from the role card's outcomes.
- **Goes to:** the onboarding plans. **Needs:** the information-technology skill for accounts and devices.

### Performance cycle and review
- **Seat:** ★ Chief Human Resources Officer (`templates/performance-review.md`).
- **Trigger:** a review cycle, a promotion case, a performance concern.
- **Completion evidence:** the cycle states its cadence, framework and calibration step; each review rates against the role card's outcomes and the level's expectations with specific, dated evidence; ratings are calibrated before they are final; the recommended outcome carries its written reason and is left to the user; a plan that may end in an exit is routed to the legal-and-compliance skill before it starts.
- **Goes to:** the review cycle; an individual review to the person's record, in a private repository only.

### Wellbeing program
- **Seat:** Wellbeing Specialist; the lead approves it (`templates/wellbeing-plan.md`, its program section).
- **Trigger:** a request for a wellbeing program, a benefits guide for employees, a stage change or a hiring wave.
- **Completion evidence:** the offering and how employees use it are stated; the health benefits are explained from the plan's own documents; it is aggregate only, with no individual's health in it; benefits plan design is referred to a licensed benefits broker and any accommodation to the legal-and-compliance skill; nothing in it diagnoses, treats or advises on medication.
- **Goes to:** the wellbeing program, in the company's Human Resources records.

### People records and reports
- **Seat:** HRIS and People Operations Analyst.
- **Trigger:** any change to a person or a position (a hire, a move, a pay change, an exit), a reconciliation, or a report (headcount, tenure, attrition, spans of control).
- **Completion evidence:** every claim traces to a field; there is one record per person and per position, with the uniqueness check run before any new record; every discrepancy is flagged with both entries named, never silently resolved; no sensitive identifier is held as a value.
- **Goes to:** the people records, in a private repository only.

## The user's own deliverables

### The approved profile batch
- **Seats:** the skill, embodied as the research-and-development skill's UX and Design Research Lead, interviews and keeps the ledger; the public-relations skill's Writer composes the batch; the legal-and-compliance skill's Privacy & Data Protection Counsel reviews it blind (`roster.md`, `templates/proposal-batch.md`).
- **Trigger:** "interview me", "fill out my profile", "confirm my unconfirmed profile entries", a facet the user names, or a facet found thin.
- **Completion evidence:** every unmarked line is verbatim-traceable to a stated ledger answer, and every inference carries the full marker and `unconfirmed` (`provenance.md`); the blind review's verdicts are applied, one round; no skip or refusal appears anywhere; no person, event, date or decision sits in a profile line; a sensitive facet was opened only on the user's opt-in; the user approved each kept line explicitly; afterward, a search for `unconfirmed` finds every pending proposal.
- **Goes to:** a profile repository, where its instructions put each facet, with its checks run; anywhere else, the conversation. Record offers go only where a profile repository's instructions keep such records, after the analyst's uniqueness check.

### Career plan and skills map
- **Seat:** ★ Chief Human Resources Officer; the analyst supplies the user's career record (`templates/career-plan.md`).
- **Trigger:** "plan my career", "what skills do I need for this role", "map my skills", a promotion case or a review of the user's own.
- **Completion evidence:** the direction is stated in the user's own words; each target role's outcomes and must-haves come from a named, dated source; each skill is placed from the user's own rating or evidence; the development plan names the few gaps that matter, how and by when each is closed, and how the user will know; the hand-offs (the job search and pay talks, an offer's money, the prose, learning the subject) are named.
- **Goes to:** a repository made to hold the user's personal context; anywhere else, the conversation.

### Wellbeing plan and check-up schedule
- **Seat:** Wellbeing Specialist (`templates/wellbeing-plan.md`).
- **Trigger:** "help me build a sleep routine", "help me start exercising", "a routine for stress", "plan my check-ups", "how do I use my health benefits".
- **Completion evidence:** the request was screened for a crisis and for clinical questions first; every figure comes from an official public-health source with its date; each routine has its cue, its smallest version and its check-in date; each check-up item has its interval, its source and date, and "confirm with your clinician"; each benefit is drawn from the user's own plan documents; the referrals are named; no diagnosis, treatment, medication, dose, condition detail or result appears.
- **Goes to:** a repository made to hold the user's personal context; anywhere else, the conversation.

## The producing chain

For a company: org design, then the hiring plan and the bands, then the role card and job description, then the interview loop, then the offer, then onboarding, then performance. Hiring without the bands creates the very inconsistency the bands exist to prevent, and a loop without a role card tests for nothing in particular. For the user: the direction, then the target role's card, then the skills map, then the development plan; and for wellbeing, the screen, then the goal and constraints, then the routine. Before producing a downstream deliverable, confirm its upstream input exists and is current; if not, produce or flag it first.

## Hand-offs to other departments

| To | What |
|----|------|
| the finance-and-accounting skill | payroll cost in the company's model; the cap-table effect of an equity grant; a signing bonus or a payroll change; the money in the user's own job offer; choosing a health plan, and a health savings or flexible spending election |
| the legal-and-compliance skill | the employment and contractor agreements, the IP and confidentiality agreement, worker classification, restrictive covenants, immigration, an accommodation, any exit with legal risk, and the retention line for candidate data |
| the information-technology skill | a new hire's accounts, devices and access, and their removal at an exit |
| the public-relations skill | an announcement to the company or the public; the user's cover letter, bio or other prose |
| the sales-and-marketing skill | the user's job search, networking, personal brand, and negotiating pay or a deal |
| the research-and-development skill | learning a subject a development plan calls for; a labor-market study; a new agent seat on one of the kit's teams |
| the business-intelligence skill | a chart of headcount or attrition; tracking the user's habits and metrics |
| the administration skill | a headcount call across the company, a reorg as a company decision, a band change; the user's life goals, priorities and calendar |
