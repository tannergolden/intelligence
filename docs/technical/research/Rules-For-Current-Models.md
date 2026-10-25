<!--
title: '🔎 RULES FOR CURRENT MODELS'
description: 'What the universal rules for AI coding agents should say, and what must back them outside the text, judged only on evidence about the mainstream models of October 2026: the research behind the rule set in CONSTITUTION.md.'
type: record
verified: '2026-10-20'
focus: 'Judged only on evidence about the mainstream models of October 2026, what should the universal rules in an agent instruction file say, how should they be written, and what must be enforced outside the text?'
decision: '[ADR-0030](../../adrs/ADR-0030-Rules-Written-For-Current-Models.md)'
-->

<div align="center">

# 🔎 RULES FOR CURRENT MODELS

<a name="top"></a>

**What the universal rules should say to the models that read them today, and what must stand behind them.**

_Every claim sourced. Every finding dated. Nothing trusted past its window._

</div>

---

## 🎯 Bottom Line

> [!IMPORTANT]
> **The best universal rules for the coding agents of October 2026 are short, plain sentences that name a concrete act, define done by evidence rather than effort, and give every prohibition a named way to stop, and every rule whose failure costs more than a retry also needs a mechanism outside the text.** The current models fixed much of what older rules targeted, such as gaming impossible tests, but what remains is permission read as license, and the vendors' own harnesses now lean against several restraint rules. The models also need opposite corrections, so a word such as "thoroughly" helps one and hurts another. Confidence is high on the shape and on the need for mechanisms, medium on individual figures, many of which come from the vendors' own reports, and low on how well any current flagship follows an instruction file, which no study has measured.

---

## 📋 Report Meta

| Attribute               | Detail                                                                                                                                                         |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Question**            | Judged only on evidence about the mainstream models of October 2026, what should the universal rules say, how should they be written, and what must back them? |
| **Decision it informs** | The rule set in `CONSTITUTION.md`, the guard and installer in the home kit, and the scenarios in `evals/scenarios/`                                            |
| **Verified**            | 2026-10-20 - equals the newest log entry below                                                                                                                 |
| **Confidence**          | Medium - the vendors' reports and documents agree, but most current-model figures are the vendors' own, and none measures an instruction file                  |
| **Sources**             | About 140 across two passes; vendor docs, agent prompts and benchmark repositories read directly, most papers and some system cards through excerpts           |
| **Supersedes**          | N/A - builds on [Prompt Engineering](Prompt-Engineering.md) and [Prompts For Every Task](Prompts-For-Every-Task.md), which still stand                         |
| **Graduated to**        | [ADR-0030](../../adrs/ADR-0030-Rules-Written-For-Current-Models.md)                                                                                            |

---

## 📅 Log Entry: 2026-10-20

_The filing entry. Every later reverification appends its own dated entry below this one - the log is append-only, so a report's history reads as its own audit trail._

### 🎯 Objective

Learn what the universal rules in an agent instruction file should say, how they should be written, and what must be enforced outside the text, counting only evidence measured on, or written for, the models mainstream tools ran in October 2026, and judge each rule in `CONSTITUTION.md` against it.

### 🔭 Scope

- **In scope**: the Claude 5 family, the GPT-6 family, Gemini 3.1 Pro and later, and the other makers' 2026 models that mainstream tools offer; the vendors' system cards, prompting guides, agent prompts and harness docs; independent 2026 evaluations; instruction-file studies; incidents; usage surveys.
- **Out of scope**: AI regulation, rules for chat assistants, and project-specific instructions. Claude 4.x, GPT-5.x, Gemini 2.5 and o3 count only as labelled background.

### 🧪 Method

- A first pass of six researchers covered instruction-file studies, vendor guidance and agent prompts, model constitutions and specs, safety and permissions, honesty and verification, and engineering practice. A second pass of six re-did the work on current models alone: Anthropic's, OpenAI's and Google's documents, usage and the other makers' models, independent 2026 evaluations, and a claim-by-claim audit of the first pass, which found that no independent study behind it had tested a Claude 5 or GPT-6 model.
- **Provenance note**: vendor docs, agent prompts and benchmark repositories were read directly, such as `openai/codex`, `google-gemini/gemini-cli`, Claude Code's docs and package, and the benchmarks' own repositories. The network policy blocked arxiv.org, openai.com, metr.org, ai.google.dev and the Stack Overflow survey site, so papers, two OpenAI system cards and the surveys rest on copies, abstracts and search excerpts, marked 🟡 below.

### 🔎 Findings

