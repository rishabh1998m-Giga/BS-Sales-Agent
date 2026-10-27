#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-28 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

Three items today:

1. NEW: Sarvam AI (Bengaluru-HQ verified; legal entity Axonwise Pvt
   Ltd) signed a five-year MoU with Headquarters Integrated Defence
   Staff (Ministry of Defence), announced by HQ IDS Oct 26 2026 and
   made public by Sarvam Oct 27 2026 -- an umbrella framework for AI
   work (decision support, target acquisition, data fusion across the
   sensor-to-shooter chain) across the Army, Navy and Air Force, led
   by Sarvam's defence division "Chanakya." Deal value undisclosed.
   B2B/government deep-tech defence contract -- qualifies regardless
   of ticket size.

2. NEW: Live2.ai (Bengaluru-HQ verified; legal entity Woovly India Pvt
   Ltd, Xelpmoc-incubated) raised Rs 130 crore (~$14M) pre-Series B led
   by IvyCap Ventures, announced Oct 27 2026. Builds AI agents for
   social commerce -- tracks brand conversations across Instagram/
   TikTok/YouTube/Reddit/X and turns rights-cleared content into
   shoppable posts, plus agentic tools (crisis detection, autonomous
   response) for enterprise/global consumer brands; serves 200+ global
   brands with 90% of revenue from outside India. B2B SaaS sold to
   brands -- qualifies regardless of ticket size.

3. UPDATE (multi-trigger): Maasi (already tracked, company_id 105,
   Bangalore HQ verified 2026-10-23) raised a further Rs 6 crore
   (~$630K) pre-seed round led by Better Capital and Antler India,
   announced Oct 27 2026 -- a second, separate fundraising trigger on
   top of its Oct 22 product-launch trigger (4,000+ waitlist signups
   within 5 days of public launch, 1,200+ parents served via 500+
   caregivers). New opportunity row inserted per the existing
   multi-trigger pattern (never editing the original Oct 23 row).

Checked and declined:
  - CopperPilot (AI PCB-design agent for electronics hardware, $390K
    pre-seed led by Neon Fund, Oct 27 2026) -- most sources (FinSMEs,
    ByteTrail) describe it as Houston, TX-based; one source calls it
    "US and India" without naming an Indian city, another calls it
    "an Indian startup" with no address at all. No source names any
    of the three qualified cities specifically. Not scored --
    insufficient evidence to assume a qualified-city India HQ.

Also checked: Chittorgarh (SFC Environmental Technologies/BLS Polymers
IPOs opening this week, Jio Platforms listing imminent -- none in a
newly-qualified city), industry movement (no qualifying item found in
this pass).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# --------------------------------------------------------------- Sarvam AI
sarvam_id = repo.get_or_create_company(conn, "Sarvam AI", industry="Indian AI foundation-model company / defence AI")
repo.set_hq_status(
    conn, sarvam_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity Axonwise Private Limited (doing business as 'Sarvam AI'), registered "
             "office 2nd Floor, 732 Urban Vault, Indiranagar, Bangalore 560038 -- per the company's "
             "own Terms of Service and Privacy Policy documents. CIN not independently confirmed via "
             "aggregator search, but the company's own self-published legal documents stating this "
             "Bangalore address are strong direct evidence.",
    source_url="https://www.sarvam.ai/privacy-policy",
)
sarvam_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (sarvam_id, "government_contract", "MAJOR_PARTNERSHIP",
     "Signed a five-year MoU with Headquarters Integrated Defence Staff (Ministry of Defence) -- an "
     "umbrella framework for AI work (decision support, target acquisition, data fusion across the "
     "sensor-to-shooter chain) across the Army, Navy and Air Force, led by Sarvam's defence division "
     "'Chanakya.' Human oversight remains in place for operational decisions. Deal value and first "
     "applications undisclosed.",
     "2026-10-26", "2026-10-27", "FACT",
     "https://theprint.in/defence/design-develop-deploy-sarvam-signs-5-year-mou-with-mod-to-build-ai-for-army-navy-iaf/3083107/",
     "ThePrint / Analytics India Magazine / CIOL",
     "\"Design, develop & deploy: Sarvam signs 5-year MoU with MoD to build AI for Army, Navy, IAF\" "
     "-- HQ IDS announced Oct 26, Sarvam made it public Oct 27 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, sarvam_id, "MAJOR_PARTNERSHIP", sarvam_event_id)

sarvam_open_triggers = repo.open_trigger_count(conn, sarvam_id)
sarvam_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.60,
        "business_standard_audience_fit": 0.70,
        "estimated_marketing_capacity": 0.65,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=sarvam_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, sarvam_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="MAJOR_PARTNERSHIP",
    trigger_count=sarvam_open_triggers,
    score=sarvam_result["score"],
    classification=sarvam_result["classification"],
    timing="IMMEDIATE",
    why_now="National-strategic defence-AI MoU announced 1-2 days ago -- a major, fresh credibility "
            "milestone for one of India's leading homegrown AI companies.",
    why_this_company="Sarvam AI, Bangalore HQ verified. A flagship Indian AI company now formally "
                      "engaged across all three armed forces via its defence division.",
    business_problem="A marquee AI company securing a major government-defence mandate needs business/"
                      "policy-press visibility to reinforce its national-strategic-technology "
                      "positioning.",
    why_business_standard="A homegrown AI company's defence-ministry mandate is a strong business/"
                           "policy story fitting BS's readership; well-funded, well-known company "
                           "supports a healthy marketing-capacity estimate.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch thought-leadership content on India's sovereign-AI/defence-AI push tied "
                        "to this MoU; no marketing contact confirmed in this pass.",
    is_qualified_target=sarvam_result["is_qualified_target"],
    score_breakdown=sarvam_result["score_breakdown"],
)

