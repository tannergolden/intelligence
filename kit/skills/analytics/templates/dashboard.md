# Dashboard: <name>

<!-- The specification of a dashboard or recurring report, written by the Data Analyst. Each view reads one governed
     metric and computes nothing of its own; the charts are drawn by the visualize skill from this specification. The
     live dashboard lives in the company's reporting tool; this record says what it must show. -->

- **Purpose:** <the decision or the watch it serves, and who reads it>
- **Owner:** <who keeps it current>
- **Refresh:** <how often, and the as-of date shown on it>

## Views

| View | Governed metric (version) | Leading or lagging | Target or band, with source | Baseline | Breakdown | Small groups |
| :--- | :------------------------ | :----------------- | :-------------------------- | :------- | :-------- | :----------- |
| <title> | <metric, v1> | <leading or lagging> | <target, or band and its source> | <prior period, same period last year> | <segment> | <suppressed below n> |

## Reading notes

- <what a reader must know: a definition break, a known data gap, a seasonal pattern>

## Not shown, and why

- <a metric the stage cannot yet support, a cut too small to report>
