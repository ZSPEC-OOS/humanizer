from __future__ import annotations

import re
from collections import Counter
from .models import TextStats

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"\b[a-zA-Z][\w'-]*\b")
TRANSITIONS = ["however", "therefore", "for example", "first", "next", "finally", "in addition"]
DEFINITION_MARKERS = ["is", "refers to", "means", "defined as", "known as"]
ABSTRACT_WORDS = ["framework", "paradigm", "optimization", "efficiency", "robust", "scalable"]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(text.strip()) if s.strip()]


def _words(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def analyze_text(text: str) -> TextStats:
    sentences = _sentences(text)
    words = _words(text)
    paragraphs = [p for p in text.split("\n") if p.strip()]
    wc = len(words)
    sc = max(len(sentences), 1)
    counts = Counter(words)
    repeated = sum(v for v in counts.values() if v > 1)

    return TextStats(
        word_count=wc,
        sentence_count=len(sentences),
        avg_sentence_length=round(wc / sc, 3),
        paragraph_density=round(len(paragraphs) / sc, 3),
        parenthetical_usage=round((text.count("(") + text.count(")")) / max(wc, 1), 3),
        transition_frequency=round(sum(text.lower().count(t) for t in TRANSITIONS) / sc, 3),
        definition_markers=sum(text.lower().count(m) for m in DEFINITION_MARKERS),
        abstraction_density=round(sum(words.count(w) for w in ABSTRACT_WORDS) / max(wc, 1), 3),
        lexical_diversity=round(len(set(words)) / max(wc, 1), 3),
        repetition_ratio=round(repeated / max(wc, 1), 3),
    )
