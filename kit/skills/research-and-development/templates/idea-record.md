---
title: "[short idea title]"
description: "[the idea in one sentence, restated as a description]"
id: "idea-[YYYYMMDD]-[4hex]"
statement: "[the idea in one sentence]"
lifecycle: "raw"        # raw | shortlisted | developed | promoted | parked | killed
ice: { impact: 0, confidence: 0, ease: 0, value: 0 }   # 1 to 10 each; value is the product
elo: 1500               # relative rank from the pairwise tournament; default 1500
elo_games: 0            # comparisons played; low means the rank is unsettled
lens: "[the generative lens that produced it]"
parents: []             # ids this idea evolved or combined from (plain ids, not links)
serves: "[the venture, project, or topic it is for; plain text, not a link]"
---

# [Idea title]

[A short paragraph: the idea, why it might work, and the open question or assumption it rests on. Keep it lightweight until it earns development. The id is the stable dedup and lineage key and is never reused; lifecycle and ice are kept by the Idea Generator's curation pass and elo by the lead's tournament as the idea moves through the pool. Idea records are leaves: parents are plain ids and serves is plain text, so the record links to nothing. Where the repository's instructions set their own frontmatter or file conventions for records, fit this scaffold to them.]
