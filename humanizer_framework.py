"""
humanizer_framework.py

A lightweight local framework for learning AI→humanized rewrite patterns from paired examples.

Core use case:
    Paste 1 = AI-generated source text
    Paste 2 = humanized target text

The system:
    1. Stores paired examples.
    2. Compares structural, lexical, and explanatory features.
    3. Extracts candidate humanization rules.
    4. Updates a reusable rule bank.
    5. Produces a prompt/checklist for future humanization.

This is intentionally transparent and editable rather than model-dependent.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import re
import statistics


# ----------------------------
# Data structures
# ----------------------------

@dataclass
class PairExample:
    example_id: str
    domain: str
    ai_text: str
    human_text: str
    notes: str = ""


@dataclass
class TextStats:
    word_count: int
    sentence_count: int
    avg_sentence_words: float
    paragraph_count: int
    parenthetical_count: int
    transition_count: int
    technical_marker_count: int
    definition_marker_count: int


@dataclass
class ComparisonResult:
    example_id: str
    domain: str
    ai_stats: TextStats
    human_stats: TextStats
    detected_changes: List[str]
    candidate_rules: List[str]


# ----------------------------
# Utility functions
# ----------------------------

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"\b[\w'-]+\b")

TRANSITIONS = {
    "for example", "in other words", "another", "finally", "at this", "unlike",
    "ultimately", "because", "when", "therefore", "however", "also", "then"
}

DEFINITION_MARKERS = {
    "called", "known as", "which means", "which states", "which describes",
    "refers to", "is the", "are the", "i.e.", "for example", "in other words"
}

TECHNICAL_MARKERS = {
    "equation", "theory", "model", "simulation", "configuration", "molecular",
    "quantum", "genome", "protein", "rna", "dna", "electron", "nuclei",
    "covalent", "ionic", "metallic", "cryptography", "computing", "cas9",
    "crispr", "density functional theory", "systems biology"
}


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    return [s.strip() for s in SENTENCE_RE.split(text) if s.strip()]


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def count_phrases(text: str, phrases: set[str]) -> int:
    lower = text.lower()
    return sum(lower.count(p) for p in phrases)


def analyze_text(text: str) -> TextStats:
    sentences = split_sentences(text)
    words = count_words(text)
    paragraph_count = len([p for p in text.split("\n") if p.strip()])
    avg_sentence_words = words / max(len(sentences), 1)

    return TextStats(
        word_count=words,
        sentence_count=len(sentences),
        avg_sentence_words=round(avg_sentence_words, 2),
        paragraph_count=paragraph_count,
        parenthetical_count=text.count("(") + text.count("["),
        transition_count=count_phrases(text, TRANSITIONS),
        technical_marker_count=count_phrases(text, TECHNICAL_MARKERS),
        definition_marker_count=count_phrases(text, DEFINITION_MARKERS),
    )


# ----------------------------
# Rule extraction
# ----------------------------

def compare_pair(example: PairExample) -> ComparisonResult:
    ai = analyze_text(example.ai_text)
    human = analyze_text(example.human_text)

    changes: List[str] = []
    rules: List[str] = []

    if human.paragraph_count > ai.paragraph_count:
        changes.append("Human version uses more paragraph breaks.")
        rules.append("Break dense AI passages into smaller instructional paragraphs.")

    if human.avg_sentence_words < ai.avg_sentence_words * 0.9:
        changes.append("Human version reduces average sentence length.")
        rules.append("Reduce long AI sentences into shorter explanatory units.")

    if human.parenthetical_count > ai.parenthetical_count:
        changes.append("Human version adds parenthetical clarifications.")
        rules.append("Add parenthetical definitions for technical or abstract terms.")

    if human.definition_marker_count > ai.definition_marker_count:
        changes.append("Human version adds more definition/explanation markers.")
        rules.append("Define key terms immediately after first use.")

    if human.transition_count >= ai.transition_count:
        changes.append("Human version preserves or increases explicit transitions.")
        rules.append("Use direct transitions such as 'for example,' 'another,' and 'finally'.")

    if human.word_count > ai.word_count * 1.05:
        changes.append("Human version expands explanatory detail.")
        rules.append("Expand compressed technical claims with plain-language explanation.")
    elif human.word_count < ai.word_count * 0.95:
        changes.append("Human version compresses some material.")
        rules.append("Remove ornamental phrasing while preserving core concepts.")

    if human.technical_marker_count >= ai.technical_marker_count * 0.75:
        changes.append("Human version retains most technical vocabulary.")
        rules.append("Preserve domain vocabulary, but surround it with explanation.")

    # Always relevant for these paired examples.
    rules.append("Replace rhetorical polish with direct classroom-style explanation.")
    rules.append("Preserve concept order unless the human example shows clearer sequencing.")

    # Deduplicate while preserving order.
    rules = list(dict.fromkeys(rules))
    changes = list(dict.fromkeys(changes))

    return ComparisonResult(
        example_id=example.example_id,
        domain=example.domain,
        ai_stats=ai,
        human_stats=human,
        detected_changes=changes,
        candidate_rules=rules,
    )


def load_reference(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_reference(data: Dict[str, Any], path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_example(
    reference_path: str | Path,
    example_id: str,
    domain: str,
    ai_text: str,
    human_text: str,
    notes: str = "",
) -> ComparisonResult:
    """
    Add a new AI→humanized pair to the reference file and update the rule bank.
    """
    reference_path = Path(reference_path)

    if reference_path.exists():
        data = load_reference(reference_path)
    else:
        data = {
            "framework_version": "0.1",
            "examples": [],
            "rule_bank": [],
            "analysis_log": []
        }

    example = PairExample(
        example_id=example_id,
        domain=domain,
        ai_text=ai_text.strip(),
        human_text=human_text.strip(),
        notes=notes.strip(),
    )

    result = compare_pair(example)

    data["examples"].append(asdict(example))
    data["analysis_log"].append(asdict(result))

    existing_rules = {r["rule"] for r in data.get("rule_bank", [])}
    for rule in result.candidate_rules:
        if rule not in existing_rules:
            data.setdefault("rule_bank", []).append({
                "rule": rule,
                "source_examples": [example_id],
                "status": "active"
            })
            existing_rules.add(rule)
        else:
            for item in data["rule_bank"]:
                if item["rule"] == rule and example_id not in item["source_examples"]:
                    item["source_examples"].append(example_id)

    save_reference(data, reference_path)
    return result


def build_humanizer_prompt(reference_path: str | Path) -> str:
    """
    Convert the current rule bank into a reusable humanization prompt.
    """
    data = load_reference(reference_path)
    active_rules = [
        r["rule"] for r in data.get("rule_bank", [])
        if r.get("status", "active") == "active"
    ]

    numbered = "\n".join(f"{i+1}. {rule}" for i, rule in enumerate(active_rules))

    return f"""HUMANIZER PROMPT GENERATED FROM FRAMEWORK v{data.get("framework_version", "0.1")}

