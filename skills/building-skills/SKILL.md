---
name: building-skills
description: Builds a new Agent Skill, or repairs one that misfires, so it loads in every coding app tannergolden uses. Decides first whether the need is a skill at all or belongs in a rule, a hook or a script; writes SKILL.md with a description that triggers; adds trigger and quality tests; and puts it where the home kit or a repository delivers it. Use when the user asks to create, write, add, package, fix or improve a skill, a slash command or a reusable procedure, or says an agent keeps getting the same multi-step task wrong, even if they never say "skill".
---

# Building skills

A skill is a folder an agent opens only when its description matches the
task in front of it. Build one only for a procedure; anything that must hold
every session goes somewhere that always loads.

## 1. Decide what it is

| The need                                        | Where it goes                                                              |
| :---------------------------------------------- | :------------------------------------------------------------------------- |
| A multi-step procedure an agent runs on request | A skill                                                                    |
| Behaviour that must hold in every session       | A rule: `law/` in tannergolden/intelligence, or a repository's `AGENTS.md` |
| Something that must never happen                | A hook or a CI check; prose alone is not enough                            |
| A deterministic transformation                  | A script, bundled in the skill that uses it                                |
| A fact about the setup, not an instruction      | The knowledge facts in tannergolden/intelligence                           |

In one published evaluation the skill was never invoked in 56% of cases, so
never put an Invariant in a skill. If the user asked for a skill and the need
is really a rule or a hook, say so and propose that instead.

## 2. Decide where it lives

- **Every repository, every app:** `skills/<name>/` in
  tannergolden/intelligence. The next release carries it, and the home kit
  copies it into `~/.agents/skills/`, `~/.claude/skills/` and
  `~/.gemini/antigravity-cli/skills/`. Never copy it into a home folder by
  hand: the kit replaces folders it owns and refuses ones it does not.
- **One repository:** `.agents/skills/<name>/` for Codex, Copilot, Cursor,
  Gemini and Antigravity, and the same folder at `.claude/skills/<name>/`,
  because Claude Code reads nothing under `.agents/`. Commit both copies.

## 3. Write it from real work

1. Start from a task an agent actually did or got wrong. Capture the steps
   that worked, the corrections it needed, and its exact inputs and outputs.
2. Cut every line the agent would get right without being told. The body
   stays loaded for the rest of the session, so each line costs every turn.
3. Give one default, not a menu. Match freedom to fragility: prose where
   several approaches work, an exact command where one mistake breaks things.
4. Write standing instructions ("run the tests after every edit"), and put
   the most important ones first: after compaction only the opening 5,000
   tokens survive.
5. Keep a "Gotchas" section in `SKILL.md` itself, where the agent will see it.

## 4. Follow the format every app accepts

- **Name:** the folder's name exactly, matching `^[a-z0-9]+(-[a-z0-9]+)*$`, at
  most 64 characters, a gerund such as `processing-pdfs`. Never `claude` or
  `anthropic` in it, and never the folder names `synced` or
  `anthropic-skills`.
- **Frontmatter:** `---` on the very first line, because loaders read
  frontmatter nowhere else, and only these keys: `name`, `description`,
  `license`, `compatibility`, `metadata`, `allowed-tools`. Any other key is
  rejected by strict loaders and ignored by the rest. This is the one place
  the standards allow a `---` fence and no decorative header or footer.
- **Description:** at most 1,024 characters and no angle brackets. Third
  person: what it does, then "Use when ..." with the user's own words, then
  the indirect asks it should catch ("even if they never say ..."). Put the
  main use case first. It carries the whole burden of triggering.
- **Body:** under 500 lines. Reference files sit one level down, such as
  `references/forms.md`, and `SKILL.md` says when to read each. A reference
  over 100 lines opens with a list of its contents.
- **Scripts** live in `scripts/`: no prompts, a `--help`, errors that say what
  to do next, structured output on stdout, the same result when run twice,
  and a `--dry-run` for anything that writes.

[`references/templates.md`](references/templates.md) has a `SKILL.md`
skeleton and a test file to copy.

## 5. Test it before anyone relies on it

1. **Triggers.** Write about ten prompts that should load the skill and ten
   near misses that should not, in varied wording. Keep six in ten for tuning
   and hold the rest back. Run each three times; a prompt passes when the
   skill loads in at least half its runs.
2. **Quality.** Run two or three real tasks with the skill and without it,
   and compare the results. If the skill does not beat no skill, it is not
   done.
3. **Tune the description, not the prompts.** Never paste a failing prompt's
   words into the description; generalise from it instead.

In Claude Code, `claude -p "<prompt>" --output-format json` shows whether a
`Skill` tool call named the skill. In the hub, tests go in
`evals/skills/<name>.json`, beside the skill rather than inside it, so they
never ship.

## 6. Ship it

- **In the hub:** add the folder and its tests, then run `make render` and
  `make check`. The renderer refuses a skill that breaks the format above.
  Open a pull request into `Development`; a release delivers it.
- **In a repository:** commit both copies in one pull request.
- Follow the standards for the branch, commits and pull request, and report
  the trigger and quality results in the pull request.

## Gotchas

- A skill named in the user's request but never triggered in tests is not
  finished; fix the description first.
- Two skills whose descriptions overlap steal each other's triggers. Search
  the existing skills before adding one, and merge rather than duplicate.
- A skill that fetches from the network or installs packages when it loads
  will fail in sandboxed apps; bundle what it needs or document the
  requirement in `compatibility`.
