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


def init_db(db_path: Path = DB_PATH, schema_path: Path = SCHEMA_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text()
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
    print(f"Database ready at {db_path}")


if __name__ == "__main__":
    init_db()
