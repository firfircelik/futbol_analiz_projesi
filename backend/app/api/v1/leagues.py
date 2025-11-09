"""
League API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.team import League
from app.schemas.league import LeagueResponse
from config.config_loader import ConfigLoader

router = APIRouter()
config_loader = ConfigLoader()


@router.get("/", response_model=List[LeagueResponse])
async def list_leagues(
    sport: str = None,
    db: Session = Depends(get_db)
):
    """List all available leagues"""
    query = db.query(League)

    if sport:
        query = query.filter(League.sport == sport)

    return query.all()


@router.get("/{league_id}", response_model=LeagueResponse)
async def get_league(
    league_id: str,
    db: Session = Depends(get_db)
):
    """Get league details"""
    league = db.query(League).filter(League.league_id == league_id).first()

    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    return league


@router.get("/{league_id}/standings")
async def get_league_standings(
    league_id: str,
    season: str = "2023-24",
    db: Session = Depends(get_db)
):
    """Get league standings"""
    league = db.query(League).filter(League.league_id == league_id).first()

    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    # Get teams in league ordered by points
    from app.models.team import Team
    teams = db.query(Team).filter(Team.league_id == league.id).order_by(Team.points.desc()).all()

    standings = []
    for idx, team in enumerate(teams, 1):
        standings.append({
            "position": idx,
            "team_name": team.name,
            "matches_played": team.matches_played,
            "wins": team.wins,
            "draws": team.draws,
            "losses": team.losses,
            "goals_for": team.goals_for,
            "goals_against": team.goals_against,
            "goal_difference": team.goals_for - team.goals_against,
            "points": team.points
        })

    return {
        "league_id": league_id,
        "league_name": league.name,
        "season": season,
        "standings": standings
    }
