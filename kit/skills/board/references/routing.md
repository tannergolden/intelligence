# Routing - which skill owns each deliverable

*The map board routes work by: each deliverable family, the skill that owns it, its lead, and what it needs from other departments. Administration's own deliverables, which board produces itself, are kept here in full. Each department's detailed catalog (every deliverable's producing seat, trigger, Definition of Done, and file) lives in its own skill's `references/deliverables.md`, which wins wherever this map differs.*

Read this with `lenses.md` (what each department brings on a decide run), `specialist-dispatch.md` (how board convenes a department and hands it work), and `deliverable-dependency-chains.md` (the producing order). The same lead that advises on a decide run owns the deliverable on an operate run. Every artifact resolves to one owning skill, one accountable lead, and one owning file: **every angle heard, one owner accountable**, in producing form. No agent writes; within a board run, agents and the department skills compose and return, and board persists.

## One department, or across departments

- **One department's work, asked for on its own, is that skill's run.** "Draft an NDA with our supplier" is the legal skill's; "close the books for October" is the finance skill's. Route it there and stop: the department skill does the work and persists its own department's records.
- **Board runs it when it crosses departments or is a company decision.** A launch, a raise, a reorganization, a plan that binds several departments, or a call the company has to make: board frames it, convenes each department's part per the map below (by dispatching that department's lead from its skill's `agents/`, or by handing the skill the whole deliverable), the quality skill's ★ Head of Quality verifies, and board persists the results.

Stage scales what is produced. A **found**-stage venture produces the lean, runway-protecting subset (a one-page model, a lean canvas, a founder-led GTM note); a **scale** venture produces the repeatable-motion set (the 3-statement model, the sales playbook, the org design); a **maintain** venture produces the durability set (the board package, the QBR, the anti-aging product review). Convene the smallest sufficient set of departments for the stage, never the full company by reflex (`lifecycle.md`, `dispatch.md`).

---

## Administration (board's own) - ★ Chief Executive Officer

The executive office: enterprise direction, the product decision, cross-department allocation, strategy framing, the governance record, and the follow-through. Owns the venture's strategic core and its decision history. On a decide run this office runs the deliberation; on an operate run it produces the strategy, roadmap and cadence artifacts the departments ladder up to.

- **Standing assets:** the company thesis and strategy; the product roadmap; the decision and governance log; the operating-cadence record and the commitment log.
- **Recurring outputs:**
  - **Strategy / business plan** (Chief Executive Officer, as chair): the thesis, the market and competitor surface, the chosen framework's output, the OKRs the departments ladder to. Trigger: a strategize run or a stage change. Lands in **Administration/Strategy.md**.
  - **Product roadmap and product decisions** (Chief Executive Officer): what to build, for whom, and when; the bets by horizon; the requirements a build is held to; the release go or no-go. It rests on the research skill's evidence about users and markets, weighs the discover skill's options, and is built by the develop skill, whose ★ Engineering Lead holds technical direction and feasibility. Trigger: a planning cycle, a launch, a pivot decision. Lands in **Administration/Roadmap.md**, with the call itself in **Administration/Decisions.md**.
  - **Decision record** (Corporate Secretary composes, board writes): the BLUF call, the rationale, the convened departments, the minority view by role, the owner, the success measure. Trigger: every decide run. Lands in **Administration/Decisions.md** (`memo.md`).
  - **Operating cadence and board record** (Chief Operating Officer): the weekly / monthly / quarterly rhythm, the board and QBR pre-reads, tracked follow-through. Trigger: a review run. Lands in **Administration/Cadence.md** (`operating-cadence.md`).
  - **Execution plan** (Chief Operating Officer): the decided call turned into owned, dated next steps across departments. Trigger: a deep decide run or an operate kickoff. Folded into **Administration/Cadence.md** and the venture `Log.md`.
  - **Commitment log** (Chief of Staff): every commitment a decision created, with its owning department, its date, and its done-test, carried to each department it binds. Trigger: every decision that binds a department. Folded into **Administration/Cadence.md**.
- **DoD, Strategy.md:** thesis stated in one paragraph; a named strategy framework with its output; OKRs that are specific and measurable and ladder to the thesis; the metric definitions referenced to **Metrics.md**, not redefined here.
- **DoD, Roadmap.md:** each roadmap item ties to a strategy objective in **Strategy.md** or **Goals.md**; each product decision cites the evidence it rests on, and an invalidated assumption is recorded as such, not quietly dropped; each requirement handed to the develop skill has acceptance criteria a verifier can check.
- **DoD, Decisions.md:** one decision per entry with the call, the rationale, the convened departments, the minority view, the single owner, the success measure, and the reversibility class; nothing material left to memory.
- **DoD, Cadence.md:** every action and commitment has one owner, a date, and a done-test; the cadence record shows which loop ran, what it graded, and what it reset.

---

## The departments

| Deliverable family | Skill | Lead | Default files |
|---|---|---|---|
| The company's money: the financial model and operating budget, the monthly close and reporting package, cash and runway, unit economics, the cap table, tax | `finance` | ★ Financial Planning Lead | `Financial-Model.md`, `Financials.md`, `Cap-Table.md` |
| Contracts (drafts, redlines, the obligation summary), the entity-formation pack, IP filings and assignment, the compliance program and policies, privacy and data protection | `legal` | ★ General Counsel | `Compliance.md` |
| Positioning and the brand guide, the GTM plan, demand generation and campaigns, the sales plan and playbook, the pipeline and forecast, the revenue plan | `sales` | ★ Chief Revenue Officer | `Brand.md`, `Products.md` (the GTM surface), `Services.md`, `Sales-Plan.md`, `Pipeline.md`, `Revenue.md` |
| SOPs and runbooks, the operations KPI view, vendor scorecards and sourcing, cross-department program and capacity plans | `operations` | ★ Head of Operations | `Operations.md` |
| Org design and the org chart, compensation bands, the hiring plan, the performance and onboarding system for hires | `people` | ★ Chief Human Resources Officer | `Hierarchy.md` |
| The internal stack: reference architecture and ADRs, the security program, SRE runbooks, the internal platform and CI/CD | `systems` | ★ Chief Information Officer | `Stack.md` |
| Governed metric definitions (the canonical KPI source, the North Star's record), dashboards and reporting, the data model | `analytics` | ★ Chief Data Officer | `Metrics.md` |
| Verification reports, test strategy and plans, the quality management plan, audits | `quality` | ★ Head of Quality | `Standards.md` |
| Onboarding playbooks, customer success plans, support SLAs, customer QBR decks | `customers` | ★ Chief Customer Officer | `Clients.md` |
| The communications plan, the press kit and newsroom, the crisis-communication plan, internal communications | `communications` | ★ Chief Communications Officer | `Press.md` |

Each department's files sit in its own folder of the venture's record, named by default for its team (`Legal & Compliance (L&C)/Compliance.md`, `Finance/Financial-Model.md`), unless the repository's instructions or its venture template name another. The finance skill's ★ Financial Planning Lead is the company's finance function and routes the work inside its team. The quality skill's ★ Head of Quality is also the independent verifier of every other department's consequential deliverable in a board run (`verification.md`).

## Product work (no single department)

| Part | Skill | Lead | Where it lands |
|---|---|---|---|
| Evidence about users and markets: user research, market sizing, competitor evidence, the validated and invalidated assumptions | `research` | ★ Research Lead | a cited synthesis, filed where the repository keeps reports; its findings carried into **Administration/Roadmap.md** |
| Options and ideas: problem hypotheses, feature, offer and positioning options | `discover` | ★ Creative Lead | a ranked shortlist, returned to the run that asked |
| The product decision: what to build, for whom, and when; the requirements; the release go or no-go | `board` | ★ Chief Executive Officer | **Administration/Roadmap.md**, the call in **Administration/Decisions.md** |
| Technical direction and building: the product's architecture, the MVP or prototype, the build and its own verification | `develop` | ★ Engineering Lead | the product's own repository, per its instructions |

## Cross-department dependencies

A department does not build on a missing input from another; board sequences the parts (`deliverable-dependency-chains.md`).

- **finance** needs the strategy and OKRs its model ladders to (board), the pipeline and revenue plan (sales), the hiring plan and comp bands (people), the metric definitions (analytics), and the entity facts behind the cap table, the 83(b) and QSBS (legal). Cap-table changes and moving money are Founder-gated.
- **legal** needs the deal terms (sales), the vendor terms (operations), the offer terms (people), the data flows and sub-processors (systems), and the cap-table effect of a formation or a round (finance). Signing and sending are Founder-gated.
- **sales** needs the strategy (board), the evidence about the market (research), the metric definitions (analytics), the contract terms it sells on (legal), and the brand-voice consistency gate on anything published (communications); it hands each closed customer to customers.
- **operations** needs each department's process owner, the vendor terms (legal), and the spend line (finance). Committing spend or signing a supplier is Founder-gated.
- **people** needs the strategy and the stage (board), the runway a plan is costed against (finance), and the employment and offer terms (legal). An actual offer is Founder-gated.
- **systems** needs the product's build (develop), the privacy obligations (legal), and the tooling vendors (operations). Its CISO, on the IT team, holds the security-risk line straight to the Founder (`workforce.md`).
- **analytics** needs the North Star chosen in strategize (board), each department's KPI owner, and the source systems (systems). Every other department's KPIs reference its definitions rather than redefine them.
- **quality** needs the deliverable, its brief, its Definition of Done, and its completion evidence from the producing skill.
- **customers** needs the closed deal and its terms (sales), the product (develop), and the metric definitions (analytics); its ticket themes feed the CEO's product decisions.
- **communications** needs positioning and brand (sales), a legal read of every external claim (legal), and the decision being announced (board). Any external publication is Founder-gated.
- **Product**: the research skill's evidence comes before the decision, the discover skill's options are weighed in it, the develop skill builds only what the decision defined, and the quality skill tests the release.

## The write rule (read with write-gate.md)

For each deliverable in a board run: the chair frames it, the owning department's lead frames the brief and its specialists produce (or the department skill runs its own loop on board's brief and returns the result), the quality skill's ★ Head of Quality verifies it against its Definition of Done, and **board writes** the verified artifact into the owning file, with the existing file's last state committed first (in a repository) and a one-line entry appended to the venture's `Log.md`. Internal drafts are autonomous; anything irreversible or external (moving money, signing or sending a contract, publishing external comms, deleting a file, changing equity or the cap table) is hard-gated and escalates to the Founder before the write. The owning file is the single home for the artifact: every angle heard in producing it, one lead accountable for it, one writer who lands it.
