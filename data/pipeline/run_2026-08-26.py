#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-26 daily-sales-brief run.

Context: the automated 04:04 UTC trigger actually completed today (session
cse_013PKbJ31UXvWQQMjxgzniFB, status SUCCEEDED, ran 04:07-04:19 UTC) -- a
change from the last two days' outright silent failures -- but still
produced no commit on main and no data/daily_report_2026-08-26.md. Its
transcript isn't inspectable with the tools available in this session, so
the exact failure point (report-save step vs. git-push step) is unknown.
Reported to the user; this run was executed live in-session again instead.

Findings today:
  - Airbound Aerospace (Bangalore, new): $37M Series A (Greenoaks-led,
    announced 2026-08-24/25) for autonomous cargo-drone logistics --
    B2B, fresh, strong opportunity.
  - Tonbo Imaging (already tracked from 2026-08-25 pass): MATERIAL
    CORRECTION -- the Dec 22 2025 DRHP was actually WITHDRAWN; the company
    refiled Aug 4 2026 and again Aug 14 2026. This is new information
    that changes the IPO's status and timing, so it's scored as a fresh
    opportunity today per project convention (insert, never edit, a past
    opportunities row) rather than silently correcting yesterday's entry.
  - Watchlist: AltDRX resolved to verified_qualified (Bangalore-registered
    tokenized real-estate platform, CIN U70200KA2022PTC166655) -- no fresh
    trigger scored today since its only funding event is 15 months old.

Checked and deliberately NOT added (kept out to avoid inflating the
pipeline with weak evidence):
  - Guidehouse's new Hyderabad hub -- Guidehouse's India presence spans
    Chennai/Trivandrum/Gurugram/Hyderabad with no single stated India HQ;
    opening one more hub doesn't establish Hyderabad as the India HQ (same
    reasoning as excluding Adobe/IKEA's non-HQ Indian offices). Left
    unverified rather than assumed.
  - Third Wave Coffee's Rs 408 Cr round -- Bengaluru HQ, but a coffee-chain
    is routine/everyday consumption, not a considered/higher-ticket
    purchase, so it fails the target-criteria brand-fit gate (same
    reasoning as excluding Britannia).
  - WATER (Hyderabad physical-AI startup, FLOW chair/CAMA bed) -- could
    not confirm a registered office/CIN in this pass; not fabricated.

Industry-movement scan (Exchange4Media/afaqs!) and decision-maker
movement spot-check: no qualifying finding today -- honestly omitted.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ------------------------------------------------------------------ AltDRX
altdrx_id = repo.get_or_create_company(conn, "AltDRX", industry="Tokenised real-estate investment platform")
repo.set_hq_status(
    conn, altdrx_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Alt DRX Private Limited, registered office Indiranagar 2nd Stage, Bengaluru "
             "(CIN U70200KA2022PTC166655).",
    source_url="https://www.zaubacorp.com/ALT-DRX-PRIVATE-LIMITED-U70200KA2022PTC166655",
)
# No opportunity scored -- only funding event on record closed May 2025, 15 months old, not a
# fresh trigger. HQ verification recorded for future reference per watchlist process.

# =========================================================================
# Airbound Aerospace -- new company, fresh FUNDRAISING trigger
# =========================================================================
airbound_id = repo.get_or_create_company(conn, "Airbound Aerospace", industry="Autonomous cargo drones/logistics")
repo.set_hq_status(
    conn, airbound_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Airbound Aerospace Pvt Ltd, registered office Bangalore, Karnataka "
             "(CIN U62100KA2021PTC152640).",
    source_url="https://www.zaubacorp.com/AIRBOUND-AEROSPACE-PRIVATE-LIMITED-U62100KA2021PTC152640",
)
airbound_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (airbound_id, "strategic_investment", "FUNDRAISING",
     "Raised $37M Series A led by Greenoaks (DoorDash, Lachy Groom, Lightspeed, Humba Ventures "
     "participating) to scale autonomous cargo-drone logistics; signed a commercial deployment "
     "agreement with the Andhra Pradesh government for a 3-city drone delivery network.",
     "2026-08-24", "2026-08-24", "FACT",
     "https://www.business-standard.com/industry/news/airbound-raises-37-million-andhra-pradesh-drone-delivery-network-126082500638_1.html",
     "Business Standard / TechCrunch",
     "\"India's Airbound bags $37M to take on trucks with rocket-like drones\" -- Series A, Aug 24-25 2026, "
     "~$50M raised total since 2023 launch",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, airbound_id, "FUNDRAISING", airbound_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (airbound_id, "Series A", "$37 million", "USD", "2026-08-24",
     "Greenoaks (lead); DoorDash, Lachy Groom, Lightspeed, Humba Ventures",
     "Scale autonomous cargo-drone logistics; Andhra Pradesh govt deployment for 3-city delivery network",
     "https://techcrunch.com/2026/08/24/indias-airbound-bags-37m-to-take-on-trucks-with-rocket-like-drones/",
     "~$50M raised total since 2023; aircraft designed/tested in India, cargo-first before passenger transport"),
)
conn.commit()

