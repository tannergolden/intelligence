# Change review: <the change, in a few words>

<!-- One record per change to the company's systems. The Platform Engineer fills Contract to Way back, the Security
     Engineer fills Threat review, the Chief Information Security Officer fills Security call when it fires, and the
     lead fills the rest. Never write a secret's value here: name where it lives. -->

- **Date:** <YYYY-MM-DD>
- **Owner:** <the seat accountable for the change, and the person who will take the gated steps>
- **Tier:** <standard or deep>

## Contract

<What the change must do, for whom, against which constraints, and why now.>

## Blast radius

| Systems touched | Accounts and roles | Data and its sensitivity | Secrets (where they live) | People affected |
| :-------------- | :----------------- | :----------------------- | :------------------------ | :-------------- |
| <system>        | <role or group>    | <data, sensitivity>      | <store, holder>           | <who>           |

## Design

<The configuration or infrastructure as code; for an integration or automation, its service identity, its scopes and its logging. Reuse, configure, buy or build, and why.>

## Way back

- **Rollback:** <the exact steps to undo it, or "cannot be undone" and why>
- **Backup taken first:** <what, where, when>

## Threat review

| Threat | Path | Exploitability | Blast radius | Mitigation |
| :----- | :--- | :------------- | :----------- | :--------- |
| <who could do what> | <how> | <high, medium or low> | <what it reaches> | <the control> |

**Verdict:** <pass, pass with mitigations, or block>

## Security call

<The Chief Information Security Officer's call, exactly as given: accept, mitigate or refuse, with the threat, the control and the residual. "Not fired" when no material residual remained. A refusal holds the change until it is redesigned and accepted, or the Founder accepts the risk; record that acceptance here, dated.>

## Gated steps

| Step | Who it touches | The way back | Confirmed by the user on |
| :--- | :------------- | :----------- | :----------------------- |
| <exact change> | <people or accounts> | <undo, or irreversible> | <date, or waiting> |

## Verification

<Who checked it, other than its author, and against what: the Security Engineer's review, and on a deep run the quality skill's ★ Head of Quality.>

## Open items

- <what remains, with an owner and a date>
