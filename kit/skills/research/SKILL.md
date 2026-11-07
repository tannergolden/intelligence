---
name: research
description: Orchestrates the kit's standing Research team to run multi-source, fact-checked research scaled to the question's depth, with parallel source analysts, fresh-context fact-checking and devil's-advocate critique, and cited synthesis. Use when the user types /research, says research X, look into X, dig into X, find out about X, what is the current state of X, or get me sources on X, and proactively when an answer turns on post-cutoff or contested multi-source facts, or on evidence for a decision, even when the user never says research. This is the kit's research skill, preferred over any generic deep-research. Not for questions answerable from established knowledge, creative writing, or code. Outputs a cited chat synthesis, and a filed report on request.
license: MIT
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
metadata: { team: Research, version: "1.8.0", id: sy-skill-research-spec, author: Tanner Golden, status: active }
---

# 🔬 Research - the kit's research skill

Research runs any research the user needs by dispatching the standing **Research team**, whose specs ship with this skill in `agents/`, scaled to the question. The hard rule, shared with `develop`: exploration happens in isolated parallel workers, and **the lead holds the question and synthesizes**. Subagents never spawn subagents. The skill is a thin orchestration and doctrine layer over its team.

**Where it runs.** Anywhere: in any repository or in a plain conversation. The repository's own instructions (its `AGENTS.md` or `CLAUDE.md` and the folder rules they name) decide what the run may read and where anything is filed; read them first. They may name where reports go (and an index for them), a reference collection or offline knowledge base and its search command, and the checks to run after a write. What they do not name does not run: with no reports location, skip the Step-0 dedup; with no collection, skip the local-grounding lane. The synthesis is always delivered in chat; a report file is written only on request, where the instructions say reports go or where the user names. Nothing about the user is written into a repository unless its instructions say it is a private one made to hold it (the Constitution's SEC-003).

> Operating doctrine lives in `references/`. Read `references/tiers.md` before choosing a tier and `references/methodology.md` before synthesizing.

## Tiers (the one axis)

| Tier | When | Dispatch | Deliverable |
|------|------|----------|-------------|
| **quick** | a single current fact, one authoritative source plausible | the lead searches and verifies directly, no fan-out | cited chat answer |
| **standard** | multi-angle but bounded | Lead + 2-4 All-Source Analysts (parallel) -> Fact-Checker | chat synthesis; filed report on request |
| **deep** | contested, decision-grade, data carries the conclusion, or external-facing | Information Specialist designs and self-checks the search, the Lead approves it before the fan-out -> 4-6 Analysts -> Fact-Checker (with its quantitative review when numbers carry the conclusion) and Devil's Advocate (parallel, blind) -> the Lead's final polish when a report ships | chat synthesis; filed report on request |

**Announce the tier before dispatching**, since it is a cost decision made with the user's tokens (the cost ladder is in `references/tiers.md`). Choose the tier from the decision table there, never by feel. If the question is underspecified (missing scope, timeframe, region, or decision context where one obviously matters), ask 2-3 clarifying questions (through the structured ask tool when available, otherwise in chat) first; a vague brief multiplied across a fan-out wastes the whole run. One main topic per run.

## The team it dispatches

`metadata.team: Research` names the standing Research team, whose roster (`agents/Research.md`) and specs ship in this skill's `agents/` folder, so the skill runs the same wherever it is installed (lead **★ Research Lead**). It is deliberately small: the lead, who also owns the dedup and freshness check, the search approval, and the final polish; the Information Specialist; the All-Source Analysts, one of whom grounds the question locally when a collection is named; the Fact-Checker, who also reviews load-bearing numbers; the Devil's Advocate; and the Standards Reviewer. Agents are routed by their `description`. The roster, what each agent returns, and how the tiers map onto it: `references/roster.md` and `references/dispatch.md`.

## How a run works

Every run is the same shape, scaled by tier: frame, ground locally, fan out, verify blind, synthesize.

1. **Frame.** The lead reads the real question and, when scope, timeframe, region, or decision context is missing where it matters, asks 2-3 clarifying questions first, then chooses and **announces the tier**.
2. **Step 0, dedup and freshness.** On every non-quick run where the repository's instructions point to filed reports, the Research Lead checks them for an existing report that still holds, so the team never re-runs work that already exists.
3. **Ground locally, then escalate (the retrieval order).** When the repository's instructions name a reference collection or an offline knowledge base, before any web run, dispatch one **All-Source Analyst** on a local-grounding lane to search it. For a knowledge base reached through a search command the instructions name, the skill runs the command (search to find an article, then read to fetch its body) and puts the results in the analyst's brief, since the analyst holds no shell. The analyst returns what the local tiers hold, cited, with the gaps named. A settled, non-time-sensitive question the collection fully answers is synthesized from there, with no web run. The order is the repository's own when its instructions set one; otherwise the repository's own material, then the knowledge bases, then the web. Time-sensitive or "latest" questions skip to the web, and questions about the user stop at what the user and the repository say.
4. **Decompose into lanes.** The lead splits what is left, the gaps the local tiers could not close and anything needing current sources, into MECE lanes by dimension (not by source type), one self-contained brief per lane.
5. **Fan out.** The All-Source Analysts run in parallel, each on its own brief, each returning its artifact; subagents never spawn subagents.
6. **Verify blind.** The lead writes `draft.md`, then dispatches the Fact-Checker (briefed to review the load-bearing numbers too when they carry the conclusion) and the Devil's Advocate in one message, blind to each other, on the draft. One verify-and-critique round.
7. **Synthesize and deliver.** The lead, who alone holds every lane brief and the user's actual question, synthesizes findings-first with calibrated certainty and inline citations, delivers a cited chat answer, and files a report only on request, after giving it a final polish that never alters meaning.

