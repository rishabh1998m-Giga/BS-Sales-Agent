#!/usr/bin/env python3
"""
Small data-access helper layer over database/sales.db.
Deduplicates companies by name (case-insensitive) and gives agents/skills a
single place to insert intelligence records instead of hand-writing SQL
everywhere. Deliberately dependency-free (stdlib sqlite3 only).
"""
import datetime as dt
import json
import sqlite3
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "database" / "sales.db"


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_or_create_company(conn: sqlite3.Connection, name: str, **fields) -> int:
    name = name.strip()
    row = conn.execute(
        "SELECT company_id FROM companies WHERE lower(name) = lower(?)", (name,)
    ).fetchone()
    if row:
        company_id = row["company_id"]
        if fields:
            sets = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(
                f"UPDATE companies SET {sets}, updated_at = datetime('now') WHERE company_id = ?",
                (*fields.values(), company_id),
            )
            conn.commit()
        return company_id
    cols = ["name", *fields.keys()]
    placeholders = ", ".join("?" for _ in cols)
    cur = conn.execute(
        f"INSERT INTO companies ({', '.join(cols)}) VALUES ({placeholders})",
        (name, *fields.values()),
    )
    conn.commit()
    return cur.lastrowid


def set_hq_status(
    conn: sqlite3.Connection,
    company_id: int,
    hq_status: str,
    claimed_city: Optional[str] = None,
    hq_city: Optional[str] = None,
    evidence: Optional[str] = None,
    source_url: Optional[str] = None,
) -> int:
    assert hq_status in (
        "BANGALORE_HQ_VERIFIED",
        "CHENNAI_HQ_VERIFIED",
        "HYDERABAD_HQ_VERIFIED",
        "NON_QUALIFIED_HQ_VERIFIED",
        "HQ_UNVERIFIED",
    ), f"invalid hq_status: {hq_status}"
    cur = conn.execute(
        """INSERT INTO company_hq (company_id, claimed_city, hq_city, hq_status, evidence, source_url)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (company_id, claimed_city, hq_city, hq_status, evidence, source_url),
    )
    conn.commit()
    return cur.lastrowid


def latest_hq_status(conn: sqlite3.Connection, company_id: int) -> Optional[str]:
    row = conn.execute(
        """SELECT hq_status FROM company_hq WHERE company_id = ?
           ORDER BY verified_at DESC LIMIT 1""",
        (company_id,),
    ).fetchone()
    return row["hq_status"] if row else None


def open_trigger(conn: sqlite3.Connection, company_id: int, trigger_type: str, source_event_id: Optional[int] = None) -> int:
    cur = conn.execute(
        "INSERT INTO opportunity_triggers (company_id, trigger_type, source_event_id) VALUES (?, ?, ?)",
        (company_id, trigger_type, source_event_id),
    )
    conn.commit()
    return cur.lastrowid


def open_trigger_count(conn: sqlite3.Connection, company_id: int, window_days: int = 90) -> int:
    row = conn.execute(
        """SELECT COUNT(*) AS n FROM opportunity_triggers
           WHERE company_id = ? AND is_open = 1
           AND julianday('now') - julianday(opened_at) <= ?""",
        (company_id, window_days),
    ).fetchone()
    return row["n"]


def insert_opportunity(conn: sqlite3.Connection, company_id: int, **fields) -> int:
    if "score_breakdown" in fields and isinstance(fields["score_breakdown"], dict):
        fields["score_breakdown"] = json.dumps(fields["score_breakdown"])
    cols = ["company_id", *fields.keys()]
    placeholders = ", ".join("?" for _ in cols)
    cur = conn.execute(
        f"INSERT INTO opportunities ({', '.join(cols)}) VALUES ({placeholders})",
        (company_id, *fields.values()),
    )
    conn.commit()
    return cur.lastrowid


def add_key_date(
    conn: sqlite3.Connection,
    company_id: int,
    date_type: str,
    month_day: str,
    label: Optional[str] = None,
    source_url: Optional[str] = None,
    evidence: Optional[str] = None,
    confidence: Optional[str] = None,
) -> int:
    """month_day must be 'MM-DD' -- validated here so a bad value fails loudly
    at insert time rather than silently breaking the calendar-window check."""
    dt.datetime.strptime(month_day, "%m-%d")  # raises ValueError if malformed
    cur = conn.execute(
        """INSERT INTO company_key_dates
           (company_id, date_type, month_day, label, source_url, evidence, confidence)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (company_id, date_type, month_day, label, source_url, evidence, confidence),
    )
    conn.commit()
    return cur.lastrowid


