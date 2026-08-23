#!/usr/bin/env python3
"""
Small data-access helper layer over database/sales.db.
Deduplicates companies by name (case-insensitive) and gives agents/skills a
single place to insert intelligence records instead of hand-writing SQL
everywhere. Deliberately dependency-free (stdlib sqlite3 only).
"""
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
        "NON_BANGALORE_HQ_VERIFIED",
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


def top_opportunities(conn: sqlite3.Connection, bangalore_only: bool = True, limit: int = 10):
    """
    One row per company: its most recently scored opportunity. Without this,
    a company re-scored on a later day (new trigger, updated info) would
    show up alongside its own stale earlier row, sometimes with contradictory
    recommended_action text once the earlier row's open question is resolved.
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
    if bangalore_only:
        query += " AND o.is_qualified_bangalore = 1"
    query += " ORDER BY o.score DESC LIMIT ?"
    return conn.execute(query, (limit,)).fetchall()
