# Deliverables - what the Legal & Compliance team produces, and where it goes

The department's producing map: each deliverable, the seat that produces it, what triggers it, the completion evidence the quality-assurance skill's ★ Head of Quality checks before it lands, and where it goes. Every deliverable resolves to one producing seat and one accountable lead, the General Counsel. A deliverable with no completion evidence cannot be verified and does not land.

**Where it goes.** The company's Legal & Compliance records live wherever the repository's instructions keep the company's department records, in the shape of `templates/legal-records.md` unless those instructions set another: the entity and IP record, the contracts, the obligations and filings calendar, the privacy record, and the matters. The user's own records (their documents, contracts, matters and privacy requests) go only into a repository whose instructions say it is a private one made to hold them (the Constitution's SEC-003). With no such instruction, a deliverable is returned in the conversation and filed only where the user asks. Inside a company-wide run, the administration skill persists that run's results; a lent seat's ledger is applied and kept by the skill that dispatched it.

**Every deliverable, always.** Each rule it turns on is cited with its official source and as-of date; it carries **the lawyer line** (a licensed lawyer must review before the act, which kind, what to bring and what to ask; or no referral trigger fires, and why); nothing asserts a legal conclusion as settled where a trigger fires; and every gated act (sign, send, file, publish, notify, request) is marked as the user's, never taken.

## The company's deliverables

### Legal risk read
- **Seat:** ★ General Counsel, with the seat whose domain the matter touches.
- **Trigger:** any matter or decision with a legal edge: a launch, a deal, a practice, a "can we do this".
- **Completion evidence:** each material risk names the party it falls on and its mitigation; the remote is named without inflation and the trivial dropped; the business call is left to the user; any irreversible exposure is escalated; the lawyer line is stated.
- **Goes to:** the conversation; a decision or an accepted risk to the records' decisions list.

### Entity-formation pack
- **Seat:** ★ General Counsel; the Commercial Counsel drafts the agreements in it.
- **Trigger:** founding the company, converting it, or forming in a new jurisdiction.
- **What it holds:** the entity choice framed by the funding path, chosen explicitly and never by inertia (in the US, a Delaware C-corporation is the usual default where venture equity is realistic, and an LLC suits an owner-income business); the formation documents (the charter, the bylaws or operating agreement, the initial consents); the founder stock issuance and the founders' agreement; the confidentiality and invention-assignment agreements; the next steps (the tax ID, the bank account, the registered agent).
- **Completion evidence:** the entity choice ties to the funding path the user stated; every document names the right entity, parties and jurisdiction, with no placeholder left; the 83(b) 30-day clock and the QSBS issuance date are flagged to the finance-and-accounting skill; every filing and signature is marked as the user's act; the corporate-lawyer referral is named.
- **Goes to:** the entity and IP record. **Needs:** the administration skill for the funding-path call in a founding run; the finance-and-accounting skill for the cap table and the tax clocks.

### IP assignment and trademark clearance
- **Seat:** ★ General Counsel; the Commercial Counsel drafts the assignment agreements.
- **Trigger:** founding, a new employee or contractor, a launch, a rebrand.
- **Completion evidence:** every founder's, employee's and contractor's work for the company is assigned to it, or the gap is named with its fix; a proposed mark is searched in the official register of each market, with the date, and its classes named; a filing is marked as the user's act; a patent question is referred to a registered patent attorney or agent.
- **Goes to:** the entity and IP record.

### Contract draft, review or redline
- **Seat:** Commercial Counsel (`templates/contract-review.md`).
- **Trigger:** a deal, a vendor, a customer, a partner, a lease, an NDA, the legal terms of a hire's agreement.
- **Completion evidence:** every risk-bearing clause (indemnity, limitation of liability, IP, warranties, data, termination, governing law, renewal) is read and marked; each redline carries its fallback and walk-away and is ranked; the parties and entity match the records; no placeholder or bracketed term survives; a non-standard term is flagged, not buried; the obligations it creates (dates, renewals, notice periods) are listed for the contract records; signing and sending are marked as the user's.
- **Goes to:** the contracts. **Needs:** the human-resources skill for an employment agreement's business terms; the Privacy & Data Protection Counsel when the agreement moves personal data.

### Compliance program, policy set and filings calendar
- **Seat:** Compliance Officer; the Privacy & Data Protection Counsel on the privacy policies.
- **Trigger:** a regulated surface, a new market, an annual cycle, a control test.
- **Completion evidence:** each obligation names its rule (source and as-of date), its control, its owner and its next date; each policy names the rule it satisfies; each finding is triaged by severity and reportability; each filing carries its deadline and is marked as the user's act.
- **Goes to:** the obligations and filings calendar.

### Privacy assessment, DPA and privacy notice
- **Seat:** Privacy & Data Protection Counsel (`templates/privacy-assessment.md`); the Commercial Counsel on the DPA's contract terms.
- **Trigger:** a new product feature, a new processor or vendor, a new market, a customer's DPA, a data subject's request.
- **Completion evidence:** the personal data and its data subjects are named; every purpose has a named lawful basis; every transfer has its mechanism; the company's role (controller or processor) is stated; the notice discloses what the law requires, checked at the official source and dated; the breach-notification clock is stated; technical controls are routed to the information-technology skill.
- **Goes to:** the privacy record.

### Breach-notification assessment
- **Seat:** Privacy & Data Protection Counsel, then the Compliance Officer for the regulator's filing.
- **Trigger:** a security incident that may touch personal data (the information-technology skill's incident).
- **Completion evidence:** whether notice is owed, to which regulators and which people, and by when, each clock computed from the moment of awareness under its cited rule; the notices drafted and marked unsent; the privacy-lawyer referral named.
- **Goes to:** the matters and the privacy record. **Needs:** the information-technology skill for the incident timeline; the public-relations skill for anything said in public.

### Dispute triage
- **Seat:** ★ General Counsel, with the seat whose domain the dispute touches (`templates/dispute-triage.md`).
- **Trigger:** a demand letter, a cease and desist, a lawsuit or arbitration served, a regulator's inquiry, a customer threatening to sue.
- **Completion evidence:** the response deadline is computed from the papers and the rule, dated, and calendared; what to preserve is named; nothing is sent; the do-not list is present; the exposure and the options are stated; a licensed litigator is named whenever a deadline runs or papers are served; anything public is routed to the public-relations skill.
- **Goes to:** the matters.

## The gates the team keeps for every department

### Standards review (the exposure ledger)
- **Seat:** Compliance Officer, joined by the Privacy & Data Protection Counsel when personal data is the exposure (`references/standards-review.md`, `templates/exposure-ledger.md`).
- **Trigger:** sensitive or external-facing output before it ships, from any department or the user: a post, an article or report, a press release, an ad or landing page, a launch asset, a marketing email, a public statement.
- **Completion evidence:** the whole output was screened for the five exposures (libel and defamation, privacy, IP and licensing, regulated or unqualified claims, disclosure); the audience and channel are stated, or the most exposed one assumed and flagged; each exposure names its specific rule (a law or regulator's rule with its official source and as-of date, a license's own term, or a named standard), the concrete risk for that audience and channel, and BLOCK, REVISE with the exact edit, or CLEAR; a genuine legal exposure is escalated, never adjudicated; the reviewer saw the output and its sources, never how it was drafted.
- **Goes to:** the requesting lead or the user, who applies the verdicts in one round; the ledger is kept only where the requester's records keep it.

### Blind profile review
- **Seat:** Privacy & Data Protection Counsel, dispatched blind by the human-resources skill's profile interview, on the brief that skill's `references/roster.md` sets (`references/standards-review.md` for how the seat works).
- **Trigger:** every proposal batch the profile interview composes, every run; there is no batch too small.
- **Completion evidence:** one review-ledger row per proposal, in the shape the human-resources skill's `references/roster.md` gives, each with BLOCK, REVISE or CLEAR, the rule it touches (read-only, propose first, facts not guesses, sensitive categories, records boundary, provenance grammar, SEC-003), the concrete risk, and the required change or the reason; every line judged against that skill's `references/provenance.md` and SEC-003; the reviewer received only the batch and the rules, never the interview reasoning, the plan or the brief to the public-relations skill's Writer.
- **Goes to:** the human-resources skill, which applies the verdicts mechanically, in one round, and alone keeps the approved batch.

## The user's own deliverables

### Personal contract or lease review
- **Seat:** Commercial Counsel (`templates/contract-review.md`).
- **Trigger:** a lease, a job offer's agreement or its non-compete, a freelance or consulting contract, a home-improvement contract, a purchase, a sale or a loan the user is about to sign.
- **Completion evidence:** as the company's contract review, plus: each clause that a law protecting the user (a tenant's, a consumer's, an employee's) overrides is marked with that rule, cited and dated; the obligations and notice dates it creates are listed for the user; the lawyer line is stated.
- **Goes to:** the conversation, or the user's own records in a private repository made to hold them.

### Will and the documents beside it
- **Seat:** ★ General Counsel, with the finance-and-accounting skill's Insurance & Estate Specialist on the money.
- **Trigger:** a will, a power of attorney, a health-care directive or a guardian to name; a life event (a marriage, a child, a home, a business, a death in the family).
- **Completion evidence:** the draft names the executor, the beneficiaries, any guardian and the attorney-in-fact, with no placeholder left; the signing formalities where the user lives (witnesses, a notary, any registration) are checked at the official source and dated; the money questions (beneficiary designations, insurance, the estate's tax) are routed to the finance-and-accounting skill; the medical choices in a directive are left to the user and their clinician; the estate-planning lawyer referral is named before signing, and signing is marked as the user's act; where the signed originals will be kept is a pointer, never the content.
- **Goes to:** the conversation, or the user's own records in a private repository made to hold them.

### Personal dispute triage
- **Seat:** ★ General Counsel (`templates/dispute-triage.md`), with the Commercial Counsel when a contract or lease is at issue.
- **Trigger:** a withheld deposit, a contractor's unfinished work, a seller's refusal once a complaint has failed, a demand letter or court papers served on the user, a neighbour's claim.
- **Completion evidence:** as the company's dispute triage, plus: the escalation path is stated in order (the written demand, the regulator's or ombudsman's complaint route, small claims within its limit, a lawyer above it), each with its deadline and the court's or regulator's own rules cited; the demand letter is drafted and marked unsent; the lawyer line names whether the matter needs one (always at once when papers are served or a criminal question arises).
- **Goes to:** the conversation, or the user's own records in a private repository made to hold them. **Needs:** the customer-experience skill's record of the complaint already made.

### Privacy request
- **Seat:** Privacy & Data Protection Counsel.
- **Trigger:** the user wants to see, correct or delete their data, or opt out of its sale or sharing; a data broker lists them; they received a breach notice.
- **Completion evidence:** the right is named with the law that grants it where the user lives, cited and dated; the holder's own request route is named; the deadline for an answer is computed; the request is drafted and marked unsent; the follow-up date and the regulator's complaint route are stated; securing the user's accounts after a breach is routed to the information-technology skill.
- **Goes to:** the conversation, or the user's own records in a private repository made to hold them.

## The producing chain

For a company: entity formation, then IP assignment (so the company owns what was built), then the contracts that buy and sell, then the compliance program and the privacy duties its products and markets create, then disputes as they come. A contract that licenses IP the company does not yet own is built on a missing input: assign first. For the user: the documents that protect the people who depend on them (the will, the powers of attorney) before the documents that commit them (a lease, a loan, a guarantee). Before producing a downstream deliverable, confirm its upstream input exists and is current; if not, produce or flag it first.

## Hand-offs to other departments

| To | What |
|----|------|
| the finance-and-accounting skill | the cap table, founder stock and option grants as numbers, the 83(b) and QSBS clocks, the tax effect of a structure or a settlement; the user's estate plan as money (beneficiaries, insurance, tax) |
| the human-resources skill | the business terms of an employment agreement, the hiring process, the people records behind an employment matter; the verdicts of the blind profile review |
| the information-technology skill | the technical controls a privacy assessment requires, the incident timeline behind a breach, and securing the user's accounts |
| the customer-experience skill | the user's complaint, return or warranty claim before it turns legal |
| the public-relations skill | anything said in public about a dispute, a breach or a policy change; the writing itself |
| the quality-assurance skill | whether a claim is true, and the verification of every consequential deliverable |
| the administration skill | a call across departments (whether to enter a market, take a round, or settle) and a life decision that is more than a legal one |
