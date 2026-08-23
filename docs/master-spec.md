# Business Standard Sales Intelligence Agent — Master Specification

Owner: Boss (Business Standard, Digital Ad Sales)
Qualified markets (updated 2026-08-23): **Bangalore (Bengaluru), Chennai, and
Hyderabad headquarters** -- see Section 2/3 and config/cities.yaml. Chennai
and Hyderabad were market-intelligence-only before 2026-08-23; that
restriction has been lifted.

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

A company qualifies for the opportunity list **only** if its headquarters
— not office, not branch, not founder residence, not campaign geography —
is in Bangalore, Chennai, or Hyderabad. For an **international** company
(global HQ outside India), it qualifies if its **India head office** is in
one of those three cities — the global HQ location is irrelevant in that
case, but a foreign company merely opening *an* office there while basing
its India operations elsewhere does not qualify. Statuses:
`BANGALORE_HQ_VERIFIED`, `CHENNAI_HQ_VERIFIED`, `HYDERABAD_HQ_VERIFIED`,
`NON_QUALIFIED_HQ_VERIFIED`, `HQ_UNVERIFIED`. Only the first three appear
in the qualified list; uncertain cases go to the `HQ_VERIFICATION_QUEUE`
and are never assumed. See `.claude/skills/hq-verification/SKILL.md` for
the enforcement mechanism (where it exists) and `config/cities.yaml` for
the canonical rule text.

## 3. Target cities

Bangalore, Chennai, and Hyderabad are all qualified sales territories as
of 2026-08-23 (see `config/cities.yaml`), scored and reported identically.
Bangalore remains the most-covered market in practice. Before 2026-08-23,
Chennai and Hyderabad were market-intelligence-only and never promoted
into the qualified list regardless of trigger strength — that restriction
no longer applies.

## 2b. Target-audience filter (added 2026-08-23)

Passing the city-HQ gate is necessary but not sufficient. A company must
also pass the brand-fit screen in `config/target-criteria.yaml` before
it's worth researching at all: any B2B brand qualifies regardless of
ticket size; a B2C brand qualifies only if its typical purchase is a
considered, higher-ticket decision (e.g. premium mattresses/furniture,
luxury automotive) rather than routine/daily consumption (FMCG, budget
consumer goods) — ordinary mass-market B2C brands are excluded even when
well-known or Bangalore-adjacent. This is a judgment call to make and
record explicitly during research, not a scorer.py dimension.

## 4-13. Intelligence engines

Each of the following has a dedicated skill under `.claude/skills/`
(see that file for exact capture schema, sources, and process):
client-intelligence, ipo-intelligence, funding-intelligence,
product-launch-intelligence, marketing-intelligence,
expansion-intelligence, revenue-intelligence (financial events),
leadership-intelligence, competitor-intelligence (incl. competitor
leakage in Section 13).

## 13b. Editorial-article scanning (added 2026-08-23)

In addition to press-release/funding/DRHP-style discovery, each of the 8
publishers in `config/publishers.yaml` (Economic Times, Times of India,
Moneycontrol, Mint, CNBC-TV18, Financial Express, BusinessLine, Deccan
Herald) should also be scanned for **editorial/opinion coverage** that
mentions a qualified-city brand -- not just their own advertising. This
surfaces brands getting organic editorial attention (a different signal
than a funding/IPO trigger) that may still be worth a pitch. Apply the
city-HQ gate and target-audience filter (Sections 2/2b) to anything found
this way before treating it as an opportunity -- editorial mentions do not
bypass either screen.

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
email, never auto-contact. No ContactOut connector exists in this
environment (checked 2026-08-23; it isn't in the connector registry at
all). Contact enrichment (phone/email) is done via the **Lusha** connector
once connected/enabled, falling back to public-web/LinkedIn research when
it isn't. Daily leads (name, designation, phone, email) are compiled into
the report once Lusha is wired in. Drafting outreach emails happens via
the **Gmail** connector once connected — draft only, **never send without
explicit approval**.

## 23-24. Daily report & Top 5

16-section report format (Sections 1-16; a former Section 12 "Follow-ups
Due" was removed 2026-08-23 -- it never had a writer populating the
`followups` table, so it was permanently empty and just added noise) and
the "Today's Top 5" narrowing rule are implemented in
`src/reports/generate_daily_report.py` and orchestrated by
`.claude/skills/daily-sales-brief/SKILL.md`.

**Sections 1-11 are scoped to TODAY only** (added 2026-08-23, per direct
instruction not to repeat an unchanged company/finding day after day): each
uses `report_date` to show only opportunities/events/triggers actually
(re)scored or recorded on that date, via
`src/db/repo.py::todays_opportunities()` and per-table `date(created_at) =
date(?)` filters. A company reported yesterday with nothing new today is
correctly absent, not repeated. The full standing pipeline (regardless of
when each item last changed) is a deliberately separate view via
`top_opportunities()`, used by `generate_weekly_report.py` -- so nothing is
lost, it just isn't repeated in every single daily digest.

