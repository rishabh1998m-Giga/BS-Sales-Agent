#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-20 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Even Healthcare (Bengaluru-based private hospital chain,
founded by CEO Mayank Banerjee) raised a $50M Series B on Oct 19 2026,
led by existing investor Khosla Ventures with Alpha Wave participating
-- triples the valuation from its raise 18 months ago (reports put
this round's valuation around $300M), takes total funding to over
$120M. Capital earmarked for five new Even hospitals across Bengaluru
over the next six months (company currently runs two, a third nearing
completion). Business model: doctors paid fixed salaries with bonuses
tied to patient-reported outcomes rather than procedure volume/revenue
-- a differentiated "value-based care" positioning. Hospital
care/surgery is inherently a considered, high-stakes purchase, not
routine/mass-market consumption -- clears the brand-fit gate easily,
regardless of B2C classification.

HQ note: two differently-registered "Even Healthcare Private Limited"
CINs exist -- U85300KA2020PTC207831 (ROC Bangalore, Indiranagar
address, status Active, confirmed via Tracxn/Instafinancials/Tofler/
Falcon Ebiz) and U85300MH2020PTC345050 (ROC Mumbai, Nagpur address,
per Zaubacorp). Falcon Ebiz identifies the Mumbai CIN as a superseded
"previous CIN" of the Bangalore entity. Treating Bangalore as current
or Bangalore CIN as authoritative: company's hospitals operate
exclusively in Bengaluru per the press's own description of the
funding's use (five new Bengaluru hospitals), consistent with the
Bangalore-registered CIN being the live one.

Checked and declined:
  - Boldfit (Bengaluru, Rs 400+ Cr Series B led by Bharat Value Fund/
    The Wealth Company Alternates, Oct 13 2026) -- Bengaluru HQ likely
    qualifies, but confirmed pricing (supplements Rs 299-2,559, apparel
    Rs 399-1,999) places it squarely budget-to-mid-market D2C fitness/
    activewear -- same reasoning as excluding Comet. Not scored on
    brand-fit grounds.
  - Fusion CX (BPO, IPO allotment today, listing Oct 22) -- registered
    AND corporate office is Salt Lake, Kolkata (CIN U72900WB2004PLC
    097921); US corporate HQ is Georgia -- neither is a qualified city.

Also checked: Chittorgarh (Tonbo Imaging IPO subscription update --
already a tracked opportunity, no new row for a subscription-status
update, same pattern as RentoMojo; Jio Platforms/Paras Healthcare/BLS
Polymers upcoming issues, none yet dated/qualified), industry movement
via afaqs!/Storyboard18 (RMAI FLAME Student Awards in Hyderabad --
an awards ceremony, not a brand-agency mandate story in scope for
Section 16; WeWork India leasing story resurfaced but is ~196 days
old, not fresh).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

even_id = repo.get_or_create_company(conn, "Even Healthcare", industry="Private hospital chain (value-based care)")
repo.set_hq_status(
    conn, even_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Even Healthcare Private Limited, 1335, 12th Cross Double Road, Binnamangla 2nd Stage, "
             "Indiranagar, Bangalore North, Karnataka 560038 (CIN U85300KA2020PTC207831, RoC-Bangalore, "
             "status Active). A differently-numbered CIN (U85300MH2020PTC345050, RoC-Mumbai, Nagpur "
             "address) is identified by Falcon Ebiz as a superseded previous CIN of this entity. "
             "Company's hospitals operate exclusively in Bengaluru (2 open, 1 nearing completion, 5 "
             "more funded by this round) -- registered AND operational HQ both Bangalore.",
    source_url="https://tracxn.com/d/legal-entities/india/even-healthcare-private-limited/__OalbfiJ9_RNrBZwiB0VXYtZPPyaqZ_SfjoJwvMbqhNk",
)
even_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (even_id, "funding_round", "FUNDRAISING",
     "Raised a $50M Series B led by existing investor Khosla Ventures, with Alpha Wave participating "
     "-- triples the company's valuation from its raise 18 months ago (reports put this round near "
     "$300M), taking total funding to over $120M. Capital earmarked for five new Even hospitals across "
     "Bengaluru over the next six months (currently operates 2, with a third nearing completion). "
     "Differentiated 'value-based care' model: doctors on fixed salaries with outcome-tied bonuses "
     "rather than procedure-volume incentives.",
     "2026-10-19", "2026-10-19", "FACT",
     "https://yourstory.com/2026/10/even-healthcare-raises-50m-in-series-b-round-led-by-khosla-ventures",
     "YourStory / Dealroom / BW Disrupt",
     "\"Even Healthcare raises $50M in Series B round led by Khosla Ventures\" -- Oct 19 2026, "
     "corroborated across YourStory, Dealroom, BW Disrupt, MediaBrief",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, even_id, "FUNDRAISING", even_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (even_id, "Series B", "$50 million", "USD", "2026-10-19",
     "Khosla Ventures (lead, existing investor), Alpha Wave",
     "Build five new hospitals across Bengaluru over the next six months",
     "https://yourstory.com/2026/10/even-healthcare-raises-50m-in-series-b-round-led-by-khosla-ventures",
     "Total funding to date over $120M; ~$300M valuation (reported, unconfirmed by company); hospital "
     "care is a considered/high-stakes purchase, clears brand-fit gate regardless of B2C "
     "classification"),
)
conn.commit()

even_open_triggers = repo.open_trigger_count(conn, even_id)
even_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.65,
        "business_standard_audience_fit": 0.60,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.50,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=even_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, even_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=even_open_triggers,
    score=even_result["score"],
    classification=even_result["classification"],
    timing="IMMEDIATE",
    why_now="Series B closed yesterday with a marquee repeat investor (Khosla Ventures) tripling the "
            "prior valuation -- strong, fresh news hook tied to a concrete 5-hospital Bengaluru "
            "expansion plan.",
    why_this_company="Even Healthcare, Bangalore HQ verified. Differentiated value-based-care hospital "
                      "chain scaling aggressively in its home city.",
    business_problem="A well-funded hospital chain opening 5 new Bengaluru facilities needs patient-"
                      "trust and brand-differentiation content to stand out in a crowded healthcare "
                      "market, especially given its unconventional non-fee-for-service model.",
    why_business_standard="Considered, high-stakes healthcare purchase with a genuine business-model "
                           "story (value-based care economics) fits BS's business and affluent-consumer "
                           "readership.",
    recommended_product="branded_content, thought_leadership, premium_display",
    recommended_action="Pitch a founder/CEO thought-leadership angle on India's shift toward value-"
                        "based healthcare economics, tied to the hospital-expansion news; no marketing "
                        "contact confirmed in this pass.",
    is_qualified_target=even_result["is_qualified_target"],
    score_breakdown=even_result["score_breakdown"],
)

conn.close()
print("Even Healthcare:", even_result)
