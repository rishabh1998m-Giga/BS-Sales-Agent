#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-23 daily-sales-brief run
(Friday -- also run generate_weekly_report.py). Self-bound 1:30 AM IST
trigger.

New finding: Maasi (childcare/on-demand nanny platform, operated by
Elephant in the Room Infotech Pvt Ltd) launched publicly in Bengaluru
on Oct 22 2026, offering trained/background-verified nannies on-
demand and via subscription (Instant Nanny visits from Rs 660;
subscriptions from Rs 15,660/month; live-in 24x7 nanny Rs 24,600/
month; postnatal "Japa" nanny Rs 33,660/month; governess from Rs
35,660/month). Already served 1,200 families and built a 5,000+
parent waitlist during an invite-only beta, with 400+ caregivers
onboarded. Founded by Gargi Pandey, Aashuthosh "Aashu" Manchali and
Reshov Roy, who previously ran Urban Parents Club, a Bengaluru parent
community. Childcare is a trust-critical, high-stakes, considered
purchase at a meaningful recurring monthly spend -- clears the brand-
fit gate easily despite being B2C, same reasoning as Even Healthcare
(2026-10-20).

Checked and declined/left unscored:
  - CureBay (rural healthcare clinic network, Rs 100 Cr Pre-Series C
    led by IvyCap Ventures, Oct 22 2026) -- HQ is Bhubaneswar, Odisha,
    not a qualified city.
  - Karta AI (Bengaluru, agentic voice AI for BFSI -- banks/insurers/
    fintechs, $3M seed led by PeerCapital and Cedar Hill Capital, Oct
    22 2026) -- consistently described as Bengaluru-based across
    multiple outlets, with a Bangalore-located job posting as
    corroborating operational evidence, but no registered-entity CIN
    could be located to confirm the legal registered office. B2B BFSI
    SaaS would qualify regardless of ticket size if HQ were confirmed
    -- worth a dedicated follow-up once a CIN surfaces. Left unscored
    rather than assumed.

Also checked: Chittorgarh (Jio Platforms/Paras Healthcare IPOs still
open -- Mumbai/Gurugram HQ respectively, not qualified; Tonbo Imaging/
Zetwerk/Bonfiglioli allotments -- already-tracked or non-qualified-
city issues), industry movement via afaqs!/Storyboard18 (only global/
non-India agency news -- Publicis-FTC LiveRamp settlement, Adidas
media review, Innocean India layoffs, WPP CEO pay package -- none a
qualifying brand-agency mandate story for the three qualified cities).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

maasi_id = repo.get_or_create_company(conn, "Maasi", industry="On-demand/subscription childcare and nanny platform")
repo.set_hq_status(
    conn, maasi_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Operated by Elephant in the Room Infotech Private Limited, 431, 25th Main Road, "
             "Parangi Palaya, Sector 2, HSR Layout, Bangalore South, Karnataka 560102 (CIN "
             "U63120KA2025PTC202307, RoC-Bangalore, incorporated 5 May 2025, status Active). Directors "
             "Aashuthosh Manchali and Gargi Pandey match the publicly reported co-founders -- "
             "registered AND operational HQ both Bangalore, no discrepancy.",
    source_url="https://tracxn.com/d/legal-entities/india/elephant-in-the-room-infotech-private-limited/__FlOxj01F9n30eYlk0L5cyHRX0Q2czg1aIJmpKFw-G8g",
)
maasi_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (maasi_id, "product_launch", "PRODUCT_LAUNCH",
     "Publicly launched its on-demand/subscription childcare and nanny platform in Bengaluru, offering "
     "trained, background-verified caregivers (Instant Nanny visits from Rs 660; monthly subscriptions "
     "from Rs 15,660; live-in 24x7 nanny Rs 24,600/month; postnatal 'Japa' nanny Rs 33,660/month; "
     "governess from Rs 35,660/month). Already served 1,200 families with 400+ caregivers and a 5,000+ "
     "parent waitlist from an invite-only beta.",
     "2026-10-22", "2026-10-22", "FACT",
     "https://indiantelevision.com/mam/maasi-launches-in-bengaluru-to-bring-trained-verified-nannies-on-demand/",
     "Indian Television Dot Com / YourStory",
     "\"Maasi launches in Bengaluru to bring trained, verified nannies on demand\" -- Oct 22 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, maasi_id, "PRODUCT_LAUNCH", maasi_event_id)

conn.execute(
    """INSERT INTO product_launches
       (company_id, brand, product_name, launch_date, target_audience, campaign_geography,
        marketing_activity, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (maasi_id, "Maasi", "On-demand/subscription childcare and nanny platform", "2026-10-22",
     "Parents of infants/young children in Bengaluru", "Bengaluru",
     "Public launch following an invite-only beta (1,200 families served, 5,000+ parent waitlist); "
     "app-based booking via iOS/Android and app.mymaasi.com",
     "https://indiantelevision.com/mam/maasi-launches-in-bengaluru-to-bring-trained-verified-nannies-on-demand/",
     "\"Maasi launches in Bengaluru to bring trained, verified nannies on demand\" -- Oct 22 2026"),
)
conn.commit()

maasi_open_triggers = repo.open_trigger_count(conn, maasi_id)
maasi_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.55,
        "advertising_marketing_signal": 0.55,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.50,
        "estimated_marketing_capacity": 0.40,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.40,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=maasi_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, maasi_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="PRODUCT_LAUNCH",
    trigger_count=maasi_open_triggers,
    score=maasi_result["score"],
    classification=maasi_result["classification"],
    timing="IMMEDIATE",
    why_now="Public launch yesterday after a strong invite-only beta (1,200 families served, 5,000+ "
            "waitlist) -- a fresh consumer-launch hook while the news is new.",
    why_this_company="Maasi, Bangalore HQ verified. Trust-critical childcare platform launching "
                      "publicly with early demand signals well ahead of typical early-stage traction.",
    business_problem="A newly-launched childcare platform needs to build parent trust and category "
                      "awareness quickly in a sensitive, safety-first purchase category.",
    why_business_standard="Considered, high-stakes, recurring-spend consumer service (Rs 15K-35K+/month "
                           "subscriptions) fits BS's affluent-consumer readership; early-stage launch "
                           "caps marketing capacity and this at WATCH rather than higher.",
    recommended_product="branded_content, digital_display",
    recommended_action="Low-to-medium urgency; pitch a founder-story/trust-building content angle tied "
                        "to the Bengaluru launch if BS wants to move on it; no marketing contact "
                        "confirmed in this pass.",
    is_qualified_target=maasi_result["is_qualified_target"],
    score_breakdown=maasi_result["score_breakdown"],
)

conn.close()
print("Maasi:", maasi_result)
