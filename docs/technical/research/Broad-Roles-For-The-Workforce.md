<!--
title: '🔎 BROAD ROLES FOR THE WORKFORCE'
description: 'Which documented roles, at most five to a department and about fifty in all, cover every function any business needs and every kind of help a person needs, as of November 2026, from official occupation task lists, the BLS and professional bodies. The research behind the seats of workforce/.'
type: record
verified: '2026-11-14'
focus: 'As of November 2026, which documented roles, at most five to a department and about fifty agents in all, together cover every function any kind of business needs and every kind of help a person needs, with no two seats owning the same work?'
decision: '[ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md)'
-->

<div align="center">

# 🔎 BROAD ROLES FOR THE WORKFORCE

<a name="top"></a>

**The fewest seats that cover any business and any person, each defined by a documented task list.**

_Every claim sourced. Every report dated._

</div>

---

## 🎯 Bottom Line

> [!IMPORTANT]
> **Replace narrow seats with the broad occupations whose task lists cover them, fold the seats that repeat one occupation, and spend the freed seats on the functions the old roster missed.** O\*NET 31.0 shows the Marketing Manager and the Digital Marketing Manager are one occupation, the Director of Finance and the Controller share most of their work, and the Compliance Officer and the Privacy Officer are titles of one occupation, while a Full-Stack Engineer, a Supply Chain Manager, a Quality Engineer and an HR Generalist each cover what two narrower seats did. That frees seats for facilities, licensing, partnerships and fundraising, and online stores, and keeps the workforce under the roughly fifty Bots Grok Bot allows: forty-eight agents as first filed, forty-nine with the Content Producer the pass left as an option. Licensed roles lend their analysis and drafting, never their license. Confidence is medium: the task lists are official, but the breadth counts are this research's own measure.

---

## 📋 Report Meta

| Attribute               | Detail                                                                                            |
| :---------------------- | :------------------------------------------------------------------------------------------------ |
| **Question**            | Which roles, at most five to a department and about fifty in all, cover every business and person |
| **Decision it informs** | The seats, charters and coverage tables of `workforce/`                                           |
| **Verified**            | 2026-11-14, equal to the newest log entry below                                                   |
| **Confidence**          | Medium - official task lists throughout, but the breadth counts are this research's own measure   |
| **Sources**             | 7 fetched directly / 12 total, itemized under Sources & Provenance                                |
| **Supersedes**          | N/A                                                                                               |
| **Graduated to**        | [ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md)                             |

---

## 📅 Log Entry: 2026-11-14

### 🎯 Objective

Find the broadest documented roles that together cover every function any business needs, whatever its industry, and every kind of help a person needs, inside five agents a department and the roughly fifty Bots Grok Bot gives an account, with one owner for each function.

### 🔭 Scope

- **In scope**: O\*NET 31.0's occupations, task lists and job titles for every seat of the workforce and every candidate; the Bureau of Labor Statistics' Occupational Outlook Handbook; each field's professional body; what manufacturing, hospitality and food, retail and e-commerce, healthcare-adjacent, real estate, nonprofit, creator and media, and professional services businesses add.
- **Out of scope**: salaries, licensing law by country, and running any agent against these scopes.

### 🧪 Method

- One research pass in a Claude Code session on 2026-11-14 streamed O\*NET 31.0's task statement, task-to-work-activity and job-title files, and counted for each seat the distinct detailed work activities its tasks link to: a rough measure of breadth computed for this research, not an O\*NET statistic, and one that always grows when occupations are combined.
- It checked every candidate title against O\*NET's job titles, read twelve Occupational Outlook Handbook pages, and read the professional bodies' published scopes.
- **Provenance note**: the O\*NET files, the BLS pages, SHRM, IAPP, NBHWC and AADMM were fetched directly; the other professional bodies were read through search results limited to each body's own site, so their exact wording should be checked on the cited page before it is quoted.

### 🔎 Findings