Task:
Rewrite the AI text into a clearer, more humanized version while preserving technical accuracy.

Rules:
{numbered}

Output requirements:
- Preserve all essential concepts.
- Do not invent unsupported facts.
- Prefer explanatory clarity over rhetorical polish.
- Use definitions, examples, and transitions where they improve comprehension.
- Keep technical terms when necessary, but explain them in accessible language.
"""


def diagnostic_report(result: ComparisonResult) -> str:
    """
    Produce a readable report for one comparison result.
    """
    return f"""Example: {result.example_id}
Domain: {result.domain}

AI stats:
- Words: {result.ai_stats.word_count}
- Sentences: {result.ai_stats.sentence_count}
- Average sentence length: {result.ai_stats.avg_sentence_words}
- Paragraphs: {result.ai_stats.paragraph_count}
- Parenthetical clarifications: {result.ai_stats.parenthetical_count}
- Definition markers: {result.ai_stats.definition_marker_count}

Humanized stats:
- Words: {result.human_stats.word_count}
- Sentences: {result.human_stats.sentence_count}
- Average sentence length: {result.human_stats.avg_sentence_words}
- Paragraphs: {result.human_stats.paragraph_count}
- Parenthetical clarifications: {result.human_stats.parenthetical_count}
- Definition markers: {result.human_stats.definition_marker_count}

Detected changes:
{chr(10).join("- " + c for c in result.detected_changes)}

Candidate rules:
{chr(10).join("- " + r for r in result.candidate_rules)}
"""


if __name__ == "__main__":
    # Minimal demonstration.
    reference = Path("humanizer_reference.json")

    print("Humanizer framework module loaded.")
    print("Use add_example(...) to add AI→humanized pairs.")
    print("Use build_humanizer_prompt(...) to generate the current prompt.")
