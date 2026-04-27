from humanizer_lab.models import HumanizationRule
from humanizer_lab.rule_bank import RuleBank


def test_rule_merge():
    rb = RuleBank()
    r1 = HumanizationRule(rule_id="1", rule="Split dense blocks.", category="structure", confidence=0.8, evidence="a", source_example="x")
    r2 = HumanizationRule(rule_id="2", rule="Split dense blocks.", category="structure", confidence=0.6, evidence="b", source_example="y")
    merged = rb.merge_similar([r1, r2])
    assert len(merged) == 1
    assert merged[0].confidence == 0.7
