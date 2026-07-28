<!--
title: '🤖 GEMINI CLI ROUTER'
description: 'Imports the canonical agent instructions for Gemini CLI, whose only automatically discovered context filename is this one.'
tags: [agent-instructions, gemini-cli, router, envelope]
category: agents
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🤖 GEMINI CLI ROUTER

<a name="top"></a>

**Gemini CLI discovers this filename and nothing else unless it is configured to, so this file imports the canonical one.**

_The name the tool looks for, pointing at the file that matters._

</div>

---

## 💡 Why This File Exists

`GEMINI.md` is the only context filename Gemini CLI discovers on its own. Reading `AGENTS.md` instead is possible, but only by committing a settings file that configures it, and a config file is a second place for behaviour to live. A router is cheaper and cannot fail silently.

**It carries no law of its own.** It cannot drift from the canonical file, cannot contradict it, and cannot go stale, because there is nothing in it to drift. Every rule lives in one place. If you came here looking for a rule, it is not here.

This file becomes deletable the day Gemini CLI discovers the canonical filename by default. That is an open request upstream, not a promise.

---

## 📝 The Import

@./AGENTS.md

---

<div align="center">

`scope: gemini cli` &middot; `contains: no law`

**A different filename over the same single source of law.**

[↑ Back to Top](#top)

</div>
