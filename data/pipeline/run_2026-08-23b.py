#!/usr/bin/env python3
"""
Second pass for 2026-08-23: three NEW Bangalore-HQ companies not already in
the companies table (Ather Energy, Yulu, River Mobility), each HQ-verified
before scoring per the hard gate. Also records the outcome of a
competitor-advertising sweep across all 8 config/publishers.yaml publishers
for the companies already tracked (Sections 9-10) -- a genuine null result,
not fabricated to fill the section.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ------------------------------------------------------------- Ather Energy
ather_id = repo.get_or_create_company(
    conn, "Ather Energy", industry="Electric two-wheelers", website="https://www.atherenergy.com",
)
repo.set_hq_status(
    conn, ather_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Registered office: 3rd Floor, Tower D, IBC Knowledge Park, Bannerghatta Main Road, "
             "Bangalore 560029 (CIN U40100KA2013PLC093769)",
    source_url="https://www.zaubacorp.com/ATHER-ENERGY-LIMITED-U40100KA2013PLC093769",
)

ather_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (ather_id, "product_launch", "PRODUCT_LAUNCH",
     "Ather's 4th annual Community Day (Aug 29, 2026, Bengaluru) will unveil/launch the first "
     "production scooter on its new EL platform -- the company's first new vehicle architecture "
     "since the 450 series, targeting the Rs 1-1.25 lakh mass-market segment.",
     "2026-08-29", "2026-08-23", "FACT",
     "https://www.autocarindia.com/bike-news/athers-el-platform-scooter-to-debut-on-august-29-440218",
     "Autocar India / BikeDekho / ZigWheels",
     "\"Ather EL01 to launch on August 29\" - multiple auto trade outlets confirm the date and "
     "platform significance ahead of the event",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, ather_id, "PRODUCT_LAUNCH", ather_event_id)

conn.execute(
    """INSERT INTO product_launches
       (company_id, brand, product_name, launch_date, target_audience, marketing_activity, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?)""",
    (ather_id, "Ather", "EL01 (EL platform)", "2026-08-29",
     "Mass-market EV buyers (Rs 1-1.25 lakh segment), Ather's first attempt at this price band",
     "Community Day flagship launch event; teaser campaign already running pre-event",
     "https://www.cartoq.com/bike-news/ather-energy-el-platform-scooter-community-day-2026/",
     "Teased ahead of Aug 29 India launch; billed as Ather's biggest platform since the 450 series"),
)
conn.commit()

ather_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (ather_id, "Tarun Mehta", "Co-Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/Ather_Energy"),
).lastrowid
conn.commit()

ather_open_triggers = repo.open_trigger_count(conn, ather_id)
ather_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.85,
        "advertising_marketing_signal": 0.70,
        "timing_urgency": 0.90,
        "business_standard_audience_fit": 0.65,
        "estimated_marketing_capacity": 0.60,
        "decision_maker_availability": 0.80,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=ather_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, ather_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="PRODUCT_LAUNCH",
    trigger_count=ather_open_triggers,
    score=ather_result["score"],
    classification=ather_result["classification"],
    timing="IMMEDIATE",
    why_now="EL01 launches at Community Day in 6 days (Aug 29) -- the pre-launch hype window is "
            "open right now and closes the day of the event.",
    why_this_company="Ather Energy, Bengaluru HQ verified. Launching its biggest new vehicle "
                      "platform since the 450 series, entering the mass-market EV scooter segment "
                      "for the first time.",
    business_problem="Needs pre-launch visibility and credibility for an entry into a new, more "
                      "price-sensitive customer segment than its existing base.",
    why_business_standard="A public EV manufacturer's platform-level strategic pivot into a new "
                           "price segment is a business-audience story (market strategy, margin "
                           "implications), not just a consumer-auto story.",
    recommended_product="premium_display, branded_content, thought_leadership",
    recommended_contact_id=ather_contact_id,
    recommended_action="Pitch pre-launch coverage now, ahead of the Aug 29 Community Day event -- "
                        "the window closes once the launch itself generates its own news cycle.",
    is_qualified_bangalore=ather_result["is_qualified_bangalore"],
    score_breakdown=ather_result["score_breakdown"],
)

# ------------------------------------------------------------------- Yulu
yulu_id = repo.get_or_create_company(
    conn, "Yulu", industry="Shared electric mobility", website="https://www.yulu.bike",
)
repo.set_hq_status(
    conn, yulu_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Multiple outlets (YourStory, Adgully, EVertiq) describe Yulu as \"Bengaluru-based\"; "
             "founded 2017 by Amit Gupta, RK Misra, Naveen Dachuri, HQ in Bengaluru per Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Yulu_(transportation_company)",
)

yulu_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (yulu_id, "funding_round_closed", "FUNDRAISING",
     "Raised $93M Series C ($63M equity + $30M debt) led by GEF Capital Partners, valuing Yulu at "
     "~$170M post-money. Funds will quadruple the active EV fleet to 200,000 over two years, "
     "launch 'Yulu Express' for e-commerce parcel delivery, and prepare for a potential listing.",
     "2026-08-12", "2026-08-12", "FACT",
     "https://yourstory.com/2026/08/ev-mobility-service-startup-yulu-raises-93-million-led-by-gef-capital",
     "YourStory / Adgully / EVertiq",
     "\"Yulu secures US$93 million in new funding led by GEF Capital\", Aug 12 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, yulu_id, "FUNDRAISING", yulu_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, expansion_plan, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?,?)""",
    (yulu_id, "Series C", "$93 million ($63M equity + $30M debt)", "USD", "2026-08-12",
     "GEF Capital Partners (lead)",
     "Quadruple EV fleet to 200,000 over 2 years; launch Yulu Express (e-commerce parcel delivery)",
     "Preparing for a potential public listing per company statements",
     "https://worldautoforum.com/yulu-secures-us93-million-in-new-funding-led-by-gef-capital-drives-leadership-across-quick-delivery-and-urban-logistics/",
     "Values Yulu at ~$170M post-money"),
)
conn.commit()

