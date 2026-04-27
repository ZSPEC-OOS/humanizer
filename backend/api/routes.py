from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from humanizer_lab.ai_client import AIClient
from humanizer_lab.converter import Converter
from humanizer_lab.models import PairExample
from humanizer_lab.rule_bank import RuleBank
from humanizer_lab.rule_extractor import extract_rules
from humanizer_lab.storage import load_profile, save_profile

router = APIRouter(prefix="/api")


class HumanizeRequest(BaseModel):
    text: str
    mode: str = "hybrid"
    audience: str = "general"
    tone: str = "neutral"
    strength: float = 0.6


class AnalyzePairRequest(BaseModel):
    ai_text: str
    human_text: str
    domain: str = "general"
    audience: str = "general"
    tone: str = "neutral"


class ConfigRequest(BaseModel):
    provider: str
    base_url: str
    api_key: str
    model_id: str
    temperature: float
    max_tokens: int
    timeout: int


@router.post("/humanize")
def humanize(req: HumanizeRequest):
    profile = load_profile()
    rb = RuleBank(profile)
    ai = AIClient() if req.mode in {"ai", "hybrid"} else None
    converter = Converter(rb, ai)
    return converter.convert(req.text, mode=req.mode, audience=req.audience, tone=req.tone, strength=req.strength)


@router.post("/analyze-pair")
def analyze_pair(req: AnalyzePairRequest):
    example = PairExample(example_id="api", ai_text=req.ai_text, human_text=req.human_text, domain=req.domain, audience=req.audience, tone=req.tone)
    result = extract_rules(example)
    return result


@router.post("/score")
def score(req: HumanizeRequest):
    profile = load_profile()
    rb = RuleBank(profile)
    converter = Converter(rb, AIClient())
    return converter.ai_score(req.text)


@router.get("/rules")
def get_rules():
    return load_profile()


@router.post("/rules/update")
def update_rules(rules_payload: dict):
    try:
        profile = load_profile().model_copy(update=rules_payload)
        save_profile(profile)
        return {"status": "ok", "rules": profile.rules}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/config")
def get_config():
    return AIClient().config


@router.post("/config")
def set_config(req: ConfigRequest):
    import json
    from pathlib import Path

    Path("config").mkdir(exist_ok=True)
    Path("config/model_config.json").write_text(json.dumps(req.model_dump(), indent=2), encoding="utf-8")
    return {"status": "saved"}


@router.post("/test-model")
def test_model():
    client = AIClient()
    try:
        out = client.rewrite("Reply with: ok")
        return {"status": "ok", "response": out}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
