<!--
title: '🗃️ FILES & FORMATS'
description: 'The exact shape of what the hub hands to something else: the markers and their hash, the pin lines, the kit and a subagent source, what a repository carries, and what the tools leave on a machine. Read it before writing a tool that reads one, or before changing the kit.'
type: reference
-->

<div align="center">

# 🗃️ FILES & FORMATS

<a name="top"></a>

**The shape of every file the hub hands to something else, byte for byte.**

_Written down, so no reader has to guess._

</div>

---

## 🏷️ The Markers

Each block the hub renders sits between two comment lines, each alone on its
line, with one blank line between each marker and the block:

```text
<!-- INTELLIGENCE:BEGIN sha256:<64 lowercase hex digits> -->

<the block>

<!-- INTELLIGENCE:END -->
```

| Block              | Markers                                                                    | Where it sits                                                                             |
| :----------------- | :------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| The rules          | `INTELLIGENCE:BEGIN sha256:<hash>`, `INTELLIGENCE:END`                     | `home/intelligence.md`, every home copy, and every repository's root `AGENTS.md`          |
| The prompts        | `INTELLIGENCE:PROMPTS:BEGIN sha256:<hash>`, `INTELLIGENCE:PROMPTS:END`     | Every repository's `docs/Prompts.md`; in `setup/Prompts.md`, unsealed, with no `sha256:`  |
| Knowledge, retired | `INTELLIGENCE:KNOWLEDGE:BEGIN sha256:<hash>`, `INTELLIGENCE:KNOWLEDGE:END` | Beside a home copy, where a release before kit format 2 wrote it; an install takes it out |

**The hash is the SHA-256 of the block's text**: everything between the two
marker lines, read as UTF-8 with CRLF as LF, with the blank lines at either
end taken off and one newline put back at the end. A file holds at most one
block of each kind: sync and the installer refuse a file that holds a second,
and `make audit` reports it. To check a file by hand:

```bash
python3 - AGENTS.md <<'EOF'
import hashlib, re, sys

text = open(sys.argv[1], encoding='utf-8').read().replace('\r\n', '\n')
for name in ('INTELLIGENCE', 'INTELLIGENCE:PROMPTS'):
    pattern = rf'^<!-- {name}:BEGIN sha256:([0-9a-f]{{64}}) -->[ \t]*\n(.*?)^<!-- {name}:END -->'
    for marker, inner in re.findall(pattern, text, re.M | re.S):
        actual = hashlib.sha256((inner.strip('\n') + '\n').encode('utf-8')).hexdigest()
        print(name, 'unedited' if actual == marker else 'edited')
EOF
```

---

## 📦 What A Release Serves

