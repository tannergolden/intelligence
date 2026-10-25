# Validation - the two-gate quality model

Every build passes two gates in parallel, and both must pass. They are complementary: one is objective and never hallucinates a pass; the other judges what rules cannot.

## Gate 1 - the deterministic validator (`scripts/validate.py`)

Deterministic checks belong in code, never an agent: a model is worse than code at counting lines and checking schema. Develop ships its validator in `scripts/`, standard-library Python with no install, so it runs in any repository on any app. It checks what is true of a skill or an agent everywhere. What is true only in one repository, such as a vault's frontmatter schema or tag vocabulary, stays with that repository's own checks, which its `AGENTS.md` names; run them too, because the repository's rules change and a frozen copy would drift.

```bash
python3 scripts/validate.py skill <skill folder> [--agents <agent home>]...
python3 scripts/validate.py agent <agent file>
python3 scripts/validate.py team <roster file>
python3 scripts/validate.py library <agent home>...
```

Add `--json` for structured output, and `--allow-em-dash` in a repository whose rules allow the character. It exits 1 on any error and prints what to fix; warnings do not fail it.

- **Skill**:
  - `SKILL.md` exists at the skill root and is the only `SKILL.md` in the tree (a template manifest is named `t-SKILL.md`);
  - its frontmatter opens on the first line and holds only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`, the keys every app accepts;
  - `name` is kebab-case, at most 64 characters, equal to the folder name, free of "claude" and "anthropic", and not a reserved name;
  - `description` is at most 1,024 characters, holds no angle brackets, and says when to use the skill with "Use when";
  - `license` is set, and `metadata` carries a `version` that equals the Changelog's Current Version;
  - `metadata.team`, when present, resolves to a staffed roster in the skill's own `agents/` or in an agent home given with `--agents`;
  - `License.txt` and `Changelog.md` exist, and `assets/`, `references/` and `templates/` exist (a warning when one is missing);
  - every file sits at most one folder below `SKILL.md`, and every file is text (a warning for a binary);
  - the body is at most 500 lines, writes paths with forward slashes, has a `## Boundaries` section, and has a `## Bootstrap` section only in develop;
  - no em dash (U+2014), en dash (U+2013) or horizontal bar (U+2015) in any file;
  - it warns when `allowed-tools` pre-approves a tool that writes or runs commands.
- **Agent**: frontmatter with `title`, `name` and `description`; a file name equal to the title's slug; `tools` drawn from `read`, `search`, `edit`, `execute`, `web` and `agent`; every core section heading (Identity, Role & Objective, Inputs, Method, Output contract, Examples, Boundaries, Recovery, Non-negotiables), counted outside code fences; an Identity block with Name, Persona and Voice (a warning when one is missing); no dashes.
- **Team**: a roster with `title`, `description`, `members` and `lead`; the lead listed in `members` and starred, the only starred member; every member resolving to an agent file in the same folder or another agent home; no dashes.
- **Library**: every agent and roster in every home given, with titles unique across the homes and spoken names unique case-insensitively. No two agents anywhere share a name or a role.

A validator error blocks the build. Run it first; it is cheap. In tannergolden/intelligence, `make check` also holds every universal skill to the renderer's own format checks.

## Gate 2 - the independent reviewers (the QA Engineer and the Application Security Engineer)

The Development team's QA Engineer, joined by the Application Security Engineer where the build is security-relevant: fresh-context reviewers who never touch the build (the QA Engineer runs the validator and tests; neither holds `edit`) and review what they did not write, so a reviewer structurally cannot fix-and-rubber-stamp. They judge what code cannot: clarity, completeness, spec conformance, whether the description would actually trigger, whether the method is coherent. An author anchored to its own context declares work ready that a fresh instance flags as flawed, and same-context self-critique can score worse than none. Never "now check your own work"; always a separate invocation. Withhold the builder's notes from them, so they do not inherit the builder's blind spots.

## Tiered heavy tests (not every build)

- **Trigger smoke test** - the ~20-query description test in `references/descriptions.md`. Reserve for Publish or the complex tier.
- **Test-drive** - run the built skill against verifiable assertions, with-skill versus baseline, to confirm it actually works, not just that it triggers. If the skill does not beat no skill, it is not done. Publish or complex tier.

## The fix loop

Validator errors or a reviewer's NEEDS-FIX verdict resume the builder on the cited issues only. Re-run the validator always; re-audit only the cited items with a fresh reviewer. If the same error survives two rounds, stop and surface a likely requirement-level conflict.
