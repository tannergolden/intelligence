# Provenance - the law of the mark

The profile interview's marking contract and the profile rules, read before composing or keeping a single line. The marker grammar here is the skill's own; when a profile repository's instructions define a provenance convention of their own, follow theirs and keep the same two-species discipline, so the marks this skill writes match the ones already in that profile. The one standard it serves: **nothing enters the profile unapproved or unmarked**. Every proposed line is either a verbatim-traceable self-report that carries no marker, or an inference that carries the full marker and stays a proposal until the user approves it.

## The two species of line

- **Stated (unmarked).** What the user actually said or selected, verbatim-traceable to a `stated` row in the interview ledger. A self-report is the default and needs no marker; a plain line is a self-reported fact. If a line cannot be traced word-for-word to a ledger answer, it is not stated, and it is not allowed to go in unmarked.
- **Observed or inferred (marked).** What the interviewer noticed rather than was told: a pattern across answers, a tone, an aside. An inference is written only with the full marker and always as a proposal (`unconfirmed`). The profile rules (below) make this absolute: an inference is never presented as a fact. When in doubt, mark.

An assumed claim, one in neither the stated nor the observed column of the ledger, does not exist and is never written in either form (`interviewing.md`, the ledger).

## The marker grammar

The marker is an inline HTML comment appended to the end of the line. It renders invisibly on GitHub and in any Markdown preview but stays in the source, so the fact reads clean while the provenance stays machine-queryable:

```
**Field:** value <!-- observed 2026-07-04 · confidence: medium · unconfirmed -->
```

Three parts, in this fixed order, so the tokens stay filterable across the whole profile:

1. **State token, with an ISO date.** Exactly one of `observed` | `confirmed` | `reviewed`, followed by a `YYYY-MM-DD` date.
   - `observed` - the AI inferred it from evidence. Always paired with `unconfirmed` when first written.
   - `confirmed` - the user approved it. The date is the confirmation date.
   - `reviewed` - a standing line re-verified later; stamped on drift-prone sections (occupation, current chapter) when confirmed to still hold.
2. **Confidence, optional.** `confidence: low | medium | high` on `observed` lines, grading how strong the evidence is. Omit it on a `confirmed` or `reviewed` line, where confidence is no longer the question.
3. **The proposal flag.** `unconfirmed` marks a line that is a proposal awaiting approval, never treated as established (the profile rules, below). Every inference this skill proposes carries it until the user says yes.

The separator between parts is the middle dot ` · `. Never a dash of any kind between marker parts.

## The lifecycle

```
observed + unconfirmed   ->   confirmed   ->   reviewed
(an AI inference,             (the user           (re-verified
 a live proposal)             approved it)         later, on use)
```

- A newly proposed inference is `<!-- observed <date> · confidence: <level> · unconfirmed -->`.
- On the user's approval, the marker shortens to `<!-- confirmed <date> -->` (confidence and the proposal flag both drop), or the marker is removed entirely, since a confirmed fact is just a fact.
- A stated fact never enters this lifecycle: it is unmarked from birth.
- A corrected confirm-pass line becomes a new stated fact and loses its marker; a shrugged one keeps its existing marker untouched.

## Examples

Stated (traceable to a `stated` ledger row, so no marker):

```
- **Default length:** terse; the bottom line first, reasoning only on request.
```

Observed or inferred (a live proposal, fully marked):

```
- **Regulatory focus:** prevention-leaning; frames choices around avoiding downside <!-- observed 2026-07-04 · confidence: low · unconfirmed -->
```

The same line after the user confirms it:

```
- **Regulatory focus:** prevention-leaning; frames choices around avoiding downside <!-- confirmed 2026-07-04 -->
```

A drift-prone standing line, re-verified on use:

```
- **Occupation:** founder, building a software startup <!-- reviewed 2026-07-04 -->
```

## The query guarantee

Because the tokens are fixed, the profile stays queryable, and the skill's exit state must satisfy it: after a run, a search for `unconfirmed` returns every pending proposal the run wrote, and nothing that was approved and shortened. A search for `confidence: low` surfaces the weakest inferences for a later re-check. A proposal the user did not approve is either dropped or left carrying `unconfirmed`; it is never quietly promoted by removing the flag without approval.

## The profile rules

These govern every line this skill proposes or keeps, wherever the profile lives. A profile repository's own rules add to them; where the two differ, the stricter wins. The legal-and-compliance skill's Privacy & Data Protection Counsel reviews every batch against them, blind (`roster.md`).

- **Read-only by default.** The profile is the user's own description of themselves and never changes on inference alone; a line changes only when the user asks or approves.
- **Propose, never write silently.** Whatever the run learns is shown as a proposal and kept only on an explicit yes.
- **Facts, not guesses.** Record only what the user said or the interviewer observed directly. Never speculate across sessions, and never present an inference as a fact: an inference carries its marker and stays `unconfirmed` until approved.
- **One home for who the user is.** A fact about the user lives in the profile and only there, never copied into a record.
- **The most care for sensitive categories.** Health and medical conditions, finances, relationships, political or religious views, legal matters, and mental health: record the minimum needed to be considerate, never a full account, and keep the most sensitive items terse and factual; a health line records what the user said, never a diagnosis, a treatment or a medication the run inferred. Absorb a profile as context; never quote it back.
- **Personal context stays where it is allowed.** The profile is written only into a private repository whose instructions say it is made to hold it; anywhere else it is returned in the conversation (SEC-003).

## The records boundary

Record-shaped facts never land in the profile, in any marker state. A person, an event, a date, or a decision is a **record offer**, not a profile line:

- A named person the user leans on -> offered as a person record, never a name written into Relationships.
- A dated happening the run surfaced -> offered as a log or event record, never an event line in Biography.
- A date that recurs (a birthday, an anniversary) -> offered as a dates record.
- A decision the user reports -> offered as a decision record.

Each offer is written only where a profile repository's instructions say such records go, in the format they set, once the HRIS and People Operations Analyst has checked it is not already kept; anywhere else it is listed in the conversation and nothing is written. The profile keeps only the user-fact phrasing (the relational style, the durable arc), and the record itself lives with the records. A fact about the user lives in exactly one place, the profile; the who, what, when, and which-decision lives in exactly one place, the records. The two never carry parallel copies. Sensitive-category discretion (the profile rules, above, and SEC-003) governs both: record the minimum needed to be considerate, never a full account.

## What the mark is not for

- A skip or a refusal is **never** written, in any marker state, anywhere (`interviewing.md`). The mark records what was proposed, never what was declined.
- A confidence grade is not a hedge to smuggle a guess past approval: `confidence: low` still needs the user's yes, and the blind review still applies (`roster.md`). Low confidence lowers the bar for how the line is phrased, never for whether it may be written.
