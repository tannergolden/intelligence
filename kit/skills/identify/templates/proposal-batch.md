<!-- the Writer RETURNS one of these at pipeline step 7 (persists nothing); the Standards Reviewer reviews it blind at
     step 8; the embodied lead presents the reviewed version in chat at step 9 for line-item approval,
     then keeps the approved lines at step 10 (written into a profile repository, or returned in the
     conversation anywhere else). Every line is either verbatim-traceable and unmarked, or an inference
     carrying the full provenance marker and left `unconfirmed` (references/provenance.md). Record-shaped
     facts go under record offers, never into a profile line (references/provenance.md, the records
     boundary). Skipped items are shown once and never persisted. No em dashes; plain
     paths, no wikilinks. -->

# Proposal batch: [Facet name]

**Target facet:** [the facet]
**Run summary:** [written N · confirmed N · deferred N, filled at step 12]
**Review status:** [the Standards Reviewer reviewed blind: BLOCK N · REVISE N · CLEAR N; verdicts applied, one round]

## Proposed lines

Numbered, markers visible, grouped per file in a profile repository (as its instructions place the facet) and per facet anywhere else. Approve all, approve except N, or per item.

### [the facet file's path in a profile repository, or the facet name]

1. **[Section] -> add / edit:**
   ```
   - **[Field]:** [value]
   ```
   [stated - traceable to ledger answer [q-id], no marker]

2. **[Section] -> add / edit:**
   ```
   - **[Field]:** [value] <!-- observed [YYYY-MM-DD] · confidence: [low|medium|high] · unconfirmed -->
   ```
   [observed - the inference and the evidence it rests on]

3. **[Confirm-pass] -> shorten marker:**
   ```
   - **[Field]:** [value] <!-- confirmed [YYYY-MM-DD] -->
   ```
   [was `unconfirmed`; the user confirmed it this run]

### [the new entry's path in a profile repository, or the entry title] (new entry)

4. **New [belief|goal|skill|condition] entry:** [Title]
   - In a profile repository, created from the template its instructions name for this kind of entry, then the body edited to (anywhere else, the body alone):
   ```
   [the entry body, each line marked per provenance.md]
   ```

## Record offers (offered, never written into the profile)

Record-shaped facts route here, never into a profile line (`references/provenance.md`, the records boundary). Each is an explicit offer, written only where a profile repository's instructions say such records go, and otherwise listed here for the user to keep:

- **[Person]:** [what the ledger holds] -> offer a person record. [The profile keeps only the user-fact phrasing, e.g. The relational style; the person record lives with the records.]
- **[Dated happening]:** [what the ledger holds] -> offer a log or event record: "[the log line]".
- **[Decision]:** [what the ledger holds] -> offer a decision record: "[the decision]".

## Skipped this run (shown once, never persisted)

- [q-id / section]: skipped. [Listed here once so the approval view is complete; recorded nowhere, never re-probed.]

## Approval

Explicit and line-item capable: **approve all**, **approve except [N]**, or **per item**. No answer, nothing kept.
