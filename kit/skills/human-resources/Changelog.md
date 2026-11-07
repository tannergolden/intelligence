# human-resources Changelog

## Current Version

**`2.1.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, tiers, the team, references, templates, the gate, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The people skill is renamed human-resources, for its department, and covers the user's own life as well as a company's: it is one of the twelve department skills. It absorbs the identify skill (1.2.0) as its profile mode, with every variant and method kept: the interview, confirm and facet-named runs, the questions drawn from validated frameworks (Big Five with the BFI-2 facets, HEXACO, Schwartz values, Moral Foundations, Self-Determination Theory, VIA, Erikson and McAdams life story), the consent gate on sensitive facets, skips never recorded, the provenance markers, the blind review, and line-by-line approval, written only into a repository made to hold the user's profile and otherwise returned in the conversation. Identify's Interview team is retired: the profile interview now borrows the research-and-development skill's UX and Design Research Lead as the interviewer the skill embodies, the public-relations skill's Writer to compose the proposal batch, and the legal-and-compliance skill's Privacy & Data Protection Counsel for the blind review the retired Standards Reviewer did; before an approved record offer is written, the HRIS and People Operations Analyst checks it is not already kept. Identify's references (interviewing, question maps, provenance, roster) and templates (the interview plan and the proposal batch) move here, rewired to those seats, with a stop on a crisis added to the interview; its regression cases move to `assets/regression-cases.jsonl`, their ids prefixed `profile-`. Two personal modes are new: career, the user's own career and skills, which the ★ Chief Human Resources Officer runs with the HRIS and People Operations Analyst keeping the user's career record (`templates/career-plan.md`); and wellbeing, run by a new seat, the Wellbeing Specialist: sleep, activity, nutrition and stress routines, appointments and check-up schedules, and using health benefits, and a company's wellbeing program, never a diagnosis, a treatment or medication advice, always referring to a clinician, and to emergency services in a crisis (`references/wellbeing.md`, `templates/wellbeing-plan.md`). The roster's global rules now carry the personal context rule and the health line, and every seat in another department is named by its new skill: administration (was board), finance-and-accounting (was finance), legal-and-compliance (was legal), information-technology (was systems), public-relations (was communications and editorial), quality-assurance (was quality) and research-and-development (was research and develop).

### `1.0.0` - 2026-11-07

Initial build of the people skill: the Human Resources (HR) department of the board skill's workforce becomes its own skill, for a company the user runs. The skill embodies the ★ Chief Human Resources Officer, who carries role design, hiring plans and job descriptions, interview loops, compensation bands and offers, onboarding and performance, and dispatches the HRIS and People Operations Analyst for the people records, to one standard, one bar for everyone, with trace it to the record as its craft rule. Three tiers (quick, standard, deep); pay figures from a named, dated source and the work location's hiring rules checked at the official source; verification by the quality skill's ★ Head of Quality; and a write-gate under which every offer, every decision about a real person and every share of personal data waits for the user, and no sensitive identifier is ever recorded. Three references (deliverables, dispatch, doctrine), six templates (brief, role card, interview loop, offer, onboarding, performance review) and the trigger tests. The roster and specs move from the board skill's `agents/`: their global rules now live in the roster, every seat in another department is named by its skill, and the HRIS and People Operations Analyst now keeps the company's people records, where the repository's instructions keep them, in place of the workforce's agent roster.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

### `2.1.0` - 2026-11-07

The profile interview's composer is now the public-relations skill's Editor, since that skill retired its Writer. It is still a borrowed seat whose spec stays in public-relations' `agents/`: it composes the proposal batch from the interview ledger alone, in the user's own voice, every inference marked, in the shape of `templates/proposal-batch.md` and following `references/provenance.md`, and persists nothing. It composes the batch and never reviews it, so the three-way separation holds: the interviewer (the skill, as the research-and-development skill's UX and Design Research Lead) is not the composer, and the blind reviewer (the legal-and-compliance skill's Privacy & Data Protection Counsel) never sees the ledger or the composer's brief. The Editor's brief gains an OBJECTIVE that names the composing duty. `SKILL.md`, the roster and the lead's spec, `references/roster.md`, `interviewing.md`, `dispatch.md`, `deliverables.md` and `question-maps.md`, the brief, interview plan and proposal batch templates, and the guard of the regression case `profile-rc-001` follow.

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
