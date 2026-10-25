# Golden set - the acceptance gate

Develop judges its own builds through reviewers it dispatches, so before its output is trusted, especially the independent review it gates with (the QA Engineer and, where security-relevant, the Application Security Engineer), it is checked against this golden set with a person as the fresh reviewer. This is the bootstrap's safety net: it breaks the circularity of a factory authoring its own quality lever. Run it again after any change to develop's pipeline, its team or its validator.

## How to run the gate

1. Have develop produce each artifact below from a cold prompt.
2. Run `python3 scripts/validate.py` on it. The known-good must pass; each known-bad must fail on the stated check.
3. Read the output yourself as the independent reviewer. Confirm the fresh reviewers it dispatches, the QA Engineer and, where security-relevant, the Application Security Engineer, would actually catch the known-bad cases.
4. Only after all rows pass do you trust develop to build unattended.

## Known-good (must validate clean)

| Artifact            | What good looks like                                                                                                                                                                                                             |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A single-file agent | Header with `title`, `name`, a routing `description` and least-privilege `tools`; a file name equal to the title's slug; all nine core sections; composable add-ons only where triggered; a Non-negotiables bracket; no em dash. |
| A team roster       | `members` and `lead` in frontmatter, the lead listed in members and starred, the only star; a dispatch order.                                                                                                                    |
| A skill             | All required files and folders; `name` = directory; `metadata.version` = the Changelog's Current Version; a description with "Use when", 4 to 6 concrete trigger phrases and an anti-undertrigger clause.                        |

## Known-bad (must be caught)

| Defect                                                             | Caught by                                             |
| ------------------------------------------------------------------ | ----------------------------------------------------- |
| Agent missing its Method section                                   | validator (missing required section)                  |
| Agent file name not the slug of its title                          | validator (identity mismatch)                         |
| Skill `metadata.version` ahead of the Changelog                    | validator (version mismatch)                          |
| Roster lead not in the members list                                | validator (lead not in roster)                        |
| A second `SKILL.md` inside `templates/`                            | validator (one SKILL.md per skill)                    |
| An em dash anywhere                                                | validator (no-dash rule)                              |
| A passive description ("helps with skills") that would not trigger | QA Engineer (judgment; the validator cannot see this) |
| A decorative persona backstory padding an agent                    | QA Engineer (spec conformance; cut the persona)       |

The last two rows are the point of the human gate: they are exactly what a factory might get wrong in the review it relies on, and only a fresh human reviewer can confirm develop caught them.