yulu_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (yulu_id, "Amit Gupta", "Co-Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/Yulu_(transportation_company)"),
).lastrowid
conn.commit()

yulu_open_triggers = repo.open_trigger_count(conn, yulu_id)
yulu_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.55,
        "timing_urgency": 0.60,
        "business_standard_audience_fit": 0.75,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.80,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=yulu_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, yulu_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=yulu_open_triggers,
    score=yulu_result["score"],
    classification=yulu_result["classification"],
    timing="NEAR_TERM",
    why_now="Series C closed 11 days ago with an explicit potential-listing signal from the "
            "company -- the investor-visibility window is open while the round is still news.",
    why_this_company="Yulu, Bengaluru HQ verified. India's largest shared EV mobility platform, "
                      "founded by ex-InMobi co-founder Amit Gupta, now funding a 4x fleet expansion "
                      "and a new B2B delivery product line.",
    business_problem="Needs investor-facing credibility ahead of a reported potential listing, plus "
                      "market awareness for the new Yulu Express B2B product line.",
    why_business_standard="Pre-listing investor-visibility story plus a new B2B logistics product "
                           "launch -- both squarely BS's business-audience territory.",
    recommended_product="investor_visibility_content, branded_content",
    recommended_contact_id=yulu_contact_id,
    recommended_action="Pitch investor-visibility content tied to the Series C and the pre-listing "
                        "signal; confirm listing timeline independently before leading with it.",
    is_qualified_bangalore=yulu_result["is_qualified_bangalore"],
    score_breakdown=yulu_result["score_breakdown"],
)

# ---------------------------------------------------------------- River Mobility
river_id = repo.get_or_create_company(
    conn, "River Mobility", industry="Electric two-wheelers",
)
repo.set_hq_status(
    conn, river_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Multiple outlets (Business Standard, Autocar India, EVreporter) describe River "
             "Mobility as \"Bengaluru-based\"; founded 2021 by Aravind Mani and Vipin George.",
    source_url="https://www.business-standard.com/amp/companies/news/river-mobility-raises-120-million-in-series-c-led-by-elev8-claypond-126080501366_1.html",
)

