#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-31 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Puravankara Ltd (already tracked, Bangalore HQ verified from
the 2026-08-23 watchlist pass) entered a Joint Development Agreement for
a 7.83-acre land parcel in South-East Bengaluru on 2026-08-25 -- Rs 1,100-
1,247 crore GDV potential, ~0.89 msft saleable area, the company's fifth
Bengaluru land transaction this fiscal year. No business_events row
existed for this company before this pass (checked first). Real estate
is a considered/higher-ticket purchase, already established brand-fit.

Checked and found nothing else new/dated today: Chittorgarh (same SME
DRHP list as recent days, no qualified-city company), general funding/
expansion search (repeats of already-tracked/excluded items -- Airbound,
WATER, CarbonStrong), industry movement (Storyboard18/afaqs! -- BMW
India's new creative agency isn't a qualified-city advertiser, no other
qualifying item found).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

pura_row = conn.execute("SELECT company_id FROM companies WHERE name LIKE '%uravankara%'").fetchone()
pura_id = pura_row["company_id"]

pura_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (pura_id, "capacity_expansion", "EXPANSION",
     "Entered a Joint Development Agreement (JDA) for a 7.83-acre land parcel in South-East "
     "Bengaluru, Rs 1,100-1,247 crore GDV potential, ~0.89 msft saleable residential area -- the "
     "company's fifth Bengaluru land transaction this fiscal year (FY27).",
     "2026-08-25", "2026-08-25", "FACT",
     "https://www.business-standard.com/markets/capital-market-news/puravankara-enters-7-83-acre-joint-development-project-in-south-east-bengaluru-126082500255_1.html",
     "Business Standard / ANI",
     "\"Puravankara Enters JDA for 7.83-acre Land Parcel in South-East Bengaluru with Rs 1,247 Crore "
     "GDV Potential\" -- Aug 25 2026, discovered 2026-08-31",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, pura_id, "EXPANSION", pura_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (pura_id, "capacity_expansion", "South-East Bengaluru", "2026-08-25",
     "7.83-acre JDA, Rs 1,100-1,247 crore GDV potential, ~0.89 msft saleable area, fifth Bengaluru "
     "land transaction this fiscal year",
     "https://www.business-standard.com/markets/capital-market-news/puravankara-enters-7-83-acre-joint-development-project-in-south-east-bengaluru-126082500255_1.html",
     "Company's fifth land transaction in Bengaluru for FY27"),
)
conn.commit()

pura_open_triggers = repo.open_trigger_count(conn, pura_id)
pura_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.65,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.45,
        "business_standard_audience_fit": 0.60,
        "estimated_marketing_capacity": 0.65,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=pura_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, pura_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=pura_open_triggers,
    score=pura_result["score"],
    classification=pura_result["classification"],
    timing="MEDIUM_TERM",
    why_now="JDA signed 6 days ago; part of an active pattern (fifth Bengaluru land deal this "
            "fiscal year), suggesting sustained development-pipeline momentum worth a corporate-"
            "storytelling angle now rather than waiting for a single mega-announcement.",
    why_this_company="Puravankara Ltd, Bangalore HQ verified. Established listed real-estate "
                      "developer actively expanding its Bengaluru land bank.",
    business_problem="A publicly listed developer with an active acquisition pace needs sustained "
                      "visibility with homebuyers and investors, not just a one-off project launch ad.",
    why_business_standard="Real-estate/property-market story fits BS's business and investor "
                           "readership -- especially the FY27 land-bank-momentum narrative angle.",
    recommended_product="corporate_storytelling, digital_display",
    recommended_action="Pitch a broader 'active Bengaluru land-bank expansion' corporate story rather "
                        "than a single-project ad; no marketing/comms contact confirmed in this pass.",
    is_qualified_target=pura_result["is_qualified_target"],
    score_breakdown=pura_result["score_breakdown"],
)

conn.close()
print("Puravankara:", pura_result)
