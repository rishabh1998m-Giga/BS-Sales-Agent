#!/usr/bin/env python3
"""
Renders the Daily Client Intelligence Report (Section 23) from whatever is
currently in database/sales.db, and stores it in the daily_reports table.

This script only FORMATS data that skills/agents have already researched,
verified, and scored into the DB during the day's run — it does not do any
research itself. See .claude/skills/daily-sales-brief/SKILL.md for the
end-to-end workflow this script slots into.

--date is always an IST calendar date (this project serves an India-based
user). SQLite's datetime('now') defaults store UTC, so every "today"-scoped
query here converts stored timestamps to IST (+5:30) before comparing dates
-- added 2026-08-30 after the daily trigger moved to 1:30 AM IST (= 20:00
UTC the PREVIOUS day), which was silently producing empty reports because
raw UTC-vs-IST date comparison never matched.

Usage:
    python3 src/reports/generate_daily_report.py [--date YYYY-MM-DD]
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db.repo import (  # noqa: E402
    connect, todays_opportunities, upcoming_key_dates, active_risk_flags,
    recent_industry_movements,
)
from pitch.generate_pitch import build_pitch, _load_product_labels  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CALENDAR_CONFIG_PATH = ROOT / "config" / "calendar-triggers.yaml"


def section(title: str) -> str:
    return f"\n## {title}\n"


def _fixed_macro_windows(today: dt.date) -> list[dict]:
    """
    Evaluates only the macro_windows in calendar-triggers.yaml with a literal
    'MM-DD to MM-DD' range (fiscal year-end, Union Budget). The festive-season
    window is explicitly "movable" (lunar calendar) and is NOT computed here
    -- it must be confirmed against a real source during research, not
    hardcoded; see the note returned alongside the fixed windows.
    """
    if not CALENDAR_CONFIG_PATH.exists():
        return []
    cfg = yaml.safe_load(CALENDAR_CONFIG_PATH.read_text())
    matches = []
    for w in cfg.get("macro_windows", []):
        window = w.get("window", "")
        if " to " not in window or "movable" in window:
            continue
        start_str, end_str = [s.strip() for s in window.split(" to ")]
        try:
            sm, sd = (int(x) for x in start_str.split("-"))
            em, ed = (int(x) for x in end_str.split("-"))
        except ValueError:
            continue
        start = dt.date(today.year, sm, sd)
        end = dt.date(today.year, em, ed)
        lead_days = w.get("lead_days", 0)
        flag_from = start - dt.timedelta(days=lead_days)
        # handle a window that already passed this year by also checking next year's occurrence
        for candidate_start, candidate_end, candidate_flag_from in (
            (start, end, flag_from),
            (dt.date(today.year + 1, sm, sd), dt.date(today.year + 1, em, ed),
             dt.date(today.year + 1, sm, sd) - dt.timedelta(days=lead_days)),
        ):
            if candidate_flag_from <= today <= candidate_end:
                status = "ACTIVE NOW" if candidate_start <= today <= candidate_end else "UPCOMING"
                matches.append({
                    "name": w["name"], "status": status,
                    "window_start": candidate_start.isoformat(), "window_end": candidate_end.isoformat(),
                    "note": w.get("note", "").strip(),
                })
                break
    return matches


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

    # Everything through Section 11 is scoped to TODAY only (report_date) --
    # a company/event already reported on an earlier day and unchanged since
    # is correctly absent here rather than repeated. Persistent/all-time
    # views (full pipeline, weekly health) live in generate_weekly_report.py
    # via top_opportunities(), not here.
    today_opps = todays_opportunities(conn, report_date, qualified_only=True, limit=10)
    lines.append(section("1. TODAY'S NEW OR UPDATED SALES OPPORTUNITIES"))
    if today_opps:
        for r in today_opps:
            lines.append(fmt_opportunity_line(r))
    else:
        lines.append("_Nothing new or rescored today -- see the weekly rollup for the full standing pipeline._")

    lines.append(section("2. QUALIFIED-MARKET (BANGALORE/CHENNAI/HYDERABAD) COMPANIES WITH NEW BUSINESS TRIGGERS TODAY"))
    rows = conn.execute(
        """SELECT DISTINCT c.name, t.trigger_type FROM opportunity_triggers t
           JOIN companies c ON c.company_id = t.company_id
           JOIN company_hq h ON h.company_id = c.company_id
           WHERE h.hq_status IN ('BANGALORE_HQ_VERIFIED','CHENNAI_HQ_VERIFIED','HYDERABAD_HQ_VERIFIED')
             AND t.is_open = 1 AND date(t.opened_at, '+5 hours', '+30 minutes') = date(?)
           ORDER BY t.opened_at DESC LIMIT 20""",
        (report_date,),
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — {r['trigger_type']}")
    if not rows:
        lines.append("_None today._")

    for title, table, cols in [
        ("3. IPO OPPORTUNITIES (NEW TODAY)", "ipo_events", "ipo_status, stage, expected_timeline"),
        ("4. FUNDRAISING OPPORTUNITIES (NEW TODAY)", "funding_events", "stage, amount, date_announced"),
        ("5. PRODUCT LAUNCHES (NEW TODAY)", "product_launches", "product_name, launch_date"),
        ("6. NEW MARKETING INITIATIVES (NEW TODAY)", "marketing_initiatives", "campaign_name, objective"),
        ("7. EXPANSION OPPORTUNITIES (NEW TODAY)", "expansion_events", "expansion_type, location"),
    ]:
        lines.append(section(title))
        rows = conn.execute(
            f"""SELECT c.name, {table}.* FROM {table}
                JOIN companies c ON c.company_id = {table}.company_id
                WHERE date({table}.created_at, '+5 hours', '+30 minutes') = date(?)
                ORDER BY {table}.created_at DESC LIMIT 15""",
            (report_date,),
        ).fetchall()
        if rows:
            for r in rows:
                detail = ", ".join(f"{k}={r[k]}" for k in cols.split(", ") if r[k])
                lines.append(f"- {r['name']} — {detail}")
        else:
            lines.append("_None today._")

    lines.append(section("8. NEW MARKETING LEADERS (NEW TODAY)"))
    rows = conn.execute(
        """SELECT c.name, l.person_name, l.title, l.appointment_date FROM leadership_changes l
           JOIN companies c ON c.company_id = l.company_id
           WHERE date(l.created_at, '+5 hours', '+30 minutes') = date(?)
           ORDER BY l.created_at DESC LIMIT 15""",
        (report_date,),
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — {r['person_name']} ({r['title']}), {r['appointment_date']}")
    if not rows:
        lines.append("_None today._")

    lines.append(section("9. COMPETITOR ADVERTISING (NEW TODAY)"))
    rows = conn.execute(
        """SELECT c.name, camp.publisher, camp.campaign_type, camp.date_observed FROM campaigns camp
           JOIN companies c ON c.company_id = camp.company_id
           WHERE date(camp.created_at, '+5 hours', '+30 minutes') = date(?)
           ORDER BY camp.created_at DESC LIMIT 15""",
        (report_date,),
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} on {r['publisher']} ({r['campaign_type']}), {r['date_observed']}")
    if not rows:
        lines.append("_None today._")

    lines.append(section("10. COMPETITOR LEAKAGE (NEW TODAY)"))
    rows = conn.execute(
        """SELECT c.name FROM competitor_activity ca
           JOIN companies c ON c.company_id = ca.company_id
           JOIN company_hq h ON h.company_id = c.company_id
           WHERE ca.leakage_flag = 1 AND date(ca.created_at, '+5 hours', '+30 minutes') = date(?)
             AND h.hq_status IN ('BANGALORE_HQ_VERIFIED','CHENNAI_HQ_VERIFIED','HYDERABAD_HQ_VERIFIED')""",
        (report_date,),
    ).fetchall()
    for r in rows:
        lines.append(f"- {r['name']} — spending with competitors, no known BS activity")
    if not rows:
        lines.append("_None today._")

    lines.append(section("11. MULTI-TRIGGER OPPORTUNITIES (NEWLY SCORED TODAY)"))
    multi = [r for r in today_opps if r["trigger_count"] >= 3]
    if multi:
        for r in multi:
            lines.append(f"- {r['company_name']} — {r['trigger_count']} open triggers, score {r['score']}")
    else:
        lines.append("_None today._")

    lines.append(section("12. TODAY'S TOP 5 ACTIONS"))
    top5 = sorted(today_opps, key=lambda r: r["score"], reverse=True)[:5]
    if top5:
        for i, r in enumerate(top5, 1):
            lines.append(
                f"{i}. **{r['company_name']}** (score {r['score']}, {r['classification']}) — "
                f"{r['recommended_action'] or 'See opportunity record for recommended action.'}"
            )
    else:
        lines.append("_Nothing new today to act on -- check the weekly rollup for standing follow-ups._")

    lines.append(section("13. TODAY'S PITCHES"))
    warm_plus = [r for r in today_opps if r["classification"] in ("HOT", "WARM")]
    if warm_plus:
        labels = _load_product_labels()
        for r in warm_plus:
            contact_name = contact_title = None
            if r["recommended_contact_id"]:
                contact = conn.execute(
                    "SELECT name, title FROM contacts WHERE contact_id = ?",
                    (r["recommended_contact_id"],),
                ).fetchone()
                if contact:
                    contact_name, contact_title = contact["name"], contact["title"]
            if not r["pitch_draft"]:
                pitch = build_pitch(dict(r), r["company_name"], contact_name, contact_title, labels)
                conn.execute(
                    "UPDATE opportunities SET pitch_draft = ?, objection_notes = ? WHERE opportunity_id = ?",
                    (pitch["pitch_draft"], pitch["objection_notes"], r["opportunity_id"]),
                )
                conn.commit()
                pitch_draft, objection_notes = pitch["pitch_draft"], pitch["objection_notes"]
            else:
                pitch_draft, objection_notes = r["pitch_draft"], r["objection_notes"]
            lines.append(f"\n### {r['company_name']} (score {r['score']}, {r['classification']})\n")
            lines.append("```")
            lines.append(pitch_draft)
            lines.append("```")
            lines.append(f"\n_Objection handling:_\n{objection_notes}\n")
    else:
        lines.append("_No WARM-or-better opportunities to pitch today._")

    lines.append(section("14. CALENDAR-DRIVEN OPPORTUNITIES (NEXT 90 DAYS)"))
    key_dates = upcoming_key_dates(conn, window_days=90)
    macro = _fixed_macro_windows(dt.date.today())
    if key_dates:
        lines.append("**Company-specific dates -- plan inventory/roadblocks ahead of these:**")
        for k in key_dates:
            lines.append(
                f"- {k['company_name']} — {k['label'] or k['date_type']} on {k['next_occurrence']} "
                f"({k['days_away']}d away)"
            )
    if macro:
        lines.append("\n**Macro calendar windows:**" if key_dates else "**Macro calendar windows:**")
        for m in macro:
            lines.append(f"- {m['name']} — {m['status']} ({m['window_start']} to {m['window_end']})")
    if not key_dates and not macro:
        lines.append("_None in the next 90 days._")
    lines.append(
        "\n_Note: festive-season (Navratri-Diwali) dates shift yearly and are not computed "
        "mechanically here -- confirmed during research when in range, per config/calendar-triggers.yaml._"
    )

    lines.append(section("15. RISK FLAGS"))
    risks = active_risk_flags(conn)
    if risks:
        for r in risks:
            lines.append(f"- **{r['company_name']}** — {r['risk_type']} ({r['severity']}): {r['description']}")
    else:
        lines.append("_None flagged._")

    lines.append(section("16. INDUSTRY MOVEMENT (Exchange4Media / afaqs! -- Bangalore/Chennai/Hyderabad only)"))
    movements = recent_industry_movements(conn, days=3)
    if movements:
        for m in movements:
            lines.append(f"- **{m['headline']}** ({m['source']}, {m['city_relevance']})")
            if m["summary"]:
                lines.append(f"  {m['summary']}")
    else:
        lines.append("_None found this pass. Separate from Sections 9-10 -- see config/industry-movement-sources.yaml._")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()

    conn = connect()
    report_md = build_report(conn, args.date)

    top5 = [dict(r) for r in todays_opportunities(conn, args.date, qualified_only=True, limit=5)]
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
