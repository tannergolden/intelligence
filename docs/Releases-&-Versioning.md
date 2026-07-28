<!--
title: '🏷️ RELEASES & VERSIONING'
description: 'The two tags this repository publishes, what each one promises a consumer, and the only recall that exists when a release is wrong.'
tags: [releases, versioning, tags, rollback]
category: docs
-->

<!-- markdownlint-disable MD041 -->
<div align="center">

# 🏷️ RELEASES & VERSIONING

<a name="top"></a>

**Moving one tag changes what every pinned repository receives on its next run.**

_A release here is a production change to every consumer at once._

</div>

---

## 🎯 Two Tags, Two Contracts

| Tag       | Promise                                                                                  |
| :-------- | :---------------------------------------------------------------------------------------- |
| `vX.Y.Z`  | **Immutable.** Cut once, never moved. For anyone who wants exactly these bytes forever    |
| `vX`      | **Moving.** Re-pointed at each release in that major line. The normal pin, and the reason a fix reaches everyone |

A consumer pinning `@v1` receives every later fix in the v1 line automatically. A consumer pinning `@v1.4.2` receives nothing ever again, which is the point, and is also why no publisher-side action can reach them.

---

## 🚀 Cutting A Release

Run [`🏷️ Cut Release`](../.github/workflows/release.yml) from the Actions tab with a `vX.Y.Z` version. It validates the version, refuses one that already exists, refuses a commit that is not reachable from the default branch, checks that the published action still resolves, **runs the product's own gates one last time**, cuts the immutable tag, publishes the release with the skill archives attached, and only then force-moves the major.

That last gate is the point of having a workflow rather than two `git tag` commands. There is no build step, so the files in the commit are the files that land, and the release is the final moment anything can check them: the sync pushes directly into consuming repositories, with no pull request and no CI anywhere downstream. It refuses to tag if a published skill fails its checks, if either checker's hostile fixtures stop being rejected, if the packager stops holding its invariants, or if any file the sync stub copies is missing, which is all seven and not only the three documents.

**The order of the last two steps is load-bearing.** The release page carries the archives, so publishing it before moving `v1` means a failed upload leaves an unreferenced `vX.Y.Z` rather than a moving pointer aimed at a version whose downloads do not exist. The tag every consumer resolves is the last thing that changes, which is the only ordering where a partial failure is recoverable without a recall.

By hand, the equivalent is two commands, and they skip every one of those checks:

```bash
git tag v1.0.0 && git push origin v1.0.0
git tag -f v1 && git push --force origin v1
```

The force-move on the second line is deliberate. `v1` **is** the moving pointer, and moving it is the entire mechanism by which a change reaches anyone.

> [!NOTE]
> **There is no prune job**, unlike the sibling publisher, which prunes with `keep: 1` and deletes the tag behind each removed release. It can, because every stub there pins the moving major and nothing pins a full version. This repository's contract permits an exact `@vX.Y.Z` pin, so deleting a version tag would break that consumer's sync at checkout with a message saying the repository does not exist. Version tags outlive their release pages here.

> [!IMPORTANT]
> **Never attach a release object to a bare major tag.** `v1` is a pointer every consumer resolves. A release attached to it turns it into an artifact that tooling may prune or freeze, which would kill distribution and the emergency brake in the same stroke.

---

## ✅ Before You Move The Tag

The review happens here, before the tag moves, because there is no review anywhere downstream: the sync pushes directly, with no pull request and no CI in the consuming repository.

- [ ] `AGENTS.md` still holds true in a repository with a different trunk name, review policy and toolchain
- [ ] Neither router gained a rule. They are envelopes and must stay empty of law
- [ ] Every skill passes the checker, and the hostile fixtures still fail it
- [ ] The diff is small enough that one person can actually read it

That last item is the real control. This repository has one maintainer, so a second reviewer is not available, and the compensating measure is that **the files here are the files that land**. There is no build step to reason about: reviewing a release is reading the diff.

---

## 🧯 Recall

There is one lever, and it is slower than you want.

```bash
git tag -f v1 <last-good-sha> && git push --force origin v1
```

> [!CAUTION]
> **Moving the tag back fixes nothing already delivered.** The previous content sits in every consuming repository until each one next syncs, which is up to a week on the default schedule and longer if GitHub has disabled a quiet repository's cron. For inert markdown that is an acceptable recall time, which is precisely why nothing executable ships through this path.

**Consumers pinned to `@vX.Y.Z` are unreachable by any publisher-side action.** For them the recovery path is a human editing their pin. That is the honest price of an exact pin, and it should be stated when one is recommended.

There is no faster lever, deliberately. A credential that could reach into every consuming repository is a credential whose theft could not be evicted from every consuming repository.

---

## 🔢 What Counts As A Major

A change is **breaking**, and belongs in a new major line, when a consumer must edit something for it to work:

- The set of published files changes, so a sync starts writing a path nobody agreed to
- The stub's shape changes, since no token available to it can write under `.github/workflows/`
- A rule in `AGENTS.md` inverts rather than tightens, for example forbidding something previously required

Everything else is a minor or a patch. Adding a skill, clarifying a rule, or deleting a router because a vendor adopted the canonical filename are all additive: nothing downstream needs editing.

---

## 📚 Documentation Index

Everything explaining how this publisher works lives in the [Documentation Index](README.md). Follow it **by link**, never by copy.

The other side of this page is [Installation](Installation.md): what a consumer commits, and what a moved tag reaches them through.

---

<div align="center">

**One tag to receive fixes, one to receive nothing, and no way to hurry either.**

[↑ Back to Top](#top)

</div>
