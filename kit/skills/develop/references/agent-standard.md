# Agent standard - one file per agent

The settled standard for an agent spec. Template: `templates/agent.md`. The validator enforces the header and the core sections.

## Header (YAML)

An agent file opens with `---` frontmatter holding four fields. A repository that keeps agents of its own may require more (a knowledge vault's frontmatter schema, for example); add them where its rules say, and keep these four.

- `title` - the role, in Title Case with spaces (for example `Software Architect`), unique across every agent home. A team **lead** carries a `★ ` prefix on its `title` (`★ Engineering Lead`), which marks the lead in rosters and catalogs. The file name is the title's slug: lowercase, hyphens for spaces, the star dropped (`engineering-lead.md`).
- `name` - the agent's spoken name, a unique first name, the addressing handle ("Hey Sloane"). Unique across every agent home, case-insensitively. The role (`title`) and the spoken name (`name`) are two separate uniqueness axes; the validator enforces both.
- `description` - the routing key. Write it as "Dispatch this agent when ..." or "Dispatch this agent to ..." so an orchestrator can route from this line alone.
- `tools` - the agent's capabilities, comma-separated, from the names every app maps: `read`, `search`, `edit`, `execute`, `web`, `agent`. Least privilege: a reviewer never holds `edit`, and only a lead holds `agent`.

## Core body, in order (all required)

0. **Identity** - the very top bracket. A tight card, not a biography: `Name` (the spoken first name), `Persona` (one line, the professional character, no competence or expertise claim), `Voice` (one line, how it sounds), and a `Global rules` pointer to the team roster, where the team-wide conventions live, stated once rather than repeated per agent. This is the talk-to-them-directly layer; it shapes voice and disposition only; it never restates Method and never claims expertise.
1. **Role & Objective** - top bracket. Who it is, the one job, the success test, the isolated-subagent framing.
2. **Inputs** - what it reads every run; what is conditional; what to assume; what to flag and stop on.
3. **Method** - numbered steps, each with its decision rule. Decision criteria hardest-first.
4. **Output contract** - the exact artifact shape. Reason first, emit the formatted result last.
5. **Examples** - the one load-bearing hard case, input to output.
6. **Boundaries** - scope, the forbidden actions, the write-scope.
7. **Recovery** - missing input, ambiguous case, cannot-complete failure shape.
8. **Non-negotiables** - bottom bracket. 2 to 4 lines restating only the hardest constraints and the one output essential. The deliberate exception to "say each thing once"; recency protects it.

## Composable add-ons (include any whose trigger applies, delete the rest)

- **Voice & Style** - when the agent ships prose a human reads. Example-driven (before to after).
- **Stance** - when the agent holds a deliberate disposition, especially as one of several seats that must diverge. Carry a calibrated 1-to-3 scale and a standing question.
- **Coordination** - when the agent is the team lead. Dispatch order, conflict rule, ship gate.

## Detail discipline

- **Carry an Identity, cut the biography.** Every agent carries the tight Identity block above: a unique name, a one-line persona, a one-line voice. It is not a backstory: no invented history, hobbies, or life story. The persona is one line that sharpens disposition and voice, never a paragraph of color, never a competence claim, never a substitute for Method. (Decorative backstory adds nothing to task quality, Zheng et al., EMNLP 2024; a thin identity for addressing and voice is the deliberate, bounded exception, because the addressing layer never enters the reasoning path.)
- **Comprehensive by coverage, not volume.** Generalizable right-altitude heuristics plus one canonical example beat enumerating every case. State each fact once; cut padding, keep all method.
- **Deepen the decision kernel, not every section.** Where an agent makes a load-bearing judgment, give each Method step its decision rule and state the role's framework once, and give Examples a contrasting decide-versus-escalate pair: those buy decision consistency. Leave Identity, Recovery, and Non-negotiables lean. Govern by instruction count and signal density, not length (a spec past ~150 lines is a smell; over-trimming costs only 1 to 2 points, so cut filler freely but never method). Deepen a section on an observed failure, not on spec: length for its own sake degrades performance (lost-in-the-middle, instruction overload).
- **Bracket the spec.** Most critical framing at the top (Role), hardest reminders at the bottom (Non-negotiables). At spec lengths a single file is not in the lost-in-the-middle zone; the two brackets are the cheap insurance that scales if it grows.
- **No em dashes.** Anywhere. The validator fails on the character unless the repository allows it.