## 25-26. Source quality & fact discipline

Official company/SEBI/NSE/BSE/government sources and reputable business
media are prioritized over social media. Every finding is tagged `FACT`,
`INFERENCE`, or `ESTIMATE` — never presented with more certainty than the
evidence supports.

## 14b-14e. Sales-rep workflow additions (added 2026-08-23)

- **14b. Pitch drafts (Section 13 of the report).** Every WARM-or-better
  opportunity gets an assembled, ready-to-send pitch draft and objection-
  handling notes, generated by `src/pitch/generate_pitch.py`. This is a pure
  templating function -- it only reorganizes fields a research pass has
  already verified (why_now, why_this_company, business_problem,
  why_business_standard, recommended_product); it never invents a fact, a
  product, or a price. Per `config/business-standard.yaml` pitch_rules,
  every draft says "PRICING: CONFIRM WITH SALES OPS" rather than quoting a
  number. Stored in `opportunities.pitch_draft` / `.objection_notes`.
- **14c. Calendar-driven opportunities (Section 14, 90-day lookahead as of
  2026-08-23 -- widened from 45 days so a founder-day anniversary, product-
  launch anniversary, or macro window a month or two out is flagged today,
  giving enough lead time to pre-plan roadblock/inventory bookings).** Two
  sources: (1) `company_key_dates` -- recurring, company-specific dates
  (founding anniversary, a landmark past product launch, a funding-round
  anniversary) worth pitching around, researched and recorded per company;
  (2) `config/calendar-triggers.yaml` macro windows (fiscal year-end, Union
  Budget reaction period, festive season, earnings season), each with a
  lead_days of 30-60 for the same reason. Passing a calendar window is a
  REASON to check a company, not proof it's a good pitch -- the city-HQ
  gate and target-criteria filter still apply. The festive-season window is
  lunar/movable and must be confirmed against a real source during research
  each year, never hardcoded.
- **14d. Risk flags (Section 15).** `risk_flags` table -- signals a deal in
  progress might stall (funding freeze, unreplaced leadership departure,
  layoffs, negative press, regulatory trouble). Separate from
  `opportunity_triggers` (reasons TO pitch); this is reasons a pitch might
  currently be a bad use of time.
- **14e. Decision-maker movement checks.** Before pitching an already-known
  contact, cross-check `src/db/repo.py::all_tracked_contacts()` against
  fresh research -- if a contact's role or company has changed since it was
  recorded, log a new `leadership_changes` row rather than pitching a
  stale contact.

## 13c. Industry movement digest (Section 16, added 2026-08-23)

Separate from the Section 9-10 ad-placement/ROS-roadblock competitor list
(config/publishers.yaml, now 5 publishers -- CNBC-TV18, BusinessLine, and
Deccan Herald were removed from ad-research coverage). A different pair of
trade-press sources, config/industry-movement-sources.yaml (Exchange4Media,
afaqs!), feeds a short 2-3 line daily digest of agency/brand movement: an
agency winning a mandate, an executive joining an agency/brand as CMO,
a new agency-brand association. Every item must be Bangalore/Chennai/
Hyderabad relevant with a stated reason -- generic industry news from
these sources does not qualify just because the source is being checked.
Stored in the `industry_movements` table via
`src/db/repo.py::add_industry_movement()`.

## 14f. Weekly rollup

`src/reports/generate_weekly_report.py` reads (never re-researches) the
past week's `opportunities`, `risk_flags`, `outreach`, and `pipeline`
records into a Friday summary: what got scored this week, current pipeline
by band, active risk flags, and outreach/pipeline tracking (honestly empty
until outreach is actually logged against an opportunity -- nothing
fabricated to fill that section).

## 27. Database

SQLite at `database/sales.db`, schema in `src/db/schema.sql`, covering:
companies, company_hq, campaigns, business_events, ipo_events,
funding_events, product_launches, marketing_initiatives,
expansion_events, leadership_changes, competitor_activity, contacts,
opportunities (incl. pitch_draft/objection_notes), opportunity_triggers,
outreach, pipeline, followups, company_key_dates, risk_flags,
daily_reports. Deduplication is by company name (case-insensitive) via
`src/db/repo.py::get_or_create_company()`.

## 28-29. Project structure & skills

See `README.md` for the full directory layout and skill/agent list, and
`docs/RUNBOOK.md` for how to actually run this day to day, including the
persistence approach chosen for this deployment (GitHub-backed, since
Cowork scheduled runs start in a fresh container each time).
