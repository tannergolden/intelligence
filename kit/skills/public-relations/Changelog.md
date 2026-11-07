# public-relations Changelog

## Current Version

**`3.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, tiers, the team, references, templates, assets, the voice, slop and formatting doctrine, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `3.0.0` - 2026-11-07

The Writer (`agents/Writer.md`) is removed, and the team is four agents: the ★ Chief Communications Officer, the Crisis & Issues Communications Manager, the Media Relations Manager and the Editor. The lead now drafts every piece at every tier, in the loaded voice and the register the piece needs (everyday, long-form, technical): the named exception to the workforce's rule that leads orchestrate and do not labor, stated in the roster and the lead's spec. The generate-then-critique split stays, because the lead drafts and the Editor, a dispatched subagent, reads fresh, and the lead never gates its own draft. Quick is unchanged; standard is the lead's draft, the Editor's gate (structure, then the line), and the lead verifying the flagged claims, applying only the cited edits and shipping; deep is the Editor's structural pass, the lead's draft to its plan, the Editor's line pass, fresh, the lead's proof and verification, and the quality-assurance skill's verification before the piece is presented as ready. A cited issue the lead would contest in its own draft goes to the user, never overruled by the lead. The Writer's craft moves to a new `references/drafting.md`, written as how the lead drafts: the three registers, the method and its decision rules, what a finished draft carries, the before-and-after examples, the recovery rules, every load-bearing claim flagged and no fact added that the brief lacks. In the public-voice mode, the prose inside a deliverable (an internal announcement's body, an op-ed, a speech, a bio, the user's own statement) is drafted by the lead or by the specialist that owns the deliverable, and the Editor reads it, always when the lead drafted it. The human-resources skill's profile interview now borrows the Editor to compose its proposal batch, which the Editor composes and never reviews; `agents/Editor.md` carries the duty. `SKILL.md`, the roster, the lead's spec, `references/writing-dispatch.md`, `dispatch.md`, `deliverables.md`, `intake.md`, `voice.md` and `difficult-messages.md`, and the brief, communications plan and situation brief templates follow.

### `2.0.0` - 2026-11-07

The workforce is twelve departments, each one skill named for it, and this one is renamed from communications to public-relations; its team stays Public Relations (PR). It absorbs the editorial skill whole, every mode and method kept, so the skill now works in two modes. The **write** mode is editorial's procedure: writing, editing and formatting any prose a person will read (emails, messages, letters, documents, posts, long-form, technical docs), its quick, standard and deep tiers, the intake situation read and situation brief, the voice and slop doctrine, the formatting references, editing in place behind a diff, and its proactive firing on prose being written or edited in any repository, structurally scoped away from code, generated files, templates and skill and agent specs. The **public-voice** mode is communications' procedure (announcements, press, media, messaging and crisis), unchanged in its tiers and its true-on-the-record doctrine. The team's one standard becomes true and clear, in that order, with audience first, one message and voice fidelity as the craft rules beneath it. The team grows to five agents: the ★ Chief Communications Officer absorbs the Editorial Lead; the Writer joins from editorial and absorbs the Long-Form Writer and the Technical Writer as its long-form and technical registers; the Line Editor becomes the Editor (`agents/Editor.md`, titled Editor) and absorbs the Developmental Editor, structure first, then the line. The Editor reviews the Writer's work inside the team and polishes a public-voice deliverable with its message and facts fixed; the quality-assurance skill verifies anything consequential going outside, its Fact-Checker taking the load-bearing claims editorial once routed to the research skill. The personal scope is all of the user's own writing and email, reputation and public presence: drafting a personal email is ordinary writing, sending anything still waits for the user, and the personal context and health rules join the skill and the roster. Editorial's twelve references, four templates and two assets come in, its `tiers-and-dispatch.md` renamed `references/writing-dispatch.md` beside communications' own `dispatch.md`; `references/deliverables.md` gains the write mode's piece, and the doctrine and crisis references cover the user speaking in public. The trigger test merges both skills' cases, with personal-life positives and near misses routed to the neighbouring departments by their new names. Neighbours are named by their department skills (administration, finance-and-accounting, legal-and-compliance, sales-and-marketing, human-resources, information-technology, research-and-development, business-intelligence, quality-assurance, customer-experience); editorial's own history, to 1.8.1, stays in the repository's history.

### `1.0.0` - 2026-11-07

Initial build of the communications skill: the company's public voice becomes a skill of its own. The Public Relations (PR) department leaves the board skill's workforce and ships here as this skill's team, in `agents/`: the ★ Chief Communications Officer leads the Crisis & Issues Communications Manager and the Media Relations Manager, to one standard, true on the record, with audience first, one message as the craft rule beneath it. Three tiers (quick, standard, deep); the skill embodies the lead and dispatches the specialists on self-contained briefs; a statement with legal exposure is cleared by the legal skill, and the quality skill's ★ Head of Quality verifies anything consequential before it is presented as ready for release. Nothing is published or sent outside the company until the user confirms it. Four references (deliverables, dispatch, doctrine, crisis), six templates (the brief, the communications plan, the press release, the messaging house, the media brief, the crisis plan), and the trigger test. Called on its own, the skill persists only its department's records, where the repository's instructions keep them; in a board run, board convenes it and persists the run's results. The roster takes develop's format with its own global rules, and the agent specs point at it, name seats in other skills as that skill's own, and hold every release for the Founder.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
