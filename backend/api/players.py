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

# TODO: Import real services in Phase 2
# from services.data_service import DataService
# from services.opta_service import OptaService


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
    # TODO Phase 2: Connect to real DataService
    # data_service = DataService()
    # results = await data_service.search_players(query, league, position)

    # TEMPORARY: Mock data for Phase 1
    mock_results = [
        PlayerSearchResult(
            player_id="player_messi",
            name="Lionel Messi",
            team="Inter Miami",
            position="RW",
            league="MLS",
            opta_index=85.2,
            market_value=25.0,
            nationality="Argentina"
        ),
        PlayerSearchResult(
            player_id="player_haaland",
            name="Erling Haaland",
            team="Manchester City",
            position="ST",
            league="Premier League",
            opta_index=92.8,
            market_value=180.0,
            nationality="Norway"
        )
    ]

    # Filter by query (case-insensitive)
    filtered_results = [
        r for r in mock_results
        if query.lower() in r.name.lower()
    ]

    # Filter by league if specified
    if league:
        filtered_results = [r for r in filtered_results if r.league == league]

    # Filter by position if specified
    if position:
        filtered_results = [r for r in filtered_results if r.position == position]

    return PlayerSearchResponse(
        query=query,
        results=filtered_results,
        total=len(filtered_results)
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
    # TODO Phase 2: Connect to real DataService and OptaService
    # data_service = DataService()
    # opta_service = OptaService()
    #
    # player_data = await data_service.get_player_profile(player_id)
    # opta_index = opta_service.calculate_index(player_data)

    # TEMPORARY: Mock data for Phase 1
    from core.products import get_plan_features
    features = get_plan_features(user.plan_tier)

    # Basic stats
    basic_stats = PlayerBasicStats(
        goals=18,
        assists=12,
        minutes_played=2847,
        matches=32
    )

    # Advanced metrics (only if user has access)
    advanced_metrics = None
    if features.advanced_metrics:
        advanced_metrics = PlayerAdvancedMetrics(
            xg=16.8,
            xa=9.3,
            progressive_passes=156,
            progressive_carries=89,
            shots_on_target_pct=62.5
        )

    # Performance data
    performance = PlayerPerformance(
        opta_index=85.2,
        rating="EXCELLENT",
        basic_stats=basic_stats,
        advanced_metrics=advanced_metrics
    )

    # Market data
    market_data = MarketData(
        market_value=65.0,
        currency="EUR",
        contract_expires="2025-06-30"
    )

    return PlayerProfile(
        player_id=player_id,
        name="Mohamed Salah",
        age=31,
        position="RW",
        team="Liverpool FC",
        league="Premier League",
        nationality="Egypt",
        performance=performance,
        market_data=market_data
    )
