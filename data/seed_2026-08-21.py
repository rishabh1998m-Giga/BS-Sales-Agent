#!/usr/bin/env python3
"""
First real research pass — 2026-08-21. Populates database/sales.db with
verified findings from live web research (see chat for full source list).
This is a one-off seed script documenting today's manual daily-sales-brief
run; future runs should go through the daily-sales-brief skill pipeline
rather than a hand-written script like this one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from db.repo import connect, get_or_create_company, set_hq_status, open_trigger, open_trigger_count, insert_opportunity  # noqa: E402
from scoring.scorer import score_opportunity, classify_timing  # noqa: E402

conn = connect()


def add_company(name, industry, website=None):
    return get_or_create_company(conn, name, industry=industry, website=website)


# ---------------------------------------------------------------- PhonePe
phonepe_id = add_company("PhonePe", "Fintech / Digital Payments", "phonepe.com")
set_hq_status(
    conn, phonepe_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru",
    hq_city="Bengaluru",
    evidence="CIN U67190KA2012PTC176031 (KA = Karnataka registration); "
             "described as 'a Bengaluru-based digital payments and fintech company founded in 2015'",
    source_url="https://www.zaubacorp.com/PHONEPE-PRIVATE-LIMITED-U67190KA2012PTC176031",
)
conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'ipo_reported', 'IPO', ?, NULL, '2026-08-01', 'FACT', ?, ?, ?, ?, ?, ?, 'HIGH')""",
    (phonepe_id,
     "PhonePe filed an updated DRHP with SEBI following regulatory approval; entirely an "
     "offer-for-sale (~$1.3B / ~Rs 12,000 Cr) benefiting existing shareholders (Walmart, Tiger "
     "Global, Microsoft exiting); no listing date announced yet.",
     "Major fintech IPO in progress; heightened investor and media scrutiny during the pre-listing window.",
     "Strong need for corporate credibility content aimed at investors/business audience ahead of listing.",
     "Pre-IPO corporate visibility, thought leadership, investor-audience content.",
     "https://groww.in/blog/phonepe-files-updated-drhp-with-sebi",
     "Groww Blog / IPO Central",
     "'PhonePe Files Updated DRHP with SEBI, Plans to Raise $1.3 billion through OFS'"),
)
phonepe_ipo_event = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
conn.execute(
    """INSERT INTO ipo_events (company_id, ipo_status, stage, expected_timeline, ipo_size,
        lead_managers, drhp_status, industry, source_url, evidence, bs_pitch_notes)
       VALUES (?, 'IPO_REPORTED', 'SEBI approved, updated DRHP filed', 'Not yet announced',
        '~$1.3B / Rs 12,000 Cr (OFS only)', 'Kotak Mahindra Capital, JPMorgan Chase, Citigroup, Morgan Stanley',
        'Updated DRHP filed post-approval', 'Fintech / Digital Payments',
        'https://ipocentral.in/phonepe-ipo-news/',
        'OFS only — company receives no proceeds; existing investors (Walmart, Tiger Global, Microsoft) selling down',
        'Pre-IPO corporate storytelling + investor-audience premium display; time-sensitive while listing news cycle is live')""",
    (phonepe_id,),
)
conn.commit()
open_trigger(conn, phonepe_id, "IPO", phonepe_ipo_event)

conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'brand_campaign', 'MARKETING_CAMPAIGN', ?, '2026-03-12', '2026-03-12', 'FACT', ?, ?, ?, ?, ?, ?, 'HIGH')""",
    (phonepe_id,
     "PhonePe Wealth launched 'Mutual Funds bhi, ab PhonePe' — a 10-week, 7-language, "
     "360-degree campaign (TV, Hotstar, YouTube, Meta, Cricket World Cup visibility) promoting "
     "its CRISP fund-selection methodology and Daily SIP feature.",
     "Confirms PhonePe has an active, well-funded, multi-channel marketing operation and agency relationships.",
     "Demonstrates real ad budget deployment capacity across formats BS could compete for.",
     "Evidence of marketing capacity for scoring; campaign itself is now >90 days old so not counted "
     "as an open trigger, but supports the estimated_marketing_capacity score.",
     "https://www.adgully.com/post/13050/phonepe-wealth-launches-campaign-promoting-simplified-mutual-fund-investing",
     "Adgully", "'Mutual Funds bhi, ab PhonePe' — 360-degree amplification over 10 weeks"),
)
conn.commit()

# ------------------------------------------------------------------- CRED
cred_id = add_company("CRED", "Fintech / Credit Card Rewards", "cred.club")
set_hq_status(
    conn, cred_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru",
    hq_city="Bengaluru",
    evidence="'CRED's main office and corporate headquarters is located at 100 Feet Road, "
             "12th Main Road, HAL 2nd Stage, in Bengaluru, 560038, India.'",
    source_url="https://www.clay.com/dossier/cred-headquarters-office-locations",
)
conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'strategic_investment', 'MAJOR_PARTNERSHIP', ?, '2026-06-22', '2026-06-22', 'FACT', ?, ?, ?, ?, ?, ?, 'HIGH')""",
    (cred_id,
     "Meta invested $900M in CRED (valuing it near $4B) and named CRED founder Kunal Shah as "
     "global head of WhatsApp; Shah is stepping back from CRED's day-to-day leadership.",
     "Major strategic capital infusion plus an unusual, high-profile founder transition — CRED "
     "will need to manage a public narrative about leadership continuity and its next chapter.",
     "Strong likely need for corporate storytelling / leadership-transition communication and "
     "renewed brand-credibility content independent of the founder's public profile.",
     "Corporate storytelling, thought leadership (new leadership team), corporate communication.",
     "https://techcrunch.com/2026/06/22/whatsapp-gets-new-chief-as-meta-taps-indias-cred-founder-kunal-shah-and-invests-900m-in-startup/",
     "TechCrunch / Bloomberg / Business Standard",
     "'Meta taps India's CRED founder Kunal Shah and invests $900M in startup'"),
)
cred_event_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
conn.execute(
    """INSERT INTO funding_events (company_id, stage, amount, date_announced, investors, purpose,
        marketing_implication, source_url, evidence)
       VALUES (?, 'Strategic investment', '$900M (~Rs 7,500 Cr)', '2026-06-22', 'Meta',
        'Strategic partnership; founder transition to lead WhatsApp globally',
        'Company will likely need a leadership-transition and forward-narrative campaign; who now runs CRED day-to-day was not confirmed in sources found -- worth a follow-up check.',
        'https://www.bloomberg.com/news/articles/2026-06-22/meta-taps-new-whatsapp-boss-as-part-of-900-million-investment',
        'Meta Invests $900 Million in Cred, Taps Founder to Head WhatsApp')""",
    (cred_id,),
)
conn.commit()
open_trigger(conn, cred_id, "MAJOR_PARTNERSHIP", cred_event_id)
open_trigger(conn, cred_id, "FUNDRAISING", cred_event_id)

