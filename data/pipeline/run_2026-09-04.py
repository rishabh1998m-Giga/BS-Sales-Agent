#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-04 daily-sales-brief run.
Self-bound 1:30 AM IST trigger. Also Friday -- weekly rollup generated
separately.

Two new findings today, both Bangalore, both dated Sep 3 2026:
  - Zerodha: received SEBI approval for merchant banking via its wholly
    owned subsidiary Zerodha Corporate Advisors, expanding beyond
    brokerage into equity-IPO advisory for new-age businesses.
  - Cradlewise: raised $12M Series A (3one4 Capital, Prudent Investment
    Management) for its AI-first smart-crib baby-tech business.
    Dual-HQ'd San Francisco/Bengaluru per Forbes India profile, with a
    real Bangalore-registered operating entity (Cradlewise Innovations
    Pvt Ltd) -- not just a nominal office. Premium smart crib (~$1500+)
    is a considered/higher-ticket B2C purchase.

Also resolved a long-pending watchlist item: Coorg Wilderness Resort is
operated by Paul Resorts & Hotels Pvt Ltd, Bangalore-registered (CIN
U55101KA2003PTC032853) -- updated config/watchlist.yaml directly (no DB
insert needed here since no fresh trigger is associated with it today).

Checked and found nothing else new: Chittorgarh (no qualified-city DRHP),
Aham Housing Finance and Sid's Farm fundraises (both dated July-August,
not today), Bijliride EV partnership (multi-city deployment, no single
clear HQ trigger), industry movement (no qualifying item).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ------------------------------------------------------------------ Zerodha
zerodha_id = repo.get_or_create_company(conn, "Zerodha", industry="Fintech/stockbroking")
repo.set_hq_status(
    conn, zerodha_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Zerodha Broking Ltd, JP Nagar, Bangalore 560078 (CIN U65929KA2018PLC116815).",
    source_url="https://www.zaubacorp.com/ZERODHA-BROKING-LIMITED-U65929KA2018PLC116815",
)
zerodha_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (zerodha_id, "major_tender", "MAJOR_PARTNERSHIP",
     "Received SEBI approval to operate as a merchant banker through its wholly owned subsidiary "
     "Zerodha Corporate Advisors, expanding beyond brokerage into equity-IPO advisory for new-age "
     "businesses. Application submitted Apr 27 2026; approval reported Sep 3 2026.",
     "2026-09-03", "2026-09-03", "FACT",
     "https://www.theswipeup.com/2026/09/zerodha-receives-sebi-approval-for.html",
     "The Swipe Up / StartupTalky",
     "\"Zerodha receives Sebi approval for commercial banking, going beyond brokerage\" -- Sep 3 2026, "
     "operations expected to begin over the next few months",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, zerodha_id, "MAJOR_PARTNERSHIP", zerodha_event_id)

zerodha_open_triggers = repo.open_trigger_count(conn, zerodha_id)
zerodha_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.45,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.70,
        "decision_maker_availability": 0.35,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=zerodha_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, zerodha_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="MAJOR_PARTNERSHIP",
    trigger_count=zerodha_open_triggers,
    score=zerodha_result["score"],
    classification=zerodha_result["classification"],
    timing="IMMEDIATE",
    why_now="SEBI approval reported 1 day ago; a genuine new-line-of-business story (merchant "
            "banking/equity-IPO advisory) with a fresh news hook before operations formally begin.",
    why_this_company="Zerodha, Bangalore HQ verified. India's largest discount broker, now expanding "
                      "into IPO advisory via a new subsidiary -- major strategic move.",
    business_problem="A brokerage-first brand entering a new, more institutional business line needs "
                      "credibility with corporates/issuers, a different audience than its retail-trader "
                      "base.",
    why_business_standard="Textbook BS fit: a major fintech's expansion into investment-banking-adjacent "
                           "services is squarely a business/investor-decision-maker story.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch corporate-communication/thought-leadership content introducing Zerodha "
                        "Corporate Advisors while the news is fresh; no marketing contact confirmed in "
                        "this pass.",
    is_qualified_target=zerodha_result["is_qualified_target"],
    score_breakdown=zerodha_result["score_breakdown"],
)

# ---------------------------------------------------------------- Cradlewise
cradlewise_id = repo.get_or_create_company(conn, "Cradlewise", industry="Baby-tech/consumer hardware")
repo.set_hq_status(
    conn, cradlewise_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Cradlewise Innovations Pvt Ltd, Kadugodi, Bangalore 560067 (CIN U36999KA2019PTC123276). "
             "Dual-HQ'd San Francisco/Bengaluru per Forbes India profile -- a real Bangalore operating "
             "entity, not a nominal office.",
    source_url="https://www.zaubacorp.com/CRADLEWISE-INNOVATIONS-PRIVATE-LIMITED-U36999KA2019PTC123276",
)
cradlewise_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (cradlewise_id, "strategic_investment", "FUNDRAISING",
     "Raised $12 million in a Series A round led by 3one4 Capital and Prudent Investment Management "
     "for its AI-first smart-crib business (channel expansion, product R&D, geographic expansion).",
     "2026-09-03", "2026-09-03", "FACT",
     "https://startuptalky.com/news/daily-indian-funding-roundup-key-news-3-september-2026/",
     "StartupTalky",
     "\"Cradlewise Raises $12 Million\" -- Sep 3 2026 daily funding roundup",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, cradlewise_id, "FUNDRAISING", cradlewise_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (cradlewise_id, "Series A", "$12 million", "USD", "2026-09-03",
     "3one4 Capital (lead), Prudent Investment Management",
     "Channel expansion, product R&D, geographic expansion",
     "https://startuptalky.com/news/daily-indian-funding-roundup-key-news-3-september-2026/",
     "AI-first smart crib, premium baby-tech product (~$1500+), considered/higher-ticket B2C purchase"),
)
conn.commit()

cradlewise_open_triggers = repo.open_trigger_count(conn, cradlewise_id)
cradlewise_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.45,
        "timing_urgency": 0.80,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.35,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.55,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=cradlewise_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, cradlewise_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=cradlewise_open_triggers,
    score=cradlewise_result["score"],
    classification=cradlewise_result["classification"],
    timing="IMMEDIATE",
    why_now="Series A closed 1 day ago, still in the fresh-announcement press-visibility window.",
    why_this_company="Cradlewise, Bangalore HQ verified (dual-HQ with San Francisco). AI-first "
                      "premium baby-tech hardware maker with a fresh, well-covered raise.",
    business_problem="A premium consumer-hardware brand needs to build category awareness and trust "
                      "for a high-ticket, infrequent-purchase product among Indian new parents.",
    why_business_standard="Considered/higher-ticket B2C purchase (~$1500+ smart crib) fits BS's affluent "
                           "readership; fresh funding news gives a natural corporate-narrative hook.",
    recommended_product="branded_content, premium_display",
    recommended_action="Pitch branded content/premium display tied to the Series A and India go-to-"
                        "market push; no marketing contact confirmed in this pass.",
    is_qualified_target=cradlewise_result["is_qualified_target"],
    score_breakdown=cradlewise_result["score_breakdown"],
)

conn.close()
print("Zerodha:", zerodha_result)
print("Cradlewise:", cradlewise_result)
