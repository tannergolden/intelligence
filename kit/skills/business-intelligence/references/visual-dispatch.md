# Visual dispatch - how the visual tiers map onto the BI team

How the business-intelligence skill spends its team on a visual, scaled to the visual. Read before choosing a tier for one. The seats a visual uses: the ★ Chief Data Officer (the lead, whom the skill embodies), the Visualization Designer, and the quality-assurance skill's Design Critic, borrowed for the visual integrity review; the Data Analyst joins when the data needs real cleaning. Every dispatch is a self-contained brief; the subagent sees none of the conversation, returns its artifact, and persists nothing. The lead alone renders and owns delivery.

## Tier decision table

| Signal | Tier |
|--------|------|
| One static chart or diagram, data already clean, stays in chat | quick |
| The visual ships, is load-bearing, will be saved, or will be seen by others | standard |
| Interactive, a dashboard, multiple linked panels, or exploration of many values | interactive |

When two rows fit, take the higher. Announce the tier before dispatching; it is a cost decision.

## What runs at each tier

- **quick.** The lead picks the form and briefs the Visualization Designer, who renders and self-checks against the integrity and accessibility checklist in `principles.md`. No separate Critic pass. Reserve for a one-off visual from clean data that stays in chat.
- **standard.** The lead frames and picks the form -> Visualization Designer makes -> the Design Critic gates (form-fit, integrity, the blocking accessibility gate, clarity) -> Designer revision loop on cited issues only, with an iteration cap -> the lead renders and delivers. The Critic is the premium seat; keep it whenever the visual ships or will be saved.
- **interactive.** As standard, plus the Designer builds the interactive as one self-contained client-side artifact, and the Critic always runs (interactives fail accessibility most often).

## How to brief each seat

- **★ Chief Data Officer.** The skill runs as the lead, so this is the frame it writes for itself in Phase 0 and threads into every dispatch: the request, the data or content, the question the visual must answer, the audience, and the chosen form and why. Use `templates/visual-brief.md`.
- **Visualization Designer.** Give the chosen form, the data (with each number's range, when it carries one), the integrity constraints, the palette or house style, and the render target (inline SVG, Mermaid, or self-contained HTML). It returns the artifact source plus a one-line note of the encoding choices.
- **The Design Critic, borrowed from the quality-assurance skill.** Its spec is that skill's `agents/Design Critic.md`, read by the absolute path of its folder, beside this one. Give the rendered visual or its source, the question it must answer, and the Critic's checklist from `principles.md`; withhold the maker's notes so it does not inherit the maker's blind spots. It returns the review: form-fit verdict, integrity findings, the accessibility gate result (PASS or FAIL with the failing checks), clarity notes, and a ship-or-hold call. It never fixes.
- **Data Analyst, when the data needs it.** Give the raw data, what the visual will plot, and the question; it returns the cleaned data with each change and its reason, and never changes a value to make the picture nicer.

## By-demand collaborations

- **The analysis mode.** When the visual draws the company's numbers and they are not yet computed, checked or defined, the analysis runs first (`dispatch.md`), so the chart draws verified numbers with their ranges. Most requests arrive with clean data and need no wrangling.
- **The research-and-development skill.** When an interactive grows into a real application (a backend, persistence, a deploy), it is no longer a widget; escalate to the research-and-development skill for the full build lifecycle. A disposable inline widget stays with the Visualization Designer.

## The fix loop

A Critic HOLD or a failed accessibility gate resumes the Visualization Designer on the cited issues only; re-render, then re-run the Critic on the cited items with a fresh pass. If the same blocking issue survives two rounds, stop and surface it to the user: it usually means the data or the request cannot honestly produce the asked-for visual.
