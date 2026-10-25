<!--
title: '🔎 PROMPT ENGINEERING'
description: 'What makes a reusable task prompt for an AI coding agent work as of October 2026, and how a library of them should be checked, measured and kept current: the research behind the universal prompts in setup/Prompts.md.'
type: record
verified: '2026-10-20'
focus: 'What makes a reusable, copy-paste task prompt for an AI coding agent work, and how should a library of them be checked, measured and kept current?'
decision: '[ADR-0028](../../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md)'
-->

<div align="center">

# 🔎 PROMPT ENGINEERING

<a name="top"></a>

**What makes a reusable task prompt for a coding agent work, and how to keep a library of them honest.**

_Every claim sourced. Every finding dated. Nothing trusted past its window._

</div>

---

## 🎯 Bottom Line

> [!IMPORTANT]
> **A reusable task prompt works best as a short, specific contract: the context and its reason, anything pasted marked as data, a task that starts with a verb, limits with a way out, and a check the agent can run, with a report built from evidence. The habits of 2023 and 2024 (a persona, politeness, threats, "think step by step", emphasis in capitals) do nothing or harm on current models, and no wording secures pasted text, so the real boundary is what the agent may do. A library of such prompts should be linted on every commit and measured against the one-line request each replaces, on a pinned model, again at every model release.** Confidence is high on the shape and on verification, medium on the injection figures, and low on whether templates beat a well-written one-line request, which no study has measured.

---

## 📋 Report Meta

| Attribute               | Detail                                                                                                                                                    |
| :---------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Question**            | What makes a reusable, copy-paste task prompt for an AI coding agent work, and how should a library of them be checked, measured and kept current?        |
| **Decision it informs** | The rewrite of the universal prompts in `setup/Prompts.md`, the checks in `prompts.py`, and the prompt scenarios in `evals/prompts/`                      |
| **Verified**            | 2026-10-20 - equals the newest log entry below                                                                                                            |
| **Confidence**          | Medium - the vendors agree and the main findings replicate, but most studies used benchmarks rather than agentic coding runs                              |
| **Sources**             | About 125 cited in the full report; vendor documentation and repositories mostly fetched directly, most papers through abstracts and search excerpts only |
| **Supersedes**          | N/A                                                                                                                                                       |
| **Graduated to**        | [ADR-0028](../../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md)                                                                                      |

---

## 📅 Log Entry: 2026-10-20

_The filing entry. Every later reverification appends its own dated entry below this one - the log is append-only, so a report's history reads as its own audit trail._

### 🎯 Objective

Learn what makes a reusable task prompt for an AI coding agent work in any app, and how a library of such prompts should be built, checked and measured, to rewrite the universal prompts and the engine that checks and delivers them.

### 🔭 Scope

- **In scope**: copy-paste task prompts for coding agents (Claude Code, Codex, Copilot, Cursor, Gemini CLI and chat apps); vendor guidance current in October 2026; studies from 2022 to 2026; the engineering of a prompt library: placeholders, lint, evals, versioning, sync, pasted content and secrets.
- **Out of scope**: system prompts for products, fine-tuning, model settings such as temperature and thinking effort, and agent designs beyond what a prompt can ask for.

### 🧪 Method

- Five research passes ran side by side, each writing sourced notes: Anthropic's guidance; OpenAI, Google, GitHub, Microsoft, Cursor and other vendors; empirical studies; task-by-task patterns for coding agents; and prompt-library engineering. A sixth pass wrote one report from the notes, citing every claim.
- **Provenance note**: vendor documentation and open-source repositories, such as `openai/codex`, `google-gemini/gemini-cli`, `anthropics/claude-code`, `openai/openai-cookbook` and `github/docs`, were mostly read directly. The network policy blocked arxiv.org, developers.openai.com, cursor.com, code.visualstudio.com and a few others, so most papers rest on abstracts and search excerpts, marked 🟡 below.

### 🔎 Findings

