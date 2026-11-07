---
name: identify
description: Interviews the user about themselves with validated frameworks (Big Five, HEXACO, Schwartz values, McAdams life story) to build and deepen their profile one facet at a time, from Working Style and Personality to Values and Goals. Use when the user types /identify, says interview me, fill out my profile, help me populate my Working Style, get to know me better, or asks to confirm unconfirmed profile entries, and proactively when a profile facet is found thin or template-empty, even when they never say identify. Mixed structured and conversational questions with skip options and a consent gate on sensitive topics; every inference is marked and reviewed blind, and only an approved proposal batch is kept. In a private repository whose instructions say it holds the user's profile, it writes the approved batch there; anywhere else it returns the approved profile in the conversation and writes nothing about the user.
license: MIT
allowed-tools: Read, Grep, Glob, AskUserQuestion
metadata: { team: "Research & Development (R&D)", version: "1.1.0", id: sy-skill-identify-spec, author: Tanner Golden, status: active }
---

# 🪪 Identify

Identify builds and deepens the user's profile by interviewing them about themselves: it finds what is thin, plans a short mixed-delivery interview from validated frameworks, and turns the answers into a reviewed proposal batch the user approves line by line. The one standard, which wins every conflict: **nothing enters the profile unapproved or unmarked**. Every kept line is either a verbatim-traceable self-report or an inference carrying the full provenance marker, and nothing is kept before the user says yes.

> Operating doctrine lives in `references/`. Read `references/interviewing.md` before asking anything, `references/question-maps.md` before planning the interview, and `references/provenance.md` (the marker grammar and the profile rules) before composing or keeping a single line.

## Where the profile lives

Read the repository's own instructions first (its `AGENTS.md` or `CLAUDE.md` and the rules of any folder it would write into). They decide which of two cases this run is in:

- **A profile repository.** Its instructions say it is a private repository made to hold the user's profile, and name where the profile facets live and which checks to run after a write. There, the run writes the approved batch where those instructions put each facet, follows their rules for every write, and runs the checks they name. Their profile rules add to the ones in `references/provenance.md`; where the two differ, the stricter wins.
- **Anywhere else** (any other repository, or a conversation with no repository). The run returns the approved profile in the conversation, ready for the user to keep wherever they keep it, and writes nothing about the user into the repository, not even when asked: the repository is not one made to hold personal context (SEC-003, the Constitution's privacy rule). Say so plainly if the user asks for a file.

## Facets

The skill's own facet vocabulary, with each facet's sections and items in `references/question-maps.md`: **Working Style, Personality, Biography, Lifestyle, Skills, Preferences, Goals, Focus** (non-sensitive), and **Health, Finances, Values, Relationships** (sensitive, opened only through the consent gate). A profile repository may file them differently; its instructions say where each lives.

## Modes

| Mode | Trigger | What it does |
|------|---------|--------------|
| **interview** | `/identify`, "interview me", "get to know me better", "fill out my profile", or a facet found thin in passing | Picks the target facet (below), then the full pipeline runs |
| **confirm** | "confirm my unconfirmed profile entries", or a confirm sweep is due | Targets existing `unconfirmed` markers (in a profile repository, or in a profile the user pastes or points to): short confirmation asks, then markers shortened to `confirmed` or the line corrected, through the same batch, review, and approval path |
| **facet-named** | The caller names a facet ("let's fill in my Working Style", "/identify Health") | Caller-named wins over coverage; the pipeline runs scoped to that facet, consent gate included when it is sensitive |

## The architecture it serves

This skill composes the **Research & Development (R&D)** department of the board skill's Agent Resources workforce, the home of its embodied lead. Three seats, all reuse, constant across runs: the skill **embodies the UX and Design Research Lead** (UX and Design Research Lead, the board skill's `agents/UX and Design Research Lead.md`) as the interviewer, so only the top-level context converses and calls the question tool; the **Writer** (Writer, the editorial skill's `agents/Writer.md`) composes the proposal batch; the **Standards Reviewer** (Standards Reviewer, the research skill's `agents/Standards Reviewer.md`) reviews it blind against the profile rules. `metadata.team` names the embodied lead's home department, and the two dispatched seats are referenced by name from their own skills. Nothing is copied locally. Seats, briefs, verdict vocabulary, and rejected alternatives: `references/roster.md`.

## The interview pipeline

