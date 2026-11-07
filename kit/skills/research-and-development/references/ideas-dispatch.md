# Dispatch - the ideas mode, per tier

How the skill spends its seats on an ideas run, scaled to the challenge. Read before choosing a tier; the lead's own method, the tournament included, is in `lead-ideas.md`. The R&D team supplies the lead (★ Head of Research & Development), who frames, runs the pairwise Elo tournament itself and applies the kill-gate, and the Idea Generators, who diverge, evolve and, in a curation pass, keep the pool. Every dispatch is a self-contained brief; the subagent sees none of the conversation; generators run in parallel and never see each other's ideas while generating; the lead alone holds the brief, runs the tournament and the kill-gate, and synthesizes.

**Borrowed seats, not members.** The critique borrows the quality-assurance skill's **Devil's Advocate**, which steelmans then stress-tests the pool and returns its idea verdict ledger. A call across ventures or projects borrows the administration skill's **Chief Operating Officer** for the RICE portfolio weighing. Each is dispatched by title from its own skill's `agents/` folder, installed beside this one, and never copied here.

## Tier decision table

| Signal | Tier |
|--------|------|
| A few quick angles, low stakes, a small question | quick |
| A real challenge worth a wide field and a fair ranking | standard |
| High stakes, or a portfolio call across ventures or projects | deep / portfolio |

When two rows fit, take the higher. Announce the tier before dispatching.

## What runs at each tier

- **quick.** The lead frames a how-might-we, dispatches one or two Idea Generators on distinct lenses, dedups the small pool, and picks a short ranked list. No full tournament; reserve it for a fast spread.
- **standard.** The lead frames and assigns lenses -> N Idea Generators in parallel (isolated, judgment deferred) -> an Idea Generator's curation pass dedups against the whole pool, killed ideas included -> the Devil's Advocate steelmans then stress-tests the survivors -> the lead runs the pairwise Elo tournament -> the Generators evolve and recombine the top, which re-enter the tournament -> the lead applies the kill-gate -> a ranked shortlist with a recommendation.
- **deep / portfolio.** As standard, with more lenses and more tournament rounds, plus the Chief Operating Officer weighing the developed survivors across ventures and projects by RICE. Ships a full ideas report, in chat or filed per Filing below.

## How to brief each seat

- **The lead.** Holds the raw challenge and any constraints, frames the how-might-we questions in `templates/generative-brief.md`, plans the dispatch, runs the tournament and the kill-gate, and synthesizes the shortlist (`lead-ideas.md`).
- **Idea Generator, diverge.** Give the framed how-might-we and ONE assigned lens (from `lenses.md`), with the rule to defer judgment, go for quantity, and welcome wild ideas. It returns a list of candidate ideas. Dispatch several in parallel, each on a contrasting lens; this is the load-bearing parallel-independent-generation step.
- **Idea Generator, curation pass.** Give the raw pool, any filed pool (live and killed), and the schema in `brief.md` (The idea record). It dedups against the whole pool, killed ideas included, flags near-duplicates for a merge the lead confirms (the higher-Elo record stays canonical), and keeps the idea records. Returns the deduped set.
- **Devil's Advocate** (borrowed). Give the deduplicated survivors and the challenge they address, in the quality-assurance skill's `templates/brief.md` shape, never the generators' reasoning or the lead's preference. It steelmans then stress-tests each for novelty, feasibility and a fatal flaw, and returns its idea verdict ledger in the quality-assurance skill's `templates/critique-ledger.md` shape: KEEP, FLAW (the flaw to evolve on) or KILL, with an evolution-potential mark on each KEEP and FLAW. It never picks the winner. Its method is the quality-assurance skill's `references/critique.md`.
- **Idea Generator, evolve.** Give the ideas the lead marked to evolve (the top by Elo plus the critique's high-evolution-potential survivors) and, for a FLAW, the named flaw. It returns the variants with their parents, which re-enter the tournament.
- **Chief Operating Officer** (borrowed). Fired only on a call across ventures or projects. Give the developed survivors across the portfolio and the strategic priorities; it weighs them by RICE (`convergence.md`) and returns a portfolio-balanced ranking.

## Applying the critique

The lead applies the idea verdict ledger mechanically, by the rule in the quality-assurance skill's `references/verification.md`: a KEEP enters the tournament; a FLAW goes to an Idea Generator to evolve on the named flaw, then re-enters; a KILL leaves the pool and stays recorded as killed, so the team never re-treads it. An idea too vague to steelman is sent back to be sharpened, not killed. Ideas are options, not deliverables, so the ledger ranks nothing: the order is the tournament's, and the choice is the user's.

## Collaborations

- **The research mode.** Ideation and research are duals: research grounds an idea in evidence, and ideation produces hypotheses research then tests. Run the research mode when an idea turns on a fact that must be verified.
- **The domain department.** When the challenge concerns a venture or a project, the run takes the context, data and feasibility read of the department that owns that ground (its skill's records where the repository's instructions keep them, or through the administration skill's Chief of Staff). The department informs the ideas and judges feasibility; it does not pick the winner, which the tournament settles fairly.

## Filing

By default the run delivers the ranked shortlist in chat and files nothing. On request, the surviving ideas are filed as records (`templates/idea-record.md`, deduped against any existing pool first, killed ideas included) and a finished ideas report is written, each where the repository's instructions say ideas and reports go, or where the user names. Follow those instructions' rules for the folder (an index to update in the same edit, the checks to run after a write). With neither an instruction nor a named path, ask before writing anywhere.
