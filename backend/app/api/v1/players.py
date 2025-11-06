"""
Player API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerResponse, PlayerDetailed, PlayerSearch, PlayerCompare, PlayerStatsResponse
from src.data_collection.comprehensive_data_aggregator import ComprehensiveDataAggregator

router = APIRouter()

# Initialize data aggregator
data_aggregator = ComprehensiveDataAggregator()


@router.get("/", response_model=List[PlayerResponse])
async def list_players(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    position: Optional[str] = None,
    league_id: Optional[int] = None,
    min_opta_index: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """
    List players with optional filters
    """
    query = db.query(Player)

    if position:
        query = query.filter(Player.position == position)
    if league_id:
        query = query.filter(Player.league_id == league_id)
    if min_opta_index:
        query = query.filter(Player.opta_index >= min_opta_index)

    players = query.offset(skip).limit(limit).all()
    return players


@router.get("/{player_id}", response_model=PlayerDetailed)
async def get_player(
    player_id: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed player information
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@router.get("/{player_id}/stats", response_model=PlayerStatsResponse)
async def get_player_stats(
    player_id: str,
    season: str = "2023-24",
    db: Session = Depends(get_db)
):
    """
    Get player statistics with advanced metrics
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Calculate per 90 stats
    minutes = player.minutes_played if player.minutes_played > 0 else 1
    games_90 = minutes / 90

    goals_per_90 = player.goals / games_90 if games_90 > 0 else 0
    assists_per_90 = player.assists / games_90 if games_90 > 0 else 0
    shots_per_90 = player.shots / games_90 if games_90 > 0 else 0
    key_passes_per_90 = player.key_passes / games_90 if games_90 > 0 else 0

    # Calculate trend (simple logic - could be more sophisticated)
    trend = "stable"
    if player.form_rating == "excellent":
        trend = "improving"
    elif player.form_rating == "poor":
        trend = "declining"

    return PlayerStatsResponse(
        player_id=player.player_id,
        player_name=player.name,
        season=season,
        matches_played=player.matches_played,
        minutes_played=player.minutes_played,
        goals=player.goals,
        assists=player.assists,
        goals_per_90=round(goals_per_90, 2),
        assists_per_90=round(assists_per_90, 2),
        shots_per_90=round(shots_per_90, 2),
        key_passes_per_90=round(key_passes_per_90, 2),
        trend=trend
    )


@router.post("/search", response_model=List[PlayerResponse])
async def search_players(
    search: PlayerSearch,
    db: Session = Depends(get_db)
):
    """
    Advanced player search with multiple filters
    """
    query = db.query(Player)

    if search.query:
        query = query.filter(Player.name.ilike(f"%{search.query}%"))
    if search.position:
        query = query.filter(Player.position == search.position)
    if search.league_id:
        query = query.filter(Player.league_id == search.league_id)
    if search.team_id:
        query = query.filter(Player.team_id == search.team_id)
    if search.min_age:
        query = query.filter(Player.age >= search.min_age)
    if search.max_age:
        query = query.filter(Player.age <= search.max_age)
    if search.min_opta_index:
        query = query.filter(Player.opta_index >= search.min_opta_index)
    if search.min_market_value:
        query = query.filter(Player.market_value_millions >= search.min_market_value)
    if search.max_market_value:
        query = query.filter(Player.market_value_millions <= search.max_market_value)

    # Pagination
    skip = (search.page - 1) * search.page_size
    players = query.offset(skip).limit(search.page_size).all()

    return players


@router.post("/compare")
async def compare_players(
    compare: PlayerCompare,
    db: Session = Depends(get_db)
):
    """
    Compare multiple players side-by-side
    """
    players = db.query(Player).filter(Player.player_id.in_(compare.player_ids)).all()

    if len(players) < 2:
        raise HTTPException(status_code=404, detail="Need at least 2 players to compare")

    # Build comparison
    comparison = {
        "players": [],
        "comparison_metrics": {},
        "best_at": {}
    }

    metrics = [
        "opta_index", "goals", "assists", "pace", "shooting", "passing",
        "dribbling", "defending", "physical", "market_value_millions"
    ]

    for player in players:
        player_data = {
            "player_id": player.player_id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team": player.team.name if player.team else "N/A",
            "metrics": {metric: getattr(player, metric, 0) for metric in metrics}
        }
        comparison["players"].append(player_data)

    # Find best at each metric
    for metric in metrics:
        best_player = max(players, key=lambda p: getattr(p, metric, 0))
        comparison["best_at"][metric] = best_player.name

    return comparison


@router.get("/{player_id}/analytics")
async def get_player_analytics(
    player_id: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive analytics for a player
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Try to get fresh data from aggregator
    try:
        comprehensive_data = data_aggregator.get_comprehensive_player_data(
            player.name,
            sport='football' if player.league and player.league.sport == 'football' else 'basketball',
            league=player.league.name if player.league else None
        )

        return {
            "player_id": player.player_id,
            "name": player.name,
            "comprehensive_data": comprehensive_data,
            "data_freshness": "live"
        }
    except Exception as e:
        # Fallback to database data
        return {
            "player_id": player.player_id,
            "name": player.name,
            "data_freshness": "cached",
            "error": str(e)
        }
