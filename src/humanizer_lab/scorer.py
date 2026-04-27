from __future__ import annotations

from .analyzer import analyze_text


def heuristic_score(text: str) -> dict:
    stats = analyze_text(text)
    uniformity = min(stats.avg_sentence_length / 28, 1)
    abstraction_penalty = stats.abstraction_density
    repetition_penalty = stats.repetition_ratio
    simplicity = max(0.0, min(1.0, 1 - abs(stats.avg_sentence_length - 18) / 18))

    ai_likeness = round(min(1.0, 0.4 * uniformity + 0.3 * abstraction_penalty + 0.3 * repetition_penalty), 3)
    readability = round(max(0.0, min(1.0, 0.6 * simplicity + 0.4 * stats.lexical_diversity)), 3)
    return {
        "ai_likeness": ai_likeness,
        "readability": readability,
        "humanization_strength": round(1 - ai_likeness, 3),
        "issues": [],
    }
