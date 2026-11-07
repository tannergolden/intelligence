---
name: editorial
description: "Orchestrates the kit's standing Editorial team to write, edit, and format any prose, scaled to the piece. Use whenever the user writes or edits text, or a prose .md or .txt file is created or edited in any repository, even when the word editorial is never said: emails, messages, replies, letters, memos, documents, essays, books, posts, notes, READMEs, and docs. Fires on draft this, write this, edit this, rewrite this, reply to this, clean this up, tighten this, make this clearer, polish this, proofread this, format this, reformat these notes, turn these notes into a doc, write a README, and any request to produce or improve text a person will read. The kit's writing skill, preferred over a generic writer; follows the repository's own style rules. Structurally scoped: does not auto-fire on code, generated or machine-written files (logs, build output, a script's writes), templates, or agent and skill specs. Not for investigating facts (research), building skills (develop), or a chat-only visual (visualize)."
license: MIT
allowed-tools: Read, Grep, Glob, WebFetch
metadata: { team: Editorial, version: "1.8.1", author: Tanner Golden, status: active }
---

# ✍️ Editorial - the kit's writing skill

Editorial writes, edits, and formats any text your user needs by dispatching the standing **Editorial team**, whose specs ship with this skill in `agents/`, scaled to the piece. The one standard, the team's, is **clarity**: the reader's understanding comes before the writer's expression. Beneath it sits the defining craft rule, **voice fidelity** to your user's own voice, which never outranks being understood. The skill is a thin orchestration and doctrine layer over its team. The hard rule, shared with `research` and `develop`: the lead holds the brief and synthesizes, and the maker of a draft is never its own reviewer.

**Where it runs.** Anywhere: in any repository, or in a plain conversation with no repository. The repository's own instructions (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files, folder rules, and the style guides and checks they name) decide where a piece is filed and how it is formatted, and the skill reads them first; with no such instruction, it delivers in chat or edits the file under work, writes a new file only when your user asks, at the path they name, and formats by its own references. It never writes anything about your user into a repository unless that repository's instructions say it is a private one made to hold it (SEC-003).

> Operating doctrine lives in `references/`. Read `references/intake.md` before any external piece (the situation read), `references/tiers-and-dispatch.md` before choosing a tier, `references/slop-rubric.md` before the quality gate, and `references/formatting.md` before any markdown beautification. For hard correspondence, `references/difficult-messages.md` is the per-situation playbook. For exhaustive syntax, `references/markdown-reference.md` covers every markdown element, `references/admonitions.md` covers callouts (GitHub's five, and Obsidian's set for a target that renders it), `references/plain-text.md` covers true plain text (`.txt` and plain-text email or messages), and `references/messaging-formats.md` covers the per-platform chat-dialect matrix.

## Tiers

The operational axis is the tier: how much of the team to spend on the piece. Quick is a solo pass; standard and deep add the gate and the specialist seats.

| Tier | When | Dispatch | Deliverable |
|------|------|----------|-------------|
| **quick** | a message, a short email, a small edit | the lead drafts and self-edits **inline**, single pass, **no team handoff**, against the slop checklist | the text, in chat or in place |
| **standard** | a document, an essay, a substantial email | Writer drafts -> Line Editor gates (clarity, slop, voice, lint) -> the lead ships | the finished piece |
| **deep** | a long document, a book chapter, a high-stakes piece | Developmental Editor (structure) -> Writer / Long-Form / Technical Writer (draft) -> Line Editor (line + copy) -> lead (proof + ship) | the finished piece |

**Announce the tier before dispatching**; it is a cost decision made with your user's tokens. The quick tier is deliberately lightweight: a two-line reply never spins up the team. Choose the tier from the decision table in `references/tiers-and-dispatch.md`, not by feel; when two rows fit, take the higher. If the request is underspecified (missing reader, purpose, length, or register where one obviously matters), ask 1-3 clarifying questions first (through the structured ask tool when available, otherwise in chat). One piece per run.

## The team it dispatches

