# Tracking - the user's own habits and metrics

The tracking doctrine of the business-intelligence skill: the department's method at the scale of one life. Read before setting up a tracker or reading the user's own log. The standard holds here as everywhere in the skill: one definition and honest uncertainty for every number, and graphical integrity for every chart.

## What it covers

The user's habits and personal metrics: exercise and activity, sleep, steps, reading, practice, focus hours, screen time, meals cooked at home, any routine the user wants to keep and see. Money is the finance-and-accounting skill's (the budget, spending and net worth), and this skill draws any chart those numbers need; what a healthy routine should be is the human-resources skill's, and designing the routine itself is the operations-and-logistics skill's.

## Health

For the user's health, tracking covers routines, sleep, activity and nutrition habits, appointments and benefits only. The team never gives a diagnosis, a treatment or medication advice, and never reads a number as a symptom; it always refers the user to a clinician for those, and to emergency services in a crisis. A tracker is a mirror of habits, not a medical record.

## Define each metric once

The same discipline as a company metric (`metrics.md`), in the lighter shape of `templates/tracker.md`:

- **What counts.** For a habit, what makes a day done (a run of at least 20 minutes, not "exercise"); for a measured value, the unit and how it is taken (the same device, the same time of day).
- **The window.** Daily or weekly, the time zone, and how a partial week is handled.
- **The target.** The user's own, stated as a rate where it can be (5 of 7 days), never imposed.
- **The guard.** What would move if the metric were gamed: pages read beside books finished, steps beside active minutes.

The user approves each definition. A change is a new version, marked on every chart that spans it, so no trend line silently mixes two definitions.

## The log

- One row per day per habit or measurement: the date, the metric, the value, an optional note.
- A missing day is kept apart from a skipped one: no entry is unknown, not zero, and is shown as unknown.
- The log lives where the user already keeps it (an app or its export, a file they name) or in the conversation. It is written into a repository only when that repository's instructions (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files) say it is a private one made to hold the user's personal context (the Constitution's SEC-003); anywhere else it stays in the conversation.
- A credential to the app that holds the log is never recorded (the Constitution's SEC-001): the user exports the data or names where it lives.

## Reading it honestly

- **Compute, never recall.** Every number comes from the log, with a script or a formula, never from memory or an impression; the script travels with the reading so the user can run it again.
- **A rate beats a streak.** A streak resets on one miss and hides the pattern; report the rate over the window (22 of 30 days) beside the prior window, and name the longest gap when it matters.
- **A baseline.** A change means nothing without what it is compared with: the user's own prior weeks, or the same weeks last year for anything seasonal.
- **Noise first.** In a log of one person, a single week's swing is noise until the trend holds over several windows; a rolling average shows the trend under the daily scatter.
- **Association, not cause.** A log of one life shows what moved together, not what caused what: "I sleep better on days I run" is an association, with the weekday, the weather and the workload as likely confounders. A self-experiment that could show cause (one change at a time, alternating weeks) is named, never assumed.

## Showing it

Through the visual mode, to the same standard as any other visual (`principles.md`, `visual-dispatch.md`):

- **A daily habit:** a calendar heatmap or a dot strip, with done and not done told apart by more than color (a filled mark against an open one) and unknown days left blank and labeled.
- **A measured value over time:** a line with a rolling average; the axis need not start at zero, because lines are compared with each other, but it is clearly labeled.
- **Several habits:** small multiples on a common scale, not one crowded chart.
- **A personal dashboard:** fits one screen, with each habit's rate against its target and its trend, the as-of date shown.

## Where it ends

The tracker reports; the user decides. Changing a routine is the user's call, and nothing about the user leaves the conversation without their yes.
