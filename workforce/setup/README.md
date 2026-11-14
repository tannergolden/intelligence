<!--
title: '🚀 SETUP'
description: 'The prompts that set the workforce up, one for each kind of environment, each with the steps the Chief of Staff follows to install it and to keep it current.'
type: index
-->

<div align="center">

# 🚀 SETUP

<a name="top"></a>

**One message turns a session or a Bot into the Chief of Staff, which sets up everyone else.**

_Paste the prompt. The steps are the Chief of Staff's._

</div>

---

## 💡 What This Folder Is For

Each file here holds one prompt, ready to copy, and under it the steps the Chief of Staff follows once it has the prompt: [`Grok Bot.md`](<Grok Bot.md>) for the Grok Bot app, where every agent becomes a Bot, and [`Terminal.md`](Terminal.md) for an app that runs commands, on a machine or in a cloud session. Each also says how the Chief of Staff brings every copy up to date when the workforce changes.

`workforce.py check` holds each prompt to the hub's prompt shape, and `test_workforce.py` holds the copies in [The Workforce](../../docs/technical/The-Workforce.md), which adds what the owner does in each app, equal to these.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                          | Purpose                                                                                                                                                                                                                                                                     |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`Grok Bot.md`](<Grok Bot.md>) | Sets the workforce up in the Grok Bot app: the prompt that turns the primary Bot into the Chief of Staff, the steps it follows to create every other Bot, the department groups and its weekly check, how it brings them up to date, and the approval rules the owner adds. |
| [`README.md`](README.md)       | This file.                                                                                                                                                                                                                                                                  |
| [`retired.json`](retired.json) | Titles the workforce no longer has, each with the seat that took over its work, or an empty string when its work was split among several.                                                                                                                                   |
| [`Terminal.md`](Terminal.md)   | Sets the workforce up where an app can run commands, on a machine or in a cloud session: the prompt that turns a session into the Chief of Staff, and the steps it follows to check, install and initialize the workforce and to bring every installed copy up to date.     |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Set up once, by the agent that runs it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
