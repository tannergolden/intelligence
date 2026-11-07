# Systems register

<!-- The standing inventory of what the company runs, kept by the ★ Chief Information Officer with entries drafted by
     the Platform Engineer. One row per tool or platform; a change updates its row. Never write a secret's value here:
     the Secrets column names where each one lives and who holds it. The vendor's contract and cost live in the
     operations-and-logistics skill's vendor register; this register names the vendor only. The section for the user's
     own accounts and devices is kept only in a private repository made to hold the user's personal context; anywhere
     else it stays in the conversation, for the user to keep. -->

- **As of:** <YYYY-MM-DD>
- **Access policy:** <where the current access policy is kept>

| System | Purpose | Owner | Access by role | Admins | Sign-in | Data held | Secrets (where they live) | Connects to | Backup | Next access review |
| :----- | :------ | :---- | :------------- | :----- | :------ | :-------- | :------------------------ | :---------- | :----- | :----------------- |
| <tool> | <what the company uses it for> | <one person or role> | <roles or groups, and what each may do> | <named, as few as the work allows> | <single sign-on, second factor> | <kind and sensitivity> | <store, holder> | <other systems> | <what, how often, last restored> | <date> |

## The user's own accounts and devices

<!-- Never a password, a PIN, a recovery code or a security answer: only where each lives. The accounts that reset the
     others (the main email, the phone number, the password manager, the bank) come first. -->

| Account or device | Purpose | Second factor (kind) | Where the password lives | Where the recovery codes live | Recovery contact | Backup | Who else can reach it | Last checked |
| :---------------- | :------ | :------------------- | :----------------------- | :---------------------------- | :--------------- | :----- | :-------------------- | :----------- |
| <the main email account> | <what it is for> | <passkey, hardware key, authenticator app, text code, none> | <the password manager> | <where they are kept, offline> | <the person or method, by role> | <what, where, last restored> | <the sharing feature or legacy contact, by role> | <date> |

## Decision records

<One short entry per choice of system: the date, what was chosen, the alternatives considered, why, and what would make the company revisit it.>
