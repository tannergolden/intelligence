# Metric: <name>

<!-- One governed definition per metric, drafted by the Analytics Engineer and settled by the ★ Chief Data Officer
     (`references/metrics.md`). Every report, dashboard and department record references this definition and never
     redefines it. A change to a definition in use is a new version, approved by the Founder before it applies. -->

- **Version:** <1, 2, ...> - approved by the Founder on <YYYY-MM-DD>
- **Owner:** <the function that acts on it>
- **North star:** <yes or no>

## The question it answers

<One sentence a newcomer can read.>

## Formula

<Explicit enough that two people compute the same value from the same data: the numerator, the denominator, any weighting.>

## Grain and population

- **Unit:** <account, person, order, ...>
- **Counted:** <who is in>
- **Excluded:** <test accounts, internal users, refunds, free tiers, ... and why>

## Sources

| Input | Table or system | Owner |
| :---- | :-------------- | :---- |
| <input> | <where it comes from> | <who keeps it> |

## Window

<The period, the time zone, and how a partial period is handled.>

## Reading it

- **Leading or lagging:** <leading, lagging, and why>
- **Load-bearing from:** <found, scale or maintain>
- **Guard metric:** <the metric that would move if this one were gamed>
- **Benchmark band:** <the band, its source and its date; "none cited" otherwise>
- **Caveats:** <what it does not capture>

## Change history

| Version | Date | What changed | History restated or break marked |
| :------ | :--- | :----------- | :------------------------------- |
| <1> | <YYYY-MM-DD> | <first definition> | <n/a> |