# ----------------------------------------------------------------- Rapido
rapido_id = add_company("Rapido", "Mobility / Ride-hailing", "rapido.bike")
set_hq_status(
    conn, rapido_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru",
    hq_city="Bengaluru",
    evidence="Corporate office: Salarpuria Softzone Tech Park, Bellandur, Bengaluru, Karnataka "
             "560103; registered as RAPIDO TRAVELS INDIA PRIVATE LIMITED, CIN U63030KA2017PTC100500",
    source_url="https://www.zaubacorp.com/RAPIDO-TRAVELS-INDIA-PRIVATE-LIMITED-U63030KA2017PTC100500",
)
conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'funding_round_closed', 'FUNDRAISING', ?, '2026-05-15', '2026-05-15', 'FACT', ?, ?, ?, ?, ?, ?, 'HIGH')""",
    (rapido_id,
     "Rapido raised $240M from Prosus at a $3B valuation, expanding beyond ride-hailing "
     "(multimodal expansion).",
     "Major growth-capital raise for continued category expansion (per TechCrunch, positions "
     "Rapido as a broader 'Uber rival' beyond bikes).",
     "Growth capital often precedes visibility/awareness pushes tied to new service categories.",
     "Investor-visibility content, business-audience display around category expansion.",
     "https://techcrunch.com/2026/05/15/indian-uber-rival-rapido-raises-240m-at-3b-valuation/",
     "TechCrunch", "'Indian Uber rival Rapido raises $240M at $3B valuation'"),
)
rapido_event_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
conn.execute(
    """INSERT INTO funding_events (company_id, stage, amount, date_announced, investors, purpose,
        expansion_plan, marketing_implication, source_url, evidence)
       VALUES (?, 'Growth capital', '$240M', '2026-05-15', 'Prosus',
        'Multimodal expansion beyond bike-taxi/ride-hailing', 'Expansion into new mobility categories',
        'Likely awareness campaign as new service lines launch; INFERENCE, not yet confirmed by a company statement.',
        ?, ?)""",
    (rapido_id, "https://techcrunch.com/2026/05/15/indian-uber-rival-rapido-raises-240m-at-3b-valuation/",
     "'Indian Uber rival Rapido raises $240M at $3B valuation'"),
)
conn.commit()
open_trigger(conn, rapido_id, "FUNDRAISING", rapido_event_id)

# ------------------------------------------------------------------ Groww
groww_id = add_company("Groww (Billionbrains Garage Ventures)", "Fintech / Broking & Wealth", "groww.in")
set_hq_status(
    conn, groww_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru",
    hq_city="Bengaluru",
    evidence="'Billionbrains Garage Ventures (Groww's parent company) is Bengaluru-headquartered.'",
    source_url="https://groww.in/blog/groww-makes-a-blockbuster-debut",
)
conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'ipo_confirmed', 'IPO', ?, '2025-11-12', '2025-11-12', 'FACT', ?, ?, ?, ?, ?, ?, 'HIGH')""",
    (groww_id,
     "Already listed (Nov 12, 2025, Rs 6,632 Cr IPO, 14% premium debut on BSE); stock has since "
     "traded up to 80% above issue price with strong Q3 (Jan 2026) results and a Rs 580 Cr State "
     "Street investment into its AMC arm.",
     "Post-IPO public company with an active growth narrative — not a fresh trigger today, but a "
     "known, credible, well-capitalized account.",
     "Post-listing investor communication and corporate storytelling opportunities recur with "
     "each quarterly result.",
     "Lower priority today (event >90 days old) — track for next quarterly-results cycle.",
     "https://www.business-standard.com/markets/news/groww-stock-price-soars-9-on-huge-volumes-analysts-expect-more-upside-126011600507_1.html",
     "Business Standard", "Groww Q3 results + State Street AMC stake, Jan 16 2026 coverage"),
)
groww_event_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
conn.execute(
    """INSERT INTO ipo_events (company_id, ipo_status, stage, expected_listing, ipo_size,
        industry, source_url, evidence, bs_pitch_notes)
       VALUES (?, 'IPO_CONFIRMED', 'Listed', '2025-11-12 (already listed)', 'Rs 6,632.3 Cr',
        'Fintech / Broking', 'https://groww.in/blog/groww-makes-a-blockbuster-debut',
        'Listed on both BSE and NSE, 14% premium debut', 'Post-IPO quarterly-results storytelling opportunity — WATCH for next results date')""",
    (groww_id,),
)
conn.commit()

# ----------------------------------------------------------------- Meesho
meesho_id = add_company("Meesho", "E-commerce / Social Commerce", "meesho.com")
set_hq_status(
    conn, meesho_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru",
    hq_city="Bengaluru",
    evidence="Wikipedia infobox: 'Headquarters: Bengaluru, Karnataka, India'",
    source_url="https://en.wikipedia.org/wiki/Meesho",
)
conn.execute(
    """INSERT INTO business_events (company_id, event_type, event_category, description,
        event_date, announcement_date, fact_or_inference, business_impact, marketing_impact,
        advertising_opportunity, source_url, source_name, evidence, confidence)
       VALUES (?, 'ipo_confirmed', 'IPO', ?, '2025-12-01', '2025-12-01', 'FACT', ?, ?, ?, ?, ?, ?, 'MEDIUM')""",
    (meesho_id,
     "Completed IPO in December 2025, raising $603M, listed on both BSE and NSE. FY25 revenue "
     "Rs 9,389 Cr, net loss Rs 3,941 Cr, 190M users.",
     "Now a listed public company; event itself is stale (>90 days) as a fresh trigger.",
     "Post-listing investor-audience visibility opportunities recur with quarterly results.",
     "Lower priority today — track for next quarterly-results cycle rather than pitching on the IPO itself.",
     "https://en.wikipedia.org/wiki/Meesho", "Wikipedia (company overview)",
     "'Meesho completed its initial public offering in December 2025, raising $603 million'"),
)
conn.commit()

# --------------------------------------------------------- scoring pass
def do_score(company_id, sub_scores, days_to_event, primary_trigger, why_now, why_company,
             biz_problem, why_bs, product, action):
    hq = conn.execute(
        "SELECT hq_status FROM company_hq WHERE company_id = ? ORDER BY verified_at DESC LIMIT 1",
        (company_id,),
    ).fetchone()["hq_status"]
    trig_count = open_trigger_count(conn, company_id)
    result = score_opportunity(sub_scores, hq_status=hq, open_trigger_count=max(trig_count, 1))
    timing = classify_timing(days_to_event)
    insert_opportunity(
        conn, company_id,
        hq_status=hq,
        primary_trigger=primary_trigger,
        trigger_count=max(trig_count, 1),
        score=result["score"],
        classification=result["classification"],
        timing=timing,
        why_now=why_now,
        why_this_company=why_company,
        business_problem=biz_problem,
        why_business_standard=why_bs,
        recommended_product=product,
        recommended_action=action,
        is_qualified_bangalore=result["is_qualified_bangalore"],
        score_breakdown=result["score_breakdown"],
    )
    return result


