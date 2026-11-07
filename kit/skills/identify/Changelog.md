# identify Changelog

## Current Version

**`1.2.0`**

The version is SemVer, per standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver). It matches `metadata.version` in `SKILL.md`, and the validator fails when they differ. Each section shows the 4 most recent entries; older entries age out. Newest on top.

---

## How This File Works

- **Tracks** changes to how the skill works: modes, the crew, references, templates, the output contract. Not below-PATCH tweaks.
- **Bump** the version by standards' [versioning policy](https://github.com/tannergolden/standards/blob/Development/docs/distribution/Releases-&-Versioning.md#-versioning-policy-semver), and update the Current Version line with every entry.
- **4-entry cap** per section; a fifth drops the oldest.

---

## Major Updates

> Breaking changes, restructured pipeline, incompatible output. Most recent 4 entries.

### `1.0.0` - 2026-07-03

Initial build of the identify skill: coverage-driven Profile interviewing. The engine's read-only `profile coverage` subcommand picks the target facet; the skill embodies the UX and Design Research Lead to run a mixed-delivery interview from validated frameworks, dispatches the Writer to compose the provenance-marked proposal batch and the Standards Reviewer to audit it blind against Article IV, and writes only what the user approves, line-item capable, through the engine write path.

## Minor Updates

> Backward-compatible additions. Most recent 4 entries.

### `1.2.0` - 2026-11-07

Identify has its own team, Interview, like every other skill: the ★ UX and Design Research Lead moved here from the dissolved Research & Development department and became its lead and interviewer, rewritten for that job, with the Writer and the Standards Reviewer borrowed from the editorial and research skills.

### `1.1.0` - 2026-11-07

The skill moved to tannergolden/intelligence and works in any repository or none. It reads the repository's instructions first: in a private repository made to hold the user's profile it writes the approved batch where those instructions say and runs the checks they name, and anywhere else it returns the approved profile in the conversation and writes nothing about the user. A named coverage command picks the facet, else the user does; Memory promotions became record offers, the profile rules now live in `references/provenance.md`, the seats are read from the board, editorial and research skills, and the folder note `Identify.md` is gone.

## Patch Updates

> Fixes and clarifications. Most recent 4 entries.

### `1.0.4` - 2026-10-26

- The skill source moved from `System/Skills/.unpackaged/` to `.agents/skills/`, where the agent apps read a repository's skills, with a copy in `.claude/skills/` for Claude Code, so the vault's own sessions load it. The Writer and the Standards Reviewer it borrows now live in the editorial and research skills' `agents/` folders, and `SKILL.md`, the namesake doc and the roster point there. They also say what the archive carries: the R&D department, never the two borrowed seats.
- The description says "Use when", `allowed-tools` pre-approves read-only tools only, and the frontmatter keeps one key to a line.

### `1.0.3` - 2026-10-19

- The provenance marker is described as invisible on GitHub and in any Markdown preview, now that the vault has no Obsidian configuration (`references/provenance.md`).

### `1.0.2` - 2026-10-19

- References point at `AGENTS.md` and the Rules in `Profile/Profile.md` and `Memory/Memory.md` instead of the retired root rule files; the review ledger names those rules in place of article numbers.
- The licence is MIT, and the versioning rules link to tannergolden/standards instead of restating them.
- Versions are plain SemVer: `01.00.01` is now `1.0.1`.

### `1.0.1` - 2026-10-19

Rewired the pipeline to the vault's scripts: `.github/scripts/profile-coverage.py` picks the target facet, a new entry is copied from its `Profile/.template/` file, Memory promotions are written in their destination's format, and `update-vault.py` and `lint-notes.py` close every run. The archive now carries its team, vendored when it is built.

