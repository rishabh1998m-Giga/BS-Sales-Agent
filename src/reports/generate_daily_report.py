#!/usr/bin/env python3
"""
Renders the Daily Client Intelligence Report (Section 23) from whatever is
currently in database/sales.db, and stores it in the daily_reports table.

This script only FORMATS data that skills/agents have already researched,
verified, and scored into the DB during the day's run — it does not do any
research itself. See .claude/skills/daily-sales-brief/SKILL.md for the
end-to-end workflow this script slots into.

Usage:
    python3 src/reports/generate_daily_report.py [--date YYYY-MM-DD]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db.repo import connect, top_opportunities  # noqa: E402


def section(title: str) -> str:
    return f"\n## {title}\n"


def fmt_opportunity_line(row) -> str:
    return (
        f"- **{row['company_name']}** — score {row['score']} "
        f"({row['classification']}, {row['timing']}) — trigger: {row['primary_trigger']}"
    )


def build_report(conn, report_date: str) -> str:
    lines = []
    lines.append("================================")
    lines.append("BUSINESS STANDARD")
    lines.append("CLIENT INTELLIGENCE")
    lines.append(f"{report_date}")
    lines.append("================================")

    top10 = top_opportunities(conn, qualified_only=True, limit=10)
    lines.append(section("1. TOP 10 NEW SALES OPPORTUNITIES"))
    if top10:
        for r in top10:
            lines.append(fmt_opportunity_line(r))
    else:
        lines.append("_No scored opportunities in the database yet. Run the daily-sales-brief skill._")

    lines.append(section("2. QUALIFIED-MARKET (BANGALORE/CHENNAI/HYDERABAD) COMPANIES WITH NEW BUSINESS TRIGGERS"))
    rows = conn.execute(
        """SELECT DISTINCT c.name, t.trigger_type FROM opportunity_triggers t
           JOIN companies c ON c.company_id = t.company_id
           JOIN company_hq h ON h.company_id = c.company_id
           WHERE h.hq_status IN ('BANGALORE_HQ_VERIFIED','CHENNAI_HQ_VERIFIED','HYDERABAD_HQ_VERIFIED')
             AND t.is_open = 1
           ORDER BY t.opened_at DESC LIMIT 20"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — {r['trigger_type']}")
    if not rows:
        lines.append("_None yet._")

    for title, table, cols in [
        ("3. IPO OPPORTUNITIES", "ipo_events", "ipo_status, stage, expected_timeline"),
        ("4. FUNDRAISING OPPORTUNITIES", "funding_events", "stage, amount, date_announced"),
        ("5. PRODUCT LAUNCHES", "product_launches", "product_name, launch_date"),
        ("6. NEW MARKETING INITIATIVES", "marketing_initiatives", "campaign_name, objective"),
        ("7. EXPANSION OPPORTUNITIES", "expansion_events", "expansion_type, location"),
    ]:
        lines.append(section(title))
        rows = conn.execute(
            f"""SELECT c.name, {table}.* FROM {table}
                JOIN companies c ON c.company_id = {table}.company_id
                ORDER BY {table}.created_at DESC LIMIT 15"""
        ).fetchall()
        if rows:
            for r in rows:
                detail = ", ".join(f"{k}={r[k]}" for k in cols.split(", ") if r[k])
                lines.append(f"- {r['name']} — {detail}")
        else:
            lines.append("_None yet._")

    lines.append(section("8. NEW MARKETING LEADERS"))
    rows = conn.execute(
        """SELECT c.name, l.person_name, l.title, l.appointment_date FROM leadership_changes l
           JOIN companies c ON c.company_id = l.company_id ORDER BY l.created_at DESC LIMIT 15"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — {r['person_name']} ({r['title']}), {r['appointment_date']}")
    if not rows:
        lines.append("_None yet._")

    lines.append(section("9. COMPETITOR ADVERTISING"))
    rows = conn.execute(
        """SELECT c.name, camp.publisher, camp.campaign_type, camp.date_observed FROM campaigns camp
           JOIN companies c ON c.company_id = camp.company_id ORDER BY camp.created_at DESC LIMIT 15"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} on {r['publisher']} ({r['campaign_type']}), {r['date_observed']}")
    if not rows:
        lines.append("_None yet._")

    lines.append(section("10. COMPETITOR LEAKAGE"))
    rows = conn.execute(
        """SELECT c.name FROM competitor_activity ca
           JOIN companies c ON c.company_id = ca.company_id
           JOIN company_hq h ON h.company_id = c.company_id
           WHERE ca.leakage_flag = 1
             AND h.hq_status IN ('BANGALORE_HQ_VERIFIED','CHENNAI_HQ_VERIFIED','HYDERABAD_HQ_VERIFIED')"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — spending with competitors, no known BS activity")
    if not rows:
        lines.append("_None yet._")

    lines.append(section("11. MULTI-TRIGGER OPPORTUNITIES"))
    rows = conn.execute(
        """SELECT c.name, o.trigger_count, o.score FROM opportunities o
           JOIN companies c ON c.company_id = o.company_id
           WHERE o.trigger_count >= 3 AND o.is_qualified_target = 1
           ORDER BY o.score DESC"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — {r['trigger_count']} open triggers, score {r['score']}")
    if not rows:
        lines.append("_None yet._")

    lines.append(section("12. FOLLOW-UPS DUE"))
    rows = conn.execute(
        """SELECT c.name, f.due_date, f.note FROM followups f
           JOIN opportunities o ON o.opportunity_id = f.opportunity_id
           JOIN companies c ON c.company_id = o.company_id
           WHERE f.is_done = 0 AND date(f.due_date) <= date('now')
           ORDER BY f.due_date"""
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — due {r['due_date']}: {r['note']}")
    if not rows:
        lines.append("_None due._")

    lines.append(section("13. TODAY'S TOP 5 ACTIONS"))
    top5 = top_opportunities(conn, qualified_only=True, limit=5)
    if top5:
        for i, r in enumerate(top5, 1):
            lines.append(
                f"{i}. **{r['company_name']}** (score {r['score']}, {r['classification']}) — "
                f"{r['recommended_action'] or 'See opportunity record for recommended action.'}"
            )
    else:
        lines.append("_No qualified opportunities scored yet._")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    conn = connect()
    report_md = build_report(conn, args.date)

    top5 = [dict(r) for r in top_opportunities(conn, qualified_only=True, limit=5)]
    conn.execute(
        """INSERT INTO daily_reports (report_date, top5_json, full_report_md)
           VALUES (?, ?, ?)
           ON CONFLICT(report_date) DO UPDATE SET
             top5_json = excluded.top5_json,
             full_report_md = excluded.full_report_md,
             generated_at = datetime('now')""",
        (args.date, json.dumps(top5), report_md),
    )
    conn.commit()

    print(report_md)


if __name__ == "__main__":
    main()
