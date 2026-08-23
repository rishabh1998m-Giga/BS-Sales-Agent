================================
BUSINESS STANDARD
CLIENT INTELLIGENCE
2026-08-23
================================

## 1. TOP 10 NEW SALES OPPORTUNITIES

- **CRED** — score 84 (HOT, IMMEDIATE) — trigger: PRODUCT_LAUNCH
- **PhonePe** — score 73 (WARM, MEDIUM_TERM) — trigger: IPO
- **Navi Technologies** — score 73 (WARM, IMMEDIATE) — trigger: FUNDRAISING
- **Ather Energy** — score 73 (WARM, IMMEDIATE) — trigger: PRODUCT_LAUNCH
- **Table Space Technologies** — score 64 (WARM, NEAR_TERM) — trigger: IPO
- **Yulu** — score 64 (WARM, NEAR_TERM) — trigger: FUNDRAISING
- **River Mobility** — score 64 (WARM, NEAR_TERM) — trigger: FUNDRAISING
- **Rapido** — score 48 (WATCH, WATCH) — trigger: FUNDRAISING

## 2. BANGALORE-HQ COMPANIES WITH NEW BUSINESS TRIGGERS

- Ather Energy — PRODUCT_LAUNCH
- Yulu — FUNDRAISING
- River Mobility — FUNDRAISING
- CRED — PRODUCT_LAUNCH
- Navi Technologies — FUNDRAISING
- Navi Technologies — IPO
- Table Space Technologies — IPO
- PhonePe — IPO
- CRED — MAJOR_PARTNERSHIP
- CRED — FUNDRAISING
- Rapido — FUNDRAISING

## 3. IPO OPPORTUNITIES

- Table Space Technologies — ipo_status=IPO_REPORTED, stage=DRHP filed
- PhonePe — ipo_status=IPO_REPORTED, stage=SEBI approved, updated DRHP filed, expected_timeline=Not yet announced
- Groww (Billionbrains Garage Ventures) — ipo_status=IPO_CONFIRMED, stage=Listed

## 4. FUNDRAISING OPPORTUNITIES

- Yulu — stage=Series C, amount=$93 million ($63M equity + $30M debt), date_announced=2026-08-12
- River Mobility — stage=Series C, amount=$120 million, date_announced=2026-08-06
- Navi Technologies — stage=Strategic/Growth, amount=$100 million, date_announced=2026-08-19
- CRED — stage=Strategic investment, amount=$900M (~Rs 7,500 Cr), date_announced=2026-06-22
- Rapido — stage=Growth capital, amount=$240M, date_announced=2026-05-15

## 5. PRODUCT LAUNCHES

- Ather Energy — product_name=EL01 (EL platform), launch_date=2026-08-29
- CRED — product_name=Circle by CRED, launch_date=2026-08-18

## 6. NEW MARKETING INITIATIVES

_None yet._

## 7. EXPANSION OPPORTUNITIES

_None yet._

## 8. NEW MARKETING LEADERS

- CRED — Miten Sampat (Interim CEO), 2026-06-22
- PhonePe — Amit Doshi (Group Chief Marketing Officer), 2025-03-07

## 9. COMPETITOR ADVERTISING

_None yet._

## 10. COMPETITOR LEAKAGE

_None yet._

## 11. MULTI-TRIGGER OPPORTUNITIES

- CRED — 3 open triggers, score 84

## 12. FOLLOW-UPS DUE

_None due._

## 13. TODAY'S TOP 5 ACTIONS

1. **CRED** (score 84, HOT) — Pitch Circle launch coverage + a leadership Q&A with Miten Sampat (now confirmed as interim CEO) before the beta window closes.
2. **PhonePe** (score 73, WARM) — Pitch pre-IPO corporate visibility package to Amit Doshi (Group CMO, ex-Britannia, hired specifically for IPO-era brand building) -- CONFIRM official email before outreach, none found publicly.
3. **Navi Technologies** (score 73, WARM) — Pitch investor-visibility content tied to the Prosus round; confirm the IPO timeline independently before leading with it (currently INFERENCE-tier only).
4. **Ather Energy** (score 73, WARM) — Pitch pre-launch coverage now, ahead of the Aug 29 Community Day event -- the window closes once the launch itself generates its own news cycle.
5. **Table Space Technologies** (score 64, WARM) — Pitch pre-IPO corporate-communication package to Co-CEO Karan Chopra; a CMO name (Megha Agarwal, per one directory listing) surfaced but is unverified - confirm the current marketing lead before including them in outreach.

## Companies checked before adding new ones (per this run's instruction to avoid duplicates)

Before researching new companies, the companies table was queried directly. It held 7 rows going into
this pass — **PhonePe, CRED, Rapido, Groww, Meesho** (2026-08-21 seed) plus **Navi Technologies** and
**Table Space Technologies** (added earlier today). Ather Energy, Myntra, and BigBasket were NOT in the
table, and a check of `data/seed_2026-08-21.py` (the only script that ever populated the 2026-08-21
baseline) confirms they were never seeded here — there is no record of them anywhere in this repo's
git history. Ather Energy is newly added by this pass (see below); Myntra and BigBasket were not
researched this run and remain untracked. If a "list of 8" including Myntra/BigBasket exists, it isn't
this database — worth reconciling with whatever tracked that before assuming continuity with this
repo's history.

## Competitor-advertising sweep (Sections 9-10) — genuine null result

Checked all 8 publishers in `config/publishers.yaml` (Economic Times, Times of India, Moneycontrol,
Mint, CNBC-TV18, Financial Express, BusinessLine, Deccan Herald) for paid placements by the now 10
tracked Bangalore-HQ companies. Found general marketing-spend disclosures (PhonePe: Rs 455 Cr
marketing spend H1 FY26; Meesho: Rs 227 Cr digital ad spend Q1 FY26) but **no dated, sourced evidence
of a specific ad placement on any of the 8 named publishers for any tracked company**. This is a real
negative result, not an uncovered gap — nothing was inserted into `campaigns`/`competitor_activity`
because there is no verifiable record to cite. Caveat: open web search does not reliably surface
publisher-level ad placements (publishers don't typically publish "we sold this ad" case studies); a
conclusive sweep would need the publishers' own media-sales records or a paid ad-intelligence tool
(e.g. Pathmatics, MediaRadar) — neither is available in this environment. Treat Sections 9-10 as
"checked, nothing found" rather than "not checked."

## What this run did NOT cover

- **The `.claude/skills` orchestration this project was designed around still doesn't exist anywhere
  reachable** — same caveat as the 2026-08-23 first pass: this report was produced by following
  `docs/master-spec.md` directly, not by a tested `hq-verification` / `opportunity-scoring` /
  `sales-opportunity-analysis` skill.
- **Sections 6-7 (marketing initiatives, expansion)** — still empty; no dedicated search pass this run.
- **Chennai/Hyderabad market intelligence** — out of scope (Bangalore-only per primary territory).
- Foreign companies opening NEW offices *in* Bangalore this run (OpenAI, Anthropic, Google/Alphabet)
  were deliberately excluded from the qualified list — their headquarters are not in Bangalore, so
  they fail the hard gate regardless of the size of their Bangalore investment.
- **No official email found** for any new contact this run (Tarun Mehta, Amit Gupta, Aravind Mani) —
  confirm a channel before outreach.
