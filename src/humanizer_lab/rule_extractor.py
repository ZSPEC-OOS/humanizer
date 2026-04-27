from __future__ import annotations

import uuid
from .analyzer import analyze_text
from .models import ComparisonResult, HumanizationRule, PairExample


def _mk_rule(text: str, category: str, confidence: float, evidence: str, example_id: str) -> HumanizationRule:
    return HumanizationRule(
        rule_id=str(uuid.uuid4()),
        rule=text,
        category=category,  # type: ignore[arg-type]
        confidence=round(confidence, 3),
        evidence=evidence,
        source_example=example_id,
        provenance=[example_id],
    )


def extract_rules(example: PairExample) -> ComparisonResult:
    ai = analyze_text(example.ai_text)
    human = analyze_text(example.human_text)
    changes: list[str] = []
    rules: list[HumanizationRule] = []

    if human.avg_sentence_length < ai.avg_sentence_length:
        changes.append("Human text uses shorter sentences")
        rules.append(_mk_rule("Simplify long sentences into shorter units.", "syntax", 0.82, "Lower avg sentence length", example.example_id))
    if human.paragraph_density > ai.paragraph_density:
        changes.append("Human text increases paragraph segmentation")
        rules.append(_mk_rule("Split dense blocks into digestible paragraphs.", "structure", 0.79, "Higher paragraph density", example.example_id))
    if human.definition_markers > ai.definition_markers:
        changes.append("Human text adds clarifying definitions")
        rules.append(_mk_rule("Define specialized terms at first mention.", "explanation", 0.85, "More definition markers", example.example_id))
    if human.transition_frequency >= ai.transition_frequency:
        changes.append("Human text improves flow with transitions")
        rules.append(_mk_rule("Add explicit transitions between ideas.", "structure", 0.68, "Higher transition frequency", example.example_id))
    if human.abstraction_density <= ai.abstraction_density:
        changes.append("Human text reduces abstract phrasing")
        rules.append(_mk_rule("Prefer concrete wording over abstract phrasing.", "tone", 0.74, "Lower abstraction density", example.example_id))
    if human.lexical_diversity >= ai.lexical_diversity * 0.95:
        rules.append(_mk_rule("Preserve domain vocabulary while improving clarity.", "tone", 0.61, "Vocabulary overlap retained", example.example_id))

    return ComparisonResult(
        example_id=example.example_id,
        ai_stats=ai,
        human_stats=human,
        detected_changes=changes,
        candidate_rules=rules,
    )
