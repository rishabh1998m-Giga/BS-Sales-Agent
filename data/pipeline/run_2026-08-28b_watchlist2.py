#!/usr/bin/env python3
"""
Second watchlist batch, 2026-08-28. User pasted 30 lines of company names
with duplicates (within the paste, and against the existing 44-name
watchlist from 2026-08-23). After dedup, 17 were genuinely new; of those,
15 are HQ-verified here as new companies (Agnikul Cosmos and Airbound
Aerospace were already tracked from the 2026-08-25/26 daily runs, so only
config/watchlist.yaml got a pointer entry for them, no DB re-add needed).

Per the operational/functional-HQ rule the user confirmed on 2026-08-23:
Kurlon, Titan, and Pravaig Dynamics all have a registered office outside
the 3 qualified cities but a clear, well-evidenced operational/corporate
HQ inside one -- same pattern as Duroflex/Sattva/ClearTax. Sleepyhead
(a Sheela Foam brand, no separate Bangalore entity) is the one exclusion
in this batch -- HQ genuinely outside the qualified cities either way.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402

conn = repo.connect()

VERIFIED = [
    ("Kurlon", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Kurlon Limited, Manipal Centre, Dickenson Road, Bangalore (CIN U17214KA1962PLC001443) -- the "
     "original brand entity, still Bangalore-registered. NOTE: Sheela Foam Ltd separately acquired "
     "94.66% of a related entity, 'Kurlon Enterprise Limited' (Mumbai-registered, CIN "
     "U36101MH2011PLC222657), in 2023 -- that acquiring entity is not Bangalore-based, but Kurlon "
     "Limited itself remains so.",
     "https://www.zaubacorp.com/company/KURLON-LIMITED/U17214KA1962PLC001443"),
    ("Perfios", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Perfios Software Solutions Pvt Ltd, Adugodi, Bangalore 560030 (CIN U72200KA2008PTC046602)",
     "https://cleartax.in/f/company/perfios-software-solutions-private-limited/U72200KA2008PTC046602/"),
    ("Titan", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Corporate/operational HQ is Electronic City, Bangalore per Titan's own investor materials -- "
     "NOTE: legal registered office is technically Hosur, Tamil Nadu (CIN L74999TZ1984PLC001456), "
     "not one of the 3 qualified cities itself. Qualifies under the operational-HQ rule.",
     "https://www.titancompany.in/contact-us"),
    ("Scripbox", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Scripbox.com India Pvt Ltd, Old Airport Road, Bangalore 560008 (CIN U74900KA2012PTC062020)",
     "https://cleartax.in/f/company/scripbox-com-india-private-limited/U74900KA2012PTC062020/"),
    ("MoneyView", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Moneyview Limited, Marathahalli, Bangalore 560103 (CIN U72200KA2014PLC075775)",
     "https://www.thecompanycheck.com/company/moneyview-limited/U72200KA2014PLC075775"),
    ("Pravaig Dynamics", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Operational HQ / manufacturing hub at the Defense and Aerospace Park, Bangalore, per the "
     "company's own social/media presence -- NOTE: legal registered office is technically New Delhi "
     "(CIN U34100DL2019PTC351262). Qualifies under the operational-HQ rule.",
     "https://www.pravaig.com/company"),
    ("TVS Emerald", "CHENNAI_HQ_VERIFIED", "Chennai",
     "TVS Emerald Ltd (formerly Emerald Haven Realty Ltd), Ispahani Centre, Nungambakkam High Road, "
     "Chennai 600034 (CIN U45200TN2010PLC075953)",
     "https://www.falconebiz.com/company/TVS-EMERALD-LIMITED-U45200TN2010PLC075953"),
    ("Sumadhura", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Sumadhura Infracon Pvt Ltd, Marathahalli, Bangalore 560037 (CIN U45200KA2012PTC062071)",
     "https://www.zaubacorp.com/SUMADHURA-INFRACON-PRIVATE-LIMITED-U45200KA2012PTC062071"),
    ("Embassy Group", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Embassy Property Developments Pvt Ltd, Infantry Road, Bangalore 560001 (CIN "
     "U85110KA1996PTC020897)",
     "https://cleartax.in/f/company/embassy-property-developments-private-limited/U85110KA1996PTC020897/"),
    ("Total Environment", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Total Environment Projects (India) Pvt Ltd, Whitefield, Bangalore 560066 (CIN "
     "U70102KA2006PTC040793)",
     "https://www.zaubacorp.com/TOTAL-ENVIRONMENT-PROJECTS-INDIA-PRIVATE-LIMITED-U70102KA2006PTC040793"),
    ("Century Real Estate", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Century Real Estate Holdings Pvt Ltd, Palace Road, Bangalore 560052 (CIN "
     "U70101KA2007PTC042078)",
     "https://www.zaubacorp.com/CENTURY-REAL-ESTATE-HOLDINGS-PRIVATE-LIMITED-U70101KA2007PTC042078"),
    ("Concorde Group", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Concorde Housing Corporation Pvt Ltd, registered at RoC-Bangalore (CIN U70102KA2008PTC046886)",
     "https://www.zaubacorp.com/CONCORDE-HOUSING-CORPORATION-PRIVATE-LIMITED-U70102KA2008PTC046886"),
    ("Madchatter Brand Solutions", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Madchatter Brand Solutions Pvt Ltd, Bangalore (CIN U74999KA2022PTC165286) -- a PR/branding "
     "agency, tracked for industry-movement relevance rather than as a direct ad-sales prospect.",
     "https://www.zaubacorp.com/MADCHATTER-BRAND-SOLUTIONS-PRIVATE-LIMITED-U74999KA2022PTC165286"),
    ("The ePlane Company", "CHENNAI_HQ_VERIFIED", "Chennai",
     "Legal entity Ubifly Technologies Pvt Ltd, IIT Madras Research Park, Taramani, Chennai 600113. "
     "CIN not independently confirmed in this pass -- MEDIUM confidence on entity name, HIGH on "
     "Chennai location (company's own site + multiple press sources).",
     "https://www.eplane.ai/about/"),
    ("Sarla Aviation", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Bengaluru HQ per Wikipedia, the company's own 'New Bengaluru HQ' announcement, and Tracxn. CIN "
     "not independently confirmed in this pass -- MEDIUM confidence.",
     "https://en.wikipedia.org/wiki/Sarla_Aviation"),
    ("BluJ Aerospace", "HYDERABAD_HQ_VERIFIED", "Hyderabad",
     "Hyderabad-based per TechTimes coverage of its Gen 2 heavy-lift eVTOL prototype. CIN not "
     "independently confirmed in this pass -- MEDIUM confidence.",
     "https://www.techtimes.com/articles/323848/20260810/dgca-grants-sarla-aviation-first-evtol-design-approval-under-indias-2024-air-taxi-framework.htm"),
]

NON_QUALIFIED = [
    ("Sleepyhead", "Brand of Sheela Foam Ltd -- registered office Mumbai (CIN L74899MH1971PLC427835), "
     "operational HQ Noida, UP. Unlike Kurlon, no separate Bangalore-registered entity exists for "
     "this brand.",
     "https://en.wikipedia.org/wiki/Sheela_Foam_Limited"),
]

for name, hq_status, hq_city, evidence, source_url in VERIFIED:
    cid = repo.get_or_create_company(conn, name)
    repo.set_hq_status(conn, cid, hq_status, claimed_city=hq_city, hq_city=hq_city,
                        evidence=evidence, source_url=source_url)

for name, evidence, source_url in NON_QUALIFIED:
    cid = repo.get_or_create_company(conn, name)
    repo.set_hq_status(conn, cid, "NON_QUALIFIED_HQ_VERIFIED", evidence=evidence, source_url=source_url)

conn.close()
print(f"Verified {len(VERIFIED)} qualified, {len(NON_QUALIFIED)} confirmed non-qualified.")
