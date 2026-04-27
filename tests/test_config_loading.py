from humanizer_lab.ai_client import AIClient


def test_config_loading_env_override(monkeypatch):
    monkeypatch.setenv("MODEL_ID", "override-model")
    client = AIClient()
    assert client.config["model_id"] == "override-model"
