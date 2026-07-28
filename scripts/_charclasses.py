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
INVISIBLE_FAMILIES = (
    (0x00AD, 0x00AD),   # soft hyphen
    (0x034F, 0x034F),   # combining grapheme joiner
    (0x061C, 0x061C),   # Arabic letter mark
    (0x115F, 0x1160),   # Hangul choseong/jungseong fillers
    (0x17B4, 0x17B5),   # Khmer inherent vowels
    (0x180B, 0x180E),   # Mongolian variation selectors and vowel separator
    (0x200B, 0x200F),   # zero width space through right-to-left mark
    (0x202A, 0x202E),   # bidirectional embedding and override
    (0x2060, 0x2064),   # word joiner through invisible plus
    (0x2066, 0x2069),   # bidirectional isolates
    (0x3164, 0x3164),   # Hangul filler
    (0xFEFF, 0xFEFF),   # zero width no-break space, and the byte order mark
    (0xFFA0, 0xFFA0),   # halfwidth Hangul filler
    (0xE0000, 0xE007F),  # tag characters: an invisible ASCII alphabet
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
