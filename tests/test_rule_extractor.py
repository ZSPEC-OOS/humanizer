from humanizer_lab.models import PairExample
from humanizer_lab.rule_extractor import extract_rules


def test_extract_rules_returns_candidates():
    ex = PairExample(example_id="e1", ai_text="This is a dense paragraph with abstract framework optimization.", human_text="This is simpler.\nIt defines framework means structure.")
    result = extract_rules(ex)
    assert result.example_id == "e1"
    assert len(result.candidate_rules) > 0
