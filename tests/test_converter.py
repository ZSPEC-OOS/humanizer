from humanizer_lab.converter import Converter
from humanizer_lab.models import HumanizationProfile, HumanizationRule
from humanizer_lab.rule_bank import RuleBank


def test_converter_integrity_rule_mode():
    profile = HumanizationProfile(rules=[
        HumanizationRule(rule_id="1", rule="Split dense blocks into digestible paragraphs.", category="structure", confidence=0.8, evidence="", source_example="ex")
    ])
    out = Converter(RuleBank(profile)).convert("Alpha. Beta.", mode="rule")
    assert out.original_text
    assert out.rewritten_text
    assert out.score_before and out.score_after
