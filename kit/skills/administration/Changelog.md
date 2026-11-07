# administration Changelog

## Current Version

**`4.0.1`**

The version is SemVer, per standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver). It matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: tiers, the team, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** the version by standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver), and update the Current Version line with every entry.
- **4-entry cap** per section; a fifth drops the oldest.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `4.0.0` - 2026-11-07

The skill is renamed from `board` to `administration` (its folder, its `name` and every mention), and the workforce is exactly twelve departments, each one skill named for it, each team at most five agents so the Chief of Staff can join every department's group of six. Administration is now the executive office of a company the user runs and of the Founder's own life: goals, priorities, decisions, calendar and commitments, and life strategy. The department skills it convenes are renamed: `finance` to `finance-and-accounting` (its team Finance to Finance & Accounting (F&A), its Financial Planning Lead to ★ Chief Financial Officer), `legal` to `legal-and-compliance`, `sales` to `sales-and-marketing` (Sales & Revenue (S&R) to Sales & Marketing (S&M), its Product Marketing Manager and Demand Generation Manager merged into the Marketing Manager), `operations` to `operations-and-logistics`, `people` to `human-resources`, `systems` to `information-technology`, `analytics` to `business-intelligence`, `quality` to `quality-assurance`, `customers` to `customer-experience` (Client Experience (CX) to Customer Experience (CX)) and `communications` to `public-relations`; `research`, `discover` and `develop` merge into `research-and-development` (the Research Lead, Creative Lead and Engineering Lead into its ★ Head of Research & Development), `editorial` into `public-relations`, `visualize` into `business-intelligence` and `identify` into `human-resources`. The Chief Operating Officer absorbs discover's Portfolio Manager: a RICE-scored, balanced allocation of capital, time and attention across ventures and projects, the Founder's personal ones included, recommended for the CEO or the Founder to decide. The Chief of Staff first confirms whether GitHub is connected for the work and which repository holds the Founder's PKM (their knowledge vault, made from the tannergolden/knowledge template), asking for either it does not know; forms a temporary working group of only the seats a job needs and closes it when the job is done; tracks the Founder's calendar and commitments; and keeps its write exception for the Founder's knowledge repository, where its `AGENTS.md` and the README files it names say. Decide and strategize serve personal decisions too (a move, a job offer, a big purchase; the Founder's goals and life strategy), with the Founder as the decider and every gate kept; review gains the Founder's weekly review, operate a personal project that crosses departments. `references/workforce.md` holds the twelve departments (51 agents, at most five a team) with each one's personal scope and the personal context rule; `references/routing.md` maps every deliverable family, a company's and the Founder's, to its department skill, research, ideas and building to research-and-development, writing to public-relations, visuals to business-intelligence, the profile and wellbeing to human-resources, verification to quality-assurance; the product roadmap moves from `Administration/Roadmap.md` to the research-and-development skill's records (`Research & Development (R&D)/Roadmap.md` where a venture keeps department folders), kept by its ★ Head of Research & Development, while the product calls stay the CEO's, recorded in `Administration/Decisions.md`; the decide run's dissent role is the quality-assurance skill's Devil's Advocate, and verification names that team's seats (the Plan Reviewer's check is now its Fact-Checker's). `templates/board-brief.md` becomes `templates/decision-brief.md`; `references/frameworks.md` gains the tools for a life choice, `references/strategy-toolkit.md` the Founder's life strategy and the portfolio method, `references/operating-cadence.md` the Founder's own cadence; the write-gate and `assets/delegation-of-authority.json` gate the Founder's calendar, an offer's acceptance and a lease, and name the Founder the decider of every personal call. The description and the trigger tests cover company and personal use and route near misses to the renamed department skills.

### `3.0.0` - 2026-11-07

