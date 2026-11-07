# Specialist dispatch - the produce loop for OPERATE

*How board reaches a department and gets real work out of it: the chair routes each department's part, the department's lead frames a brief and dispatches its specialists (not just itself), the work goes to the independent verifier, and then to board, which alone writes it into the venture. It also covers the other way in: handing a whole deliverable to a department skill. Read before any operate run.*

OPERATE is the mode that produces real work product into a venture's record, and in board it is the work that crosses departments. DECIDE convenes department leads as advisors and resolves to a recommendation (`deliberation.md`, `dispatch.md`); OPERATE reaches one tier deeper, to the specialists who actually build each artifact, and lands it. This file is the producing half of what `dispatch.md` is the deciding half of. The chain is fixed: the chair frames and routes, the **lead frames the brief and dispatches its specialists**, the specialists produce, the **quality skill's ★ Head of Quality verifies**, and **board writes** behind the write-gate. No agent in that chain holds Write or Edit. The standard is unchanged: every angle heard, one owner accountable.

## Two ways to convene a department

Each department is its own skill, with its team in that skill's `agents/` and its deliverables in that skill's `references/deliverables.md` (`workforce.md`; `routing.md` names the owner of each deliverable family). Board reaches a department in one of two ways, chosen per part:

- **Dispatch the lead.** Board reads the lead's spec from the department skill's `agents/` (for legal, the legal skill's `agents/★ General Counsel.md`) and dispatches it with a self-contained brief; the lead frames its specialists' briefs, reads their specs from the same folder, dispatches them, and returns the assembled work. Use it when the part is one deliverable that must be fitted closely to other departments' parts in the same run, so the chair keeps the seams in view.
- **Hand the skill a whole deliverable.** Board gives the department skill a self-contained brief, the deliverable contract (`templates/deliverable-contract.md`), and the skill runs its own loop under its own doctrine (its tiers, its `references/deliverables.md`, its own team's reviewer where it has one) and returns the verified result. Use it when the part is a substantial, self-contained department deliverable that the department's own method should govern. Handed inside a board run, the skill persists nothing: the run is board's, so the result comes back to board, where the quality skill's ★ Head of Quality verifies it before board writes it.

Either way the department composes and returns, the chair holds the seams between departments, and board persists. A department's work asked for on its own, outside any board run, is that skill's run, not this loop (`routing.md`).

## Why the dispatch reaches below the lead tier

Leads orchestrate and never labor (the company-wide rules, `workforce.md`: "leads orchestrate, they do not labor"). A lead carries `Task` and can dispatch; a specialist carries only the read tools and does the hands-on work. DECIDE only ever convenes leads, because a decision needs judgment, not a built artifact. That is exactly why DECIDE cannot produce: a lead returns advice, not a contract. The producers are the specialists beneath each lead (the Commercial Counsel, the Privacy & Data Protection Counsel, the Product Marketing Manager, the Process Analyst). An operate run that stops at the lead tier returns a plan or an opinion and nothing lands. To produce a real deliverable the run must reach the specialist who builds it, and the lead must dispatch that specialist rather than do the work itself. A lead doing the labor is the same failure as a chair grading their own view: the orchestrator collapses into the worker, and the seam where the work gets checked disappears.

Two consequences follow, and both hold on every operate run:

- **The lead frames and dispatches; it does not type the artifact.** The lead's product is a precise brief and, at the end, an approval. The specialist's product is the artifact.
- **No producer verifies its own work.** The specialist who built it does not grade it; the quality skill's ★ Head of Quality does. A producer checking its own output is the generate-and-self-check pattern the AI-operating-system research flags as worse than no check (see `verification.md`).

## The roles in a produce loop

| Role | Seat | Holds | Produces | Tools it does NOT hold |
|---|---|---|---|---|
| **Chair** | the board skill's ★ Chief Executive Officer | The Founder's real question, the venture context, the seams between departments, the synthesis | the framed deliverable request per department and the owner | (orchestrates only) |
| **Lead** | the owning department's lead, from its skill's `agents/` (e.g. the legal skill's ★ General Counsel) | the department's standard and the output contract | the dispatch briefs, then the approval | Write, Edit |
| **Specialist(s)** | the producer(s) on the lead's team (e.g. the Commercial Counsel) | the craft | the actual artifact, with completion evidence | Write, Edit, Task |
| **Verifier** | the quality skill's ★ Head of Quality | the independent check | a pass or a fail against the completion evidence | Write, Edit |
| **Writer** | board | the only Write/Edit in a board run | the persisted file, the `Log.md` entry | (is not an agent) |

Within a board run, board is the sole writer. Agents and the department skills it convenes compose and return; board persists, behind the write-gate (`write-gate.md`). Every reference that once said an agent "files" or "records" a deliverable is wrong: the agent returns content, board writes it. A department skill called on its own persists its own department's records behind the same gate; inside a board run it does not.

## The produce loop, end to end

This is steps 2 and 3 of the universal run shape (SKILL.md) expanded for OPERATE. Route, preflight, and stage detection (step 0) and the chair's frame (step 1) have already happened; the chair has read the venture's `Overview.md`, `Goals.md`, `Strategy.md`, and recent `Log.md`, and detected the stage (`lifecycle.md`).

1. **The chair splits and routes.** From the framed request, the chair names each department's part: the exact deliverable, the owning skill and its lead (`routing.md`), the acceptance criteria, and the target file. One deliverable and one owning lead per loop; a request that needs three artifacts is three loops, sequenced on their dependencies across departments (`deliverable-dependency-chains.md`). For each part the chair chooses whether to dispatch the lead or hand the skill the whole deliverable (above).

2. **The lead frames the brief.** The lead translates the request into a self-contained dispatch brief for its specialists. The brief carries: the artifact and its purpose; the inputs (the venture files, the numbers, the upstream deliverables it depends on, including other departments'); the template or output contract to fill (the department skill's `references/deliverables.md`); the acceptance criteria the verifier will check against; the stage-scaled rigor (a seed-stage NDA is a standard mutual form, not a negotiated enterprise paper); and the **completion evidence** the specialist must return with the work (every clause traced to the playbook or the regulation, every number to a source, every assumption named). The brief is self-contained: the specialist sees none of this conversation.

3. **The lead dispatches its specialists.** The lead spawns the producer(s). One specialist for a single-craft artifact; several in parallel for a composite one (a customer agreement pulls the commercial terms from the Commercial Counsel and the data-processing terms from the Privacy & Data Protection Counsel). Parallel specialists run blind to each other on independent slices, exactly as parallel leads do in DECIDE; the lead, not the specialists, integrates the slices. The lead does not write any part of the artifact itself.

4. **The specialists produce and return.** Each specialist builds its slice to the contract and returns it with completion evidence. It persists nothing; it returns the content and the evidence to its lead.

5. **The lead assembles and approves (first-line check, not the verification).** The lead integrates the slices into the candidate deliverable and checks it against the department's standard. This is the producer's own quality bar, not the independent check, and the lead's approval is necessary but not sufficient. The lead names itself as the artifact's accountable owner.

6. **The quality skill's ★ Head of Quality verifies (independent, before anything lands).** The candidate goes to the Head of Quality, who did not build it. The Head of Quality checks it against the acceptance criteria and the completion evidence: are the numbers grounded, the assumptions named, the contract met, the claims supported, the venture's other records consistent with it. The Head of Quality returns a pass, or a fail with the specific defects. A fail returns to the lead, which re-dispatches the specialist to fix the named defects; it does not return to the Head of Quality's desk as someone else's problem. Consequential output does not land unverified (`verification.md`).

7. **The chair assembles and states a view last.** The chair, who alone holds the Founder's real question, the venture context, and every department's part, confirms the verified artifact answers the request and fits the other parts, attaches the one accountable owner (the lead), and notes any reservation last so it does not anchor the work.

8. **Board writes back, behind the write-gate.** Board, the only writer in its runs, persists the verified artifact into the owning department's file in the venture's record (in a repository, with an existing file's last state committed first; in the conversation, by returning it there), appends a dated entry to that venture's `Log.md`, and updates `Goals.md` or the `Overview.md` stage if they changed. The Chief of Staff carries the result to every department it binds and tracks the commitments it creates. Internal drafts land autonomously; anything irreversible or external (money, a contract, external comms, a delete, an equity or cap-table change) is hard-gated and escalates to the Founder before the write (`write-gate.md`, `assets/delegation-of-authority.json`).

## Selecting the specialists

Convene the smallest sufficient set of producers, the same discipline as the deciding tier. The lead picks specialists by craft against the artifact, not by seniority or by who is named first:

- **Match the producer to the craft.** Contract drafting and redlines are the Commercial Counsel's; data-protection terms are the Privacy & Data Protection Counsel's; a regulatory filing calendar is the Compliance Officer's; positioning is the sales skill's Product Marketing Manager, not its Demand Generation Manager. Each department skill's `references/deliverables.md` names the producing seat for each of its artifacts.
- **One specialist unless the artifact is genuinely composite.** Add a second producer only when the artifact has two distinct crafts in it, and run them in parallel and blind, with the lead integrating.
- **Validate the named agent at dispatch.** Each seat is checked against its department skill's `agents/` (a spec titled for the seat, listed on its team's roster) before the dispatch, so a renamed, retired, or unspawned agent fails loudly, not silently; an unspawned seat is covered by its lead (`workforce.md`, Scaling).
- **Stage scales the producer set.** Found-stage artifacts are lighter and use fewer producers; scale and maintain artifacts are heavier and may pull a seat in that a seed-stage version never needs, such as the Compliance Officer on a regulated market's filing calendar (`lifecycle.md`).

## Worked example: the EU launch's customer agreement

The Founder, on a Series A venture, asks: "Run the EU launch." It crosses departments, so it is board's operate run. The chair has run the preflight (read `Overview.md`, `Goals.md`, `Strategy.md`, recent `Log.md`) and detected the stage (scale). It splits the launch into each department's part and sequences them: the EU customer agreement (legal) comes first, because the sales motion cannot sell on terms legal has not cleared; then the EU positioning and GTM plan (sales), the onboarding playbook update (customers), and the press kit (communications). This loop follows legal's part.

1. **The chair scopes and routes.** Deliverable: the EU-ready customer agreement, the master services agreement revised for EU customers plus a data processing agreement meeting GDPR Article 28, with an obligation summary. Owning skill: legal; lead: the legal skill's ★ General Counsel. Target file: the venture's `Legal & Compliance (L&C)/Compliance.md` (the legal skill's `references/deliverables.md` names it). Acceptance criteria: every clause the legal skill's playbook requires is present; the processing terms cover Article 28; the party names and entity match the venture record; no placeholder or bracketed term survives; every non-standard term is flagged, not buried. Because these terms must fit the sales skill's pricing and the customers skill's onboarding in the same run, the chair dispatches the lead rather than handing legal the whole deliverable, reading the spec from the legal skill's `agents/★ General Counsel.md`.

2. **The General Counsel frames the briefs.** It splits the work by craft: the commercial terms (scope, liability cap, payment, termination) are the Commercial Counsel's; the data processing agreement, the transfer mechanism, and the sub-processor schedule are the Privacy & Data Protection Counsel's. It writes one brief per producer, each carrying the inputs (the current MSA, the venture's entity record, the systems skill's `Stack.md` for where customer data flows), the contract from the legal skill's `references/deliverables.md`, the acceptance criteria, the scale-stage rigor, and the completion-evidence requirement.

3. **The General Counsel dispatches, in parallel and blind.** It dispatches the **Commercial Counsel** to return the revised MSA with each change against the current version explained, and the **Privacy & Data Protection Counsel** to return the data processing agreement and its sub-processor schedule. The General Counsel drafts none of it itself.

4. **The specialists produce and return.** The Commercial Counsel returns the MSA with every clause traced to the playbook and every deviation flagged. The Privacy & Data Protection Counsel returns the agreement with each Article 28 term mapped to its clause and the sub-processors listed with their locations. Both return completion evidence; neither persists anything.

5. **The General Counsel assembles and approves.** It integrates the two into one candidate agreement, checks the seam between them (the MSA's liability cap against the data processing agreement's indemnity), and names itself the accountable owner. It flags that signing and sending the agreement to any customer are gated to the Founder. Its approval is the first-line check, not the verification.

6. **The quality skill's ★ Head of Quality verifies.** The candidate goes to the **Head of Quality**, who did not build it, and who checks every clause against the completion evidence and the venture's own record. It finds the sub-processor schedule omits an analytics vendor that the systems skill's `Stack.md` shows receiving customer data, and fails the agreement on that defect. The General Counsel re-dispatches the Privacy & Data Protection Counsel to correct the schedule; the fixed agreement returns to the Head of Quality, who passes it.

7. **The chair assembles.** The chair confirms the verified agreement answers the launch's need and fits the sales skill's pricing, attaches the General Counsel as the accountable owner, and notes the one reservation last (the transfer mechanism rests on the standard contractual clauses, worth revisiting if the legal basis for transfers changes).

8. **Board writes.** The agreement is an internal draft, autonomous under the write-gate. Board makes sure the last state of `Legal & Compliance (L&C)/Compliance.md` is committed, writes the verified agreement and its obligation summary there, and appends a dated entry to the venture's `Log.md` ("EU customer agreement drafted and verified; owner the legal skill's General Counsel; transfer basis flagged for review"). The Chief of Staff carries it to the sales skill's ★ Chief Revenue Officer, whose part waits on it, with the commitment that no EU deal is quoted on any other paper. Sending the agreement to an EU customer, or signing it, is hard-gated to the Founder before any send (`write-gate.md`).

**The next part, handed to a skill.** With the terms in hand, the chair hands the sales skill the EU positioning and GTM plan as a whole deliverable: a self-contained deliverable contract carrying the verified terms, the strategy, the ICP evidence from the research skill, and the acceptance criteria. The sales skill runs its own loop (its ★ Chief Revenue Officer frames, its Product Marketing Manager and Demand Generation Manager produce) and returns the plan; the quality skill's ★ Head of Quality verifies it against the contract; board writes it into the sales records. The customers and communications parts follow the same way, each on its upstream inputs.

The same loop produces every artifact, only the seats change: an SOP is the operations skill's (its ★ Head of Operations leading, the Process Analyst producing); the brand guide and positioning are the sales skill's (its ★ Chief Revenue Officer leading, the Product Marketing Manager producing, with the communications skill holding the brand-voice consistency gate); the financial model is the finance skill's (its ★ Financial Planning Lead routing the work inside its team). In every case the lead frames and dispatches, the specialist produces, the Head of Quality verifies, board writes, and one lead is the named owner.

## The rules that do not bend

- **Leads orchestrate, specialists produce.** A lead frames the brief and approves; it never types the artifact. Reaching below the lead tier is required, because the producers live there.
- **No producer verifies its own work.** The specialist builds it, the quality skill's ★ Head of Quality checks it, and consequential output does not land unverified. Self-checking is not verification.
- **Board is the sole writer in its runs.** Agents and the department skills compose and return; board persists, behind the write-gate. The irreversible-action gate is never bypassed.
- **Every angle heard, one owner accountable.** Every craft and every department the work needs is produced; the result is one deliverable per part with one accountable lead.
- **Stage-scaled and grounded.** The producer set, the rigor, and the artifact match the venture's stage, and every loop reads the venture's real context first and writes its result back, so the next run is not blind.
- **Smallest sufficient dispatch.** Convene only the departments and specialists the work requires; a bigger producing team is not a better one.

See `dispatch.md` for the deciding tier, `routing.md` for the skill that owns each deliverable, `deliverable-dependency-chains.md` for producing order, `verification.md` for the Head of Quality's discipline, and `write-gate.md` for what lands autonomously versus what escalates to the Founder.
