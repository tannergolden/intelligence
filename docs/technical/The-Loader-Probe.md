<!--
title: '🧪 THE LOADER PROBE'
description: 'How the hub proves, on the machine that runs it, which instruction files each AI coding app actually loads, what it touches, and the results so far.'
type: guide
-->

<div align="center">

# 🧪 THE LOADER PROBE

<a name="top"></a>

**Every claim about where an app looks, checked on the machine that relies on it.**

_A code cannot be guessed. An app that reports one has read the file._

</div>

---

## 💡 Why It Exists

The plan rests on claims about where each app looks for its instructions,
gathered from documentation and source code. Apps change where they look
without notice, so the probe checks every claim on the machine that will rely
on it, before anything is built on top.

**It plants a random twelve-character code in each file an app should read,
then asks the app, headless, which codes its instructions define.** A code
cannot be guessed, so an app that reports one has loaded the file that holds
it.

| Value          | Planted in                                  | Expected                                                  |
| :------------- | :------------------------------------------ | :-------------------------------------------------------- |
| `PROBE_REPO`   | A scratch git repository's root `AGENTS.md` | Every app reads it                                        |
| `PROBE_HOME`   | The home copy in each app's own folder      | Every app with a home copy reads it                       |
| `PROBE_MASTER` | `~/.agents/AGENTS.md`                       | No app reads it, so the kit's copies can never load twice |

---

## 🎯 What It Checks

| App             | Command                                     | Home copy it should read                                     |
| :-------------- | :------------------------------------------ | :----------------------------------------------------------- |
| Claude Code     | `claude -p`, with its file tools disallowed | `~/.claude/rules/intelligence-probe.md`                      |
| Codex           | `codex exec --sandbox read-only`            | A marked block in `~/.codex/AGENTS.md`                       |
| Antigravity CLI | `agy -p`                                    | A marked block in `~/.gemini/AGENTS.md`                      |
| Copilot CLI     | `copilot -p --trust-folder`                 | `~/.copilot/instructions/intelligence-probe.instructions.md` |
| Grok Build      | `GROK_FOLDER_TRUST=0 grok -p`               | Claude Code's copy, which it reads by default                |
| Cursor CLI      | `cursor-agent -p`                           | None: Cursor's User Rules are pasted by hand                 |

Every flag that decides whether instructions load is set explicitly, because
headless runs skip them silently in documented cases. **Controls check those
cases, and each expects the repository's `AGENTS.md` to be skipped unless
stated:**

| Control                                              | Expected                       |
| :--------------------------------------------------- | :----------------------------- |
| Claude Code beside a `CLAUDE.md`                     | Skips `AGENTS.md`              |
| Claude Code beside a `CLAUDE.md`, reading both       | Reads it, through `--settings` |
| Claude Code beside a `CLAUDE.local.md`               | Skips `AGENTS.md`              |
| Claude Code beside a `CLAUDE.local.md`, reading both | Reads it, through `--settings` |
| Grok Build in an untrusted folder                    | Skips `AGENTS.md`              |

If your own Claude settings already read both files, the two Claude controls
expect `AGENTS.md` to load, and their labels say so.

**The skill canary, with `--skills`.** The home kit installs each skill as a
copy in three folders, which is safe only if every app sees exactly one copy.
The canary plants one skill name in each folder, each copy with its own code,
and asks every app which copies it can see:

| App                   | The copy it should see, and no other              |
| :-------------------- | :------------------------------------------------ |
| Claude Code           | `~/.claude/skills/`                               |
| Codex and Copilot CLI | `~/.agents/skills/`                               |
| Antigravity CLI       | `~/.gemini/antigravity-cli/skills/`               |
| Grok Build and Cursor | Either `~/.agents/skills/` or `~/.claude/skills/` |

VS Code reads both of those folders and has no headless mode, so check it by
hand with `--keep --skills`.

---

## 🚀 Running It

From the root of the hub:

```bash
python3 .github/scripts/loader-probe.py --dry-run     # show the plan, change nothing
python3 .github/scripts/loader-probe.py               # every installed app
python3 .github/scripts/loader-probe.py --apps claude,grok
python3 .github/scripts/loader-probe.py --skills      # add the skill canary
python3 .github/scripts/loader-probe.py --keep        # set up a check by hand
python3 .github/scripts/loader-probe.py --cleanup     # undo --keep, or a crash
```

It needs Python 3.9 or later and git, and nothing else. Each check is one model
call: twelve in a full run, and one more per app with `--skills`, on your own
subscriptions. An app installed under
another name takes `--command`, which must keep the `{prompt}` slot:

```bash
python3 .github/scripts/loader-probe.py --apps codex --command "codex=codex-beta exec {prompt}"
```

**Checking by hand.** Copilot in VS Code and the Cursor editor have no headless
mode. `--keep` writes the same files and fixtures, prints the question and the
codes a correct answer names, and leaves everything in place until
`--cleanup`.

---

## 🛡️ What It Touches

- **Nothing it did not create is ever overwritten.** A file the probe would own
  that already exists stops the run.
- **Your own files keep every byte.** In `~/.codex/AGENTS.md`,
  `~/.gemini/AGENTS.md` and `~/.agents/AGENTS.md`, the probe appends a marked
  block and keeps an exact backup.
- **Every change is written down before it is made**, in
  `~/.cache/intelligence-probe/manifest.json`, and undone newest first when
  the run finishes, fails or is stopped with Ctrl-C, `SIGTERM` or `SIGHUP`.
- **A run that dies anyway leaves its manifest behind.** The next run refuses
  to start until `--cleanup` replays it.
- **Results stay on your machine**, in
  `~/.cache/intelligence-probe/results-<time>.json`, with each app's version
  and its raw answer.

---

## 📊 Results So Far

| Date       | App         | Version | Where                       | Result             |
| :--------- | :---------- | :------ | :-------------------------- | :----------------- |
| 2026-10-17 | Claude Code | 2.1.302 | Linux, Claude cloud session | 5 of 5 checks pass |

The Claude Code run, as the probe printed it:

| Check                                              | PROBE_REPO | PROBE_HOME | PROBE_MASTER | Result |
| :------------------------------------------------- | :--------- | :--------- | :----------- | :----- |
| Claude Code                                        | read       | read       | not read     | pass   |
| Claude Code beside a CLAUDE.md                     | not read   | read       | not read     | pass   |
| Claude Code beside a CLAUDE.md, reading both       | read       | read       | not read     | pass   |
| Claude Code beside a CLAUDE.local.md               | not read   | read       | not read     | pass   |
| Claude Code beside a CLAUDE.local.md, reading both | read       | read       | not read     | pass   |

Add a row for each machine and app as it runs. Phase 0 is done when every app
you use has one that passes, headless and by hand.

---

## 🔬 Its Own Tests

```bash
python3 .github/scripts/test_loader_probe.py
```

They run whole probes against a fake app and a throwaway home folder, and
check every write and restore to the byte. They never call a real model and
never touch your home folder.

---

## 🔗 See Also

- [ADR-0002](../adrs/ADR-0002-One-Root-AGENTS-File.md): one root `AGENTS.md` per repository, which the probe proves every app reads
- [ADR-0005](../adrs/ADR-0005-Home-Copies-Not-Links.md): home files are copies, which the probe proves each app loads
- [The Home Kit](The-Home-Kit.md): the copies the probe stands in for

---

<div align="center">

**Every claim checked on the machine that relies on it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
