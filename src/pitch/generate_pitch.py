#!/usr/bin/env python3
"""
Pitch draft assembly -- Section 14 of the daily report, added 2026-08-23.

Deliberately a pure templating function, like scorer.py: it only rearranges
fields a research pass has ALREADY verified (why_now, why_this_company,
business_problem, why_business_standard, recommended_product) into
pitch-ready copy. It never invents a fact, a product, or a price that isn't
already in the opportunity record -- per config/business-standard.yaml's
pitch_rules (no invented inventory/pricing, ever; flag pricing questions to
sales ops instead of quoting a number).

Only called for WARM-or-better opportunities (config/scoring.yaml bands) --
a LOW/WATCH opportunity doesn't have enough verified substance yet for a
pitch to be worth drafting.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
BUSINESS_STANDARD_PATH = ROOT / "config" / "business-standard.yaml"


def _load_product_labels() -> dict:
    cfg = yaml.safe_load(BUSINESS_STANDARD_PATH.read_text())
    return {key: val["label"] for key, val in cfg.get("products", {}).items()}


def _product_labels(recommended_product: str, labels: dict) -> str:
    keys = [k.strip() for k in (recommended_product or "").split(",") if k.strip()]
    names = [labels.get(k, k) for k in keys]
    return ", ".join(names) if names else "a placement suited to this trigger (confirm with sales ops)"


def build_pitch(opportunity: dict, company_name: str, contact_name: str | None = None,
                 contact_title: str | None = None, labels: dict | None = None) -> dict:
    """
    opportunity: a dict with the same keys as an `opportunities` table row
    (why_now, why_this_company, business_problem, why_business_standard,
    recommended_product, primary_trigger, classification).

    Returns {"pitch_draft": str, "objection_notes": str}.
    """
    labels = labels or _load_product_labels()
    product_text = _product_labels(opportunity.get("recommended_product", ""), labels)
    greeting = f"Hi {contact_name.split()[0]}," if contact_name else "Hi,"
    title_line = f" ({contact_title})" if contact_name and contact_title else ""

    pitch_draft = f"""Subject: {company_name}{title_line} -- {opportunity.get('primary_trigger', 'opportunity')} idea from Business Standard

{greeting}

{opportunity.get('why_now') or '[why-now not recorded -- do not send until this is filled in]'}

{opportunity.get('why_this_company') or ''}

{opportunity.get('business_problem') or ''}

{opportunity.get('why_business_standard') or ''} We'd suggest starting the conversation around: {product_text}.

PRICING: CONFIRM WITH SALES OPS before quoting anything -- this draft intentionally
does not include rates or specific inventory availability.

Happy to set up a short call this week if useful.

-- Business Standard, Digital Ad Sales""".strip()

    objection_notes = (
        f"Anticipated pushback and how to answer, based only on what's verified for this opportunity "
        f"(classification: {opportunity.get('classification', 'n/a')}):\n"
        f"- \"We already have coverage elsewhere / another publisher reached out first\" -> "
        f"lead with the specific trigger ({opportunity.get('primary_trigger', 'n/a')}) and why the "
        f"BS business/investor audience fits it better than a general news outlet -- "
        f"see: {opportunity.get('why_business_standard') or '[not recorded]'}\n"
        f"- \"What does this cost?\" -> do not quote a number; say pricing is being confirmed with "
        f"sales ops and ask what budget range/objective they have in mind first.\n"
        f"- \"Why now, specifically?\" -> restate why_now verbatim, it's time-bound: "
        f"{opportunity.get('why_now') or '[not recorded]'}\n"
        f"- If the contact pushes on a claim not in the record above, do not improvise an answer -- "
        f"say you'll confirm and follow up, then verify before replying."
    )

    return {"pitch_draft": pitch_draft, "objection_notes": objection_notes}


if __name__ == "__main__":
    example = build_pitch(
        {
            "primary_trigger": "PRODUCT_LAUNCH",
            "classification": "HOT",
            "why_now": "Circle beta went live 5 days ago and is still in its awareness window.",
            "why_this_company": "CRED, Bengaluru HQ verified, well-funded, proven marketing spender.",
            "business_problem": "Needs to build trust for a brand-new paid product.",
            "why_business_standard": "BS's business/investor audience overlaps with Circle's target users.",
            "recommended_product": "branded_content, thought_leadership",
        },
        company_name="CRED",
        contact_name="Miten Sampat",
        contact_title="Interim CEO",
    )
    print(example["pitch_draft"])
    print("\n---\n")
    print(example["objection_notes"])