A release tag serves [`home/`](../../home/README.md) as it was at that
commit, and [The Home Kit](../technical/The-Home-Kit.md#-how-a-machine-gets-it)
lists the addresses a consumer downloads from:

| File                   | Shape                                                                                   |
| :--------------------- | :-------------------------------------------------------------------------------------- |
| `home/intelligence.md` | The rules block between its markers, and nothing else                                   |
| `home/kit.json`        | The kit, below                                                                          |
| `home/install.py`      | The installer, byte for byte the same as `.github/scripts/install.py`                   |
| `home/SHA256SUMS`      | One line per file above, `<sha256>  <path>`, two spaces apart, as `sha256sum` prints it |

`make pins VERSION=vX.Y.Z` prints the four lines a consumer pins, the same
names dotfiles' `agents/intelligence.pin` holds:

```text
version=v0.2.0
home_sha256=<sha256 of home/intelligence.md>
install_sha256=<sha256 of home/install.py, or of scripts/install.py in a release from before it moved>
kit_sha256=<sha256 of home/kit.json, or empty for a release from before the kit>
```

Without `VERSION` it prints `version=unreleased` and the hashes of this
checkout. The cloud setup script carries the same four values as `VERSION`,
`HOME_SHA256`, `INSTALL_SHA256` and `KIT_SHA256`, and `make cloud-setup` fills
them in where the hub's copy holds `'@VERSION@'` and its like. A copy whose
version is still a placeholder installs nothing, and one whose kit pin is
empty or a placeholder installs the rules alone.

---

## 🧩 The Kit

`home/kit.json` is one JSON object, which `kit.py` renders and the installer
refuses in any format but its own:

| Key         | Holds                                                                                                |
| :---------- | :--------------------------------------------------------------------------------------------------- |
| `//`        | A note that the file is rendered and never edited by hand                                            |
| `format`    | `2`, the one format the installer reads                                                              |
| `guard`     | The text of `kit/guard.py`                                                                           |
| `skills`    | Each skill's name, mapped to every file in its folder, by its path inside the folder, as text        |
| `subagents` | Each subagent's name, mapped to `claude`, `copilot` and `codex`: the text of the file each app reads |

`make render` and `make check` refuse to go on while any part of the bundle
names a tannergolden repository that is not on `kit.py`'s list of the ones a
public file may name, or holds an en or em dash, or while a skill breaks the
rules in
[Skills & Subagents](../technical/Skills-&-Subagents.md#-what-every-skill-here-follows)
or a subagent's source is out of shape. `kit.py --check` lists each problem.

**A subagent's source** is `kit/subagents/<name>.md`: a `---` frontmatter
fence holding these keys and no others, then the prompt it runs with:

```markdown
---
name: worker
description: What it does, and when a session should hand it work.
tools: read, search, edit, execute
---

The prompt the subagent runs with.
```

`name` is the file's name, in lowercase words joined by hyphens, and the
`description` is required, since it is what delegation reads. `tools` lists
abstract tools, each from the table below, which each app gets in its own
words:

| Tool      | Claude Code                     | Copilot   |
| :-------- | :------------------------------ | :-------- |
| `read`    | `Read`                          | `read`    |
| `search`  | `Grep`, `Glob`                  | `search`  |
| `edit`    | `Edit`, `Write`, `NotebookEdit` | `edit`    |
| `execute` | `Bash`                          | `execute` |
| `web`     | `WebFetch`, `WebSearch`         | `web`     |
| `agent`   | `Agent`                         | `agent`   |

Codex's TOML carries no tool list: the body becomes its
`developer_instructions`. Every rendered file carries the kit's mark as a
comment at its top, so the installer can tell it is the kit's.

---

## 🗂️ What A Repository Carries

| What                                      | Shape                                                                                                                                                                                                                                                                                                                                                          |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md`                               | The rules block and the sections the repository owns. One a first sync creates has hidden frontmatter, a masthead, the block, an `[!IMPORTANT]` admonition saying the repository's own rules go below it, then `## Commands`, `## Definition of done`, `## Conventions`, `## Where things live`, `## Gotchas`, `## Ask first` and `## Overrides`, and a footer |
| `docs/Prompts.md`                         | A masthead, the prompts block, then `## 📌 Prompts For This Repository`, which is the repository's own                                                                                                                                                                                                                                                         |
| `.github/workflows/intelligence-sync.yml` | The stub, at exactly that path, which is where `make audit` looks for it                                                                                                                                                                                                                                                                                       |
| Topics                                    | `no-intelligence` keeps the repository out of sync; `no-intelligence-prompts` keeps only the prompts out                                                                                                                                                                                                                                                       |

**An Overrides entry** is one line in the section under a heading that reads
exactly `## Overrides`, which runs to the next `## ` heading or a `---` line.
An entry is `- RULE-ID: reason`: a `*` works as the bullet, the ID may sit in
backticks, and the colon may be left out. HTML comments in the section are
ignored, so the hint a first sync leaves there counts for nothing. `make audit`
reports an entry that names an Invariant, and an entry for `STD-001` with no
reason.

**A sync pull request** comes from `chore/intelligence`. Its title is
`chore(agents): 🤖 sync the universal rules to <hash>`, or
`chore(agents): 🤖 sync the universal prompts to <hash>` when only the prompts
change, ending in the first twelve hex digits of that block's hash, and its
body has `## Impact`, `## Validation` and `## Rollback` sections.

---

## 💾 What The Tools Leave On A Machine

| File                                              | Written by        | Holds                                                                                                                                                                                                                                                                                                                                          |
| :------------------------------------------------ | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `~/.local/state/intelligence/install.json`        | `install.py`      | The install record: for each file it touched, whether it created it, the folders it made and the separator it put before a block; the earlier value of Claude Code's `instructionFiles` setting; the hash of the block it installed. `uninstall` reads it, then deletes it                                                                     |
| `~/.cache/intelligence-probe/manifest.json`       | `loader-probe.py` | Every change of the run in progress, written before the change is made. A run that dies leaves it behind, and `--cleanup` replays it                                                                                                                                                                                                           |
| `~/.cache/intelligence-probe/results-<time>.json` | `loader-probe.py` | Each app's version and its raw answer                                                                                                                                                                                                                                                                                                          |
| `~/.cache/intelligence-evals/results-<time>.json` | `evals.py`        | `format` 1, `when`, and one row per run: the scenario, rule, app and condition, the status (`pass`, `fail` or `timeout`), the exit code, each check's verdict and what it saw, and the last 3,000 characters of output with placeholders taken out. A trigger test's rows hold each prompt, whether it should trigger, its rate and its status |

`XDG_STATE_HOME` takes the place of `~/.local/state`, and `XDG_CACHE_HOME` of
`~/.cache`. The probe also takes `--state`, and `evals.py` `--out`.

---

## 🔗 See Also

- [The Home Kit](../technical/The-Home-Kit.md): where each file lands on a machine
- [Repository Sync](../technical/Repository-Sync.md): how a repository's files are written and kept
- [Glossary](Glossary.md): the words this page uses

---

<div align="center">

**One shape for each file, and every reader can count on it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
