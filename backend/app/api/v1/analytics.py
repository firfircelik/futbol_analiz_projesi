"""
Analytics API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.player import Player
from app.schemas.analytics import OptaIndexResponse, XGResponse
from src.opta_analytics.performance_index import OptaPerformanceIndex, PerformanceMetrics
from src.opta_analytics.expected_goals import ExpectedGoalsEngine, ShotContext

router = APIRouter()


@router.get("/opta-index/{player_id}", response_model=OptaIndexResponse)
async def get_opta_index(
    player_id: str,
    db: Session = Depends(get_db)
):
    """
    Get Opta Performance Index for a player
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Create metrics from player data
    metrics = PerformanceMetrics(
        goals=player.goals,
        assists=player.assists,
        passes_completed=player.passes_completed,
        passes_attempted=player.passes_attempted,
        tackles=player.tackles,
        interceptions=player.interceptions,
        shots=player.shots,
        shots_on_target=player.shots_on_target,
        dribbles_completed=player.dribbles_completed,
        clearances=player.clearances,
        blocks=player.blocks,
        key_passes=player.key_passes,
        progressive_passes=player.progressive_passes
    )

    # Calculate index
    opta_calculator = OptaPerformanceIndex()
    result = opta_calculator.calculate_index(metrics, player.position)

    # Determine rating
    index = result['opta_index']
    if index >= 85:
        rating = "world_class"
    elif index >= 75:
        rating = "excellent"
    elif index >= 65:
        rating = "good"
    elif index >= 50:
        rating = "average"
    else:
        rating = "poor"

    return OptaIndexResponse(
        player_id=player_id,
        player_name=player.name,
        position=player.position,
        opta_index=result['opta_index'],
        rating=rating,
        breakdown=result['breakdown'],
        strengths=result['top_contributions'][:3],
        weaknesses=[]
    )


@router.post("/xg")
async def calculate_xg(
    shot_data: dict
):
    """
    Calculate Expected Goals (xG) for a shot or match
    """
    xg_engine = ExpectedGoalsEngine()

    # If single shot
    if 'distance_to_goal' in shot_data:
        shot = ShotContext(**shot_data)
        result = xg_engine.calculate_xg(shot)
        return result

    # If multiple shots
    if 'shots' in shot_data:
        shots = [ShotContext(**s) for s in shot_data['shots']]
        match_xg = xg_engine.calculate_match_xg(shots, shot_data.get('team', 'Team'))
        return match_xg

    raise HTTPException(status_code=400, detail="Invalid shot data format")
