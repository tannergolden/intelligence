# Deliverables - what the IT department produces, and where it lands

The producing map for every `systems` run: each deliverable, the seat that produces it, what triggers it, the completion evidence it must carry before it lands, and where it goes. Read it with `dispatch.md`, which sets who runs in what order, and `gated-acts.md`, which sets what waits for the user's yes. The standard is the team's: **secure by default, reversible by design**.

## Where the work lands

A venture's department records go where the repository's own instructions keep them: the venture's **Information Technology (IT) records**, in whatever folder and files those instructions name (a repository with a venture template maps each deliverable below onto its own files). With no such instruction, the deliverable is returned in the conversation and a file is written only where the user asks, at the path they name. Called on its own, this skill persists its own department's records; in a board run, the board skill persists that run's results. No record ever holds a secret's value: it holds where the secret lives and who holds it.

## Standing assets

The durable records the department maintains and a run updates rather than re-creates:

- **The systems register**: every tool and platform the company runs, its owner, its access model by role, its admins, how people sign in, the data it holds, where its secrets live, what it connects to, and its backups (`templates/systems-register.md`).
- **The security program**: the access policy, the controls and what each one closes, and the monitoring posture.
- **The runbooks**: the joiner, mover and leaver paths, restoring each critical system, and the incident playbooks.

## Recurring outputs

**Systems register and reference architecture** (the ★ Chief Information Officer; the Platform Engineer drafts the entries).
- Trigger: a new tool or platform, a change to one, an incident, or a review run.
- Completion evidence: every system has one owner, an access model by role, its admins named, its sign-in method, its data's sensitivity, where its secrets live (never their values), what it connects to, and its backup; each choice of system carries a short decision record with the alternatives considered.
- Lands in: the venture's IT records.

**Change plan and threat review** (the Platform Engineer designs; the Security Engineer reviews, blind; the Chief Information Security Officer rules when a material residual remains).
- Trigger: any change to the company's systems: a new tool or integration, an automation, a configuration change, an access-policy change, a new person's or a leaver's accounts.
- Completion evidence: the blast radius mapped; the design reproducible; the rollback and the backup named; each threat rated by exploitability and blast radius with its mitigation; the Security Engineer's verdict; the Chief Information Security Officer's call recorded exactly as given where it fired; every gated step listed with its way back (`templates/change-review.md`).
- Lands in: the venture's IT records, beside the register entry it changes.

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
- Trigger: any security incident or outage on the company's internal systems.
- Completion evidence: the timeline; each containment step, with when the user confirmed it; the evidence kept and where; the cause; the eradication and the recovery; the residual and the follow-ups, each with an owner and a date (`templates/incident-record.md`).
- Lands in: the venture's IT records. Anything sent outside the company about it is gated (`gated-acts.md`).

## What comes from other departments

A deliverable is never built on a missing input; when one is missing, the lead produces or flags it first.

- **The people skill**: the roles, and each joiner, mover and leaver, which the access model and the provisioning paths follow. The person's employment is people's; their accounts are this skill's.
- **The operations skill** (its Vendor Manager): the vendor's selection, contract, cost and renewal. This skill supplies the security and integration read on a tool before it is bought, and runs it after.
- **The legal skill** (its Privacy & Data Protection Counsel): what privacy and data-protection law requires of the data a system holds, and any duty to notify after an incident. This skill implements the controls.
- **The develop skill**: software, a skill or an agent built to a brief, reviewed by its own Application Security Engineer. This skill reviews the change to the company's systems when the build is connected or deployed.
- **The quality skill's ★ Head of Quality**: the independent verification of a standing record before it lands on a deep run.
- **The communications skill**: any message about an incident that leaves the company, sent only on the user's yes.

The producing order: the roles and the access policy before any access is granted; the vendor chosen before the integration; the blast radius mapped before the design; the threat review before the change ships.
