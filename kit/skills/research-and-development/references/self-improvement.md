# Self-improvement - the build mode's recursive loop

How the build mode improves a skill or agent that misbehaved, this skill included. Self-correction is reliable only when bound to an external signal; prompt-only self-critique is weak and can degrade output. So every step here is anchored to an oracle (a failing test, the validator, a tool result, a golden example), never to the model's own say-so.

## The loop

1. **Capture** the failure from the transcript and any explicit notes: what was asked, what the skill did, what was wrong. Concrete, not paraphrased.
2. **Blameless postmortem** to the root cause, not the symptom (Google SRE). 5-Whys: a wrong output usually traces to a missing instruction, an ambiguous boundary, or a weak description, not to "the model erred." Fix the cause.
3. **Minimal corrective diff.** The smallest change that addresses the root cause and prevents the class of failure. Resist rewriting; a large diff is a new build, not a fix.
4. **Propose, then apply only on approval.** Show the diff and the reasoning; apply nothing until your user approves.
5. **Verify independently.** Re-run `scripts/validate.py` on the skill, and the repository's own checks for conformance with its rules; dispatch a fresh QA Test Engineer, borrowed from the quality-assurance skill, to re-check only the changed area, joined by the information-technology skill's Security Engineer where the change is security-relevant; run a trigger check if the description changed. The author never grades its own fix (self-preference bias is real and significant).
6. **Freeze a regression case.** Append one line to the target skill's `assets/regression-cases.jsonl`: the failing input, the expected behavior, and a one-line lesson. Every future self-edit must re-pass every frozen case, so a later fix cannot silently regress an earlier lesson.

## No self-grading, even on this skill itself

When the build mode edits this skill, the same rule holds: the fix is verified by the deterministic validator and the independent reviewer and the regression ledger, never by the skill declaring its own change good. The ledger is the objective memory that keeps recursion honest. In tannergolden/intelligence, a change to this skill also passes `make check`, and its trigger test, drawn from its own `assets/trigger-evals.json` into `evals/skills/research-and-development.json` by `evals.py --draw`.

## Regression ledger format (`assets/regression-cases.jsonl`)

One JSON object per line:

```text
{"id":"rc-0001","date":"YYYY-MM-DD","skill":"<name>","input":"<the triggering request>","expected":"<the correct behavior>","was":"<what it did wrong>","lesson":"<the one-line rule that prevents recurrence>"}
```

Managed append-only. The file ships empty at `1.0.0` and grows one entry per real fix. In a skill with several modes, an id carries its mode as a prefix (this skill's are `research-rc-001` and `build-rc-0001` onward), and a case carried over from a skill that was merged in keeps its fields and its number under that prefix, its `skill`, where it has one, naming the skill it now guards.
