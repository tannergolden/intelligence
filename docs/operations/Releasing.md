<!--
title: '🚀 RELEASING'
description: 'Every step from a green Development to the rules on every machine and in every repository: cutting the tag, pinning it, the cloud setup script, and the sync.'
type: guide
keywords: [release, versioning, pins, sync]
-->

<div align="center">

# 🚀 RELEASING

<a name="top"></a>

**Each release is a tag, and every step after it is one command.**

_Nothing leaves the hub until a release does._

</div>

---

## 💡 What A Release Does

A merge to `Development` reaches no machine and no other repository. A release
does: it is a tag, `vX.Y.Z`, with the moving `vX` beside it, and everything
downstream pins it. Dotfiles' `make agents` and the Claude cloud setup script
download the home file, the kit and the installer from the tag and check each
against its SHA-256; every repository's stub runs the hub's code at the moving
`vX`; and `make sync` delivers the block of the latest tag. `make help` lists
every command below.

---

## 🚀 The Steps

1. On `Development`, `make check` passes. The first release that ships the
   [prompts](../technical/Prompts.md) also needs a release of the standards
   whose Machined Block Check hashes the code fences inside a block: every
   repository's CI runs that check at the standards' `v1`, and an earlier one
   reads the prompts block as edited.
2. Run 🏷️ Cut Release with the next version, such as `v0.1.0`. It runs
   `make check` again, and refuses a release whose rendered files have
   drifted from the Constitution, or that is missing a file a consumer or a stub
   resolves at the tag.
3. `make pins VERSION=v0.1.0` prints the hashes to pin: the home file, the
   installer and the kit. Put them in dotfiles' `agents/intelligence.pin`,
   then run `make agents` on each machine, as [the home
   kit](../technical/The-Home-Kit.md) describes.
4. `make cloud-setup VERSION=v0.1.0` prints the Claude cloud setup script,
   pinned. Paste it into the cloud environment's setup script, as [Cloud
   Setup](../technical/Cloud-Setup.md) describes.
5. `make audit`, then `make sync ARGS=--dry-run`, then `make sync`: one pull
   request per repository. A repository that carries the stub picks the
   release up by itself on Monday, so this step is for the rest, or for now
   rather than Monday. [Repository Sync](../technical/Repository-Sync.md)
   covers both routes.
6. Review each first sync, and each pull request that adds `docs/Prompts.md`,
   by hand. After that, `make merge` lands every sync whose diff is only the
   blocks and whose checks passed.

Every version stays: the stub passes `keep-versions: true`, so standards' Cut
Release never prunes here, because a pin to a full version must keep
resolving and `make audit` names old blocks by the release that shipped them.

---

## 🔗 See Also

- [ADR-0010](../adrs/ADR-0010-Releases-Serve-Rendered-Files.md): a release tag serves the rendered files, checked against pins
- [Roadmap](Roadmap.md): what the first releases have to prove

---

<div align="center">

**Cut once, pinned everywhere.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
