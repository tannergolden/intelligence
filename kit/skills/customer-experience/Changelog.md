# customer-experience Changelog

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

The `customers` skill is renamed `customer-experience`, named for its department, one of the twelve that cover every area of a company the user runs and of the user's own life. Its team is renamed from Client Experience (CX) to Customer Experience (CX), with its roster renamed to `agents/Customer Experience (CX).md` and `metadata.team` to match; the three seats (the ★ Chief Customer Officer, the Customer Success Manager and the Support Specialist) keep their titles, and nothing was absorbed or merged into the team. The department now stands up for the user as a customer too: complaints, returns, refunds, warranty claims and subscriptions, which the description used to send to editorial as writing. New: `references/consumer.md` (the facts, the claim a first-tier agent can grant, the escalation ladder, returns and warranties, subscriptions, and the consumer gate), `templates/claim.md` and `templates/subscriptions.md`, personal deliverables and routing, personal gated acts in the write-gate, the personal context and health rules in `SKILL.md` and the roster's Global rules, and personal triggers in the description and the trigger test, where the airline complaint that was a near miss is now a positive. The skill and its two specialists gain `WebSearch` and `WebFetch`, so a seller's return policy, a warranty's terms and a provider's cancellation steps are fetched from their own pages and dated. Every mention of another department follows the renames (board to administration, sales to sales-and-marketing, quality to quality-assurance, systems to information-technology, communications and editorial to public-relations, finance to finance-and-accounting, legal to legal-and-compliance, operations to operations-and-logistics, analytics and visualize to business-intelligence, research and develop to research-and-development), and seats in other departments are named as the new skill's.

### `1.0.0` - 2026-11-07

Initial build of the customers skill: the Client Experience (CX) department becomes its own skill, laid out like discover, research and finance. The skill runs as the ★ Chief Customer Officer and dispatches the Customer Success Manager and the Support Specialist, scaled by tier (quick, standard, deep), to one standard: the customer's outcome first, and every loop closed. The roster takes develop's format with self-contained global rules; each spec points its Identity at the roster, names the skill that owns each routed cause (the quality skill for a defect, the systems skill for internal tooling, the finance skill for billing, the communications skill for a public incident, the sales skill for renewal pricing and expansion) in place of the retired departments, and carries the department's full scope: the knowledge base with support, and the voice of the customer with the lead. Four references (deliverables, dispatch, escalation, account health), four templates (the brief, the resolution, the account review, the voice-of-the-customer report) and a trigger test. Consequential work is verified by the quality skill's ★ Head of Quality, and every reply to a real customer, every refund or credit, and every published article waits for the user.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
