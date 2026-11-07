# legal-and-compliance Changelog

## Current Version

**`2.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: tiers, the team, references, templates, the gate, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The workforce is twelve departments, one skill each, covering every area of a company and of the Founder's personal life. Renamed: the `legal` skill is now `legal-and-compliance`, named for its department, and its team keeps the title Legal & Compliance (L&C), four seats with the ★ General Counsel as lead. Absorbed: the research skill's Standards Reviewer is merged into the Compliance Officer, which now also keeps the legal, ethics and standards gate on sensitive or external-facing output from any department or the Founder (libel and defamation, privacy, intellectual property and licensing, regulated claims, disclosure), returning an exposure ledger with a BLOCK, REVISE or CLEAR verdict per exposure; and the blind privacy review of the profile interview, which the human-resources skill now holds, goes to the Privacy & Data Protection Counsel, which reviews every proposal batch blind (never the interview reasoning or the brief to the public-relations skill's Writer) against the human-resources skill's `references/provenance.md` and SEC-003, and returns one BLOCK, REVISE or CLEAR row per proposal in the shape that skill's `references/roster.md` gives, on the brief that roster sets. Personal life joins the scope, where it was out of it before: leases and the Founder's own contracts, personal disputes, wills, powers of attorney and health-care directives, and the Founder's own privacy rights, with every deliverable stating the lawyer line (a licensed lawyer must review before the act, and which kind; or no trigger fires, and why) and a referral table for personal matters. New: `references/standards-review.md` (the standards gate's brief, its five exposures and its verdict rules, and how the seat runs the profile review) and `templates/exposure-ledger.md` (the standards gate's ledger); the deliverables, dispatch and doctrine references, the brief, contract-review, dispute-triage, privacy-assessment and records templates, the roster and all four specs updated; the personal context and health rules added to the roster's global rules; every other department named by its new skill (administration, finance-and-accounting, human-resources, information-technology, customer-experience, public-relations, quality-assurance, research-and-development, sales-and-marketing, operations-and-logistics); the trigger test redrawn for the merged and personal scope.

### `1.0.0` - 2026-11-07

Initial build of the legal skill: the Legal & Compliance (L&C) department of the board skill's workforce becomes its own skill, for a company the user runs. The skill embodies the ★ General Counsel and dispatches the Commercial Counsel, the Compliance Officer and the Privacy & Data Protection Counsel across entity formation, contracts, IP, the compliance program, privacy and data protection, and dispute triage, to one standard, never bound blind, with cite the law and its date as its craft rule. Three tiers (quick, standard, deep); a law check against the official source, dated, on every rule a deliverable turns on, so the three counsel seats now carry the web tools; verification by the quality skill's ★ Head of Quality; referral triggers for where a licensed lawyer must review; and a write-gate under which the skill never signs, sends or files anything. Three references (deliverables, dispatch, doctrine), five templates (brief, contract review, privacy assessment, dispute triage, legal records) and the trigger tests. The roster and specs move from the board skill's `agents/`: their global rules now live in the roster, every seat in another department is named by its skill, and the department persists its own records where the repository's instructions keep them.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
