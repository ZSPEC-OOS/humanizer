from __future__ import annotations

from difflib import ndiff
from .ai_client import AIClient
from .models import RewriteResult
from .prompts import build_rewrite_prompt, build_scoring_prompt
from .rule_bank import RuleBank
from .scorer import heuristic_score


class Converter:
    def __init__(self, rule_bank: RuleBank, ai_client: AIClient | None = None):
        self.rule_bank = rule_bank
        self.ai_client = ai_client

    def _rule_preprocess(self, text: str) -> tuple[str, list[str]]:
        changed = text.strip()
        applied: list[str] = []
        for rule in self.rule_bank.profile.rules:
            if not rule.enabled:
                continue
            if "shorter units" in rule.rule.lower() and len(changed.split()) > 25:
                changed = changed.replace(";", ".")
                applied.append(rule.rule)
            if "paragraph" in rule.rule.lower():
                changed = changed.replace(". ", ".\n")
                applied.append(rule.rule)
        return changed, list(dict.fromkeys(applied))

    def convert(self, text: str, mode: str = "hybrid", audience: str = "general", tone: str = "neutral", strength: float = 0.6) -> RewriteResult:
        base_score = heuristic_score(text)
        preprocessed, applied = self._rule_preprocess(text)
        warnings: list[str] = []

        if mode == "rule":
            rewritten = preprocessed
        elif mode == "ai":
            if not self.ai_client:
                raise RuntimeError("AI mode selected but AI client is not configured")
            rewritten = self.ai_client.rewrite(build_rewrite_prompt(text, self.rule_bank.prompt_rules(), audience, tone, strength))
        else:
            rewritten = preprocessed
            if self.ai_client:
                prompt = build_rewrite_prompt(preprocessed, self.rule_bank.prompt_rules(), audience, tone, strength)
                rewritten = self.ai_client.rewrite(prompt)
            else:
                warnings.append("AI client unavailable; hybrid mode used rule-only fallback")

        postprocessed, enforced = self._rule_preprocess(rewritten)
        applied.extend(enforced)
        after_score = heuristic_score(postprocessed)
        change_log = [line for line in ndiff(text.splitlines(), postprocessed.splitlines()) if line.startswith("- ") or line.startswith("+ ")]

        return RewriteResult(
            original_text=text,
            rewritten_text=postprocessed,
            applied_rules=list(dict.fromkeys(applied)),
            warnings=warnings,
            change_log=change_log,
            score_before=base_score,
            score_after=after_score,
        )

    def ai_score(self, text: str) -> dict:
        if not self.ai_client:
            return heuristic_score(text)
        return self.ai_client.score(build_scoring_prompt(text))
