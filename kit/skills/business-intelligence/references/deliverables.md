# Deliverables - what the BI department produces, and where it lands

The producing map for every run of the business-intelligence skill: each deliverable, the seat that produces it, what triggers it, the completion evidence it must carry before it lands, and where it goes. Read it with `dispatch.md` and `visual-dispatch.md`, which set who runs in what order, and `metrics.md`, `evidence.md`, `tracking.md` and `principles.md`, which set the doctrine each deliverable is checked against. The standard is the team's: **integrity**, one definition and honest uncertainty for every number, graphical integrity for every visual.

## Where the work lands

A venture's department records go where the repository's own instructions keep them: the venture's **Business Intelligence (BI) records**, in whatever folder and files those instructions name (a repository with a venture template maps each deliverable below onto its own files). The governed metric definitions are the company's one canonical source for every metric: other departments' records and the venture's goals reference them and never redefine them. With no such instruction, the deliverable is returned in the conversation and a file is written only where the user asks, at the path they name. Called on its own, this skill persists its own department's records; in an administration run, the administration skill persists that run's results. No record holds rows about a person (a customer, a user or an employee), and the user's own tracker goes into a repository only when its instructions say it is a private one made to hold the user's personal context.

## Standing assets

The durable records the department maintains and a run updates rather than re-creates:

- **The metric definitions**: one governed definition per metric, the north star among them (`templates/metric-definition.md`).
- **The data model and its sources**: the curated tables, their grain, their tests, and where each source comes from.
- **The dashboards and reports**: what each one watches, against which definitions and bands, refreshed how often, owned by whom (`templates/dashboard.md`).
- **The visuals the repository keeps**, where its instructions say visuals go.
- **The user's own tracker**, where the user keeps it (`templates/tracker.md`).

## Recurring outputs

**Visuals** (the ★ Chief Data Officer frames and picks the form; the Visualization Designer makes; the quality-assurance skill's Design Critic gates above the quick tier; the lead renders).
- Trigger: a request for any chart, graph, diagram, flowchart, timeline, dashboard or interactive visual, or a response whose data or structure lands better seen than read.
- Completion evidence: the question it answers and the chosen form named; integrity held (a zero baseline on bars, lie factor near 1, no forbidden encoding; for a diagram, every real relationship present and no false one); each number's range shown where it carries one; a palette from the library matched to the data; the accessibility floor met and a text alternative present; above the quick tier, the Design Critic's PASS.
- Lands in: rendered in chat; saved as an `.svg` or self-contained `.html` file only on the user's yes, where the repository's instructions say visuals go or at the home the user names, following that folder's rules.

**Governed metric definitions** (the Analytics Engineer drafts; the ★ Chief Data Officer settles; the Founder approves a change to one already in use).
- Trigger: any new metric, a metric two reports compute differently, or a definition that has drifted from what the business means.
- Completion evidence: exactly one definition per metric; the formula explicit; the grain stated; each input naming its source table or system; filters and exclusions listed; an owner; the leading or lagging tag; the stage at which it becomes load-bearing; a benchmark band, where one is cited, with its source and date; no second definition of the same metric anywhere in the records.
- Lands in: the venture's BI records, as the canonical definition every other record references.

**The north star and the metric set** (the ★ Chief Data Officer recommends; the Founder chooses).
- Trigger: a strategy cycle, a stage change, or a north star that no longer moves with the business.
- Completion evidence: the north star passes its three tests (`metrics.md`); the input metrics that move it are named; the one metric that matters for this stage is named; metrics the stage cannot yet support are marked as not yet meaningful rather than reported.
- Lands in: the venture's BI records; the venture's goals point at it.

**Data model and sources** (the Analytics Engineer).
- Trigger: a new source, a metric that needs a model, or a number that broke.
- Completion evidence: the grain declared; sources staged, then transformed; the tests passing (uniqueness on the key, not-null on required fields, accepted ranges, referential integrity, freshness) and a reconciliation to a known total shown; columns documented; each source's owner named; personal data limited to the columns the model needs.
- Lands in: the venture's BI records, as the documentation of the model; the model itself lives where the company's data platform keeps it.

**Dashboards and reports** (the Data Analyst specifies; the Visualization Designer draws the charts in the visual mode).
- Trigger: a review run, or a number the company wants to watch on a cadence.
- Completion evidence: each view maps to one governed metric and computes nothing of its own; each number shown against its target or benchmark band and its baseline; leading and lagging labeled; the as-of date and refresh cadence stated; an owner named; small groups suppressed or flagged.
- Lands in: the venture's BI records, as the specification; the live dashboard lives in the company's reporting tool.

**Analysis** (the Data Analyst; the ★ Chief Data Officer's synthesis).
- Trigger: a business question tied to a decision.
- Completion evidence: the question and the decision it serves stated; the governed definitions, window and population named; every number produced by an attached query or script; each load-bearing number reproduced by the seat that did not produce it; the uncertainty stated (sample, range, baseline); association kept apart from cause; what would change the answer named (`templates/answer.md`).
- Lands in: returned in the conversation; filed in the venture's BI records on request.

**The user's own tracker** (the Analytics Engineer defines; the Data Analyst reads; the Visualization Designer charts).
- Trigger: the user wants to track a habit or a personal metric, or asks how one is going.
- Completion evidence: each metric defined once (what counts, the unit, the window, the user's target) and approved by the user; the log's shape and where it lives named; the reading computed from the log, as a rate over the window beside the prior window, with gaps and noise named; association kept apart from cause; nothing that reads as a diagnosis (`tracking.md`).
- Lands in: the conversation; a repository only when its instructions say it is a private one made to hold the user's personal context.

## What comes from other departments

A deliverable is never built on a missing input; when one is missing, the lead produces or flags it first.

- **The administration skill**: the strategy and the goals the north star and the metric set serve, and the decision an analysis informs.
- **The finance-and-accounting skill**: the financial model and statements, and every financial figure (revenue as booked, cash, runway), and the user's own budget and spending. This department takes them as given and defines the operating metrics around them; it never restates the books.
- **The sales-and-marketing skill**: the pipeline and the revenue forecast (its ★ Chief Revenue Officer). This department keeps the definitions the forecast reads, such as win rate and pipeline coverage.
- **The research-and-development skill**: facts about the outside world, such as a benchmark band or a market figure, sourced and dated; and the build when a widget becomes a real application.
- **The information-technology skill**: access to the data and the platform, and its security. This department never grants itself access.
- **The legal-and-compliance skill**: what privacy law allows the company to do with personal data.
- **The quality-assurance skill**: its Design Critic's visual integrity review above the quick tier, and its ★ Head of Quality's independent verification of a deliverable on a deep run.

The producing order: metric definitions, then the data model and its sources, then the dashboards and the scorecard. A dashboard built before its definitions are agreed reports numbers no one trusts.
