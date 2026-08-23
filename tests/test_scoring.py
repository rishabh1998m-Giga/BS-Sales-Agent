#!/usr/bin/env python3
"""Basic sanity tests for the scoring engine. Run: python3 -m pytest tests/ -q
(or python3 tests/test_scoring.py if pytest isn't installed)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from scoring.scorer import score_opportunity, load_config, classify_timing  # noqa: E402


def test_weights_sum_to_100():
    cfg = load_config()
    assert sum(cfg["weights"].values()) == 100


def test_qualified_gate_blocks_non_qualified():
    result = score_opportunity(
        sub_scores={k: 1.0 for k in load_config()["weights"]},
        hq_status="NON_QUALIFIED_HQ_VERIFIED",
    )
    assert result["is_qualified_target"] == 0
    assert result["score"] == 100  # score still computed, just not qualified


def test_qualified_gate_allows_bangalore():
    result = score_opportunity(
        sub_scores={k: 1.0 for k in load_config()["weights"]},
        hq_status="BANGALORE_HQ_VERIFIED",
    )
    assert result["is_qualified_target"] == 1


def test_qualified_gate_allows_chennai_and_hyderabad():
    for hq_status in ("CHENNAI_HQ_VERIFIED", "HYDERABAD_HQ_VERIFIED"):
        result = score_opportunity(
            sub_scores={k: 1.0 for k in load_config()["weights"]},
            hq_status=hq_status,
        )
        assert result["is_qualified_target"] == 1


def test_hq_unverified_is_not_qualified():
    result = score_opportunity(
        sub_scores={k: 1.0 for k in load_config()["weights"]},
        hq_status="HQ_UNVERIFIED",
    )
    assert result["is_qualified_target"] == 0


def test_multi_trigger_bonus_applied():
    base = score_opportunity(
        sub_scores={k: 0.5 for k in load_config()["weights"]},
        hq_status="BANGALORE_HQ_VERIFIED",
        open_trigger_count=1,
    )
    boosted = score_opportunity(
        sub_scores={k: 0.5 for k in load_config()["weights"]},
        hq_status="BANGALORE_HQ_VERIFIED",
        open_trigger_count=4,
    )
    assert boosted["score"] > base["score"]


def test_timing_classification():
    assert classify_timing(3) == "IMMEDIATE"
    assert classify_timing(20) == "NEAR_TERM"
    assert classify_timing(60) == "MEDIUM_TERM"
    assert classify_timing(200) == "WATCH"


if __name__ == "__main__":
    fns = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"OK: {fn.__name__}")
    print(f"\n{len(fns)} tests passed.")