airbound_open_triggers = repo.open_trigger_count(conn, airbound_id)
airbound_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.85,
        "advertising_marketing_signal": 0.45,
        "timing_urgency": 0.90,
        "business_standard_audience_fit": 0.80,
        "estimated_marketing_capacity": 0.65,
        "decision_maker_availability": 0.55,
        "official_contact_availability": 0.15,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=airbound_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, airbound_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=airbound_open_triggers,
    score=airbound_result["score"],
    classification=airbound_result["classification"],
    timing="IMMEDIATE",
    why_now="Series A closed 1-2 days ago, still in the fresh-announcement press-visibility window; also "
            "carries a newsworthy government-deployment angle (Andhra Pradesh drone corridor).",
    why_this_company="Airbound Aerospace, Bengaluru HQ verified. Deep-tech logistics/aerospace startup with "
                      "credible marquee investors (Greenoaks, DoorDash) and a live government contract.",
    business_problem="Pre-mainstream-brand deep-tech company needs investor and enterprise-customer "
                      "credibility following a large raise, not consumer awareness.",
    why_business_standard="Strong fit for BS's investor/business readership -- large fresh Series A plus a "
                           "government-logistics angle is a compelling corporate-narrative/thought-leadership "
                           "story, similar to the existing Skyroot/Agnikul space-tech opportunities.",
    recommended_product="thought_leadership, corporate_communication, branded_content",
    recommended_action="Pitch founder thought-leadership tied to the Series A and Andhra Pradesh deployment "
                        "while the news cycle is still fresh (1-2 days old); no marketing/comms contact "
                        "identified yet -- verify before outreach.",
    is_qualified_target=airbound_result["is_qualified_target"],
    score_breakdown=airbound_result["score_breakdown"],
)

# =========================================================================
# Tonbo Imaging -- correction: original DRHP was withdrawn, refiled twice
# =========================================================================
tonbo_row = conn.execute("SELECT company_id FROM companies WHERE name = ?", ("Tonbo Imaging",)).fetchone()
tonbo_id = tonbo_row[0]

tonbo_correction_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (tonbo_id, "drhp_filed", "IPO",
     "CORRECTION to the 2026-08-25 entry: the original Dec 22 2025 DRHP was WITHDRAWN. Tonbo Imaging "
     "refiled its DRHP with SEBI on Aug 4 2026, then refiled again on Aug 14 2026. Still an OFS-only "
     "issue of up to 1.81 Cr shares; JM Financial is lead manager, KFin Technologies is registrar.",
     "2026-08-14", "2026-08-26", "FACT",
     "https://www.chittorgarh.com/ipo/tonbo-imaging-india-ipo/3215/",
     "Chittorgarh.com",
     "Chittorgarh IPO page confirms initial Dec 2025 submission was withdrawn and refiled Aug 4 2026, "
     "refiled again Aug 14 2026 -- found via today's Chittorgarh check, corrects yesterday's stale "
     "Dec-2025-only record",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, tonbo_id, "IPO", tonbo_correction_event_id)

conn.execute(
    """INSERT INTO ipo_events
       (company_id, ipo_status, stage, ipo_size, source_url, evidence)
       VALUES (?,?,?,?,?,?)""",
    (tonbo_id, "IPO_REPORTED", "DRHP refiled (Aug 14 2026), original Dec 2025 filing withdrawn",
     "OFS of up to 1.81 Cr shares (no fresh issue)",
     "https://www.chittorgarh.com/ipo/tonbo-imaging-india-ipo/3215/",
     "Refiling is materially fresher (12 days old) than the withdrawn Dec 2025 filing -- re-scored with "
     "higher timing urgency than 2026-08-25's entry"),
)
conn.commit()

tonbo_open_triggers = repo.open_trigger_count(conn, tonbo_id)
tonbo_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.75,
        "business_standard_audience_fit": 0.80,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.65,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=tonbo_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, tonbo_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="IPO",
    trigger_count=tonbo_open_triggers,
    score=tonbo_result["score"],
    classification=tonbo_result["classification"],
    timing="NEAR_TERM",
    why_now="The Aug 14 2026 refiling is only 12 days old and materially changes the picture from "
            "yesterday's entry (which relied on the withdrawn Dec 2025 filing) -- re-scored with higher "
            "timing urgency now that the IPO process is active again.",
    why_this_company="Tonbo Imaging, Bengaluru HQ verified. India's largest defence-optics OEM, now actively "
                      "back in the IPO process after a withdraw-and-refile.",
    business_problem="Pre-listing defence-tech company needs investor/business credibility; the "
                      "withdraw-and-refile is itself a narrative point worth addressing proactively.",
    why_business_standard="Defence-tech IPO story fits BS's investor readership; the refiling gives a "
                           "genuine news hook that wasn't available yesterday.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch investor-visibility content now that the DRHP is active again; the "
                        "withdraw-refile history is worth transparently addressing in any pitch angle.",
    is_qualified_target=tonbo_result["is_qualified_target"],
    score_breakdown=tonbo_result["score_breakdown"],
)

conn.close()
print("Airbound Aerospace:", airbound_result)
print("Tonbo Imaging (correction):", tonbo_result)
