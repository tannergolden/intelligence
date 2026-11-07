# Deliverables - what the Human Resources team produces, and where it goes

The department's producing map: each deliverable, the seat that produces it, what triggers it, the completion evidence the quality skill's ★ Head of Quality checks before it lands, and where it goes. Every deliverable resolves to one producing seat and one accountable lead, the Chief Human Resources Officer. A deliverable with no completion evidence cannot be verified and does not land.

**Where it goes.** The company's Human Resources records live wherever the repository's instructions keep the company's department records: the org chart, the bands, the hiring plan, the open roles with their role cards and interview kits, the onboarding plans, the review cycle, and the people records. A person's record goes only into a private repository made to hold the company's people records (`doctrine.md`). With no such instruction, a deliverable is returned in the conversation and filed only where the user asks. Inside a board run, the board skill persists that run's results.

**Every deliverable, always.** Each market figure carries its named source and date and each rule its official source and date; each fact about a person or a role traces to the records or the user; no sensitive identifier appears; and no real person's pay, promotion or exit is decided in it: those are recommended, and the user decides.

## The deliverables

### Org design and org chart
- **Seat:** ★ Chief Human Resources Officer; the analyst supplies the current records.
- **Trigger:** a reorg, a funding round, a stage change, a new team.
- **Completion evidence:** every role has one manager and a charter; spans are stated; the next-hire sequence ties to the strategy; every current person is placed, reconciled against the records.
- **Goes to:** the org chart. **Needs:** the board skill for the strategy, and for any reorg as a company decision.

### Hiring plan
- **Seat:** ★ Chief Human Resources Officer.
- **Trigger:** a planning cycle, a raise, a new goal.
- **Completion evidence:** each hire names the bottleneck or goal it serves; headcount by quarter, with each role's level and band; costed by the finance skill against the company's model and runway; inside the headcount the board skill approved, or marked as a request for it.
- **Goes to:** the hiring plan. **Needs:** the finance skill for payroll cost; the board skill for a headcount call across the company.

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
- **Completion evidence:** each band is a range by level and function, naming its benchmark source and date and its location differential; the ranges were set before current pay was seen; every current person is placed, with each outlier flagged; the equity guidelines by level are stated; the cost is checked by the finance skill.
- **Goes to:** the bands. **Gated:** a band change is framed by the board skill's ★ Chief Executive Officer and decided by the user.

### Offer
- **Seat:** ★ Chief Human Resources Officer; the analyst places it against the band and peers (`templates/offer.md`).
- **Trigger:** a candidate chosen.
- **Completion evidence:** the base sits inside the band, or the exception is named and escalated; internal equity is checked against peers at the level without naming them; every number in the letter matches the band, the plan and the summary; the contingencies and the expiry are stated; an equity grant is marked for the company's board and the cap table; no placeholder survives; the offer is marked unsent.
- **Goes to:** the conversation until the user sends it; the person's record once accepted. **Needs:** the legal skill for the employment agreement and the IP and confidentiality agreement; the finance skill for the cost and the grant.

### Onboarding plan
- **Seat:** ★ Chief Human Resources Officer (`templates/onboarding.md`).
- **Trigger:** an accepted offer.
- **Completion evidence:** every task has an owner and a date; the work-authorization check carries the deadline the location's law sets, checked and dated; accounts, devices and access are requested from the systems skill; the 30, 60 and 90-day goals are drawn from the role card's outcomes.
- **Goes to:** the onboarding plans. **Needs:** the systems skill for accounts and devices.

### Performance cycle and review
- **Seat:** ★ Chief Human Resources Officer (`templates/performance-review.md`).
- **Trigger:** a review cycle, a promotion case, a performance concern.
- **Completion evidence:** the cycle states its cadence, framework and calibration step; each review rates against the role card's outcomes and the level's expectations with specific, dated evidence; ratings are calibrated before they are final; the recommended outcome carries its written reason and is left to the user; a plan that may end in an exit is routed to the legal skill before it starts.
- **Goes to:** the review cycle; an individual review to the person's record, in a private repository only.

### People records and reports
- **Seat:** HRIS and People Operations Analyst.
- **Trigger:** any change to a person or a position (a hire, a move, a pay change, an exit), a reconciliation, or a report (headcount, tenure, attrition, spans of control).
- **Completion evidence:** every claim traces to a field; there is one record per person and per position, with the uniqueness check run before any new record; every discrepancy is flagged with both entries named, never silently resolved; no sensitive identifier is held as a value.
- **Goes to:** the people records, in a private repository only.

## The producing chain

Org design, then the hiring plan and the bands, then the role card and job description, then the interview loop, then the offer, then onboarding, then performance. Hiring without the bands creates the very inconsistency the bands exist to prevent, and a loop without a role card tests for nothing in particular. Before producing a downstream deliverable, confirm its upstream input exists and is current; if not, produce or flag it first.

## Hand-offs to other departments

| To | What |
|----|------|
| the finance skill | payroll cost in the company's model; the cap-table effect of an equity grant; a signing bonus or a payroll change |
| the legal skill | the employment and contractor agreements, the IP and confidentiality agreement, worker classification, restrictive covenants, immigration, any exit with legal risk, and the retention line for candidate data |
| the systems skill | a new hire's accounts, devices and access, and their removal at an exit |
| the communications skill | an announcement to the company or the public |
| the board skill | a headcount call across the company, a reorg as a company decision, a band change |
