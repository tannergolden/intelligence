# Portability

A skill is authored once and read by several tools that agree on very little beyond the two required fields. Everything here is a way a skill can work perfectly for its author and do nothing for a colleague.

## The directory a skill is installed into differs

There is no path every tool reads. A skill is copied into whichever directory the reader's tool looks in, which is why skills are installed rather than committed into every repository: committing them for two tools would mean two copies that drift.

Nothing in the skill itself should assume a path. If the body needs to point at a bundled file, point at it relative to the skill directory, never at an absolute location and never at a vendor directory by name.

## Frontmatter beyond the two required fields is ignored somewhere

Only `name` and `description` are read everywhere. Everything else is either optional and portable (`license`, `compatibility`, `metadata`) or implemented by one tool and dropped by the rest. See `frontmatter.md` for the full split.

The rule that follows: a skill using any single-tool field declares that with `compatibility`. Not because the field is dangerous, but because the skill's behaviour is now conditional on who read it, and a reader deserves to know that from the file rather than from a bug report.

## Two content forms behave differently, and both are invisible

**A bang immediately followed by a backticked command**, and the fenced form of the same thing, are executed as shell by one supported tool before the model ever sees the file, and are literal characters everywhere else. The tool that runs it produces a grounded answer; the tools that do not print punctuation. It is a genuine feature, not a typo, so the rule is not "never": a skill using it declares itself with `compatibility`.

**An at sign followed by a path**, with whitespace before it, is an import in every supported tool. It pulls the target file into context, and where the target cannot be resolved it can replace the token with a comment, deleting whatever instruction shared that line. There is no declaration that makes this safe in a skill, because the failure is silent and lands in a repository you have never seen. Rewrite the line.

## Invisible characters

Zero-width spaces, bidirectional controls, and format characters that render as nothing are the only defect class in instruction text that a human provably cannot catch by reading the diff. They arrive by paste, from documents, chat clients and web pages. The checker rejects them; do not disable that rule to make a paste work.

## Every bundled file is part of the deal

At least one supported tool adds the folder structure to context and grants the model access to the entire skill directory on activation. A file nobody references still costs context, and it widens what the user is asked to approve.

So: reference every file from `SKILL.md`, with a sentence saying when to load it, or delete the file. A reference file named without a trigger gets read always or never, and neither is what you wanted.
