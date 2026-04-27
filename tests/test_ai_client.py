from humanizer_lab.ai_client import AIClient


def test_ai_client_score_fallback(monkeypatch):
    client = AIClient()

    def fake_request(prompt: str):
        return "not json"

    monkeypatch.setattr(client, "_request", fake_request)
    data = client.score("x")
    assert "ai_likeness" in data
