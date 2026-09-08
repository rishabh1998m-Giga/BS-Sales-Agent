#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-09 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Udaan (B2B e-commerce marketplace, founded 2016 by
ex-Flipkart execs Amod Malviya/Sujeet Kumar/Vaibhav Gupta) is acquiring
Swiggy-owned LYNK Logistics for Rs 500 crore in a share-swap deal
(Swiggy receiving a combined 3.2% stake in Udaan), announced Sep 7-8
2026, reportedly as Udaan "readies for IPO." Operating legal entity
Hiveloop Technology Pvt Ltd is Bangalore-registered (holding entity is
Trusthoot Internet, per deal mechanics) -- clean HQ match, no
registered-vs-operational discrepancy. B2B marketplace -- qualifies
regardless of ticket size.

Checked and declined:
  - Circolife (Rs 4.5 Cr pre-Series A, subscription AC) -- Mumbai HQ,
    not a qualified city.
  - Kuku Technologies (Kuku FM) -- operational/corporate HQ is HSR
    Layout, Bangalore per the company's own contact page (registered
    entity is Mumbai) -- HQ would likely qualify via the operational-HQ
    rule, but the flagship product (audio-content subscription app) is
    a low-ticket recurring consumer subscription, closer to routine mass-
    market B2C than a considered/higher-ticket purchase -- same
    reasoning as excluding Peeko/Comet/Third Wave Coffee. Not scored on
    brand-fit grounds.
  - Jio's 2027 satellite launch target -- Reliance/Jio is Mumbai HQ'd,
    not a qualified city.

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

udaan_id = repo.get_or_create_company(conn, "Udaan", industry="B2B e-commerce marketplace")
repo.set_hq_status(
    conn, udaan_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Operating legal entity Hiveloop Technology Pvt Ltd, HSR Layout, Bangalore 560102 (CIN "
             "U72900KA2016PTC093868, RoC-Bangalore) -- registered AND operational HQ both Bangalore, "
             "no discrepancy. (Holding entity Trusthoot Internet is referenced in the LYNK deal "
             "mechanics as the share-issuing parent.)",
    source_url="https://www.zaubacorp.com/company/HIVELOOP-TECHNOLOGY-PRIVATE-LIMITED/U72900KA2016PTC093868",
)
udaan_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (udaan_id, "acquisition_announced", "ACQUISITION",
     "Acquiring Swiggy-owned LYNK Logistics for Rs 500 crore in a share-swap deal (Trusthoot Internet "
     "issuing 166,534 Series R CCPS to Swiggy Networks at $314.4/share, plus a separate Rs 75 Cr cash "
     "infusion for 0.4% more) -- Swiggy's total stake in Udaan reaching 3.2%. LYNK generated Rs 668 Cr "
     "revenue in FY26 (2.9% of Swiggy's consolidated revenue); Bengaluru/Hyderabad/Chennai/Kolkata "
     "account for 75% of LYNK's revenue. Deal reported alongside Udaan 'readying for IPO' "
     "(unconfirmed, INFERENCE-tier). Closing expected by Oct 22 2026, pending regulatory clearance.",
     "2026-09-07", "2026-09-08", "FACT",
     "https://www.business-standard.com/industry/news/udaan-buys-swiggy-s-lynk-for-500-cr-as-e-commerce-firm-readies-for-ipo-126090701103_1.html",
     "Business Standard / Inc42 / MediaNama",
     "\"Udaan buys Swiggy's LYNK for Rs 500 cr as e-commerce firm readies for IPO\" -- Sep 7-8 2026, "
     "multiple corroborating sources",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, udaan_id, "ACQUISITION", udaan_event_id)

udaan_open_triggers = repo.open_trigger_count(conn, udaan_id)
udaan_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.75,
        "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.70,
        "decision_maker_availability": 0.35,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=udaan_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, udaan_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="ACQUISITION",
    trigger_count=udaan_open_triggers,
    score=udaan_result["score"],
    classification=udaan_result["classification"],
    timing="IMMEDIATE",
    why_now="Deal announced 1-2 days ago, tied to a reported (unconfirmed) IPO-readiness narrative -- "
            "a strong, fresh corporate-narrative hook while the news cycle is active.",
    why_this_company="Udaan, Bangalore HQ verified (Hiveloop Technology Pvt Ltd). Major B2B e-commerce "
                      "unicorn making a significant logistics acquisition ahead of a possible listing.",
    business_problem="A pre-IPO B2B unicorn absorbing a logistics business needs investor/business-"
                      "press visibility to build the growth-and-scale narrative ahead of any listing.",
    why_business_standard="Textbook BS fit: a major B2B platform's acquisition, tied to IPO-readiness "
                           "speculation, is squarely a business/investor-decision-maker story.",
    recommended_product="corporate_communication, investor_visibility_content, thought_leadership",
    recommended_action="Pitch corporate-communication content on the LYNK acquisition and logistics "
                        "integration; if BS wants to lead with the IPO angle, flag it as unconfirmed/"
                        "INFERENCE-tier until independently verified. No marketing contact confirmed in "
                        "this pass.",
    is_qualified_target=udaan_result["is_qualified_target"],
    score_breakdown=udaan_result["score_breakdown"],
)

conn.close()
print("Udaan:", udaan_result)