# --------------------------------------------------------------- Live2.ai
live2ai_id = repo.get_or_create_company(conn, "Live2.ai", industry="AI agents for social commerce (Xelpmoc-incubated)")
repo.set_hq_status(
    conn, live2ai_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity Woovly India Private Limited, Flat No. 001, Ground Floor, HM Delphi, 7th C "
             "Main, 3rd Block, Koramangala, Bangalore 560034 (CIN U74999KA2017PTC104778, RoC-Bangalore, "
             "incorporated 18 Jul 2017) -- registered AND operational HQ both Bangalore, no "
             "discrepancy. Incubated by listed company Xelpmoc Design and Tech, also Bangalore-based.",
    source_url="https://www.zaubacorp.com/WOOVLY-INDIA-PRIVATE-LIMITED-U74999KA2017PTC104778",
)
live2ai_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (live2ai_id, "funding_round", "FUNDRAISING",
     "Raised Rs 130 crore (~$14M) pre-Series B led by IvyCap Ventures (primary investment for growth, "
     "plus a secondary component giving early shareholders partial liquidity; split/valuation "
     "undisclosed). Builds AI agents for social commerce -- tracks brand conversations across "
     "Instagram/TikTok/YouTube/Reddit/X, turns rights-cleared content into shoppable posts, plus "
     "agentic tools (crisis detection, autonomous response). Serves 200+ global brands; revenue grew "
     "4x in the past 12 months with 90% from outside India. Funds go toward its agentic-intelligence "
     "layer, enterprise/global-brand GTM, and regional cloud infra (North America/Europe/APAC).",
     "2026-10-27", "2026-10-27", "FACT",
     "https://indianstartupnews.com/funding/xelpmoc-incubated-live2ai-raises-rs-130-crore-to-build-ai-agents-for-social-commerce-12757884",
     "Indian Startup News / CIOL / DealStreetAsia",
     "\"Xelpmoc-incubated Live2.ai raises Rs 130 crore to build AI agents for social commerce\" -- "
     "Oct 27 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, live2ai_id, "FUNDRAISING", live2ai_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (live2ai_id, "Pre-Series B", "Rs 130 crore (~$14 million)", "INR", "2026-10-27",
     "IvyCap Ventures (lead)",
     "Scale agentic-intelligence layer, enterprise/global-brand go-to-market, regional cloud "
     "infrastructure (North America, Europe, APAC)",
     "https://indianstartupnews.com/funding/xelpmoc-incubated-live2ai-raises-rs-130-crore-to-build-ai-agents-for-social-commerce-12757884",
     "B2B SaaS for brands -- qualifies regardless of ticket size; 200+ global brand clients, 90% "
     "revenue from outside India"),
)
conn.commit()

