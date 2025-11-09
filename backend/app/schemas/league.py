"""
League Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class LeagueBase(BaseModel):
    """Base league schema"""

    name: str = Field(..., min_length=1, max_length=255)
    sport: str = Field(..., pattern="^(football|basketball)$")
    country: Optional[str] = None
    prestige: Optional[str] = Field(None, pattern="^(elite|high|medium|emerging)$")


class LeagueCreate(LeagueBase):
    """Schema for creating a league"""

    league_id: str = Field(..., min_length=1, max_length=100)


class LeagueResponse(LeagueBase):
    """Schema for league responses"""

    id: int
    league_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeagueWithTeamsResponse(LeagueResponse):
    """League with teams"""

    teams: List[dict] = []
    total_teams: int = 0


class LeagueStandingsResponse(BaseModel):
    """League standings"""

    league_id: str
    league_name: str
    season: str

    standings: List[dict]  # List of team standings


class LiveScoreResponse(BaseModel):
    """Live score schema"""

    match_id: str
    league: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str  # 'live', 'finished', 'scheduled'
    minute: Optional[int] = None
    match_date: datetime
