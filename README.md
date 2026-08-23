# Business Standard — Sales Intelligence Agent

A Claude Code project that finds companies headquartered in Bangalore
(primary), Chennai, and Hyderabad (market intelligence) that are likely
to have a reason to spend advertising/marketing money right now — and
turns that into a scored, reasoned, daily sales-action list for Business
Standard's Digital Ad Sales team.

Full spec: `docs/master-spec.md`. How it actually runs day to day
(including the GitHub-persistence setup, since this was built inside
Cowork's cloud sandbox): `docs/RUNBOOK.md`.

## Core question this answers every day

**"Which Bangalore-headquartered companies should I approach today, and
WHY?"**

## Hard rule

A company only counts as a Bangalore opportunity if its **headquarters**
(not office, not campaign, not founder) is in Bangalore. See
`.claude/skills/hq-verification/SKILL.md`.

## Project structure

```
.claude/
  skills/                  18 skills — one per intelligence domain, plus
                            opportunity-scoring, sales-opportunity-analysis,
                            pitch-generation, media-planning,
                            follow-up-intelligence, revenue-intelligence,
                            and the daily-sales-brief orchestrator.
  agents/                  6 subagents (market-researcher,
                            competitor-researcher, hq-verifier,
                            prospect-researcher, opportunity-analyzer,
                            sales-analyst) matching the pipeline stages.
config/
  cities.yaml              Bangalore = primary territory; Chennai/Hyderabad
                            = market intelligence only.
  scoring.yaml             0-100 scoring weights, HOT/WARM/WATCH/LOW bands,
                            timing windows, Bangalore HQ gate,
                            multi-trigger bonus.
  publishers.yaml          Competitor publishers monitored.
  opportunity-triggers.yaml Trigger taxonomy -> default BS product mapping.
  business-standard.yaml   BS product catalogue (edit before real pitches —
                            no invented inventory/pricing).
src/
  db/                      schema.sql, init_db.py, repo.py (data-access layer)
  scoring/                 scorer.py (pure scoring function over the config)
  reports/                 generate_daily_report.py (renders Section 23 report)
data/                      Raw research working files, if any (companies/,
                            events/, campaigns/, opportunities/, pipeline/)
database/
  sales.db                 SQLite database (created by init_db.py)
docs/
  master-spec.md           Full specification, organized by section
  RUNBOOK.md               How to actually run this day to day
tests/
  test_scoring.py          Scoring engine sanity tests
```

## Quick start

```bash
pip install -r requirements.txt --break-system-packages
python3 src/db/init_db.py
python3 -m pytest tests/ -q      # or: python3 tests/test_scoring.py
```

Then, inside Claude Code (or a Claude session with these skills loaded),
say: *"Run today's Business Standard sales brief"* — that invokes the
`daily-sales-brief` skill, which orchestrates all the others.

## Example research commands the agent understands

- "Find Bangalore-HQ companies preparing for IPO."
- "Find Bangalore-HQ companies that raised funding this week."
- "Find Bangalore-HQ companies appointing new CMOs."
- "Find Bangalore-HQ companies advertising on competitors."
- "Find Chennai-HQ companies preparing for IPO." (market intelligence —
  never enters the Bangalore qualified list)
- "Find companies with multiple sales triggers."
- "Who should I approach today, and why?"

## Fact discipline

Every finding is tagged `FACT`, `INFERENCE`, or `ESTIMATE` (see
`docs/master-spec.md` Section 26). Never presented with more certainty
than the evidence supports.

## What's NOT included

- No pricing/inventory beyond what's listed in
  `config/business-standard.yaml` — fill that in with real BS ad-sales
  inventory before pitching.
- No automatic outreach — this system drafts and recommends, a human
  always sends.
- No ContactOut/enrichment API — contact research is public web/LinkedIn
  based (see `.claude/skills/contact-verification/SKILL.md`).
