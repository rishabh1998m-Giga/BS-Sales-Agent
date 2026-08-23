#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-23 daily-sales-brief run.
Records today's verified research findings into database/sales.db using the
existing repo.py/scorer.py helpers. Not part of the permanent pipeline code
(there is no orchestrating skill in this repo to call this automatically) —
kept here as a record of exactly what this run inserted and why.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# ---------------------------------------------------------------- CRED update
cred_id = repo.get_or_create_company(conn, "CRED")

event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (cred_id, "app_launch", "PRODUCT_LAUNCH",
     "CRED launched Circle, a members-only app for paid one-to-one advice from vetted "
     "'Residents' on careers, money, wellness and relationships (Rs 25/min, beta).",
     "2026-08-18", "2026-08-18", "FACT",
     "https://www.business-standard.com/companies/news/cred-rolls-out-circle-platform-to-connect-users-with-vetted-domain-experts-126081801226_1.html",
     "Business Standard",
     "\"Cred rolls out Circle platform to connect users with vetted domain experts\" - beta live Aug 18, 2026, 100+ Residents, Rs 25/min",
     "HIGH"),
).lastrowid
conn.commit()

repo.open_trigger(conn, cred_id, "PRODUCT_LAUNCH", event_id)

conn.execute(
    """INSERT INTO product_launches
       (company_id, brand, product_name, launch_date, target_audience, marketing_activity, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?)""",
    (cred_id, "CRED", "Circle by CRED", "2026-08-18",
     "CRED's ~1.7 crore affluent-member base",
     "Beta rollout via app + PR; waitlist for non-selected members",
     "https://entrackr.com/snippets/cred-launches-circle-app-to-connect-members-with-experienced-peers-12395718",
     "Beta live Aug 18, 100+ Residents offering paid 1:1 advice"),
)
conn.commit()

conn.execute(
    """INSERT INTO leadership_changes
       (company_id, person_name, title, appointment_date, relevance, confidence, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?)""",
    (cred_id, "Miten Sampat", "Interim CEO", "2026-06-22",
     "Resolves the open follow-up from the 2026-08-21 brief (\"who runs CRED day-to-day\") "
     "after Kunal Shah moved to lead WhatsApp globally.",
     "HIGH",
     "https://www.business-standard.com/companies/news/cred-rolls-out-circle-platform-to-connect-users-with-vetted-domain-experts-126081801226_1.html",
     "Quoted as \"Miten Sampat, interim chief executive officer (CEO), CRED\" on the Circle launch, Aug 18 2026"),
)
conn.commit()

cred_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (cred_id, "Miten Sampat", "Interim CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://www.business-standard.com/companies/news/cred-rolls-out-circle-platform-to-connect-users-with-vetted-domain-experts-126081801226_1.html"),
).lastrowid
conn.commit()

cred_open_triggers = repo.open_trigger_count(conn, cred_id)  # Meta/leadership (Jun 22) + Circle launch (Aug 18)
cred_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.50,
        "timing_urgency": 0.85,
        "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.85,
        "decision_maker_availability": 0.90,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=cred_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, cred_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="PRODUCT_LAUNCH",
    trigger_count=cred_open_triggers,
    score=cred_result["score"],
    classification=cred_result["classification"],
    timing="IMMEDIATE",
    why_now="Circle beta went live 5 days ago and is still in its awareness/waitlist-expansion window; "
            "it also gives BS a confirmed interim-CEO contact where the prior brief had none.",
    why_this_company="CRED, Bengaluru HQ verified. Well-funded (Meta $900M, Jun 2026), proven marketing "
                      "spender, now diversifying revenue into paid advisory for its affluent member base.",
    business_problem="Needs to build awareness and trust for a brand-new paid product among a skeptical, "
                      "already-affluent user base, while reassuring the market post-founder-transition.",
    why_business_standard="BS's business/investor-decision-maker audience overlaps directly with the "
                           "'affluent Indians' Circle is targeting, and with the corporate-narrative "
                           "audience needed post-leadership-transition.",
    recommended_product="branded_content, thought_leadership, corporate_communication",
    recommended_contact_id=cred_contact_id,
    recommended_action="Pitch Circle launch coverage + a leadership Q&A with Miten Sampat "
                        "(now confirmed as interim CEO) before the beta window closes.",
    is_qualified_bangalore=cred_result["is_qualified_bangalore"],
    score_breakdown=cred_result["score_breakdown"],
)

