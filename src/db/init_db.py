#!/usr/bin/env python3
"""
Initialize (or upgrade) database/sales.db from schema.sql.
Safe to re-run: all statements are CREATE TABLE IF NOT EXISTS.

Usage:
    python3 src/db/init_db.py
"""
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "src" / "db" / "schema.sql"
DB_PATH = ROOT / "database" / "sales.db"


def _migrate_qualified_hq_model(conn: sqlite3.Connection) -> None:
    """
    2026-08-23: Chennai/Hyderabad promoted from market-intelligence-only to
    full qualified markets alongside Bangalore, and NON_BANGALORE_HQ_VERIFIED
    was renamed NON_QUALIFIED_HQ_VERIFIED. CREATE TABLE IF NOT EXISTS in
    schema.sql only helps fresh databases -- an existing sales.db keeps its
    old CHECK constraint and column names until migrated here. Idempotent:
    no-ops once opportunities.is_qualified_target already exists.
    """
    cols = [row[1] for row in conn.execute("PRAGMA table_info(opportunities)").fetchall()]
    if "is_qualified_target" in cols:
        return

    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("PRAGMA legacy_alter_table = ON")  # keep other tables' FK text pointed at "opportunities"
    try:
        conn.execute("ALTER TABLE company_hq RENAME TO company_hq_old")
        conn.execute(
            """CREATE TABLE company_hq (
                hq_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id      INTEGER NOT NULL REFERENCES companies(company_id),
                claimed_city    TEXT,
                hq_city         TEXT,
                hq_status       TEXT NOT NULL CHECK (hq_status IN
                                    ('BANGALORE_HQ_VERIFIED','CHENNAI_HQ_VERIFIED',
                                     'HYDERABAD_HQ_VERIFIED','NON_QUALIFIED_HQ_VERIFIED','HQ_UNVERIFIED')),
                evidence        TEXT,
                source_url      TEXT,
                verified_at     TEXT DEFAULT (datetime('now')),
                verified_by     TEXT DEFAULT 'hq-verification-skill'
            )"""
        )
        conn.execute(
            """INSERT INTO company_hq (hq_id, company_id, claimed_city, hq_city, hq_status,
                   evidence, source_url, verified_at, verified_by)
               SELECT hq_id, company_id, claimed_city, hq_city,
                   CASE hq_status WHEN 'NON_BANGALORE_HQ_VERIFIED' THEN 'NON_QUALIFIED_HQ_VERIFIED'
                       ELSE hq_status END,
                   evidence, source_url, verified_at, verified_by
               FROM company_hq_old"""
        )
        conn.execute("DROP TABLE company_hq_old")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_company_hq_company ON company_hq(company_id)")

        conn.execute("ALTER TABLE opportunities RENAME TO opportunities_old")
        conn.execute(
            """CREATE TABLE opportunities (
                opportunity_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id      INTEGER NOT NULL REFERENCES companies(company_id),
                hq_status       TEXT NOT NULL,
                primary_trigger TEXT,
                trigger_count   INTEGER DEFAULT 1,
                score           INTEGER,
                classification  TEXT CHECK (classification IN ('HOT','WARM','WATCH','LOW')),
                timing          TEXT CHECK (timing IN ('IMMEDIATE','NEAR_TERM','MEDIUM_TERM','WATCH')),
                why_now         TEXT,
                why_this_company TEXT,
                business_problem TEXT,
                why_business_standard TEXT,
                recommended_product TEXT,
                recommended_contact_id INTEGER REFERENCES contacts(contact_id),
                recommended_action TEXT,
                is_qualified_target INTEGER DEFAULT 0,
                scored_at       TEXT DEFAULT (datetime('now')),
                score_breakdown TEXT
            )"""
        )
        conn.execute(
            """INSERT INTO opportunities (opportunity_id, company_id, hq_status, primary_trigger,
                   trigger_count, score, classification, timing, why_now, why_this_company,
                   business_problem, why_business_standard, recommended_product,
                   recommended_contact_id, recommended_action, is_qualified_target, scored_at,
                   score_breakdown)
               SELECT opportunity_id, company_id,
                   CASE hq_status WHEN 'NON_BANGALORE_HQ_VERIFIED' THEN 'NON_QUALIFIED_HQ_VERIFIED'
                       ELSE hq_status END,
                   primary_trigger, trigger_count, score, classification, timing, why_now,
                   why_this_company, business_problem, why_business_standard, recommended_product,
                   recommended_contact_id, recommended_action, is_qualified_bangalore, scored_at,
                   score_breakdown
               FROM opportunities_old"""
        )
        conn.execute("DROP TABLE opportunities_old")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_opps_company ON opportunities(company_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_opps_score ON opportunities(score DESC)")
        conn.commit()
    finally:
        conn.execute("PRAGMA legacy_alter_table = OFF")
        conn.execute("PRAGMA foreign_keys = ON")


def init_db(db_path: Path = DB_PATH, schema_path: Path = SCHEMA_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text()
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        _migrate_qualified_hq_model(conn)
    finally:
        conn.close()
    print(f"Database ready at {db_path}")


if __name__ == "__main__":
    init_db()
