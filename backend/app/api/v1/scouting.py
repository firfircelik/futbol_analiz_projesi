"""
Scouting Reports API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.player import Player
from app.schemas.analytics import ScoutingReportResponse
from src.opta_analytics.scouting_reports import ScoutingReportGenerator

router = APIRouter()


@router.get("/report/{player_id}", response_model=ScoutingReportResponse)
async def get_scouting_report(
    player_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate comprehensive scouting report for a player
    """
    player = db.query(Player).filter(Player.player_id == player_id).first()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Prepare player data
    player_data = {
        'name': player.name,
        'age': player.age,
        'position': player.position,
        'nationality': player.nationality,
        'current_team': player.team.name if player.team else "Unknown",
        'height_cm': player.height_cm,
        'weight_kg': player.weight_kg,
        'preferred_foot': player.preferred_foot,
        'goals': player.goals,
        'assists': player.assists,
        'matches_played': player.matches_played,
        'market_value_millions': player.market_value_millions or 10.0,
        'pace': player.pace,
        'shooting': player.shooting,
        'passing': player.passing,
        'dribbling': player.dribbling,
        'defending': player.defending,
        'physical': player.physical,
        'opta_index': player.opta_index,
        'personality_type': player.personality_type,
        'temperament': player.temperament
    }

    # Generate report
    generator = ScoutingReportGenerator()
    report = generator.generate_player_report(player_data)

    return ScoutingReportResponse(
        player_id=player_id,
        player_name=player.name,
        position=player.position,
        age=player.age,
        current_team=player_data['current_team'],
        executive_summary=report['executive_summary'],
        overall_rating=report['overall_rating'],
        player_profile=report['player_profile'],
        performance_analysis=report['performance_analysis'],
        technical_assessment=report['technical_assessment'],
        physical_profile=report['physical_profile'],
        tactical_analysis=report['tactical_analysis'],
        mental_attributes=report['mental_attributes'],
        market_intelligence=report['market_intelligence'],
        swot=report['swot_analysis'],
        scouting_verdict=report['scouting_verdict'],
        generated_at=datetime.utcnow()
    )


@router.get("/targets")
async def get_scouting_targets(
    position: str = None,
    max_price: float = None,
    min_opta_index: float = 70.0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get recommended scouting targets
    """
    query = db.query(Player).filter(Player.opta_index >= min_opta_index)

    if position:
        query = query.filter(Player.position == position)
    if max_price:
        query = query.filter(Player.market_value_millions <= max_price)

    players = query.order_by(Player.opta_index.desc()).limit(limit).all()

    targets = []
    for player in players:
        targets.append({
            "player_id": player.player_id,
            "name": player.name,
            "position": player.position,
            "age": player.age,
            "team": player.team.name if player.team else "N/A",
            "opta_index": player.opta_index,
            "market_value_millions": player.market_value_millions,
            "potential_rating": "high" if player.opta_index >= 80 else "medium"
        })

    return {
        "total_targets": len(targets),
        "filters_applied": {
            "position": position,
            "max_price": max_price,
            "min_opta_index": min_opta_index
        },
        "targets": targets
    }
