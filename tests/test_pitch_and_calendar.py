#!/usr/bin/env python3
"""Sanity tests for the 2026-08-23 additions: pitch drafts, key dates, risk flags."""
import datetime as dt
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from db.init_db import init_db  # noqa: E402
from db.repo import (  # noqa: E402
    connect, get_or_create_company, add_key_date, upcoming_key_dates,
    add_risk_flag, active_risk_flags, add_industry_movement, recent_industry_movements,
)
from pitch.generate_pitch import build_pitch  # noqa: E402


def _fresh_conn():
    tmp = Path(tempfile.mkstemp(suffix=".db")[1])
    init_db(db_path=tmp)
    return connect(db_path=tmp)


def test_upcoming_key_dates_within_window():
    conn = _fresh_conn()
    cid = get_or_create_company(conn, "TestCo")
    today = dt.date(2026, 8, 23)
    add_key_date(conn, cid, "founding_anniversary", "09-15", label="Founding day")
    matches = upcoming_key_dates(conn, window_days=45, today=today)
    assert len(matches) == 1
    assert matches[0]["days_away"] == (dt.date(2026, 9, 15) - today).days


def test_upcoming_key_dates_wraps_year_boundary():
    conn = _fresh_conn()
    cid = get_or_create_company(conn, "TestCo2")
    today = dt.date(2026, 12, 20)
    add_key_date(conn, cid, "founding_anniversary", "01-15", label="Founding day")
    matches = upcoming_key_dates(conn, window_days=45, today=today)
    assert len(matches) == 1
    assert matches[0]["next_occurrence"] == "2027-01-15"


def test_upcoming_key_dates_outside_window_excluded():
    conn = _fresh_conn()
    cid = get_or_create_company(conn, "TestCo3")
    today = dt.date(2026, 8, 23)
    add_key_date(conn, cid, "founding_anniversary", "12-25", label="Far off")
    assert upcoming_key_dates(conn, window_days=45, today=today) == []


def test_risk_flag_roundtrip():
    conn = _fresh_conn()
    cid = get_or_create_company(conn, "RiskCo")
    add_risk_flag(conn, cid, "funding_freeze", description="Round stalled", severity="HIGH")
    flags = active_risk_flags(conn)
    assert len(flags) == 1
    assert flags[0]["company_name"] == "RiskCo"
    assert flags[0]["severity"] == "HIGH"


def test_pitch_never_includes_a_price_and_flags_sales_ops():
    result = build_pitch(
        {
            "primary_trigger": "IPO", "classification": "WARM",
            "why_now": "test", "why_this_company": "test",
            "business_problem": "test", "why_business_standard": "test",
            "recommended_product": "premium_display",
        },
        company_name="TestCo",
    )
    assert "CONFIRM WITH SALES OPS" in result["pitch_draft"]
    assert "$" not in result["pitch_draft"]
    assert "Rs " not in result["pitch_draft"] and "₹" not in result["pitch_draft"]


def test_industry_movement_roundtrip():
    conn = _fresh_conn()
    add_industry_movement(
        conn, source="afaqs!", movement_type="agency_mandate_win",
        headline="Agency X wins Y's mandate", summary="Two-line summary.",
        city_relevance="Bangalore -- brand HQ verified",
    )
    rows = recent_industry_movements(conn, days=3)
    assert len(rows) == 1
    assert rows[0]["source"] == "afaqs!"


if __name__ == "__main__":
    fns = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"OK: {fn.__name__}")
    print(f"\n{len(fns)} tests passed.")
