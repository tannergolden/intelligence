# Descriptions - writing the line that decides whether a skill fires

The `description` is a skill's single most important deliverable. A strong body behind a passive description never triggers. The same goes for an agent's `description`, which is its routing key.

## The rules (skill descriptions)

1. **Third person: what it does, then "Use when ..."** with the user's own words. "Builds skills ... Use when the user asks to ..." not "I build skills."
2. **Concrete quoted trigger phrases**, 4 to 6, drawn from how a user actually asks: "build a skill", "create an agent", "make a team", "turn this workflow into a skill".
3. **A pushy anti-undertrigger clause**: "even if they never say skill." Under-triggering is the common failure; lean against it.
4. **Front-load keywords.** The first words carry the most routing weight; put the main use case first.
5. **Keep all when-to-use in the description.** Do not split it between the description and the body; the router sees only the description.
6. **Stay short.** One to three sentences of trigger surface, at most 1,024 characters and no angle brackets. Every installed skill's description loads into every session, so each word costs everywhere the skill is installed.
7. **No "do not use for" list.** Negative examples contaminate the keyword field and cause the misses they mean to prevent; put near misses in the trigger tests instead.
8. **No "claude" or "anthropic" in the name.**
9. **Search before adding.** Two skills whose descriptions overlap steal each other's triggers. Merge rather than duplicate.

## Agent descriptions

Same spirit, routing-first: "Dispatch this agent when ...", naming the capability and the situation. The orchestrator routes from this line alone, so make the trigger condition unmistakable.

## How it is tested

- **Light trigger check** (every build): run the skill's `assets/trigger-evals.json` cases, or at least read the description cold against them and confirm the obvious phrasings would route to it.
- **Full smoke test** (Publish or complex tier): about 20 queries, half should-trigger and half near-miss negatives in varied wording, each run three times; a prompt passes when the skill loads in at least half its runs. Keep six in ten for tuning and hold the rest back. Score the true-negative rate as carefully as the hits.
- **Seeing a trigger**: activation is proven by a skill tool call in a real run, never by reading the description. In Claude Code, `claude -p "<prompt>" --output-format json` shows whether a `Skill` tool call named the skill. A headless harness can fail to trigger skills at all, so verify the harness before blaming the description.
- **In tannergolden/intelligence**, a universal skill's trigger test lives in `evals/skills/<name>.json`, beside the skill rather than inside it, and `make evals` runs it.
- **Tune the description, not the prompts.** Never paste a failing prompt's words into the description; generalise from it instead.