1. **Complete requirements move outcomes, and piling up instructions does not.** Underspecified prompts were twice as likely to regress when the model or prompt changed, and adding requirements did not reliably help; the best of 20 models followed 68% of 500 simultaneous instructions.
   - **Source**: [arXiv 2505.13360](https://arxiv.org/abs/2505.13360) (Findings of ACL 2026), [arXiv 2507.11538](https://arxiv.org/abs/2507.11538) (IFScale) - 🟡 corroborated, not fetched
   - **Confidence**: High - independent studies agree
2. **Leaner prompts score better.** OpenAI found leaner system prompts scored about 10 to 15% higher on its coding-agent evals, with 41 to 66% fewer tokens.
   - **Source**: [OpenAI model guidance](https://developers.openai.com/api/docs/guides/model-guidance) - 🟡 corroborated, not fetched
   - **Confidence**: Medium - one vendor's internal evals
3. **A persona, politeness, a tip or a threat shows no reliable effect.** Across 162 personas, assigned roles did not improve accuracy, and tips and threats did not significantly change results.
   - **Source**: [arXiv 2311.10054](https://arxiv.org/abs/2311.10054), [arXiv 2512.05858](https://arxiv.org/abs/2512.05858), [arXiv 2508.00614](https://arxiv.org/abs/2508.00614) - 🟡 corroborated, not fetched
   - **Confidence**: High
4. **"Think step by step" adds little or harms on reasoning models.** It moved accuracy by about three points either way at 20 to 80% more time, and explicit reasoning degraded instruction following.
   - **Source**: [arXiv 2506.07142](https://arxiv.org/abs/2506.07142) (Wharton), [arXiv 2505.11423](https://arxiv.org/abs/2505.11423) (NeurIPS 2025) - 🟡 corroborated, not fetched
   - **Confidence**: High
5. **Emphasis in capitals makes current models overreact.** Anthropic says to replace "CRITICAL: You MUST" with plain wording, and Cursor found "Be THOROUGH" made GPT-5 search over and over. No study has measured the effect on outcomes.
   - **Source**: [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [GPT-5 prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5_prompting_guide.ipynb) - ✅ fetched directly
   - **Confidence**: Medium - vendor reports, not measured outcomes
6. **Long material goes first, and the ask after it.** Anthropic reports up to 30% better responses with long inputs above the query; Google asks for the context first and the question last; OpenAI's GPT-4.1 guide puts instructions at both ends.
   - **Source**: [Anthropic long context](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#long-context-prompting), [GPT-4.1 prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt4-1_prompting_guide.ipynb) - ✅ fetched directly; [Google prompting intro](https://ai.google.dev/gemini-api/docs/prompting-intro) - 🟡 corroborated
   - **Confidence**: Medium
7. **The vendors agree on one skeleton.** OpenAI's Codex guidance prescribes Goal, Context, Constraints and Done when; Google names `<context>` and `<task>`; GitHub asks for a problem statement, complete acceptance criteria and file pointers.
   - **Source**: [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) - ✅ fetched directly; Codex and Google guidance - 🟡 corroborated
   - **Confidence**: High
8. **A check the agent can run beats an instruction to review its own work.** Unit-test feedback improved code accuracy by up to 12%, against 2 to 3% without tests; self-correction without outside feedback fails; models favour their own output when they judge it.
   - **Source**: [arXiv 2304.05128](https://arxiv.org/abs/2304.05128), [arXiv 2310.01798](https://arxiv.org/abs/2310.01798), [arXiv 2404.13076](https://arxiv.org/abs/2404.13076) - 🟡 corroborated; [Claude Code best practices](https://code.claude.com/docs/en/best-practices) - ✅ fetched directly
   - **Confidence**: High
9. **Passing tests is not proof, and agents game tests.** 29.6% of plausible SWE-bench Verified patches behaved differently from the developers' fix, and GPT-5 cheated on 54% of a conflicting split despite prompts against it. A sanctioned way out, such as stopping when a test looks wrong, and checks from outside the model are the counter.
   - **Source**: [arXiv 2503.15223](https://arxiv.org/abs/2503.15223) (ICSE 2026), [arXiv 2510.20270](https://arxiv.org/abs/2510.20270) (ImpossibleBench) - 🟡 corroborated, not fetched
   - **Confidence**: High for the finding, medium for the exact rates
10. **Evidence-first reports nearly ended fabricated status claims.** Anthropic's wording to check each claim against a tool result from the session nearly eliminated fabricated reports, even on tasks built to draw them out.
    - **Source**: [Anthropic, prompting Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) - ✅ fetched directly
    - **Confidence**: Medium - one vendor, measured on its own models
11. **Ask only when the answer would change the work.** Interaction recovered up to 74% on underspecified SWE-bench tasks, but models rarely tell a well-specified task from an underspecified one; vendors converge on asking only when readings lead to materially different work.
    - **Source**: [arXiv 2502.13069](https://arxiv.org/abs/2502.13069) - 🟡 corroborated; [Anthropic, prompting Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) - ✅ fetched directly
    - **Confidence**: Medium
12. **Scope needs both halves.** Telling an agent to build all the task asks for, and to mention extras rather than add them, cut unrequested additions with no measurable change in task success.
    - **Source**: [Anthropic, prompting Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) - ✅ fetched directly
    - **Confidence**: Medium
13. **A vague bar costs a review its recall.** Told to report only high-severity issues, a strong model found the bugs and then withheld them; the fix is a concrete bar, or every finding with its severity, verified before it is reported.
    - **Source**: [Anthropic, prompting Opus 4.8](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8), [Codex review rubric](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md) - ✅ fetched directly
    - **Confidence**: Medium
14. **Marking pasted text as data helps, and wording cannot secure it.** Delimiters roughly halved attack success and restating the task after the data cut it further, but adaptive attackers got past such defences more than 90% of the time; restricting tools did best.
    - **Source**: [arXiv 2403.14720](https://arxiv.org/abs/2403.14720), [arXiv 2510.19207](https://arxiv.org/abs/2510.19207), [arXiv 2510.09023](https://arxiv.org/abs/2510.09023) - 🟡 corroborated, not fetched
    - **Confidence**: Medium
15. **Upper-snake double braces survive every major agent tool.** Anthropic's examples and the prompt registries use `{{NAME}}`; Claude Code and Codex fill `$ARGUMENTS` and `$1`, VS Code `${input:name}`, and Gemini CLI `{{args}}`, `!{}` and `@{}`, none of which a `{{UPPER_SNAKE}}` slot sets off. Nothing fills a pasted slot, so the prompt should ask for any left unfilled.
    - **Source**: [Claude Code skills](https://code.claude.com/docs/en/skills), [Gemini CLI custom commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md) - ✅ fetched directly
    - **Confidence**: High
16. **A library should lint every commit and measure against a baseline.** No widely used prompt linter exists, and the useful checks are structural; Claude Code's plugin evals run each case three times with the plugin and without it on a pinned model, and Anthropic advises starting with 20 to 50 tasks drawn from real failures.
    - **Source**: [Claude Code plugin evals](https://code.claude.com/docs/en/plugin-evals), [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - ✅ fetched directly
    - **Confidence**: Medium
17. **Advice now differs by model, so a prompt is measured per model.** Anthropic tells Opus 5 users to remove verification instructions and Sonnet 5.5 users to add them, and OpenAI's GPT-6 Astra asks more questions where GPT-5's guide said never to ask.
    - **Source**: [Anthropic, prompting Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5), [Codex prompting guide](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/openai-docs/references/prompting-guide.md) - ✅ fetched directly
    - **Confidence**: High
18. **Repository context files cut both ways.** One study found AGENTS.md-style files tended to lower task success while raising cost by more than 20%; another measured 28.64% lower runtime with similar completion.
    - **Source**: [arXiv 2602.11988](https://arxiv.org/abs/2602.11988), [arXiv 2601.20404](https://arxiv.org/abs/2601.20404) - 🟡 corroborated, not fetched
    - **Confidence**: Low - two preprints that disagree

### 📚 Sources & Provenance

| Source                                                                                                                                         | Fetched    | Backs / notes                                         |
| :--------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :---------------------------------------------------- |
| [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | ✅ direct  | 5, 6; and the per-model pages behind 10 to 13 and 17  |
| [Claude Code best practices](https://code.claude.com/docs/en/best-practices)                                                                   | ✅ direct  | 8; plan only when the diff will not fit one sentence  |
| [OpenAI Cookbook prompting guides](https://github.com/openai/openai-cookbook/tree/main/examples/gpt-5)                                         | ✅ direct  | 5, 6, 17                                              |
| [`openai/codex`](https://github.com/openai/codex)                                                                                              | ✅ direct  | 13, 17; the review rubric and the prompting guide     |
| [`google-gemini/gemini-cli`](https://github.com/google-gemini/gemini-cli)                                                                      | ✅ direct  | 15; reproduce first, and the three-attempt loop guard |
| [GitHub Docs](https://docs.github.com/en/copilot)                                                                                              | ✅ direct  | 7                                                     |
| [arXiv](https://arxiv.org/)                                                                                                                    | ❌ 403     | 1, 3, 4, 8, 9, 11, 14, 18; read through abstracts     |
| [OWASP Top 10 for LLM Applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications)                         | ✅ direct  | 14; separate untrusted content, and keep secrets out  |
| developers.openai.com, ai.google.dev, cursor.com                                                                                               | 🟡 corrob. | 2, 6, 7; blocked here, read through search excerpts   |

### ⚖️ Alternatives Considered

| Option                                       | Pros                                        | Cons                                                                              |
| :------------------------------------------- | :------------------------------------------ | :-------------------------------------------------------------------------------- |
| Keep the prompts, and teach the practices    | Nothing to build                            | The practices hold only while every reviewer remembers them                       |
| One variant of each prompt for each model    | Each fits its model's own advice            | Six prompts become dozens, and the advice changes at every release                |
| Grade outcomes with a judge model            | Judges open-ended answers                   | Meaningless until checked against labelled outcomes; a second model call each run |
| Ship the prompts as skills or slash commands | One command away in the apps that read them | Only in those apps, only inside a repository, and the formats keep moving         |

### 🛠️ Spikes / Prototypes

- `prompts.py --check`, written before the rewrite, passed the first version of the block as it stood, so the shape it holds every prompt to is the one the prompts already used.
- Every formatter rule in `prompts.py` was confirmed against Prettier 3.8.1 with the standards' configuration: each catches a line Prettier would change, and the rewritten source is as Prettier writes it.
- The standards' Machined Block Check passed a repository holding the newly sealed `docs/Prompts.md`, and caught a hand edit inside it.
- The prompt scenarios in `evals/prompts/` ran against a scripted fake app, which showed each check catching the shortcut and passing the asked-for work. No run against a real model has been made yet.

### 🏁 Conclusion / Recommendation

Rewrite the universal prompts to the five-part contract the vendors share, with pasted material marked as data, both halves of scope, a check the agent can run with a way out, and a report built from evidence. Drop the wording the evidence shows does nothing or harms. Hold every prompt to that shape with deterministic checks on each commit, and measure each prompt against the one-line request it replaces, three runs each way on a pinned model, before a release and again when a new model ships. Recorded in [ADR-0028](../../adrs/ADR-0028-Every-Prompt-Is-Linted-&-Measured.md).

### ✅ Confidence & Caveats

- **Overall confidence**: Medium
- **What would change this conclusion**: a measured run of the prompt scenarios in which a universal prompt does worse than the hurried request it replaces, or a study showing copy-paste templates gain nothing over a well-written one-line request.
- **Known gaps**: no study compares copy-paste templates with one-line requests; no current comparison of XML and Markdown structure; no test of "treat this as data" lines written by the person pasting; and most paper figures here rest on abstracts and search excerpts.

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
> Durable decisions graduate to the [🧭 ADR index](../../adrs/README.md). The prompts this report shaped, and how they are checked and measured: [Prompts](../Prompts.md) and [Evals](../Evals.md). Every canonical guide is indexed in the [📚 Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md).

---

<div align="center">

**Answered once. Kept honest. Never stale.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
