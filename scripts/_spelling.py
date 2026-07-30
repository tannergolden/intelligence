"""The one spelling variant this repository has actually drifted into, twice.

WHY THIS EXISTS. Every document here is American, matching the sibling
publisher it is built alongside. Nothing enforced that, so British spellings
arrived twice: once across twelve files, and again in three skill references
written after the first sweep. Both times a person had to notice, and the
second time proved the first sweep was a one-off rather than a fix.

A SPELL CHECKER CANNOT DO THIS. Both spellings are correct English, so the
shared continuous integration's dictionary pass sees nothing wrong. What is
wrong is the inconsistency, and only a list of pairs can decide that.

DELIBERATELY NARROW. Every entry is a word with no American homograph, so the
rule cannot fire on correct text:

  * `analyses` is absent. It is the American plural of "analysis", so only the
    verb forms `analyse`, `analysed` and `analysing` are listed.
  * `licence` is absent. `LICENCE` is a real filename a third party may ship,
    and this module's own importer names it to exempt exactly that.
  * `towards`, `amongst` and `burnt` are absent. All three are ordinary in
    American English, so flagging them would be a house style rather than a
    consistency rule. `amongst` was in the table anyway, three lines below
    the sentence saying it must not be, and it is the entry that sorts first
    so it was also the canary both self-tests reached for.

Adding a pair is cheap. Adding one that fires on correct text is how a gate
gets switched off, so the bar is that the British form has no American reading.
"""

from __future__ import annotations

import re

BRITISH_SPELLINGS = {
    # The -our family. None has an American reading.
    "behaviour": "behavior", "behaviours": "behaviors",
    "colour": "color", "coloured": "colored", "colours": "colors",
    "favour": "favor", "favoured": "favored", "favours": "favors",
    "flavour": "flavor", "flavours": "flavors",
    "honour": "honor", "honoured": "honored",
    "humour": "humor", "labour": "labor",
    "neighbour": "neighbor", "neighbours": "neighbors",
    "neighbouring": "neighboring", "neighbourhood": "neighborhood",
    "rumour": "rumor", "endeavour": "endeavor",
    # -ise where American uses -ize. The noun forms are identical in both, so
    # only the verb and participle forms appear.
    "organise": "organize", "organised": "organized",
    "organising": "organizing", "organisation": "organization",
    "recognise": "recognize", "recognised": "recognized",
    "optimise": "optimize", "optimised": "optimized",
    "optimising": "optimizing",
    "normalise": "normalize", "normalised": "normalized",
    "prioritise": "prioritize", "prioritised": "prioritized",
    "summarise": "summarize", "summarised": "summarized",
    "categorise": "categorize", "categorised": "categorized",
    "standardise": "standardize", "standardised": "standardized",
    "specialise": "specialize", "specialised": "specialized",
    "minimise": "minimize", "minimised": "minimized",
    "maximise": "maximize", "maximised": "maximized",
    "utilise": "utilize", "utilised": "utilized",
    "criticise": "criticize", "criticised": "criticized",
    "emphasise": "emphasize", "emphasised": "emphasized",
    "analyse": "analyze", "analysed": "analyzed", "analysing": "analyzing",
    # Doubled consonants.
    "travelling": "traveling", "travelled": "traveled",
    "modelling": "modeling", "modelled": "modeled",
    "cancelling": "canceling", "cancelled": "canceled",
    "labelling": "labeling", "labelled": "labeled",
    "signalling": "signaling", "signalled": "signaled",
    "fuelled": "fueled",
    # The rest, each unambiguous.
    "centre": "center", "centres": "centers", "centred": "centered",
    "defence": "defense", "offence": "offense", "pretence": "pretense",
    "practise": "practice", "practised": "practiced",
    "fulfil": "fulfill", "fulfilment": "fulfillment",
    "whilst": "while",
    "learnt": "learned", "spelt": "spelled",
    "programme": "program", "programmes": "programs",
    "grey": "gray",
}

BRITISH_RE = re.compile(
    r"\b(" + "|".join(sorted(BRITISH_SPELLINGS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE)


def british_hits(line: str):
    """Every British spelling on one line, as (found, american) pairs."""
    return [(m.group(), BRITISH_SPELLINGS[m.group().lower()])
            for m in BRITISH_RE.finditer(line)]
