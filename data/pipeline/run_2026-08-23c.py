#!/usr/bin/env python3
"""
Third pass for 2026-08-23 -- a live timed test run requested directly, using
the new 3-city scope for real: Garuda Aerospace (first Chennai-qualified
opportunity) and Skyroot Aerospace (first Hyderabad-qualified opportunity).
Both verified via CIN/registered-office before scoring, per the hard gate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ------------------------------------------------------------- Garuda Aerospace
garuda_id = repo.get_or_create_company(
    conn, "Garuda Aerospace", industry="Drone technology (agri/defence/enterprise)",
    website="https://www.garudaaerospace.com",
)
repo.set_hq_status(
    conn, garuda_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Registered office: Third Floor, Agni Business Centre, K B Dasan Road, Alwarpet, "
             "Chennai 600018 (CIN U74900TN2015PLC102474)",
    source_url="https://tracxn.com/d/legal-entities/india/garuda-aerospace-limited/__QdzUiJxc9A1Z8TwscosAfJCs6ZdDFe2uGAYOmBCzxzk",
)

garuda_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (garuda_id, "ipo_approval", "IPO",
     "SEBI issued final observation (approval) for a Rs 1,000 Cr book-built IPO: Rs 750 Cr fresh "
     "issue + Rs 250 Cr OFS. MS Dhoni-backed dronetech (agri/defence/enterprise UAVs). Target "
     "listing late 2026.",
     None, "2026-08-05", "FACT",
     "https://inc42.com/buzz/dronetech-startup-garuda-aerospace-gets-sebi-nod-for-%E2%82%B9750-cr-ipo/",
     "Inc42 / IPO Central",
     "\"Dronetech Startup Garuda Aerospace Gets SEBI Nod For Rs750 Cr+ IPO\" - SEBI observation Aug 5 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, garuda_id, "IPO", garuda_event_id)

conn.execute(
    """INSERT INTO ipo_events
       (company_id, ipo_status, stage, ipo_size, lead_managers, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (garuda_id, "IPO_REPORTED", "SEBI approved (observation issued)", "Rs 1,000 Cr (Rs 750 Cr fresh + Rs 250 Cr OFS)",
     "SBI Capital Markets, Axis Capital, ICICI Securities, IIFL Capital Services",
     "https://inc42.com/buzz/dronetech-startup-garuda-aerospace-gets-sebi-nod-for-%E2%82%B9750-cr-ipo/",
     "SEBI final observation Aug 5 2026; target listing late 2026, no fixed date yet"),
)
conn.commit()

garuda_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (garuda_id, "Agnishwar Jayaprakash", "Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/Agnishwar_Jayaprakash"),
).lastrowid
conn.commit()

garuda_open_triggers = repo.open_trigger_count(conn, garuda_id)
garuda_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80, "advertising_marketing_signal": 0.45,
        "timing_urgency": 0.70, "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.50, "decision_maker_availability": 0.85,
        "official_contact_availability": 0.20, "strategic_relevance": 0.70,
    },
    hq_status="CHENNAI_HQ_VERIFIED", open_trigger_count=garuda_open_triggers, config=cfg,
)
repo.insert_opportunity(
    conn, garuda_id,
    hq_status="CHENNAI_HQ_VERIFIED", primary_trigger="IPO", trigger_count=garuda_open_triggers,
    score=garuda_result["score"], classification=garuda_result["classification"], timing="NEAR_TERM",
    why_now="SEBI approval landed 18 days ago; target listing is late 2026 with no fixed date, "
            "so the pre-listing visibility window is open now and will stay open for a while.",
    why_this_company="Garuda Aerospace, Chennai HQ verified (CIN U74900TN2015PLC102474) -- first "
                      "Chennai-qualified opportunity under the broadened city scope. MS Dhoni-backed "
                      "dronetech B2B company (agri/defence/enterprise), Rs 1,000 Cr IPO.",
    business_problem="Needs investor/business-audience credibility ahead of listing for a B2B "
                      "hardware company less consumer-visible than a typical fintech IPO story.",
    why_business_standard="Pre-IPO B2B defence/enterprise-tech company is squarely BS's "
                           "investor/business-decision-maker audience.",
    recommended_product="corporate_communication, thought_leadership, premium_display",
    recommended_contact_id=garuda_contact_id,
    recommended_action="Pitch pre-IPO corporate visibility to Agnishwar Jayaprakash; confirm listing "
                        "timeline stays live before leading with urgency language.",
    is_qualified_target=garuda_result["is_qualified_target"], score_breakdown=garuda_result["score_breakdown"],
)

