#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-11-15 daily-sales-brief run
(Sunday). Self-bound 1:30 AM IST trigger.

CORRECTIVE ACTION this run: on 2026-11-06, a search surfaced a
"homepage snapshot" summary claiming four dated headlines including
"altM $10.3M round led by Rainmatter/Mela Ventures (Nov 5)" and
"EloElo $80M Series C (Nov 5)". At the time, targeted re-searches for
each failed to turn up any corroborating source, so neither was
recorded -- logged as a likely search-tool synthesis error.

Today, following a separate StartupTalky daily-roundup lead (dated
articles for Nov 4-5 2026), BOTH rounds were re-searched from scratch
and this time are extensively corroborated by many independent,
reputable, dated sources (Inc42, YourStory -- URLs dated 2026/11 --
Entrepreneur India, TechCrunch/TheNextWeb, Dealroom, NewsBytes,
Exchange4Media, GreenQueen, AgroSpectrum, and others). The 2026-11-06
dismissal was a research error, not a correct call -- both rounds are
real and closed. Correcting that error now:

  - altM (legal entity Alt Material Innovations Private Limited,
    Bengaluru -- CB Insights places it at Electronic City Phase 2,
    Konappana Agrahara, Bengaluru; consistently described as
    "Bengaluru-based" across Inc42/YourStory/Entrepreneur
    India/TheAIWorld/AgroSpectrum) -- raised $10.3M Series A led by
    Rainmatter by Zerodha and Mela Ventures (existing investors
    Omnivore/Theia Ventures/Aureolis Ventures/Spectrum Impact also
    participated), announced 5 Nov 2026. Founded 2022 by Apoorv Garg
    and Yugal Raj Jain (both ex-Tesla), with cofounder/CSO Velankar.
    Converts agricultural residue into specialty chemicals/
    biomaterials (thermoset binders, silica, rheology modifiers,
    cellulosic pulp) -- a clean B2B deep-tech fit, qualifies
    regardless of ticket size. SCORED below.
  - EloElo / Story TV (Bengaluru micro-drama/live-social-entertainment
    app) -- raised $80M Series C co-led by Hornbill Capital and
    NBCUniversal, announced 4 Nov 2026, valuing the company at $500M
    (40M+ MAU, 300M app installs across its four apps). HQ is
    genuinely Bengaluru and the round is real, but Story TV is a
    free-to-download, ad/coin/subscription-monetized mass-market
    entertainment app (microdrama streaming) -- the video-streaming
    equivalent of the already-excluded Matiks/Spill Games social-
    gaming category: routine, mass-market B2C entertainment, not a
    considered/higher-ticket purchase. Declined on brand-fit, not
    scored, despite the funding being fully confirmed.

Honest note: no other new findings surfaced in today's broader sweep
(Chittorgarh, real-estate news for Prestige/Sumadhura/Puravankara --
only FY26/FY27 aggregate pipeline commentary, nothing dated to this
window -- and industry-movement sources).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

