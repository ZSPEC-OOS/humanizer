from __future__ import annotations


def build_rewrite_prompt(text: str, rules: list[str], audience: str, tone: str, strength: float) -> str:
    numbered = "\n".join(f"{idx + 1}. {rule}" for idx, rule in enumerate(rules)) or "1. Preserve meaning and improve clarity."
    return (
        "SYSTEM:\n"
        "You are a humanization engine.\n\n"
        f"RULES:\n{numbered}\n\n"
        "TASK:\n"
        f"Rewrite for audience={audience}, tone={tone}, strength={strength:.2f}.\n\n"
        "OUTPUT REQUIREMENTS:\n"
        "- preserve meaning\n- improve clarity\n- reduce AI-like phrasing\n"
        "- define technical terms when needed\n\n"
        f"INPUT TEXT:\n{text}\n"
    )


def build_scoring_prompt(text: str) -> str:
    return (
        "Score this text as JSON with ai_likeness/readability/humanization_strength (0-1) and issues list.\n"
        f"TEXT:\n{text}"
    )
