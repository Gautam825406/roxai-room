"""Detection of bot-name mentions in a transcript, tolerant of the specific ASR
misrecognitions the spec calls out (dost/dosth/dast, sathi/saathi/sathee).

We use a curated alias allowlist rather than a generic edit-distance/ratio threshold.
Tried that first: SequenceMatcher ratio for "dast" vs "dost" is 0.75 -- identical to
"cost" vs "dost" and "most" vs "dost". Any cutoff that catches the intended ASR error
also fires on ordinary English words, which is worse than the problem it solves. For a
closed set of two names, an explicit list of known variants is the safer choice; add to
it as new misrecognitions turn up in testing.

The STT providers run in code-mixed Hindi/English mode (Deepgram nova-3 with
`language="multi"`, Sarvam Saarika similarly), so a bot name spoken in Hindi
comes back in Devanagari script (e.g. "साथी"), not a
romanization -- both scripts need aliases or every Hindi-spoken invocation of
the bots is silently dropped by stage-A routing.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

DOST = "dost"
SATHI = "sathi"

DOST_ALIASES = frozenset({"dost", "dosth", "dast", "dosht", "dosdt", "दोस्त"})
SATHI_ALIASES = frozenset(
    {"sathi", "saathi", "sathee", "saathee", "shathi", "sathhi", "साथी", "साथि"}
)


@dataclass(frozen=True)
class BotMention:
    bot: str  # "dost" | "sathi"
    start: int
    end: int


def find_bot_mentions(text: str) -> list[BotMention]:
    mentions: list[BotMention] = []
    for m in re.finditer(r"\S+", text):
        token = m.group().strip(".,?!\"'।॥").lower()
        if token in DOST_ALIASES:
            mentions.append(BotMention(bot=DOST, start=m.start(), end=m.end()))
        elif token in SATHI_ALIASES:
            mentions.append(BotMention(bot=SATHI, start=m.start(), end=m.end()))
    return mentions


def mentioned_bots(text: str) -> frozenset[str]:
    return frozenset(m.bot for m in find_bot_mentions(text))