The company's departments are now their own skills, and board is the orchestrator that convenes them. Board's own team is Administration (★ Chief Executive Officer, Chief Operating Officer, Corporate Secretary, Chief of Staff), the only roster left in its `agents/`; `legal`, `sales`, `operations`, `people`, `systems`, `analytics`, `quality`, `customers` and `communications` each carry their department's roster, agents and deliverables. Board convenes a department by dispatching its lead from that skill's `agents/`, or by handing the skill a whole department deliverable; within a board run board persists the results, and a department skill called on its own persists its own department's records. Three departments are removed: Finance & Accounting (a company's money is the `finance` skill's, whose ★ Financial Planning Lead is the company's finance function), Research & Development and Product Technology (evidence about users and markets is `research`'s, options are `discover`'s, technical direction and building are `develop`'s ★ Engineering Lead's, and the product decision is the CEO's, recorded in `Administration/Roadmap.md`). Information Security merges into the `systems` skill, whose IT team holds the Chief Information Security Officer. The quality skill's ★ Head of Quality stays the independent verifier. `references/department-deliverable-catalog.md` becomes `references/routing.md`, a map of each deliverable family to the skill that owns it, its lead and its cross-department dependencies, with Administration's own deliverables kept in full; `references/specialist-dispatch.md` is rebuilt around a legal worked example and the hand-off to a department skill; `references/workforce.md` is the company's organization: the department table (41 agents in 11 teams with finance's), the company-wide rules each roster restates, the Chief of Staff's relay, and the committees, with the Compensation Committee under the people skill's CHRO and the security residuals under the systems skill's CISO. Every reference, template and asset names the department skills in place of the removed seats. The description routes a single department's work to its skill, the trigger tests gain near misses for the department skills, and `metadata` drops `id`.

### `2.0.0` - 2026-06-29

Rebuilt board from a decision-only skill into the knowledge vault's venture operating system: five modes (found, strategize, decide, operate, review) over the expanded Agent Resources (AR) Fortune 500 workforce, scaled to the venture's stage. The decision engine is preserved as the decide mode. New: a venture-context preflight (read Overview/Goals/Strategy/Log, detect the stage) and write-back into the venture folder; the sole-writer model (no AR agent holds Write/Edit; the skill persists, behind a write-gate that gates money, contracts, external comms, deletes, and equity to the Founder); specialist dispatch (a lead frames, specialists produce) and the Head of Quality as the independent verifier of consequential output. Added ten references (modes-router, lifecycle, founding-playbook, strategy-toolkit, metrics-and-kpis, operating-cadence, write-gate, verification, specialist-dispatch, department-deliverable-catalog), six templates (founding-checklist, okr-cycle, deliverable-contract, venture-scorecard, qbr-sixpager, venture-health-check), and three assets (expanded trigger-evals, delegation-of-authority, stage-machine). Built alongside the AR expansion (90 agents, 18 departments, board and committees) and the venture template upgrade (an Administration strategic core, a financial model, and a cap table). Grounded in a deep research and audit pass on Fortune 500 structure, function deliverables, the company lifecycle, the operating model, strategy frameworks, metrics, venture creation, governance, and AI-operating-system guardrails.

### `1.0.0` - 2026-06-29

Initial build of the board skill: the knowledge vault's decision skill, convening the Agent Resources (AR) corporate workforce as a board (the CEO chairs from Administration, the department leads give independent functional views, a dissent pass beats groupthink, and the chair synthesizes by RAPID to one recommendation with one accountable owner), to the standard every angle heard, one owner accountable. It decides and names the owner; irreversible or major calls escalate to the Founder. Replaces the archived company skill. Grounded in a research pass on executive deliberation (the chair's role and governance basics, the multi-perspective decision-framework toolkit, orchestrating functional heads without groupthink or the highest-paid opinion, and the board-style decision-memo format).

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

### `2.3.0` - 2026-11-07

Added the Chief of Staff to Administration: the connective office that sits with every department, relays between them, tracks each commitment to done, and keeps the Founder's knowledge repository current behind the write-gate. When the workforce runs as standing agents, one group per department with the Chief of Staff in each, it holds the pen no skill holds there. The commitment tracking the COO had absorbed returns to it.

### `2.2.0` - 2026-11-07

Board is universal: a venture is a company the user runs, kept wherever the repository's instructions say (a venture folder, a repository of its own, or the conversation), founded from the repository's template or this skill's `templates/`, with the repository's own checks run after a write in place of fixed check scripts. The workforce is now the skill's own team in `agents/` (14 department rosters in develop's roster format, 43 agents with `title:`, at most 6 per department including the lead), its rules, hierarchy, committees, scaling, and department table in `references/workforce.md`; `Board.md` is folded in and deleted.

### `2.1.0` - 2026-07-02

Aligned the skill to the 2026-07-02 workforce lean build. Four AR departments dissolved (Sales & Marketing, Strategy & Corporate Development, Enterprise Risk, Internal Audit): the marketing seats (Product Marketing Manager, Demand Generation Manager) moved under the Chief Revenue Officer in Sales & Revenue and every CMO reference repointed there; strategy framing absorbed by the CEO (options, reversibility flags, recommend-not-decide) and every CSO reference repointed; the Risk/Audit scorecard row and lifecycle committee layer re-mechanized onto the write-gate, health, changelog, and backups, with the CISO holding security residuals. Retired specialist references repointed to their named survivors, the five nonexistent "Head of" titles corrected to the real chief titles, the crisis-communications plan reassigned to its actual producer, and the functional-lead count fixed. Venture-folder paths (the Sales & Marketing (S&M)/ files) are unchanged.

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

### `4.0.1` - 2026-11-07

- A temporary working group holds at most five seats and the Chief of Staff, so it fits a Grok Bot group of six; a job that needs more seats is split into parts, a group for each (`agents/Chief of Staff.md`, `references/workforce.md`).

### `2.1.5` - 2026-10-26

- The skill source moved from the vault's unpackaged skills folder to `.agents/skills/`, where the agent apps read a repository's skills, with a copy in `.claude/skills/` for Claude Code, so the vault's own sessions load it.
- The description is quoted and says "Use when": unquoted, its colon made the frontmatter invalid YAML, so a loader dropped the description and the skill could never trigger.
- `allowed-tools` pre-approves read-only tools only, and the frontmatter keeps one key to a line.

### `2.1.4` - 2026-10-22

- The description routes the Founder's personal and household money to the new `finance` skill ("personal money is finance"), so a personal "should I" no longer competes with a business one, and Boundaries says where the two meet. "Fortune 500" left the description to keep it under the 1,024-character limit; the body is unchanged.
- Two near-miss trigger tests route personal money questions to `finance`.

### `2.1.3` - 2026-10-19

- Founding gives each copied venture file its real `title`, `description` and `type`, the vault's hidden frontmatter, in place of rewriting the retired `id` and `path` (`SKILL.md`, `references/modes-router.md`, `references/write-gate.md`).
- The callouts in `references/metrics-and-kpis.md` and `templates/qbr-sixpager.md` are GitHub alerts.

