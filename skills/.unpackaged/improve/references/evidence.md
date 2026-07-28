# Establishing And Grading A Lesson

A lesson enters an instruction file with the authority of a rule and stays there until someone deliberately removes it. Nothing downstream re-checks it. So the bar is not "does this sound right", it is "what actually established this".

## Why this matters more than it looks

An agent's account of why something failed is frequently wrong, and the failure mode is specific: the account is **plausible**, **confident**, and **built from the same reasoning that produced the mistake**. Writing it down converts a bad guess into a permanent instruction that every future agent obeys.

The three failures worth naming, because each has happened:

- **A measurement recalled rather than repeated.** A number remembered from earlier in a session, off by a factor that made a rejected design look better than it was.
- **A file described rather than opened.** A claim about what a file contains, made from a rendering of that file that had already stripped the part in question.
- **A search summary trusted over a primary source.** A confident secondary claim that the vendor's own documentation contradicts, believed twice because the correction was never written down with its source.

Every one of those would have become a permanent rule under a loop with no grading step.

## The three grades

| Grade | What earns it | What the entry must carry |
| :--- | :--- | :--- |
| **probed** | Something ran, here, and you saw the result | The command and the observed output, trimmed but not paraphrased |
| **documented** | A primary source states it | The source, specific enough to re-find, and the date read |
| **unverified** | Believed from a secondary source or from memory | An explicit note that it is a lead, and what would confirm it |

**A primary source is the thing itself**: the vendor's own documentation, the specification, the tool's `--help`, the code. A blog post, a search summary, and an answer you recall are all secondary, however confident.

## Promote rather than assume

An **unverified** lesson is allowed to exist. It is not allowed to be written as a rule.

Record it as a question with the check that would settle it, and promote it when someone runs that check. A lead that says "this may be true, run X to find out" is useful. The same sentence with the hedge removed is a liability.

## Grade the correction, not the story

Write what was true and what to do, not a narrative of how the mistake happened. A future agent needs the fact, and the evidence that it is a fact. It does not need the plot.

**Weak:** "I tried to run the tests but they failed, and after some investigation it turned out the fixtures needed generating first, so I did that."

**Strong:** "The test suite requires generated fixtures. `make test` fails with `fixtures/ not found` until `make fixtures` has run once. (probed, 2026-07-28)"

The second is shorter, checkable, and states the trigger a future agent will actually encounter.

## Date anything that can rot

A version number, a vendor behavior, a URL, an API shape: all of these expire, and nothing tells you when. A dated entry lets a reader judge staleness. An undated one is trusted forever by default.