def upcoming_key_dates(conn: sqlite3.Connection, window_days: int = 45, today: Optional[dt.date] = None):
    """
    Company-specific recurring dates (company_key_dates) falling within the
    next `window_days` of `today`, wrapping correctly across a year boundary
    (e.g. today=Dec 20, window=45 must still catch Jan 15).
    """
    today = today or dt.date.today()
    rows = conn.execute(
        """SELECT k.*, c.name AS company_name FROM company_key_dates k
           JOIN companies c ON c.company_id = k.company_id
           ORDER BY k.month_day"""
    ).fetchall()
    matches = []
    for row in rows:
        month, day = (int(x) for x in row["month_day"].split("-"))
        this_year = dt.date(today.year, month, day)
        next_year = dt.date(today.year + 1, month, day)
        candidate = this_year if this_year >= today else next_year
        days_away = (candidate - today).days
        if 0 <= days_away <= window_days:
            matches.append({**dict(row), "days_away": days_away, "next_occurrence": candidate.isoformat()})
    return sorted(matches, key=lambda r: r["days_away"])


def add_risk_flag(
    conn: sqlite3.Connection,
    company_id: int,
    risk_type: str,
    description: Optional[str] = None,
    severity: Optional[str] = None,
    source_url: Optional[str] = None,
    evidence: Optional[str] = None,
) -> int:
    cur = conn.execute(
        """INSERT INTO risk_flags (company_id, risk_type, description, severity, source_url, evidence)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (company_id, risk_type, description, severity, source_url, evidence),
    )
    conn.commit()
    return cur.lastrowid


def active_risk_flags(conn: sqlite3.Connection):
    return conn.execute(
        """SELECT r.*, c.name AS company_name FROM risk_flags r
           JOIN companies c ON c.company_id = r.company_id
           WHERE r.is_active = 1
           ORDER BY CASE r.severity WHEN 'HIGH' THEN 0 WHEN 'MEDIUM' THEN 1 ELSE 2 END, r.flagged_at DESC"""
    ).fetchall()


def all_tracked_contacts(conn: sqlite3.Connection):
    """
    Every contact on file, most recent per company first -- for cross-
    checking against fresh research to catch decision-maker movement
    (promoted, left the company, replaced) before pitching the wrong person.
    """
    return conn.execute(
        """SELECT c.name AS company_name, ct.contact_id, ct.name, ct.title, ct.created_at
           FROM contacts ct JOIN companies c ON c.company_id = ct.company_id
           ORDER BY c.name, ct.created_at DESC"""
    ).fetchall()


def add_industry_movement(
    conn: sqlite3.Connection,
    source: str,
    movement_type: str,
    headline: str,
    summary: Optional[str] = None,
    city_relevance: Optional[str] = None,
    source_url: Optional[str] = None,
    date_observed: Optional[str] = None,
) -> int:
    cur = conn.execute(
        """INSERT INTO industry_movements
           (source, movement_type, headline, summary, city_relevance, source_url, date_observed)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (source, movement_type, headline, summary, city_relevance, source_url, date_observed),
    )
    conn.commit()
    return cur.lastrowid


def recent_industry_movements(conn: sqlite3.Connection, days: int = 3):
    return conn.execute(
        """SELECT * FROM industry_movements
           WHERE julianday('now') - julianday(created_at) <= ?
           ORDER BY created_at DESC""",
        (days,),
    ).fetchall()


def top_opportunities(conn: sqlite3.Connection, qualified_only: bool = True, limit: int = 10):
    """
    One row per company: its most recently scored opportunity. Without this,
    a company re-scored on a later day (new trigger, updated info) would
    show up alongside its own stale earlier row, sometimes with contradictory
    recommended_action text once the earlier row's open question is resolved.

    qualified_only filters to companies that passed the city-HQ hard gate
    (Bangalore, Chennai, or Hyderabad HQ -- see config/cities.yaml).
    """
    query = """
        SELECT o.*, c.name AS company_name FROM opportunities o
        JOIN companies c ON c.company_id = o.company_id
        WHERE o.opportunity_id = (
            SELECT o2.opportunity_id FROM opportunities o2
            WHERE o2.company_id = o.company_id
            ORDER BY o2.scored_at DESC, o2.opportunity_id DESC LIMIT 1
        )
    """
    if qualified_only:
        query += " AND o.is_qualified_target = 1"
    query += " ORDER BY o.score DESC LIMIT ?"
    return conn.execute(query, (limit,)).fetchall()
