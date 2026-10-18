<!--
title: '🏠 HOME FILE'
description: 'The rendered home file the home kit installs, and the hashes a consumer pins, served from every release tag.'
tags: [home-kit, release, checksums, dotfiles]
category: docs
-->

<div align="center">

# 🏠 HOME FILE

<a name="top"></a>

**What every machine downloads from a release: the rules between their markers, and the hashes to check them against.**

_Rendered, never written. Pinned, never trusted blind._

</div>

---

## 💡 What This Folder Is For

`intelligence.md` is the universal block between its `INTELLIGENCE`
markers, exactly as `scripts/render.py` renders it from `law/`. The home kit
copies it into each app's home folder, and the Claude cloud setup script
writes it into a fresh session.

| File              | What it is                                                             |
| :---------------- | :--------------------------------------------------------------------- |
| `intelligence.md` | The home file: the universal block between its `INTELLIGENCE` markers  |
| `SHA256SUMS`      | The SHA-256 of the home file and of `scripts/install.py`, for a reader |

Both change with every render, so the file log below leaves them out and
this table describes them instead. **Never edit anything here by hand.**
`make render` rewrites this folder, and `make check` fails CI when it has
drifted from the law.

---

## 📦 How A Machine Gets It

A release is a tag, and each tag serves this folder and the installer as
they were at that commit:

```text
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/home/intelligence.md
https://raw.githubusercontent.com/tannergolden/intelligence/<version>/scripts/install.py
```

The consumer checks each file against a SHA-256 it pinned beforehand, and
never against a hash from the same download. `make pins VERSION=vX.Y.Z`
prints those pins for a release, and `SHA256SUMS` here lists the same
hashes for a reader.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log exclude=intelligence.md,SHA256SUMS -->

| Entry                    | Purpose    |
| :----------------------- | :--------- |
| [`README.md`](README.md) | This file. |

<!-- AUTO-INDEX:END -->

---

<div align="center">

**One file, one hash, the same on every machine.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../LICENSE).

</div>
