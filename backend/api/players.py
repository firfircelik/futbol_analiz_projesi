"""
Player API routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from core.database import get_db
from core.auth import get_current_user
from core.quotas import check_quota_dependency
from schemas.player import PlayerSearchResponse, PlayerProfile, PlayerSearchResult
from schemas.player import PlayerBasicStats, PlayerAdvancedMetrics, PlayerPerformance, MarketData

router = APIRouter(prefix="/api/v1/players", tags=["Players"])

# Import real services
from services.data_service import get_data_service
from services.opta_service import get_opta_service


@router.get("/search", response_model=PlayerSearchResponse)
async def search_players(
    query: str = Query(..., min_length=2),
    league: Optional[str] = None,
    position: Optional[str] = None,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    _quota = Depends(check_quota_dependency("api_requests_per_month"))
):
    """
    Search for players

    - Searches across all supported leagues
    - Returns player list with Opta Index
    - Counts towards API requests quota

    Filters:
    - query: Player name (min 2 characters)
    - league: Filter by league (optional)
    - position: Filter by position (optional)
    """
    # Get data service and search players
    data_service = get_data_service()
    results = await data_service.search_players(query, league, position)

    return PlayerSearchResponse(
        query=query,
        results=results,
        total=len(results)
    )


@router.get("/{player_id}", response_model=PlayerProfile)
async def get_player_profile(
    player_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
    _quota = Depends(check_quota_dependency("player_reports_per_month"))
):
    """
    Get complete player profile

    - Full player stats and analytics
    - Opta Performance Index
    - Advanced metrics (if user has access)
    - Market data
    - Counts towards player reports quota
    """
    from core.products import get_plan_features
    from fastapi import HTTPException, status

    # Get services
    data_service = get_data_service()
    opta_service = get_opta_service()

    # Get player data
    player_data = await data_service.get_player_profile(player_id)

    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player not found: {player_id}"
        )

    # Get user features
    features = get_plan_features(user.plan_tier)

    # Extract basic info
    basic_info = player_data.get('basic_info', {})
    perf_stats = player_data.get('performance_stats', {})

    # Create basic stats
    basic_stats = PlayerBasicStats(
        goals=perf_stats.get('goals', 0),
        assists=perf_stats.get('assists', 0),
        minutes_played=perf_stats.get('minutes_played', 0),
        matches=perf_stats.get('matches', 0)
    )

    # Calculate Opta Index
    opta_result = await opta_service.calculate_player_index(
        player_data,
        position=basic_info.get('position', 'MID')
    )

    # Advanced metrics (only if user has access)
    advanced_metrics = None
    if features.advanced_metrics:
        xg_stats = player_data.get('xg_stats', {})
        advanced_metrics = PlayerAdvancedMetrics(
            xg=xg_stats.get('total_xg', perf_stats.get('xg', 0.0)),
            xa=perf_stats.get('xa', 0.0),
            progressive_passes=perf_stats.get('progressive_passes', 0),
            progressive_carries=perf_stats.get('progressive_carries', 0),
            shots_on_target_pct=perf_stats.get('shots_on_target_pct', 0.0)
        )

    # Performance data
    performance = PlayerPerformance(
        opta_index=opta_result.get('opta_index'),
        rating=opta_result.get('rating'),
        basic_stats=basic_stats,
        advanced_metrics=advanced_metrics
    )

    # Market data
    market_info = player_data.get('market_data', {})
    market_data = MarketData(
        market_value=market_info.get('market_value', 10.0),
        currency=market_info.get('currency', 'EUR'),
        contract_expires=market_info.get('contract_expires')
    )

    return PlayerProfile(
        player_id=player_id,
        name=basic_info.get('name', player_data.get('player_name', 'Unknown')),
        age=basic_info.get('age', 25),
        position=basic_info.get('position', 'MID'),
        team=basic_info.get('team', 'Unknown'),
        league=player_data.get('league', 'Unknown'),
        nationality=basic_info.get('nationality', 'Unknown'),
        performance=performance,
        market_data=market_data
    )
