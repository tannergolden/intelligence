<!--
title: '🛡️ SCOPE & BOUNDARIES'
description: 'What may live in this repository, what never may, and the reasoning behind each exclusion so it is argued with rather than forgotten.'
tags: [scope, boundaries, governance, portability]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🛡️ SCOPE & BOUNDARIES

<a name="top"></a>

**Every file added here is paid for again in every repository it lands in.**

_Argued for once. Argue with it, never drift past it._

</div>

---

## 🎯 The Four Rules

1. **Law is universal, or it is not law.** No rule in `AGENTS.md` may depend on a capability some supported tool lacks, or on a fact only one repository can vouch for. The law is byte-identical in repositories with different languages, branch models and review policies, so it can only contain what is true across all of them.
2. **Carriers are vendor-specific and carry nothing.** `CLAUDE.md` and `GEMINI.md` are envelopes. They are permitted to differ precisely because they hold no content that could drift from the law or contradict it.
3. **Supported means a named surface, tested.** Not a product. Copilot's coding agent reads the law by default and its JetBrains client reportedly does not, and both are called Copilot. A tool nobody tested is incidental, which is welcome and is not a promise.
4. **Nothing executes on clone.** No hooks, no `settings.json`, no plugin manifest, no MCP configuration. A skill bundling `scripts/` is the single boundary crossing, and the checker reports it every time.

---

## ✅ What Lives Here

| Path              | Why it earns its place                                                                 |
| :---------------- | :------------------------------------------------------------------------------------- |
| `AGENTS.md`       | The law. The only file with rules in it                                                |
| `CLAUDE.md`       | Claude Code has no discovery path for `AGENTS.md`, verified by probe                   |
| `GEMINI.md`       | Gemini CLI discovers only `GEMINI.md` unless a settings file says otherwise            |
| `skills/.unpackaged/` | The second product. One canonical copy per skill, installed rather than synced      |
| `.github/`        | The skill gate, a stub calling the shared CI, and `CODEOWNERS`                          |
| `docs/`           | These documents                                                                        |
| `Makefile`        | The standardized task entry point. The shared CI resolves `lint-docs` here and nowhere else |
| `scripts/`        | What the Makefile invokes. Inert until someone runs it, so rule 4 holds                |
| `LICENSE`         | Output copied into other repositories with no licence is unusable by anyone but its author |

> [!NOTE]
> **`Makefile` and `scripts/` do not breach rule 4.** Nothing here runs on clone: `make` is invoked deliberately, by a person or by CI. That is the whole difference between a task runner and a git hook, and it is why one is permitted and the other is not.

---

## 🚫 What Never Lives Here

Each row is a decision, not an oversight. That is the point of writing them down.

| Excluded                                        | Because                                                                                                                                        |
| :---------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `.claude/`, `.gemini/` config directories       | They are the vendor config layer. Shipping one reopens executable content on clone and gives law a second place to hide                        |
| Hooks and `settings.json`                       | A committed hook is arbitrary code execution on clone, and Claude Code runs project hooks in headless sessions with no prompt                   |
| `.claude-plugin/plugin.json`, marketplaces      | Claude-only. Gemini's equivalent is `gemini-extension.json`, user-scope only, with no repository-declared install and manual updates            |
| `.github/copilot-instructions.md`               | Copilot's coding agent and CLI read `AGENTS.md` natively, so a copy would be a second file holding law                                          |
| MCP configuration                               | No standard, four forked formats, written by vendor UIs, and every tool gates project MCP behind a per-developer prompt anyway                  |
| Per-tool rule and command dialects              | Each reaches exactly one supported tool, and none is law                                                                                        |
| A build step, emitters, a `payload/` directory  | The emit set is three root markdown files this repository wants at its own root regardless. A compiler whose output equals its input is overhead |
| A local-law injection region                    | The law now tells agents to find a repository's own context wherever it lives, so there is nothing left to inject                               |
| Committed skill archives                        | Build output nobody can review in a diff. The release builds them from source and attaches them to the release page instead |
| `SECURITY.md`                                   | GitHub serves it from the owner's `.github` repository for every repository lacking one. A copy here would override that with a second one to keep current |
| A copy of the styling specification             | It is followed by link. `scripts/check-docs.py` encodes the subset a machine can decide and names the upstream document as the source |

---

## ⚖️ How To Add Something

> [!IMPORTANT]
> **The test is not "is this useful?" It is "does every supported tool get value from it, and does the repository still uninstall cleanly?"** A file that helps one vendor and is inert in the other two is a file that makes the repository behave differently depending on who showed up.

Three questions, in order:

1. **Is it law?** Then it goes in `AGENTS.md` and it must hold in any repository. If it cannot, it is not law; it belongs in the consuming repository's own context.
2. **Is it a capability?** Then it is a skill, and [Skill Authoring](Skill-Authoring.md) governs it.
3. **Is it neither?** Then it is probably vendor configuration, and rule 4 applies.

A rule that varies by repository cannot live in a file that is byte-identical in every repository. That single sentence resolves most arguments about what belongs in the law.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

Most exclusions above trace to a measurement rather than a preference, and those are in [Vendor Facts](Vendor-Facts.md).

---

<div align="center">

**Additive, deletable, and inert. Anything else needs an argument.**

[↑ Back to Top](#top)

</div>
