# business-intelligence Changelog

## Current Version

**`2.0.0`**

Semantic versioning, `MAJOR.MINOR.PATCH`, with no leading zeros, as [SemVer 2.0.0](https://semver.org) requires. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The workforce becomes twelve departments, one skill each, named for its department. **Renamed:** the analytics skill is now `business-intelligence` (its folder, its `name` and every reference); the team keeps its title, Business Intelligence (BI), and the run workspace becomes `business-intelligence-runs/`. **Absorbed:** the visualize skill, whole, as the visual mode: any chart, graph, diagram, flowchart, timeline, dashboard or interactive visual, to a standard of graphical integrity, with every tier (quick, standard, interactive), its proactive use (a response whose data or structure lands better seen than read gets a visual unasked), its frame, make, gate and render method, and its save rules. Its references come in under their own names (`principles.md`, `palette.md`, `formats.md`, `inline-aesthetics.md`, `interactive.md`, `svg-craft.md`), its dispatch as `references/visual-dispatch.md`, its brief as `templates/visual-brief.md`, and its palette library as `assets/palettes.json`, the hex unchanged. **Merged:** the Design Lead into the ★ Chief Data Officer, who now frames every visual and picks its form, and never makes or reviews it; the Visualization Designer moves in from the Design team, which no longer exists; the Design Critic moves to the quality-assurance skill and is borrowed back for the visual integrity review above the quick tier; the Data Analyst now also cleans a visual's data, a duty visualize once borrowed from this team. **New:** the tracking mode for the user's own habits and metrics (`references/tracking.md`, `templates/tracker.md`), and the personal context and health rules in the skill and the roster. The analysis mode keeps its tiers (quick, standard, deep) and its method. Neighbours are named for their departments: administration, finance-and-accounting, sales-and-marketing, information-technology, legal-and-compliance, research-and-development, quality-assurance and public-relations. The description leads with the visual triggers, then the data and tracking triggers, then where neighbouring requests go. The visualize skill's own history, to its 1.6.1, stays in the repository's history.

### `1.0.0` - 2026-11-07

Initial build of the analytics skill: the company's Business Intelligence (BI) department, which board convened as part of its workforce, becomes a skill of its own that answers a company's business questions with its own data (metric definitions and the north star, the data model and its sources, dashboards and reports, and analysis), to the standard one definition, honest uncertainty, with the craft rule compute, never recall. The skill embodies the ★ Chief Data Officer and dispatches the Analytics Engineer and the Data Analyst by tier; each reproduces the other's load-bearing numbers blind, and the quality skill's ★ Head of Quality verifies on deep runs. The two specialists may run read-only queries and scripts in a run workspace outside any repository. The skill persists its own department's records behind its write-gate, where a change to a governed definition waits for the user's approval and no record ever holds rows about a person. Ships `references/deliverables.md`, `dispatch.md`, `metrics.md` and `evidence.md`, the brief, metric-definition, answer and dashboard templates, and its trigger test.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
