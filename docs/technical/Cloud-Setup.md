<!--
title: '☁️ CLOUD SETUP'
description: 'The setup script that installs the universal rules and the kit into every Claude Code cloud session, pinned to one release and unable to fail the session.'
type: guide
-->

<div align="center">

# ☁️ CLOUD SETUP

<a name="top"></a>

**The universal rules in every Claude cloud session, from a pinned release, without ever stopping a session from starting.**

_Pinned at the source. Silent when it cannot help._

</div>

---

## 💡 What It Does

A Claude Code cloud session starts in a fresh container, so nothing the [home
kit](The-Home-Kit.md) installed on your machines is there. Each repository's
own `AGENTS.md` still carries the rules; the setup script adds the home copy,
so a session in a repository with no block of its own gets them too.

[`setup/claude-cloud-setup.sh`](../../setup/claude-cloud-setup.sh) downloads
the home file, the kit and the installer from one release, checks each against
its pin, and installs Claude Code's share:

- `~/.claude/CLAUDE.md`, with the rules between their markers;
- the guard hook, registered in `~/.claude/settings.json`, which Claude Code's
  docs say a cloud session does not read; whether that covers a file written
  inside the container is untested, as
  [Backstops & Residual Risk](../operations/Backstops-&-Residual-Risk.md)
  records;
- the skills in `~/.claude/skills/` and the subagents in `~/.claude/agents/`.

A kit that cannot be downloaded or misses its pin is left out, and the rules
still install; an empty kit pin, from a release before the kit, installs the
rules alone. **It always exits 0**: a setup script that fails stops the
session from starting, so every failure prints a notice instead.

---

## 🚀 Installing It

1. Cut a release, then print the script with that release's pins:

   ```bash
   make cloud-setup VERSION=v0.1.0
   ```

2. Paste the output into the cloud environment's settings: open the
   environment menu in a session's title bar, choose Edit, and put it under
   Setup script. New sessions run it.
3. After each new release, print it again and replace the old one.

The copy in the hub keeps placeholders where the pins go, and refuses to
install anything until they are filled.

---

## 🔗 See Also

- [ADR-0010](../adrs/ADR-0010-Releases-Serve-Rendered-Files.md): a release tag serves the rendered files, checked against pins
- [Releasing](../distribution/Releasing.md): where printing the setup script falls among the release steps
- [Troubleshooting The Home Kit](../operations/Troubleshooting-The-Home-Kit.md): what each notice the script prints means

---

<div align="center">

**Every cloud session starts with the rules, or starts anyway.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](../../LICENSE).

</div>
