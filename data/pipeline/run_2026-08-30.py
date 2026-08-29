#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-30 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: LiveRamp (international company) opened its first-ever
India office in Hyderabad on 2026-07-01 -- since it's the company's ONLY
India presence (250+ employees already, growing to 350+, "strategic
center for AI, data science, product innovation, engineering... business
technology, finance, and customer success, supporting both regional and
global operations"), this is their India HQ under the international-
company rule, even though the legal entity LiveRamp India Pvt Ltd is
registered in Delhi (a nominal address from its 2020 incorporation,
before the company had any real India operations) -- same operational-
HQ-over-registered-office pattern as Titan/Pravaig Dynamics/Duroflex.
B2B (data-collaboration/identity-resolution platform for advertisers) --
qualifies under the brand-fit gate regardless of size.

Discovered today via a funding/expansion-news search, but the office
opening itself is ~2 months old (Jul 1 2026) -- timed as MEDIUM_TERM
(newly discovered, not urgent) rather than IMMEDIATE, same treatment as
the Tonbo Imaging discovery on 2026-08-25.

Checked and found nothing else new/dated today: Chittorgarh (no new
qualified-city DRHP), industry movement (Exchange4Media/afaqs!/
Storyboard18/Campaign India -- no qualifying item), CarbonStrong and AWS
Builder Loft Hyderabad (already seen before / not a company-HQ trigger,
skipped).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

liveramp_id = repo.get_or_create_company(conn, "LiveRamp India", industry="Data collaboration/marketing technology")
repo.set_hq_status(
    conn, liveramp_id, "HYDERABAD_HQ_VERIFIED",
    claimed_city="Hyderabad", hq_city="Hyderabad",
    evidence="International company -- India HQ verified: Hyderabad is LiveRamp's first and only "
             "India office (opened Jul 1 2026, Aparna Technopolis, HITEC City), described as a "
             "'strategic center for AI, data science, product innovation, engineering... supporting "
             "both regional and global operations,' 250+ employees already, growing to 350+. NOTE: "
             "the legal entity LiveRamp India Pvt Ltd (CIN U72900DL2020PTC375142) is registered in "
             "New Delhi -- a nominal address from its Dec 2020 incorporation, before the company had "
             "any real India operations. Qualifies under the operational-HQ rule (same pattern as "
             "Titan/Pravaig Dynamics/Duroflex).",
    source_url="https://bestmediainfo.com/mediainfo/mediainfo-digital/liveramp-opens-first-india-office-in-hyderabad-after-publicis-deal-to-hire-over-100-12123157",
)
liveramp_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (liveramp_id, "entering_india", "INTERNATIONAL_EXPANSION",
     "Opened its first-ever India office in Hyderabad (Aparna Technopolis, HITEC City), its 12th "
     "global location; 250+ employees already, plans to add 100+ more (engineering/product) over "
     "the next 12 months.",
     "2026-07-01", "2026-07-01", "FACT",
     "https://bestmediainfo.com/mediainfo/mediainfo-digital/liveramp-opens-first-india-office-in-hyderabad-after-publicis-deal-to-hire-over-100-12123157",
     "BestMediaInfo / The Wire / CXOToday",
     "\"LiveRamp opens first India office in Hyderabad after Publicis deal, to hire over 100\" -- "
     "discovered 2026-08-30, event dated Jul 1 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, liveramp_id, "INTERNATIONAL_EXPANSION", liveramp_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (liveramp_id, "entering_india", "Hyderabad", "2026-07-01",
     "First India office; strategic hub for AI/data science/engineering; 250+ employees, growing to "
     "350+ within 12 months",
     "https://bestmediainfo.com/mediainfo/mediainfo-digital/liveramp-opens-first-india-office-in-hyderabad-after-publicis-deal-to-hire-over-100-12123157",
     "Aparna Technopolis, HITEC City, Hyderabad"),
)
conn.commit()

liveramp_open_triggers = repo.open_trigger_count(conn, liveramp_id)
liveramp_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.60,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.35,
        "business_standard_audience_fit": 0.65,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.25,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="HYDERABAD_HQ_VERIFIED",
    open_trigger_count=liveramp_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, liveramp_id,
    hq_status="HYDERABAD_HQ_VERIFIED",
    primary_trigger="INTERNATIONAL_EXPANSION",
    trigger_count=liveramp_open_triggers,
    score=liveramp_result["score"],
    classification=liveramp_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Newly discovered today, but the office opening itself is ~2 months old (Jul 1 2026) -- "
            "not an urgent news-cycle trigger, but a genuinely new India HQ worth tracking going "
            "forward for future triggers (hiring milestones, further expansion).",
    why_this_company="LiveRamp India, Hyderabad HQ verified (first and only India office). Global "
                      "data-collaboration/identity-resolution platform for advertisers, entering India "
                      "at meaningful scale (250+ employees already).",
    business_problem="A newly-arrived international B2B tech company needs to build market and "
                      "talent-brand visibility in India from a standing start.",
    why_business_standard="B2B martech/adtech company entering India fits BS's business-decision-maker "
                           "readership; a 'new India entrant' corporate-narrative angle is available "
                           "while the news is still relatively fresh to Indian coverage.",
    recommended_product="corporate_communication, thought_leadership",
    recommended_action="Low-to-medium urgency; monitor for a follow-up hiring/expansion milestone "
                        "before pitching -- no India marketing/comms contact identified in this pass.",
    is_qualified_target=liveramp_result["is_qualified_target"],
    score_breakdown=liveramp_result["score_breakdown"],
)

conn.close()
print("LiveRamp India:", liveramp_result)