# ---------------------------------------------------------- Navi Technologies
navi_id = repo.get_or_create_company(
    conn, "Navi Technologies", industry="Fintech", website="https://navi.com",
)
repo.set_hq_status(
    conn, navi_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Registered office: 9th floor, Vaishnavi Tech Square, HSR Layout, Bengaluru 560102 "
             "(CIN U72900KA2018PLC119297, ROC Bangalore)",
    source_url="https://www.zaubacorp.com/NAVI-TECHNOLOGIES-LIMITED-U72900KA2018PLC119297",
)

fund_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (navi_id, "strategic_investment", "FUNDRAISING",
     "Navi raised $100M from Prosus (via MIH Payments Holdings BV) in its first-ever institutional "
     "funding round, valuing Navi at ~$1.3B; deal subject to CCI approval.",
     "2026-08-19", "2026-08-19", "FACT",
     "https://www.business-standard.com/companies/start-ups/sachin-bansal-led-navi-raises-100-mn-from-prosus-in-maiden-funding-round-126081901515_1.html",
     "Business Standard / TechCrunch",
     "\"Sachin Bansal-led Navi raises $100 mn from Prosus in maiden funding round\", Aug 19 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, navi_id, "FUNDRAISING", fund_event_id)

ipo_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (navi_id, "ipo_reported", "IPO",
     "Reported to be preparing a fresh listing attempt, seeking to raise roughly $300M; no DRHP "
     "confirmed in this pass.",
     None, "2026-08-19", "INFERENCE",
     "https://techcrunch.com/2026/08/19/sachin-bansals-fintech-navi-raises-first-outside-capital-with-100m-prosus-investment/",
     "TechCrunch",
     "\"the Bengaluru-based fintech is preparing to list on the Indian stock exchanges, reportedly "
     "seeking to raise about $300 million\" - reported alongside the Prosus round, not independently confirmed",
     "MEDIUM"),
).lastrowid
conn.commit()
repo.open_trigger(conn, navi_id, "IPO", ipo_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (navi_id, "Strategic/Growth", "$100 million", "USD", "2026-08-19", "Prosus (MIH Payments Holdings BV)",
     "First outside institutional capital; company already preparing for a market listing",
     "https://techcrunch.com/2026/08/19/sachin-bansals-fintech-navi-raises-first-outside-capital-with-100m-prosus-investment/",
     "Values Navi at ~$1.3B; subject to CCI approval"),
)
conn.commit()

navi_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (navi_id, "Sachin Bansal", "Founder & Group CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/Navi_Group"),
).lastrowid
conn.commit()

navi_open_triggers = repo.open_trigger_count(conn, navi_id)
navi_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.50,
        "timing_urgency": 0.80,
        "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.60,
        "decision_maker_availability": 0.80,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=navi_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, navi_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=navi_open_triggers,
    score=navi_result["score"],
    classification=navi_result["classification"],
    timing="IMMEDIATE",
    why_now="First-ever outside institutional round closed 4 days ago, announced alongside a reported "
            "(unconfirmed) pre-listing plan - the validation/visibility window is open now.",
    why_this_company="Navi, Bengaluru HQ verified (CIN U72900KA2018PLC119297). Sachin Bansal-founded "
                      "fintech now taking outside capital for the first time in its history.",
    business_problem="Needs to build investor and public confidence ahead of a reported listing attempt, "
                      "especially given the company's 2022 IPO attempt was previously withdrawn.",
    why_business_standard="Direct fit for BS's investor/business-decision-maker readership during a "
                           "pre-listing, first-institutional-round credibility moment.",
    recommended_product="investor_visibility_content, branded_content, corporate_communication",
    recommended_contact_id=navi_contact_id,
    recommended_action="Pitch investor-visibility content tied to the Prosus round; confirm the IPO "
                        "timeline independently before leading with it (currently INFERENCE-tier only).",
    is_qualified_bangalore=navi_result["is_qualified_bangalore"],
    score_breakdown=navi_result["score_breakdown"],
)

