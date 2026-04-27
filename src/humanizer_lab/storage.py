from __future__ import annotations

import json
from pathlib import Path
from dataclasses import asdict
from .models import HumanizationProfile, PairExample, HumanizationRule


def load_examples(path: str = "data/humanizer_reference.json") -> list[PairExample]:
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [PairExample(**item) for item in data.get("examples", [])]


def save_examples(examples: list[PairExample], path: str = "data/humanizer_reference.json") -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {"examples": [asdict(e) for e in examples]}
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_profile(path: str = "data/rule_bank.json") -> HumanizationProfile:
    p = Path(path)
    if not p.exists():
        return HumanizationProfile()
    raw = json.loads(p.read_text(encoding="utf-8"))
    rules = raw.get("rules", [])
    raw["rules"] = [HumanizationRule(**r) if isinstance(r, dict) else r for r in rules]
    return HumanizationProfile(profile_id=raw.get("profile_id", "default"), rules=raw["rules"])


def save_profile(profile: HumanizationProfile, path: str = "data/rule_bank.json") -> None:
    Path(path).write_text(profile.model_dump_json(indent=2), encoding="utf-8")
