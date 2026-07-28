# Evaluating A Skill

Seeing a skill trigger tells you it was found. It does not tell you it did what you intended, and it does not tell you the session was better for having loaded it.

## Measure three numbers, not one

| Number | Question |
| :--- | :--- |
| Pass rate | Did the skill make the answer more correct? |
| Tokens | What did that cost, in every session it loaded into? |
| Time | Did it make the task slower? |

The comparison that matters is **with the skill against without it**, on the same prompts. Each case runs twice, and the harness keeps the two runs side by side so the delta is visible rather than inferred.

**A skill that does not beat its own baseline should not ship**, however well written. Cost is not a rounding error here: the description is paid in every session, and the body is paid for the rest of any session that loads it.

## Start with two or three cases

Do not over-invest before the first round of results. Two or three realistic prompts tell you more than twenty speculative ones, because the first run usually reveals that the description, not the body, is what needs work.

Grow the set from what the runs show. If several test cases all produced the agent writing the same helper, that is the signal to bundle a script, and it comes from the transcripts rather than from guessing.

## Run each case in a fresh session

Context left over from writing the skill hides gaps in what the skill actually says. A fresh session is the only way to see what the file alone conveys.

## The eval file

`evals/evals.json` holds the cases. It is read by tooling and never by an agent, so it costs no context and needs no reference from `SKILL.md`.

```json
{
  "skill_name": "string",
  "evals": [
    {
      "id": 1,
      "prompt": "a realistic request, in the words a user would type",
      "expected_output": "what a correct response looks like",
      "files": ["optional input files the case needs"],
      "assertions": ["a checkable claim about the output"]
    }
  ]
}
```

## Writing cases worth running

**Use real phrasings.** A prompt written in the same words as the description proves the description matches itself and nothing else. Write what someone would actually type, including the careless version.

**Make assertions checkable.** "The output is good" cannot fail. "Every heading matches the required pattern" can.

**Cover the adjacent request you are most afraid of.** Every skill has one neighbouring task it will wrongly claim. That case is worth writing before any of the happy paths, because over-triggering is the failure that costs every session rather than one.

## The loop

Propose an improvement, rerun every case, grade the results, aggregate the benchmark, look at the transcripts yourself, and repeat until iterations stop producing a meaningful difference. Then stop. A skill polished past the point where the numbers move is a skill being tuned to its own test set.
