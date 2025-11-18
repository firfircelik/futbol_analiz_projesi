"""
Pricing API routes
"""
from fastapi import APIRouter
from typing import List, Dict

from core.products import PLANS, PlanTier

router = APIRouter(prefix="/api/v1/pricing", tags=["Pricing"])


@router.get("")
async def get_pricing():
    """
    Get all pricing plans (public endpoint, no auth required)

    Returns all subscription tiers with:
    - Pricing information
    - Feature limits
    - Target audience
    """
    plans_data = []

    for tier, plan in PLANS.items():
        plans_data.append({
            "tier": tier.value,
            "name": plan["pricing"].name,
            "description": plan["pricing"].description,
            "price_monthly": plan["pricing"].price_monthly_eur,
            "price_yearly": plan["pricing"].price_yearly_eur,
            "savings_percent": plan["pricing"].yearly_savings_percent,
            "currency": plan["pricing"].currency,
            "features": {
                "player_reports": plan["features"].player_reports_per_month,
                "leagues": plan["features"].leagues_access,
                "team_fit": plan["features"].team_fit_analyses_per_month,
                "api_requests": plan["features"].api_requests_per_month,
                "advanced_metrics": plan["features"].advanced_metrics,
                "moneyball": plan["features"].moneyball_valuation,
                "pdf_exports": plan["features"].pdf_exports,
                "excel_exports": plan["features"].excel_exports,
                "api_access": plan["features"].api_access,
            },
            "popular": plan.get("popular", False),
            "recommended": plan.get("recommended", False),
            "target_audience": plan.get("target_audience", "")
        })

    return {"plans": plans_data}


@router.get("/{tier}")
async def get_plan_details(tier: PlanTier):
    """
    Get details for a specific pricing tier

    Returns detailed information about a single plan
    """
    if tier not in PLANS:
        return {"error": "Plan not found"}, 404

    plan = PLANS[tier]

    return {
        "tier": tier.value,
        "pricing": {
            "name": plan["pricing"].name,
            "description": plan["pricing"].description,
            "price_monthly": plan["pricing"].price_monthly_eur,
            "price_yearly": plan["pricing"].price_yearly_eur,
            "savings_percent": plan["pricing"].yearly_savings_percent,
            "currency": plan["pricing"].currency,
        },
        "features": {
            "player_reports_per_month": plan["features"].player_reports_per_month,
            "leagues_access": plan["features"].leagues_access,
            "team_fit_analyses_per_month": plan["features"].team_fit_analyses_per_month,
            "api_requests_per_month": plan["features"].api_requests_per_month,
            "advanced_metrics": plan["features"].advanced_metrics,
            "moneyball_valuation": plan["features"].moneyball_valuation,
            "pdf_exports": plan["features"].pdf_exports,
            "excel_exports": plan["features"].excel_exports,
            "email_reports": plan["features"].email_reports,
            "api_access": plan["features"].api_access,
            "multi_user_seats": plan["features"].multi_user_seats,
        },
        "target_audience": plan.get("target_audience", ""),
        "key_benefits": plan.get("key_benefits", []),
    }
