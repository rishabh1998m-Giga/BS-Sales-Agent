#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-09-12 daily-sales-brief run
(Saturday). Self-bound 1:30 AM IST trigger.

New finding: QClairvoyance Quantum Labs (Hyderabad-based deep-tech
quantum computing company, founded 2024) signed an MoU on Sep 11 2026
with the IITM-C-DOT Samgnya Technologies Foundation -- India's National
Hub for Quantum Communication under the National Quantum Mission (DST,
Govt of India). Scope covers quantum computing, quantum algorithms,
quantum AI, post-quantum cybersecurity, and next-gen computing --
research, tech development, and validation, with pathways to testbed
validation, talent development, and technology translation/
commercialization. Covered directly by Business Standard. Deep-tech
B2B/government-research partnership -- qualifies regardless of ticket
size. (Same pattern as QNu Labs' Sep 9 raise and Inbound Aerospace's
Sep 10 MoU -- India's National Quantum Mission ecosystem generating a
steady stream of qualified-city deep-tech triggers this week.)

Checked and declined:
  - Popo Global (The Pizza Bakery / Paris Panini / Smash Guys operator)
    -- Bengaluru HQ, raised Rs 532 Cr from Artal Asia (its first
    external round, Rs 1,500 Cr valuation) -- but QSR/casual dining
    (pizza, sandwiches, smash burgers) is routine mass-market food
    consumption, not a considered/higher-ticket purchase -- same
    reasoning as excluding Third Wave Coffee/Britannia/Swish. Not
    scored on brand-fit grounds.
  - BharatPeX (BharatPe's enterprise payment-gateway launch at GFF
    2026) -- BharatPe HQ is Gurugram/Delhi, neither a qualified city.
  - Piston (cardless fleet-fuel payments, $15M Series A led by FPV
    Ventures) -- HQ is US, with only an engineering centre in Kolkata
    (not a qualified city, and not an India-HQ under the international-
    company rule since Kolkata isn't one of the three cities either).
  - Hero Motors IPO (Rs 1,000 Cr, opens Sep 16) -- registered office
    Ludhiana, Punjab -- not a qualified city.
  - Namma Yatri's "Namma Santhe" driver retail platform launch
    (Bengaluru) -- Namma Yatri's core product is zero-commission
    ride-hailing, a routine low-ticket B2C mobility service (same
    reasoning as excluding other ride-hailing/quick-commerce apps);
    the retail-platform extension for drivers is lower-ticket still.
    Not scored on brand-fit grounds.

Also checked: Chittorgarh (IPO closures today -- Rentomojo (already
tracked), Karamtara Engineering, LCC Projects, Amtech Esters, and
others -- none in a newly-qualified city), real-estate developer news
(no fresh dated item for the watchlist's tracked developers this
pass), industry movement via afaqs!/Storyboard18 (no qualifying
brand-agency mandate story found for the three qualified cities today).
Weekend news cycle is naturally thinner outside the one deep-tech item
above.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

qcv_id = repo.get_or_create_company(conn, "QClairvoyance Quantum Labs", industry="Quantum computing / quantum algorithms deep-tech R&D")
repo.set_hq_status(
    conn, qcv_id, "HYDERABAD_HQ_VERIFIED",
    claimed_city="Hyderabad", hq_city="Hyderabad",
    evidence="Qclairvoyance Quantum Labs Private Limited, Plot No. 191, Sy No. 60, Teachers Colony, "
             "Sainikpuri, Tirumalagiri, Hyderabad 500094 (CIN U72100TS2024PTC185393, RoC-Hyderabad) -- "
             "registered AND operational HQ both Hyderabad, no discrepancy.",
    source_url="https://www.tofler.in/qclairvoyance-quantum-labs-private-limited/company/U72100TS2024PTC185393",
)
qcv_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (qcv_id, "strategic_partnership", "MAJOR_PARTNERSHIP",
     "Signed an MoU with the IITM-C-DOT Samgnya Technologies Foundation -- India's National Hub for "
     "Quantum Communication under the National Quantum Mission (Dept of Science & Technology, Govt of "
     "India) -- covering quantum computing, quantum algorithms, quantum AI, post-quantum cybersecurity, "
     "and next-generation computing. Scope includes joint research, technology development and "
     "validation via testbeds, talent development, and potential technology translation/"
     "commercialization.",
     "2026-09-11", "2026-09-11", "FACT",
     "https://www.business-standard.com/companies/news/qclairvoyance-iitm-cdot-samgnya-quantum-technology-mou-126091100595_1.html",
     "Business Standard / The Quantum Insider / Telangana Today",
     "\"QClairvoyance Quantum Labs, IITM-C-DOT Samgnya tie up on quantum tech\" -- Sep 11 2026, "
     "corroborated across Business Standard, The Quantum Insider, Telangana Today, CXO Digitalpulse",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, qcv_id, "MAJOR_PARTNERSHIP", qcv_event_id)

qcv_open_triggers = repo.open_trigger_count(conn, qcv_id)
qcv_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.55,
        "advertising_marketing_signal": 0.25,
        "timing_urgency": 0.55,
        "business_standard_audience_fit": 0.60,
        "estimated_marketing_capacity": 0.30,
        "decision_maker_availability": 0.25,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.65,
    },
    hq_status="HYDERABAD_HQ_VERIFIED",
    open_trigger_count=qcv_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, qcv_id,
    hq_status="HYDERABAD_HQ_VERIFIED",
    primary_trigger="MAJOR_PARTNERSHIP",
    trigger_count=qcv_open_triggers,
    score=qcv_result["score"],
    classification=qcv_result["classification"],
    timing="IMMEDIATE",
    why_now="MoU with a National Quantum Mission hub signed yesterday -- a fresh national-strategic-"
            "technology hook, though the company is early-stage (founded 2024) with limited marketing "
            "budget today.",
    why_this_company="QClairvoyance Quantum Labs, Hyderabad HQ verified. Early-stage deep-tech quantum "
                      "computing company now formally tied into India's National Quantum Mission "
                      "ecosystem.",
    business_problem="An early-stage deep-tech company entering a government-linked research "
                      "partnership needs credibility-building business/investor-press visibility ahead "
                      "of future fundraising.",
    why_business_standard="Deep-tech quantum-computing partnership tied to a national strategic mission "
                           "fits BS's business/policy readership; early-stage/pre-revenue status caps "
                           "this at WATCH rather than higher.",
    recommended_product="corporate_communication, thought_leadership",
    recommended_action="Low-to-medium urgency; pitch a thought-leadership angle on Hyderabad's emerging "
                        "role in India's National Quantum Mission ecosystem if BS wants to move on it; "
                        "no marketing contact confirmed in this pass.",
    is_qualified_target=qcv_result["is_qualified_target"],
    score_breakdown=qcv_result["score_breakdown"],
)

conn.close()
print("QClairvoyance Quantum Labs:", qcv_result)
