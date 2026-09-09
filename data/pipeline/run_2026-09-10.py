#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-10 daily-sales-brief run.
Self-bound 1:30 AM IST trigger.

New finding: QNu Labs (QuNu Labs Pvt Ltd) -- deep-tech quantum-safe
cybersecurity company (QKD, QRNG, PQC), founded 2016 by Srinivasa Rao
Aluri and Sunil Gupta, incubated at IIT Madras before operating out of
Bengaluru -- raised Rs 200 crore ($25M) Series A1 on Sep 9 2026, led by
the National Quantum Mission and Speciale Invest, with Sony Innovation
Fund, Gaja Capital, and Artha Ventures participating. Takes total
funding to Rs 375 crore; ~80% of this round from new global investors.
Capital earmarked for R&D, sales/GTM scale-up, an RDI-approved project
building India's Quantum Secure and Sensing Networks backbone, and
expansion into quantum sensing and AI. Deep-tech B2B cybersecurity --
qualifies regardless of ticket size. Covered directly by Business
Standard itself.

Checked and declined:
  - Carrum Mobility ($10M Series B from Uber, fleet-management,
    $168M valuation) -- HQ is Gurugram (confirmed via Inc42/TechCrunch/
    YourStory), not a qualified city. Operates fleets across Bengaluru/
    Hyderabad/Chennai among other cities, but operational presence !=
    HQ (same reasoning as Adobe/Guidehouse/Parkobot).
  - Cross-checked the StartupTalky Sep 9 roundup blurb, which had
    conflated Carrum's Uber-led round into the QNu Labs item ("National
    Quantum Mission, Speciale Invest and Uber were among the day's lead
    investors") -- verified independently via Entrepreneur India/The
    Quantum Insider/Business Standard/YourStory/StartupTalky's own
    dedicated QNu Labs article, none of which mention Uber as a QNu
    investor. Uber excluded from the funding_events entry as
    unsubstantiated/likely a source-aggregation error.
  - RentoMojo raising Rs 376 Cr from anchor investors ahead of IPO
    opening -- already a tracked WATCH-tier opportunity (IPO trigger
    opened 2026-09-07); this is a further milestone in the same
    progressing IPO, not a new company or a new trigger category, so no
    duplicate opportunity row created.

Also checked: Chittorgarh (no new qualified-city DRHP beyond the
already-tracked RentoMojo), industry movement via Storyboard18/afaqs!
(indie-agency-vs-AOR trend pieces and a creativity-awards recap --
no individual brand-agency mandate/association story in scope for
Section 16).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

qnu_id = repo.get_or_create_company(conn, "QNu Labs", industry="Quantum-safe cybersecurity (QKD/QRNG/PQC)")
repo.set_hq_status(
    conn, qnu_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="QuNu Labs Private Limited, Centenary Building, East Wing, 2nd Floor, No. 28, M.G. Road, "
             "Bengaluru, Karnataka 560025 (CIN U72900KA2016PTC096629, RoC-Bangalore) -- registered AND "
             "operational HQ both Bangalore, no discrepancy.",
    source_url="https://www.zaubacorp.com/company/QUNU-LABS-PRIVATE-LIMITED/U72900KA2016PTC096629",
)
qnu_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (qnu_id, "funding_round", "FUNDRAISING",
     "Raised Rs 200 crore (~$25M) Series A1 led by the National Quantum Mission and Speciale Invest, "
     "with Sony Innovation Fund, Gaja Capital, and Artha Ventures participating -- takes total funding "
     "to Rs 375 crore, with ~80% of this round from new global investors. Proceeds earmarked for R&D, "
     "sales/GTM scale-up, an RDI-approved project to build the technology backbone of India's Quantum "
     "Secure and Sensing Networks, and expansion into quantum sensing and AI.",
     "2026-09-09", "2026-09-09", "FACT",
     "https://www.business-standard.com/companies/news/qnu-labs-raises-200-crore-as-demand-for-quantum-safe-security-builds-126090901042_1.html",
     "Business Standard / YourStory / The Quantum Insider",
     "\"QNu Labs raises Rs 200 crore as demand for quantum-safe security builds\" -- Sep 9 2026, "
     "corroborated across Business Standard, YourStory, The Quantum Insider, StartupTalky",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, qnu_id, "FUNDRAISING", qnu_event_id)

conn.execute(
    """INSERT INTO funding_events
       (company_id, stage, amount, currency, date_announced, investors, purpose, source_url, evidence)
       VALUES (?,?,?,?,?,?,?,?,?)""",
    (qnu_id, "Series A1", "Rs 200 crore (~$25 million)", "INR", "2026-09-09",
     "National Quantum Mission and Speciale Invest (co-leads), Sony Innovation Fund, Gaja Capital, "
     "Artha Ventures",
     "R&D, sales/GTM scale-up, RDI-approved Quantum Secure and Sensing Networks backbone project, "
     "expansion into quantum sensing and AI",
     "https://www.business-standard.com/companies/news/qnu-labs-raises-200-crore-as-demand-for-quantum-safe-security-builds-126090901042_1.html",
     "Total funding to date Rs 375 crore; ~80% of this round from new global investors; deep-tech B2B "
     "cybersecurity qualifies regardless of ticket size"),
)
conn.commit()

qnu_open_triggers = repo.open_trigger_count(conn, qnu_id)
qnu_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.30,
        "timing_urgency": 0.75,
        "business_standard_audience_fit": 0.70,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.70,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=qnu_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, qnu_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="FUNDRAISING",
    trigger_count=qnu_open_triggers,
    score=qnu_result["score"],
    classification=qnu_result["classification"],
    timing="IMMEDIATE",
    why_now="Series A1 announced today, backed by a government-linked lead investor (National Quantum "
            "Mission) plus a marquee strategic (Sony Innovation Fund) -- a strong, fresh national-"
            "deep-tech narrative hook.",
    why_this_company="QNu Labs, Bangalore HQ verified. India's first commercial quantum cryptography "
                      "company, now positioned at the center of India's Quantum Secure and Sensing "
                      "Networks push.",
    business_problem="A deep-tech company scaling GTM after a large raise, with a government-mission "
                      "narrative attached, needs business/investor-press visibility to build category "
                      "credibility as it moves from R&D-stage to commercial scale.",
    why_business_standard="Deep-tech B2B funding tied to a national strategic-technology mission is a "
                           "strong BS business/policy-readership fit; already covered directly by "
                           "Business Standard's own newsroom, indicating existing editorial interest.",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_action="Pitch thought-leadership content on India's quantum-safe security push tied to "
                        "the National Quantum Mission angle; no marketing contact confirmed in this "
                        "pass.",
    is_qualified_target=qnu_result["is_qualified_target"],
    score_breakdown=qnu_result["score_breakdown"],
)

conn.close()
print("QNu Labs:", qnu_result)
