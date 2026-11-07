# research-and-development Changelog

## Current Version

**`2.0.2`**

The version is SemVer, per standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver). It matches `metadata.version` in `SKILL.md`, and this skill's validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: its modes and tiers, the team and the seats it borrows, the dispatch wiring, references, templates, scripts, and the output and freshness contract. Not below-PATCH tweaks.
- **Bump** the version by standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver), and update the Current Version line with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured modes or tiers, incompatible output. Most recent 4 entries.

### `2.0.0` - 2026-11-07

The research skill is renamed research-and-development, the Research & Development (R&D) department, one of the twelve department skills (ADR-0039), and it covers the user's own life as well as a company's: researching anything, learning plans, ideas for anything, side projects, and building tools, skills and software. It absorbs two skills whole, each as a mode, with every mode and method kept: **discover** (1.2.1) becomes the **ideas** mode (frame a how-might-we, generate wide from distinct lenses, converge by a fair pairwise Elo tournament, the kill-gate; its references `brief.md`, `convergence.md`, `lenses.md` and `method.md`, its dispatch as `references/ideas-dispatch.md`, and its templates `generative-brief.md` and `idea-record.md`), and **develop** (5.0.1) becomes the **build** mode (decide whether a need is a skill at all, research, reuse before create, the Create, Update, Recursive and Publish sub-modes, the two gates, self-improvement from regression cases, and the `## Bootstrap` section, which the validator now reserves for this skill's name; its `scripts/validate.py` and `scripts/package.py`, unchanged in logic, its references, its templates and `assets/golden-set.md`). Research's own method is the **research** mode, its dispatch now `references/research-dispatch.md`.

- **The team** is Research & Development (R&D), five seats with one lead, in develop's roster format. The **★ Head of Research & Development** merges the Research Lead, the Creative Lead and the Engineering Lead, and runs the Tournament Ranker's pairwise tournament as its own method; each mode's stance and method is in `references/lead-research.md`, `references/lead-ideas.md` and `references/lead-build.md`. The **All-Source Analyst** absorbs the Information Specialist (the search strategy and its PRESS self-check, as a strategy pass). The **Idea Generator** absorbs the Idea Curator (dedup against the whole pool, killed ideas included, and the idea records, as a curation pass). The **Full-Stack Engineer** absorbs the Software Architect: it designs before it builds; its file is `agents/Full-Stack Engineer.md`, titled to match. The **UX and Design Research Lead**, from identify, is an unstarred member again: user and customer research for products, a build's design intent, and the interviewer the human-resources skill's profile interview borrows.
- **Borrowed seats, not members:** the quality-assurance skill's Fact-Checker and Devil's Advocate (the research mode's blind round; the Devil's Advocate also the ideas mode's critique, absorbing the Idea Critic), QA Test Engineer (absorbing develop's QA Engineer) and Design Critic; the information-technology skill's Security Engineer (absorbing the Application Security Engineer); and by demand the legal-and-compliance skill's Compliance Officer (the standards gate, absorbing the Standards Reviewer), the administration skill's Chief Operating Officer (the portfolio weighing, absorbing the Portfolio Manager) and the public-relations skill's Editor (a report's polish, in place of the editorial skill).
- **Moved to their owners:** `templates/verification.md` and `templates/critique.md` are now the quality-assurance skill's `templates/fact-check-ledger.md` and `templates/critique-ledger.md`. `assets/distractor-descriptions.json`, which nothing read, is gone.
- **Assets:** `assets/trigger-evals.json` merges research's, discover's and develop's should-trigger cases and near misses with the user's own life; `assets/regression-cases.jsonl` carries research's and develop's frozen cases, their ids prefixed by mode (`research-rc-001`, `build-rc-0001`).

---

## Minor Updates

> New tier behavior, new references, new by-demand seats. Most recent 4 entries.

### `1.8.0` - 2026-11-07

The Research team is trimmed to its six most critical agents: the Research Lead, Information Specialist, All-Source Analyst, Fact-Checker, Devil's Advocate, and Standards Reviewer. Five seats are retired and their duties folded into survivors. The Fact-Checker now also reviews load-bearing quantitative claims (sample, method, effect size, base rates) when numbers carry the conclusion, and `templates/verification.md` gains the number ledger. The Research Lead owns the Step-0 dedup, reuse-is-review and freshness check, approves the search strategy before a deep fan-out, and gives a shipping report its final polish without altering meaning (or hands the prose polish to the editorial skill). The Information Specialist self-checks its strategy PRESS-style (a sentinel check), folded into `templates/source-strategy.md`. One All-Source Analyst lane grounds the question in a named reference collection or offline knowledge base before the web; cataloging and weeding a collection is no longer the team's job. `templates/statistical-review.md` and `templates/search-audit.md` are deleted.

### `1.7.0` - 2026-11-07

The hub now owns and authors the skill, made universal: the hand-over rule to a vault's own copy is gone. A report is returned in chat and filed only where the repository's instructions say reports go (with their index, if they keep one) or where the user names; the Knowledge Manager's Step-0 runs against whatever reports those instructions point to. The Librarian (`agents/Librarian.md`, read-only tools) joins the Research team as a seat dispatched only when the repository names a reference collection or offline knowledge base, cataloging and weeding only under the rules it defines. The roster is in develop's format, every spec carries `title:` and is known by it alone (spoken names dropped), and the namesake `Research.md` is folded into the roster and `references/methodology.md` and deleted.

### `1.6.0` - 2026-10-26

The Research team now ships inside the skill, in `agents/`, instead of living in a faculty folder of the knowledge vault, and the skill source moved from the vault's unpackaged skills folder to `.agents/skills/`, where the agent apps read a repository's skills, so the vault's own sessions finally load it and tannergolden/intelligence's home kit can carry it to every repository. Briefs read each spec from `<skill>/agents/`. A new **Where it runs** rule: in a vault, the vault's own copy runs, so a home copy hands over to it; anywhere else the run skips the Step-0 dedup and the Librarian and delivers in chat. `allowed-tools` now pre-approves read-only tools only, and the frontmatter keeps one key to a line, as the home kit's reader requires.

### `1.5.0` - 2026-06-28

Added the knowledge-base read step to local grounding and tightened the knowledge-base doctrine. The vault's command gained a `kb read "article"` subcommand (full article text by title or path, with a citation line) and now rejects unknown flags on `kb search`; the grounding step and the Librarian use `kb search` to find an article then `kb read` to fetch and read its body, so a knowledge-base finding is fetched and read, not snippet-guessed. `references/methodology.md` adds: single-source grounding downgrades confidence and corroborates; the web-escalation triggers (current events, post-snapshot facts, primary research, non-English, specialized depth); and intra-source contradictions are surfaced like cross-source ones. Output gains a learn-loop: when grounding finds no curated library note on a durable topic, offer to promote the synthesis for the Librarian to catalog.

---

## Patch Updates

> Fixes, wording, reference tweaks. Most recent 4 entries.

### `2.0.2` - 2026-11-07

- In the profile interview, the UX and Design Research Lead hands its ledger to the public-relations skill's Editor, which now composes the proposal batch in place of that skill's retired Writer, and the blind reviewer never sees the Editor's brief (`agents/UX and Design Research Lead.md`). `references/architecture.md` says there is no standalone subagent: every agent belongs to a department's team.

### `2.0.1` - 2026-11-07

- `references/architecture.md` says a team, and a skill's own `agents/`, holds at most five agents, its lead included, so a build keeps a team to its most critical seats.

### `1.8.1` - 2026-11-07

A repository with no agent instructions now explains itself in its `README.md` files: the skill reads the root one and the one in each folder it writes into.

### `1.5.3` - 2026-10-19

- A report's three-month window ends on its `review_by` date, since the hidden frontmatter retired `updated` (`references/reporting.md`, `templates/report.md`).

