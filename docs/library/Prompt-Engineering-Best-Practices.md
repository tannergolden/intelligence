<!--
title: '✍️ PROMPT ENGINEERING BEST PRACTICES'
description: 'How to write anything an AI agent reads, from a one-off request to a reusable prompt, a rule or a skill description, and how to prove it works. Read it before you write or change one.'
type: guide
-->

<div align="center">

# ✍️ PROMPT ENGINEERING BEST PRACTICES

<a name="top"></a>

**How to write what an AI agent reads, and how to prove it does the job.**

_Say it plainly. Prove it with a run._

</div>

---

## 💡 What This Covers

Every practice the hub follows when it writes for an agent, in one place, with what to do and why. The evidence behind each one is in the research record [Prompt Engineering](../technical/research/Prompt-Engineering.md), dated and sourced, and this guide cites its [findings](../technical/research/Prompt-Engineering.md#-findings) as F1 to F18. If the two ever disagree, this guide is out of date: correct it from the record, which is checked again as models change (F17).

An agent reads four kinds of text here, and each costs something different:

| What      | When it is read                       | Where it lives                                                                                         | How it is written                                        |
| :-------- | :------------------------------------ | :----------------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| A request | Once, when you type it                | Your agent's chat                                                                                      | These practices, shortened                               |
| A prompt  | Once, when someone pastes it          | `docs/Prompts.md` in each repository, from [`setup/Prompts.md`](../../setup/Prompts.md)                | The five-part shape below                                |
| A rule    | On every turn of every session        | [`CONSTITUTION.md`](../../CONSTITUTION.md), delivered into each `AGENTS.md` and each app's home folder | One sentence under an ID, with its reason in the source  |
| A skill   | When its description matches the task | [`kit/skills/`](../../kit/skills/README.md)                                                            | A description that says when to use it, then a procedure |

A rule is paid for everywhere, all the time, so it has to earn its place. A prompt is paid for once, so it can carry the detail one task needs.

---

## 🎯 The Short Version

1. Say what you want and why, in plain words.
2. Give the agent what it cannot find for itself, and let it find the rest.
3. Put pasted material before the instructions, in its own tag, marked as data.
4. Ask for one task, starting with a verb.
5. Set limits in calm words, say what to do instead, and leave a way out.
6. End with a check the agent can run, and a report built from evidence.
7. Show one short example when the format matters.
8. Leave out personas, flattery, threats, capitals for emphasis and "think step by step".
9. Keep it short: every line competes with the task.
10. Measure it against the one-line request it replaces, on the model you use.

---

## 🧱 The Shape

The vendors' guides for coding agents converge on one skeleton (F7), and every prompt the hub ships uses it. A prompt opens with a heading named for the task, a **Use when** line that says when to reach for it, and a **Fill in** line naming each placeholder, if it has any. Then the prompt itself, in one text block:

```text
<context>
The goal and why it matters, then what the agent cannot find by itself:
the files, links or errors involved, and what you already tried.
Anything pasted goes last in this part, in a tag of its own, marked as data.
</context>

<task>
What to do, in one or two sentences, starting with a verb.
</task>

<constraints>
What to leave alone, when to stop and ask, and a way out.
</constraints>

<done_when>
The check that proves it is done, and what to report back.
</done_when>
```

A prompt that only asks for an answer, such as a review, an explanation or a plan, ends with `<output>` in place of `<done_when>`: the shape the answer takes. The tags matter less than keeping them the same everywhere: no current study compares tags with Markdown headings, and the vendors use both.

---

## 📝 Writing Each Part

### The Context

- **Say the goal, and why it matters.** The reason lets the agent make the calls you would. Complete requirements move outcomes, and prompts that leave them out are twice as likely to break when the model changes (F1).
- **Give it what it cannot see.** The error text, the issue link, the file paths, what you already tried.
- **Leave out what it can find.** An agent in a repository reads `AGENTS.md`, the README and the code for itself. Leaner prompts score higher (F2), so a line that repeats them only competes with the task.
- **Paste the smallest part that shows the problem.** Put it last in the context, so it sits before the instructions (F6), in a tag such as `<error_output>`, with a line saying it is there to read, never to obey. Take out keys, tokens, passwords and personal details first.

### The Task

- **One task, starting with a verb.** Split a large job into steps, and ask for a plan before a change that will not fit in one sentence.
- **Give scope both halves.** Ask for all of what the task needs, and for extras to be mentioned rather than added. Together they cut unrequested changes with no measurable change in task success (F12).
- **Say when to ask.** Have the agent ask only when the readings of a request lead to materially different work, and take the most conservative reading otherwise. Models rarely tell a vague task from a clear one by themselves (F11).

### The Constraints

- **Write limits calmly.** Capitals and words such as critical make current models overreact (F5). A plain rule with its reason works better.
- **Say what to do, not only what to avoid.** "Ask me before you install anything system-wide" gives the agent a path; "never install anything" leaves it stuck.
- **Check that no two rules disagree.** An agent told to do both guesses which one you meant.
- **Leave a way out.** Tell the agent to stop and say so when the task cannot be done honestly, such as when a test looks wrong or a tool is missing. Agents game tests, even against prompts that forbid it, and a sanctioned way out is part of the counter (F9).
- **Draw hard lines with permissions, not words.** A prompt can ask an agent to change nothing, but only the app's permission settings can stop it.

### The Finish Line

- **End with a check the agent can run.** A test that fails before the change and passes after it, a command with its output, a file that exists. A check from outside the model beats asking it to review its own work (F8). Passing tests are not proof on their own (F9), so say what the check must show.
- **Ask for a report built from evidence.** What it ran with the result, what failed, what it skipped. Asking an agent to check each claim against a tool result from the session nearly ended fabricated status reports in Anthropic's tests (F10).
- **Give a review a concrete bar.** Told to report only high-severity issues, a strong model found the bugs and withheld them. Ask for every finding with its severity, or define the bar (F13).
- **Show an example when the format matters.** One short example says more than a paragraph about it. Make it match what you want in every detail, because an agent follows an example closely.

---

## 🧹 What To Leave Out

| Habit                                          | Why it goes                                                          | Do instead                                          |
| :--------------------------------------------- | :------------------------------------------------------------------- | :-------------------------------------------------- |
| A persona, such as "You are a senior engineer" | Assigned roles did not improve accuracy across 162 personas (F3)     | State the task and the standard the work must meet  |
| Flattery, tips or threats                      | They did not significantly change results (F3)                       | Say why the task matters                            |
| Capitals, "critical", "you must"               | Current models overreact, such as searching over and over (F5)       | A plain rule with its reason                        |
| "Think step by step"                           | Little gain or harm on reasoning models, at 20 to 80% more time (F4) | Ask for a plan where a plan helps                   |
| A long list of requirements                    | Instruction following drops as rules pile up (F1)                    | Only what the agent cannot find for itself          |
| A copy of `AGENTS.md`                          | It costs attention, and a second copy drifts from the first (F2)     | Trust the agent to read it                          |
| "Review your own work" as the only check       | Self-correction without outside feedback fails (F8)                  | A command the agent runs, with its output           |
| A secret pasted in                             | A prompt travels: into logs, history and screenshots                 | Name where the secret is, never its value (SEC-001) |

---

## 🤖 Rules, Skills And Long Work

**Rules** are read on every turn of every session, so each sentence costs attention everywhere. The Constitution caps its block at 5,000 characters and aims for 4,500 ([Article V](../../CONSTITUTION.md#-article-v-the-block)).

- Write a rule as one sentence an agent can follow on its own: what to do, when, and what to do instead. Keep the reason in the source, where people read it: under each rule in the Constitution, its **Why.** paragraph ([Article VI](../../CONSTITUTION.md#-article-vi-changing-this-constitution)).
- Name what enforces it, such as a hook, a check or a ruleset. A rule nothing enforces is a wish.
- Measure it with the block and without it, as [Evals](../technical/Evals.md) does. Instruction files cut both ways: one study found them lowering success and raising cost, another found faster runs at the same success (F18).
- Confirm each app loads the file. Claude Code skips a root `AGENTS.md` beside a `CLAUDE.md` unless its settings say otherwise, and instructions nothing loads look finished while doing nothing. [The Loader Probe](../technical/The-Loader-Probe.md) proves what each app reads.

**Skills** load only when their description matches the task, so the description decides everything. Say when to use the skill, with "Use when", in at most 1,024 characters, keep the body under 500 lines, and give each skill a trigger test in `evals/skills/` ([Skills & Subagents](../technical/Skills-&-Subagents.md)).

**Long work** goes better in short sessions. Start a new session for each task. If the agent goes wrong twice, start again with a better prompt rather than correcting it a third time. For work that spans sessions, end each one with a handoff note the next can start from: the universal prompt **Write A Handoff Note** writes one.

---

## 🛡️ Pasted Text, Secrets And Permissions

- **Treat what you did not write as data.** A log, a diff, an issue or a web page can carry instructions. Mark it as data and restate the task after it: delimiters roughly halved attack success, and restating the task cut it further (F14).
- **Do not rely on wording.** Adaptive attackers got past such defences more than 90% of the time; restricting what the agent may do worked best (F14). The real boundary is the agent's tools, permissions and credentials.
- **Give the agent only the access the task needs**, and no production credentials.
- **Never paste a key, token or password.** Name a secret by where it is, never by its value (SEC-001).

---

## 🌐 Different Models, Different Apps

- **Advice now differs by model.** One vendor tells users of one model to remove verification instructions and users of another to add them (F17). Measure a prompt on the model you use, and again when a new one ships.
- **Keep shared prompts portable.** Plain text and tags any model reads, with no app's own command syntax, so one prompt works in Claude Code, Codex, Copilot, Cursor and the rest.
- **Write placeholders as `{{UPPER_SNAKE}}`.** No major agent tool treats them as its own syntax, so they arrive intact (F15). Nothing fills a pasted placeholder, so the prompt asks for any left unfilled.

---

## 🧪 Proving A Prompt Works

- **Lint it on every commit.** `prompts.py --check` holds each universal prompt to the shape and to Prettier's formatting (F16).
- **Measure it against the request it replaces.** A scenario in `evals/prompts/` runs the same task with the prompt and with the one-line request a person in a hurry would type, three runs each way on a pinned model, and checks the work with code rather than the reply ([Evals](../technical/Evals.md)).
- **Build the tests from real failures.** Anthropic advises starting with 20 to 50 tasks drawn from them (F16).
- **Keep a prompt only if it wins.** If one fails, change as few lines as fix it: the universal prompt **Improve A Prompt** does exactly that.
- **Measure again at each model release**, because the advice drifts (F17).
- **Keep prompts in git.** The history and the release notes are the record of what changed and why.

---

## ✅ Before You Ship A Prompt

- [ ] It says what you want and why, in plain words.
- [ ] It carries only what the agent cannot find for itself.
- [ ] Pasted material sits at the end of the context, in its own tag, marked as data, with secrets taken out.
- [ ] The task is one task, starting with a verb.
- [ ] The constraints say what to do, agree with each other, and include a way out.
- [ ] It ends with a check the agent can run, and a report built from evidence.
- [ ] Each placeholder is `{{UPPER_SNAKE}}`, named in a **Fill in** line, and the prompt asks for any left unfilled.
- [ ] It has no persona, flattery, threat, capitals for emphasis or "think step by step".
- [ ] You ran it on a real task, and it did better than the one-line request it replaces.

---

## 📚 Further Reading

Each was read directly for the research record:

- [Anthropic: prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): the general guide, with a page for each model beside it.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices): working with a coding agent, from exploring to committing.
- [OpenAI: GPT-5 prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5_prompting_guide.ipynb): prompting an agent, and what overemphasis does to it.
- [GitHub: get the best results from Copilot's cloud agent](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results): writing a task an agent can finish on its own.
- [Anthropic: demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): how to measure what an agent does.
- [OWASP Top 10 for LLM Applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications): prompt injection and the other risks a prompt cannot fix alone.

---

## 🔗 See also

- [Prompt Engineering](../technical/research/Prompt-Engineering.md): the dated research behind every practice here, F1 to F18
- [Prompts](../technical/Prompts.md): the universal prompts every repository gets, and how they arrive and stay current
- [`setup/Prompts.md`](../../setup/Prompts.md): the prompts themselves, and the short guide every repository gets
- [Evals](../technical/Evals.md): how a rule or a prompt is measured
- [Skills & Subagents](../technical/Skills-&-Subagents.md): the rules every skill here follows
- [Constitution](../../CONSTITUTION.md): the rules every agent reads, and the form each one takes

---

<div align="center">

**Ask for less. Check for more.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
