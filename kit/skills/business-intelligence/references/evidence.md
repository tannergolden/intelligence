# Evidence - answering a business question with the company's own data

The analysis doctrine of the business-intelligence skill. Read before answering any question with data, the company's or the user's own, and before synthesizing a finding. The standard: **one definition, honest uncertainty**; the craft rule: **compute, never recall**.

## The decision first

Every analysis starts from the decision it serves. A question with no decision behind it produces a number nobody acts on, so the lead names the decision before any query, or flags that none exists. The decision also sets how sure the answer must be: a reversible test needs less certainty than a hire or a price change.

## Definitions before numbers

Every metric in the question is computed from its governed definition (`metrics.md`). A missing or contested one is drafted and settled before any number is computed; an analysis never invents a private version of a metric the company already defines.

## Is the data fit to answer?

Before the analysis, the sources are checked:

- **Grain**: one row means what it should, with no duplicated keys.
- **Completeness and freshness**: the window is fully loaded; late or missing data is named.
- **Reconciliation**: a total ties to a known figure from the system of record.
- **Population**: who is in and who is out (test accounts, internal users) matches the definition.

An untested source may still be used, marked un-modeled and lower-confidence.

## Compute, never recall

Every number comes from a query or a script run on the data, read-only, in the run workspace (`dispatch.md`), and the query or script travels with the answer. No figure is estimated by eye or carried from memory, and every load-bearing number is reproduced by the seat that did not produce it before it ships.

## State the uncertainty

A number without its uncertainty is not an answer. Every finding states:

- **The sample**: how many units, over what window.
- **A range**: an interval for a rate or an estimate, computed rather than guessed; for a small group, say plainly that the range is wide.
- **The baseline**: what the number is compared with (the prior period, the same period last year, a control group), because a change means nothing without one.
- **What else could explain it**: seasonality, a change in the mix of customers, a tracking change, a one-off event, regression toward the usual level after an extreme period.

Look out for the traps that make a confident number wrong: a trend that reverses inside every subgroup when the groups are pooled; a cohort that only counts the survivors; testing many cuts and reporting the one that looked significant; and a small group whose swing is noise.

## Association is not cause

An analysis of what happened shows association. A claim that one thing caused another needs a design that can show it: a randomized experiment, a holdout, or a natural comparison where the groups differ only in the cause. Without one, the finding says "associated with", names the likeliest confounders, and names the test that would settle it. A log of one person's life is held to the same rule (`tracking.md`).

## Confidence

The lead grades each finding:

- **High**: governed definitions, tested data, an adequate sample, a reproduced number, and either a causal design or a claim that is only about association.
- **Moderate**: sound but limited: a short window, an un-modeled source, a modest sample, or a plausible confounder left open.
- **Low**: a thin or stale sample, an untested source, or a number that did not fully reproduce.

When the data cannot answer the question, the finding says so and names what would answer it; it never forces a number.

## Writing the finding

Findings first, in the `templates/answer.md` shape: the answer in one sentence with its range and confidence, the decision it informs, the evidence, the method (definitions, sources, window, the query or script), the caveats, and what would change the answer. Numbers are rounded to what the data supports, and every chart is drawn in the visual mode from the numbers and their ranges, so the uncertainty survives into the picture.

## Personal data

An analysis reads only the personal data its question needs, reports in aggregates large enough that no one can be singled out, and suppresses or merges a group too small to report safely. Rows about a person (a customer, a user or an employee) never go into a record or a commit, and appear in a reply only when the user asks for them and the question needs them; sharing them beyond the conversation is gated and waits for the user's explicit yes. What privacy law allows is the legal-and-compliance skill's call.
