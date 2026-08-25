#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-25 daily-sales-brief run.

Context: the automated 04:04 UTC daily trigger fired on both 2026-08-24 and
2026-08-25 but produced no commit and no visible session either day -- root
cause not identified (reported to the user). This run was executed live,
interactively, in the main chat session instead, using the same rules as
the automated prompt (docs/master-spec.md, config/*.yaml).

Two watchlist items resolved (config/watchlist.yaml updated separately):
  - Salesforce: registered office is Bengaluru (CIN U72200KA2005PTC037330);
    largest India operational hub is Hyderabad -- both are qualified
    cities, so this resolves either way. verified_qualified.
  - Vector Consulting Group: registered office Thane, Maharashtra (Mumbai-
    adjacent) -- not a qualified city. verified_non_qualified.

New opportunities found via the Vetri Tamil Nadu Investors' Conclave
(held 2026-08-13, Chennai; config/state-events.yaml already tracked this
event from the 2026-08-23 pass via Skyroot's MoU) -- checking who ELSE
signed MoUs there surfaced three more qualified-city EXPANSION triggers
that were not previously in our database, plus one for an already-tracked
company (Saint-Gobain) that didn't have this event recorded yet.

Also found via a fresh Chittorgarh/DRHP check: Tonbo Imaging (Bengaluru-
HQ defence-electronics OEM), an IPO-stage company not previously tracked.

Decision-maker movement check: cross-checked all 9 tracked contacts;
spot-checked the two most likely to have changed (CRED's Miten Sampat,
PhonePe's Amit Doshi) -- both roles confirmed unchanged, no
leadership_changes rows needed.

Editorial/industry-movement scan (Exchange4Media/afaqs!): no Bangalore/
Chennai/Hyderabad-relevant agency-movement item found today -- honestly
omitted rather than padded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402
from scoring import scorer  # noqa: E402

conn = repo.connect()
cfg = scorer.load_config()

# --------------------------------------------------------------- Salesforce
sf_id = repo.get_or_create_company(conn, "Salesforce", industry="Enterprise SaaS/CRM")
repo.set_hq_status(
    conn, sf_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Salesforce.com India Pvt Ltd registered office: Torrey Pines, Embassy Golflinks, "
             "Bangalore 560071 (CIN U72200KA2005PTC037330). Largest India operational/engineering hub is "
             "Hyderabad (DivyaSree Orion) -- both Bengaluru and Hyderabad are qualified cities, so this "
             "resolves as qualified either way; no single-HQ ambiguity affects the gate outcome.",
    source_url="https://www.zaubacorp.com/SALESFORCE-COM-INDIA-PRIVATE-LIMITED-U72200KA2005PTC037330",
)

# ----------------------------------------------------------- Vector Consulting
vector_id = repo.get_or_create_company(conn, "Vector Consulting Group", industry="Management consulting")
repo.set_hq_status(
    conn, vector_id, "NON_QUALIFIED_HQ_VERIFIED",
    evidence="Vector Management Consulting Pvt Ltd registered office: Thane One, Ghodbunder Road, "
             "Thane (West), Maharashtra 400610 -- not a qualified city despite a Bengaluru presence.",
    source_url="https://www.vectorconsulting.in/en/about-us/the-firm/",
)

# -------------------------------------------------------- Michelin (HQ only)
# Found via a Chennai-expansion search; HQ verified for future reference, but
# no opportunity scored today -- the "upcoming Chennai plant" news found
# could not be confirmed as dated recently, and never fabricate an event
# date. Revisit if a dated trigger surfaces in a future run.
michelin_id = repo.get_or_create_company(conn, "Michelin India", industry="Tyres/automotive")
repo.set_hq_status(
    conn, michelin_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Michelin India Pvt Ltd registered office: Shyamala Towers, Arcot Road, Saligramam, "
             "Chennai 600093 (CIN U25119TN2009PTC071454).",
    source_url="https://opencorpdata.com/lei/5493005EBQ2O0VNEOB83",
)

# =========================================================================
# Vetri Tamil Nadu Investors' Conclave (2026-08-13, Chennai) -- MoU sweep
# =========================================================================

# ------------------------------------------------------------ Saint-Gobain
# Already tracked + HQ-verified (2026-08-23d watchlist pass); this event was
# not yet recorded for them.
sg_row = conn.execute("SELECT company_id FROM companies WHERE name = ?", ("Saint-Gobain",)).fetchone()
sg_id = sg_row[0]
sg_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (sg_id, "capacity_expansion", "EXPANSION",
     "Will invest Rs 2,000 crore in Tamil Nadu: a new greenfield plant in Krishnagiri and an expansion "
     "at Kanchipuram -- MoU signed at the Vetri Tamil Nadu Investors' Conclave.",
     "2026-08-13", "2026-08-13", "FACT",
     "https://www.business-standard.com/amp/industry/news/tamil-nadu-investment-conclave-daimler-saint-gobain-ykk-projects-126081300907_1.html",
     "Business Standard",
     "\"Global majors bet on Tamil Nadu as Daimler, Saint-Gobain line up projects\" -- Rs 2,000 Cr across "
     "Krishnagiri (greenfield) + Kanchipuram (expansion), Aug 13 2026 conclave",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, sg_id, "EXPANSION", sg_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (sg_id, "new_plant + capacity_expansion", "Krishnagiri and Kanchipuram, Tamil Nadu", "2026-08-13",
     "Rs 2,000 crore investment; greenfield plant in Krishnagiri + expansion at Kanchipuram",
     "https://www.business-standard.com/amp/industry/news/tamil-nadu-investment-conclave-daimler-saint-gobain-ykk-projects-126081300907_1.html",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave, Aug 13 2026"),
)
conn.commit()

sg_open_triggers = repo.open_trigger_count(conn, sg_id)
sg_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.55,
        "business_standard_audience_fit": 0.70,
        "estimated_marketing_capacity": 0.75,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.60,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=sg_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, sg_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=sg_open_triggers,
    score=sg_result["score"],
    classification=sg_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Rs 2,000 Cr Tamil Nadu MoU is 12 days old, still in the announcement-visibility window before "
            "ground-breaking coverage cycles move on.",
    why_this_company="Saint-Gobain, Chennai HQ verified. Major building-materials/glass MNC making a large, "
                      "freshly announced two-site Tamil Nadu commitment.",
    business_problem="A large capex announcement needs sustained investor/business-press visibility beyond "
                      "the initial signing-day news cycle.",
    why_business_standard="B2B industrial/infrastructure story squarely in BS's business-decision-maker "
                           "readership; good fit for corporate storytelling around the investment.",
    recommended_product="corporate_storytelling, branded_content, display",
    recommended_action="Pitch corporate storytelling tied to the Krishnagiri/Kanchipuram investment; no "
                        "confirmed India marketing contact found in this pass -- verify before outreach.",
    is_qualified_target=sg_result["is_qualified_target"],
    score_breakdown=sg_result["score_breakdown"],
)

# ------------------------------------------------ Daimler India Commercial Vehicles
dicv_id = repo.get_or_create_company(conn, "Daimler India Commercial Vehicles", industry="Commercial vehicles")
repo.set_hq_status(
    conn, dicv_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Daimler India Commercial Vehicles Pvt Ltd -- registered office SIPCOT Industrial Growth "
             "Centre, Oragadam, Sriperumbudur Taluk, Kancheepuram, TN 602105 (CIN U34200TN2007PTC072876); "
             "corporate office RMZ Millenia, Perungudi, Chennai. Oragadam is part of the Chennai "
             "metropolitan industrial belt, same treatment as Toyota Kirloskar/Bidadi for Bangalore.",
    source_url="https://www.zaubacorp.com/DAIMLER-INDIA-COMMERCIAL-VEHICLES-PRIVATE-LIMITED-U34200TN2007PTC072876",
)
dicv_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (dicv_id, "capacity_expansion", "EXPANSION",
     "Will invest Rs 4,000 crore to expand its Oragadam facility for design, R&D, and manufacturing of "
     "commercial vehicles -- MoU signed at the Vetri Tamil Nadu Investors' Conclave.",
     "2026-08-13", "2026-08-13", "FACT",
     "https://www.business-standard.com/amp/industry/news/tamil-nadu-investment-conclave-daimler-saint-gobain-ykk-projects-126081300907_1.html",
     "Business Standard",
     "\"Global majors bet on Tamil Nadu as Daimler, Saint-Gobain line up projects\" -- Rs 4,000 Cr Oragadam "
     "expansion, Aug 13 2026 conclave",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, dicv_id, "EXPANSION", dicv_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (dicv_id, "capacity_expansion", "Oragadam, Chennai", "2026-08-13",
     "Rs 4,000 crore investment to expand the Oragadam facility (design, R&D, manufacturing)",
     "https://www.business-standard.com/amp/industry/news/tamil-nadu-investment-conclave-daimler-saint-gobain-ykk-projects-126081300907_1.html",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave, Aug 13 2026"),
)
conn.commit()

dicv_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (dicv_id, "Torsten Schmidt", "Managing Director & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://www.autocarpro.in/news/torsten-schmidt-named-managing-director-ceo-of-daimler-india-commercial-vehicles-129777"),
).lastrowid
conn.commit()

dicv_open_triggers = repo.open_trigger_count(conn, dicv_id)
dicv_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.80,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.55,
        "business_standard_audience_fit": 0.70,
        "estimated_marketing_capacity": 0.75,
        "decision_maker_availability": 0.55,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.60,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=dicv_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, dicv_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=dicv_open_triggers,
    score=dicv_result["score"],
    classification=dicv_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Rs 4,000 Cr Oragadam expansion MoU is 12 days old; new CEO (Torsten Schmidt, took over early "
            "2026) gives a fresh leadership-visibility angle alongside the capex story.",
    why_this_company="Daimler India Commercial Vehicles, Chennai HQ verified. One of the largest single "
                      "commitments at the conclave.",
    business_problem="Needs sustained business-press visibility for a large capex commitment plus "
                      "introducing a new MD & CEO to the Indian business audience.",
    why_business_standard="B2B commercial-vehicle manufacturing story with a new-leadership angle -- fits "
                           "BS's corporate/industrial readership.",
    recommended_product="corporate_storytelling, branded_content",
    recommended_contact_id=dicv_contact_id,
    recommended_action="Pitch a combined new-CEO-plus-Oragadam-expansion corporate story; confirm India "
                        "marketing/comms contact before outreach.",
    is_qualified_target=dicv_result["is_qualified_target"],
    score_breakdown=dicv_result["score_breakdown"],
)

# ------------------------------------------------------------ Trivitron Healthcare
trivitron_id = repo.get_or_create_company(conn, "Trivitron Healthcare", industry="Medical devices")
repo.set_hq_status(
    conn, trivitron_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Trivitron Healthcare Pvt Ltd, Sapthagiri Bhawan, Abhiramapuram, Chennai 600018 "
             "(CIN U85110TN1998PTC040515, RoC-Chennai).",
    source_url="https://www.zaubacorp.com/company/TRIVITRON-HEALTHCARE-PRIVATE-LIMITED/U85110TN1998PTC040515",
)
trivitron_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (trivitron_id, "capacity_expansion", "EXPANSION",
     "Announced a Rs 200 crore brownfield expansion, creating approx. 200 direct jobs -- MoU signed at the "
     "Vetri Tamil Nadu Investors' Conclave.",
     "2026-08-13", "2026-08-13", "FACT",
     "https://www.etvbharat.com/en/state/vettri-tamil-nadu-investors-conclave-2026-mou-cm-joseph-vijay-august-13-enn26081302026",
     "ETV Bharat",
     "\"Tamil Nadu Investors' Conference: MoUs Signed With 97 Companies\" -- Trivitron Healthcare Rs 200 Cr "
     "brownfield expansion, ~200 jobs, Aug 13 2026",
     "MEDIUM"),
).lastrowid
conn.commit()
repo.open_trigger(conn, trivitron_id, "EXPANSION", trivitron_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (trivitron_id, "brownfield_expansion", "Tamil Nadu", "2026-08-13",
     "Rs 200 crore brownfield expansion; approx. 200 direct jobs",
     "https://www.etvbharat.com/en/state/vettri-tamil-nadu-investors-conclave-2026-mou-cm-joseph-vijay-august-13-enn26081302026",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave, Aug 13 2026"),
)
conn.commit()

trivitron_open_triggers = repo.open_trigger_count(conn, trivitron_id)
trivitron_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.55,
        "advertising_marketing_signal": 0.30,
        "timing_urgency": 0.50,
        "business_standard_audience_fit": 0.55,
        "estimated_marketing_capacity": 0.45,
        "decision_maker_availability": 0.30,
        "official_contact_availability": 0.10,
        "strategic_relevance": 0.45,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=trivitron_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, trivitron_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=trivitron_open_triggers,
    score=trivitron_result["score"],
    classification=trivitron_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Rs 200 Cr brownfield expansion MoU is 12 days old; smaller commitment than the others at the "
            "same conclave, so a modest, watch-tier opportunity rather than an urgent one.",
    why_this_company="Trivitron Healthcare, Chennai HQ verified. Medical-devices manufacturer expanding "
                      "domestic capacity.",
    business_problem="Smaller B2B med-tech manufacturer with limited public marketing footprint; expansion "
                      "news is a modest opportunity to build visibility.",
    why_business_standard="B2B healthcare-manufacturing story fits BS's industrial/business coverage, "
                           "though audience overlap is narrower than the larger conclave commitments.",
    recommended_product="corporate_storytelling, digital_display",
    recommended_action="Low-urgency watch; revisit if the expansion generates further coverage or a "
                        "marketing contact surfaces.",
    is_qualified_target=trivitron_result["is_qualified_target"],
    score_breakdown=trivitron_result["score_breakdown"],
)

# ------------------------------------------------------------------ Agnikul Cosmos
agnikul_id = repo.get_or_create_company(conn, "Agnikul Cosmos", industry="Space launch vehicles")
repo.set_hq_status(
    conn, agnikul_id, "CHENNAI_HQ_VERIFIED",
    claimed_city="Chennai", hq_city="Chennai",
    evidence="Agnikul Cosmos Pvt Ltd, National Centre for Combustion Research and Development, IIT Madras, "
             "Chennai (CIN U74999TN2017PTC119779, RoC-Chennai).",
    source_url="https://www.zaubacorp.com/company/AGNIKUL-COSMOS-PRIVATE-LIMITED/U74999TN2017PTC119779",
)
agnikul_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (agnikul_id, "capacity_expansion", "EXPANSION",
     "Committed Rs 400 crore and ~1,500 jobs to set up assembly and integration operations for its "
     "reusable, liquid-propelled launch vehicles -- MoU signed at the Vetri Tamil Nadu Investors' Conclave.",
     "2026-08-13", "2026-08-13", "FACT",
     "https://www.business-standard.com/india-news/vetri-tamil-nadu-investment-conclave-2026-agnikul-skyroot-semiconductor-investments-126081300888_1.html",
     "Business Standard",
     "\"Tamil Nadu Investment Conclave: Space firms line up Rs 650 Cr investments\" -- Agnikul Cosmos "
     "Rs 400 Cr, ~1,500 jobs, Aug 13 2026",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, agnikul_id, "EXPANSION", agnikul_event_id)

conn.execute(
    """INSERT INTO expansion_events
       (company_id, expansion_type, location, announcement_date, details, source_url, evidence)
       VALUES (?,?,?,?,?,?,?)""",
    (agnikul_id, "new_facility", "Tamil Nadu", "2026-08-13",
     "Rs 400 crore investment; ~1,500 jobs for assembly/integration of reusable launch vehicles",
     "https://www.business-standard.com/india-news/vetri-tamil-nadu-investment-conclave-2026-agnikul-skyroot-semiconductor-investments-126081300888_1.html",
     "MoU signed at Vetri Tamil Nadu Investors' Conclave, Aug 13 2026"),
)
conn.commit()

agnikul_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (agnikul_id, "Srinath Ravichandran", "Co-Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://en.wikipedia.org/wiki/AgniKul_Cosmos"),
).lastrowid
conn.commit()

agnikul_open_triggers = repo.open_trigger_count(conn, agnikul_id)
agnikul_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.75,
        "advertising_marketing_signal": 0.40,
        "timing_urgency": 0.55,
        "business_standard_audience_fit": 0.75,
        "estimated_marketing_capacity": 0.50,
        "decision_maker_availability": 0.70,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.70,
    },
    hq_status="CHENNAI_HQ_VERIFIED",
    open_trigger_count=agnikul_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, agnikul_id,
    hq_status="CHENNAI_HQ_VERIFIED",
    primary_trigger="EXPANSION",
    trigger_count=agnikul_open_triggers,
    score=agnikul_result["score"],
    classification=agnikul_result["classification"],
    timing="MEDIUM_TERM",
    why_now="Rs 400 Cr / ~1,500-job Tamil Nadu commitment is 12 days old; same conclave that produced "
            "Skyroot's MoU, and space-tech is a live BS/industrial-press narrative right now.",
    why_this_company="Agnikul Cosmos, Chennai HQ verified (IIT Madras-incubated). Reusable-launch-vehicle "
                      "space-tech firm with a credible founder story and a fresh capital commitment.",
    business_problem="A deep-tech, pre-mainstream-brand company needs credibility and visibility with "
                      "investors/enterprise customers, not consumer awareness.",
    why_business_standard="Strong fit for BS's business/investor readership -- space-tech + a large state "
                           "investment commitment is a compelling corporate-narrative and thought-leadership "
                           "angle (comparable to the existing Skyroot Aerospace opportunity).",
    recommended_product="thought_leadership, corporate_communication, branded_content",
    recommended_contact_id=agnikul_contact_id,
    recommended_action="Pitch a founder thought-leadership piece tied to the Tamil Nadu facility "
                        "commitment; group with Skyroot for a joint 'India's space-tech corridor' angle if "
                        "BS wants a bigger feature.",
    is_qualified_target=agnikul_result["is_qualified_target"],
    score_breakdown=agnikul_result["score_breakdown"],
)

# =========================================================================
# Tonbo Imaging -- new IPO-stage company (Bengaluru HQ), found via Chittorgarh/
# DRHP check. DRHP filed Dec 2025; still pre-listing as of this pass, no
# listing date confirmed -- newly discovered/tracked today.
# =========================================================================
tonbo_id = repo.get_or_create_company(conn, "Tonbo Imaging", industry="Defence electronics/imaging")
repo.set_hq_status(
    conn, tonbo_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Tonbo Imaging India Ltd, registered at Chikkayellappa Tower-II, Sarjapur Main Road, "
             "Jakkasandra Extn, Bangalore 560034.",
    source_url="https://groww.in/blog/tonbo-imaging-india-files-drhp-with-sebi",
)
tonbo_event_id = conn.execute(
    """INSERT INTO business_events
       (company_id, event_type, event_category, description, event_date,
        announcement_date, fact_or_inference, source_url, source_name, evidence, confidence)
       VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    (tonbo_id, "drhp_filed", "IPO",
     "Filed DRHP with SEBI for an Offer-for-Sale-only IPO of up to 1.81 crore shares (no fresh issue); "
     "not previously tracked in this database. No listing date confirmed as of this pass.",
     "2025-12-22", "2025-12-22", "FACT",
     "https://groww.in/blog/tonbo-imaging-india-files-drhp-with-sebi",
     "Groww / IndianStartupNews",
     "\"Bengaluru-based defence electronics maker Tonbo Imaging India files DRHP with SEBI for IPO\" -- "
     "OFS-only, up to 18,085,246 shares, filed Dec 22 2025",
     "HIGH"),
).lastrowid
conn.commit()
repo.open_trigger(conn, tonbo_id, "IPO", tonbo_event_id)

conn.execute(
    """INSERT INTO ipo_events
       (company_id, ipo_status, stage, ipo_size, source_url, evidence)
       VALUES (?,?,?,?,?,?)""",
    (tonbo_id, "IPO_REPORTED", "DRHP filed", "OFS of up to 1.81 Cr shares (no fresh issue)",
     "https://groww.in/blog/tonbo-imaging-india-files-drhp-with-sebi",
     "DRHP filed Dec 22 2025; no listing date yet as of this pass"),
)
conn.commit()

tonbo_contact_id = conn.execute(
    """INSERT INTO contacts (company_id, name, title, official_email_status, confidence, source_url)
       VALUES (?,?,?,?,?,?)""",
    (tonbo_id, "Arvind Lakshmikumar", "Founder & CEO", "OFFICIAL_EMAIL_NOT_FOUND", "HIGH",
     "https://tonboimaging.com/defense/aboutus/arvind/"),
).lastrowid
conn.commit()

tonbo_open_triggers = repo.open_trigger_count(conn, tonbo_id)
tonbo_result = scorer.score_opportunity(
    sub_scores={
        "business_event_strength": 0.65,
        "advertising_marketing_signal": 0.35,
        "timing_urgency": 0.45,
        "business_standard_audience_fit": 0.80,
        "estimated_marketing_capacity": 0.55,
        "decision_maker_availability": 0.65,
        "official_contact_availability": 0.20,
        "strategic_relevance": 0.65,
    },
    hq_status="BANGALORE_HQ_VERIFIED",
    open_trigger_count=tonbo_open_triggers,
    config=cfg,
)
repo.insert_opportunity(
    conn, tonbo_id,
    hq_status="BANGALORE_HQ_VERIFIED",
    primary_trigger="IPO",
    trigger_count=tonbo_open_triggers,
    score=tonbo_result["score"],
    classification=tonbo_result["classification"],
    timing="MEDIUM_TERM",
    why_now="DRHP was filed 8 months ago (Dec 2025) and is still pre-listing with no confirmed date -- "
            "newly discovered by BS today, not a fresh event, so timed as MEDIUM_TERM/watch rather than "
            "IMMEDIATE despite being a first-time find.",
    why_this_company="Tonbo Imaging, Bengaluru HQ verified. India's largest defence-optics OEM, OFS-only "
                      "IPO in progress.",
    business_problem="Pre-listing defence-tech company needs investor/business credibility; being newly "
                      "public will require sustained business-press visibility.",
    why_business_standard="Defence-tech IPO story fits BS's investor readership; founder has a strong, "
                           "citable public narrative (15-year defence-systems build, CNBC entrepreneur "
                           "award).",
    recommended_product="corporate_communication, thought_leadership, investor_visibility_content",
    recommended_contact_id=tonbo_contact_id,
    recommended_action="Pitch investor-visibility content ahead of a listing date announcement; monitor "
                        "Chittorgarh for the RHP/listing-date update before escalating urgency.",
    is_qualified_target=tonbo_result["is_qualified_target"],
    score_breakdown=tonbo_result["score_breakdown"],
)

conn.close()
print("Saint-Gobain:", sg_result)
print("Daimler India CV:", dicv_result)
print("Trivitron Healthcare:", trivitron_result)
print("Agnikul Cosmos:", agnikul_result)
print("Tonbo Imaging:", tonbo_result)
