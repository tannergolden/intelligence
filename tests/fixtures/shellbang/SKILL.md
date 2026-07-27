<!--
HOSTILE FIXTURE. This file exists to FAIL `actions/ai-sync/check.py`.

Its NAME is forced by the rule under test. `shellbang` keys on a set of
basenames and this is one of them, so the fixture cannot be called anything
else. It is not a skill: nothing here is published, no skill is shipped in
v1, and `payload/.agents/skills/` holds only its sentinel. This file is a
fixture, not a document; it is deliberately exempt from the repository's
markdown styling rules and is never delivered anywhere.

Expected result: exactly TWO shellbang violations and ONE permalink
violation, on the three lines marked HAZARD, and NONE on the two marked SAFE.
-->

# Hostile fixture: shellbang and permalink

This file must be REJECTED. The two spellings below are inert in Gemini CLI
and LIVE in Claude Code, and Anthropic's own skill importers refuse to
auto-port them for exactly that reason. The rule covers every instruction
file this publisher ships, not only this basename, because the hazard is
worse in an always-loaded file than in a skill.

Nothing here is a real instruction. Do not copy any of it into payload/.

## HAZARD 1 - fenced shell block, must be caught by `shellbang`

```!
echo this executes in Claude Code and reads as prose in Gemini
```

## HAZARD 2 - inline shellbang, must be caught by `shellbang`

Run !`whoami` before you continue.

## HAZARD 3 - branch-form permalink, must be caught by `permalink`

See https://github.com/tannergolden/standards/blob/Development/README.md for
the long form.

## SAFE 1 - a SHA-pinned permalink, must NOT be caught

See https://github.com/tannergolden/standards/blob/0123456789abcdef0123456789abcdef01234567/README.md
for the exact revision.

## SAFE 2 - an ordinary fence, must NOT be caught

```sh
echo this is a normal shell block
```
