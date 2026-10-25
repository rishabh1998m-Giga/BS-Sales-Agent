#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-26 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: IndiQube Spaces Limited (Bangalore-HQ verified, listed
flexible/managed office-space provider) -- its board approved (Oct 19
2026 meeting, surfaced in coverage Oct 24-25) an investment of up to
Rs 35 crore in SaiEdge Realty Private Limited (via equity shares and/
or convertible securities, in multiple tranches, subject to definitive
agreements) for up to a 49% stake on a fully-diluted basis. SaiEdge was
only incorporated 28 Jul 2026, has not started operations and has no
turnover yet -- it plans to build commercial office space that
IndiQube intends to lease once complete, i.e. this is a forward-
funding/expansion move to secure IndiQube's own future office-space
pipeline. B2B managed-office-space company -- qualifies regardless of
ticket size.

Checked and declined:
  - Palmonas (demi-fine jewellery D2C brand, opened its 115th store at
    HSR Layout, Bengaluru, Oct 24 2026) -- HQ is genuinely
    contradictory even within a single source (Tracxn states both
    "headquartered in Pune, India" AND lists a Bengaluru HSR Layout
    registered-office address), and the CIN found (incorporation year
    2012) doesn't match the brand's 2022 founding, suggesting it may
    belong to an unrelated/predecessor entity. Left unscored on HQ
    ambiguity rather than assumed -- a store opening is also a lower-
    signal trigger than a funding/expansion event even if HQ had been
    confirmed.

Also checked: Chittorgarh (Jio Platforms IPO closed Oct 23, fully
subscribed 21.36x -- Mumbai/Reliance HQ, not qualified; no new
qualified-city DRHP), industry movement via afaqs!/Storyboard18 (only
a Bengaluru Storyboard18 Visionaries recognition event, undated, and
the 202-day-old WeWork India leasing story resurfacing -- neither a
fresh qualifying brand-agency mandate story for Section 16).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

indiqube_id = repo.get_or_create_company(conn, "IndiQube Spaces", industry="Flexible/managed office-space provider")
repo.set_hq_status(
    conn, indiqube_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Indiqube Spaces Limited, Plot # 53, Careernet Campus, Kariyammanna Agrahara Road, "
             "Devarabisanahalli, Outer Ring Road, Bangalore 560103 (CIN L45400KA2015PLC133523, "
             "RoC-Bangalore, incorporated 14 Jan 2015, recently converted from private to public/listed "
             "-- CIN changed from U45400KA2015PLC133523 to the L-prefixed listed-company CIN per the "
             "company's own Aug 2025 stock-exchange filing). Registered AND corporate office both "
             "Bangalore, no discrepancy.",
    source_url="https://www.zaubacorp.com/INDIQUBE-SPACES-LIMITED-L45400KA2015PLC133523",
)
indiqube_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (indiqube_id, "strategic_investment", "EXPANSION",
     "Board approved (meeting Oct 19 2026) an investment of up to Rs 35 crore in SaiEdge Realty Pvt "
     "Ltd via equity shares and/or convertible securities, across multiple tranches, for up to a 49% "
     "stake on a fully-diluted basis -- subject to definitive agreements. SaiEdge (incorporated 28 Jul "
     "2026, pre-revenue, not yet operational) plans to build commercial office space that IndiQube "
     "intends to lease once complete -- a forward-funding move to secure IndiQube's own future "
     "office-space supply pipeline.",
     "2026-10-19", "2026-10-24", "FACT",
     "https://entrackr.com/news/indiqube-to-invest-rs-35-cr-in-saiedge-realty-for-49-stake-12690289",
     "Entrackr / Lapaas Voice / Constro Facilitator",
     "\"IndiQube to invest Rs 35 Cr in SaiEdge Realty for 49% stake\" -- board approval Oct 19 2026, "
     "surfaced in coverage Oct 24-25 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, indiqube_id, "EXPANSION", indiqube_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (indiqube_id, "strategic_investment", "Bangalore (SaiEdge Realty)", "2026-10-19",
     "Up to Rs 35 crore for up to 49% stake in SaiEdge Realty, to secure future office-space supply "
     "for IndiQube's own managed-office leasing pipeline",
     "https://entrackr.com/news/indiqube-to-invest-rs-35-cr-in-saiedge-realty-for-49-stake-12690289",
     "Board-approved, subject to definitive agreements; SaiEdge is pre-revenue/pre-operational"),
)
conn.commit()

indiqube_open_triggers = repo.open_trigger_count(conn, indiqube_id)
indiqube_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.45,
        "advertising_marketing_signal": 0.25,
        "timing_urgency": 0.45,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.50,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.40,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=indiqube_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, indiqube_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=indiqube_open_triggers,
    score=indiqube_result["score"],
    classification=indiqube_result["classification"],
    timing="NEAR_TERM",
    why_now="Board-approved strategic investment surfaced in coverage this week -- a real-estate/"
            "business-expansion story, though the underlying deal is still pre-definitive-agreement "
            "and SaiEdge itself is pre-revenue, keeping urgency moderate.",
    why_this_company="IndiQube Spaces, Bangalore HQ verified. Recently-listed managed-office-space "
                      "company securing its own future office-supply pipeline via a strategic stake.",
    business_problem="A newly-listed flexible-workspace company making its first disclosed strategic "
                      "investment as a public company needs investor-facing business-press visibility "
                      "to build credibility with the market.",
    why_business_standard="B2B real-estate/workspace strategic-investment story with listed-company "
                           "investor relevance fits BS's business readership well.",
    recommended_product="corporate_communication, investor_visibility_content",
    recommended_action="Pitch investor-visibility content on IndiQube's post-listing expansion "
                        "strategy tied to the SaiEdge investment; no marketing contact confirmed in "
                        "this pass.",
    is_qualified_target=indiqube_result["is_qualified_target"],
    score_breakdown=indiqube_result["score_breakdown"],
)

conn.close()
print("IndiQube Spaces:", indiqube_result)
