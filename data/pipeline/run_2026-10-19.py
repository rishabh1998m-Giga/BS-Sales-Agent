#!/usr/bin/env python3
"""
Catch-up/resumption run for the 2026-10-19 daily-sales-brief
(self-bound 1:30 AM IST trigger).

OPERATIONAL GAP NOTE: this session went idle after the 2026-09-13
brief. The self-bound trigger kept firing nightly, but the resulting
notifications queued up unprocessed until this session was re-engaged
(user message "Continue from where you left off" on 2026-10-18/19).
16 nightly firings (2026-09-14 through 2026-10-18) were never acted on
-- no research, no commits, no reports, no deliveries for that window.

Rather than fabricate 16 individual retroactive "daily" reports from
news that is now 1-5 weeks stale (and of near-zero sales-outreach value
today), this script treats the gap honestly: it is called out directly
to the user in the delivery message for today's brief (not shoehorned
into the Section 15 Risk Flags mechanism, which is schema-bound to
company-specific risk signals, not pipeline-operational issues), and
this single run resumes the pipeline from today's actual news cycle
rather than inventing a backfill. The watchlist/pipeline DB is
otherwise untouched for the gap period -- no data was fabricated to
paper over the missed window.

New finding: Scimplify (Bengaluru; legal entity CoCreate Global
Technologies Pvt Ltd) -- an AI-led specialty-chemicals/advanced-
materials platform helping manufacturers reduce reliance on Chinese
chemical inputs -- raised a $25M strategic round on Oct 17 2026, led
by Hitachi Ventures (Hitachi Group's corporate VC arm), with Henkel
and Teknor Apex joining as new investors alongside existing backers
Accel India, Bertelsmann India Investments, Omnivore, and 3one4
Capital. Takes total equity funding to ~$80M; round earmarked partly
for US expansion. Deep-tech/advanced-materials B2B platform --
qualifies regardless of ticket size.

Checked and declined:
  - Spill Games (Bengaluru, $10.5M Series A led by Elevation Capital,
    Oct 2026) -- mobile gaming studio; mobile games are a routine,
    freemium/low-ticket mass-market B2C category, not a considered/
    higher-ticket purchase -- same reasoning as excluding Kuku FM/
    Pocket FM/Swish. Not scored on brand-fit grounds.
  - RapidCanvas ($29M Series B, Vertex Ventures SEA & India lead,
    Hitachi Ventures participating, Oct 15 2026) -- HQ is Austin,
    Texas; no India entity or India-city claim found, so the
    international-company rule (India HQ in a qualified city) doesn't
    apply either.
  - Cosmochute ($1.5M pre-seed led by Prosus Ventures, space robotics,
    Oct 2026) -- HQ is Ahmedabad, not a qualified city.
  - C-CAMP (Bengaluru) selected as one of five Focused Research
    Organisations under the Centre's Rs 500 Cr RDI Fund allocation
    (Oct 16-17 2026) -- real and HQ'd in a qualified city, but C-CAMP
    is a government-backed biotech research consortium, not a
    commercial advertiser/brand -- not a conventional ad-sales
    prospect in the sense this pipeline tracks (same category
    reasoning as excluding pure trade-body/chamber entities). Noted
    for awareness, not scored as a company opportunity.
  - WeWork India's 7 lakh sq ft Bengaluru/Hyderabad/Chennai leasing
    expansion -- previously declined (Mumbai/Bengaluru co-HQ
    ambiguity, flexible-workspace B2B2C category); resurfaced in this
    search with no new qualifying detail, not re-scored.

Also checked: Chittorgarh (current mainboard pipeline -- Tonbo
Imaging, HD Fire Protect, Zetwerk Manufacturing, Bonfiglioli
Transmissions, Sahajanand Medical Technologies, Fusion CX, Jio
Platforms, Paras Healthcare -- no new qualified-city company beyond
what would need dedicated follow-up later), industry movement via
afaqs!/Storyboard18 (no qualifying brand-agency mandate found for the
three qualified cities in this pass).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

scimplify_id = repo.get_or_create_company(conn, "Scimplify", industry="AI-led specialty chemicals / advanced materials platform")
repo.set_hq_status(
    conn, scimplify_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Legal entity CoCreate Global Technologies Pvt Ltd (CIN U21009KA2023PTC179006, RoC-"
             "Bangalore, incorporated 22 Sep 2023, status Active). Registered-office street address "
             "varies slightly across aggregators (Zaubacorp: L73 15th Cross Rd, Sector 6, Bangalore "
             "South 560102; Instafinancials/Vakilsearch: HSR Layout 560102; Tracxn: Kodichikkanahalli/"
             "Bommanahalli 560068) but all agree on Bangalore South, Karnataka -- company itself "
             "described as Bengaluru-based with R&D facilities in Bengaluru and Hyderabad.",
    source_url="https://www.zaubacorp.com/COCREATE-GLOBAL-TECHNOLOGIES-PRIVATE-LIMITED-U21009KA2023PTC179006",
)
scimplify_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (scimplify_id, "strategic_investment", "FUNDRAISING",
     "Raised a $25M strategic round led by Hitachi Ventures (Hitachi Group's corporate VC arm), with "
     "Henkel and Teknor Apex joining as new investors and existing backers Accel India, Bertelsmann "
     "India Investments, Omnivore, and 3one4 Capital participating. Takes total equity funding to "
     "~$80M; capital earmarked partly for US expansion. Reported post-money valuation near $250M "
     "(unconfirmed by company).",
     "2026-10-17", "2026-10-17", "FACT",
     "https://entrackr.com/news/scimplify-raises-25-mn-in-strategic-round-led-by-hitachi-ventures-12676144",
     "Entrackr / Global Venturing / Indian Startup News",
     "\"Scimplify raises $25 Mn in strategic round led by Hitachi Ventures\" -- Oct 17 2026, "
     "corroborated across Entrackr, Global Venturing, Indian Startup News, JobsNHire",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, scimplify_id, "FUNDRAISING", scimplify_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (scimplify_id, "Strategic round", "$25 million", "USD", "2026-10-17",
     "Hitachi Ventures (lead), Henkel, Teknor Apex (new); Accel India, Bertelsmann India Investments, "
     "Omnivore, 3one4 Capital (existing)",
     "US expansion; scale AI-led specialty chemicals/advanced materials manufacturing platform",
     "https://entrackr.com/news/scimplify-raises-25-mn-in-strategic-round-led-by-hitachi-ventures-12676144",
     "Total funding to date ~$80M; deep-tech/advanced-materials B2B platform qualifies regardless of "
     "ticket size"),
)
conn.commit()

scimplify_open_triggers = repo.open_trigger_count(conn, scimplify_id)
scimplify_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.70,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.60,
        "business_standard_audience_fit": 0.65,
        "estimated_marketing_capacity": 0.60,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.55,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=scimplify_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, scimplify_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=scimplify_open_triggers,
    score=scimplify_result["score"],
    classification=scimplify_result["classification"],
    timing="IMMEDIATE",
    why_now="Strategic round closed 2 days ago with a marquee corporate investor (Hitachi Ventures) "
            "plus new strategics (Henkel, Teknor Apex) -- a strong, fresh industrial-credibility hook "
            "while the news is active.",
    why_this_company="Scimplify, Bangalore HQ verified. AI-led specialty-chemicals platform targeting "
                      "US expansion with marquee strategic backing.",
    business_problem="A deep-tech manufacturing platform expanding internationally after a strategic "
                      "raise needs business/investor-press visibility to build category credibility "
                      "with manufacturers and global partners.",
    why_business_standard="B2B deep-tech/advanced-materials funding with marquee strategic investors "
                           "and a US-expansion angle fits BS's business/industrial readership.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch thought-leadership content on reducing Indian manufacturers' reliance on "
                        "Chinese chemical inputs, tied to the Hitachi Ventures-led round; no marketing "
                        "contact confirmed in this pass.",
    is_qualified_target=scimplify_result["is_qualified_target"],
    score_breakdown=scimplify_result["score_breakdown"],
)

conn.close()
print("Scimplify:", scimplify_result)
