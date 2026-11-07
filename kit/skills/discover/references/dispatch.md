# Dispatch - how the tiers map onto the Discovery team

How `discover` spends the Discovery team, scaled to the challenge. Read before choosing a tier. The roster is the lead plus five: Creative Lead, Idea Generator, Idea Critic, Tournament Ranker, Idea Curator, Portfolio Manager. Every dispatch is a self-contained brief; the subagent sees none of the conversation; generators run in parallel and never see each other's ideas while generating; the lead alone holds the brief, runs the kill-gate, and synthesizes.

## Tier decision table

| Signal | Tier |
|--------|------|
| A few quick angles, low stakes, a small question | quick |
| A real challenge worth a wide field and a fair ranking | standard |
| High-stakes, or a cross-venture / cross-project portfolio call | deep / portfolio |

When two rows fit, take the higher. Announce the tier before dispatching.

## What runs at each tier

- **quick.** The Lead frames a how-might-we, dispatches one or two Idea Generators on distinct lenses, dedups the small pool, and picks a short ranked list. No full tournament; reserve for a fast spread.
- **standard.** Lead frames and assigns lenses -> N Idea Generators in parallel (isolated, judgment deferred) -> Curator dedups against the whole pool including killed ideas -> Critic steelmans then stress-tests the survivors -> Tournament Ranker runs the pairwise Elo tournament -> Generators evolve and recombine the top, which re-enter the tournament -> Lead applies the kill-gate -> ranked shortlist with a recommendation.
- **deep / portfolio.** As standard, with more lenses and more tournament rounds, plus the Portfolio Manager weighing the developed survivors across ventures by RICE. Ships a full discovery report, in chat or filed per Filing below.

## How to brief each agent

- **Creative Lead.** Give the raw challenge and any constraints. He returns the framed how-might-we questions and the dispatch plan, then orchestrates, runs the kill-gate, and synthesizes the shortlist. Use `templates/generative-brief.md`.
- **Idea Generator.** Give the framed HMW and ONE assigned lens (from `references/lenses.md`), with the rule to defer judgment, go for quantity, and welcome wild ideas. She returns a list of candidate ideas. Dispatch several in parallel, each on a contrasting lens; this is the load-bearing parallel-independent-generation step.
- **Idea Curator.** Give the raw pool. She dedups against the whole pool including killed ideas, merges near-duplicates (keeping the higher-Elo record canonical), and keeps the idea records. Returns the deduped set.
- **Idea Critic.** Give the survivors. He steelmans then stress-tests each for novelty, feasibility, and fatal flaws. Returns the classified critique; he never picks the winner.
- **Tournament Ranker.** Give the shortlist. He runs the pairwise Elo tournament and returns the stable order with Elo scores and games played.
- **Portfolio Manager.** Fired only on a cross-venture or cross-project call. Give the developed survivors across the portfolio; he weighs them by RICE and returns a portfolio-balanced ranking.

## Collaborations

- **Research team.** Ideation and research are duals: research grounds an idea in evidence, and ideation produces hypotheses research then tests. Reach for `research` when an idea turns on a fact that must be verified.
- **The domain team.** When the challenge concerns a venture or a project, work with the team that owns that domain (an Agent Resources department of the board workforce, or the project crew) for context, data, and feasibility grounding. The domain team informs the ideas and judges feasibility; it does not pick the winner, which the tournament settles fairly.

## Filing

By default the run delivers the ranked shortlist in chat and files nothing. On request, the surviving ideas file as records (`templates/idea-record.md`, deduped against any existing pool first, including killed ideas) and a finished discovery report is written, each where the repository's instructions say ideas and reports go, or where your user names. Follow those instructions' rules for the folder (an index to update in the same edit, the checks to run after a write). With neither an instruction nor a named path, ask before writing anywhere.
