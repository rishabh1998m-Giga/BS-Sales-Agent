#!/usr/bin/env python3
"""
EV vehicle/manufacturing watchlist sweep, 2026-08-29. Per user request:
research EV manufacturers and ecosystem players (batteries, charging/
swapping infrastructure) across Bangalore/Chennai/Hyderabad. Electric
two-wheelers/cars are a considered/higher-ticket B2C purchase; battery-
swap and rapid-charging infra players are B2B -- both pass the brand-fit
gate regardless of ticket size.

Ather Energy, Ultraviolette, Yulu, River Mobility, Pravaig Dynamics, and
Toyota Kirloskar Motor were already tracked before this pass -- not
re-added here, only pointer entries added to config/watchlist.yaml.

No comparably large, independent EV manufacturer headquartered in
Hyderabad was found in this pass -- honestly left out rather than padded
with a weak fit.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402

conn = repo.connect()

VERIFIED = [
    ("TVS Motor Company", "CHENNAI_HQ_VERIFIED", "Chennai",
     "CIN L35921TN1992PLC022845, Khader Nawaz Khan Road, Nungambakkam, Chennai 600006. Publicly "
     "listed, makes the TVS iQube e-scooter among other vehicles. LinkedIn ~781,304 followers.",
     "https://www.zaubacorp.com/TVS-MOTOR-COMPANY-LIMITED-L35921TN1992PLC022845"),
    ("Ola Electric Mobility", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "CIN L74999KA2017PLC099619, Koramangala, Bangalore 560095. E-scooter manufacturer, publicly "
     "listed (2024 IPO). LinkedIn ~644,101 followers.",
     "https://www.tofler.in/ola-electric-mobility-limited/company/L74999KA2017PLC099619"),
    ("SUN Mobility", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "CIN U35100KA2016PTC124376, Whitefield, Bangalore 560048. Battery-swapping infrastructure -- "
     "B2B, sells to fleet operators. LinkedIn ~152,700 followers.",
     "https://www.zaubacorp.com/company/SUN-MOBILITY-PRIVATE-LIMITED/U35100KA2016PTC124376"),
    ("Simple Energy", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Simpleenergy Pvt Ltd, CIN U29309KA2019PTC127859, Venkatala Village, Bangalore 560064. "
     "E-scooter manufacturer (Simple One). LinkedIn ~66,213 followers.",
     "https://www.thecompanycheck.com/company/simpleenergy-private-limited/U29309KA2019PTC127859"),
    ("Exponent Energy", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "CIN U34300KA2020PTC139964, Singasandra, Bangalore 560068. 15-minute rapid-charging tech for "
     "commercial EVs -- B2B. LinkedIn ~50,826 followers.",
     "https://www.zaubacorp.com/company/EXPONENT-ENERGY-PRIVATE-LIMITED/U34300KA2020PTC139964"),
    ("Bounce Infinity", "BANGALORE_HQ_VERIFIED", "Bengaluru",
     "Registered address JP Nagar 3rd Phase, Bangalore 560078 -- exact CIN not independently "
     "confirmed in this pass, MEDIUM confidence. E-scooters with removable batteries. LinkedIn "
     "~12,099 followers.",
     "https://www.linkedin.com/company/bounceinfinity"),
]

for name, hq_status, hq_city, evidence, source_url in VERIFIED:
    cid = repo.get_or_create_company(conn, name, industry="Electric vehicles/EV infrastructure")
    repo.set_hq_status(conn, cid, hq_status, claimed_city=hq_city, hq_city=hq_city,
                        evidence=evidence, source_url=source_url)

conn.close()
print(f"Verified {len(VERIFIED)} qualified EV/EV-infrastructure companies.")
