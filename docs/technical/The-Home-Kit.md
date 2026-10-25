<!--
title: '🏠 THE HOME KIT'
description: 'What make agents installs into each AI app''s home folder, the kit that rides beside the rules, the guard hook, and how a machine gets them from a release.'
type: guide
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

| Folder        | Universal rules                                                              | Setting                                                                                                                                                   |
| :------------ | :--------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `~/.agents/`  | `AGENTS.md`, the master copy every other copy is checked against             | none                                                                                                                                                      |
| `~/.claude/`  | `rules/intelligence.md`; in a Claude cloud session, `CLAUDE.md` instead      | `instructionFiles: claude-md-and-agents-md`, so AGENTS.md loads beside a CLAUDE.md; and `permissions.ask` rules, [below](#-asking-before-outward-actions) |
| `~/.codex/`   | A marked block in `AGENTS.md`, so your own text stays                        | none                                                                                                                                                      |
| `~/.gemini/`  | `AGENTS.md`, which Antigravity CLI reads natively                            | none                                                                                                                                                      |
| `~/.copilot/` | `instructions/intelligence.instructions.md`, with `applyTo: "**"`            | none                                                                                                                                                      |
| `~/.grok/`    | Nothing: Grok Build reads `~/.claude` by default, so a copy would load twice | none                                                                                                                                                      |
| `~/.cursor/`  | Nothing to write: paste the home file into Cursor's User Rules once          | none                                                                                                                                                      |

Copies, not links: links fail silently in Claude's desktop sessions and Grok's
sandbox, and would take over files you keep notes in. `make agents-check`
compares every copy with the release, and `make agents-uninstall` puts back
what was there before. In a Claude cloud session, [the setup
script](Cloud-Setup.md) does the same from a pinned release, and can never
stop the session from starting. A cloud session gets no `instructionFiles`
setting, ask rules or compaction reminder: only `CLAUDE.md`, and the kit's
guard, skills and subagents.

---

## 🧩 The Kit

The kit rides beside the rules in the same release, as one pinned file,
`home/kit.json`, and the installer puts each piece where its app reads it:

| Module                                       | What it is                                                                                                                             | Where it lands                                                                                                                                                                                  |
| :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guard hook, below                            | Denies force-pushes, merges, `--no-verify`, AI sign-offs, irreversible commands, credential reads and unread downloads before they run | `~/.agents/hooks/`, registered in Claude Code's settings (read by Grok and Cursor), Codex's and Antigravity's `hooks.json`, and Copilot's `hooks/`; Claude Code also runs it after a compaction |
| [`develop`](Skills-&-Subagents.md)           | The one skill: builds, tests and ships every other skill, and the agents and teams they dispatch                                       | `~/.agents/skills/`, `~/.claude/skills/` and Antigravity's skills folder                                                                                                                        |
| [Worker and Reviewer](Skills-&-Subagents.md) | Subagents that make one change, and check one without editing                                                                          | `~/.claude/agents/`, `~/.copilot/agents/` and `~/.codex/agents/`                                                                                                                                |

Everything the kit writes carries its mark, so it replaces only its own files
and `make agents-uninstall` takes back exactly what it added. A file that is a
symlink, as dotfiles often make `~/.claude/settings.json`, is written through,
so it stays a link to the file the dotfiles keep.

---

## 🛡️ The Guard Hook

[`kit/guard.py`](../../kit/guard.py) is the one script behind every
app's pre-tool hook. Each app pipes the tool call it is about to make to it,
and it either stays silent or denies the call with exit 2 and one line saying
why and what to do instead. It never allows and never asks, so each app's own
permissions decide everything else.

| Rule      | What it denies                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| OPS-001   | Pushing to a default or protected branch, force-pushing without `--force-with-lease`, deleting or pruning remote refs, pushing tags, and merging a pull request through `git`, `gh` or a GitHub MCP tool. Its owner lifts it for a Claude Code session by typing `override OPS-001` in a repository tannergolden owns, which the guard reads only from what the user typed                                                                                                                                                                                                                                                                                                                                                                                                                  |
| OPS-003   | What git cannot undo, when there is something to lose: a hard reset or whole-tree checkout over uncommitted work, `git clean -f`, dropped stashes, history rewrites, and deleting data or settings. A recursive delete of a root, drive or home folder counts in every spelling: `rm -r`, and on Windows `rmdir /s`, `rd /s`, `del /s` and `Remove-Item -Recurse` with its aliases                                                                                                                                                                                                                                                                                                                                                                                                          |
| OPS-004   | `--no-verify`, hooks switched off for one command, and edits that would remove the guard or its registrations, the compaction reminder included, or drop one of the kit's ask rules from Claude Code's settings                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| GIT-001   | A commit git would author, or sign off, as an AI's identity                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| SEC-001   | A credential-shaped string in a command or in a file being written. Reading a credential store in the home folder, by a read tool or by a command that prints, searches, archives or copies one: private keys under `~/.ssh` and `~/.gnupg`, `~/.aws/credentials`, gcloud's credential files, Azure's tokens, `~/.docker/config.json`, `~/.kube/config`, `~/.netrc`, `~/.git-credentials`, `~/.npmrc`, `~/.pypirc`, `~/.cargo/credentials`, `~/.gem/credentials` and `~/.config/gh/hosts.yml`. And a command that prints a credential: `gh auth token`, `gh auth status --show-token`, `git credential fill`, `aws configure get` of a secret, `aws configure export-credentials`, `gcloud auth print-access-token`, `az account get-access-token`, and `security find-generic-password -w` |
| SEC-004   | A download a shell or an interpreter runs before anyone reads it: piped in, as in `curl ... \| sh` or `iwr ... \| iex`; fed in, as in `bash <(curl ...)`, `sh < <(curl ...)` or `bash <<< "$(curl ...)"`; substituted in, as in `sh -c "$(curl ...)"` or `eval $(curl ...)`; or saved and run in the same line, as in `curl -o i.sh ... && bash i.sh`. And a package install that names a registry other than the public default, on the command line or in a variable set for it: `npm install --registry`, `pip install --index-url`, `uv add --index`, `cargo add --registry`, `PIP_INDEX_URL=...` and their like                                                                                                                                                                        |
| DOC-002   | An em dash added to a Markdown file, a commit message, or a pull request's title or body through `gh` or the GitHub MCP server, in a repository tannergolden owns: one with no remote yet, or whose every remote is on github.com under tannergolden, so never a fork. A `DOC-002` entry under `## Overrides` in the repository's `AGENTS.md` turns it off there                                                                                                                                                                                                                                                                                                                                                                                                                            |
| The block | A hand edit inside the block the hub renders, the rules in `AGENTS.md`, which the next sync would overwrite anyway; a repository's `docs/Prompts.md` is all its own                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

It reads a command the way a careful reviewer would, so it catches the honest
mistake and a determined workaround gets past it: the rulesets and CI stay the
real gates. In Codex and Antigravity, a guard that cannot start lets the call
through. To see what it would say about one command:

```bash
python3 kit/guard.py --command 'git push --force origin main'
```

A few of its checks draw a careful line:

- **A credential store** is the file itself. Under `~/.ssh`, a public key,
  `config*`, `known_hosts*`, `authorized_keys*`, `environment`, `rc`, a
  `*.conf` file and anything in a `*.d` folder pass, as do `ssh-keygen -l`
  and a project's own `.env`. Searching, archiving or copying a folder that
  holds a store, such as `grep -r ~/.ssh`, `tar czf aws.tgz ~/.aws` or
  `cp -r ~/.ssh`, counts as reading the store. `rg` and `ag` skip hidden
  folders, so for them the home folder counts only with `--hidden`.
- **A pattern is not a file.** The first operand of `grep`, `rg`, `sed`,
  `awk` or `jq` is its pattern, script or filter unless a flag gives it, and
  a `cd` earlier in the line moves the commands after it, on cmd and
  PowerShell's side too. So a session started in the home folder can run
  `grep -rn ".netrc" code/` or `cd code/app && cat .netrc`.
- **A download** may be saved to a file, or read as data by `jq`, `grep` or
  `python3 -c`. Only a shell or interpreter that runs it as code in the same
  command line is denied: save it in one command, and run it in another once
  your user agrees. `iex` counts only as a command, never inside quoted text,
  so a commit message that names it passes. The public default registries,
  `https://registry.npmjs.org`, `https://pypi.org/simple`,
  `https://rubygems.org` and crates.io, may be named outright.
- **The em dash** counts only in Markdown, commit messages and pull
  requests, and only when a change adds one, so code, data and an edit that
  keeps an older one pass. If your user asked for the dash, a `DOC-002` entry
  under `## Overrides` in the repository's `AGENTS.md` turns the check off
  there. Outside a git repository, and in a fork, the guard says nothing
  about it. It does not see a dash a shell writes, through a here-document,
  `sed -i` or `>>`, a message `git commit -F` reads from a file, or the body
  of `gh pr comment` or `gh pr review`.

Claude Code sends its `Read` calls to the guard too, so it can deny reading a
credential store. That costs about 75 ms per read, measured in a cloud
container, almost all of it Python starting and loading the script. `Grep` and
`Glob` stay out, since every search would pay the same. Copilot and
Antigravity send every call, and a search tool among them counts as `rg`
does: a store's folder is denied, the home folder is not. Codex reads files
through its shell.

---

## ✋ Asking Before Outward Actions

OPS-005 lets an agent push, open a pull request, comment or publish only when
your user asked for that action. On a machine's own install, not in a cloud
session, the installer adds Claude Code `permissions.ask` rules to
`~/.claude/settings.json`, so Claude Code asks your user before each one in
every permission mode, auto and `bypassPermissions` included, and denies it in
`dontAsk` mode:

| Action                                   | Rules                                                                                                                                                                                                                                                                                                                                                               |
| :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A push                                   | `Bash(git push *)`                                                                                                                                                                                                                                                                                                                                                  |
| A pull request, drafts too               | `Bash(gh pr create *)`, `Bash(gh pr edit *)`, `Bash(gh pr ready *)`, `Bash(gh pr close *)`, and the GitHub MCP server's `create_pull_request`, `update_pull_request` and `update_pull_request_branch`                                                                                                                                                               |
| A comment, review or issue               | `Bash(gh pr comment *)`, `Bash(gh pr review *)`, `Bash(gh issue create *)`, `Bash(gh issue edit *)`, `Bash(gh issue close *)`, `Bash(gh issue comment *)`, and the MCP server's comment, review, issue and thread tools                                                                                                                                             |
| A release                                | `Bash(gh release create *)`, `Bash(gh release upload *)`, `Bash(gh release edit *)`                                                                                                                                                                                                                                                                                 |
| A repository, fork, gist or workflow run | `Bash(gh repo create *)`, `Bash(gh repo fork *)`, `Bash(gh gist create *)`, `Bash(gh workflow run *)`                                                                                                                                                                                                                                                               |
| A write through `gh api`                 | A method of `POST`, `PATCH`, `PUT` or `DELETE`, by `-X` or `--method`, as in `Bash(gh api *-X*POST*)`; or a field or body flag, `-f`, `-F`, `--field`, `--raw-field` or `--input`, after a REST path under `repos/`, as in `Bash(gh api repos/* -f *)`; or a GraphQL mutation, `Bash(gh api graphql *mutation*)`. A GraphQL query, which reads, runs without asking |
| A published package                      | `npm`, `pnpm` and `yarn publish`, `yarn npm publish`, `cargo publish`, `twine upload`, `gem push` and `docker push`                                                                                                                                                                                                                                                 |
| A change made straight on GitHub         | The MCP server's `create_or_update_file`, `push_files`, `delete_file`, `create_branch`, `create_repository`, `fork_repository` and `actions_run_trigger`                                                                                                                                                                                                            |

The full list is `ASK_RULES` in the installer, and the guard holds the same
list: it denies an edit to `~/.claude/settings.json` that drops one of them
(OPS-004). A rule your user already has is never added twice, and
`make agents-uninstall` takes out only the rules the kit added, which the
install record lists. A rule whose one `*` ends it after a space, such as
`Bash(gh pr create *)`, also matches the bare command, `gh pr create`. A `*`
anywhere else matches anything, so each `gh api` rule finds its flag wherever
it stands, and a GraphQL query sent with `-f` asks too. A rule matches a
command as it is usually typed, so `git -C . push` gets past it; the guard
still denies the pushes and merges OPS-001 forbids, in any spelling. The MCP
rules name the server `github`, so a GitHub server added under another name
needs its own.

An ask rule wins over an allow rule and asks in every mode, so a headless
`claude -p` run, with no one to answer, cannot push or open a pull request:
the call is denied. To let one through, run the session interactively, or
answer the prompt with a `PermissionRequest` hook or a
`--permission-prompt-tool` that decides as your user would.

---

## 🔁 After A Compaction

When Claude Code compacts a long conversation, it runs each `SessionStart`
hook whose matcher is `compact` and adds what the hook prints to the
compacted context. On a machine's own install, the installer registers one
that runs the guard as `intelligence-guard.py --remind`, which prints a line
saying these rules still hold after compaction, the precedence line for
Invariants, and the Invariants, from `~/.claude/rules/intelligence.md`. It
prints nothing when that copy is missing or holds no block.

The guard protects this registration as it protects its own: an edit that
drops it is denied (OPS-004), and `make agents-uninstall` takes it out. To see
what it prints:

```bash
python3 ~/.agents/hooks/intelligence-guard.py --remind
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
- [Troubleshooting The Home Kit](../operations/Troubleshooting-The-Home-Kit.md): what each status of the installer, its check and the guard means

---

<div align="center">

**The same rules in every app, on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
