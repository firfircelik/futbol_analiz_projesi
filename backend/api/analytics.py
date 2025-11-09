"""
Analytics API routes (Team Fit, Moneyball, etc.)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.auth import get_current_user
from core.quotas import check_quota_dependency
from core.products import get_plan_features
from schemas.analytics import TeamFitRequest, TeamFitResponse, TeamFitBreakdown
from schemas.analytics import MoneyballValuationResponse, ComparablePlayer

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

# TODO Phase 2: Import real services
# from services.team_fit_service import TeamFitService
# from services.moneyball_service import MoneyballService


@router.post("/team-fit", response_model=TeamFitResponse)
async def analyze_team_fit(
    request: TeamFitRequest,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    _quota = Depends(check_quota_dependency("team_fit_analyses_per_month"))
):
    """
    Analyze how well a player fits a specific team

    - 7-dimensional compatibility analysis
    - Fit score (0-100)
    - Recommendation (AVOID, MONITOR, BUY, STRONG_BUY)
    - Adaptation timeline
    - Counts towards team fit quota

    Requires: Scout plan or higher
    """
    # Check if user has access to team fit
    features = get_plan_features(user.plan_tier)
    if not features.team_fit_analyses_per_month > 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Team Fit Analysis requires Scout plan or higher. Upgrade to access this feature."
        )

    # TODO Phase 2: Connect to real TeamFitService
    # team_fit_service = TeamFitService()
    # result = team_fit_service.analyze_fit(request.player_id, request.team_id)

    # TEMPORARY: Mock data for Phase 1
    breakdown = TeamFitBreakdown(
        statistical_fit=90.0,
        tactical_fit=88.0,
        personality_fit=85.0,
        chemistry_fit=87.0,
        cultural_fit=92.0,
        budget_fit=75.0,
        age_fit=95.0
    )

    return TeamFitResponse(
        player_id=request.player_id,
        player_name="Mohamed Salah",
        team_id=request.team_id,
        team_name="Liverpool FC",
        fit_score=87.5,
        fit_rating="EXCELLENT_FIT",
        recommendation="STRONG_BUY",
        breakdown=breakdown,
        strengths=[
            "Plays in priority position (RW)",
            "Perfect age bracket for immediate impact",
            "Excellent cultural and tactical alignment",
            "High performance level matches team standards"
        ],
        concerns=[
            "Market value may be above budget constraints",
            "Minor tactical adjustment needed for pressing system"
        ],
        adaptation_timeline="IMMEDIATE (0-1 months)"
    )


@router.post("/moneyball/{player_id}", response_model=MoneyballValuationResponse)
async def get_moneyball_valuation(
    player_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    _quota = Depends(check_quota_dependency("player_reports_per_month"))
):
    """
    Get Moneyball-style player valuation

    - Compare market value vs calculated value
    - ROI potential
    - Value category (OVERVALUED, FAIR, UNDERVALUED, BARGAIN)
    - Comparable players
    - Recommendation (SELL, HOLD, BUY, STRONG_BUY)

    Requires: Professional plan or higher
    """
    # Check if user has access to moneyball
    features = get_plan_features(user.plan_tier)
    if not features.moneyball_valuation:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Moneyball Valuation requires Professional plan or higher. Upgrade to access this feature."
        )

    # TODO Phase 2: Connect to real MoneyballService
    # moneyball_service = MoneyballService()
    # result = moneyball_service.calculate_valuation(player_id)

    # TEMPORARY: Mock data for Phase 1
    comparables = [
        ComparablePlayer(name="Bukayo Saka", value=120.0, similarity=0.92),
        ComparablePlayer(name="Rafael Leão", value=90.0, similarity=0.88),
        ComparablePlayer(name="Khvicha Kvaratskhelia", value=80.0, similarity=0.85)
    ]

    return MoneyballValuationResponse(
        player_id=player_id,
        player_name="Mohamed Salah",
        market_value=65.0,
        calculated_value=95.0,
        value_ratio=1.46,
        category="UNDERVALUED",
        roi_potential=46.2,
        recommendation="BUY",
        comparable_players=comparables
    )