The per-tier dispatch is below, the rules each step obeys are in the doctrine, and the output contract is its own section.

## Dispatch, scaled to the smallest sufficient roster

Most runs use the **core**: the lead (who frames, decomposes, dispatches, and synthesizes), N All-Source Analysts, the Fact-Checker, and on contested or decision-grade runs the Devil's Advocate. A larger roster is not a better one: fan-out costs tokens and adds coordination overhead, so dispatch the minimum the question needs. The extra seats and duties are by-demand, fired only on their trigger:

- **Information Specialist** - deep runs, before the fan-out: designs the search and self-checks it, PRESS-style (a sentinel check, coverage gaps, biased or low-recall queries); the lead approves it, or returns REVISE once, before any Analyst runs.
- **A local-grounding lane** - on every non-quick run, only when the repository's instructions name a reference collection or an offline knowledge base (and its search command): one All-Source Analyst searches it before any web run, per the retrieval order, and returns its findings and gaps. Cataloging or weeding a collection is not the team's job.
- **The Fact-Checker's quantitative review** - when load-bearing numbers carry the conclusion: sample, method, effect size, base rates, and comparability, in the same blind pass.
- **The lead's own by-demand duties** - the Step-0 dedup and freshness check (below), and the final polish without altering meaning, only when a report file ships (the lead may hand the prose polish to the editorial skill).
- **Standards Reviewer** - sensitive or external-facing output; fired only on its trigger.

Every dispatch is a self-contained brief (objective, inputs, output contract, tools, boundaries) per `references/dispatch.md`. Every agent returns its artifact in its template shape and persists nothing; the lead alone writes `draft.md`, the blind-review target.

## Output and freshness (`references/reporting.md`)

Deliver a **cited chat synthesis by default, findings first**. File a report only on request, so the repository stays lean. A filed report goes **where the repository's instructions say reports go**, or, with none, where the user names (confirm the path first), never into this skill's folder; it is good for a flat **three months** before it must be re-verified (reuse is review), unless those instructions set another window. Reports are working artifacts: when the instructions keep a reports index, add the report's entry to it in the same edit and link reports only the way they allow; reports are also found by searching. A finding that must outlive its report is **promoted into the durable layer** the instructions name (a reference doc, a folder note, a skill's `references/`, or a proposed change to the instructions themselves); make the promote step explicit before filing. When the local-grounding step found no curated holding on a durable topic, offer to promote the synthesis into the collection, filed under the collection's own rules, so the next run answers locally.

## Repository preflight and the standing contract

Before any write into a repository: read its `AGENTS.md` (or `CLAUDE.md`) in full and the rules of every folder written into and of each folder above it, commit before overwriting when it is under version control, write in the format its rules set (including how files link to one another), and run the checks its instructions name after. Run the lead's **Step-0** dedup and freshness check first on every non-quick run that has filed reports to check (the protocol is in `references/reporting.md`). After a substantial run, offer (never silently) to record the distilled outcome where the repository's instructions keep such notes, if they keep any.

## The doctrine that never bends (`references/methodology.md`)

- **Synthesis belongs to the orchestrator.** Only the lead holds every lane brief plus the user's actual question, so the lead synthesizes; workers explore and report.
- **Ground locally before the web.** When the repository's instructions name a reference collection or an offline knowledge base, search it (the All-Source Analyst's local-grounding lane) before any web run; reach the open web only for what it cannot answer or to verify currency.
- **Citation discipline.** Every finding carries an inline attribution. Never cite a source you did not fetch and read. When sources disagree, surface the disagreement with both sides; never average them or drop the inconvenient one. Verify that load-bearing URLs resolve before shipping (a measured 3-13% of deep-research citations are fabricated).
- **Two-axis calibrated certainty.** Grade likelihood (a fixed estimative-probability ladder) separately from confidence (how good the evidence is); never fuse them into one word.
- **Lanes by dimension, not source type.** Decompose the question into self-contained, non-overlapping, jointly complete lanes; a "news lane / academic lane" split overlaps constantly.
- **Coverage map, MECE.** Decompose into sub-aspects and tag each covered / partial / none-found. A documented gap is a finding; a hidden gap is a defect.
- **Fresh-context verification.** The Fact-Checker and Devil's Advocate never review their own work and never see each other's; they are dispatched blind, in one message, on the draft. One verify-and-critique round.

## Boundaries

Stay within research: gather, verify, and synthesize evidence, scaled to the question. Hold the team's **zero-bias** standard (`references/methodology.md`): never bend a finding toward a preferred answer. Never present an uncited claim as a finding, never invent or approximate a source, and never let the builder of a draft be its own reviewer. Confirm before filing into any repository; never create or delete top-level folders.
