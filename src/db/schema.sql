-- Business Standard Sales Intelligence Agent — database schema (Section 27)
-- SQLite. Foreign keys enforce Company -> Event -> Trigger -> Opportunity ->
-- Decision Maker -> Contact -> Outreach -> Pipeline relationships.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- companies
CREATE TABLE IF NOT EXISTS companies (
    company_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    brand_name      TEXT,
    industry        TEXT,
    website         TEXT,
    linkedin_url    TEXT,
    is_listed       INTEGER DEFAULT 0,           -- 0/1
    created_at      TEXT DEFAULT (datetime('now')),
    updated_at      TEXT DEFAULT (datetime('now')),
    UNIQUE(name)
);

-- --------------------------------------------------------------- company_hq
-- One row per HQ-verification pass; keep history rather than overwrite.
CREATE TABLE IF NOT EXISTS company_hq (
    hq_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    claimed_city    TEXT,                        -- city mentioned in the triggering source
    hq_city         TEXT,                        -- verified HQ city, NULL if unverified
    hq_status       TEXT NOT NULL CHECK (hq_status IN
                        ('BANGALORE_HQ_VERIFIED','NON_BANGALORE_HQ_VERIFIED','HQ_UNVERIFIED')),
    evidence        TEXT,                        -- quote/snippet supporting the verdict
    source_url      TEXT,
    verified_at     TEXT DEFAULT (datetime('now')),
    verified_by     TEXT DEFAULT 'hq-verification-skill'
);
CREATE INDEX IF NOT EXISTS idx_company_hq_company ON company_hq(company_id);

