from __future__ import annotations

from dataclasses import dataclass, field, asdict, replace
from typing import Any, Literal
import json


@dataclass
class PairExample:
    example_id: str
    ai_text: str
    human_text: str
    domain: str = "general"
    audience: str = "general"
    tone: str = "neutral"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextStats:
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    paragraph_density: float
    parenthetical_usage: float
    transition_frequency: float
    definition_markers: int
    abstraction_density: float
    lexical_diversity: float
    repetition_ratio: float


@dataclass
class HumanizationRule:
    rule_id: str
    rule: str
    category: Literal["syntax", "tone", "structure", "explanation"]
    confidence: float
    evidence: str
    source_example: str
    enabled: bool = True
    provenance: list[str] = field(default_factory=list)

    def model_copy(self, deep: bool = False):
        return replace(self, provenance=list(self.provenance))


@dataclass
class ComparisonResult:
    example_id: str
    ai_stats: TextStats
    human_stats: TextStats
    detected_changes: list[str]
    candidate_rules: list[HumanizationRule]

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent)


@dataclass
class HumanizationProfile:
    profile_id: str = "default"
    rules: list[HumanizationRule] = field(default_factory=list)

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent)

    def model_copy(self, update: dict | None = None):
        data = asdict(self)
        if update:
            data.update(update)
        rules = [HumanizationRule(**r) if isinstance(r, dict) else r for r in data.get("rules", [])]
        return HumanizationProfile(profile_id=data.get("profile_id", "default"), rules=rules)


@dataclass
class RewriteResult:
    original_text: str
    rewritten_text: str
    applied_rules: list[str]
    warnings: list[str] = field(default_factory=list)
    change_log: list[str] = field(default_factory=list)
    score_before: dict[str, float | list[str]] = field(default_factory=dict)
    score_after: dict[str, float | list[str]] = field(default_factory=dict)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent)
