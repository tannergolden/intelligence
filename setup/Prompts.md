<!--
title: '💬 PROMPTS'
description: 'Ready-made prompts for working in this repository with an AI agent: copy one, fill in its placeholders, and paste it into any AI app.'
type: reference
keywords: [prompts, ai-agents, prompt-engineering]
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 💬 PROMPTS

<a name="top"></a>

**Ready-made prompts for working in this repository with an AI agent.**

_Copy one. Fill it in. Paste it._

</div>

---

<!-- INTELLIGENCE:PROMPTS:BEGIN -->

## 🚀 How To Use A Prompt

1. Find the prompt for your task: a universal one below, or one of this repository's own at the end of this file.
2. Copy it with the button at the top right of its block.
3. Replace every placeholder in double braces, such as `{{ERROR_OUTPUT}}`, with your details, and delete any line that does not apply.
4. Paste it into your AI app. An agent working in this repository also reads its `AGENTS.md`; an app that cannot see the repository needs the files you paste with it.

## 🧰 Universal Prompts

### Fix A Bug

**Use when** something is broken and you can say what you saw. **Fill in** what is broken, what happens, what should happen, how to see it, and the error.

```text
<context>
{{WHAT_IS_BROKEN}} is broken.
What happens: {{WHAT_HAPPENS}}
What should happen: {{WHAT_SHOULD_HAPPEN}}
How to see it: {{STEPS_OR_COMMAND}}
The error, exactly as printed:
{{ERROR_OUTPUT}}
</context>

<task>
Find the cause and fix it with the smallest change that does. Reproduce the bug before you change anything, or tell me why you could not.
</task>

<constraints>
- Fix the cause, not the symptom. Never weaken, skip or delete a test to make it pass.
- Change only what the fix needs.
</constraints>

<done_when>
- A test that failed before the fix passes after it, and every other check still passes.
- You tell me the cause in one or two sentences, what you changed, and what you ran.
</done_when>
```

### Add A Feature

**Use when** you want new behaviour, built and tested. **Fill in** who needs it and why, what it should do, where it belongs, and anything to avoid.

```text
<context>
{{WHO}} needs {{WHAT_IT_SHOULD_DO}}, so that {{WHY}}.
Where it belongs: {{FILES_OR_AREA}}
</context>

<task>
Build it, with tests. If the request reads two ways, ask me before you start. If it touches more than a few files, show me a short plan first and wait for my yes.
</task>

<constraints>
- Follow the conventions of the code around it.
- {{ANYTHING_TO_AVOID}}
</constraints>

<done_when>
- Tests cover the new behaviour and its edge cases, and every check passes.
- You list what you changed, and every assumption you made.
</done_when>
```

### Review My Change

**Use when** a change is ready and you want a careful second look before it merges. **Fill in** what changed, why, and where to find it.

```text
<context>
I changed {{WHAT_CHANGED}} so that {{WHY}}.
The change: {{BRANCH_PULL_REQUEST_OR_DIFF}}
</context>

<task>
Review it the way a careful senior engineer would. Read the diff and the code around it, and run the checks yourself.
</task>

<constraints>
- Report only problems you can point to: the file and line, and what goes wrong.
- Change nothing.
</constraints>

<output>
Findings ranked by severity, each with its evidence and a suggested fix, then anything you could not check. If you find nothing wrong, say so.
</output>
```

### Explain This Code

**Use when** you need to understand part of the code before you change it. **Fill in** what to explain, why, and what you already know.

```text
<context>
I need to understand {{FILE_FUNCTION_OR_FOLDER}} because {{WHY}}.
What I already know: {{WHAT_YOU_KNOW}}
</context>

<task>
Explain what it does, how it does it, and why it is built that way. Read the code before you answer, and never guess about code you have not opened.
</task>

<output>
A short summary first, then the details in the order a newcomer needs them, with file and line references. End with anything that looks surprising or risky.
</output>
```

### Write A New Prompt

**Use when** you keep asking for the same kind of help and want a prompt for it in this file. **Fill in** the task, as roughly as you like.

```text
<context>
I want a reusable prompt for this kind of task: {{ROUGH_REQUEST}}
Read docs/Prompts.md for the shape its prompts take, and AGENTS.md for how this repository works.
</context>

<task>
Write the prompt in the shape docs/Prompts.md describes: a heading, when to use it, what to fill in, and the prompt itself in a text block, with a placeholder in double braces for each detail that changes from one use to the next. If the task is unclear, ask me up to three questions first.
</task>

<done_when>
- The prompt says what to do and why, gives the context an agent cannot find for itself, sets its limits, and says how to tell when it is done.
- It sits under "Prompts For This Repository" in docs/Prompts.md, and nothing else in the file changed.
</done_when>
```

## ✍️ How A Good Prompt Is Written

Every prompt here follows the same practices, and a new one should too:

- **Say what you want, and why.** The reason lets the agent make the calls you would make.
- **Give it what it cannot see.** Name the files, paste the error, link the issue. An agent in this repository reads `AGENTS.md` for itself, so a prompt carries only what is particular to the task.
- **One task per prompt.** Split a large job into steps, and ask for a plan before a big change.
- **Separate the parts.** Tags such as `<context>` and `<task>` keep the background apart from the instructions.
- **Set the limits.** Say what to leave alone, and ask the agent to check with you when a request reads two ways.
- **Say how to tell it is done.** A test that passes, a command's output, a file that exists, and what to report back.
- **Show an example when the format matters.** One good example says more than a paragraph about it.
- **Mark what changes.** Put each detail that changes from one use to the next in a placeholder, so nobody pastes a prompt half filled in.

The shape, ready to fill:

```text
<context>
What the agent cannot find by itself: the goal and why it matters, the files, links or errors involved, and what you already tried.
</context>

<task>
What to do, in one or two sentences, starting with a verb.
</task>

<constraints>
What to leave alone, what to avoid, and when to stop and ask.
</constraints>

<done_when>
The check that proves it is done, and what to report back.
</done_when>
```

<!-- INTELLIGENCE:PROMPTS:END -->

---

## 📌 Prompts For This Repository

_This repository's own prompts go here, in the shape above. 🔁 Intelligence Sync keeps the guide and the universal prompts above current, and never changes this section._

---

<div align="center">

**A better prompt in, better work out.**

[↑ Back to Top](#top)

</div>