-- ------------------------------------------------------------------ campaigns
-- Competitor advertising intelligence (Sections 12-13).
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    publisher       TEXT NOT NULL,
    campaign_name   TEXT,
    campaign_type   TEXT,                        -- display/roadblock/branded_content/...
    product         TEXT,
    geography       TEXT,
    date_observed   TEXT,
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------- business_events
CREATE TABLE IF NOT EXISTS business_events (
    event_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    event_type      TEXT NOT NULL,                -- e.g. product_launch, cmo_appointment
    event_category  TEXT,                         -- maps to a trigger_type
    description     TEXT,
    event_date       TEXT,                        -- actual/expected date of the event
    announcement_date TEXT,                        -- date it was announced/published
    fact_or_inference TEXT CHECK (fact_or_inference IN ('FACT','INFERENCE','ESTIMATE')),
    business_impact TEXT,
    marketing_impact TEXT,
    advertising_opportunity TEXT,
    source_url      TEXT,
    source_name     TEXT,
    evidence        TEXT,
    confidence      TEXT CHECK (confidence IN ('HIGH','MEDIUM','LOW')),
    created_at      TEXT DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_events_company ON business_events(company_id);

-- ------------------------------------------------------------------ ipo_events
CREATE TABLE IF NOT EXISTS ipo_events (
    ipo_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    ipo_status      TEXT NOT NULL CHECK (ipo_status IN
                        ('IPO_CONFIRMED','IPO_REPORTED','IPO_POSSIBLE','IPO_UNVERIFIED')),
    stage           TEXT,                         -- considering/DRHP filed/approved/roadshow/listed
    expected_timeline TEXT,
    ipo_size        TEXT,
    lead_managers   TEXT,
    drhp_status     TEXT,
    expected_listing TEXT,
    industry        TEXT,
    source_url      TEXT,
    evidence        TEXT,
    bs_pitch_notes  TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- --------------------------------------------------------------- funding_events
CREATE TABLE IF NOT EXISTS funding_events (
    funding_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    stage           TEXT,                         -- Series A/B/... growth/PE/debt
    amount          TEXT,
    currency        TEXT DEFAULT 'INR',
    date_announced  TEXT,
    investors       TEXT,
    purpose         TEXT,
    expansion_plan  TEXT,
    marketing_implication TEXT,
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------ product_launches
CREATE TABLE IF NOT EXISTS product_launches (
    launch_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    brand           TEXT,
    product_name    TEXT,
    launch_date     TEXT,
    target_audience TEXT,
    campaign_geography TEXT,
    marketing_activity TEXT,
    competitor_activity TEXT,
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- --------------------------------------------------------- marketing_initiatives
CREATE TABLE IF NOT EXISTS marketing_initiatives (
    initiative_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    campaign_name   TEXT,
    agency          TEXT,
    objective       TEXT,
    timing          TEXT,
    geography       TEXT,
    target_audience TEXT,
    media_activity  TEXT,
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------- expansion_events
CREATE TABLE IF NOT EXISTS expansion_events (
    expansion_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    expansion_type  TEXT,                         -- new_city/new_office/new_plant/international/...
    location        TEXT,
    announcement_date TEXT,
    details         TEXT,
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------- leadership_changes
CREATE TABLE IF NOT EXISTS leadership_changes (
    leadership_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    person_name     TEXT,
    title           TEXT,
    appointment_date TEXT,
    linkedin_url    TEXT,
    relevance       TEXT,
    confidence      TEXT CHECK (confidence IN ('HIGH','MEDIUM','LOW')),
    source_url      TEXT,
    evidence        TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------- competitor_activity
CREATE TABLE IF NOT EXISTS competitor_activity (
    activity_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id     INTEGER REFERENCES campaigns(campaign_id),
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    has_bs_activity INTEGER DEFAULT 0,            -- 0/1, known Business Standard activity?
    leakage_flag    INTEGER DEFAULT 0,            -- 1 if competitor spend + no BS activity
    created_at      TEXT DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------------- contacts
CREATE TABLE IF NOT EXISTS contacts (
    contact_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    name            TEXT,
    title           TEXT,
    linkedin_url    TEXT,
    official_email  TEXT,                         -- NULL if not found; NEVER a personal email
    official_email_status TEXT CHECK (official_email_status IN
                        ('FOUND','OFFICIAL_EMAIL_NOT_FOUND')) DEFAULT 'OFFICIAL_EMAIL_NOT_FOUND',
    professional_phone TEXT,
    is_new_appointment INTEGER DEFAULT 0,
    confidence      TEXT CHECK (confidence IN ('HIGH','MEDIUM','LOW')),
    source_url      TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- --------------------------------------------------------------- opportunity_triggers
CREATE TABLE IF NOT EXISTS opportunity_triggers (
    trigger_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    trigger_type    TEXT NOT NULL,                 -- IPO/FUNDRAISING/PRODUCT_LAUNCH/...
    source_event_id INTEGER REFERENCES business_events(event_id),
    opened_at       TEXT DEFAULT (datetime('now')),
    is_open         INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_triggers_company ON opportunity_triggers(company_id);

-- ------------------------------------------------------------------- opportunities
CREATE TABLE IF NOT EXISTS opportunities (
    opportunity_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES companies(company_id),
    hq_status       TEXT NOT NULL,                 -- copied from company_hq at scoring time
    primary_trigger TEXT,
    trigger_count   INTEGER DEFAULT 1,
    score           INTEGER,                       -- 0-100
    classification  TEXT CHECK (classification IN ('HOT','WARM','WATCH','LOW')),
    timing          TEXT CHECK (timing IN ('IMMEDIATE','NEAR_TERM','MEDIUM_TERM','WATCH')),
    why_now         TEXT,
    why_this_company TEXT,
    business_problem TEXT,
    why_business_standard TEXT,
    recommended_product TEXT,
    recommended_contact_id INTEGER REFERENCES contacts(contact_id),
    recommended_action TEXT,
    is_qualified_bangalore INTEGER DEFAULT 0,      -- hard gate result, 0/1
    scored_at       TEXT DEFAULT (datetime('now')),
    score_breakdown TEXT                            -- JSON string of weighted sub-scores
);
CREATE INDEX IF NOT EXISTS idx_opps_company ON opportunities(company_id);
CREATE INDEX IF NOT EXISTS idx_opps_score ON opportunities(score DESC);

-- ------------------------------------------------------------------------- outreach
CREATE TABLE IF NOT EXISTS outreach (
    outreach_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id  INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
    contact_id      INTEGER REFERENCES contacts(contact_id),
    channel         TEXT,                          -- email/call/linkedin/in-person
    status          TEXT,                           -- planned/sent/replied/no_response
    message_summary TEXT,
    sent_at         TEXT,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------------------- pipeline
CREATE TABLE IF NOT EXISTS pipeline (
    pipeline_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id  INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
    stage           TEXT,                           -- prospecting/contacted/meeting/proposal/won/lost
    value_estimate  TEXT,
    next_step       TEXT,
    next_step_date  TEXT,
    owner           TEXT DEFAULT 'user',
    updated_at      TEXT DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------------------- followups
CREATE TABLE IF NOT EXISTS followups (
    followup_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id  INTEGER NOT NULL REFERENCES opportunities(opportunity_id),
    due_date        TEXT,
    note            TEXT,
    is_done         INTEGER DEFAULT 0,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------- daily_reports
CREATE TABLE IF NOT EXISTS daily_reports (
    report_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date     TEXT NOT NULL UNIQUE,
    top5_json       TEXT,
    full_report_md  TEXT,
    generated_at    TEXT DEFAULT (datetime('now'))
);
