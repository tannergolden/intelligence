# Evaluation

Seeing a skill trigger tells you it was found. It does not tell you it did what you intended, and it does not tell you the session was better for having loaded it.

## Measure two things, because they fail separately

**Invocation.** Does it load on the requests it should, and stay quiet on the ones it should not? This is a property of the description alone.

**Output.** When it does load, is the result right? This is a property of the body and its references.

A skill that triggers reliably and answers badly, and a skill that answers well and never triggers, are both broken. Only the first looks like it is working.

## The comparison that decides whether it ships

Run each case twice in a fresh session, once with the skill available and once without, and compare. A fresh session matters: context left over from writing the skill hides gaps in what the skill actually says.

Then compare three numbers, not one:

| Number | Question |
| :--- | :--- |
| Pass rate | Did the skill make the answer more correct? |
| Tokens | What did that cost on every session it loaded in? |
| Time | Did it make the task slower? |

**A skill that does not beat its own baseline should not ship**, however well written. Published research finds context files often fail to improve task success while adding substantial inference cost, so the burden of proof sits with the skill.

## The eval file

`evals/evals.json` holds the cases. It is read by tooling and never by an agent, so it costs no context and needs no reference from `SKILL.md`.

Include **should-not-trigger** cases, and do not treat them as padding. A skill that fires on every adjacent request spends context in every session and crowds out the skills that should have fired instead. Those cases are how a too-broad description gets caught.

Shape:

```json
{
  "schema": 1,
  "skill": "<name>",
  "cases": [
    {
      "id": "trigger-direct",
      "prompt": "the plainest request that should summon it",
      "should_trigger": true,
      "assertions": ["what must be true of the output"]
    },
    {
      "id": "no-trigger-adjacent",
      "prompt": "a nearby request that should NOT summon it",
      "should_trigger": false,
      "assertions": ["the skill is not loaded, and why"]
    }
  ]
}
```

## Writing cases that are worth running

**Use real phrasings.** A case written in the same words as the description proves the description matches itself and nothing more. Write what someone would actually type, including the sloppy version.

**Make assertions checkable.** "The output is good" cannot fail. "The header matches the required pattern" can.

**Cover the adjacent request you are most afraid of.** For every skill there is one neighbouring task it will wrongly claim. That is the case worth writing first.
