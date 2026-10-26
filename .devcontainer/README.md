<!--
title: '🐳 DEVELOPMENT CONTAINER'
description: 'The development container for working on the intelligence hub: the environment image, with every tool the checks run at the versions CI installs.'
type: index
-->

<div align="center">

# 🐳 DEVELOPMENT CONTAINER

<a name="top"></a>

**The hub, worked on inside the machine every check runs on.**

_The environment's image, and the hub's own hooks._

</div>

---

## 💡 What This Folder Is For

Open the repository in a dev container - <kbd>Reopen in Container</kbd> in VS
Code, or a Codespace - and this folder decides what you get: the environment's
image, [`ghcr.io/tannergolden/environment:1`](https://github.com/tannergolden/environment).
It holds git, Python 3.12, Node.js 22 and every tool the standards' checks run,
at the versions CI installs them at, so the hub's own checks, the validator,
the renderer's check and the installer and kit tests, run here as they run in
CI.

When it is created it does what the template's container does: installs the
scripts' requirement, PyYAML, switches on the
[git hooks](../.github/scripts/hooks/README.md), and sets the commit message
template. The image already holds gitleaks, at the version CI scans with, so
the `pre-commit` hook scans what you stage for secrets with the same one.

**This file is the hub's own.** Its two lines in
[`.github/template-sync`](../.github/template-sync) are switched off, so a sync
never puts the template's container back. The image is for the repositories
other repositories call, like this one; the template keeps a container of its
own for everything else.

`.gitattributes` marks this folder `export-ignore`, so `git archive` leaves it
out of a source tarball. It is for developing the project, not for shipping it.

---

## 📝 File Log

<!-- AUTO-INDEX:BEGIN dir=. style=log -->

| Entry                                    | Purpose                                                                  |
| :--------------------------------------- | :----------------------------------------------------------------------- |
| [`devcontainer.json`](devcontainer.json) | Development container for the intelligence hub: the environment's image. |
| [`README.md`](README.md)                 | This file.                                                               |

<!-- AUTO-INDEX:END -->

🗂️ Machined Indexes redraws this log after every push to the default branch,
from what each file says about itself.

---

## ⚙️ Keeping It In Step

- Every check tool's version is the environment's: a new image reaches this
  container after `docker pull ghcr.io/tannergolden/environment:1` and a
  rebuild.
- Add an editor extension to `customizations.vscode.extensions`, and anything
  the hub needs beyond the image to `postCreateCommand`, keeping what is
  already there.
- Rebuild the container after any change here.

> [!NOTE]
> **There is no `settings` block, deliberately.** VS Code reads
> [`.vscode/settings.json`](../.vscode/settings.json) inside the container like
> anywhere else, so a copy here would be a second source of truth, and the copy
> that drifts is always the one nobody remembers.

`devcontainer.json` is JSON with comments, which is what dev containers read.
The repository validator parses it the same way, so a comment is never reported
as an error.

---

<div align="center">

**The same tools as CI, wherever you open it.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
