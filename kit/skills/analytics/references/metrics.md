# Metrics - one definition for every number the company runs on

The metric doctrine for `analytics`. Read before defining, changing or choosing a metric. The standard holds here as everywhere in the skill: **one definition, honest uncertainty**.

## One definition per metric

Every metric the company uses has exactly one governed definition, kept in the venture's BI records, and every report, dashboard, goal and department record uses it by reference. A metric defined a second time, even slightly differently, is a defect: two "churn" numbers in two reports cost more trust than either is worth.

A governed definition (`templates/metric-definition.md`) states:

- **The question it answers**, in one sentence a newcomer can read.
- **The formula**, explicit enough that two people compute the same value from the same data.
- **The grain and the population**: what one unit is (an account, a person, an order) and who is counted.
- **The sources**: each input's table or system, and its owner.
- **Filters and exclusions**: test accounts, internal users, refunds, free tiers, and anything else left out, with why.
- **The window and the time zone**, and how a partial period is handled.
- **Leading or lagging**: whether it moves before the outcome, so the company can still act on it, or confirms what already happened.
- **The stage** at which it becomes load-bearing (below).
- **A benchmark band**, only where one is cited, with its source and its date; outside benchmarks come from the research skill.
- **An owner**, and the date the definition was last approved.

## Changing a definition

A change to a definition already in use changes every number that reads it, so it is versioned, never edited in place:

- The new version carries its date and what changed; the old one stays on record.
- The Founder approves the change before it replaces the old version.
- The history is either restated under the new definition or the break is marked on every chart and report that spans it, so no trend line silently mixes two definitions.

## The north star

The north star is the one output metric that best captures the value the company delivers to its customers, the number the whole company is trying to move over the long run. The ★ Chief Data Officer recommends it and the Founder chooses it. It must pass three tests:

1. **It reflects realized customer value**, not reach or activity that delivers none.
2. **The company's growth depends on it**: it leads revenue rather than restating it.
3. **A team can move it** through work it controls.

Beneath it sit the input metrics that move it, each owned by the function that can act on it. A north star that no longer moves with the business is replaced deliberately, as a definition change, never quietly.

## The one metric that matters, by stage

Where the north star is durable, the one metric that matters is the number the company concentrates on now, for its stage and its constraint, and it rotates:

- **Found** (idea to first funding): evidence that the problem is real and the product keeps users: retention, activation, willingness to pay, runway. Revenue is reported but read as a weak signal.
- **Scale** (a repeatable motion to grow): efficiency: payback on acquiring a customer, net revenue retention, the cash burned per dollar of new recurring revenue.
- **Maintain** (an established company): durability: growth and margin together, free cash flow, gross retention.

A metric the stage cannot yet support is marked not yet meaningful rather than reported, because reporting it implies a precision the business does not have. The financial metrics themselves are defined with the finance skill and the pipeline metrics with the sales skill; analytics keeps the one governed definition each record references.

## Metrics that mislead

- **Vanity metrics.** A cumulative total, raw sign-ups, page views: numbers that only go up and inform no decision. Prefer rates, cohorts and active use.
- **Targets that corrupt the measure.** A metric made a target starts to be gamed. Pair it with a guard metric that would move if it were gamed (sign-ups with activation, tickets closed with reopen rate).
- **Averages that hide the shape.** A mean over a skewed population misleads; report the median and the spread, or the distribution.
- **Ratios that hide their parts.** A rate moves when its denominator moves; report both parts beside the rate.
