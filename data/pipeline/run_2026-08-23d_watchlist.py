#!/usr/bin/env python3
"""
Watchlist HQ-verification pass, 2026-08-23. Per direct instruction, the
user provided a standing list of client names to check (config/watchlist.yaml).
This pass verifies HQ status ONLY (companies + company_hq tables) -- no
triggers/opportunities are created here, since these companies were added
because the user wants them tracked, not because a specific news event was
found for each. Future runs will score them normally once/if a real
trigger shows up.

Policy clarified by the user: "headquartered" means the operational/
functional HQ (what the company itself calls its head office), not
strict legal CIN registration state. Several companies below are legally
registered in one state but operationally HQ'd in a qualified city
(Duroflex: registered Kerala, ops HQ Bangalore; Sattva Group: registered
Kolkata, ops HQ Bangalore; ClearTax/Defmacro: registered Delhi/Haryana,
ops HQ Bangalore) -- these qualify under the clarified rule. Evidence
notes the discrepancy honestly rather than hiding it.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402

conn = repo.connect()

# (name, hq_status, hq_city, evidence, source_url)
VERIFIED = [
    ("Razorpay", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Razorpay Software Pvt Ltd, 1st Floor, SJR Cyber, Laskar Hosur Road, Adugodi, Bangalore 560030 (CIN U72200KA2013PTC097389)",
     "https://www.zaubacorp.com/RAZORPAY-SOFTWARE-PRIVATE-LIMITED-U72200KA2013PTC097389"),
    ("Wakefit", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Wakefit Innovations Ltd, registered office Adugodi/Tavarekere, Bangalore 560029 (CIN U52590KA2016PLC086582)",
     "https://www.zaubacorp.com/WAKEFIT-INNOVATIONS-PRIVATE-LIMITED-U52590KA2016PTC086582"),
    ("Cashfree Payments", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Cashfree Payments India Pvt Ltd, Ecoworld, Bellandur, Bangalore 560103 (CIN U72900KA2015PTC082987)",
     "https://www.zaubacorp.com/CASHFREE-PAYMENTS-INDIA-PRIVATE-LIMITED-U72900KA2015PTC082987"),
    ("Ultraviolette", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Ultraviolette Automotive Pvt Ltd, Domlur, Bangalore 560071 (CIN U34102KA2015PTC084804)",
     "https://cleartax.in/f/company/ultraviolette-automotive-private-limited/U34102KA2015PTC084804/"),
    ("Sobha Ltd", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Sobha Ltd, Sarjapur-Marathahalli ORR, Bellandur, Bangalore 560103 (CIN L45201KA1995PLC018475)",
     "https://www.zaubacorp.com/SOBHA-LIMITED-L45201KA1995PLC018475"),
    ("Canara Bank", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Public sector bank, Head Office 112 J C Road, Bengaluru 560002",
     "https://en.wikipedia.org/wiki/Canara_Bank"),
    ("Ujjivan Small Finance Bank", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Grape Garden, Koramangala, Bangalore 560095 (CIN L65110KA2016PLC142162)",
     "https://tracxn.com/d/legal-entities/india/ujjivan-small-finance-bank-limited/__8vSWvoINTgQu99Pd9gRFowePXfr0L1tdCUDwvDvC2YU"),
    ("Jana Small Finance Bank", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "The Fairway Business Park, Domlur, Bangalore 560071 (CIN L65923KA2006PLC040028)",
     "https://en.wikipedia.org/wiki/Jana_Small_Finance_Bank"),
    ("Prestige Group", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Prestige Estates Projects Ltd, Prestige Falcon Tower, Brunton Road, Bangalore 560025 (CIN L07010KA1997PLC022322)",
     "https://www.zaubacorp.com/PRESTIGE-ESTATES-PROJECTS-LIMITED-L07010KA1997PLC022322"),
    ("Puravankara", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Puravankara Ltd, Ulsoor Road, Bangalore 560042 (CIN L45200KA1986PLC051571)",
     "https://www.zaubacorp.com/company/PURAVANKARA-LIMITED/L45200KA1986PLC051571"),
    ("Toyota Kirloskar Motor", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Plot No.1, Bidadi Industrial Area, Bangalore Rural District (CIN U34101KA1997PTC022858)",
     "https://en.wikipedia.org/wiki/Toyota_Kirloskar_Motor"),
    ("Fisdom", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Finwizard Technology Pvt Ltd, St Marks Road, Bangalore 560001 (CIN U74900KA2015PTC080747)",
     "https://fisdom.com/"),
    ("Stable Money", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Stable Finserv Pvt Ltd, Bhive HSR Premium Campus, Bangalore 560068 (CIN U66309KA2023PTC172771)",
     "https://stablemoney.in/"),
    ("Jiraaf", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Jiraaf Platform Pvt Ltd, Koramangala, Bangalore 560034 (CIN U72900KA2021PTC149273)",
     "https://www.jiraaf.com/"),
    ("Nambiar Builders", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Nambiar Builders Pvt Ltd, Kadubisanahalli, Bangalore 560103 (CIN U45201KA2009PTC050747)",
     "https://nambiarbuilders.com/"),
    ("DS Max Properties", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "DS-Max Properties Pvt Ltd, HBR Layout, Bangalore 560043 (CIN U70102KA2007PTC041508)",
     "https://www.zaubacorp.com/DS-MAX-PROPERTIES-PRIVATE-LIMITED-U70102KA2007PTC041508"),
    ("Evolve Back", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Orange County Resorts & Hotels Ltd (brand: Evolve Back), Richmond Road, Bangalore 560025 (CIN U55101KA2001PLC029232)",
     "https://tracxn.com/d/legal-entities/india/orange-county-resorts-hotels-limited/___iU-S0xe-mwFBiWdh98C177vxP2UE6epNPu2SdPuG3c"),
    ("IBM", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "International company -- India HQ verified: IBM India Pvt Ltd, Bannerghatta Road, Bangalore 560029 (CIN U72200KA1997PTC022382)",
     "https://www.zaubacorp.com/IBM-INDIA-PRIVATE-LIMITED-U72200KA1997PTC022382"),
    ("OnePlus", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "International company -- India HQ verified: OnePlus Technology India Pvt Ltd, UB City, Bangalore 560001 (CIN U74990KA2020FTC139455)",
     "https://www.zaubacorp.com/company/ONEPLUS-TECHNOLOGY-INDIA-PRIVATE-LIMITED/U74990KA2020FTC139455"),
    ("Dell", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "International company -- India HQ verified: Dell International Services India Pvt Ltd, Embassy Golf Links, Domlur, Bangalore 560071 (CIN U74999KA1996FTC055568)",
     "https://www.indiafilings.com/search/dell-international-services-india-private-limited-cin-U74999KA1996FTC055568"),
    ("Kyndryl", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "International company -- India HQ verified: Kyndryl Solutions Pvt Ltd, Embassy Golf Links, Domlur, Bangalore 560071 (CIN U72900KA2021PTC142940)",
     "https://tracxn.com/d/legal-entities/india/kyndryl-solutions-private-limited/__MTt6pUwtC22iNelx9GGkl4Soww06pBND4mhgNMksDeM"),
    ("Acer", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "International company -- India HQ verified: Acer India Pvt Ltd, Magrath Road, Bangalore 560025 (CIN U31909KA1999PTC025698)",
     "https://www.zaubacorp.com/ACER-INDIA-PRIVATE-LIMITED-U31909KA1999PTC025698"),
    ("Duroflex", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Operational/corporate HQ is HSR Layout, Bangalore 560068, per company's own investor-relations materials -- NOTE: legal registered office is technically Alappuzha, Kerala (CIN U36104KL1981PLC003447); qualifies under the operational-HQ rule the user confirmed, not the strict CIN-registration state.",
     "https://www.duroflexworld.com/pages/investors-relations"),
    ("Sattva Group", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Corporate office at Salarpuria Windsor, Ulsoor Road, Bangalore 560042, per the company's own site -- NOTE: Sattva Developers Pvt Ltd's legal registered office is technically Kolkata (CIN U70101WB2004PTC097736); qualifies under the operational-HQ rule.",
     "https://sattvagroup.com/our-journey/corporate-overview/"),
    ("ClearTax", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Corporate office at AMR Tech Park, Hosur Road, Hongasandra, Bangalore 560068, widely cited as ClearTax HQ -- NOTE: the legal entity Defmacro Software Pvt Ltd's registered office is technically Delhi/Haryana; qualifies under the operational-HQ rule.",
     "https://www.clear.in/s/legal"),
    ("Assetz Property Group", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Assetz House, Crescent Road, Bengaluru 560001 (CIN U70100KA2003PTC032616) -- registered AND operational HQ both Bangalore, no discrepancy",
     "https://cleartax.in/f/company/assetz-property-management-services-private-limited/U70100KA2003PTC032616/"),
    ("Shriram Properties", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Company's own materials describe Shriram House, T Chowdaiah Road, Bengaluru 560080 as its corporate headquarters (CIN L72200TN2000PLC044560 shows legal registration in Chennai -- also a qualified city either way)",
     "https://www.bseindia.com/xml-data/corpfiling/AttachHis/bfbd7eaa-ab05-44bc-9b42-719b59ee49c3.pdf"),
    ("Mudrex", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "HSR Layout, Bangalore 560102, per company/directory listings -- MEDIUM confidence, exact CIN not independently confirmed in this pass",
     "https://mudrex.com/about-us"),
    ("Sify", "CHENNAI_HQ_VERIFIED", "Chennai",
     "Sify Technologies Ltd, Tidel Park, Taramani, Chennai 600113 (CIN U72200TN1995PLC050809)",
     "https://www.indiafilings.com/search/sify-technologies-limited-cin-U72200TN1995PLC050809"),
    ("Sundaram Mutual Fund", "CHENNAI_HQ_VERIFIED", "Chennai",
     "Sundaram Asset Management Company Ltd, Sundaram Towers, Whites Road, Chennai 600014; registered office Patullos Road, Chennai 600002",
     "https://www.sundarammutual.com/About"),
    ("Guidewire", "CHENNAI_HQ_VERIFIED", "Chennai",
     "International company -- India HQ verified: Guidewire Software Solutions India Pvt Ltd, MGR Road, Perungudi, Chennai 600096 (CIN U72900TN2015PTC099051); note significant Bengaluru engineering office also exists but registered/legal India entity is Chennai",
     "https://www.zaubacorp.com/GUIDEWIRE-SOFTWARE-SOLUTIONS-INDIA-PRIVATE-LIMITED-U72900TN2015PTC099051"),
    ("Saint-Gobain", "CHENNAI_HQ_VERIFIED", "Chennai",
     "International company -- India HQ verified: Saint-Gobain India Pvt Ltd, Sigapi Achi Building, Egmore, Chennai 600008 (CIN U26109TN1997PTC037875)",
     "https://www.zaubacorp.com/SAINT-GOBAIN-INDIA-PRIVATE-LIMITED-U26109TN1997PTC037875"),
]

NON_QUALIFIED = [
    ("Delhivery", "Registered office New Delhi; corporate/operational HQ Gurugram, Haryana (CIN L63090DL2011PLC221234) -- neither is a qualified city",
     "https://en.wikipedia.org/wiki/Delhivery"),
    ("Adobe", "International company -- India HQ is Noida, UP (\"Adobe's largest hub in India and acts as the company's headquarters in the country\" per Adobe's own newsroom); Bengaluru office exists but is engineering-focused, not the India HQ",
     "https://news.adobe.com/en/apac/news/2026/04/adobe-opens-new-noida-office-expanding-investment-in-india-innovation"),
    ("IKEA", "International company -- India HQ (IKEA India Pvt Ltd registered office) is Gurgaon, Haryana; Bengaluru presence is a business-support office only, not the India HQ",
     "https://www.indiafilings.com/search/ikea-india-private-limited-cin-U52399DL2013FTC256222"),
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
