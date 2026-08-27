#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-27 daily-sales-brief run.

Context: the automated 04:04 UTC trigger fired a third time today
(session cse_016LyA2vpJRboPdUBbgeRNTD, reported SUCCEEDED, but ran only
~3 minutes vs the prior day's 12) and again produced no commit/report --
three consecutive days of the same failure mode despite the trigger
itself reporting success. Per the user's explicit request today, the old
create_new_session_on_fire trigger (trig_01SfdDkyqFZv2rfuXTJxQeR8) was
deleted and replaced with a new one bound directly to this conversation
(trig_016bfNkuSgZaguWS9QCc9uv2, self-bind via persistent_session_id),
firing daily at 04:30 UTC (10:00 AM IST) and delivering the .docx into
this same session via SendUserFile -- since manual in-session runs have
now worked reliably 4 days running (Aug 24-27) while every fresh-session
firing has failed silently.

New finding today, from the same Aug 13 2026 Vetri Tamil Nadu Investors'
Conclave already mined on 2026-08-25 (checking who else signed MoUs
there continues to surface qualified-city companies not yet in our
database):
  - Plugzmart / MERAS Plugins Pvt Ltd (Chennai, new): Rs 100 Cr MoU to
    scale EV-charger manufacturing at Oragadam, ~500 jobs. B2B
    (EV-charging infrastructure sold to businesses/fleets/govt).

Checked and deliberately excluded:
  - Peeko (Bengaluru babycare quick-commerce platform, Rs 67.4 Cr Series A,
    announced Aug 20 2026) -- fails the brand-fit gate. 30-minute-delivery
    baby consumables/apparel/toys is routine, repeat-purchase quick
    commerce, not a "considered, higher-ticket purchase" under
    config/target-criteria.yaml -- same reasoning as excluding Britannia.
  - Coorg Wilderness Resort (watchlist, needs_clarification) -- confirmed
    it's operated by Paul John Resorts & Hotels (Bangalore hospitality
    group, also runs The Paul Bangalore, Kumarakom Lake Resort) but still
    no registered-office/CIN found for the parent entity. Left unresolved
    rather than guessed.
  - "Absolute Barbecues awards its digital mandate to Schbang" -- found
    via the afaqs!/industry-movement check, but the announcement date is
    July 25 2022, not a fresh finding. No industry-movement item
    qualifies today.

Decision-maker movement and IPO (Chittorgarh) checks: no changes/no new
qualified-city IPO found today.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ------------------------------------------------------------- Plugzmart
plugzmart_id = repo.get_or_create_company(conn, "Plugzmart (MERAS Plugins)", industry="EV charging infrastructure")
repo.set_hq_status(
    conn, plugzmart_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="MERAS Plugins Pvt Ltd (brand: Plugzmart), registered office 4/36 Mustara Begum Street, "
             "Royapettah, Chennai 600014 (CIN U31905TN2018PTC126007). IIT Madras Research Park-incubated.",
    source_url="https://builtinchennai.in/company/plugzmart",
)
plugzmart_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (plugzmart_id, "capacity_expansion", "EXPANSION",
     "Signed a Rs 100 crore MoU with the Tamil Nadu government to scale EV-charger manufacturing, R&D, "
     "and charging-infrastructure capacity at Oragadam near Chennai, creating 500+ deep-tech jobs -- MoU "
     "signed at the Vetri Tamil Nadu Investors' Conclave.",
     "2026-08-13", "2026-08-13", "FACT",
     "https://www.dtnext.in/amp/story/news/tamilnadu/plugzmart-inks-rs-100-crore-mou-with-tamil-nadu-to-generate-500-jobs",
     "DT Next / India Education Diary",
     "\"Plugzmart inks Rs 100 crore MoU with Tamil Nadu; to generate 500 jobs\" -- Aug 13 2026 conclave, "
     "scaling manufacturing at Oragadam",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, plugzmart_id, "EXPANSION", plugzmart_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (plugzmart_id, "capacity_expansion", "Oragadam, Chennai", "2026-08-13",
     "Rs 100 crore investment; 500+ jobs in hardware engineering, power electronics, embedded software, "
     "advanced manufacturing over 3 years",
     "https://www.dtnext.in/amp/story/news/tamilnadu/plugzmart-inks-rs-100-crore-mou-with-tamil-nadu-to-generate-500-jobs",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave, Aug 13 2026"),
)
conn.commit()

plugzmart_open_triggers = repo.open_trigger_count(conn, plugzmart_id)
plugzmart_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.60,
        "advertising_marketing_signal": 0.30,
        "timing_urgency": 0.50,
        "business_standard_audience_fit": 0.60,
        "estimated_marketing_capacity": 0.40,
        "decision_maker_availability": 0.35,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=plugzmart_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, plugzmart_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=plugzmart_open_triggers,
    score=plugzmart_result["score"],
    classification=plugzmart_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Rs 100 Cr Oragadam MoU is 14 days old, same conclave that produced Saint-Gobain/Daimler/"
            "Trivitron/Agnikul -- smaller-scale deep-tech commitment than those, so a modest opportunity.",
    why_this_company="Plugzmart (MERAS Plugins), Chennai HQ verified, IIT Madras-incubated EV-charging "
                      "infrastructure manufacturer scaling up.",
    business_problem="Small-to-mid deep-tech manufacturer with limited public marketing footprint; capex "
                      "news is a modest visibility opportunity.",
    why_business_standard="B2B EV-infrastructure manufacturing story fits BS's industrial/business coverage, "
                           "narrower audience overlap than the conclave's larger commitments.",
    recommended_product="corporate_storytelling, digital_display",
    recommended_action="Low-to-medium urgency watch; group with other Vetri TN Conclave stories "
                        "(Saint-Gobain, Daimler, Trivitron, Agnikul) if BS wants a combined feature on the "
                        "investment wave.",
    is_qualified_target=plugzmart_result["is_qualified_target"],
    score_breakdown=plugzmart_result["score_breakdown"],
)

conn.close()
print("Plugzmart:", plugzmart_result)
