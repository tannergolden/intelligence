# Deliverables - what the IT department produces, and where it lands

The producing map for every `information-technology` run: each deliverable, the seat that produces it, what triggers it, the completion evidence it must carry before it lands, and where it goes. Read it with `dispatch.md`, which sets who runs in what order, and `gated-acts.md`, which sets what waits for the user's yes. The standard is the team's: **secure by default, reversible by design**.

## Where the work lands

A venture's department records go where the repository's own instructions keep them: the venture's **Information Technology (IT) records**, in whatever folder and files those instructions name (a repository with a venture template maps each deliverable below onto its own files). The user's own devices and accounts are their personal context: their records go only into a repository whose instructions (its `AGENTS.md` or `CLAUDE.md`, or with neither its root and folder `README.md` files) say it is a private one made to hold it (the Constitution's SEC-003). A build's security ledger goes where the repository that holds the build keeps its reviews, or back to the research-and-development skill when it borrowed the seat. With no such instruction, the deliverable is returned in the conversation and a file is written only where the user asks, at the path they name. Called on its own, this skill persists its own department's records; in a company-wide run, the administration skill persists that run's results. No record ever holds a secret's value: it holds where the secret lives and who holds it.

## Standing assets

The durable records the department maintains and a run updates rather than re-creates:

- **The systems register**: every tool and platform the company runs, its owner, its access model by role, its admins, how people sign in, the data it holds, where its secrets live, what it connects to, and its backups (`templates/systems-register.md`).
- **The security program**: the access policy, the controls and what each one closes, and the monitoring posture.
- **The runbooks**: the joiner, mover and leaver paths, restoring each critical system, and the incident playbooks.
- **The user's own accounts and devices**, where a private repository made to hold them says so: each account and device, its second factor, where its password and recovery codes live (never what they are), its recovery contact, its backup, and when it was last checked (the personal section of `templates/systems-register.md`).

## Recurring outputs

**Systems register and reference architecture** (the ★ Chief Information Officer; the Platform Engineer drafts the entries).
- Trigger: a new tool or platform, a change to one, an incident, or a review run.
- Completion evidence: every system has one owner, an access model by role, its admins named, its sign-in method, its data's sensitivity, where its secrets live (never their values), what it connects to, and its backup; each choice of system carries a short decision record with the alternatives considered.
- Lands in: the venture's IT records.

**Change plan and threat review** (the Platform Engineer designs; the Security Engineer reviews, blind; the Chief Information Security Officer rules when a material residual remains).
- Trigger: any change to the company's systems: a new tool or integration, an automation, a configuration change, an access-policy change, a new person's or a leaver's accounts.
- Completion evidence: the blast radius mapped; the design reproducible; the rollback and the backup named; each threat rated by exploitability and blast radius with its mitigation; the Security Engineer's verdict; the Chief Information Security Officer's call recorded exactly as given where it fired; every gated step listed with its way back (`templates/change-review.md`).
- Lands in: the venture's IT records, beside the register entry it changes.

**Security ledger for a build** (the Security Engineer, blind to the builder's reasoning; the Chief Information Security Officer rules on a material residual or a request to ship past a block).
- Trigger: anything built that is about to ship (an app, a tool, a script, a skill, an agent, a pull request), every build the research-and-development skill makes, or a build the user asks to have reviewed.
- Completion evidence: the attack surface mapped (inputs, trust boundaries, the adversary, the worst credible case); the exploitable classes reviewed (injection, broken authentication and authorization, exposed secrets, unsafe dependencies, data exposure), with every dependency's risk looked up at its source and dated; each finding with its severity, its exploit path and its fix, ranked by exploitability and blast radius; the checks run named, read-only, in the build's own checkout; a ship-or-block verdict, block while any reachable high-severity flaw stands; a secret found reported by where it is, never what it is (`templates/security-ledger.md`).
- Lands in: the review record of the repository that holds the build, where its instructions keep one; with the research-and-development skill's ★ Head of Research & Development when it borrowed the seat; otherwise the conversation. A block goes back to the builder, who applies the fix; the build is reviewed again before it ships.

**Security program: access policy and controls** (the Chief Information Security Officer sets the policy; the Security Engineer proposes the controls and the monitoring posture).
- Trigger: a new surface, a review run, or an incident's lesson.
- Completion evidence: each control names the threat it closes; the access policy says who may approve which access, where single sign-on and a second factor are required, how admin access is granted and expires, how automations are identified, and how often access is reviewed; security findings are completion evidence, not opinion.
- Lands in: the venture's IT records.

**Access review** (the Security Engineer).
- Trigger: the policy's review cadence, a leaver, a role change, or an incident.
- Completion evidence: every grant matched to a role, a reason and an owner; standing admin, shared accounts, accounts of people who have left and automations running as a person each named; every removal prepared as a gated step.
- Lands in: the venture's IT records, with the removals waiting for the user's yes.

**Runbooks** (the Platform Engineer).
- Trigger: a process that lives in one person's head, a new critical system, or an incident that exposed a gap.
- Completion evidence: runnable step by step, each step checkable; owners named; failure and rollback paths present; a backup that has been restored at least once named as tested, and one that has not named as untested; no secret in the text.
- Lands in: the venture's IT records.

**Incident record** (the Security Engineer for a security incident, the Platform Engineer for an outage; the Chief Information Security Officer for the residual).
- Trigger: any security incident or outage on the company's internal systems, or a hacked account or a lost or stolen device in the user's own life.
- Completion evidence: the timeline; each containment step, with when the user confirmed it; the evidence kept and where; the cause; the eradication and the recovery; the residual and the follow-ups, each with an owner and a date (`templates/incident-record.md`).
- Lands in: the venture's IT records, or for the user's own account a private repository made to hold it, otherwise the conversation. Anything sent outside the company about it is gated (`gated-acts.md`).

## For the user's own life

**Security checkup** (the Security Engineer; the Chief Information Security Officer on any risk the user chooses to carry).
- Trigger: the user asks how safe their accounts are, a breach notice names one of their accounts, a new year, or a hacked account's lesson.
- Completion evidence: the accounts that reset the others (the main email, the phone number, the password manager, the bank) checked first; for each account, whether a second factor is on and of what kind, where its password lives, whether it is reused, where its recovery codes live and who the recovery contact is, all asked as where, never what; the devices' updates, encryption, screen lock and find-my setting; each fix in order of the risk it closes, each change of a password or a factor named as a step the user takes.
- Lands in: the conversation, or the user's own records in a private repository made to hold them.

**Device setup, move or backup plan** (the Platform Engineer).
- Trigger: a new device, a move between devices, a device to sell or give away, or data that lives in one place only.
- Completion evidence: the settings (updates, encryption, screen lock, find-my), what moves to the new device and how, the backup with a second copy kept elsewhere and a restore tested, and wiping the old device prepared as a gated step that waits until the new device and the backup are confirmed.
- Lands in: the conversation, or the user's own records in a private repository made to hold them.

**Scam or phishing read** (the Security Engineer; quick tier).
- Trigger: a message, a call, a text or a link the user is unsure of.
- Completion evidence: the signs read from the message itself (the sender, the link's real destination, the urgency, the ask), the verdict (likely scam, likely genuine, or unsure), and the safe next step (contact the organization through a channel the user already knows, never the one in the message); if the user already clicked, entered a password or paid, the run becomes an incident.
- Lands in: the conversation.

**The user's accounts and devices record** (the ★ Chief Information Officer; the Platform Engineer drafts the entries).
- Trigger: the user asks to keep track of their accounts and devices, or a checkup or an incident shows nobody knows where things live.
- Completion evidence: each account and device with its purpose, its second factor, where its password and recovery codes live, its recovery contact and its backup; who in the family can reach which account if the user cannot (with the legal-and-compliance skill for a will); never a password, a PIN, a recovery code or a security answer.
- Lands in: only a private repository made to hold the user's personal context; otherwise the conversation, for the user to keep.

## What comes from other departments

A deliverable is never built on a missing input; when one is missing, the lead produces or flags it first.

- **The human-resources skill**: the roles, and each joiner, mover and leaver, which the access model and the provisioning paths follow. The person's employment is the human-resources skill's; their accounts are this skill's.
- **The operations-and-logistics skill** (its Vendor Manager): the vendor's selection, contract, cost and renewal. This skill supplies the security and integration read on a tool before it is bought, and runs it after.
- **The legal-and-compliance skill** (its Privacy & Data Protection Counsel): what privacy and data-protection law requires of the data a system holds, any duty to notify after an incident, and a will that says who inherits the user's accounts. This skill implements the controls.
- **The research-and-development skill**: software, a skill or an agent built to a brief; every build comes back here for its security ledger before it ships, and this skill reviews the change to the company's systems when the build is connected or deployed.
- **The quality-assurance skill**: its ★ Head of Quality for the independent verification of a standing record before it lands on a deep run, and its QA Test Engineer for whether a build works.
- **The public-relations skill**: any message about an incident that leaves the company, sent only on the user's yes.
- **The customer-experience skill**: a device's return, repair or warranty claim, and a subscription to cancel.
- **The finance-and-accounting skill**: fraud on a card or a bank account, a credit freeze, and the budget for tools and devices.

The producing order: the roles and the access policy before any access is granted; the vendor chosen before the integration; the blast radius mapped before the design; the threat review before the change ships; the security ledger before a build ships; the backup confirmed before a device is wiped.
