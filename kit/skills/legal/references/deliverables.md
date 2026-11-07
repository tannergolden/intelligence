# Deliverables - what the Legal & Compliance team produces, and where it goes

The department's producing map: each deliverable, the seat that produces it, what triggers it, the completion evidence the quality skill's ★ Head of Quality checks before it lands, and where it goes. Every deliverable resolves to one producing seat and one accountable lead, the General Counsel. A deliverable with no completion evidence cannot be verified and does not land.

**Where it goes.** The company's Legal & Compliance records live wherever the repository's instructions keep the company's department records, in the shape of `templates/legal-records.md` unless those instructions set another: the entity and IP record, the contracts, the obligations and filings calendar, the privacy record, and the matters. With no such instruction, a deliverable is returned in the conversation and filed only where the user asks. Inside a board run, the board skill persists that run's results.

**Every deliverable, always.** Each rule it turns on is cited with its official source and as-of date; nothing asserts a legal conclusion as settled without the caveat that a licensed lawyer confirms it where a referral trigger fires; and every gated act (sign, send, file, publish, notify) is marked as the user's, never taken.

## The deliverables

### Legal risk read
- **Seat:** ★ General Counsel, with the seat whose domain the matter touches.
- **Trigger:** any matter or decision with a legal edge: a launch, a deal, a practice, a "can we do this".
- **Completion evidence:** each material risk names the party it falls on and its mitigation; the remote is named without inflation and the trivial dropped; the business call is left to the user; any irreversible exposure is escalated, and any referral named.
- **Goes to:** the conversation; a decision or an accepted risk to the records' decisions list.

### Entity-formation pack
- **Seat:** ★ General Counsel; the Commercial Counsel drafts the agreements in it.
- **Trigger:** founding the company, converting it, or forming in a new jurisdiction.
- **What it holds:** the entity choice framed by the funding path, chosen explicitly and never by inertia (in the US, a Delaware C-corporation is the usual default where venture equity is realistic, and an LLC suits an owner-income business); the formation documents (the charter, the bylaws or operating agreement, the initial consents); the founder stock issuance and the founders' agreement; the confidentiality and invention-assignment agreements; the next steps (the tax ID, the bank account, the registered agent).
- **Completion evidence:** the entity choice ties to the funding path the user stated; every document names the right entity, parties and jurisdiction, with no placeholder left; the 83(b) 30-day clock and the QSBS issuance date are flagged to the finance skill; every filing and signature is marked as the user's act; the corporate-lawyer referral is named.
- **Goes to:** the entity and IP record. **Needs:** the board skill for the funding-path call in a founding run; the finance skill for the cap table and the tax clocks.

### IP assignment and trademark clearance
- **Seat:** ★ General Counsel; the Commercial Counsel drafts the assignment agreements.
- **Trigger:** founding, a new employee or contractor, a launch, a rebrand.
- **Completion evidence:** every founder's, employee's and contractor's work for the company is assigned to it, or the gap is named with its fix; a proposed mark is searched in the official register of each market, with the date, and its classes named; a filing is marked as the user's act; a patent question is referred to a registered patent attorney or agent.
- **Goes to:** the entity and IP record.

### Contract draft, review or redline
- **Seat:** Commercial Counsel (`templates/contract-review.md`).
- **Trigger:** a deal, a vendor, a customer, a partner, a lease, an NDA, the legal terms of a hire's agreement.
- **Completion evidence:** every risk-bearing clause (indemnity, limitation of liability, IP, warranties, data, termination, governing law, renewal) is read and marked; each redline carries its fallback and walk-away and is ranked; the parties and entity match the records; no placeholder or bracketed term survives; a non-standard term is flagged, not buried; the obligations it creates (dates, renewals, notice periods) are listed for the contract records; signing and sending are marked as the user's.
- **Goes to:** the contracts. **Needs:** the people skill for an employment agreement's business terms; the Privacy & Data Protection Counsel when the agreement moves personal data.

### Compliance program, policy set and filings calendar
- **Seat:** Compliance Officer; the Privacy & Data Protection Counsel on the privacy policies.
- **Trigger:** a regulated surface, a new market, an annual cycle, a control test.
- **Completion evidence:** each obligation names its rule (source and as-of date), its control, its owner and its next date; each policy names the rule it satisfies; each finding is triaged by severity and reportability; each filing carries its deadline and is marked as the user's act.
- **Goes to:** the obligations and filings calendar.

### Privacy assessment, DPA and privacy notice
- **Seat:** Privacy & Data Protection Counsel (`templates/privacy-assessment.md`); the Commercial Counsel on the DPA's contract terms.
- **Trigger:** a new product feature, a new processor or vendor, a new market, a customer's DPA, a data subject's request.
- **Completion evidence:** the personal data and its data subjects are named; every purpose has a named lawful basis; every transfer has its mechanism; the company's role (controller or processor) is stated; the notice discloses what the law requires, checked at the official source and dated; the breach-notification clock is stated; technical controls are routed to the systems skill.
- **Goes to:** the privacy record.

### Breach-notification assessment
- **Seat:** Privacy & Data Protection Counsel, then the Compliance Officer for the regulator's filing.
- **Trigger:** a security incident that may touch personal data (the systems skill's incident).
- **Completion evidence:** whether notice is owed, to which regulators and which people, and by when, each clock computed from the moment of awareness under its cited rule; the notices drafted and marked unsent; the privacy-lawyer referral named.
- **Goes to:** the matters and the privacy record. **Needs:** the systems skill for the incident timeline; the communications skill for anything said in public.

### Dispute triage
- **Seat:** ★ General Counsel, with the seat whose domain the dispute touches (`templates/dispute-triage.md`).
- **Trigger:** a demand letter, a cease and desist, a lawsuit or arbitration served, a regulator's inquiry, a customer threatening to sue.
- **Completion evidence:** the response deadline is computed from the papers and the rule, dated, and calendared; what to preserve is named; nothing is sent; the do-not list is present; the exposure and the options are stated; a licensed litigator is named whenever a deadline runs or papers are served; anything public is routed to the communications skill.
- **Goes to:** the matters.

## The producing chain

Entity formation, then IP assignment (so the company owns what was built), then the contracts that buy and sell, then the compliance program and the privacy duties the company's products and markets create, then disputes as they come. A contract that licenses IP the company does not yet own is built on a missing input: assign first. Before producing a downstream deliverable, confirm its upstream input exists and is current; if not, produce or flag it first.

## Hand-offs to other departments

| To | What |
|----|------|
| the finance skill | the cap table, founder stock and option grants as numbers, the 83(b) and QSBS clocks, the tax effect of a structure or a settlement |
| the people skill | the business terms of an employment agreement, the hiring process, the people records behind an employment matter |
| the systems skill | the technical controls a privacy assessment requires, and the incident timeline behind a breach |
| the communications skill | anything said in public about a dispute, a breach or a policy change |
| the board skill | a call across departments: whether to enter a market, take a round, or settle |