do_score(
    phonepe_id,
    sub_scores={
        "business_event_strength": 0.95, "advertising_marketing_signal": 0.7,
        "timing_urgency": 0.6, "business_standard_audience_fit": 0.95,
        "estimated_marketing_capacity": 0.9, "decision_maker_availability": 0.3,
        "official_contact_availability": 0.1, "strategic_relevance": 0.9,
    },
    days_to_event=45, primary_trigger="IPO",
    why_now="PhonePe's IPO is actively in motion — updated DRHP filed post-SEBI-approval, media "
            "and investor attention is elevated right now, and no listing date has been fixed yet, "
            "meaning the pre-listing visibility window is still open.",
    why_company="A ~$15B fintech going public via an all-OFS structure has a specific narrative "
                "need: convincing the market of durable value beyond the selling shareholders' exit, "
                "distinct from a routine fundraise pitch.",
    biz_problem="Building investor and business-audience confidence ahead of listing, independent "
                "of the underlying OFS mechanics.",
    why_bs="Business Standard's core audience (investors, business decision-makers) is exactly who "
           "PhonePe needs to reach during the pre-IPO quiet-to-loud period.",
    product="corporate_communication, premium_display, thought_leadership",
    action="Pitch pre-IPO corporate visibility package; time outreach to the DRHP news cycle rather "
           "than waiting for a listing date announcement — CONFIRM decision-maker contact first.",
)

do_score(
    cred_id,
    sub_scores={
        "business_event_strength": 1.0, "advertising_marketing_signal": 0.4,
        "timing_urgency": 0.5, "business_standard_audience_fit": 0.85,
        "estimated_marketing_capacity": 0.85, "decision_maker_availability": 0.2,
        "official_contact_availability": 0.1, "strategic_relevance": 0.8,
    },
    days_to_event=60, primary_trigger="MAJOR_PARTNERSHIP",
    why_now="A $900M Meta investment plus its founder's very public move to lead WhatsApp globally "
            "is an unusual, high-visibility event CRED will need to actively narrate — who leads "
            "next, and why the business is stronger, not weaker, without its founder day-to-day.",
    why_company="Few companies face a public founder-transition story at this scale; the "
                "communication need is specific and time-bound, not generic brand marketing.",
    biz_problem="Managing a leadership-transition narrative and reinforcing institutional (not "
                "founder-dependent) credibility with a business/investor audience.",
    why_bs="This is a corporate-credibility story, squarely BS's audience — not a mass-consumer "
           "brand campaign that would suit a general news outlet better.",
    product="corporate_storytelling, thought_leadership, corporate_communication",
    action="Research who now runs CRED day-to-day (not confirmed in this pass) before pitching — "
           "that person is the right contact, not Kunal Shah.",
)

do_score(
    rapido_id,
    sub_scores={
        "business_event_strength": 0.7, "advertising_marketing_signal": 0.4,
        "timing_urgency": 0.3, "business_standard_audience_fit": 0.6,
        "estimated_marketing_capacity": 0.7, "decision_maker_availability": 0.2,
        "official_contact_availability": 0.1, "strategic_relevance": 0.5,
    },
    days_to_event=95, primary_trigger="FUNDRAISING",
    why_now="A $240M raise at a $3B valuation for multimodal expansion is real growth capital, "
            "though the announcement is now ~3 months old, so urgency is moderate rather than high.",
    why_company="Category expansion beyond bike-taxi typically requires new-category awareness "
                "campaigns as new services launch.",
    biz_problem="Building awareness for expanded service categories funded by this round.",
    why_bs="Business-audience visibility around funding/expansion milestones fits BS's readership; "
           "weaker fit than PhonePe/CRED since Rapido's core product is consumer-mobility, not "
           "inherently a BS-reader-facing story.",
    product="investor_visibility_content, business_audience_display",
    action="Lower priority than PhonePe/CRED today; watch for a category-expansion product "
           "announcement, which would refresh the trigger and timing.",
)

print("Seed complete.")
for row in conn.execute(
    "SELECT c.name, o.score, o.classification, o.timing, o.is_qualified_bangalore FROM opportunities o "
    "JOIN companies c ON c.company_id = o.company_id ORDER BY o.score DESC"
):
    print(dict(row))

conn.close()
