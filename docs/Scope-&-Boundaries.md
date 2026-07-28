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
4. **Everything that executes is delivered deliberately, bounded, and gated.** This rule used to read "nothing executes on clone", and it was amended when the skill router was added. What replaced it is not weaker, it is specific: executable content ships only where it earns its place, and nothing ships without a gate measuring what it costs. No plugin manifest, no MCP configuration, and no hook that has not been priced. The [amendment](#-what-changed-in-rule-4-and-why) below records what was given up.

---

## ✅ What Lives Here

| Path              | Why it earns its place                                                                 |
| :---------------- | :------------------------------------------------------------------------------------- |
| `AGENTS.md`       | The law. The only file with rules in it                                                |
| `CLAUDE.md`       | Claude Code has no discovery path for `AGENTS.md`, verified by probe                   |
| `GEMINI.md`       | Gemini CLI discovers only `GEMINI.md` unless a settings file says otherwise            |
| `skills/.unpackaged/` | The second product. One canonical copy per skill, installed rather than synced. `develop` authors them; `improve` is the feedback loop |
| `.github/`        | The workflows, and `CODEOWNERS`                                                        |
| `actions/`        | The one published composite action, at the same path the sibling publisher uses        |
| `.claude/`, `.gemini/` | The skill router, one per vendor, delivered and gated. See the rule 4 amendment below |
| `docs/`           | These documents                                                                        |
| `Makefile`        | The standardized task entry point. The shared CI resolves `lint-docs` here and nowhere else |
| `scripts/`        | Both checkers. What the Makefile invokes, and what `actions/` reaches up two levels for |
| `LICENSE`         | Output copied into other repositories with no license is unusable by anyone but its author |

> [!NOTE]
> **`Makefile` and `scripts/` are not the executable content rule 4 is about.** `make` is invoked deliberately, by a person or by CI, and neither is delivered anywhere. The hooks are the delivered executable content, and they are the reason rule 4 now talks about bounding rather than forbidding.

---

## 🚫 What Never Lives Here

Each row is a decision, not an oversight. That is the point of writing them down.

| Excluded                                        | Because                                                                                                                                        |
| :---------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Law inside `.claude/` or `.gemini/`             | Those directories now carry a skill router and nothing else. The moment one holds a rule, the law has a second place to hide and the envelopes stop being envelopes |
| Any hook whose output is not measured           | A hook fires on every prompt, so its output is charged on every turn. One that nothing measures is an unbounded recurring cost with no owner    |
| `.claude-plugin/plugin.json`, marketplaces      | Claude-only. Gemini's equivalent is `gemini-extension.json`, user-scope only, with no repository-declared install and manual updates            |
| `.github/copilot-instructions.md`               | Copilot's coding agent and CLI read `AGENTS.md` natively, so a copy would be a second file holding law                                          |
| MCP configuration                               | No standard, four forked formats, written by vendor UIs, and every tool gates project MCP behind a per-developer prompt anyway                  |
| Per-tool rule and command dialects              | Each reaches exactly one supported tool, and none is law                                                                                        |
| A build step, emitters, a `payload/` directory  | The emit set is three root markdown files this repository wants at its own root regardless. A compiler whose output equals its input is overhead |
| A local-law injection region                    | The law now tells agents to find a repository's own context wherever it lives, so there is nothing left to inject                               |
| Committed skill archives                        | Build output nobody can review in a diff. The release builds them from source and attaches them to the release page instead |
| `SECURITY.md`                                   | GitHub serves it from the owner's `.github` repository for every repository lacking one. A copy here would override that with a second one to keep current |
| A copy of the styling specification             | It is followed by link. `scripts/check-docs.py` encodes the subset a machine can decide and names the upstream document as the source |
| A vendored copy of `standards` in this tree      | A consuming repository may pin one as a submodule, which is a pin rather than a copy. This repository is the publisher's peer and reads it by link |

---

## 📜 What Changed In Rule 4, And Why

Rule 4 read **"Nothing executes on clone. No hooks, no `settings.json`."** It was argued for, it held for the life of the repository, and it was amended deliberately to ship the skill router. That is the shape this document asks for: argue with it, do not drift past it.

**What the old rule was protecting, and it was right about all of it:**

| Risk | Still true? |
| :--- | :--- |
| A committed hook is code execution somebody did not opt into | **Yes.** Verified: a `UserPromptSubmit` hook ran in a headless session with no prompt at all |
| Its output is unbounded | **Yes.** Verified: 15,024 characters passed through untruncated |
| It fires on every prompt, so any cost recurs forever | **Yes** |

**What changed is not the risk, it is that the risk is now bounded and visible.** The router prints **nothing** when no skills are installed, so a repository that ignores the feature pays exactly zero. When skills are present it prints their names and stops, and [`check-docs.py`](../scripts/check-docs.py) fails the build if that exceeds 256 bytes against a three-skill fixture, or if the script is not valid shell, or if it prints nothing when skills exist. Both failure modes were mutation-tested rather than assumed.

**What was genuinely given up, stated plainly:**

- **Clone is no longer inert.** Receiving these files means receiving a script that runs unprompted. That is a real cost and no gate removes it.
- **Gemini re-prompts on every change.** Gemini CLI fingerprints project hooks and treats a changed command as new and untrusted, so a sync that alters the hook asks the user to approve it again.
- **There are two implementations, not one.** Claude Code and Gemini CLI share no hook event names: `UserPromptSubmit` against `BeforeAgent`, `PreToolUse` against `BeforeTool`. The two routers are siblings, not translations, and both have to be maintained.

**What would reverse it:** if the router turns out not to improve skill selection, it should go. The mechanism it supplements already exists, since every skill's description is loaded at startup whether the router runs or not, and the documented fix for a skill that never fires is a better description rather than a louder reminder. This is the one part of the repository whose value is asserted rather than measured.

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

**Additive and deletable. Anything that also executes has to argue for itself.**

[↑ Back to Top](#top)

</div>
