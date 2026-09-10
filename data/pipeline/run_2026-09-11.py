#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-11 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: Inbound Aerospace (Chennai-based, IIT Madras-incubated
space-tech startup developing an autonomous, unmanned, recoverable
re-entry spacecraft for LEO missions -- microgravity research, in-orbit
tech demos, in-space manufacturing, payload return, plus precision-
landing capability relevant to defence/disaster response) signed a
five-year MoU with Australia's Space Angel Group on Sep 10 2026 (a
three-year framework effective immediately) to explore collaboration on
flight/drop testing, high-altitude and near-space trials, recovery
operations, spaceport infrastructure, and mission planning, with scope
for joint tech development, pilots, and India/Australia market
expansion. Deep-tech aerospace/space-tech B2B -- qualifies regardless
of ticket size. (Company's only funding to date is a $1M pre-seed from
Jul 23 2025 (Speciale Invest-led) -- over a year old, not a fresh
trigger; the MoU is today's actual news.)

Checked and declined:
  - Swish (10-min food delivery, $24M raise led by Bertelsmann India
    Investments, announced today) -- Bangalore HQ verified (HSR Layout,
    per company registration), but quick-commerce food delivery is a
    routine, low-ticket, mass-market daily-consumption purchase, not a
    considered/higher-ticket one -- same reasoning as excluding Peeko/
    Comet/Kuku FM/Third Wave Coffee. Not scored on brand-fit grounds.

Checked and left unscored (deal not yet closed): Mesa School of
Business (Bengaluru-based) -- Entrackr's "Exclusive: Mesa School set to
raise Rs 100 Cr in Series A; co-founder may sell 2.9% stake" (Sep 10
2026) is pre-close reporting ("set to raise", "may sell") on a round
that has not been confirmed as closed. Per the no-fabrication rule, an
unclosed/rumoured round is not scored as a FUNDRAISING event -- worth a
follow-up check once/if the round is confirmed closed.

Checked and declined (not a fresh trigger): Razorpay presented its
Vulcan AI payments foundation model to PM Modi at GFF 2026 (Sep 10
2026) -- Vulcan itself launched Aug 18 2026 (NVIDIA/AWS-backed, trained
on ~4B payments); today's news is a PR/showcase appearance of an
already-3-week-old product launch, not a new business event. Razorpay
is already verified_qualified on the watchlist; no duplicate trigger
opened for a re-presentation of old news.

Also checked: Chittorgarh (IPO closures today were Prasol Chemicals/
Glass Wall Systems/Kanohar Electricals -- none in a qualified city),
real-estate developer news (Sobha's 40-acre North Bengaluru pre-launch
is real but undated/general, not a fresh dated trigger this pass),
industry movement via afaqs!/Storyboard18 (no qualifying brand-agency
mandate story found for the three qualified cities today).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

ia_id = repo.get_or_create_company(conn, "Inbound Aerospace", industry="Space-tech / re-entry spacecraft manufacturing")
repo.set_hq_status(
    conn, ia_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Inbound Aerospace Private Limited, C/o IITM Research Park, 1FA, I Floor, Kanagam Road, "
             "TTTI Taramani, Chennai 600113 (CIN U30300TN2025PTC175928, RoC-Chennai) -- registered AND "
             "operational HQ both Chennai, no discrepancy.",
    source_url="https://www.tofler.in/inbound-aerospace-private-limited/company/U30300TN2025PTC175928",
)
ia_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (ia_id, "strategic_partnership", "MAJOR_PARTNERSHIP",
     "Signed a five-year MoU with Australia's Space Angel Group (three-year framework effective "
     "September 2026) to explore collaboration across flight/drop testing, high-altitude and near-space "
     "trials, recovery operations, spaceport infrastructure, and mission planning -- scope includes "
     "joint tech development, pilots, and India/Australia market expansion for Inbound's autonomous, "
     "unmanned, recoverable re-entry spacecraft for LEO missions.",
     "2026-09-10", "2026-09-10", "FACT",
     "https://yourstory.com/2026/09/startup-news-and-updates-daily-roundup-september-10-2026",
     "YourStory",
     "\"Inbound Aerospace signs five-year MoU with Australia's Space Angel Group\" -- Sep 10 2026 "
     "daily roundup",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, ia_id, "MAJOR_PARTNERSHIP", ia_event_id)

ia_open_triggers = repo.open_trigger_count(conn, ia_id)
ia_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.55,
        "advertising_marketing_signal": 0.25,
        "timing_urgency": 0.55,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.30,
        "decision_maker_availability": 0.25,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.65,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=ia_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, ia_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="MAJOR_PARTNERSHIP",
    trigger_count=ia_open_triggers,
    score=ia_result["score"],
    classification=ia_result["classification"],
    timing="IMMEDIATE",
    why_now="Cross-border strategic MoU signed yesterday -- a fresh international-partnership hook "
            "while the news is new, though the company is still a very early-stage (pre-seed only) "
            "startup with limited marketing budget today.",
    why_this_company="Inbound Aerospace, Chennai HQ verified. IIT Madras-incubated space-tech startup "
                      "building autonomous re-entry spacecraft, now expanding testing infrastructure "
                      "internationally via Australia's Space Angel Group.",
    business_problem="An early-stage deep-tech space company signing its first major international "
                      "infrastructure partnership needs credibility-building business/investor-press "
                      "visibility ahead of future fundraising rounds.",
    why_business_standard="Deep-tech aerospace B2B partnership with a national-strategic (space/defence-"
                           "adjacent) angle fits BS's business/policy readership, though low current "
                           "marketing capacity (pre-seed stage) caps this at WATCH rather than higher.",
    recommended_product="corporate_communication, thought_leadership",
    recommended_action="Low-to-medium urgency; pitch a thought-leadership angle on India's private "
                        "space-tech sector's first cross-border testing partnerships if BS wants to "
                        "move on it; no marketing contact confirmed in this pass.",
    is_qualified_target=ia_result["is_qualified_target"],
    score_breakdown=ia_result["score_breakdown"],
)

conn.close()
print("Inbound Aerospace:", ia_result)