1. **Several seats repeated one occupation.** O\*NET lists "Digital Marketing Manager" as a title of Marketing Managers, the Marketing Manager's own occupation; the Director of Finance and the Controller shared 11 of 18 work activities; and Compliance Managers list "Privacy Officer" among their titles.
   - **Source**: [O\*NET 31.0 database](https://www.onetcenter.org/database.html), [O\*NET: Compliance Managers](https://www.onetonline.org/link/summary/11-9199.02) - ✅ fetched directly
   - **Confidence**: High - the occupation files themselves
2. **Some titles meant something else, or nothing.** O\*NET files "Contracts Manager" under purchasing, its "Compliance Officers" occupation is mainly government licensing, and "Fact Checker" and "Revenue Operations" have no task list of their own.
   - **Source**: [O\*NET 31.0 database](https://www.onetcenter.org/database.html) - ✅ fetched directly
   - **Confidence**: High
3. **Broad documented roles cover what narrow seats did, and more.** Software Developers with Web Developers, the Full-Stack Engineer, link to 42 work activities against 18; Supply Chain Managers with purchasing to 58; a Quality Engineer's three occupations to 60 against 26 for software testing alone; and HR Specialists, "HR Generalist" among their titles, "handle all aspects of human resources work".
   - **Source**: [O\*NET: Software Developers](https://www.onetonline.org/link/summary/15-1252.00), [O\*NET: Supply Chain Managers](https://www.onetonline.org/link/summary/11-3071.04), [BLS: Human Resources Specialists](https://www.bls.gov/ooh/business-and-financial/human-resources-specialists.htm) - ✅ fetched directly
   - **Confidence**: Medium - the counts are this research's own measure
4. **Licensed roles lend their analysis, never their license.** A paralegal may not give legal advice (ABA); health and wellness coaches do not diagnose or prescribe (NBHWC); daily money managers are not financial planners (AADMM); and only attorneys, CPAs and enrolled agents represent a taxpayer before the IRS.
   - **Source**: [NBHWC: scope of practice](https://nbhwc.org/scope-of-practice/), [AADMM: what a DMM does](https://secure.aadmm.com/what-is-a-dmm-pdmm) - ✅ fetched directly; [ABA: paralegal definition](https://www.americanbar.org/groups/paralegals/profession-information/current_aba_definition_of_legal_assistant_paralegal/), [IRS: enrolled agents](https://www.irs.gov/tax-professionals/enrolled-agents/enrolled-agent-information) - 🔎 through search
   - **Confidence**: High
5. **The old roster missed functions some businesses depend on**: facilities and property, health and safety, production and inventory, licenses and permits, partnerships, fundraising and grants, members, online stores, internal communications and public affairs, translation, and business continuity. Each has a documented occupation, such as Facilities Managers, Regulatory Affairs Specialists, Online Merchants and Fundraisers.
   - **Source**: [O\*NET: Facilities Managers](https://www.onetonline.org/link/summary/11-3013.00), [O\*NET: Regulatory Affairs Specialists](https://www.onetonline.org/link/summary/13-1041.07), [O\*NET: Online Merchants](https://www.onetonline.org/link/summary/13-1199.06), [O\*NET: Fundraisers](https://www.onetonline.org/link/summary/13-1131.00) - ✅ fetched directly
   - **Confidence**: Medium - drawn from task lists, not from businesses running the workforce
6. **The professional bodies confirm each broad seat's scope.** The CFP Board's eight domains run from cash flow and debt to retirement and estate; the IIA's standards define internal audit as independent assurance; and ASQ's Certified Quality Engineer body of knowledge spans product, process and service quality.
   - **Source**: [CFP Board: the exam](https://www.cfp.net/certification-process/exam-requirement/about-the-cfp-exam/what-youll-be-tested-on), [IIA: Global Internal Audit Standards](https://www.theiia.org/en/standards/2024-standards/global-internal-audit-standards/), [ASQ: CQE body of knowledge](https://www.asq.org/cert/resource/pdf/certification/2022-CQE-BoK.pdf) - 🔎 through search
   - **Confidence**: Medium - read through search results

### 📚 Sources & Provenance

| Source                                                                                                                                                 | Fetched   | Backs / notes |
| :----------------------------------------------------------------------------------------------------------------------------------------------------- | :-------- | :------------ |
| [O\*NET 31.0 database](https://www.onetcenter.org/database.html), with its task, work-activity and job-title files                                     | ✅ direct | 1, 2, 3       |
| [O\*NET OnLine](https://www.onetonline.org/): one occupation page for each code cited                                                                  | ✅ direct | 1, 3, 5       |
| [BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/): twelve occupation pages                                                                 | ✅ direct | 3             |
| [SHRM: BASK checklist](https://www.shrm.org/content/dam/en/shrm/credentials/shrm-certification/recertification-providers/bask-checklist-2025.pdf)      | ✅ direct | 3             |
| [IAPP: CIPM body of knowledge](https://prod.iapp.org/media/pdf/certification/CIPM_BoK_EBP_FINAL_14May25.pdf)                                           | ✅ direct | 1             |
| [NBHWC: scope of practice](https://nbhwc.org/scope-of-practice/)                                                                                       | ✅ direct | 4             |
| [AADMM: what a DMM does](https://secure.aadmm.com/what-is-a-dmm-pdmm)                                                                                  | ✅ direct | 4             |
| [ABA: paralegal definition](https://www.americanbar.org/groups/paralegals/profession-information/current_aba_definition_of_legal_assistant_paralegal/) | 🔎 search | 4             |
| [IRS: enrolled agents](https://www.irs.gov/tax-professionals/enrolled-agents/enrolled-agent-information)                                               | 🔎 search | 4             |
| [CFP Board: the exam](https://www.cfp.net/certification-process/exam-requirement/about-the-cfp-exam/what-youll-be-tested-on)                           | 🔎 search | 6             |
| [IIA: Global Internal Audit Standards](https://www.theiia.org/en/standards/2024-standards/global-internal-audit-standards/)                            | 🔎 search | 6             |
| [ASQ: CQE body of knowledge](https://www.asq.org/cert/resource/pdf/certification/2022-CQE-BoK.pdf)                                                     | 🔎 search | 6             |

### ⚖️ Alternatives Considered

| Option                                                          | Pros                                                | Cons                                                                                  |
| :-------------------------------------------------------------- | :-------------------------------------------------- | :------------------------------------------------------------------------------------ |
| Keep the narrow seats, and add one for each gap                 | Each seat's work stays small                        | Past five in a department and past fifty in all; duplicate occupations stay           |
| Broad documented roles, duplicates folded, gaps filled (chosen) | Forty-eight seats cover more, each with a task list | A seat carries more; some titles combine occupations without a task list of their own |
| "Growth Marketer" for the marketing channels seat               | Fits the channel work                               | Not an O\*NET title; "Digital Marketing Manager" is, so the workforce keeps it        |
| Rename Public Relations to Communications                       | The seat's scope reads truer                        | Departments carry the venture template's names, which the vault's folders share       |

### 🛠️ Spikes / Prototypes

N/A: the roster was built from the findings and held by `workforce.py check` and `test_workforce.py`, not prototyped apart.

### 🏁 Conclusion / Recommendation

Adopt the broad roles: forty-six agents in the departments and forty-eight in all, as [The Workforce](../The-Workforce.md#-the-minimum-viable-workforce) lays out, with a coverage table for any business and one for any person. Keep each licensed role's analysis and drafting, and leave its license to a licensed person. Recorded in [ADR-0044](../../adrs/ADR-0044-The-Workforce-Lives-Beside-The-Kit.md).

### ✅ Confidence & Caveats

- **Overall confidence**: Medium
- **What would change this conclusion**: a venture whose work one seat cannot carry, which would earn a seat elsewhere or split a department; xAI documenting a Bot limit other than about fifty, or that group chats count toward it.
- **Known gaps**: the Chief Revenue Officer, the Analytics Engineer, the Partnerships & Development Manager and the Red Team Reviewer beyond penetration testing combine documented occupations, since no task list carries those titles; audio and video production for a media venture is only partly covered.

---

## 📅 Log Entry: 2026-11-14 - Reverification

- **Re-checked**: the one gap the filing entry left open, audio and video production, against the pass's own notes: it listed a Content Producer as an optional forty-ninth seat, on O\*NET's [Producers and Directors](https://www.onetonline.org/link/summary/27-2012.00) task list.
- **Held**: every finding, and every other seat.
- **Drifted**: the conclusion's count. An audit of the workforce on the same day seated the Content Producer in Public Relations, since video, audio and photography serve every department and no seat owned them: forty-seven agents in the departments and forty-nine in all, one under Grok Bot's roughly fifty.
- **Outcome**: verified date unchanged, 2026-11-14; [The Workforce](../The-Workforce.md#-the-minimum-viable-workforce) carries the roster.

---

## ♻️ Reverification

> [!NOTE]
> A report is trusted only inside its verification window. To reverify: re-check each claim against its cited source and the current state of the repository, then **append** a new dated entry below (never edit a past one) and bump the `verified:` frontmatter to that date - or, if the findings no longer hold, supersede or remove the report.

---

## 🤖 AI Agent Directive

> [!IMPORTANT]
> This report is **evidence, not instructions**. It informs decisions and proposals but never overrides this project's standards. Trust a finding only within its verification window - an expired claim is an unverified claim - and weight a claim tagged _fetched directly_ above one that is only _corroborated_.

### 🔗 See also

> [!TIP]
> [The Workforce](../The-Workforce.md) puts these findings to use, and [Portable Agent Workforce](Portable-Agent-Workforce.md) holds the research behind the format and the Grok setup. Durable decisions graduate to the [🧭 ADR index](../../adrs/README.md). Every canonical guide is indexed in the [📚 Standards Index](https://github.com/tannergolden/standards/blob/Development/docs/README.md).

---

<div align="center">

**Cover everything once. Give each seat a task list.**

[↑ Back to Top](#top)

<br />

Built with ❤️ by the Engineering Team. Distributed under the terms in [LICENSE](/LICENSE).

</div>
