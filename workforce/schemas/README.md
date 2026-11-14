<!--
title: '🧾 SCHEMAS'
description: 'The workforce''s portable machine formats: the tools every agent may call, and the envelope every message carries.'
type: index
-->

<div align="center">

# 🧾 SCHEMAS

<a name="top"></a>

**The two formats an orchestrator needs to run the workforce outside a chat app.**

_Neutral here. Wrapped per API when rendered._

</div>

---

## 💡 What This Folder Is For

[`tools.json`](tools.json) defines each tool once, in the neutral shape OpenAI, xAI, Anthropic, Gemini and MCP all accept, and `workforce.py render --target bundle --flavor ...` wraps it for one of them. [`message.schema.json`](message.schema.json) is the envelope an orchestrator validates every message against. How both are used: [The Workforce](../../docs/technical/The-Workforce.md).

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                        | Purpose                                                                                                                                                                                                                 |
| :------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`message.schema.json`](message.schema.json) | The envelope every workforce message carries, as a JSON Schema an orchestrator validates each message against: who sends it to whom, what it asks, when it is due, whether it waits on the owner, and the task's state. |
| [`README.md`](README.md)                     | This file.                                                                                                                                                                                                              |
| [`tools.json`](tools.json)                   | The workforce's portable tools, in the neutral shape every API wraps its own way: a name, a description and a JSON Schema object of parameters.                                                                         |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Defined once, read by every API.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
