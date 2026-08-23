# Business Standard Sales Intelligence Agent — Master Specification

Owner: Boss (Business Standard, Digital Ad Sales)
Primary qualification market: **Bangalore (Bengaluru) headquarters only**
Market-intelligence-only cities: Chennai, Hyderabad

## 1. Core objective

Every day, answer: **"Which Bangalore-headquartered companies should I
approach today, and WHY?"**

Opportunities are discovered from many trigger types, not just competitor
advertising: IPO activity/filings, fundraising, product/brand launches,
marketing campaigns, partnerships, business/geographic expansion, new
offices/plants/stores, M&A, leadership appointments, financial results,
business milestones, events/sponsorships, hiring campaigns, new platforms,
rebranding, government contracts/tenders, international expansion, tech
launches, CSR, consumer/reputation campaigns, and any other credible
event that may create an advertising opportunity.

## 2. Critical regional HQ rule (hard gate)

A company qualifies for the Bangalore opportunity list **only** if its
headquarters — not office, not branch, not founder residence, not
campaign geography — is in Bangalore. Statuses:
`BANGALORE_HQ_VERIFIED`, `NON_BANGALORE_HQ_VERIFIED`, `HQ_UNVERIFIED`.
Only the first appears in the qualified list; uncertain cases go to the
`HQ_VERIFICATION_QUEUE` and are never assumed. See
`.claude/skills/hq-verification/SKILL.md` for the enforcement mechanism.

## 3. Target cities

Bangalore is the primary sales territory. Chennai and Hyderabad are
researchable as separate market intelligence but never auto-promoted into
the Bangalore qualified list.

## 4-13. Intelligence engines

Each of the following has a dedicated skill under `.claude/skills/`
(see that file for exact capture schema, sources, and process):
client-intelligence, ipo-intelligence, funding-intelligence,
product-launch-intelligence, marketing-intelligence,
expansion-intelligence, revenue-intelligence (financial events),
leadership-intelligence, competitor-intelligence (incl. competitor
leakage in Section 13).

## 14-16. Opportunity trigger engine, timing, scoring

Trigger taxonomy lives in `config/opportunity-triggers.yaml`. Timing
classification: IMMEDIATE (0-7d), NEAR_TERM (8-30d), MEDIUM_TERM (31-90d),
WATCH (90+d). Scoring is 0-100 across 8 weighted dimensions (weights in
`config/scoring.yaml`), bands: HOT 80-100, WARM 60-79, WATCH 40-59,
LOW 0-39. The Bangalore HQ gate is mandatory and independent of score.
See `.claude/skills/opportunity-scoring/SKILL.md` and
`src/scoring/scorer.py`.

## 17-18. Sales reasoning & Business Standard solution mapping

Nine reasoning questions per HOT/WARM opportunity (WHY NOW ... WHEN TO
CONTACT) — see `.claude/skills/sales-opportunity-analysis/SKILL.md`.
Trigger-to-product mapping is config-driven
(`config/opportunity-triggers.yaml` + `config/business-standard.yaml`);
no invented inventory or pricing, ever.

## 19-20. Research commands & multi-trigger opportunities

The agent understands natural-language research commands per city and
trigger type (see README.md for examples). A company with 3+ open
triggers within a 90-day window is flagged as a MULTI-TRIGGER
OPPORTUNITY and scored with a bonus (`config/scoring.yaml`).

## 21-22. Decision-maker & contact intelligence

`.claude/skills/prospect-research/SKILL.md` finds the right title;
`.claude/skills/contact-verification/SKILL.md` finds an official
(company-domain) email or shows a professional phone — never a personal
email, never auto-contact. No ContactOut/enrichment API is connected in
this environment; research is public-web/LinkedIn based.

## 23-24. Daily report & Top 5

Full 13-section report format and the "Today's Top 5" narrowing rule are
implemented in `src/reports/generate_daily_report.py` and orchestrated by
`.claude/skills/daily-sales-brief/SKILL.md`.

## 25-26. Source quality & fact discipline

Official company/SEBI/NSE/BSE/government sources and reputable business
media are prioritized over social media. Every finding is tagged `FACT`,
`INFERENCE`, or `ESTIMATE` — never presented with more certainty than the
evidence supports.

## 27. Database

SQLite at `database/sales.db`, schema in `src/db/schema.sql`, covering:
companies, company_hq, campaigns, business_events, ipo_events,
funding_events, product_launches, marketing_initiatives,
expansion_events, leadership_changes, competitor_activity, contacts,
opportunities, opportunity_triggers, outreach, pipeline, followups,
daily_reports. Deduplication is by company name (case-insensitive) via
`src/db/repo.py::get_or_create_company()`.

## 28-29. Project structure & skills

See `README.md` for the full directory layout and skill/agent list, and
`docs/RUNBOOK.md` for how to actually run this day to day, including the
persistence approach chosen for this deployment (GitHub-backed, since
Cowork scheduled runs start in a fresh container each time).
