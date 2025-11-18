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

# Import real services
from services.team_fit_service import get_team_fit_service
from services.moneyball_service import get_moneyball_service
from services.data_service import get_data_service


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

    # Get services
    team_fit_service = get_team_fit_service()
    data_service = get_data_service()

    # Get player data
    player_data = await data_service.get_player_profile(request.player_id)
    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player not found: {request.player_id}"
        )

    # Prepare team data (in real app, this would come from database or request)
    team_data = {
        'team_name': request.team_name if hasattr(request, 'team_name') else 'Liverpool FC',
        'league': 'Premier League',
        'playing_style': 'high_press',
        'formation': '4-3-3',
        'average_age': 26.5,
        'budget_millions': 50.0,
        'priority_positions': ['RW', 'ST', 'CAM'],
        'desired_traits': ['pace', 'finishing', 'work_rate'],
        'average_player_value': 30.0,
        'team_personality': 'ambitious',
        'requires_pace': True,
        'requires_physicality': False,
        'requires_technique': True,
        'requires_experience': False,
    }

    # Analyze team fit
    result = await team_fit_service.analyze_fit(
        player_id=request.player_id,
        player_data=player_data,
        team_id=request.team_id,
        team_data=team_data
    )

    # Convert breakdown to TeamFitBreakdown schema
    breakdown_data = result.get('breakdown', {})
    breakdown = TeamFitBreakdown(
        statistical_fit=breakdown_data.get('statistical_fit', {}).get('score', 50.0),
        tactical_fit=breakdown_data.get('tactical_fit', {}).get('score', 50.0),
        personality_fit=breakdown_data.get('personality_fit', {}).get('score', 50.0),
        chemistry_fit=breakdown_data.get('chemistry_fit', {}).get('score', 50.0),
        cultural_fit=breakdown_data.get('cultural_fit', {}).get('score', 50.0),
        budget_fit=breakdown_data.get('budget_fit', {}).get('score', 50.0),
        age_fit=breakdown_data.get('age_fit', {}).get('score', 50.0)
    )

    return TeamFitResponse(
        player_id=request.player_id,
        player_name=result.get('player_name', 'Unknown'),
        team_id=request.team_id,
        team_name=result.get('team_name', 'Unknown Team'),
        fit_score=result.get('overall_fit_score', 50.0),
        fit_rating=result.get('fit_rating', 'MODERATE_FIT'),
        recommendation=result.get('recommendation', 'Requires further assessment'),
        breakdown=breakdown,
        strengths=result.get('key_strengths', []),
        concerns=result.get('potential_concerns', []),
        adaptation_timeline=result.get('adaptation_timeline', 'UNKNOWN')
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

    # Get services
    moneyball_service = get_moneyball_service()
    data_service = get_data_service()

    # Get player data
    player_data = await data_service.get_player_profile(player_id)
    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player not found: {player_id}"
        )

    # Get market value
    market_value = player_data.get('market_data', {}).get('market_value', 10.0)

    # Calculate Moneyball valuation
    result = await moneyball_service.calculate_valuation(
        player_id=player_id,
        player_stats=player_data,
        market_value=market_value
    )

    # Prepare comparable players (placeholder - TODO: implement similarity search)
    comparables = result.get('comparable_players', [])
    comparable_list = [
        ComparablePlayer(
            name=comp.get('name', 'Unknown'),
            value=comp.get('value', 0.0),
            similarity=comp.get('similarity', 0.0)
        )
        for comp in comparables
    ]

    return MoneyballValuationResponse(
        player_id=player_id,
        player_name=result.get('player_name', 'Unknown'),
        market_value=result.get('market_value', 10.0),
        calculated_value=result.get('calculated_value', 10.0),
        value_ratio=result.get('value_ratio', 1.0),
        category=result.get('category', 'FAIR'),
        roi_potential=result.get('roi_potential', 0.0),
        recommendation=result.get('recommendation', 'HOLD'),
        comparable_players=comparable_list
    )