# ------------------------------------------------------------ Skyroot Aerospace
skyroot_id = repo.get_or_create_company(
    conn, "Skyroot Aerospace", industry="Private space launch vehicles", website="https://www.skyroot.in",
)
repo.set_hq_status(
    conn, skyroot_id, "HYDERABAD_HQ_VERIFIED",
    claimed_city="Hyderabad", hq_city="Hyderabad",
    evidence="Registered office: 4B/4B1, GMR Hyderabad Aviation SEZ, GMR Aerospace and Industrial "
             "Park, Mamidipally, Rangareddy, Hyderabad 500108 (CIN U74999TG2018PTC125073)",
    source_url="https://tracxn.com/d/legal-entities/india/skyroot-aerospace-private-limited/__m9dLWsM1CotvuM9pete4o-wm5fNTnQIP3_kI9XfskSs",
)

skyroot_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (skyroot_id, "capacity_expansion", "EXPANSION",
     "Will invest Rs 250 Cr in a new Tamil Nadu facility (Thoothukudi) for storage/assembly/"
     "integration/testing of launch vehicles, ~500 jobs -- MoU signed at the Vetri Tamil Nadu "
     "Investors' Conclave, near ISRO's second spaceport at Kulasekarapattinam.",
     None, "2026-08-13", "FACT",
     "https://www.business-standard.com/india-news/vetri-tamil-nadu-investment-conclave-2026-agnikul-skyroot-semiconductor-investments-126081300888_1.html",
     "Business Standard / The Hans India",
     "\"Skyroot deepens aerospace footprint with Tamil Nadu facility\" -- Rs 250 Cr, MoU at Vetri Conclave Aug 13 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, skyroot_id, "EXPANSION", skyroot_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (skyroot_id, "new_plant", "Thoothukudi, Tamil Nadu", "2026-08-13",
     "Rs 250 Cr investment, ~500 jobs; storage/assembly/integration/testing facility for launch vehicles",
     "https://www.thehansindia.com/business/skyroot-deepens-aerospace-footprint-with-tamil-nadu-facility-1109171",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave 2026"),
)
conn.commit()

skyroot_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (skyroot_id, "Pawan Kumar Chandana", "Co-Founder, CEO & CTO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/Skyroot_Aerospace"),
).lastrowid
conn.commit()

skyroot_open_triggers = repo.open_trigger_count(conn, skyroot_id)
skyroot_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75, "advertising_marketing_signal": 0.45,
        "timing_urgency": 0.60, "business_standard_audience_fit": 0.80,
        "estimated_marketing_capacity": 0.55, "decision_maker_availability": 0.75,
        "official_contact_availability": 0.20, "strategic_relevance": 0.65,
    },
    hq_status="HYDERABAD_HQ_VERIFIED", open_trigger_count=skyroot_open_triggers, config=cfg,
)
repo.insert_opportunity(
    conn, skyroot_id,
    hq_status="HYDERABAD_HQ_VERIFIED", primary_trigger="EXPANSION", trigger_count=skyroot_open_triggers,
    score=skyroot_result["score"], classification=skyroot_result["classification"], timing="NEAR_TERM",
    why_now="Rs 250 Cr Tamil Nadu facility MoU was signed 10 days ago -- first Hyderabad-qualified "
            "opportunity under the broadened city scope, still within the fresh-news window.",
    why_this_company="Skyroot Aerospace, Hyderabad HQ verified (CIN U74999TG2018PTC125073). India's "
                      "first private orbital-launch company, space-tech unicorn, expanding manufacturing "
                      "capacity for a 12-launch/year cadence target.",
    business_problem="A deep-tech B2B/B2G company needs business-audience visibility for a capital "
                      "and manufacturing story, not a consumer-facing pitch.",
    why_business_standard="Strategic manufacturing expansion by a unicorn space-tech company is a "
                           "core BS business-audience story (capital allocation, industrial policy "
                           "relevance via ISRO's new spaceport).",
    recommended_product="corporate_communication, business_audience_display, thought_leadership",
    recommended_contact_id=skyroot_contact_id,
    recommended_action="Pitch business-audience content around the Tamil Nadu facility investment "
                        "and India's private space-launch narrative to Pawan Kumar Chandana.",
    is_qualified_target=skyroot_result["is_qualified_target"], score_breakdown=skyroot_result["score_breakdown"],
)

conn.close()
print("Garuda Aerospace:", garuda_result)
print("Skyroot Aerospace:", skyroot_result)
