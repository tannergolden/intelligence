# Reporting - the research mode's output, filing, and freshness

How a run's findings are delivered, filed, and kept fresh. This is the kit's model, and it overrides any per-volatility scheme a generic research skill would use. Where a report is filed, and how it is named, indexed and linked, is set by the repository's own instructions (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files, and the folder rules they name), which the lead reads first; this file supplies the method and the defaults for what they leave open.

## Chat first, file on request

Every run delivers a **cited chat synthesis, findings first**, in a fixed shape: **Bottom line** (the answer with its two-axis certainty) -> **findings by angle**, each inline-cited and source-tier-aware -> **disagreements and the falsifier** (what would change the conclusion). Findings first, never a narrative of the run. A report **file** is produced only when the user asks for one, or by a standing instruction in the repository's instructions, so the repository stays lean. Offer it; do not file by reflex.

**Resolve before shipping (a stop step).** Before any deliverable ships, chat or file, resolve every load-bearing URL (live, dead, or fabricated): any that does not resolve is cut or replaced before the synthesis ships, never shipped with a caveat. A measured 3-13% of deep-research citations are fabricated, so this is a gate, not a hope.

## The Step-0 check (before every non-quick run with filed reports to check)

When the repository's instructions point to filed reports (a reports folder, an index, or both), the lead canonicalizes the topic (reduce the question to its topic slug, then match it against existing report titles and `keywords`) and checks those reports for an existing one first; on a near-match it returns the candidate and the lead, who is the one talking to the user, confirms it is the same topic before reusing. A report still inside its three-month window is **reused** (a quick confirmation of its load-bearing claims refreshes the window without a rewrite, reuse is review), not re-run. A match that has aged out is **refreshed in place**: same file, same `id` and `created`, advance `updated` and `review_by`; the report is rewritten as a fresh report, never as a diff. This check is the single largest token saver, so it runs first. With no reports location named, there is nothing to check, and the run proceeds.

## Polish before filing

A report that ships gets one final polish from the lead after the verify-and-critique round: findings first (bottom line, then key findings, then detail, so a reader can stop early and still be right), likelihood and confidence kept as two separate axes, every claim still carrying its citation, and padding cut so each fact is stated once. The lead may hand the prose polish to the public-relations skill's Editor, briefed never to alter substance, and then confirms every citation and hedge survived. The polish never alters meaning: a passage that cannot be cleaned without changing what it claims goes back to the quality-assurance skill's Fact-Checker or Devil's Advocate, and a cut that loses a finding or its citation is a bug.

## Filing a report

A filed report goes **where the repository's instructions say reports go**; with no such instruction, or no repository, it goes where the user names, after confirming the path. Never into the skill's own folder, which holds the team. One topic, one canonical file, named by the repository's naming rules, or `<Topic Title>.md` (the topic title alone, no prefix) by default, built from `templates/report.md` with the frontmatter the repository's rules require and a `review_by` date. **When the instructions keep a reports index, add the report's entry to it in the same edit** (in the index's own format: typically a link to the new file, its `review_by` "good through" date, and a one-line summary), so the index always mirrors the folder; a refreshed report has its index entry updated, a cleared one has it removed. Follow the repository's edit protocol when filing: commit first if overwriting under version control, write, then run the checks its instructions name.

## Flat three-month freshness

Every report is good through its `review_by` date, **three months** after it was filed or last verified, unless the repository's instructions set another window; after that it must be verified before reuse. One flat window covers all reports. The kit deliberately does not use per-volatility windows: the flat window plus the promote-to-durable step below is the whole freshness model.

## Link reports only the way the repository allows

A report is a working artifact: produced, consumed, refreshed, cleared. When the repository's instructions keep a reports index, that index is the one hub that links every filed report, and no other file links to one, which keeps the wider link graph free of disposable nodes; follow whatever stricter or looser rule the instructions set. Reports are also found by searching their folder.

## Promote to the durable layer (the explicit step)

The flat three-month window is correct only because durable findings do not live in reports. Before filing, the lead names any finding that must outlive three months and **promotes it into the durable layer** the repository's instructions name: a reference doc in its collection, a folder note, a skill's `references/`, or a proposed change to the instructions themselves. With no repository, name the finding as durable in the chat synthesis so the user can keep it. The disposable report then expires harmlessly; the durable finding persists and can be linked. A foundational result left to rot in an expiring report is the failure this step prevents, so make the promote decision explicit on every filed run, not an afterthought.

## Write-back

After a substantial run, offer (never silently) to record the distilled outcome where the repository's instructions keep such notes (a log entry, a decision or knowledge note, a session summary), if they keep any. The offer is the contract; the user decides. Nothing about the user is written into a repository unless its instructions say it is a private one made to hold it (the Constitution's SEC-003).
