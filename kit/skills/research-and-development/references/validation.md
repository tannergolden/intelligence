# Validation - the build mode's two-gate quality model

Every build the build mode makes passes two gates in parallel, and both must pass. They are complementary: one is objective and never hallucinates a pass; the other judges what rules cannot.

## Gate 1 - the deterministic validator (`scripts/validate.py`)

Deterministic checks belong in code, never an agent: a model is worse than code at counting lines and checking schema. This skill ships its validator in `scripts/`, standard-library Python with no install, so it runs in any repository on any app. It checks what is true of a skill or an agent everywhere. What is true only in one repository, such as a vault's frontmatter schema or tag vocabulary, stays with that repository's own checks, which its `AGENTS.md` names; run them too, because the repository's rules change and a frozen copy would drift.

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
  - the body is at most 500 lines, writes paths with forward slashes, has a `## Boundaries` section, and has a `## Bootstrap` section only in research-and-development;
  - no em dash (U+2014), en dash (U+2013) or horizontal bar (U+2015) in any file;
  - it warns when `allowed-tools` pre-approves a tool that writes or runs commands.
- **Agent**: frontmatter with `title` and `description` and no `name`, since an agent is known by its title alone; a file name equal to the title or to the title's slug; `tools` drawn from `read`, `search`, `edit`, `execute`, `web` and `agent` or the app tool names they map to (a warning for any other); a description that starts "Dispatch this agent" (a warning when it does not); every core section heading (Identity, Role & Objective, Inputs, Method, Output contract, Examples, Boundaries, Recovery, Non-negotiables), counted outside code fences; an Identity block with Persona and Voice (a warning when one is missing) and no Name line; no dashes.
- **Team**: a roster with `title`, `description`, `members` and `lead`; the lead listed in `members` and starred, the only starred member; every member resolving to an agent file in the same folder or another agent home; no dashes.
- **Library**: every agent and roster in every home given, with titles unique across the homes, and no agent carrying a personal name. No two agents anywhere share a role.

A validator error blocks the build. Run it first; it is cheap. In tannergolden/intelligence, `make check` also holds every universal skill to the renderer's own format checks.

## Gate 2 - the independent reviewers (borrowed from the quality-assurance and information-technology skills)

The quality-assurance skill's QA Test Engineer, the information-technology skill's Security Engineer on every build, and the quality-assurance skill's Design Critic on a build with a user-facing interface: fresh-context reviewers who never touch the build (none holds an edit tool; the validator's and the tests' output reaches them as evidence) and review what they did not write, so a reviewer structurally cannot fix-and-rubber-stamp. They are borrowed by title, never members of the R&D team, and briefed per `orchestration.md`. They judge what code cannot: clarity, completeness, spec conformance, whether the description would actually trigger, whether the method is coherent. An author anchored to its own context declares work ready that a fresh instance flags as flawed, and same-context self-critique can score worse than none. Never "now check your own work"; always a separate invocation. Withhold the builder's notes from them, so they do not inherit the builder's blind spots.

## Tiered heavy tests (not every build)

- **Trigger smoke test** - the ~20-query description test in `references/descriptions.md`. Reserve for Publish or the complex tier.
- **Test-drive** - run the built skill against verifiable assertions, with-skill versus baseline, to confirm it actually works, not just that it triggers. If the skill does not beat no skill, it is not done. Publish or complex tier.

## The fix loop

Validator errors or a reviewer's NEEDS-FIX, FAIL, HOLD or block resume the builder on the cited issues only. Re-run the validator always; re-audit only the cited items with a fresh reviewer. If the same error survives two rounds, stop and surface a likely requirement-level conflict.