1. **Preflight.** Read the repository's instructions and settle which case this is (Where the profile lives). In a profile repository, read its profile rules and the target facet's current content. Then read `references/interviewing.md`, `references/question-maps.md`, and `references/provenance.md`. Announce as the UX and Design Research Lead embodied, no handoff ceremony: curious, grounded, one line of what is about to happen.
2. **Target.** A caller-named facet wins. Otherwise, if the repository's instructions name a coverage command, run it and take its target (the thinnest facet). Otherwise ask the user which facet, with one question-tool ask offering three non-sensitive facets and "another facet" (the user names it); take the one they choose.
3. **Consent gate.** Sensitive facets (Health, Finances, Values, Relationships) open only on opt-in: one question-tool ask offering that facet, two non-sensitive alternatives (the next-thinnest by coverage when there is a coverage command, otherwise two not yet covered this session), and "not today". Non-sensitive facets get a one-line announcement ("Working Style is still empty; about 10 questions, say stop anytime").
4. **Section detail + plan.** Find the facet's gaps: the coverage command's per-facet detail when it has one, the facet's current content in a profile repository (and a search for `unconfirmed` in it), or, with neither, the facet's sections in `references/question-maps.md` less anything the user has already told you in the conversation. Fill `templates/interview-plan.md`: max 2 confirm-pass items for existing unconfirmed markers first, then the highest-signal unfilled sections per `references/question-maps.md`; Snapshot always last; about 10 questions (6 to 8 for sensitive facets).
5. **Interview loop.** Scaled items via the question tool, batched up to 4 per call within one framework block, max 4 options each; every sensitive-facet question and sensitive-adjacent item carries an explicit "Prefer not to say" option (never the tool's free-text Other as the skip). Narrative items one at a time in chat prose; simple fact clusters as one compact chat question. Skips honored silently: no follow-up, no recording of the refusal anywhere. Keep the session ledger: verbatim answers tagged stated; lead observations tagged observed with confidence.
6. **Checkpoint at about 10 questions** (question tool): continue 10 more, switch to another thin facet, or wrap to proposals. Any stop signal goes straight to step 7 with whatever was gathered.
7. **Compose (dispatch the Writer).** Self-contained brief in the `references/roster.md` shape: the interview ledger inline, the facet's current content (its file paths in a profile repository, or the profile the user shared, if any), `references/provenance.md`, and `templates/proposal-batch.md`. The Writer returns the batch and persists nothing.
8. **Review (dispatch the Standards Reviewer, blind).** Inputs: the batch, the profile rules in `references/provenance.md` plus a profile repository's own rules, SEC-003, and the marker grammar; never the interview reasoning or the Writer's brief. One ledger row per proposal: BLOCK, REVISE, or CLEAR. Verdicts apply mechanically: REVISE applied, BLOCK dropped or re-marked, one round only.
9. **Present the proposal batch** in chat in the `templates/proposal-batch.md` shape: numbered proposals per facet (per file in a profile repository) with markers visible, then record offers, then skipped items (shown once, never kept). Approval is explicit and line-item capable: approve all, approve except N, or per item. No answer, nothing kept.
10. **Keep the approved batch (the skill is the sole writer).** In a profile repository: make each approved change where its instructions put that facet, following their rules for edits (for example, committing a file's last state first or bumping an `updated:` date, when they ask for it); create a new entry from the template its instructions name for that kind of entry, when they name one; then run the checks its instructions name on every touched file, which must pass. Anywhere else: return the approved profile in the conversation, one block per facet with its sections, markers kept as approved, and write nothing about the user into the repository.
11. **Record offers.** People, events, dates, and decisions are records, never profile lines (`references/provenance.md`, the records boundary). In a profile repository whose instructions say where such records go, offer each one and write each approved record there in the format they set. Anywhere else, list them in the conversation for the user to keep and write nothing.
12. **Closing.** Report written (or returned), confirmed, and deferred counts; offer (never silently) a session log entry only where the repository's instructions keep such a log; name another thin facet as the natural next run; in a profile repository, confirm its checks are clean. No unapproved text remains anywhere.

## Dispatch scaling

Posture scales by sensitivity, not by roster size; the seats are constant.

- **Non-sensitive facet run** (Working Style, Personality, Biography, Lifestyle, Skills, Preferences, Goals, Focus): announce and go; about 10 questions to the checkpoint; the Writer then the Standards Reviewer on the batch.
- **Sensitive facet run** (Health, Finances, Values, Relationships): consent gate first, 6 to 8 questions, explicit skip on every item, gentlest register; the Writer then the Standards Reviewer on the batch, and the Standards Reviewer's blind review is non-negotiable here.
- **Aborted run** (stop before any answers): dispatch nobody; close with what is thin and the offer to run later.
- Every run that produces a proposal batch dispatches the Writer then the Standards Reviewer, the Standards Reviewer always and always blind. There is no batch too small to review.

## Design basis

The items rest on the frameworks named per facet in `references/question-maps.md`: BFI-2 facets and HEXACO Honesty-Humility for Personality, Schwartz's four higher-order value families and Moral Foundations for Values, Self-Determination Theory for motivation, VIA character strengths, Erikson life stage, McAdams narrative identity for Biography, and the assistant custom-instruction schema for Working Style. The framework names stay in the plan and the ledger, never in the question the user hears.

## Quality bars

- **Nothing enters the profile unapproved or unmarked**, the one standard. Unmarked lines must be verbatim-traceable to a ledger answer; when in doubt, mark (`references/provenance.md`).
- Provenance tokens are exact and machine-queryable: `observed` | `confirmed` | `reviewed` with ISO date, optional `confidence: low|medium|high`, proposal flag `unconfirmed`. A search for `unconfirmed` must find every pending proposal afterward.
- Skips are silent and stateless: never probed again, never recorded anywhere, session-only.
- One construct per question, non-leading, 3-point scales plus skip where scaled; hard caps (checkpoint at about 10, 6 to 8 on sensitive facets).
- No em dashes anywhere (DOC-002); the shared validator fails on the character.
- Tools declared exactly: `allowed-tools` is the minimal read-only set the workflow calls.
- Record-shaped facts (people, events, dates, decisions) route to record offers, never into a profile line (`references/provenance.md`, the records boundary).
- Personal context never lands in a repository not made to hold it (SEC-003).

## Boundaries

- Stay within profile interviewing and keeping the approved batch. Never write unapproved or unproposed text, never record a refusal, never open a sensitive facet without opt-in, never re-probe a skip, never store people, events, dates, or decisions in the profile (they are record offers), and never write a record beyond the approved offers. Confirm-first governs every write; never create or delete top-level folders.
- vs **research**: questions about the world route to research; identify asks the user about themselves. "Research Big Five versus HEXACO" is research, not identify.
- vs **editorial**: a prose file under instruction is editorial's; identify keeps only the approved proposal batch.
- vs the **normal write path**: a user-dictated update ("update my Focus: heads-down on the launch") is a direct edit, which the profile rules allow when the user asks (in a profile repository; elsewhere it is just noted in the conversation), no interview needed; identify is for eliciting, not transcribing.
