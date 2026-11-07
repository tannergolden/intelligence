# Security ledger: <the build, in a few words>

<!-- One ledger per security review of a build: an app, a tool, a script, a skill, an agent or a pull request. The
     Security Engineer fills it fresh, never having read the builder's reasoning, and returns it to the lead of the
     skill that sent the build (this skill's ★ Chief Information Officer, or the research-and-development skill's
     ★ Head of Research & Development). The Chief Information Security Officer fills Security call when it fires. Cite
     each fix; never apply it. Never write a secret's value here: a secret found is named by where it is. -->

- **Date:** <YYYY-MM-DD>
- **Build:** <what was reviewed: the checkout path and revision, or the pull request>
- **Requirements reviewed against:** <the locked requirements, inline or by path>
- **Sent by:** <the skill and seat that sent the build>
- **Tier:** <standard or deep, and why>

## Attack surface

| Input or boundary | Who controls it | What it reaches | Worst credible case |
| :---------------- | :-------------- | :-------------- | :------------------ |
| <a form field, a file upload, an API call, a webhook, a prompt> | <anyone on the internet, a signed-in user, an admin, another service> | <the query, the shell, the store, the data> | <what an attacker gets> |

**The adversary:** <who would attack this and why, in a sentence>

## Checks run

<The read-only checks run in the build's own checkout, each with its date and what it found: a dependency audit, a secret scan, the build's own tests, a reproduction against a local copy. "None run" with the reason, when none could be.>

## Findings

| # | Class | Severity | Exploit path (how it is reached) | Fix | Status |
| :- | :---- | :------- | :------------------------------- | :-- | :----- |
| 1 | <injection, broken authentication or authorization, exposed secret, unsafe dependency, data exposure, other> | <high, medium or low> | <the concrete path from the input to the harm, or the assumption that would make it reachable> | <the fix the builder applies> | <open, fixed and re-reviewed> |

Ranked by exploitability and blast radius, hardest-hit first. A dependency's risk carries its source and the date it was looked up.

## Verdict

**<SHIP or BLOCK>** - <one line: the reachable high-severity finding that blocks it, or why nothing reachable at high severity remains>

- **Follow-ups that do not block:** <each lower finding, with an owner, or "none">

## Security call

<The Chief Information Security Officer's call, exactly as given, when a material residual remains or someone asks to ship past a block: accept, mitigate or refuse, with the threat, the control and the residual. "Not fired" otherwise. A refusal holds the build until it is fixed and re-reviewed, or the Founder accepts the risk; record that acceptance here, dated.>

## Re-review

<For each fixed finding: the date it was reviewed again and the result. A block lifts only when every reachable high-severity finding reads fixed and re-reviewed.>