altm_id = repo.get_or_create_company(conn, "altM", industry="Specialty chemicals / biomaterials from agricultural residue")
repo.set_hq_status(
    conn, altm_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity Alt Material Innovations Private Limited, founded 2022 by Apoorv Garg and "
             "Yugal Raj Jain (both ex-Tesla) with cofounder/CSO Velankar. CB Insights places the company "
             "at Electronic City Phase 2 Industrial Area, Konappana Agrahara, Bengaluru -- consistently "
             "corroborated as Bengaluru-based across Inc42, YourStory, Entrepreneur India, TheAIWorld, "
             "and AgroSpectrum India. No single third-party CIN registry listing located under this exact "
             "name in this pass, but multi-source editorial consistency plus CB Insights' specific "
             "Bengaluru address meets the same evidentiary bar used previously for Sarvam AI.",
    source_url="https://www.cbinsights.com/company/altmat/financials",
)
altm_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (altm_id, "funding_round", "FUNDRAISING",
     "Raised $10.3M (~Rs 97.5 Cr) Series A led by Rainmatter by Zerodha and Mela Ventures, with "
     "existing investors Omnivore, Theia Ventures, Aureolis Ventures, and Spectrum Impact also "
     "participating. Follows a $3.5M seed round in 2023. altM converts agricultural residue into "
     "specialty chemicals and biomaterials (thermoset binders, silica, rheology modifiers, cellulosic "
     "pulp) -- six molecules taken to demonstration scale, three selected for pilot production. Funds "
     "will scale manufacturing/R&D toward commercialization; a 1,000-tonne/year commercial plant is "
     "targeted by 2028.",
     "2026-11-05", "2026-11-05", "FACT",
     "https://yourstory.com/2026/11/altm-raises-103m-series-a-funding-rainmatter-mela-ventures",
     "YourStory / Inc42 / Entrepreneur India / Dealroom / AgroSpectrum India",
     "\"altM raises $10.3M in Series A funding led by Rainmatter, Mela Ventures\" -- 5 Nov 2026, "
     "independently corroborated across at least 8 reputable outlets. Corrective re-scoring: this round "
     "was first encountered via an unverifiable search summary on 2026-11-06 and could not be confirmed "
     "at that time; it is now extensively corroborated and is scored here as the genuine finding it is, "
     "ten days after the original announcement, in place of the missed same-week window.",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, altm_id, "FUNDRAISING", altm_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (altm_id, "Series A", "$10.3 million", "USD", "2026-11-05",
     "Rainmatter by Zerodha, Mela Ventures (co-leads); Omnivore, Theia Ventures, Aureolis Ventures, "
     "Spectrum Impact (existing investors)",
     "Scale manufacturing and R&D to commercialize agri-waste-derived specialty chemicals/biomaterials",
     "https://yourstory.com/2026/11/altm-raises-103m-series-a-funding-rainmatter-mela-ventures",
     "B2B deep-tech/cleantech qualifies regardless of ticket size; founders are ex-Tesla operators, "
     "strong technical credibility narrative"),
)
conn.commit()

altm_open_triggers = repo.open_trigger_count(conn, altm_id)
altm_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.60,
        "advertising_marketing_signal": 0.30,
        "timing_urgency": 0.40,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.40,
        "decision_maker_availability": 0.25,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=altm_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, altm_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=altm_open_triggers,
    score=altm_result["score"],
    classification=altm_result["classification"],
    timing="NEAR_TERM",
    why_now="A $10.3M Series A (Nov 5 2026) to scale commercial manufacturing of agri-waste-derived "
            "specialty chemicals -- a credible deep-tech sustainability story with ex-Tesla founder "
            "pedigree, though the news cycle is now ~10 days old (scored late due to an earlier "
            "verification miss, documented in this script's docstring).",
    why_this_company="altM, Bangalore HQ verified. B2B cleantech/materials-science company turning "
                      "agricultural residue into specialty chemicals, backed by Rainmatter and Mela "
                      "Ventures, founded by ex-Tesla engineers.",
    business_problem="A newly-funded deep-tech materials company moving from pilot to commercial scale "
                      "needs credibility-building business/sustainability press as it approaches "
                      "commercial launch.",
    why_business_standard="B2B cleantech/circular-economy funding story with strong founder pedigree "
                           "(ex-Tesla) fits BS's business and sustainability-focused readership.",
    recommended_product="corporate_communication, thought_leadership, sustainability_content",
    recommended_action="Pitch a founder-story/thought-leadership angle on India-built circular-economy "
                        "chemicals manufacturing tied to the Series A; no marketing contact confirmed in "
                        "this pass.",
    is_qualified_target=altm_result["is_qualified_target"],
    score_breakdown=altm_result["score_breakdown"],
)

conn.close()
print("altM:", altm_result)
