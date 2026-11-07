# research Changelog

## Current Version

**`1.8.1`**

The version is SemVer, per standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver). It matches `metadata.version` in `SKILL.md`, and develop's validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how research works: tiers, the dispatch wiring, references, templates, the output and freshness contract. Not below-PATCH tweaks.
- **Bump** the version by standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver), and update the Current Version line with every entry.
- **4-entry cap** per section; a fifth drops the oldest.

---

## Major Updates

> Breaking changes, restructured tiers, incompatible output. Most recent 4 entries.

_None yet._

---

## Minor Updates

> New tier behavior, new references, new by-demand seats. Most recent 4 entries.

### `1.8.0` - 2026-11-07

The Research team is trimmed to its six most critical agents: the Research Lead, Information Specialist, All-Source Analyst, Fact-Checker, Devil's Advocate, and Standards Reviewer. Five seats are retired and their duties folded into survivors. The Fact-Checker now also reviews load-bearing quantitative claims (sample, method, effect size, base rates) when numbers carry the conclusion, and `templates/verification.md` gains the number ledger. The Research Lead owns the Step-0 dedup, reuse-is-review and freshness check, approves the search strategy before a deep fan-out, and gives a shipping report its final polish without altering meaning (or hands the prose polish to the editorial skill). The Information Specialist self-checks its strategy PRESS-style (a sentinel check), folded into `templates/source-strategy.md`. One All-Source Analyst lane grounds the question in a named reference collection or offline knowledge base before the web; cataloging and weeding a collection is no longer the team's job. `templates/statistical-review.md` and `templates/search-audit.md` are deleted.

### `1.7.0` - 2026-11-07

The hub now owns and authors the skill, made universal: the hand-over rule to a vault's own copy is gone. A report is returned in chat and filed only where the repository's instructions say reports go (with their index, if they keep one) or where the user names; the Knowledge Manager's Step-0 runs against whatever reports those instructions point to. The Librarian (`agents/Librarian.md`, read-only tools) joins the Research team as a seat dispatched only when the repository names a reference collection or offline knowledge base, cataloging and weeding only under the rules it defines. The roster is in develop's format, every spec carries `title:` and is known by it alone (spoken names dropped), and the namesake `Research.md` is folded into the roster and `references/methodology.md` and deleted.

### `1.6.0` - 2026-10-26

The Research team now ships inside the skill, in `agents/`, instead of living in `Inbox/Faculties/Research/`, and the skill source moved from `System/Skills/.unpackaged/` to `.agents/skills/`, where the agent apps read a repository's skills, so the vault's own sessions finally load it and tannergolden/intelligence's home kit can carry it to every repository. Briefs read each spec from `<skill>/agents/`. A new **Where it runs** rule: in a vault, the vault's own copy runs, so a home copy hands over to it; anywhere else the run skips the Step-0 dedup and the Librarian and delivers in chat. `allowed-tools` now pre-approves read-only tools only, and the frontmatter keeps one key to a line, as the home kit's reader requires.

### `1.5.0` - 2026-06-28

Added the `kb read` step to local grounding and tightened the knowledge-base doctrine. `brain.command` gained a `kb read "article"` command (full article text by title or path, with a citation line) and now rejects unknown flags on `kb search`; the grounding step and the Librarian use `kb search` to find an article then `kb read` to fetch and read its body, so a knowledge-base finding is fetched and read, not snippet-guessed. `references/methodology.md` adds: single-source grounding downgrades confidence and corroborates; the web-escalation triggers (current events, post-snapshot facts, primary research, non-English, specialized depth); and intra-source contradictions are surfaced like cross-source ones. Output gains a learn-loop: when grounding finds no curated `Library/` note on a durable topic, offer to promote the synthesis for the Librarian to catalog.

---

## Patch Updates

> Fixes, wording, reference tweaks. Most recent 4 entries.

### `1.8.1` - 2026-11-07

A repository with no agent instructions now explains itself in its `README.md` files: the skill reads the root one and the one in each folder it writes into.

### `1.5.3` - 2026-10-19

- A report's three-month window ends on its `review_by` date, since the hidden frontmatter retired `updated` (`references/reporting.md`, `templates/report.md`).

### `1.5.2` - 2026-10-19

- References point at `AGENTS.md` (Start here holds the retrieval order) and the folder notes' Rules instead of the retired root rule files.
- The licence is MIT, and the versioning rules link to tannergolden/standards instead of restating them.
- Versions are plain SemVer: `01.05.01` is now `1.5.1`.

### `1.5.1` - 2026-10-19

Moved local grounding and the preflight off the retired engine: the offline knowledge bases are searched with `.github/scripts/knowledge-base.py` when one is installed, a report overwrite starts from a committed state, and `update-vault.py` and `check-vault.py` replace `sync` and `health`. The archive now carries the Research team, vendored when it is built.

