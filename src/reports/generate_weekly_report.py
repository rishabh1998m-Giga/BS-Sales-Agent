#!/usr/bin/env python3
"""
Weekly rollup (added 2026-08-23) -- a Friday summary so daily snapshots
don't bury the bigger picture: what's new this week, what's gone quiet,
and pipeline health. Reads what the daily runs already wrote; does no
research of its own.

Usage:
    python3 src/reports/generate_weekly_report.py [--date YYYY-MM-DD]
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db.repo import connect, active_risk_flags  # noqa: E402


def build_weekly_report(conn, as_of: str) -> str:
    since = (dt.date.fromisoformat(as_of) - dt.timedelta(days=7)).isoformat()
    lines = [
        "================================",
        "BUSINESS STANDARD",
        f"WEEKLY PIPELINE ROLLUP -- week ending {as_of}",
        "================================",
    ]

    lines.append(f"\n## 1. OPPORTUNITIES SCORED THIS WEEK (since {since})\n")
    rows = conn.execute(
        """SELECT c.name, o.score, o.classification, o.primary_trigger, o.scored_at
           FROM opportunities o JOIN companies c ON c.company_id = o.company_id
           WHERE date(o.scored_at) >= date(?) AND o.is_qualified_target = 1
           ORDER BY o.scored_at DESC""",
        (since,),
    ).fetchall()
    if rows:
        for r in rows:
            lines.append(f"- {r['name']} — {r['score']} ({r['classification']}), {r['primary_trigger']}, {r['scored_at'][:10]}")
    else:
        lines.append("_No opportunities scored this week._")

    lines.append("\n## 2. CURRENT QUALIFIED PIPELINE BY BAND\n")
    rows = conn.execute(
        """SELECT o.classification, COUNT(*) as n FROM opportunities o
           WHERE o.opportunity_id = (
               SELECT o2.opportunity_id FROM opportunities o2
               WHERE o2.company_id = o.company_id ORDER BY o2.scored_at DESC, o2.opportunity_id DESC LIMIT 1
           ) AND o.is_qualified_target = 1
           GROUP BY o.classification"""
    ).fetchall()
    band_counts = {r["classification"]: r["n"] for r in rows}
    for band in ("HOT", "WARM", "WATCH", "LOW"):
        lines.append(f"- {band}: {band_counts.get(band, 0)}")

    lines.append("\n## 3. RISK FLAGS ACTIVE NOW\n")
    risks = active_risk_flags(conn)
    if risks:
        for r in risks:
            lines.append(f"- {r['company_name']} — {r['risk_type']} ({r['severity']}): {r['description']}")
    else:
        lines.append("_None active._")

    lines.append("\n## 4. PIPELINE / OUTREACH TRACKING\n")
    outreach_count = conn.execute("SELECT COUNT(*) AS n FROM outreach").fetchone()["n"]
    pipeline_count = conn.execute("SELECT COUNT(*) AS n FROM pipeline").fetchone()["n"]
    if outreach_count or pipeline_count:
        lines.append(f"- {outreach_count} outreach record(s), {pipeline_count} pipeline record(s) on file.")
        rows = conn.execute(
            """SELECT c.name, p.stage, p.next_step, p.next_step_date FROM pipeline p
               JOIN opportunities o ON o.opportunity_id = p.opportunity_id
               JOIN companies c ON c.company_id = o.company_id
               ORDER BY p.updated_at DESC LIMIT 20"""
        ).fetchall()
        for r in rows:
            lines.append(f"  - {r['name']} — {r['stage']}, next: {r['next_step']} ({r['next_step_date']})")
    else:
        lines.append(
            "_No pipeline/outreach records exist yet -- this section will stay empty until outreach "
            "is actually logged (e.g. after a pitch from Section 14 is sent and a response tracked). "
            "Nothing fabricated here._"
        )

    lines.append(
        "\n## 5. NOTE\n\nThis rollup only reads what the daily runs already recorded -- it does not "
        "re-research anything. If a section above looks thin, that reflects what's actually been "
        "tracked, not a gap in this script."
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    conn = connect()
    print(build_weekly_report(conn, args.date))


if __name__ == "__main__":
    main()
