#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-31 daily-sales-brief run
(Saturday). Self-bound 1:30 AM IST trigger.

New finding: Cent (Bengaluru-HQ verified; legal entity Centai
Technologies Pvt Ltd) -- a D2C preventive-healthcare platform
operating its own diagnostic centres (full-body scans/"One-Scan
Protocol") -- raised a $15M Series A (equity + debt) co-led by Blume
Ventures and existing investor South Park Commons, announced Oct 27-28
2026. Also acquired Medsee, an AI-powered radiology-reporting
platform, as part of the same announcement. Founded Jan 2025 by
well-known operators: Shashank ND (Practo co-founder), Anshul
Khandelwal (former Ola CMO), and Arpit Garg (former Lenskart product
head). Covered directly by Business Standard itself. Preventive
diagnostic healthcare is a considered, high-stakes purchase -- clears
the brand-fit gate easily despite B2C classification, same reasoning
as Even Healthcare (2026-10-20).

Checked and declined:
  - Ultraviolette (Bengaluru, already HQ-verified on 2026-08-24) --
    its $85M Series E led by Yali Capital and TDK Ventures was
    actually announced 23 Sep 2026, over five weeks ago and inside the
    previously-documented session-dormancy gap. Resurfaced in today's
    search but is not fresh news for this window -- not re-scored.
  - Troovy (healthy-snacks D2C brand, Rs 100 Cr Series B led by
    Fireside Ventures, Oct 27 2026) -- HQ is Gurugram, not a qualified
    city.
  - Procol (AI procurement-orchestration platform) -- operating HQ is
    Gurugram (per the company's own careers page) with its registered
    office in New Delhi (Pitampura, per its own privacy policy) --
    neither is a qualified city.

Also checked: Chittorgarh (SFC Environmental Technologies/BLS Polymers
IPOs closing this week, Core4 Engineers allotment -- none in a newly-
qualified city), industry movement via afaqs!/Storyboard18 (Lodestar
UM's AMFI media-account win is undated and untied to the three
qualified cities; Famous Innovations' Bengaluru CCO hire is an
agency's own leadership move, not a client marketing-leader trigger;
WeWork India/RMAI FLAME items resurfaced again with no new detail).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

cent_id = repo.get_or_create_company(conn, "Cent", industry="D2C preventive healthcare / diagnostics platform")
repo.set_hq_status(
    conn, cent_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity Centai Technologies Private Limited, CIN U62090KA2025PTC197421, "
             "registered office in Basavanagudi, Bengaluru (Karnataka RoC) -- confirmed via Tracxn. "
             "Registered AND operational HQ both Bangalore, no discrepancy.",
    source_url="https://tracxn.com/d/companies/cent/__nGDqR31GGxsLqi8F9UPFu-yeeD0fvFnC1V8Hx0ItmvY",
)
cent_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (cent_id, "funding_round", "FUNDRAISING",
     "Raised a $15M Series A (equity + debt) co-led by Blume Ventures and existing investor South "
     "Park Commons -- also acquired Medsee, an AI-powered radiology-reporting platform, as part of "
     "the same announcement. Cent operates its own diagnostic centres offering preventive full-body "
     "scans under its 'One-Scan Protocol.' Founded Jan 2025 by Shashank ND (Practo co-founder), "
     "Anshul Khandelwal (former Ola CMO), and Arpit Garg (former Lenskart product head).",
     "2026-10-27", "2026-10-28", "FACT",
     "https://www.business-standard.com/companies/start-ups/cent-raises-15-million-to-expand-ai-powered-preventive-healthcare-platform-126102701118_1.html",
     "Business Standard / Inc42 / YourStory",
     "\"Cent raises $15 million to expand AI-powered preventive healthcare platform\" -- Oct 27-28 "
     "2026, corroborated across Business Standard, Inc42, YourStory, Analytics India Magazine",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, cent_id, "FUNDRAISING", cent_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (cent_id, "Series A", "$15 million (equity + debt)", "USD", "2026-10-27",
     "Blume Ventures, South Park Commons (co-leads, existing investor)",
     "Expand AI-powered preventive-healthcare diagnostic platform; acquired AI radiology platform "
     "Medsee",
     "https://www.business-standard.com/companies/start-ups/cent-raises-15-million-to-expand-ai-powered-preventive-healthcare-platform-126102701118_1.html",
     "Preventive diagnostic healthcare is a considered/high-stakes purchase, clears brand-fit gate "
     "regardless of B2C classification; covered directly by Business Standard"),
)
conn.commit()

cent_open_triggers = repo.open_trigger_count(conn, cent_id)
cent_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.65,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.35,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=cent_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, cent_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=cent_open_triggers,
    score=cent_result["score"],
    classification=cent_result["classification"],
    timing="IMMEDIATE",
    why_now="Series A plus an AI-radiology acquisition announced 2-3 days ago, led by well-known "
            "operator-founders (Practo/Ola/Lenskart alumni) -- a strong, fresh, credible funding-and-"
            "M&A story, and already covered directly by Business Standard.",
    why_this_company="Cent, Bangalore HQ verified. Preventive-healthcare diagnostics platform backed "
                      "by proven founders, scaling via its own diagnostic centres plus an AI-radiology "
                      "acquisition.",
    business_problem="A newly-funded preventive-healthcare brand with marquee founders needs patient-"
                      "trust and category-education content to grow adoption of full-body preventive "
                      "scanning.",
    why_business_standard="Considered, high-stakes healthcare purchase with a strong founder-"
                           "credibility narrative and a fresh M&A angle fits BS's business and "
                           "affluent-consumer readership; already has BS editorial coverage.",
    recommended_product="branded_content, thought_leadership, premium_display",
    recommended_action="Pitch a founder-story/thought-leadership angle on preventive healthcare and "
                        "AI-driven diagnostics tied to the raise and Medsee acquisition; no marketing "
                        "contact confirmed in this pass.",
    is_qualified_target=cent_result["is_qualified_target"],
    score_breakdown=cent_result["score_breakdown"],
)

conn.close()
print("Cent:", cent_result)
