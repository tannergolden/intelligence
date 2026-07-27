<!--
title: '🧾 RETIREMENT CONTRACT'
description: 'The three conditions a published file must satisfy before this publisher deletes it from a repository it does not own, and exactly what happens when one of them fails.'
tags: [retirement, deletion, lockfile, ownership]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🧾 RETIREMENT CONTRACT

<a name="top"></a>

**Retirement is this publisher deleting a file from somebody else's repository, by bot, on a schedule, with no pull request in the path. These are the rules it obeys before it does that.**

_Every other mistake here is a diff. This one is a deletion._

</div>

---

## 🎯 Why It Exists At All

Retirement cannot simply be switched off. A file that arrives and never leaves makes the whole system undeletable, and being cleanly removable is one of the six requirements this repository was built to. The lockfile is therefore two things at once: the record of what was delivered, and the manifest for taking it away.

The price of that is a bot with a delete capability pointed at repositories it does not own. Everything below is how that capability is made narrow enough to live with.

---

## ✅ The Delete Rule

A path is removed **only** when all three of these are true. Any one of them failing stops the delete.

```text
delete(path) requires
  1. the lockfile records that WE wrote it        ownership
  2. payload/ no longer ships it                  intent
  3. sha256(bytes on disk) == sha256 in the lock  untouched since delivery
```

Each clause is answering a different question, which is why none of them is redundant:

- **Ownership** is what separates _"the publisher put this here"_ from _"this repository already had one"_. Without a stored digest, a retirement cannot tell those apart, and the delete becomes a guess.
- **Intent** is the only thing that starts a retirement. Files leave because the payload stopped shipping them, never because a consumer looks like it does not want them.
- **Untouched** is the consent check. A file whose bytes have changed since delivery has a human's work in it.

Two edge cases resolve without ceremony:

- **The file is already gone.** Nothing to delete, and the bookkeeping goes with it. Not an error.
- **The path is a symlink.** Never followed, never deleted. Writing or deleting through a link can leave the repository entirely, so it is treated as contested and left alone.

---

## ⚖️ Contested Paths

A digest mismatch means the consumer edited a file this publisher delivered. The run does **not** delete it, and it does **not** forget it:

- the delete is refused and printed by name, with the reason;
- the lock entry is kept, with `status` set to `contested`;
- the path is also listed in the lock's `contested` array, so it is visible without diffing entries.

> [!IMPORTANT]
> **Dropping the entry would be the silent failure here.** A contested path whose ownership record is deleted becomes invisible: the next run has no record that anything was ever owed at that path, so the file is skipped forever and nobody is told. Keeping the entry is what makes the condition surface every single run until a human resolves it.

Resolution is a person, and there are only three answers: restore the delivered bytes and let it retire, delete it by hand, or keep it, in which case it is theirs now and the lock entry should go with the same edit.

---

## 🛑 The Floors

Two hard stops sit in front of the delete rule, because the delete rule is per file and the dangerous failures are per run.

| Floor                                    | What it stops                                                                                                                                         | What it does instead                                                   |
| :--------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| **Empty payload**                        | A publisher-side mistake that removes the product entirely, which would read as _"retire every delivered file"_ in every consuming repository at once | Aborts the run before writing anything, and records the failed outcome |
| **More than two retirements in one run** | The same mistake at smaller scale: one careless deletion inside `payload/` reaching the fleet on the next schedule                                    | Prints the full list of what would go, refuses, and changes nothing    |

Two is a count, not a percentage. A proportional heuristic is noise at this size: with a handful of published paths, half of them is one file.

> [!IMPORTANT]
> **The floor is fixed at the publisher, never waved through at the consumer.** The engine carries an `--allow-large-retire` flag for a maintainer running it by hand, and that flag is deliberately not reachable from the reusable workflow: it takes no inputs, so the stub stays the whole consumer-side surface. **Retiring more than two paths means splitting the change across releases**, two paths at a time. Anything else turns one careless deletion into a fleet-wide sync failure that every consumer sees weekly and none of them can clear.

One consequence of the delete rule is worth stating on its own, because it is silent. **A lockfile that cannot be read forfeits all retirement bookkeeping.** The run recovers, treats the repository as a first sync and refuses nothing, but every path an earlier release delivered there and the current payload no longer ships is now unowned: it can never be retired and stays in that repository forever. The run says so; nothing else will.

The settings file is exempt from all of this in one direction only. It is **never** deleted, because it is the consumer's file. Retiring it means removing the hook entries carrying this publisher's frozen command prefix and leaving every other key, and every foreign hook, exactly as found.

---

## 🧾 An Opt-Out Suppresses Actions, Never Bookkeeping

This is one rule, and it shows up in three places. It is worth stating as a rule because each instance looks like a special case on its own.

1. **A run that refuses carries the previous lock's `files` forward verbatim.** A refused sync is not a sync that never happened, and afterwards only the lockfile can tell those two states apart. Dropping ownership on refusal would orphan every path the publisher owned, permanently, and make the next retirement unsafe.
2. **`.ai/hooks/.disabled` stops hooks executing. It does not un-own them.** The hook script is still delivered, still recorded in the lock, still retired when the payload stops shipping it. The sentinel is consumer-owned: this publisher never creates it and never deletes it, so a sync can never quietly re-arm a hook somebody switched off.
3. **An ignored path keeps its tombstone.** In the template engine this publisher takes these paths over from, ownership entries for ignored paths are carried forward permanently rather than dropped, so removing the ignore line later still retires a file the template has since deleted. Same rule, older code, and the reason the handoff order matters: ignore first, hand over last.

The general form: **an opt-out governs what happens next, never what already happened.**

---

## 🧹 Removing It Completely

From a consuming repository, in this order:

1. **Delete `.github/workflows/ai-sync.yml`.** No stub, no sync. Nothing further arrives, ever, and no credential needs revoking because none was ever issued.
2. **Read `.ai/ai.lock.json`.** It lists every path that was delivered, with its digest and its owner. This is the manifest.
3. **Remove those paths, and the hook entries.** `sh .ai/ai.sh remove` walks the manifest for you; by hand, delete the listed files and strip the hook entries whose command begins with the frozen prefix from `.claude/settings.json`, leaving the rest of that file untouched.
4. **Delete `.ai/`.** `sh .ai/ai.sh remove --force` does it, and it moves `.ai/local/agents-local.md` out to `./agents-local.md` on the way rather than deleting it. That file was always yours: every sync read it and none of them ever wrote it, so uninstalling this publisher must not be able to destroy it. Nothing else under `.ai/` survives.
5. **Leave the tombstone lines alone** in `.template-sync-ignore`. They belong to the other engine, and deleting them re-arms it against paths it no longer ships.

`AGENTS.md`, `CLAUDE.md` and `GEMINI.md` are yours to keep or delete. Once step 1 is done they are ordinary files in your repository, and nothing will ever touch them again.

---

## 🔗 See also

> [!TIP]
> The deletion capability described here is one of several this publisher holds over a repository that installs it. [The threat model](Threat-Model.md) covers the rest, including the one that executes rather than writes.

---

<div align="center">

**Owned, then unwanted, then unchanged. Nothing is deleted on fewer than three.**

[↑ Back to Top](#top)

</div>
