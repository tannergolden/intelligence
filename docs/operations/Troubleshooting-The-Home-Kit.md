<!--
title: '🩺 TROUBLESHOOTING THE HOME KIT'
description: 'What the installer, its check, the Claude cloud setup script and the guard hook print when something on a machine is wrong, and what to do about each. Read it when make agents-check is not all current, a cloud session starts without the rules, the guard blocks a call, or Claude Code asks before an action.'
type: guide
keywords: [install, agents-check, cloud-setup, guard, dotfiles, uninstall]
-->

<div align="center">

# 🩺 TROUBLESHOOTING THE HOME KIT

<a name="top"></a>

**What a machine's copies, its cloud sessions and its guard say when something is off.**

_Every status has a cause, and most have one command._

</div>

---

## 💡 Where To Look

- **dotfiles' `make agents-check`** runs the installer's `check` against the
  pinned release: one line per file, its status first. Any status but
  `current` fails it, apart from a `warning` and the `manual` line, and
  `make agents` is the fix for most of them.
- **dotfiles' `make agents`** runs `install`, which prints the same lines with
  `wrote`, `current` or `refused`, and exits 1 when it refused anything.
- **The install record**, `~/.local/state/intelligence/install.json`, holds
  what `make agents-uninstall` needs to put each file back: whether the kit
  created it, the separator it put before a block, the earlier value of
  Claude Code's `instructionFiles` setting, and the ask rules the kit added
  to Claude Code's `permissions.ask`.
- **A cloud session's setup script** prints each problem as a line that starts
  `intelligence:`, and still exits 0, so the session starts either way.

Every path below is the default; [The Home Kit](../technical/The-Home-Kit.md)
shows where each app's copy lands, and `CODEX_HOME` moves Codex's.

---

## 🔍 What check Says

| Status    | What it means                                                                                                                                                                                                                           | What to do                                                                                                                                              |
| :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `current` | The file matches the release                                                                                                                                                                                                            | Nothing                                                                                                                                                 |
| `missing` | The file, its block, Claude Code's `instructionFiles` setting or one of its ask rules, a guard registration, or the compaction reminder is not there                                                                                    | `make agents`                                                                                                                                           |
| `edited`  | A copy's block no longer matches its marker, a file the kit owns was changed, or a skill folder holds files the kit did not put there                                                                                                   | `make agents`, which writes it again. Keep your own notes outside the markers, and out of the files the kit owns whole                                  |
| `stale`   | A copy's block is from another release, a guard registration differs from the one this release writes, or a retired knowledge block is still there                                                                                      | `make agents`, with the pin you mean to run                                                                                                             |
| `broken`  | A file holds more than one `INTELLIGENCE` block, a hook or settings file is not valid JSON, Claude Code's `permissions` or its `ask` list is in a shape the installer cannot add to, or a guard registration runs a Python that is gone | Delete the extra block, or fix the JSON, by hand. For a Python that is gone, `make agents` registers the guard again with the one that runs the install |
| `foreign` | A file or folder sits where the kit writes one, without the kit's mark                                                                                                                                                                  | The installer never replaces it. Move it aside, then `make agents`                                                                                      |
| `warning` | A shadow: a file that would hide a copy, or load the rules a second time                                                                                                                                                                | Below                                                                                                                                                   |
| `manual`  | Cursor keeps its User Rules in its own settings, where no installer reaches                                                                                                                                                             | Paste the home file into Settings, Rules, User Rules, and again after a release changes the block                                                       |

Three files draw a `warning`, each for its own reason:

| File                          | Why it is named                                                                  |
| :---------------------------- | :------------------------------------------------------------------------------- |
| `~/.codex/AGENTS.override.md` | Codex reads it instead of `~/.codex/AGENTS.md`, so Codex's home copy never loads |
| `~/AGENTS.md`                 | Apps that walk up the folder tree load it in every project under home            |
| `~/CLAUDE.md`                 | Claude Code loads it in every project under home                                 |

Keep one only if you mean it to do that. The install and the check carry on
either way: a warning never fails them.

---

## 📥 What install Says

Each line is `wrote`, `current` or `refused`, or `would write` under
`--dry-run`. A `retired` line means it took out the knowledge facts an older
release wrote, which is expected once. A refusal names its file and why:

