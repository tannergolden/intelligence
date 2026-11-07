# Deliverable contract (the output contract every operate deliverable carries)

*The header every OPERATE artifact ships with before it lands: what it is, which skill and lead own it, where it is filed, the Definition of Done it was built against, the verifier's sign-off, and whether it is Founder-gated. Administration fills it from the chair's brief, the owning lead (or the department skill it is handed to) works to it, the quality-assurance skill's ★ Head of Quality signs it, and administration (the sole writer in its runs) lands it. No agent writes; agents and the department skills compose and return, and administration persists.*

This is the producing-side twin of `templates/decision-brief.md` (which frames a decide run). A decision brief frames a question; a deliverable contract frames a produced artifact and travels with it from the lead's brief, through the Head of Quality's verification, to the write-gate. It is also the self-contained brief administration hands a department skill when it gives that skill a whole deliverable (`references/specialist-dispatch.md`). One contract per artifact. A request that needs three artifacts is three contracts, sequenced on their dependencies (`references/deliverable-dependency-chains.md`). The contract is what makes the producer-to-artifact handoff checkable end to end: a deliverable with no owning file and no Definition of Done is not producible, and the verifier returns it unbuilt.

Read this with `references/specialist-dispatch.md` (the produce loop that fills it), `references/routing.md` (the skill and lead that own each deliverable family, and Administration's own deliverables in full), the owning department skill's references (its `references/deliverables.md` where it keeps one: its owning file and DoD for each artifact), `references/verification.md` (how the Head of Quality checks the DoD), and `references/write-gate.md` (the green and red lanes the gate field maps to). The owning-file names and the DoD lines come from those sources; never invent a new owning file here.

## The contract (fill one per artifact)

```
ARTIFACT:        [the specific deliverable, named, not a capability. "Q3 3-statement model", not "finance work".]
OWNING SKILL:    [the skill that owns it, and its team, e.g. legal-and-compliance (Legal & Compliance (L&C)), or administration for its own.]
LEAD (owner):    [the one accountable lead, named for its skill, e.g. the legal-and-compliance skill's ★ General Counsel. One name. The accountable owner of record.]
SPECIALIST(S):   [the producer(s) the lead dispatched, e.g. Commercial Counsel. Who built it, for the record.]
HOW CONVENED:    [lead dispatched by administration | whole deliverable handed to the skill. See specialist-dispatch.md.]
FILED TO:        [the single file of the venture's record it lands in, from the owning skill's references. e.g. Legal & Compliance (L&C)/Compliance.md.
                  A personal artifact: only where a private repository made to hold it says, else the conversation.]
TRIGGER:         [what called for it: a planning cycle, a raise, a launch, a review run, a stage change.]
STAGE:           [found | scale | maintain. Scales the rigor: a seed-stage NDA is a standard form, not a negotiated enterprise paper.]
LADDERS TO:      [the strategy objective or OKR in Strategy.md / Goals.md this serves, so nothing is built unmoored.]
DEPENDS ON:      [the upstream artifacts it builds on, including other departments' (e.g. legal's terms before sales' GTM); none if it is a root artifact.]

DEFINITION OF DONE (the bar the Head of Quality checks, from the owning skill's references):
  - [checkable condition 1]
  - [checkable condition 2]
  - [checkable condition 3]

COMPLETION EVIDENCE (returned with the artifact; the verifier checks the evidence, not the claim):
  - [every number traced to a source, a tool call, or a venture file; every assumption named.]

VERIFIER SIGN-OFF (the quality-assurance skill's ★ Head of Quality, or the seat on its team it assigns):
  - Result:     [ cleared | cleared with noted defects | returned | escalated ]
  - Checked:    [the specific evidence checked, not a general thumbs-up.]
  - Defects:    [any noted gaps or open questions that travel with the artifact; none if clean.]

FOUNDER-GATED:   [no | yes - <which red category>. A "no" means administration writes it autonomously into the venture's record
                  once verified, with the prior state committed. A "yes" means administration prepares the action and stops for the Founder's
                  explicit confirmation. The five red categories are fixed (write-gate.md): moving money, signing or
                  sending a contract, publishing or sending external comms, deleting a file, changing equity or the cap
                  table. When in doubt, gated.]

WRITE-BACK:      [the Log.md line administration appends, and any Goals.md / Overview.md stage update the artifact triggers.]
```

## How each field is set, and by whom

- **Artifact, owning skill, filed-to, DoD** come from `references/routing.md` (which skill owns the deliverable family) and the owning skill's references (its file and its DoD), or, for Administration's own deliverables, from `references/routing.md` itself. Those are the source of truth; the contract copies them, it does not redefine them. If no owning file exists for the artifact, the artifact is not yet producible, and that is a finding, not a thing to invent a home for.
- **Lead, specialist(s), and how convened** come from the owning skill's roster and the chair's choice (`references/specialist-dispatch.md`). The lead is the single accountable owner; the specialists are the producers the lead dispatched. The lead frames and approves and never types the artifact; the specialist builds it; neither one writes the file. When the whole deliverable is handed to the skill, the skill's own lead and team fill these lines and return the contract with the artifact.
- **Stage and ladders-to** come from the preflight: the chair read `Overview.md`, `Goals.md`, `Strategy.md`, and recent `Log.md`, and detected the stage (`references/lifecycle.md`). The stage scales the rigor and the deliverable set; ladders-to keeps the artifact tied to a real objective so the work is not unmoored.
- **Completion evidence** is the producer's, returned with the artifact. The rule is `references/verification.md`'s: every number, every named fact, every external claim traces to a tool call, a venture file, or a cited source. Nothing load-bearing rests on recall.
- **Verifier sign-off** is the quality-assurance skill's alone: its ★ Head of Quality's, or the seat on its team it assigns (the Fact-Checker for claims and figures, the QA Test Engineer for a release, the Design Critic for a visual). A producer never verifies its own work. The Head of Quality receives the artifact, this contract, and the claimed sources in a fresh worker that holds none of the producer's reasoning, and checks the artifact against the DoD and the evidence. The four results are `cleared`, `cleared with noted defects`, `returned`, `escalated` (`references/verification.md`). A `returned` artifact does not land; it goes back to the lead with the specific finding. Consequential output does not land unverified.
- **Founder-gated** maps to the write-gate's two lanes (`references/write-gate.md`). Green (autonomous): internal, reversible drafts and models into the venture's own record, or into the Founder's own records where a private repository made to hold them allows, written once verified, with the prior state committed. Red (hard-gated): the five fixed categories, which never go autonomous at any stage or tier; a CEO-seat yes is advice, not authorization. Stage moves the dollar line inside the green lane, never the category line.
- **Write-back** is what administration does after the gate clears: persist the artifact into the filed-to file (with an existing file's last state committed first), append a dated line to the venture `Log.md`, and update `Goals.md` or the `Overview.md` stage when they changed. Then run the checks the repository's instructions name.

## The gate the contract walks before it is written

Administration walks the write-gate checklist (`references/write-gate.md`) against this contract, in order, and stops at the first red:

1. **Is the FOUNDER-GATED field a red category?** (money, contract, external comms, delete, equity or cap table.) Yes - frame the action, state it, get the Founder's explicit confirmation. Do not proceed on a CEO-seat yes.
2. **Does it cross outside this venture's record (or the Founder's own records), touch the Founder's calendar or accounts, or is it irreversible?** Yes - same as above.
3. **Is it the Founder's personal context, headed for a repository not made to hold it?** Stop - it stays in the conversation.
4. **Does the implied spend or hire exceed the stage threshold** (`assets/delegation-of-authority.json`)? The artifact is green to draft; the action is red to execute. Gate the action.
5. **Green so far - is the existing file's last state committed?** No - commit it first. A new file needs nothing.
6. **Is the output consequential, and has the Head of Quality cleared it?** Consequential and unverified does not pass, even when reversible. Verify first.
7. **All clear - write it.** Persist, append to `Log.md`, update `Goals.md` / `Overview.md` if changed, then run the checks the repository's instructions name.

---

## Worked stubs (the highest-value contracts, pre-filled)

Four worked stubs: the product requirements that carry the CEO's product decision into the research-and-development skill's roadmap, and three more common department deliverables administration convenes inside a company-wide run. Copy the relevant stub into a fresh contract, fill the brackets from the venture, and let the body of the artifact follow the stub's structure. The department stubs are the hand-off form only: the owning skill's references are canonical for its file and its DoD, and win wherever a stub differs.

### Stub A - Product requirements (the research-and-development skill, on the CEO's product decision)

```
ARTIFACT:        [feature or product name] requirements
OWNING SKILL:    research-and-development (Research & Development (R&D)): the roadmap and its requirements are its;
                  the product decision they carry out is the CEO's
LEAD (owner):    the research-and-development skill's ★ Head of Research & Development
SPECIALIST(S):   its All-Source Analyst and UX and Design Research Lead (the evidence the requirements rest on), its
                  Idea Generator (the options weighed, when the choice set was thin), and its Full-Stack Engineer
                  (feasibility, and the design and build plan the requirements turn into)
HOW CONVENED:    [whole deliverable handed to the research-and-development skill, on the CEO's recorded product
                  decision | lead dispatched by administration]
FILED TO:        the research-and-development records' Roadmap.md (Research & Development (R&D)/Roadmap.md where the
                  venture keeps department folders; the CEO's call itself in Administration/Decisions.md; the GTM
                  surface for the same product lands in the sales records' Products.md)
TRIGGER:         a build is greenlit by the CEO's product decision
STAGE:           [scale, typically]
LADDERS TO:      [the strategy objective in Strategy.md / the OKR in Goals.md this build serves]
DEPENDS ON:      the CEO's product decision in Administration/Decisions.md; the research-and-development skill's evidence
                  (the user-research synthesis and the market requirements)
DEFINITION OF DONE:
  - the requirement ties to a strategy objective in Strategy.md or Goals.md
  - each requirement has acceptance criteria a verifier can check (testable, not aspirational)
  - the validated and invalidated assumptions are recorded; an invalidated assumption is kept, not quietly dropped
  - the build contract is unambiguous: scope in, scope out, and the go / no-go gates named, each gate the CEO's call
FOUNDER-GATED:   no  (an internal spec; the build it authorizes may carry gated spend, checked separately)
```

Body sections: problem and the evidence for it; the user and the job-to-be-done; goals and non-goals; requirements with acceptance criteria; the assumptions (validated and invalidated); dependencies and the release gates; the metric that will tell us it worked (defined in Metrics.md, not redefined here).

### Stub B - SOP / runbook (the operations-and-logistics skill)

```
ARTIFACT:        [process name] SOP
OWNING SKILL:    operations (Operations & Logistics (O&L))
LEAD (owner):    the operations-and-logistics skill's ★ Head of Operations
SPECIALIST(S):   Process Analyst (maps and improves the process)
HOW CONVENED:    [lead dispatched by administration | whole deliverable handed to the operations-and-logistics skill]
FILED TO:        Operations & Logistics (O&L)/Operations.md
TRIGGER:         a process that lives in one head, an audit, or a handoff between departments that keeps breaking
STAGE:           [scale or maintain]
LADDERS TO:      [the operating objective or the reliability / cycle-time target this procedure serves]
DEPENDS ON:      none (or the upstream process it hands off from, in whichever department owns it)
DEFINITION OF DONE:
  - every step is executable as written (a stranger to the process can run it)
  - The RACI names real owners, not placeholders
  - the exception and rollback paths exist and are reachable from the happy path
  - each KPI the SOP is measured by has a definition, a target band, and a current value (referencing Metrics.md)
FOUNDER-GATED:   no  (committing vendor spend or signing a supplier contract surfaced by the SOP is red, gated separately)
```

Body sections: purpose and scope; the trigger and the inputs; the RACI; the step-by-step procedure (a flowchart where it helps); the exception paths and the rollback; the KPIs and their target bands; the review cadence and the owner.

### Stub C - GTM one-pager (the sales-and-marketing skill)

```
ARTIFACT:        [product or launch name] GTM one-pager
OWNING SKILL:    sales-and-marketing (Sales & Marketing (S&M))
LEAD (owner):    the sales-and-marketing skill's ★ Chief Revenue Officer
SPECIALIST(S):   Marketing Manager (positioning, the launch, the channel and pipeline plan)
HOW CONVENED:    [lead dispatched by administration | whole deliverable handed to the sales-and-marketing skill]
FILED TO:        the sales records' Products.md   (the offer detail lands in Services.md; positioning lives in Brand.md)
TRIGGER:         a launch or a new market
STAGE:           [found for a founder-led GTM note; scale for the repeatable motion]
LADDERS TO:      [the growth OKR in Goals.md this launch serves]
DEPENDS ON:      the positioning and brand guide in Brand.md (positioning precedes GTM); the contract terms the launch sells on
                  (the legal-and-compliance skill)
DEFINITION OF DONE:
  - The ICP is specific (not "everyone"); the segment is named and bounded
  - the why-now is evidenced, not asserted
  - launch tiers have owners and dates
  - the pipeline target and the channel mix are stated and traceable to a number
  - any published external asset is flagged Founder-gated, never sent autonomously
FOUNDER-GATED:   the plan: no.  any external publication or send it produces: yes - publishing or sending external comms.
```

Body sections (one page): ICP and the job-to-be-done; the why-now; how-we-win (the wedge against alternatives); the offer and pricing surface; launch tiers with owners and dates; the channel mix and the pipeline target; the metric that defines a successful launch (from Metrics.md).

### Stub D - Compensation bands (the human-resources skill)

```
ARTIFACT:        Compensation bands - [scope: a level, a department, or company-wide]
OWNING SKILL:    people (Human Resources (HR))
LEAD (owner):    the human-resources skill's ★ Chief Human Resources Officer
SPECIALIST(S):   the HRIS and People Operations Analyst, or a compensation seat spawned on demand (the benchmarked ranges and
                  the rewards mix)
HOW CONVENED:    [lead dispatched by administration | whole deliverable handed to the human-resources skill]
FILED TO:        Human Resources (HR)/Hierarchy.md
TRIGGER:         a hiring wave or an annual compensation review
STAGE:           [scale, typically]
LADDERS TO:      [the org-design objective in Strategy.md; costed against the runway in the finance records' Financial-Model.md]
DEPENDS ON:      the org design and the role charters in Hierarchy.md; the runway in the finance-and-accounting skill's
                  Financial-Model.md
DEFINITION OF DONE:
  - each band is benchmarked to a named source and stated as a range, not a point
  - the equity guidelines and the approval workflow are stated
  - the plan is costed against Financial-Model.md runway, not set in a vacuum
  - no real person's actual compensation or termination is decided here (those escalate to the Founder)
FOUNDER-GATED:   the bands: no.  an actual offer drawn from them: yes - it commits money and is a contract.
```

Body sections: the leveling framework (the ladder the bands sit on); the benchmark source and its vintage; the bands by level and department (range, not point); the equity and total-rewards guidelines; the approval workflow; the runway cost of filling the open plan at band midpoint.

---

## The standard the contract holds

One contract, one artifact, one owning file, one accountable lead, one verifier's sign-off, one writer. **Every angle heard in producing it, one owner accountable for it.** The lead frames and approves; the specialists produce in isolation and never grade their own work; the quality-assurance skill's ★ Head of Quality verifies independently against the DoD; administration alone writes, behind the write-gate. The contract is stage-aware (the rigor and the deliverable set scale to found, scale, or maintain), grounded (every number traces, the artifact ladders to a real objective), and gated (the five red categories are the Founder's alone to authorize). A deliverable that cannot fill this contract is not done, and administration does not write a deliverable the verifier returned.

See `references/specialist-dispatch.md` for the produce loop that fills the contract, `references/verification.md` for the sign-off discipline, `references/write-gate.md` for the gate the FOUNDER-GATED field maps to, and `references/routing.md` for the skill that owns every other deliverable (and that skill's references for its owning file and DoD).
