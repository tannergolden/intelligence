<!--
title: '🏠 THE HOME KIT'
description: 'What make agents installs into each AI app''s home folder, the kit that rides beside the rules, the guard hook, and how a machine gets them from a release.'
type: guide
keywords: [install, guard, dotfiles]
-->

<div align="center">

# 🏠 THE HOME KIT

<a name="top"></a>

**The rules and their kit in every app's home folder, copied from a pinned release.**

_Copies, not links. Checked against the release, and taken back to the byte._

</div>

---

## 💡 What Gets Installed

`make agents`, in your dotfiles, downloads the pinned release's home file,
kit and installer from [`home/`](../../home/README.md), checks each against
its SHA-256, and runs the installer, which writes byte-identical copies, one
per app, in the shape each app reads:

| Folder        | Universal rules                                                              | Setting                                                                            |
| :------------ | :--------------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `~/.agents/`  | `AGENTS.md`, the master copy every other copy is checked against             | none                                                                               |
| `~/.claude/`  | `rules/intelligence.md`; in a Claude cloud session, `CLAUDE.md` instead      | `instructionFiles: claude-md-and-agents-md`, so AGENTS.md loads beside a CLAUDE.md |
| `~/.codex/`   | A marked block in `AGENTS.md`, so your own text stays                        | none                                                                               |
| `~/.gemini/`  | `AGENTS.md`, which Antigravity CLI reads natively                            | none                                                                               |
| `~/.copilot/` | `instructions/intelligence.instructions.md`, with `applyTo: "**"`            | none                                                                               |
| `~/.grok/`    | Nothing: Grok Build reads `~/.claude` by default, so a copy would load twice | none                                                                               |
| `~/.cursor/`  | Nothing to write: paste the home file into Cursor's User Rules once          | none                                                                               |

Copies, not links: links fail silently in Claude's desktop sessions and Grok's
sandbox, and would take over files you keep notes in. `make agents-check`
compares every copy with the release, and `make agents-uninstall` puts back
what was there before. In a Claude cloud session, [the setup
script](Cloud-Setup.md) does the same from a pinned release, and can never
stop the session from starting.

---

## 🧩 The Kit

The kit rides beside the rules in the same release, as one pinned file,
`home/kit.json`, and the installer puts each piece where its app reads it:

| Module                                       | What it is                                                                                         | Where it lands                                                                                                                                     |
| :------------------------------------------- | :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guard hook, below                            | Denies force-pushes, merges, `--no-verify`, AI sign-offs and irreversible commands before they run | `~/.agents/hooks/`, registered in Claude Code's settings (read by Grok and Cursor), Codex's and Antigravity's `hooks.json`, and Copilot's `hooks/` |
| [`develop`](Skills-&-Subagents.md)           | The one skill: builds, tests and ships every other skill, and the agents and teams they dispatch   | `~/.agents/skills/`, `~/.claude/skills/` and Antigravity's skills folder                                                                           |
| [Worker and Reviewer](Skills-&-Subagents.md) | Subagents that make one change, and check one without editing                                      | `~/.claude/agents/`, `~/.copilot/agents/` and `~/.codex/agents/`                                                                                   |

Everything the kit writes carries its mark, so it replaces only its own files
and `make agents-uninstall` takes back exactly what it added.

---

## 🛡️ The Guard Hook

[`kit/guard.py`](../../kit/guard.py) is the one script behind every
app's pre-tool hook. Each app pipes the tool call it is about to make to it,
and it either stays silent or denies the call with exit 2 and one line saying
why and what to do instead. It never allows and never asks, so each app's own
permissions decide everything else.

| Rule      | What it denies                                                                                                                                                                                           |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OPS-001   | Pushing to a default or protected branch, force-pushing without `--force-with-lease`, deleting or pruning remote refs, pushing tags, and merging a pull request through `git`, `gh` or a GitHub MCP tool |
| OPS-003   | What git cannot undo, when there is something to lose: a hard reset or whole-tree checkout over uncommitted work, `git clean -f`, dropped stashes, history rewrites, and deleting data or settings       |
| OPS-004   | `--no-verify`, hooks switched off for one command, and edits that would remove the guard or its registrations                                                                                            |
| GIT-001   | A commit git would author, or sign off, as an AI's identity                                                                                                                                              |
| SEC-001   | A credential-shaped string in a command or in a file being written                                                                                                                                       |
| The block | A hand edit inside a block the hub renders, which the next sync would overwrite anyway                                                                                                                   |

It reads a command the way a careful reviewer would, so it catches the honest
mistake and a determined workaround gets past it: the rulesets and CI stay the
real gates. In Codex and Antigravity, a guard that cannot start lets the call
through. To see what it would say about one command:

```bash
python3 kit/guard.py --command 'git push --force origin main'
```

---

## 📦 How A Machine Gets It

`home/` holds everything a machine downloads, rendered from the Constitution,
[`kit/`](../../kit/README.md) and the installer's source, and never edited by
hand: `make render` rewrites it, and `make check` fails CI when it has drifted.

| File              | What it is                                                                                                       |
| :---------------- | :--------------------------------------------------------------------------------------------------------------- |
| `intelligence.md` | The home file: the universal block between its `INTELLIGENCE` markers                                            |
| `kit.json`        | The kit: the guard, the skills and the subagents                                                                 |
| `install.py`      | The installer, copied from [`.github/scripts/install.py`](../../.github/scripts/install.py), where its tests run |
| `SHA256SUMS`      | The SHA-256 of the home file, the kit and the installer, for a reader                                            |

A release is a tag, and each tag serves that folder as it was at that commit:

```text
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/home/intelligence.md
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/home/kit.json
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/home/install.py
```

A release from before the installer moved into `home/` serves it at
`scripts/install.py`, and dotfiles, the setup script and `make pins` look
there for such a release ([ADR-0024](../adrs/ADR-0024-The-Hub-Keeps-Its-Template-Layout.md)).

The consumer checks each file against a SHA-256 it pinned beforehand, and
never against a hash from the same download. `make pins VERSION=vX.Y.Z`
prints those pins for a release, and `SHA256SUMS` lists the same hashes for a
reader.

---

## 🔗 See Also

- [ADR-0005](../adrs/ADR-0005-Home-Copies-Not-Links.md): home files are copies, checked against the release
- [ADR-0010](../adrs/ADR-0010-Releases-Serve-Rendered-Files.md): a release tag serves the rendered files, checked against pins
- [ADR-0012](../adrs/ADR-0012-One-Pinned-Kit-For-Every-Module.md): every module ships in one pinned kit beside the rules
- [ADR-0013](../adrs/ADR-0013-The-Guard-Denies-Never-Allows.md): one guard behind every app's hook, which only ever denies
- [ADR-0024](../adrs/ADR-0024-The-Hub-Keeps-Its-Template-Layout.md): the scripts in `.github/scripts/`, the kit's sources in `kit/`, and everything a machine downloads in `home/`

---

<div align="center">

**The same rules in every app, on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
