# Runbook — how this actually runs day to day

## The environment reality this project is built for

This build runs inside **Cowork's cloud sandbox**, not a persistent
Claude Code CLI checkout. That matters for one specific reason: a daily
**scheduled task** (what fires the morning report automatically) starts a
**brand-new, empty container every time**. Nothing written to disk in one
run is visible in the next run unless it's stored somewhere external.
That's why this project is a git repo from the start — GitHub is the
persistence layer for `database/sales.db`, the skills, and the config.

## One-time setup (you do this once)

1. **Create an empty GitHub repository** (private, recommended) — e.g.
   `bs-sales-intel`. Do not initialize it with a README/license (this
   project already has files).
2. Take the zip delivered to you in this conversation, unzip it, and push
   it as the initial commit:
   ```
   cd bs-sales-intel
   git remote add origin https://github.com/<you>/bs-sales-intel.git
   git branch -M main
   git push -u origin main
   ```
3. **For automated daily runs**, the scheduled-task session needs write
   access to that repo. Create a **fine-grained GitHub Personal Access
   Token** scoped to *only* this repository, with **Contents: Read and
   write** permission, and a reasonable expiry (e.g. 90 days — rotate it
   when it expires). Give me the repo URL and token when you want daily
   automation turned on; I'll store the token inside the scheduled task's
   prompt so each morning's fresh session can clone, update the DB, and
   push back. This is a real tradeoff worth knowing: the token lives as
   plaintext in that scheduled task's stored prompt in your account, not
   in a dedicated secrets vault (this environment doesn't expose one to
   me). A repo-scoped, short-lived, revocable token is the standard way
   to bound that risk — don't reuse a broad/account-wide token here.
   If you'd rather not do this, use the manual-run option below instead.

## Manual run (no token needed, works today)

Any time, ask me (in a Cowork conversation) to "run today's Business
Standard sales brief." I'll pull the latest repo state you've pushed (or
work from whatever's already in this session if we just built it),
run the `daily-sales-brief` pipeline, and deliver the report + push the
updated database back to GitHub if you've connected a repo and I have
push access for that session (e.g., you pasted a token into that
conversation, or your desktop app is connected and I can shell out via
the device bridge to a local `git`/`gh` that's already authenticated as
you).

## Automated daily run (once the token is provided)

A scheduled task (cron, ~8:00 AM IST = 02:30 UTC) fires a fresh session
whose prompt tells it to:
1. `git clone` the repo using the stored token.
2. `pip install -r requirements.txt --break-system-packages`
3. `python3 src/db/init_db.py`
4. Run the `daily-sales-brief` skill end to end.
5. `git add database/sales.db data/ && git commit -m "daily run <date>" && git push`
6. Deliver the report back to you as a message in that run (push
   notification if configured).

## Alternative persistence (if you skip GitHub)

If you'd rather not manage a token, two fallbacks exist, both weaker:
- **Desktop-folder persistence**: connect a folder via the Claude desktop
  app; I write `database/sales.db` and reports there each run. Daily
  automation then requires your desktop app to be open at run time (the
  device bridge only works while it's connected), so this suits
  on-demand runs better than unattended ones.
- **Stateless daily runs**: each scheduled run does a fresh research pass
  and produces a report with no memory of prior days — no
  `pipeline`/`outreach`/`followups` continuity, no de-duplication against
  previously-seen opportunities. Simplest, but loses the CRM-like value
  of the system over time.

## Local (non-Cowork) use

If you later run this inside an actual Claude Code CLI checkout of this
repo, everything under `.claude/skills/` and `.claude/agents/` works
exactly as designed with no changes — that's the native format Claude
Code project loads automatically.
