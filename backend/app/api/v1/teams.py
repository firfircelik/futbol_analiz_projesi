"""
Team API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import sys
sys.path.append('../../..')

from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamResponse, TeamStatsResponse

router = APIRouter()


@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    league_id: int = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """List all teams"""
    query = db.query(Team)

    if league_id:
        query = query.filter(Team.league_id == league_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    db: Session = Depends(get_db)
):
    """Get team details"""
    team = db.query(Team).filter(Team.team_id == team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team


@router.get("/{team_id}/players")
async def get_team_players(
    team_id: str,
    db: Session = Depends(get_db)
):
    """Get all players in a team"""
    from app.models.player import Player

    team = db.query(Team).filter(Team.team_id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    players = db.query(Player).filter(Player.team_id == team.id).all()

    return {
        "team_id": team_id,
        "team_name": team.name,
        "total_players": len(players),
        "players": players
    }


@router.get("/{team_id}/stats", response_model=TeamStatsResponse)
async def get_team_stats(
    team_id: str,
    db: Session = Depends(get_db)
):
    """Get team statistics"""
    team = db.query(Team).filter(Team.team_id == team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    win_pct = (team.wins / team.matches_played * 100) if team.matches_played > 0 else 0

    return TeamStatsResponse(
        team_id=team_id,
        team_name=team.name,
        league=team.league.name if team.league else "Unknown",
        matches_played=team.matches_played,
        wins=team.wins,
        draws=team.draws,
        losses=team.losses,
        win_percentage=round(win_pct, 2),
        goals_for=team.goals_for,
        goals_against=team.goals_against,
        goal_difference=team.goals_for - team.goals_against,
        points=team.points,
        form_last_5="N/A"  # Would calculate from recent matches
    )
