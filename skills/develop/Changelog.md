# develop Changelog

## Current Version

**`04.00.00`**

Semantic versioning, `MAJOR.MINOR.PATCH`, two-digit zero-padded segments. This value matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how develop works: modes, the team, references, templates, scripts, the output contract. Not below-PATCH tweaks.
- **Bump** PATCH for a fix, MINOR for a backward-compatible addition, MAJOR for a breaking change. Update the Current Version line and `metadata.version` with every entry.
- **4-entry cap** per section; a fifth drops the oldest, which the repository's history keeps.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `04.00.00` - 2026-10-19

Develop became the one universal skill. tannergolden/intelligence ships it in `skills/develop/`, and the home kit installs it into every coding app in place of building-skills, whose decision table, placement rules and cross-app format it now carries. It works in any repository: the same modes, the same Create pipeline, the same Development team and the same two gates, with nothing it needs outside its own folder.

- The Development team ships inside the skill, in `agents/`, the published form develop already described: a roster and five agents with portable frontmatter and capability names every app maps.
- Gate 1 is `scripts/validate.py`, bundled and standard-library only, checking skills, agents, teams and agent libraries against the format every app accepts. A repository's own rules stay with its own checks, which develop runs beside it.
- `scripts/package.py` builds a `.skill` archive that vendors the team from its agent home, byte-identical on every rebuild.
- Skills live by tier: a universal skill in the hub, a repository's in `.agents/skills/` and `.claude/skills/`, the Claude app's as an archive.
- The frontmatter keeps one line per key, `metadata` as a one-line map; the description says when to use it with "Use when"; the skill templates sit one level down; `allowed-tools` pre-approves read-only tools at most.
- The licence is MIT.

Earlier versions, `01.00.00` to `03.06.02`, were built inside the knowledge vault, and their history is in that repository's git log.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

_None yet._

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

_None yet._