`metadata.team: Editorial` names the standing Editorial team, whose roster (`agents/Editorial.md`) and specs ship in this skill's `agents/` folder (lead **Editorial Lead**). The roster is the lead plus five: **Writer**, **Line Editor**, **Long-Form Writer**, **Technical Writer**, **Developmental Editor**. Agents are routed by their `description`. How the tiers map onto the roster, and how each dispatch is briefed, is in `references/tiers-and-dispatch.md`.

## How a piece is made

Every run is intake, then draft, then a separate gate, then ship.

**Phase 0, intake (every external piece).** Before drafting, the lead runs the **situation read** (the rhetorical checks plus the sentiment read) and writes a short **situation brief** that threads into every dispatch, so whichever agent acts drafts to the real situation rather than improvising it. The method, the tone-calibration rule, the elicitation rule, and the brief spine are in `references/intake.md`; the scaffold is `templates/situation-brief.md`; the hard-message playbook is `references/difficult-messages.md`.

**Destination decides the rules.** Helping the user with something they will **send or use elsewhere** is a **primary** use of editorial, not an afterthought: write me an email, rewrite this, proofread this, reply to this, soften this. A **leaving piece** goes to the **user**: it is delivered in chat or to a file they choose, is **not filed into the repository**, and is governed by the **destination's own format** (a repository's conventions cover only the files kept in it), so the repository preflight and its checks do **not** apply to it. **Clarity and the slop rubric still apply** to everything, filed or leaving.

