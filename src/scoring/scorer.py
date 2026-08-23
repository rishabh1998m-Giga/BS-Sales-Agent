#!/usr/bin/env python3
"""
Opportunity scoring engine — Section 16 of master spec.

Weights and bands live in config/scoring.yaml, NOT hardcoded here, so the
user can tune them without touching code. This module is intentionally a
pure function of its inputs: it does not do research or judgment calls
(that's the sales-opportunity-analysis / opportunity-scoring skills' job
when run inside Claude) — it just turns 0-10 sub-scores that a skill/agent
has already judged into a final 0-100 score, classification, and the
Bangalore hard-gate decision.
"""
import sys
from pathlib import Path
from typing import TypedDict

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml --break-system-packages", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "scoring.yaml"


class SubScores(TypedDict, total=False):
    business_event_strength: float       # 0-1 fraction of the weight's max
    advertising_marketing_signal: float
    timing_urgency: float
    business_standard_audience_fit: float
    estimated_marketing_capacity: float
    decision_maker_availability: float
    official_contact_availability: float
    strategic_relevance: float


def load_config(path: Path = CONFIG_PATH) -> dict:
    cfg = yaml.safe_load(path.read_text())
    total = sum(cfg["weights"].values())
    if total != 100:
        raise ValueError(f"scoring.yaml weights must sum to 100, got {total}")
    return cfg


def classify(score: int, bands: dict) -> str:
    for label, (lo, hi) in bands.items():
        if lo <= score <= hi:
            return label
    return "LOW"


def score_opportunity(
    sub_scores: SubScores,
    hq_status: str,
    open_trigger_count: int = 1,
    config: dict | None = None,
) -> dict:
    """
    sub_scores: each key maps to a 0.0-1.0 fraction (e.g. 0.8 = 80% of that
    dimension's max weight). Fractions come from an agent's/skill's
    judgment on the underlying evidence, not from this function.

    Returns a dict with score, classification, is_qualified_bangalore,
    and a breakdown for auditability.
    """
    cfg = config or load_config()
    weights = cfg["weights"]

    breakdown = {}
    raw_total = 0.0
    for dim, weight in weights.items():
        frac = max(0.0, min(1.0, sub_scores.get(dim, 0.0)))
        points = frac * weight
        breakdown[dim] = round(points, 2)
        raw_total += points

    # Multi-trigger bonus
    bonus_cfg = cfg.get("multi_trigger_bonus", {})
    bonus = 0
    if bonus_cfg.get("enabled") and open_trigger_count > 1:
        bonus = min(
            (open_trigger_count - 1) * bonus_cfg.get("bonus_per_extra_trigger", 0),
            bonus_cfg.get("max_bonus", 0),
        )
    total = round(raw_total) + bonus
    total = min(total, bonus_cfg.get("cap_at", 100))
    total = max(0, total)

    is_qualified_bangalore = 1 if hq_status == "BANGALORE_HQ_VERIFIED" else 0

    return {
        "score": total,
        "classification": classify(total, cfg["bands"]),
        "score_breakdown": {**breakdown, "multi_trigger_bonus": bonus},
        "is_qualified_bangalore": is_qualified_bangalore,
        "hq_status": hq_status,
    }


def classify_timing(days_to_event: int, config: dict | None = None) -> str:
    if days_to_event <= 7:
        return "IMMEDIATE"
    if days_to_event <= 30:
        return "NEAR_TERM"
    if days_to_event <= 90:
        return "MEDIUM_TERM"
    return "WATCH"


if __name__ == "__main__":
    # Self-test / example
    example = score_opportunity(
        sub_scores={
            "business_event_strength": 0.9,
            "advertising_marketing_signal": 0.8,
            "timing_urgency": 1.0,
            "business_standard_audience_fit": 0.9,
            "estimated_marketing_capacity": 0.7,
            "decision_maker_availability": 0.6,
            "official_contact_availability": 0.5,
            "strategic_relevance": 0.8,
        },
        hq_status="BANGALORE_HQ_VERIFIED",
        open_trigger_count=3,
    )
    print(example)