river_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (river_id, "funding_round_closed", "FUNDRAISING",
     "Raised $120M Series C led by Elev8 Venture Partners and Claypond Capital (participation from "
     "Singularity AMC, Anicut Capital, 360 ONE Asset, JIF Capital, HDFC AMC, plus venture debt and "
     "existing strategic investors Yamaha Motor, Al Futtaim Group, Mitsui & Co). Funds a new "
     "greenfield manufacturing plant and new products in the 'utility lifestyle' segment; targeting "
     "350+ stores by 2028.",
     "2026-08-06", "2026-08-06", "FACT",
     "https://www.business-standard.com/amp/companies/news/river-mobility-raises-120-million-in-series-c-led-by-elev8-claypond-126080501366_1.html",
     "Business Standard / Autocar India / EVreporter",
     "\"River Mobility raises $120 million in Series C led by Elev8, Claypond\", Aug 6 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, river_id, "FUNDRAISING", river_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, expansion_plan, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?,?)""",
    (river_id, "Series C", "$120 million", "USD", "2026-08-06",
     "Elev8 Venture Partners, Claypond Capital (co-leads); Yamaha Motor, Al Futtaim Group, Mitsui & Co (existing)",
     "New greenfield manufacturing plant; new utility-lifestyle segment products",
     "Expand to 350+ stores by 2028",
     "https://evreporter.com/river-mobility-raises-120-million-in-series-c-funding/",
     "Oversubscribed round; strategic auto-industry investors (Yamaha, Al Futtaim, Mitsui) participated"),
)
conn.commit()

river_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (river_id, "Aravind Mani", "Co-Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "MEDIUM",
     "https://startupstorymedia.com/river-mobility-raises-120-million-in-series-c-to-power-its-next-phase-of-growth/"),
).lastrowid
conn.commit()

river_open_triggers = repo.open_trigger_count(conn, river_id)
river_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.55,
        "timing_urgency": 0.50,
        "business_standard_audience_fit": 0.75,
        "estimated_marketing_capacity": 0.60,
        "decision_maker_availability": 0.75,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=river_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, river_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=river_open_triggers,
    score=river_result["score"],
    classification=river_result["classification"],
    timing="NEAR_TERM",
    why_now="Series C closed 17 days ago; still within the post-raise visibility window, with a "
            "concrete expansion plan (new plant, 350+ stores by 2028) to hang a pitch on.",
    why_this_company="River Mobility, Bengaluru HQ verified. Oversubscribed $120M round with "
                      "marquee strategic investors (Yamaha, Al Futtaim, Mitsui) backing a "
                      "manufacturing and retail expansion.",
    business_problem="Needs business-audience visibility for a capital-intensive manufacturing "
                      "expansion story, distinct from a typical consumer-EV pitch.",
    why_business_standard="Strategic-investor-backed manufacturing expansion is a core BS "
                           "business-audience story (capacity, capital allocation, industrial "
                           "strategy), not a mass-consumer ad play.",
    recommended_product="corporate_communication, business_audience_display",
    recommended_contact_id=river_contact_id,
    recommended_action="Pitch business-audience content around the manufacturing expansion and "
                        "strategic-investor roster; timing is moderate, not urgent -- round is "
                        "2.5 weeks old.",
    is_qualified_bangalore=river_result["is_qualified_bangalore"],
    score_breakdown=river_result["score_breakdown"],
)

conn.close()
print("Ather Energy:", ather_result)
print("Yulu:", yulu_result)
print("River Mobility:", river_result)

print()
print("Competitor-advertising sweep (Sections 9-10): checked all 8 publishers in "
      "config/publishers.yaml (Economic Times, Times of India, Moneycontrol, Mint, CNBC-TV18, "
      "Financial Express, BusinessLine, Deccan Herald) for paid placements by the 10 tracked "
      "Bangalore-HQ companies. Found general marketing-spend disclosures (e.g. PhonePe Rs 455 Cr "
      "H1 FY26, Meesho Rs 227 Cr Q1 FY26 digital ad spend) but NO dated, sourced evidence of a "
      "specific placement on any of the 8 named publishers for any tracked company. Genuine null "
      "result for this pass -- not inserted into campaigns/competitor_activity as no verifiable "
      "record exists to cite. Open web search does not reliably surface publisher-level ad "
      "placements; a real check would need the publishers' own media-sales records or an ad "
      "intelligence tool (e.g. Pathmatics/MediaRadar), neither of which is available in this "
      "environment.")