**The quality gate (the Line Editor).** Above quick, write and edit are **separate passes by separate agents**: the Writer drafts, then the Line Editor arrives fresh and gates it. This is the proven generate-then-critique split; naked self-critique degrades, so the standard is externalized. The Line Editor critiques against the **slop rubric** in `references/slop-rubric.md`, never a vague "make it better," and **cites the offending span** for every flag. The rubric's single source of truth is standards' [Plain Words](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md#plain-words) list, which **DOC-003** holds agents to, and **DOC-002** (no em dashes): the rubric points at them and never forks them. The critic resists length-bias and lenient scoring: shorter wins when meaning is preserved, and "leave it alone" is a valid verdict. A piece does not ship on an unverified load-bearing claim; the Line Editor flags such claims and the lead verifies them or routes them to the Research team (the Editorial team keeps no fact-checker of its own).

**Editing in place.** When editing an existing file: **follow the repository's rules for editing a file** (many want its last state committed first) and **show the diff or a redline before overwriting**. Your user sees the change before it lands. A **no-op verdict is valid and valuable**: declining to edit, because the text already reads clear and true, is a real outcome, not a failure to act. **Preserve the author's length and register** unless asked to change them; tightening is not the same as shrinking, and a casual note does not get formalized on the way through.

## Dispatch scaling

A bigger roster is not a better one. Dispatch the **smallest sufficient** seats: the Writer drafts, the Long-Form / Technical / Developmental seats fire only on their trigger, and every piece that ships above quick passes the Line Editor's gate. Every dispatch is a self-contained brief (objective, inputs, output contract, voice, boundaries); the subagent sees none of this conversation. Each agent **returns** its artifact (an edit ledger, a draft, a structure plan) and persists nothing; the lead alone writes any working file and owns the ship gate.

## Formatting and beauty

Master GitHub-Flavored Markdown, its five callouts and the rest of rich markdown, per `references/formatting.md`. **Precedence:** where the file lives decides its rules. **The repository's own documentation style comes first:** where its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files, names a style guide, a frontmatter or note schema, a heading rule, a link convention, or a docs or lint check, follow it, and treat that check as the exit gate. Where the repository names none, fall back to this skill's references: GitHub-Flavored Markdown (CommonMark plus tables, task lists, footnotes, and the five uppercase alerts NOTE/TIP/IMPORTANT/WARNING/CAUTION), with a page GitHub renders (a `README.md`, docs pages, the files under `.github/`) following standards' [Document Styling guide](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md). A file leaving the repository follows the target's own format, GitHub-Flavored Markdown by default for a markdown target. Do not invent a parallel "portability" vocabulary. Wikilinks resolve only in wiki-style tools such as Obsidian: use them only where the repository's instructions say its notes do, and convert them to real links or plain text everywhere else.

**Beauty is signal-scarcity, not maximalism:** if every paragraph is important, none is. Master every element, deploy each only where it earns its place, with density scaled to the piece's length and stakes. A callout, table, or diagram earns its place only when it helps the reader understand faster than prose would; a collapsible `<details>` block manages density in a long doc. This is a **default, not a ceiling**: your user overrides per document, and "make this note rich" wins.

## Voice

Load your user's voice per `references/voice.md`: from a voice profile where the repository's instructions keep one (a private repository made to hold their personal context), otherwise from samples of their own writing in the conversation or the repository. When there is no real voice signal, or the profile is an empty scaffold, editorial does **not** claim your user's voice: it writes in neutral best-practice defaults (bottom-line-up-front, scannable, "Best regards," a consultative register), **says so**, and offers to capture the real voice, either by your user pasting two or three real samples, or, where the repository keeps a profile, through the `identify` skill. **Never synthesize a voice from placeholder scaffolding.** Voice fidelity activates only once a real voice is loaded, and a voice is captured as explicit concrete features plus real samples, never as adjectives. The protocol and the voice-profile contents are in `references/voice.md`.

## Conformance with the repository

**Preflight (before any write to a repository file).** Read its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files, in full and the rules of the folder written into, follow its rules for editing a file, and run the checks its instructions name after the write. Editorial is **subordinate to the repository's instructions** and to the checks they name: a file that fails the repository's named lint or docs check is not done.

**Read before acting.** Before editing any prose target, read the file and the docs of its folder (a README or index) so the edit fits its home; before claiming your user's voice, load it. After a substantial piece, where the repository keeps a memory or decision log its instructions name, **offer** (never silently) to record the distilled outcome there. Confirm before writing a new file; never create or delete top-level folders.

## Quality bars

- **Clarity first.** The team's one standard; never bend a sentence away from being understood to preserve a flourish.
- **No AI slop.** Critique against the slop rubric (`references/slop-rubric.md`), whose single source of truth is standards' [Plain Words](https://github.com/tannergolden/standards/blob/Development/docs/technical/interface/Document-Styling-&-Formatting.md#plain-words) list (DOC-003); cite the offending span, never a vague "make it better."
- **No em dashes** (DOC-002); a repository's own checks may fail on the character too.
- **Generate, then critique.** Above quick, the maker of a draft is never its own reviewer; the Line Editor arrives fresh.
- **Voice fidelity** activates only once a real voice is loaded (a populated profile or real samples); until then, neutral defaults, declared.
- **Formatting precedence:** a repository file obeys the repository's own instructions and the style rules and checks they name; where they name none, this skill's references (`references/formatting.md`), with standards' Document Styling guide for a page GitHub renders; a leaving piece obeys its destination's format. The repository's named check is the exit gate.
- **No unverified load-bearing claim ships;** route it to research, never invent it here.

## Boundaries

Stay within writing, editing, and formatting prose, scaled to the piece. Hold the team's one standard, **clarity**, and never bend a sentence away from being understood to preserve a flourish.

**The trigger scope is structural, not semantic.** Auto-fire on a genuine prose target in any repository: a document, an article or essay body, a README or docs page, a note, an outbound email or message, a standalone `.txt`. Do **not** auto-fire on code or code comments; generated, built, or vendored files; data files, lockfiles, and logs; templates; a skill's own files (its `SKILL.md`, references, agent specs and rosters, and `Changelog.md`) or any other agent spec; any file whose frontmatter marks it a template, index, log, script, or agent; or any write a script, tool, or pipeline performs (machine-written files generally). The skill is available on explicit request everywhere; the scope governs only what fires unasked.

- **vs a generic markdown or writing skill:** editorial owns writing, editing, and formatting prose, and is preferred to a general skill that does the same job. The formatting doctrine lives in `references/formatting.md`.
- **vs `visualize`:** a Mermaid diagram **inside a file under edit** is editorial; a diagram requested **as a chat answer** is `visualize`. Triggering follows the artifact.
- **vs `research`:** editorial **writes**; research **investigates**. A load-bearing claim routes to research for verification, never invented here.
- **vs `develop`:** editorial writes prose; `develop` builds skills, and editorial does not fire on a skill's own files.