| After the file name                                                               | What to do                                                                                                                                                                                                                  |
| :-------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exists and is not the kit's; it is never overwritten`                            | Move your file aside, or fold what you need from it into one the kit does not own, then install again                                                                                                                       |
| `holds more than one INTELLIGENCE block; remove the extra by hand`                | Delete the extra block, then install again                                                                                                                                                                                  |
| `is not valid JSON (...); fix it first, it is never overwritten`                  | Fix that settings or hooks file, such as `~/.claude/settings.json`, then install again                                                                                                                                      |
| `is not a JSON object`, or says a part of the file is not an object or not a list | The same: the file's shape is not one the installer can add to without guessing. When only Claude Code's `permissions` is, the ask rules are refused on their own line and the `instructionFiles` setting is written anyway |
| `holds an "intelligence" hook that is not the kit's`                              | Antigravity's `hooks.json` has a hook of yours under that name: rename it, then install again                                                                                                                               |

Some problems stop the install before it writes anything, because the files it
was given are not a release's:

| The installer says                                                                                                                                    | What to do                                                                           |
| :---------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `... is not a home file: it must be exactly one INTELLIGENCE block`                                                                                   | Pass the release's `intelligence.md`, as downloaded                                  |
| `... was edited: its content does not match the hash in its marker`                                                                                   | Download it again, and check it against its pin                                      |
| `... is a kit in format N; this installer reads format 2`                                                                                             | The kit and the installer come from different releases: take both from one           |
| `cannot read the kit`, `carries a guard without the kit's mark`, `names a skill file outside its folder`, `names a subagent that is not a plain name` | The kit is not one the hub rendered: download it again, and check it against its pin |

---

## ↩️ What uninstall Says

`removed` takes out a file or a folder that is the kit's own, and `restored`
puts a file back as it was before, without the kit's block or hook. Two notes
explain what it leaves:

- `no install record, so only marked blocks and the kit's own files go`: the
  record is gone, so it takes out only what is unmistakably the kit's, and
  every file of yours keeps its text.
- `Claude Code's instructionFiles setting and ask rules were left as they are`:
  without the record it cannot know what the setting was before, or which ask
  rules were yours, so it leaves them all.

A `refused` line during uninstall means a file holds more than one block or is
not valid JSON. Fix it by hand, and run it again.

---

## ☁️ What The Cloud Setup Script Says

Each notice starts `intelligence:`. The session starts whatever it says, and
runs on each repository's own `AGENTS.md`, which carries the same rules.

| The notice says                                                                                 | What to do                                                                                                                           |
| :---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `no release is pinned here yet; run make cloud-setup VERSION=vX.Y.Z in the hub`                 | The hub's copy was pasted, placeholders and all. Paste the output of `make cloud-setup VERSION=vX.Y.Z` instead                       |
| `curl is not installed, so the rules were not installed`, and the same for `python3`            | Install it earlier in the environment's setup                                                                                        |
| `could not make a scratch folder`                                                               | The container could not create a temporary folder: check its temporary directory                                                     |
| `could not download the home file for vX.Y.Z`, or `the installer`                               | Check the version is a real tag, and that the environment can reach `raw.githubusercontent.com`                                      |
| `the home file for vX.Y.Z does not match its pin, so nothing was installed`, or `the installer` | The pins are from another release, or were changed. Print the script again with `make cloud-setup VERSION=vX.Y.Z` and paste it whole |
| `could not download the kit for vX.Y.Z, so only the rules were installed`                       | The rules are in, and the guard, the skills and the subagents are not. Check the network, as for the home file                       |
| `the kit for vX.Y.Z does not match its pin, so only the rules were installed`                   | Print the script again and paste it whole                                                                                            |
| `the installer reported a problem; see above`                                                   | Read the installer's `refused` lines above it, as in [What install Says](#-what-install-says)                                        |

An empty kit pin is no fault: it comes from a release before the kit, and
installs the rules alone. `make cloud-setup` itself stops with
`vX.Y.Z:home/intelligence.md is not in this repository` when your checkout of
the hub does not have that tag: run `git fetch --tags` there first.

---

## 🛡️ When The Guard Blocks A Call

The app shows one line, from the guard:

```text
intelligence guard blocked this (OPS-001): `git push --force` can overwrite commits on the remote. Use --force-with-lease on a branch you created, or ask your user
```

The word in parentheses is the rule it upholds, in the
[Constitution](../../CONSTITUTION.md), or `machine-written block` for an edit
inside a block the hub renders. The sentence after it says what to do instead.

- **To see what it says about a command**, run
  `python3 ~/.agents/hooks/intelligence-guard.py --command '<command>'`, or
  `python3 kit/guard.py --command '<command>'` in the hub. It prints `allowed`,
  or the denial.
- **It reads only an agent's tool calls**, through each app's pre-tool hook. A
  command you type in your own terminal never reaches it, so when it stops
  something you do want, such as a merge, run it yourself.
- **A block edit it denies** is one the next sync would overwrite anyway.
  Change the rule in `CONSTITUTION.md` and release it; a repository's own text
  goes outside the markers, and its `docs/Prompts.md` is all its own.
- **A DOC-002 denial** comes only in a repository tannergolden owns, and only
  for an em dash the change adds to Markdown, a commit message or a pull
  request; code and data never draw one. Use a comma, colon, parentheses or a
  spaced hyphen. If your user asked for the dash, they can add
  `- DOC-002: <why>` under `## Overrides` in the repository's `AGENTS.md`,
  which turns the check off there.
- **A SEC-004 denial for a download** means a shell or interpreter would run
  it unread, in the same command line. Save it to a file in one command, show
  your user what it would run, and run it in another once they agree. For a
  registry named on the command line, or in a variable set for one command,
  install from the one the project's configuration names, or ask your user to
  add the new one there; the public default registries pass.
- **A SEC-001 denial for a credential store** names the file, never its
  contents. Let the tool that owns the login use it, such as `gh` or `aws`,
  rather than reading the file. A command that prints a credential, such as
  `gh auth token`, is denied the same way: `gh` and `aws` use theirs without
  printing them. A search that names a pattern, such as
  `grep -rn ".netrc" code/`, passes; one run over a store's folder does not.
- **An OPS-004 denial for an ask rule** means an edit to
  `~/.claude/settings.json` would drop one of the rules the kit added. Leave
  them: `make agents-uninstall` takes them out with the rest of the kit.
- **`intelligence guard: internal error, call allowed: ...`** is a bug in the
  guard. It lets the call through rather than stop every call, so report it
  with the command that caused it.
- **It denies edits that would remove it or its registrations.** To take it
  out, run `make agents-uninstall`, which removes it with the rest of the kit.
- **In Codex and Antigravity, a guard that cannot start lets the call
  through.** `make agents-check` reports a registration whose Python is gone
  as `broken`.
- **After a compaction**, Claude Code runs the guard with `--remind`, which
  prints the Invariants back into the conversation. To see what it prints,
  run `python3 ~/.agents/hooks/intelligence-guard.py --remind`; it prints
  nothing when `~/.claude/rules/intelligence.md` is missing or holds no
  block, and `make agents` puts that copy back.

---

## ✋ When Claude Code Asks First

The ask rules the kit adds make Claude Code ask your user before a push, a
pull request, a comment, a release, a publish, or a write through `gh api`,
as [The Home Kit](../technical/The-Home-Kit.md#-asking-before-outward-actions)
lists them.

- **It asks in every mode.** An ask rule wins over an allow rule, and asks
  even in `bypassPermissions` and auto mode; `dontAsk` mode denies the call
  instead. A rule that ends in a lone ` *`, such as `Bash(git push *)`, also
  matches the bare command, `git push`.
- **A headless `claude -p` run cannot push.** With no one to answer, the
  call is denied. Run the session interactively, or answer the prompt with a
  `PermissionRequest` hook or a `--permission-prompt-tool` that decides as
  your user would.
- **A spelling the rules do not expect gets past them**, such as
  `git -C . push`. The guard still denies the pushes and merges OPS-001
  forbids, in any spelling.

---

## 🔗 See Also

- [The Home Kit](../technical/The-Home-Kit.md): what each copy is, and where it lands
- [Cloud Setup](../technical/Cloud-Setup.md): how the setup script is printed and pasted
- [Commands](../references/Commands.md): every option of the installer and the guard

---

<div align="center">

**A status names the cause. Most causes take one command.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
