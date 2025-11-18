"""
User API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import get_current_user
from core.products import get_plan, get_plan_features
from core.quotas import get_current_usage
from models.user import User
from schemas.user import UserResponse, QuotaInfo, UserQuotas, PlanInfo

router = APIRouter(prefix="/api/v1/me", tags=["User"])


@router.get("", response_model=UserResponse)
async def get_current_user_info(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user information with quotas and features

    Returns:
    - User profile
    - Current plan details
    - Usage quotas (used/limit/remaining)
    - Available features
    """
    # Get plan information
    plan = get_plan(user.plan_tier)
    features = get_plan_features(user.plan_tier)

    # Get current usage
    player_reports_used = get_current_usage(user.id, "player_reports_per_month", db)
    team_fit_used = get_current_usage(user.id, "team_fit_analyses_per_month", db)
    api_requests_used = get_current_usage(user.id, "api_requests_per_month", db)

    # Build quota information
    quotas = UserQuotas(
        player_reports=QuotaInfo(
            used=player_reports_used,
            limit=features.player_reports_per_month,
            remaining=max(0, features.player_reports_per_month - player_reports_used)
        ),
        team_fit=QuotaInfo(
            used=team_fit_used,
            limit=features.team_fit_analyses_per_month,
            remaining=max(0, features.team_fit_analyses_per_month - team_fit_used)
        ),
        api_requests=QuotaInfo(
            used=api_requests_used,
            limit=features.api_requests_per_month,
            remaining=max(0, features.api_requests_per_month - api_requests_used)
        )
    )

    # Build plan information
    plan_info = PlanInfo(
        tier=user.plan_tier.value,
        name=plan["pricing"].name,
        price_monthly=plan["pricing"].price_monthly_eur
    )

    # Build features dictionary
    features_dict = {
        "advanced_metrics": features.advanced_metrics,
        "moneyball_valuation": features.moneyball_valuation,
        "pdf_exports": features.pdf_exports,
        "excel_exports": features.excel_exports,
        "api_access": features.api_access
    }

    return UserResponse(
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        plan=plan_info,
        quotas=quotas,
        features=features_dict,
        created_at=user.created_at
    )
