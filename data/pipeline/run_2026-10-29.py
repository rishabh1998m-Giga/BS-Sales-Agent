#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-29 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Simplismart (Bengaluru-HQ verified; legal entity Verute
Technologies Pvt Ltd) -- an AI-infrastructure company whose software
helps enterprises run AI models more efficiently -- raised a $14M
all-primary Series B led by Dallas Venture Capital, with NVIDIA, Accel,
Shastra VC, and Micromax participating, announced Oct 27-28 2026. Takes
the four-year-old company to a ~$100M valuation; reported 14x revenue
growth. B2B AI-infrastructure platform -- qualifies regardless of
ticket size.

Checked and declined:
  - BioStack (healthtech/medical-AI data-infrastructure startup, $9.5M
    seed led by Peak XV Partners with Y Combinator/DCVC/Afore Capital
    etc. participating, announced Oct 22 2026) -- genuinely conflicting
    HQ claims: one source (Indian Retailer) calls it "Chennai-based,"
    another describes it as "a San Francisco-based healthcare
    technology company," with no source confirming an India-registered
    entity or CIN either way. Also a 6-day-old announcement by the
    time this surfaced, not fresh for this window. Left unscored on
    HQ ambiguity rather than assumed.
  - Matiks (Bengaluru, social/puzzle gaming platform -- mental math,
    memory, logic games -- $10M pre-Series A led by General Catalyst,
    with Ronnie Screwvala/Info Edge Ventures/Tanglin Venture Partners
    participating) -- Bengaluru HQ plausible, but mobile/social gaming
    is a routine, mass-market, typically-free-to-play B2C entertainment
    category, not a considered/higher-ticket purchase -- same
    reasoning as excluding Spill Games. Not scored on brand-fit
    grounds.

Also checked: Chittorgarh (Jio Platforms listed today at a ~21% debut
premium -- Mumbai/Reliance HQ, not qualified; Paras Healthcare listed
today -- Gurugram HQ, not qualified; SFC Environmental Technologies/
BLS Polymers IPOs still open, Core4 Engineers allotment -- none in a
newly-qualified city), industry movement via afaqs!/Storyboard18 (only
stale items resurfaced -- a ~3-month-old TVS Motor media-review story,
an April Samsung/L'Oreal pitch roundup, a 2026 Blackberrys creative-
mandate win -- none dated to this window or in scope for Section 16).

Honest "one new opportunity, several declined" -- nothing fabricated.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

simplismart_id = repo.get_or_create_company(conn, "Simplismart", industry="AI infrastructure / inference optimization platform")
repo.set_hq_status(
    conn, simplismart_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity Verute Technologies Private Limited, CIN U72200KA2022PTC165981, "
             "registered office 133/2, 4th Floor, Janardhan Towers, Residency Road, Bengaluru 560025 "
             "(incorporated 12 Sep 2022) -- confirmed via Tracxn and PitchBook, registered AND "
             "operational HQ both Bangalore, no discrepancy.",
    source_url="https://tracxn.com/d/companies/simplismart/__vQ7UoZdcJrqECEmTHroF9255tc01M9HvJngvtlXbOng",
)
simplismart_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (simplismart_id, "funding_round", "FUNDRAISING",
     "Raised a $14M all-primary Series B led by Dallas Venture Capital, with NVIDIA, Accel, Shastra "
     "VC, and Micromax participating -- values the four-year-old AI-infrastructure company at roughly "
     "$100M. Reports cite 14x revenue growth. Simplismart's software helps enterprises run AI models "
     "more efficiently (inference optimization).",
     "2026-10-27", "2026-10-28", "FACT",
     "https://analyticsindiamag.com/ai-news/bengaluru-ai-startup-simplismart-raises-14-mn-in-nvidia-backed-round",
     "Analytics India Magazine / StartupTalky / AdGully",
     "\"Bengaluru AI Startup Simplismart Raises $14 Mn in NVIDIA-Backed Round\" -- Oct 27-28 2026, "
     "corroborated across Analytics India Magazine, StartupTalky, AdGully, TradingView",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, simplismart_id, "FUNDRAISING", simplismart_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (simplismart_id, "Series B", "$14 million (all-primary)", "USD", "2026-10-27",
     "Dallas Venture Capital (lead), NVIDIA, Accel, Shastra VC, Micromax",
     "Scale AI-infrastructure/inference-optimization platform",
     "https://analyticsindiamag.com/ai-news/bengaluru-ai-startup-simplismart-raises-14-mn-in-nvidia-backed-round",
     "~$100M valuation; 14x reported revenue growth; B2B AI infra qualifies regardless of ticket size"),
)
conn.commit()

simplismart_open_triggers = repo.open_trigger_count(conn, simplismart_id)
simplismart_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.60,
        "business_standard_audience_fit": 0.60,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.55,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=simplismart_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, simplismart_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=simplismart_open_triggers,
    score=simplismart_result["score"],
    classification=simplismart_result["classification"],
    timing="IMMEDIATE",
    why_now="Series B closed with marquee strategic backing (NVIDIA) and a strong reported revenue-"
            "growth story -- a fresh, credible funding-and-traction hook.",
    why_this_company="Simplismart, Bangalore HQ verified. AI-infrastructure company with NVIDIA "
                      "strategic backing, scaling fast after a strong Series B.",
    business_problem="A fast-growing, NVIDIA-backed AI-infrastructure company needs business/"
                      "investor-press visibility to build category credibility as it scales "
                      "enterprise sales globally.",
    why_business_standard="B2B deep-tech AI funding with a marquee strategic investor (NVIDIA) and a "
                           "strong revenue-growth narrative fits BS's business/technology readership.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch thought-leadership content on India-built AI infrastructure winning "
                        "NVIDIA's strategic backing, tied to the Series B; no marketing contact "
                        "confirmed in this pass.",
    is_qualified_target=simplismart_result["is_qualified_target"],
    score_breakdown=simplismart_result["score_breakdown"],
)

conn.close()
print("Simplismart:", simplismart_result)
