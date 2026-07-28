---
name: replace-with-directory-name
description: Use this skill when the user <the situation, in their words>, or when they <the symptom they would describe instead>. Applies even when they do not say <the domain word>.
---

## Steps

1. The first action, imperative and standing rather than narrated.
2. The second. This text persists for the whole session once loaded, so every
   line is paid repeatedly.
3. Validate the result against <the source of truth> before moving on.

## Gotchas

Keep these in the body, not a reference: they have to be read *before* the
situation arrives, not after it goes wrong.

- The environment-specific fact an agent cannot infer.
- The call that reports success on failure.

## Output template

Give the shape rather than describing it. Agents match a concrete structure far
more reliably than a paragraph about one.

```text
<the exact shape the result should take>
```

## Additional resources

Name the **condition**, not just the subject. A resource listed by subject alone
gets read always or never.

- `references/<topic>.md` - read this if <the condition that makes it relevant>.