# --------------------------------------------------- Table Space Technologies
tablespace_id = repo.get_or_create_company(
    conn, "Table Space Technologies", industry="Managed workspace / commercial real estate",
)
repo.set_hq_status(
    conn, tablespace_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Multiple outlets describe Table Space as \"Bengaluru-headquartered\" managed workspace "
             "solutions provider to GCCs, Fortune 500s and MNCs.",
    source_url="https://www.businesstoday.in/markets/ipo-corner/story/tablespace-technologies-files-drhp-with-sebi-to-launch-its-ipo-check-details-548484-2026-08-11",
)

ts_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (tablespace_id, "drhp_filed", "IPO",
     "Filed DRHP with SEBI: fresh issue of up to Rs 800 crore plus an OFS of up to 6.55 crore equity "
     "shares. FY26 normalised revenue Rs 24,776.83 million, up 56.42% YoY.",
     "2026-08-11", "2026-08-11", "FACT",
     "https://www.freepressjournal.in/business/table-space-technologies-files-drhp-with-sebi-for-800-crore-ipo-plans-ofs-of-up-to-655-crore-shares",
     "Free Press Journal / Business Today",
     "\"Table Space Technologies Files DRHP With Sebi For Rs800-Crore IPO\", Aug 11 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, tablespace_id, "IPO", ts_event_id)

conn.execute(
    """INSERT INTO ipo_events
       (company_id, ipo_status, stage, ipo_size, source_url, evidence)
       VALUES (?,?,?,?,?,?)""",
    (tablespace_id, "IPO_REPORTED", "DRHP filed", "Rs 800 Cr fresh issue + OFS up to 6.55 Cr shares",
     "https://www.businesstoday.in/markets/ipo-corner/story/tablespace-technologies-files-drhp-with-sebi-to-launch-its-ipo-check-details-548484-2026-08-11",
     "DRHP filed Aug 11 2026; no listing date yet"),
)
conn.commit()

ts_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (tablespace_id, "Karan Chopra", "Founder & Co-CEO", "OFFICIAL_EMAIL_NOT_FOUND", "MEDIUM",
     "https://tracxn.com/d/companies/table-space/__u3ZDXVQ6kqGVyKfLnn75jsPuoBmEkQmXYZgvFDKv-bM"),
).lastrowid
conn.commit()

ts_open_triggers = repo.open_trigger_count(conn, tablespace_id)
ts_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.90,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.75,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.75,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=ts_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, tablespace_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="IPO",
    trigger_count=ts_open_triggers,
    score=ts_result["score"],
    classification=ts_result["classification"],
    timing="NEAR_TERM",
    why_now="DRHP filed 12 days ago (Aug 11); pre-listing quiet-to-loud window is open, no listing "
            "date fixed yet.",
    why_this_company="Table Space, Bengaluru HQ. Managed-workspace provider to GCCs/Fortune 500s filing "
                      "for an Rs 800 Cr IPO with strong revenue growth (+56% YoY).",
    business_problem="A B2B/enterprise-facing brand with limited consumer visibility needs credibility "
                      "with investors and the business audience ahead of listing.",
    why_business_standard="Textbook BS fit: a B2B real-estate/workspace company serving Fortune 500s and "
                           "GCCs, pre-IPO, needs exactly the investor/business-decision-maker reach BS "
                           "offers - arguably the strongest audience match of today's three opportunities.",
    recommended_product="corporate_communication, thought_leadership, premium_display",
    recommended_contact_id=ts_contact_id,
    recommended_action="Pitch pre-IPO corporate-communication package to Co-CEO Karan Chopra; a CMO "
                        "name (Megha Agarwal, per one directory listing) surfaced but is unverified - "
                        "confirm the current marketing lead before including them in outreach.",
    is_qualified_bangalore=ts_result["is_qualified_bangalore"],
    score_breakdown=ts_result["score_breakdown"],
)

conn.close()
print("CRED:", cred_result)
print("Navi:", navi_result)
print("Table Space:", ts_result)
