#!/usr/bin/env python3
"""
One-off data-entry script for the 2026-10-30 daily-sales-brief run
(Friday -- also run generate_weekly_report.py). Self-bound 1:30 AM IST
trigger.

No new qualified opportunity found today. Checked and declined:
  - Jagruti Rehabilitation Centre (Rs 28 Cr Series A led by Alkemi
    Growth Capital, its first institutional round) -- HQ is Pune
    (founded there 2008), not a qualified city.
  - Coratia Technologies (underwater robotics, Navy supplier, Rs 18 Cr
    bridge/extension round led by MGF Kavachh) -- HQ is Rourkela,
    Odisha (NIT Rourkela campus address, CIN U72900OR2021PTC038315),
    not a qualified city.
  - Gramiyaa (Bengaluru, cold-pressed cooking-oil D2C brand, Rs 18.65
    Cr Series A at a reported Rs 110 Cr valuation) -- Bengaluru HQ
    plausible, but the announcement itself dates to Oct 10 2026 (20
    days old, inside the previously-documented session-dormancy gap,
    not fresh); separately, cold-pressed cooking oil is a routine
    grocery/FMCG product -- low-ticket, mass-market, fails brand-fit
    regardless of HQ or freshness, same reasoning as excluding
    Britannia/Third Wave Coffee.
  - Amaha (mental healthcare provider, $3M round per a single
    secondary aggregator citing Economic Times, round-stage label
    inconsistent between "Pre-Series A" and "Seed") -- HQ genuinely
    conflicting: older/Tracxn sources and its 2024 Series A coverage
    describe it as Mumbai-based (company was founded there as
    InnerHour in 2016), while one 2025 Entrackr piece alone calls it
    Bengaluru-based. Weak single-aggregator sourcing plus HQ
    ambiguity -- left unscored rather than assumed.
  - Famous Innovations appointing Senthil Kumar as Managing Partner
    and CCO, Bengaluru -- Famous Innovations is an advertising agency,
    not a brand/advertiser; an agency's own internal leadership hire
    is not a Section 8 (client marketing-leader) trigger, same
    reasoning as excluding Finnpartners from direct ad-sales scoring.

Also checked: Chittorgarh (M.K.Sons Fine Jewels/SFC Environmental/BLS
Polymers IPOs mid-cycle, Jio Platforms/Paras Healthcare already listed
-- none in a newly-qualified city), industry movement via afaqs!/
Storyboard18 (Lodestar UM winning AMFI's Rs 600 Cr media account is
undated and not tied to any of the three qualified cities; WeWork
India leasing story and RMAI FLAME Awards resurfaced again with no new
detail).

Honest "none found" rather than padded.
"""
print("2026-10-30: no new qualified opportunity found. See docstring for what was checked.")
