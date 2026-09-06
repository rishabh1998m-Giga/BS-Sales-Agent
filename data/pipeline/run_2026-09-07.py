#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-07 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

Two new Bangalore findings, both surfaced via StartupTalky's daily
funding roundups for early September (checked several consecutive days'
roundups since the search engine hadn't yet indexed a same-day one):

  - Ultrahuman: closed a $70M Series C (Qualcomm Ventures-led, with
    Labcorp, Alpha Wave, Blume Ventures, Nexus Venture Partners, Alteria
    Capital) on Sep 3 2026, valuing the company at $365M. Evolving from
    a smart-ring wearable into a broader health-intelligence platform.
    Smart rings (~$350-500+) are a considered/higher-ticket B2C purchase.
  - RentoMojo: set its IPO price band (Rs 384-404/share) on Sep 4 2026 --
    a fresh milestone in an already-progressing IPO (DRHP filed Mar 28
    2026, company converted to a public limited company Jan 2026).
    Furniture/appliance rental is a considered household decision, not
    routine/daily consumption.

Checked and declined: Comet (Bengaluru D2C sneaker brand, Rs 100 Cr
Series B, Sep 4 2026) -- HQ qualifies, but priced at Rs 4,299-4,499
("40-50% savings versus Nike/Adidas... aspirational value above budget
brands" per coverage), this reads as mid-market discretionary fashion
retail rather than a considered/higher-ticket purchase -- same reasoning
as excluding Britannia/Third Wave Coffee/Peeko. Not scored.

Also checked: Chittorgarh (same Paptech Corp DRHP as recent days, no
qualified-city company), industry movement (no qualifying item).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# --------------------------------------------------------------- Ultrahuman
ultrahuman_id = repo.get_or_create_company(conn, "Ultrahuman", industry="Wearable health-tech")
repo.set_hq_status(
    conn, ultrahuman_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Ultrahuman Healthcare Pvt Ltd, Bommanahalli, Hosur Main Road, Bangalore 560068 "
             "(CIN U74999KA2019PTC129250).",
    source_url="https://www.zaubacorp.com/ULTRAHUMAN-HEALTHCARE-PRIVATE-LIMITED-U74999KA2019PTC129250",
)
uh_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (ultrahuman_id, "strategic_investment", "FUNDRAISING",
     "Closed a $70M Series C (split $65M equity / $5M debt) led by Qualcomm Ventures, with Labcorp, "
     "Alpha Wave, Blume Ventures, Nexus Venture Partners, and Alteria Capital participating -- values "
     "the company at $365M. Evolving from smart-ring wearables into a broader multimodal "
     "health-intelligence/human-computer-interface platform.",
     "2026-09-03", "2026-09-03", "FACT",
     "https://techcrunch.com/2026/09/03/qualcomm-backs-ultrahuman-in-70m-round-on-bet-to-turn-smart-rings-into-computers/",
     "TechCrunch / Business Standard",
     "\"Qualcomm backs Ultrahuman in $70M round on bet to turn smart rings into computers\" -- Sep 3 "
     "2026, $365M valuation",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, ultrahuman_id, "FUNDRAISING", uh_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (ultrahuman_id, "Series C", "$70 million ($65M equity + $5M debt)", "USD", "2026-09-03",
     "Qualcomm Ventures (lead), Labcorp, Alpha Wave, Blume Ventures, Nexus Venture Partners, Alteria Capital",
     "Expand beyond wearables into a multimodal health-intelligence platform",
     "https://techcrunch.com/2026/09/03/qualcomm-backs-ultrahuman-in-70m-round-on-bet-to-turn-smart-rings-into-computers/",
     "$365M valuation; smart ring (~$350-500+) is a considered/higher-ticket B2C purchase"),
)
conn.commit()

uh_open_triggers = repo.open_trigger_count(conn, ultrahuman_id)
uh_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.50,
        "timing_urgency": 0.70,
        "business_standard_audience_fit": 0.65,
        "estimated_marketing_capacity": 0.70,
        "decision_maker_availability": 0.40,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.60,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=uh_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, ultrahuman_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=uh_open_triggers,
    score=uh_result["score"],
    classification=uh_result["classification"],
    timing="IMMEDIATE",
    why_now="Series C closed 4 days ago with a marquee strategic investor (Qualcomm Ventures) and a "
            "notable valuation jump ($365M) -- strong, fresh news hook.",
    why_this_company="Ultrahuman, Bangalore HQ verified. Fast-growing wearable health-tech company "
                      "repositioning as a broader health-intelligence platform.",
    business_problem="A premium wearable-hardware brand pivoting into platform/software territory "
                      "needs to build category-defining narrative credibility, not just product "
                      "awareness.",
    why_business_standard="Considered/higher-ticket B2C hardware plus a genuine strategic/technology "
                           "narrative (Qualcomm's human-computer-interface bet) fits BS's business and "
                           "affluent-consumer readership.",
    recommended_product="branded_content, thought_leadership, premium_display",
    recommended_action="Pitch a founder thought-leadership angle on the 'wearables to health platform' "
                        "pivot tied to the Qualcomm round; no marketing contact confirmed in this pass.",
    is_qualified_target=uh_result["is_qualified_target"],
    score_breakdown=uh_result["score_breakdown"],
)

# --------------------------------------------------------------- RentoMojo
rentomojo_id = repo.get_or_create_company(conn, "RentoMojo", industry="Furniture/appliance rental")
repo.set_hq_status(
    conn, rentomojo_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="RentoMojo Ltd (converted from Pvt Ltd to public Jan 2 2026), BHIVE Workspace, AKR Tech "
             "Park, Hosur Road, Bangalore 560068 (CIN U72200KA2012PLC063551).",
    source_url="https://www.zaubacorp.com/RENTOMOJO-LIMITED-U72200KA2012PLC063551",
)
rm_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (rentomojo_id, "ipo_approval", "IPO",
     "Set its IPO price band at Rs 384-404 per share -- a fresh milestone in an already-progressing "
     "IPO (DRHP filed Mar 28 2026, converted from private to public limited company Jan 2 2026).",
     "2026-09-04", "2026-09-04", "FACT",
     "https://www.chittorgarh.com/ipo/rentomojo-ipo/2971/",
     "Chittorgarh / StartupTalky",
     "\"RentoMojo Sets IPO Price Band\" -- Sep 4 2026 daily funding roundup, price band Rs 384-404",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, rentomojo_id, "IPO", rm_event_id)

conn.execute(
    """INSERT INTO ipo_events
       (company_id, ipo_status, stage, ipo_size, source_url, evidence)
       VALUES (?,?,?,?,?,?)""",
    (rentomojo_id, "IPO_CONFIRMED", "Price band set", "Price band Rs 384-404/share",
     "https://www.chittorgarh.com/ipo/rentomojo-ipo/2971/",
     "DRHP filed Mar 28 2026; converted to public limited company Jan 2026; price band set Sep 4 2026"),
)
conn.commit()

rm_open_triggers = repo.open_trigger_count(conn, rentomojo_id)
rm_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.80,
        "business_standard_audience_fit": 0.75,
        "estimated_marketing_capacity": 0.60,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.55,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=rm_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, rentomojo_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="IPO",
    trigger_count=rm_open_triggers,
    score=rm_result["score"],
    classification=rm_result["classification"],
    timing="IMMEDIATE",
    why_now="Price band just set (3 days ago) -- the IPO listing window is imminent, a high-urgency "
            "pre-listing visibility moment.",
    why_this_company="RentoMojo, Bangalore HQ verified. Furniture/appliance rental platform now at the "
                      "final pre-listing stage of its IPO.",
    business_problem="A consumer-facing rental platform going public needs investor and retail-investor "
                      "visibility right as the listing window opens.",
    why_business_standard="Pre-listing IPO story with a set price band is a textbook BS investor-"
                           "audience fit -- urgency is high given the imminent listing.",
    recommended_product="investor_visibility_content, corporate_communication",
    recommended_action="Pitch investor-visibility content immediately given the imminent listing "
                        "window; no marketing contact confirmed in this pass.",
    is_qualified_target=rm_result["is_qualified_target"],
    score_breakdown=rm_result["score_breakdown"],
)

conn.close()
print("Ultrahuman:", uh_result)
print("RentoMojo:", rm_result)
