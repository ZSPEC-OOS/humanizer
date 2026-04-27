from __future__ import annotations

import argparse
import uuid
from .ai_client import AIClient
from .converter import Converter
from .models import PairExample
from .rule_bank import RuleBank
from .rule_extractor import extract_rules
from .storage import load_examples, load_profile, save_examples, save_profile


def cmd_add_example() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai-text", required=True)
    parser.add_argument("--human-text", required=True)
    parser.add_argument("--domain", default="general")
    parser.add_argument("--audience", default="general")
    parser.add_argument("--tone", default="neutral")
    args = parser.parse_args()

    examples = load_examples()
    ex = PairExample(example_id=str(uuid.uuid4()), ai_text=args.ai_text, human_text=args.human_text, domain=args.domain, audience=args.audience, tone=args.tone)
    examples.append(ex)
    save_examples(examples)
    print(ex.example_id)


def cmd_analyze_pair() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai-text", required=True)
    parser.add_argument("--human-text", required=True)
    args = parser.parse_args()
    ex = PairExample(example_id="cli", ai_text=args.ai_text, human_text=args.human_text)
    print(extract_rules(ex).model_dump_json(indent=2))


def cmd_humanize() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--mode", choices=["rule", "ai", "hybrid"], default="hybrid")
    args = parser.parse_args()
    rb = RuleBank(load_profile())
    ai = AIClient() if args.mode in {"ai", "hybrid"} else None
    print(Converter(rb, ai).convert(args.text, mode=args.mode).model_dump_json(indent=2))


def cmd_score() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    rb = RuleBank(load_profile())
    print(Converter(rb).ai_score(args.text))


def cmd_export_prompt() -> None:
    rb = RuleBank(load_profile())
    print("\n".join(f"- {rule}" for rule in rb.prompt_rules()))


def main() -> None:
    print("Use entrypoint commands: add-example, analyze-pair, humanize, score, export-prompt")