live2ai_open_triggers = repo.open_trigger_count(conn, live2ai_id)
live2ai_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.60,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.45,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=live2ai_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, live2ai_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=live2ai_open_triggers,
    score=live2ai_result["score"],
    classification=live2ai_result["classification"],
    timing="IMMEDIATE",
    why_now="Pre-Series B closed 1 day ago with a strong growth narrative (4x revenue growth, 200+ "
            "global brand clients) -- a fresh, credible funding-and-traction story.",
    why_this_company="Live2.ai, Bangalore HQ verified. Xelpmoc-incubated AI-agents-for-social-commerce "
                      "platform with majority international revenue, scaling after a fresh raise.",
    business_problem="A fast-growing B2B AI/social-commerce platform expanding its enterprise GTM "
                      "globally needs business-press visibility to build category credibility with "
                      "prospective brand clients.",
    why_business_standard="B2B AI/martech funding with a strong global-revenue growth story fits BS's "
                           "business/technology readership.",
    recommended_product="corporate_communication, thought_leadership",
    recommended_action="Pitch thought-leadership content on AI-driven social commerce and India-built "
                        "AI agents winning global enterprise clients, tied to the raise; no marketing "
                        "contact confirmed in this pass.",
    is_qualified_target=live2ai_result["is_qualified_target"],
    score_breakdown=live2ai_result["score_breakdown"],
)

# --------------------------------------------------------- Maasi (multi-trigger)
maasi_id = repo.get_or_create_company(conn, "Maasi", industry="On-demand/subscription childcare and nanny platform")
maasi_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (maasi_id, "funding_round", "FUNDRAISING",
     "Raised a further Rs 6 crore (~$630K) pre-seed round led by Better Capital and Antler India "
     "(angel investors including Rapido's Rishikesh SR and Shadowfax's Vaibhav Khandelwal also "
     "participated) -- a second, separate trigger on top of its Oct 22 2026 public-launch trigger. "
     "Reports 4,000+ waitlist sign-ups within 5 days of public launch and 1,200+ parents served via "
     "500+ caregivers. Funds earmarked for caregiver recruitment/training, its tech platform, and its "
     "Bengaluru team.",
     "2026-10-27", "2026-10-27", "FACT",
     "https://entrackr.com/snippets/child-care-startup-maasi-raises-rs-6-cr-in-pre-seed-round-12757624",
     "Entrackr / BW Disrupt / StartupTalky",
     "\"Child-care startup Maasi raises Rs 6 Cr in pre-seed round\" -- Oct 27 2026, press release "
     "dateline Bengaluru",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, maasi_id, "FUNDRAISING", maasi_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (maasi_id, "Pre-seed", "Rs 6 crore (~$630K)", "INR", "2026-10-27",
     "Better Capital, Antler India (co-leads); angels incl. Rapido's Rishikesh SR, Shadowfax's "
     "Vaibhav Khandelwal, Crane VC's Siddhant Goyal, Multiply Ventures' Sanjay Ramakrishnan",
     "Caregiver recruitment/training, technology platform, Bengaluru team",
     "https://entrackr.com/snippets/child-care-startup-maasi-raises-rs-6-cr-in-pre-seed-round-12757624",
     "Second funding trigger for an already-qualified company (HQ verified 2026-10-23)"),
)
conn.commit()

maasi_open_triggers = repo.open_trigger_count(conn, maasi_id)
maasi_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.60,
        "advertising_marketing_signal": 0.55,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.45,
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
    primary_trigger="FUNDRAISING",
    trigger_count=maasi_open_triggers,
    score=maasi_result["score"],
    classification=maasi_result["classification"],
    timing="IMMEDIATE",
    why_now="Fresh pre-seed close 1 day ago, on top of a strong public-launch waitlist story from "
            "last week -- a second active news hook in under a week, now with 2 open triggers.",
    why_this_company="Maasi, Bangalore HQ verified (re-confirmed). Trust-critical childcare platform "
                      "now capitalized to scale after a strong launch.",
    business_problem="A freshly-funded, trust-critical childcare platform needs sustained business/"
                      "consumer-press visibility while both its launch and funding narratives are "
                      "active.",
    why_business_standard="Second active trigger in under a week raises this company's multi-trigger "
                           "profile -- considered, high-stakes consumer spend plus a fresh funding "
                           "story fits BS's readership well.",
    recommended_product="branded_content, digital_display",
    recommended_action="Pitch a combined launch-plus-funding founder story while both news hooks are "
                        "fresh; no marketing contact confirmed in this pass.",
    is_qualified_target=maasi_result["is_qualified_target"],
    score_breakdown=maasi_result["score_breakdown"],
)

conn.close()
print("Sarvam AI:", sarvam_result)
print("Live2.ai:", live2ai_result)
print("Maasi:", maasi_result)
