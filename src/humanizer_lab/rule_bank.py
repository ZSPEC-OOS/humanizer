from __future__ import annotations

from collections import defaultdict
from .models import HumanizationProfile, HumanizationRule


class RuleBank:
    def __init__(self, profile: HumanizationProfile | None = None):
        self.profile = profile or HumanizationProfile()

    def add_rules(self, rules: list[HumanizationRule]) -> None:
        self.profile.rules.extend(rules)
        self.profile.rules = self.merge_similar(self.profile.rules)

    def merge_similar(self, rules: list[HumanizationRule]) -> list[HumanizationRule]:
        grouped: dict[tuple[str, str], list[HumanizationRule]] = defaultdict(list)
        for rule in rules:
            key = (rule.category, rule.rule.strip().lower())
            grouped[key].append(rule)

        merged: list[HumanizationRule] = []
        for (_, _), members in grouped.items():
            base = members[0].model_copy(deep=True)
            base.confidence = round(sum(m.confidence for m in members) / len(members), 3)
            prov: list[str] = []
            for m in members:
                prov.extend(m.provenance or [m.source_example])
            base.provenance = sorted(set(prov))
            merged.append(base)
        return merged

    def set_enabled(self, rule_id: str, enabled: bool) -> bool:
        for rule in self.profile.rules:
            if rule.rule_id == rule_id:
                rule.enabled = enabled
                return True
        return False

    def export_framework(self) -> dict:
        return self.profile.model_dump()

    def prompt_rules(self) -> list[str]:
        return [r.rule for r in self.profile.rules if r.enabled]
