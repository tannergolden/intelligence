<!--
title: '🧰 SKILLS'
description: 'The skills the home kit installs into every AI coding app, each a folder in the open Agent Skills format.'
type: index
-->

<div align="center">

# 🧰 SKILLS

<a name="top"></a>

**Procedures an agent loads only when the task in front of it needs them.**

_Every skill written here, for any repository._

</div>

---

## 💡 What This Folder Is For

The skills the home kit installs, one folder each in the open Agent Skills
format, every one written here and universal, each with the team it
dispatches in its own `agents/`.
Where they land and the rules every skill here follows: [Skills &
Subagents](../../docs/technical/Skills-&-Subagents.md).

---

## 🤖 Running The Workforce As Grok Bot Agents

The Agent Resources workforce in [`board/agents/`](board/agents/) can also
run as standing bots in the Grok Bot app: one bot for each agent, one group
chat for each department, and the Chief of Staff in every group to carry
messages between them. The Chief of Staff also keeps your own knowledge
repository, made from the
[knowledge template](https://github.com/tannergolden/knowledge), current.

### Which File Makes Each Bot

Each bot is made from that agent's own file, not from a `SKILL.md`. A
`SKILL.md` is a whole skill's procedure: [`board/SKILL.md`](board/SKILL.md)
tells one agent how to convene the workforce, and no bot needs it when the
departments run as their own groups.

| Grok Bot piece   | Comes from                                                                                                                                                                                               |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The bot's name   | The agent's `title`, which is also its file name, such as `Account Executive`. Agents have no personal names                                                                                             |
| Its main job     | The agent's `description`                                                                                                                                                                                |
| Its instructions | The body of `board/agents/<title>.md`, followed by [`board/references/workforce.md`](board/references/workforce.md), the rules every agent follows                                                       |
| A group          | One department roster, `board/agents/<department>.md`: the group is named for the roster's `title`, such as `Sales & Revenue (S&R)`, and holds every agent in its `members`, the starred lead among them |
| The orchestrator | [`board/agents/Chief of Staff.md`](board/agents/Chief%20of%20Staff.md), with `workforce.md` and [`board/references/write-gate.md`](board/references/write-gate.md) added to its instructions             |
| Where records go | Your knowledge repository's `AGENTS.md`, whose "Where the skills write" section names each folder                                                                                                        |

### Setting It Up

1. **Make your knowledge repository.** On GitHub, choose **Use this
   template** on tannergolden/knowledge and create a **private** repository.
   It will hold your personal context, so it must never be public.
2. **Create the Chief of Staff first.** Give it its instructions from the
   table, and give it, and no other bot, access to your knowledge
   repository.
3. **Create each department.** For each of the 14 rosters, create one bot
   for each member, then a group named after the department, and add those
   bots and the Chief of Staff to it. The Chief of Staff is already a member
   of Administration.
4. **Talk to the workforce.** Bring a request to the department that owns
   it, or to the Chief of Staff when you are not sure which one does.

### How Messages Move

- A department's agents talk within their own group. No agent messages
  another department; the Chief of Staff carries the message, restated so
  it makes sense without the other group's conversation.
- When two departments disagree, the Chief of Staff takes both answers to
  the Chief Executive Officer in Administration, and never picks one itself.
- Only the Chief of Staff writes to your knowledge repository: decisions,
  deliverables and the commitments they create, in the folders its
  `AGENTS.md` names. Every other agent composes its work and hands it back.
- Moving money, signing or sending a contract, sending anything outside
  the company, deleting a file, and changing equity all wait for you to
  confirm in the conversation. No bot does them on its own.

### Group Sizes

Each department keeps at most six agents, its lead included, and `kit.py`
refuses a roster with more. With the Chief of Staff added, the groups are:

| Group                        | Department's agents | With the Chief of Staff |
| :--------------------------- | :-----------------: | :---------------------: |
| Administration               |          4          |    4, it is a member    |
| Business Intelligence (BI)   |          3          |            4            |
| Client Experience (CX)       |          3          |            4            |
| Finance & Accounting (F&A)   |          3          |            4            |
| Human Resources (HR)         |          2          |            3            |
| Information Security         |          1          |            2            |
| Information Technology (IT)  |          3          |            4            |
| Legal & Compliance (L&C)     |          4          |            5            |
| Operations & Logistics (O&L) |          4          |            5            |
| Product Technology           |          1          |            2            |
| Public Relations (PR)        |          3          |            4            |
| Quality Assurance (QA)       |          2          |            3            |
| Research & Development (R&D) |          5          |            6            |
| Sales & Revenue (S&R)        |          6          |            7            |

> [!WARNING]
> **Check the app's group limit before you build Sales & Revenue.** Reports
> on Grok Bot's early beta say a group chat holds two to six bots, and do
> not say whether one bot can sit in several groups. If both hold, Sales &
> Revenue, at six agents plus the Chief of Staff, does not fit, and the
> Chief of Staff could not sit in every group. Confirm both in the app.

### Keeping The Bots Current

The files here are the source; each bot is a copy. When an agent's file,
`workforce.md` or `write-gate.md` changes here, paste the new text into that
bot. When a roster gains or loses a member, add or remove that bot in its
department's group.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                      | Purpose                                                                                                             |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| [`board/`](board/)         | Founds and runs a company with the Agent Resources workforce, at most six agents a department, behind a write-gate. |
| [`develop/`](develop/)     | Builds, tests and ships every other skill, and the agents and teams they dispatch.                                  |
| [`discover/`](discover/)   | Generates options from distinct lenses and ranks them fairly, with the Discovery team.                              |
| [`editorial/`](editorial/) | Writes, edits and formats prose, with the Editorial team.                                                           |
| [`finance/`](finance/)     | Advises on personal and household money, with the Finance team.                                                     |
| [`identify/`](identify/)   | Interviews the user with validated frameworks into a profile they approve line by line.                             |
| [`research/`](research/)   | Runs multi-source, fact-checked research, with the Research team and the Librarian.                                 |
| [`visualize/`](visualize/) | Makes charts, diagrams and other visuals, with the Design team.                                                     |
| [`README.md`](README.md)   | This file.                                                                                                          |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**Load the procedure when the task calls for it, and only then.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
