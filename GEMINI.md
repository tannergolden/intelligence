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

**Gemini CLI looks only for this filename, so this file imports the law.**

_The name the tool looks for, pointing at the file that matters._

</div>

---

## 💡 Why This File Exists

`GEMINI.md` is the only context filename Gemini CLI discovers on its own. Reading `AGENTS.md` instead is possible, but only by committing a settings file that configures it, and a config file is a second place for behavior to live. A router is cheaper and cannot fail silently.

**It carries no law of its own.** It cannot drift from the canonical file, cannot contradict it, and cannot go stale, because there is nothing in it to drift. Every rule lives in one place. If you came here looking for a rule, it is not here.

Like the file it imports, this one is **published rather than authored here** and is overwritten in full on the next sync, so a local edit is a change that will be silently reverted. In the repository that publishes it, it is the source.

This file becomes deletable the day Gemini CLI discovers the canonical filename by default. That is an open request upstream, not a promise.

---

## 📝 The Import

@./AGENTS.md

---

<div align="center">

**A different filename over the same single source of law.**

[↑ Back to Top](#top)

</div>
