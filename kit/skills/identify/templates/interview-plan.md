<!-- The embodied lead fills one of these at pipeline step 4, after the target is picked and the
     facet's gaps are found, before the interview loop. It is a working scaffold held in the lead's context,
     never persisted. Draw every item from references/question-maps.md; obey references/
     interviewing.md for delivery, batching, and the skip rules. Order is fixed: up to 2 confirm-pass
     items first, then the highest-signal unfilled sections, Snapshot never asked (the Writer composes it
     last). Cap: about 10 questions, 6 to 8 on a sensitive facet. No em dashes; plain paths, no wikilinks. -->

# Interview plan: [Facet name]

**Sensitivity:** [non-sensitive / SENSITIVE - consent gate cleared on <date>]
**Frameworks in play:** [the frameworks from this facet's question-maps entry]
**Cap for this run:** [about 10 questions / 6 to 8 for a sensitive facet]

## Coverage gaps

From the repository's coverage command and the facet's current content, in a profile repository whose instructions name them; otherwise from this facet's sections in `references/question-maps.md`, less what the user has already said in the conversation:

- **Thin or template-empty sections:** [list the sections the coverage command flags, or that hold nothing yet]
- **Existing `unconfirmed` markers in this facet:** [list them (from a profile repository or a profile the user shared), or "none" - these seed the confirm-pass items]
- **Highest-signal sections to target (question-maps fill order):** [the 2 to 4 sections that most change how an assistant helps the user]

## Ordered question list

Confirm-pass items first (max 2), then highest-signal unfilled sections, Snapshot never listed.

| # | Section | Construct | Delivery | Item / options | Skip |
|---|---------|-----------|----------|----------------|------|
| 1 | [confirm-pass, if any] | [the marked line] | tool | "I have you down as [X]. Does that hold?" / Yes / Correction / [skip] | [always] |
| 2 | [confirm-pass, if any] | [...] | tool | [...] | [always] |
| 3 | [highest-signal section] | [one construct] | tool / prose / cluster | [item text; for tool, the 3-point scale plus skip] | [required if sensitive or sensitive-adjacent] |
| ... | [...] | [...] | [...] | [...] | [...] |
| N | [Snapshot] | NOT ASKED | - | composed by the Writer from the run's material, proposed like any other line | - |

**Delivery notes.** Scaled items (tool) batch up to 4 per call within one framework block; max 4 options each. Narrative items (prose) go one at a time, never stacked. A fact cluster (cluster) is one compact chat question. Every sensitive-facet item and every sensitive-adjacent item carries an explicit "Prefer not to say" option, never the tool's free-text Other as the skip.

## Checkpoint

At about [10 / the sensitive cap] questions, the verbatim question-tool checkpoint (`interviewing.md`): Continue (10 more) / Switch facet / Wrap up to proposals. Any stop signal collapses the run straight to composition with whatever was gathered.