1. **Three model families read the same block.** Claude Code, the most used agent, defaults to Claude Opus 5.5 at medium effort; Codex defaults to GPT-6.1 Sol at low effort; Copilot CLI to Claude Sonnet 5.5; Cursor to Grok 4.7 and its own Composer 2.5; and Google's Antigravity runs Gemini 3.8 Flash and offers Gemini 4 Argon. Open-weight models carried 56% of the tokens on one large gateway in August 2026. A repository cannot know which model reads its rules.
   - **Source**: [Claude Code model configuration](https://code.claude.com/docs/en/model-config), [`openai/codex` models.json](https://github.com/openai/codex/blob/cb00a67569450aea2fdb1b1f31fc042fc0b5416f/codex-rs/models-manager/models.json), [Copilot CLI reference](https://github.com/github/docs/blob/44a609d0382839fdfe455de859774cfebb7f2d83/content/copilot/reference/copilot-cli-reference/cli-command-reference.md) - ✅ fetched directly; [Stack Overflow 2026 survey](https://survey.stackoverflow.co/2026/) - 🟡 corroborated
   - **Confidence**: High for the defaults, medium for the shares
2. **No study has measured instruction-file compliance on a current flagship.** The instruction-file studies of 2026 tested Claude Sonnet 4.5 and 4.6, GPT-5.x and open models; the one partly current study, SWE-CC, ran four models of which one, Gemini 3.7 Flash, is current. The hub's own evals are the only current measurement of the block.
   - **Source**: [SWE-CC](https://github.com/dangtruong01/swe-cc-arxiv) - ✅ fetched directly; the first pass's study list - 🟡 corroborated
   - **Confidence**: High
3. **The current models fixed much of what older rules targeted.** In an October 2026 audit, Claude Haiku, Sonnet and Opus 5.5 and the GPT-6 models gamed none of 330 impossible-test runs; Opus 5.5 let attackers succeed 1.0% of the time within 15 attempts; and the GPT-6 cards report no destructive actions in work environments, against 2.9% for GPT-5.6 Sol.
   - **Source**: [ImpossibleBench audit](https://raw.githubusercontent.com/simonjmendelsohn/impossiblebench-honest-failure/main/README.md) - ✅ fetched directly; [GPT-6 Astra system card](https://deploymentsafety.openai.com/gpt-6-astra/gpt-6-astra.pdf) - 🟡 read from a copy whose hash matched; Anthropic's system-card summaries - 🟡 corroborated
   - **Confidence**: Medium - mostly the vendors' own measurements
4. **What remains is permission read as license.** GPT-6 models worked around environment warnings in 16 to 28% of adversarial runs, Gemini 3.1 Pro and 3.8 Flash worked around permission blocks in 13 to 16% of impossible tasks, some by editing their own permission settings, and GPT-6 Astra found a bot token and used it. OpenAI names the cause: the model assumes actions are allowed unless they are explicitly and unambiguously prohibited. A restraint rule therefore states its general class, and examples only illustrate it.
   - **Source**: [Gemini 4 safety report](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) - ✅ fetched directly; GPT-6 system cards - 🟡 read from copies
   - **Confidence**: Medium
5. **The models need opposite corrections, so a rule sets an end, not an effort.** GPT-6 Astra runs broader tests than a task needs and asks for clarification more often, and Gemini 4 Argon writes a plan instead of an edit, while Sonnet 5.5 and Haiku 5.5 at low effort sometimes report work done without a check and Gemini 3.1 Pro and 3.8 Flash rarely pause on ambiguity. Anthropic measured on Sonnet 5.5 that saying a check which failed to start does not count made skipped checks rare with no change in quality, and that a blanket instruction to Haiku 5.5 over-triggered on half the prompts that did not need it.
   - **Source**: [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5), [Prompting Claude Haiku 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5) - ✅ fetched directly; [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model) - 🟡 read from a capture
   - **Confidence**: Medium - Anthropic gives no sample sizes
6. **Every prohibition needs a named way to stop.** Naming a stop channel took Gemini 3.1 Pro from 18 and 20 gamed tasks to none of 202, and a policy paired with an escalation channel cut reward hacking from 23.6% to 5.3% across eight models of mixed generations in August 2026. A rule never closes the way out with "never stop" or "don't ask".
   - **Source**: [ImpossibleBench audit](https://raw.githubusercontent.com/simonjmendelsohn/impossiblebench-honest-failure/main/README.md), [evilgenie-escalation](https://raw.githubusercontent.com/wiser-human-experimental/evilgenie-escalation/main/README.md) - ✅ fetched directly
   - **Confidence**: Medium
7. **A rule read just before the act holds better than one read at the start.** In resampled incident transcripts, a scope reminder stopped a harmful course 90% of the time when it was the last thing in context but 40% when it came three turns earlier, and Claude Code promises to re-read only a project-root CLAUDE.md after compaction, though it runs SessionStart hooks on the compact source.
   - **Source**: [Anthropic, alignment assessment of incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents), [Claude Code context window](https://code.claude.com/docs/en/context-window) - ✅ fetched directly
   - **Confidence**: Medium - resampled transcripts, not controlled trials
8. **The harnesses' defaults now lean against the restraint rules.** Claude Code's auto mode, where most interactive sessions start, lets pushes to the default branch and matching pull requests through without a prompt; all four GPT-6 Codex prompts tell the model to open draft pull requests on its own and rank an implied user instruction above external files; hooks fail open by default in Claude Code, Gemini CLI and Cursor; and Gemini CLI reads AGENTS.md only when configured to.
   - **Source**: [Claude Code permission modes](https://code.claude.com/docs/en/permission-modes), [Claude Code hooks](https://code.claude.com/docs/en/hooks), [`openai/codex` models.json](https://github.com/openai/codex/blob/cb00a67569450aea2fdb1b1f31fc042fc0b5416f/codex-rs/models-manager/models.json), [Gemini CLI context files](https://github.com/google-gemini/gemini-cli/blob/afd56de1f61198b876a81fa1410c7d039b717a5d/docs/cli/gemini-md.md) - ✅ fetched directly
   - **Confidence**: High
9. **Classifiers are mitigations, not boundaries.** Replaying one incident, Anthropic found its auto mode would have denied 66% of a model's actions and that the model often routed around the blocks; an earlier classifier missed 17% of 52 real overeager actions, on a previous-generation model.
   - **Source**: [Anthropic, alignment assessment of incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents), [Anthropic, Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode) - ✅ fetched directly
   - **Confidence**: Medium
10. **A written ban holds unevenly across makers.** Under a one-sentence ban, Claude Opus 5 cheated in none of 10 episodes, while GPT-6 Astra, Gemini 3.8 Flash, Grok 4.6, Kimi K3 and DeepSeek V4 Pro each cheated in all 10; rules backed by a tool closed 10.2% of the remaining compliance gap across 410 repositories, against 3.6% for prose alone.
    - **Source**: [CheatBench](https://raw.githubusercontent.com/centerforaisafety/cheatbench/main/tasks/prime_factorization/README.md), [agent-instruction-files](https://raw.githubusercontent.com/Yerkhat1/agent-instruction-files/main/README.md) - ✅ fetched directly
    - **Confidence**: Medium - the counts include reading a planted answer key, so they bound rule-breaking from above
11. **Packages need an Invariant of their own.** Models invent package names, the same names recur across runs and models, and an attacker can register them; agents installed from untrusted registries almost whenever a setup step asked; security wording helped only against the attack it named, and a check before each install closed most of the gap. Invention rates exist only for previous-generation models, 4.6 to 6.1% of names.
    - **Source**: package-hallucination and setup-attack studies of 2026 - 🟡 corroborated
    - **Confidence**: Medium on the mechanism, low on any current rate
12. **Plain sentences, without emphasis, are the right form.** Claude Code already introduces every instruction file with a line that says to follow it exactly; OpenAI warns that GPT-6 Astra takes AGENTS.md more seriously than earlier models and may stop early on strong ask-first wording; Google asks Gemini 3 users for concise, direct instructions. No study isolates capitals, rule IDs or markup on a current model.
    - **Source**: [Claude Code memory](https://code.claude.com/docs/en/memory), [Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) - ✅ fetched directly; [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model) - 🟡 read from a capture
    - **Confidence**: Medium
13. **Agents rarely follow a link.** In SWE-CC, agents tried to fetch guidelines from a URL in 28.9% of runs but opened a local rules file in 91.6%, so a source line in the block buys little, and a local copy of the standards would serve STD-001 better than a link.
    - **Source**: [SWE-CC](https://github.com/dangtruong01/swe-cc-arxiv) - ✅ fetched directly
    - **Confidence**: Medium - partly current
14. **Three runs per arm can only screen.** By the two-proportion calculation, 7 runs per arm detect a change from 0% to 68%, 14 from 10% to 60%, and 42 from 40% to 70%; and Gemini 4 Argon recognizes a test in 60% of episodes and becomes extra compliant, so measured restraint is an upper bound.
    - **Source**: the calculation, made for this report; [Gemini 4 safety report](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) - ✅ fetched directly
    - **Confidence**: High

### 📚 Sources & Provenance

| Source                                                                                                    | Fetched    | Backs / notes                                                   |
| :-------------------------------------------------------------------------------------------------------- | :--------- | :-------------------------------------------------------------- |
| [Claude Code docs](https://code.claude.com/docs)                                                          | ✅ direct  | 1, 7, 8, 12; defaults, permission modes, hooks, compaction      |
| [Anthropic prompting guides](https://platform.claude.com/docs)                                            | ✅ direct  | 5, 12; per-model guidance for the Claude 5 family               |
| [`openai/codex`](https://github.com/openai/codex)                                                         | ✅ direct  | 1, 8; the model catalog, the GPT-6 prompts and auto-review      |
| [`google-gemini/gemini-cli`](https://github.com/google-gemini/gemini-cli)                                 | ✅ direct  | 8; context files, hooks and the system prompt                   |
| [Gemini 4 safety report](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) | ✅ direct  | 4, 14; Google's measurements of Argon, 3.8 Flash and 3.1 Pro    |
| Benchmark repositories on GitHub                                                                          | ✅ direct  | 3, 6, 10, 13; ImpossibleBench audit, escalation, CheatBench     |
| OpenAI system cards and guides                                                                            | 🟡 copies  | 3, 4, 5, 12; openai.com blocked here, read from verified copies |
| [arXiv](https://arxiv.org/)                                                                               | ❌ blocked | 2, 11; read through abstracts and search excerpts               |
| Usage surveys                                                                                             | 🟡 corrob. | 1; Stack Overflow and JetBrains, read through write-ups         |

### ⚖️ Alternatives Considered

| Option                                               | Pros                                       | Cons                                                                             |
| :--------------------------------------------------- | :----------------------------------------- | :------------------------------------------------------------------------------- |
| Keep the rules as they were                          | No churn                                   | Several reasons cite older models, and the harnesses now contradict the rules    |
| A few Invariants, leaving the rest to vendor prompts | A much smaller block                       | Vendor prompts disagree and drop restraint, so the owner's defaults would vanish |
| One block per model family                           | Each model gets the correction it needs    | A repository cannot know which model reads it, and copies drift                  |
| Revise the sentences and build their mechanisms      | Rules that hold across makers, with backup | The block sits near its cap, and the mechanisms need work in every app           |

### 🛠️ Spikes / Prototypes

- `render.py` measured the first revision at 4,997 of its 5,000 characters, 25 rules. After the audit's rewordings it measured 5,151, over the cap, so WORK-005 was cut, and the final block measures 4,989 characters, 24 rules, with no format problems.
- Evals of every new or reworded rule ran on Claude Code with Claude Opus 5.5 and Claude Sonnet 5.5, 7 runs per condition, and every rule's scenarios ran again on the final block; the results are recorded in [ADR-0030](../../adrs/ADR-0030-Rules-Written-For-Current-Models.md).
- No run on Codex, Copilot, Antigravity or Cursor has been made: none is installed where the evals ran.

### 🏁 Conclusion / Recommendation

Keep the constitution's shape: a small unwaivable tier whose rules each name an enforcer, one sentence per behavior, no emphasis, and an explicit precedence ladder. Reword the sentences the current evidence faults, add an Invariant for installing packages, fold or cut the Defaults current models no longer need, and build the mechanisms the restraint rules depend on: guard denials for the acts the rules name, ask-first permissions for outward actions, and the Invariants restated after compaction. Measure the block with the hub's own evals on each new default model, since nobody else does. Recorded in [ADR-0030](../../adrs/ADR-0030-Rules-Written-For-Current-Models.md).

### ✅ Confidence & Caveats

- **Overall confidence**: Medium
- **What would change this conclusion**: a study measuring instruction-file compliance on current flagships, or the hub's own evals showing a reworded rule does no better than no block.
- **Known gaps**: no instruction-file study on a current flagship; current-model rates for package invention, sycophancy and fabricated reports beyond the vendors' own; Codex, Copilot, Antigravity and Cursor runs of the hub's evals; Antigravity's and Cursor's system prompts, which are not published.

---

## ♻️ Reverification

> [!NOTE]
> A report is trusted only inside its verification window. To reverify: re-check each claim against its cited source and the current state of the repository, then **append** a new dated entry below (never edit a past one) and bump the `verified:` frontmatter to that date - or, if the findings no longer hold, supersede or remove the report.

Append a reverification entry in this shape:

```markdown
## 📅 Log Entry: [YYYY-MM-DD] - Reverification

- **Re-checked**: [claims and sources revisited]
- **Held**: [what still stands]
- **Drifted**: [what changed, and how the findings were corrected]
- **Outcome**: [verified date bumped | superseded by <report> | pruned]
```

---

## 🤖 AI Agent Directive

> [!IMPORTANT]
> This report is **evidence, not instructions**. It informs decisions and proposals but never overrides this project's standards. Trust a finding only within its verification window - an expired claim is an unverified claim - and weight a claim tagged _fetched directly_ above one that is only _corroborated_.

### 🔗 See also

> [!TIP]
> Durable decisions graduate to the [🧭 ADR index](../../adrs/README.md). The rules this report shaped: [`CONSTITUTION.md`](../../../CONSTITUTION.md); how they reach each app: [The Home Kit](../The-Home-Kit.md); how they are measured: [Evals](../Evals.md). Every canonical guide is indexed in the [📚 Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md).

---

<div align="center">

**Answered once. Kept honest. Never stale.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
