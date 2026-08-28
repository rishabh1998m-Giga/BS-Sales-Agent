#!/usr/bin/env python3
"""
Aerospace/aviation/defense-manufacturing watchlist sweep, 2026-08-28. Per
user request: find LARGE, established companies in this sector across the
3 qualified cities, using LinkedIn follower count as a spending-capability
proxy (first pass: 20-30k+ requested; second pass, this file: specifically
also covers the 10k-30k band). All are B2B (government/enterprise defense,
aerospace, and space-tech manufacturers/suppliers) -- qualify under the
brand-fit gate regardless of ticket size.

Skyroot Aerospace, Garuda Aerospace, Agnikul Cosmos, and Tonbo Imaging were
already tracked before this pass (2026-08-23/25/26 runs) -- not re-added
here, only pointer entries added to config/watchlist.yaml.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402

conn = repo.connect()

VERIFIED = [
    ("Hindustan Aeronautics Limited (HAL)", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "PSU, CIN L35301KA1963GOI001622, 15/1 Cubbon Road, Bangalore 560001. India's largest aerospace "
     "manufacturer (fighter jets, helicopters). LinkedIn ~94,400 followers.",
     "https://www.zaubacorp.com/company/HINDUSTAN-AERONAUTICS-LIMITED/L35301KA1963GOI001622"),
    ("Bharat Electronics Limited (BEL)", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "PSU, CIN L32309KA1954GOI000787, Outer Ring Road, Nagavara, Bangalore 560045. Defense "
     "electronics/radar/avionics. LinkedIn ~45,570 followers, ~8,844 employees (Mar 2025).",
     "https://www.zaubacorp.com/BHARAT-ELECTRONICS-LIMITED-L32309KA1954GOI000787"),
    ("Bellatrix Aerospace", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "CIN U35300KA2015PTC078701, Sankey Road, Seshadripuram, Bangalore 560020 (company's own contact "
     "page + directory listings agree). Satellite propulsion systems. LinkedIn ~100,176 followers.",
     "https://bellatrix.aero/contact"),
    ("Pixxel", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Pixxelspace India Pvt Ltd, CIN U74999KA2019FTC122792, Indiranagar, Bangalore. Earth-imaging "
     "satellite constellation. LinkedIn ~43,867 followers, 314 employees.",
     "https://www.zaubacorp.com/PIXXELSPACE-INDIA-PRIVATE-LIMITED-U74999KA2019FTC122792"),
    ("Skylark Drones", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "CIN U29253KA2015PTC183331, HSR Layout, Bangalore 560102. Enterprise drone data/mapping/"
     "analytics. LinkedIn ~40,236 followers.",
     "https://www.zaubacorp.com/SKYLARK-DRONES-PRIVATE-LIMITED-U29253KA2015PTC183331"),
    ("Dhruva Space", "HYDERABAD_HQ_VERIFIED", "Hyderabad",
     "CIN U74900TG2012PTC150151, Begumpet, Hyderabad 500016. Satellite manufacturing/space "
     "infrastructure. LinkedIn ~54,775 followers.",
     "https://www.zaubacorp.com/DHRUVA-SPACE-PRIVATE-LIMITED-U74900TG2012PTC150151"),
    ("Zen Technologies", "HYDERABAD_HQ_VERIFIED", "Hyderabad",
     "CIN L72200TG1993PLC015939, Sanathnagar Industrial Estate, Hyderabad 500018. Publicly listed "
     "defense training simulators and anti-drone systems. LinkedIn ~75,355 followers.",
     "https://www.zaubacorp.com/ZEN-TECHNOLOGIES-LIMITED-L72200TG1993PLC015939"),
    ("Data Patterns (India) Ltd", "CHENNAI_HQ_VERIFIED", "Chennai",
     "CIN L72200TN1998PLC061236, SIPCOT IT Park, Siruseri (Chennai OMR IT corridor). Publicly listed "
     "defense/aerospace electronics. LinkedIn ~25,262 followers.",
     "https://www.datapatternsindia.com/contact.php"),
    ("Marut Drones (Marut Dronetech)", "HYDERABAD_HQ_VERIFIED", "Hyderabad",
     "CIN U74999TG2019PTC132342, T-Hub, IIIT Gachibowli, Hyderabad 500032. Industrial/agri drone "
     "manufacturer. LinkedIn ~14,768 followers.",
     "https://www.zaubacorp.com/MARUT-DRONETECH-PRIVATE-LIMITED-U74999TG2019PTC132342"),
    ("MTAR Technologies", "HYDERABAD_HQ_VERIFIED", "Hyderabad",
     "Publicly listed precision manufacturer for aerospace/defense/nuclear/clean-energy, HQ Hyderabad "
     "per company materials -- CIN not independently confirmed in this pass, MEDIUM confidence. "
     "LinkedIn ~13,441 followers.",
     "https://www.mtarusa.com/"),
    ("Alpha Design Technologies", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Defense electronics/avionics manufacturer, registered office Bangalore per directory listings "
     "-- CIN not independently confirmed in this pass, MEDIUM confidence. LinkedIn ~11,866 followers.",
     "https://in.linkedin.com/company/alpha-design-technologies"),
]

for name, hq_status, hq_city, evidence, source_url in VERIFIED:
    cid = repo.get_or_create_company(conn, name, industry="Aerospace/defense/space manufacturing")
    repo.set_hq_status(conn, cid, hq_status, claimed_city=hq_city, hq_city=hq_city,
                        evidence=evidence, source_url=source_url)

conn.close()
print(f"Verified {len(VERIFIED)} qualified aerospace/defense companies.")
