# operations-and-logistics Changelog

## Current Version

**`2.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The `operations` skill is renamed `operations-and-logistics`, named for its department, one of the twelve that cover every area of a company the user runs and of the user's own life. Nothing was absorbed or merged into it: the team keeps its title, Operations & Logistics (O&L), and its four seats (the ★ Head of Operations, the Process Analyst, the Program & Project Manager and the Vendor Manager). The department now runs the user's own life too: the household and its routines, errands, travel, a move, and the contractors and service providers on the home, through a new `references/household.md`, household deliverables and done-tests in `references/deliverables.md`, household routing in `references/dispatch.md`, household notes in the four templates, personal triggers in the description and the trigger test, and the personal context and health rules in `SKILL.md` and the roster's Global rules. The skill and the Program & Project Manager and Vendor Manager gain `WebSearch` and `WebFetch`, so a current fact a plan rests on (an entry rule, a contractor's license, a carrier's rate) is fetched from its source and dated. Every mention of another department follows the renames (board to administration, legal to legal-and-compliance, finance to finance-and-accounting, people and identify to human-resources, systems to information-technology, analytics and visualize to business-intelligence, quality to quality-assurance, customers to customer-experience, communications and editorial to public-relations, and research, discover and develop to research-and-development), and seats in other departments are named as the new skill's: the quality-assurance skill's ★ Head of Quality, the administration skill's ★ Chief Executive Officer, Chief Operating Officer and Chief of Staff, and the legal-and-compliance skill's Commercial Counsel.

### `1.0.0` - 2026-11-07

Initial build of the operations skill: the company's Operations & Logistics (O&L) department, which the board skill's workforce held until now, becomes a skill of its own that runs in any repository or a plain conversation. It dispatches its own team (the ★ Head of Operations, whom the skill embodies, with the Process Analyst, the Program & Project Manager and the Vendor Manager) to one standard, the constraint first, across standard operating procedures and process design, program and project plans, vendors and procurement, and logistics. Three tiers (quick, standard, deep); every consequential deliverable verified by the quality skill's ★ Head of Quality before it lands; a write-gate under which the skill persists only its own department's records and signing a vendor contract, paying a vendor, committing spend or sending anything outside the company waits for the user. The roster takes develop's format with self-contained global rules, every agent points at it, the board seats it escalates to are named as the board skill's, and the Vendor Manager hands contract terms to the legal skill and never signs or pays. Three references (deliverables, dispatch, doctrine), four templates (brief, SOP, program plan, vendor scorecard) and a trigger test.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
