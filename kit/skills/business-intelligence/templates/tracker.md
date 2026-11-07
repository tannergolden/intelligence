# Tracker: <what the user is tracking>

<!-- The user's own tracker (`references/tracking.md`): one definition per habit or personal metric, where the log
     lives, and how it is read and shown. The Analytics Engineer drafts the definitions and the log's shape, the
     Data Analyst writes the reading, and the Visualization Designer draws the chart. Kept in the conversation, or in a
     repository only when its instructions say it is a private one made to hold the user's personal context. Health:
     habits only, never a diagnosis, a treatment or medication advice. -->

- **Started:** <YYYY-MM-DD>
- **What it is for:** <what the user wants to watch or change>
- **The log lives:** <the app or its export, the file the user named, or this conversation>
- **Reading:** <how often the user wants one: weekly, monthly>

## Metrics

| Metric | What counts | Unit | Window | Target | Guard |
| :----- | :---------- | :--- | :----- | :----- | :---- |
| <habit> | <what makes a day done> | <done, minutes, pages> | <daily or weekly; time zone> | <the user's own, as a rate> | <what would move if it were gamed> |

## Log shape

| Date | Metric | Value | Note |
| :--- | :----- | :---- | :--- |
| <YYYY-MM-DD> | <habit> | <value; blank when unknown, never zero> | <optional> |

## The reading

| Metric | This window | Prior window | Longest gap | Trend |
| :----- | :---------- | :----------- | :---------- | :---- |
| <habit> | <rate, n of N days> | <rate> | <days> | <holding, rising, falling, or too short to tell> |

- **Computed by:** <the script or formula, attached>
- **What moved together:** <an association, its likely confounders, and the self-experiment that could test it>

## Chart

<The form and why (a calendar heatmap for a daily habit, a line with a rolling average for a measured value), drawn
in the visual mode.>

## Definition changes

| Version | Date | Metric | What changed |
| :------ | :--- | :----- | :----------- |
| <1> | <YYYY-MM-DD> | <habit> | <first definition> |
