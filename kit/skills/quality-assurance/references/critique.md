# Critique - conclusions, ideas and visuals

The method of the team's two critics: the Devil's Advocate, who attacks a conclusion and stress-tests ideas, and the Design Critic, who rules whether a visual ships. Read it before any critique, whether this skill runs it or another department's skill borrows the seat. The rule above both: **build the strongest version before you strike, and never fix what you judge**.

## Conclusions: the objection set

For a research draft, a recommendation, a strategy, a business case, a decision case, or the user's own plan for a big step.

1. **Attack the framing first.** Name what the work actually claims and the question it thinks it answers. A wrong frame is the costliest error: "which option is cheapest" answered perfectly is still wrong when the real question is "which survives a downturn".
2. **Steelman the strongest alternative.** Build the best rival explanation for the same evidence before striking, so the attack meets the conclusion at its strongest, not a straw version.
3. **Surface the load-bearing assumptions.** List what must hold for the conclusion to stand, and where each would break. Look for groupthink: a conclusion everyone agreed to quickly, an assumption nobody stated, a source everyone cites back to one origin.
4. **Name the falsifier.** Every FATAL and MATERIAL objection names the specific evidence that would overturn the conclusion. An objection with no named falsifier, or "I disagree" with no source, is not an objection.
5. **Classify, and default to refuted.** FATAL kills a conclusion; MATERIAL forces a change; MINOR is noted. When an objection cannot be resolved, it stands; it is answered only by the citation that settles it, never by assertion. Never inflate a MINOR to look rigorous, and never manufacture doubt where the evidence is clean: "the conclusion holds" is a finding too.

The caller responds to every FATAL and MATERIAL: it accepts (and changes the conclusion) or rebuts with the settling citation, and logs which. The Devil's Advocate runs blind to the Fact-Checker, because the two find different failures: a claim can be true, well cited and still carry a misframed conclusion.

## Ideas: the verdict ledger

For a pool of ideas to narrow, after generation and deduplication and before ranking. Generation and judgment never happen at once: ideas are generated with judgment deferred, then judged here, by a seat that generated none of them.

1. **Steelman each idea first.** Build its strongest version before testing it. Premature judgment is what kills creativity, so a bold idea never dies on a weak first read.
2. **Stress-test on three axes.** Is it genuinely **novel** (not obvious or derivative)? Is it **feasible**? Is it free of a **fatal flaw**? A feasible but obvious idea fails novelty; a dazzling idea that cannot be built fails feasibility.
3. **Verdict each idea.**
   - **KEEP** - sound on all three axes; it goes on to the ranking. A sound but incremental idea is a KEEP with low evolution potential.
   - **FLAW** - a specific, fixable flaw, named so the generator can evolve the idea against it; it re-enters after evolution.
   - **KILL** - a fatal flaw, named; it leaves the pool and stays recorded as killed, so it is never re-trodden.
4. **Mark evolution potential,** high or low, on each KEEP and FLAW, so the caller spends its evolution effort on the survivors worth it.
5. **When torn between FLAW and KILL,** default to FLAW and name the flaw, unless it is provably fatal.

A KEEP says an idea is sound, not that it wins: the ranking is the caller's (in the research-and-development skill, a pairwise tournament its ★ Head of Research & Development runs), and the choice among the options is the user's.

## Visuals: the design review

For a chart, a diagram, a dashboard, an interactive, an infographic or a slide visual. The one standard is **graphical integrity**: the visual never distorts what is true. Beneath it sits the craft rule, **legible and accessible**, which never outranks the truth. The Critic checks in this order, and the order matters.

### 1. Form-fit (first)

Is this the right form for the question and the data? A wrong form is FATAL even when the execution is flawless.

| The question is about | Form | Notes |
|-----------------------|------|-------|
| Comparison of values across categories | Bar or column | Sorted by value unless the order is inherent (time). Zero baseline. |
| A trend over ordered time | Line | Lines are compared to each other, so a non-zero axis is acceptable if clearly labeled. |
| Correlation between two variables | Scatter | A trend line only when it is honest. |
| Part-to-whole | Stacked bar, rarely a pie | A pie only for 2 to 3 slices; a sorted bar reads a ranking better. |
| A process or decision logic | Flowchart | One flow direction; decision branches labeled. |
| Static structure or components | Architecture or entity diagram | Grouped by subsystem; crossings minimized. |
| Object interaction over time | Sequence diagram | Time down the page; actors across the top. |
| Events along time | Timeline | A consistent scale; the events labeled, not the gaps. |
| Exploration of many values | Interactive | Overview first, then zoom and filter, then details. |
| A concept or mechanism | Explanatory illustration | One visual language; semantic, not decorative. |

### 2. Integrity

- **Charts:** a zero baseline on bars (clipping it is the most common lie); a lie factor near 1 (the size of the effect shown divided by the size of the effect in the data); geometry proportional to the numbers; no 3D, no dual y-axes (they manufacture spurious correlation), no area or bubble encoding of a single quantity; chartjunk removed; comparisons on a common scale; the most important quantity on the most accurately read channel (position on a common scale, then length, then angle, then area, then color).
- **Diagrams:** every real relationship present and no false one; edge crossings minimized; the flow direction and the hierarchy honest; notation consistent.

### 3. Accessibility (blocking, enumerated; WCAG 2.2)

- Text contrast at least **4.5:1**; large text (18 point, or 14 point bold) at least **3:1** (1.4.3).
- Non-text contrast: the parts of a graphic needed to understand it, and UI components, at least **3:1** against adjacent colors, not rounded: 2.99:1 fails (1.4.11).
- Information never conveyed by **color alone**: paired with a label, a pattern or direct labeling (1.4.1).
- A **color-vision-deficiency-safe palette**: Okabe-Ito for categorical data, viridis or ColorBrewer for sequential.
- A **text alternative** for every chart or diagram (1.1.1).
- For an interactive, controls **keyboard-reachable and labeled**.

Any failure fails the gate, and a failed gate blocks the ship.

### 4. Clarity

One clear takeaway; the title states the so-what; axes, units and legends labeled; for a dashboard, the headline on one screen without digging; for an interactive, overview first, then zoom and filter, then details on demand.

### The call

Each issue is classed **FATAL** (a wrong form, a lie, or a failed accessibility gate), **MATERIAL** (an integrity or form problem that forces a remake) or **MINOR** (clarity). **SHIP** when there is no FATAL or MATERIAL issue and the gate passed; otherwise **HOLD**, back to the maker on the cited issues only, then a fresh re-review of the cited issues and every mark the fix touched. A blocking issue that survives two rounds goes to the user: it usually means the data or the request cannot honestly produce the visual asked for.

## What a critic never does

- Fixes, rewrites, redraws or regenerates what it judges; the maker does.
- Critiques its own conclusion, idea or visual.
- Ranks the options or decides among them.
- Softens a finding to keep the peace, or invents one to look rigorous.

## Sources

- Analysis of competing hypotheses and red-team practice in intelligence analysis (the steelman, the falsifier, the load-bearing assumptions check).
- The research on idea selection: deferred judgment in generation, and steelmanning before critique.
- The Visual Display of Quantitative Information (graphical integrity, the lie factor, data-ink, chartjunk); "Graphical Perception," JASA, 1984 (the ranking of how accurately each channel is read).
- W3C WAI, WCAG 2.2 Understanding documents, success criteria 1.4.3, 1.4.11, 1.4.1 and 1.1.1; the Okabe-Ito Color Universal Design palette; viridis and ColorBrewer.
