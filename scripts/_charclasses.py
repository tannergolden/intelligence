"""Character classes both checkers reject, defined once.

WHY THIS FILE EXISTS. The skill checker rejected invisible characters from the
day it was written; the documentation checker did not. So a hidden-Unicode rule
could be injected into `AGENTS.md` and pass every gate on the way to being
delivered into every consuming repository, while the same bytes inside a
`SKILL.md` were caught. That is the Rules-File-Backdoor shape, and the fix is
not to write the class out twice: a copy is what goes stale.

STANDARD LIBRARY ONLY, like both of its importers. The skill checker ships
inside a composite action that runs in other people's continuous integration,
where a dependency resolution is a network call and a supply chain.
"""

from __future__ import annotations

import re

# Built from CODEPOINTS so this file never contains one of the characters it
# rejects. Each family runs to its end: a range stopping one codepoint short of
# the hazard is the failure this exists to prevent.
#
# The set is deliberately wider than "zero-width space". Bidirectional
# overrides reorder what a reviewer sees against what a parser reads, tag
# characters carry a full invisible ASCII alphabet, and the Hangul and Braille
# fillers render as nothing while counting as word characters.
#
# COVERING THE TAG BLOCK WHILE MISSING THE VARIATION SELECTORS WAS THE HOLE
# THAT MATTERED. They are the same attack one range apart, and the selectors
# are the range the published emoji-smuggling technique actually uses: an
# arbitrary byte string hidden behind a single visible character. The comment
# above also claimed the Braille filler was covered while U+2800 was absent,
# so the reasoning had been right and the table had not.
#
# Controls and the Unicode space family are here for the tree scan rather than
# for documents. `check_tree` exists to catch a hidden directive in a hook
# script or a workflow, and in an executable file an ESC writes an ANSI
# sequence to the operator's terminal on every prompt, while a no-break space
# changes shell word splitting into something that still passes `sh -n`.
#
# EVERY EXCLUSION IS NAMED, because a family quietly left out is how the last
# hole got here. Tab, newline and carriage return are structure rather than
# hazards, and the line splitter never sees the last of them. U+FE0F is the
# emoji presentation selector and sits inside 42 headings in this repository,
# so the family ships without it: 15 of the 16 selectors and all 240 of the
# E0100 block still fail. That one codepoint is a residual channel, named here
# rather than left for someone to discover.
INVISIBLE_FAMILIES = (
    (0x0000, 0x0008),   # C0 controls, up to but not including tab
    (0x000B, 0x000C),   # vertical tab and form feed
    (0x000E, 0x001F),   # the rest of C0, after carriage return
    (0x007F, 0x009F),   # DELETE and the whole C1 block, CSI among them
    (0x00A0, 0x00A0),   # no-break space
    (0x00AD, 0x00AD),   # soft hyphen
    (0x034F, 0x034F),   # combining grapheme joiner
    (0x061C, 0x061C),   # Arabic letter mark
    (0x115F, 0x1160),   # Hangul choseong/jungseong fillers
    (0x17B4, 0x17B5),   # Khmer inherent vowels
    (0x180B, 0x180E),   # Mongolian variation selectors and vowel separator
    (0x2000, 0x200F),   # the space family, then zero width space to RLM
    (0x2028, 0x2029),   # line and paragraph separators
    (0x202A, 0x202F),   # bidirectional overrides, then narrow no-break space
    (0x205F, 0x205F),   # medium mathematical space
    (0x2060, 0x2064),   # word joiner through invisible plus
    (0x2066, 0x2069),   # bidirectional isolates
    (0x2800, 0x2800),   # Braille pattern blank: renders as nothing
    (0x3000, 0x3000),   # ideographic space
    (0x3164, 0x3164),   # Hangul filler
    (0xFE00, 0xFE0E),   # variation selectors 1 to 15. See the U+FE0F note above
    (0xFEFF, 0xFEFF),   # zero width no-break space, and the byte order mark
    (0xFFA0, 0xFFA0),   # halfwidth Hangul filler
    (0xE0000, 0xE007F),  # tag characters: an invisible ASCII alphabet
    (0xE0100, 0xE01EF),  # variation selectors 17 to 256: the smuggling channel
)

INVISIBLE_RE = re.compile(
    "[" + "".join(
        chr(lo) if lo == hi else f"{chr(lo)}-{chr(hi)}"
        for lo, hi in INVISIBLE_FAMILIES
    ) + "]"
)

# Typography the styling standard bans outright, also built from codepoints so
# neither checker's source contains what it rejects. Both shipped once with the
# literal characters in them and failed their own repository on the first run.
BANNED_CHARS = {
    chr(0x2014): "em dash (U+2014)",
    chr(0x2013): "en dash (U+2013)",
    chr(0x2018): "curly opening quote (U+2018)",
    chr(0x2019): "curly closing quote (U+2019)",
    chr(0x201C): "curly opening double quote (U+201C)",
    chr(0x201D): "curly closing double quote (U+201D)",
}
