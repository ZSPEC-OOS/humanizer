from __future__ import annotations

import json
import os
from pathlib import Path
from urllib import request, error


class AIClient:
    def __init__(self, config_path: str = "config/model_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        with self.config_path.open("r", encoding="utf-8") as f:
            config = json.load(f)
        config["base_url"] = os.getenv("MODEL_BASE_URL", config["base_url"])
        config["api_key"] = os.getenv("MODEL_API_KEY", config["api_key"])
        config["model_id"] = os.getenv("MODEL_ID", config["model_id"])
        return config

    def _request(self, prompt: str) -> str:
        url = f"{self.config['base_url'].rstrip('/')}/chat/completions"
        payload = {
            "model": self.config["model_id"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.config.get("temperature", 0.4),
            "max_tokens": self.config.get("max_tokens", 2000),
        }
        req = request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config['api_key']}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.config.get("timeout", 30)) as resp:  # noqa: S310
                body = resp.read().decode("utf-8")
            data = json.loads(body)
            return data["choices"][0]["message"]["content"]
        except (error.URLError, error.HTTPError, KeyError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"AI request failed: {exc}") from exc

    def rewrite(self, prompt: str) -> str:
        return self._request(prompt)

    def score(self, prompt: str) -> dict:
        raw = self._request(prompt)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "ai_likeness": 0.5,
                "readability": 0.5,
                "humanization_strength": 0.5,
                "issues": ["Model did not return valid JSON."],
            }
