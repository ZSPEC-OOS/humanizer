from humanizer_lab.analyzer import analyze_text


def test_analyzer_basic_metrics():
    stats = analyze_text("First sentence. Second sentence with (note).")
    assert stats.word_count >= 6
    assert stats.sentence_count == 2
    assert 0 <= stats.lexical_diversity <= 1
