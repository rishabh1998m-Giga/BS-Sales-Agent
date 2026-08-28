#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-08-28 daily-sales-brief run --
first automatic firing of the new self-bound trigger (trig_016bfNkuSgZaguWS9QCc9uv2),
resuming this session directly at 04:36 UTC / 10:06 AM IST. Worked as intended:
no separate fresh session, no missing commit -- this run picks up exactly
where the last several manual in-session runs left off.

No new qualified opportunity to score today. This run's contribution is
watchlist resolution:
  - Seiko: RESOLVED to verified_qualified. Seiko Watch India Pvt Ltd,
    registered office Bangalore (CIN U33301KA2007FTC041898). Luxury
    watches are a considered/higher-ticket purchase (same reasoning as
    the Lexus example in config/target-criteria.yaml), so this also
    passes the brand-fit gate -- no fresh trigger found for them today,
    but they're now a fully qualified company to watch going forward.
  - Movado: re-checked, still unresolved. No dedicated Movado India
    entity/CIN found (unlike Seiko, likely distributed via multi-brand
    retail rather than a wholly-owned subsidiary) -- left unverified
    rather than guessed.

Checked and deliberately excluded/deferred:
  - Asaya (D2C skincare, Rs 88 Cr Series A) -- widely reported as
    "Bengaluru-based" but its actual registered office is Ranchi,
    Jharkhand, not a qualified city; also a routine-repeat-purchase
    skincare brand, which would fail the brand-fit gate even if the city
    matched. Two independent reasons to exclude, both recorded here
    rather than trusting the casual "Bengaluru-based" framing in press
    coverage.
  - WATER (Hyderabad physical-AI startup, $2.5M seed) -- checked a third
    time (now with founder names) across two days' worth of passes; still
    no registered-office/CIN found. Not fabricated, left for a future
    pass if it surfaces again with more concrete company-registration
    detail.
  - Guidehouse's Hyderabad hub, Third Wave Coffee, Airbound, Chittorgarh
    DRHP list -- all already covered/resolved in the 2026-08-25/26/27
    passes; nothing new found on any of them today.

Industry-movement (Exchange4Media/afaqs!) and decision-maker movement
checks: no qualifying finding today.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import repo  # noqa: E402

conn = repo.connect()

seiko_id = repo.get_or_create_company(conn, "Seiko Watch India", industry="Luxury watches/retail")
repo.set_hq_status(
    conn, seiko_id, "BANGALORE_HQ_VERIFIED",
    claimed_city="Bengaluru", hq_city="Bengaluru",
    evidence="Seiko Watch India Pvt Ltd, registered office Temple Vista, Sri Krishna Temple Road, "
             "Indiranagar 1st Stage, Bangalore 560038 (CIN U33301KA2007FTC041898), subsidiary of a "
             "foreign company, ROC Bangalore.",
    source_url="https://www.zaubacorp.com/company/Seiko-Watch-India-Private-Limited/U33301KA2007FTC041898",
)
# No opportunity scored -- no fresh business event/trigger found for Seiko today. HQ verification
# recorded so they're a fully qualified company to watch on future passes.

conn.close()
print("No new opportunities scored today. Watchlist resolved: Seiko -> verified_qualified.")
