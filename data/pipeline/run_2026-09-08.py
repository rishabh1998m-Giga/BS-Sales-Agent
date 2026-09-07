#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-08 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Tazapay (international company, global HQ Singapore) --
its India entity Tazapay India Pvt Ltd is registered in Chennai (CIN
U62013TN2023FTC158701, RoC-Chennai), already a qualified city under the
international-company rule. Opened a new Bengaluru Centre of Excellence
on Sep 7 2026 (60 employees now, scaling to 150+ over 18 months,
engineering/product/treasury-ops focus) -- a fresh EXPANSION trigger for
an already-qualified company. B2B payments infrastructure -- qualifies
regardless of ticket size.

Checked and left UNSCORED (genuine ambiguity, not assumed): Navana.ai
(voice AI for BFSI, Rs 40 Cr Series A led by Ronnie Screwvala, dated
Sep 7 2026) -- widely described in press as "Bengaluru-based," but its
registered legal entity (Navana Tech India Pvt Ltd, CIN
U72900MH2018PTC315075) is Mumbai-registered (Nanavati Mahalaya, Fort,
Mumbai -- possibly a founder-family-linked address, founders are Raoul
and Jai Nanavati). Unlike the Titan/Pravaig precedent, no source found
where the company itself states an operational Bangalore HQ distinct
from the Mumbai registration -- "Bengaluru-based" here reads as
journalistic shorthand, not confirmed fact. Left HQ_UNVERIFIED rather
than assumed; worth a dedicated follow-up (e.g. checking the company's
own site/LinkedIn for a stated HQ) in a future pass.

Also checked: Chittorgarh (no new qualified-city DRHP), industry
movement (no qualifying item).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

tazapay_id = repo.get_or_create_company(conn, "Tazapay", industry="Cross-border payments infrastructure")
repo.set_hq_status(
    conn, tazapay_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="International company (global HQ Singapore) -- India HQ verified: Tazapay India Pvt "
             "Ltd, Guindy Industrial Estate, Chennai 600032 (CIN U62013TN2023FTC158701, "
             "RoC-Chennai, classified as Subsidiary of Foreign Company).",
    source_url="https://www.tofler.in/tazapay-india-private-limited/company/U62013TN2023FTC158701",
)
taza_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (tazapay_id, "new_office", "EXPANSION",
     "Launched a Bengaluru Centre of Excellence (315 Work Avenue, Koramangala, 11,000 sq ft) with 60 "
     "employees, planning to scale to 150+ over 18 months across Engineering, Product, and Treasury "
     "Operations.",
     "2026-09-07", "2026-09-07", "FACT",
     "https://newspatrolling.com/tazapay-announces-launch-of-bengaluru-centre-of-excellence-plans-to-scale-team-to-150/",
     "Newspatrolling / Business News This Week",
     "\"Tazapay Announces Launch of Bengaluru Centre of Excellence, Plans to Scale Team to 150+\" -- "
     "Sep 7 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, tazapay_id, "EXPANSION", taza_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (tazapay_id, "new_office", "Koramangala, Bengaluru", "2026-09-07",
     "11,000 sq ft Centre of Excellence, 60 employees scaling to 150+ over 18 months",
     "https://newspatrolling.com/tazapay-announces-launch-of-bengaluru-centre-of-excellence-plans-to-scale-team-to-150/",
     "Engineering/Product/Treasury Operations focus"),
)
conn.commit()

taza_open_triggers = repo.open_trigger_count(conn, tazapay_id)
taza_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.55,
        "advertising_marketing_signal": 0.30,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.45,
        "decision_maker_availability": 0.25,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.45,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=taza_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, tazapay_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=taza_open_triggers,
    score=taza_result["score"],
    classification=taza_result["classification"],
    timing="IMMEDIATE",
    why_now="CoE launch announced 1 day ago -- fresh hiring-expansion story while the news is still "
            "new.",
    why_this_company="Tazapay, India HQ (Chennai) verified. Singapore-HQ'd cross-border payments "
                      "infrastructure company scaling up its India operations via a new Bengaluru hub.",
    business_problem="A B2B payments infrastructure company growing its India engineering footprint "
                      "needs employer-branding and business-press visibility for the new hub.",
    why_business_standard="B2B fintech-infrastructure expansion story fits BS's business readership; "
                           "moderate scale (60 employees) keeps this a WATCH-tier rather than urgent "
                           "priority.",
    recommended_product="digital_display, corporate_storytelling",
    recommended_action="Low-to-medium urgency; pitch employer-branding/corporate-storytelling content "
                        "tied to the new Bengaluru hub if BS wants to move on it; no marketing contact "
                        "confirmed in this pass.",
    is_qualified_target=taza_result["is_qualified_target"],
    score_breakdown=taza_result["score_breakdown"],
)

conn.close()
print("Tazapay:", taza_result)
