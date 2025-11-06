"""
Team Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TeamBase(BaseModel):
    """Base team schema"""

    name: str = Field(..., min_length=1, max_length=255)
    league_id: Optional[int] = None
    stadium: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class TeamCreate(TeamBase):
    """Schema for creating a team"""

    team_id: str = Field(..., min_length=1, max_length=100)


class TeamResponse(TeamBase):
    """Schema for team responses"""

    id: int
    team_id: str

    # Tactical
    playing_style: Optional[str] = None
    formation: Optional[str] = None
    manager: Optional[str] = None

    # Performance
    matches_played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class TeamProfile(BaseModel):
    """Team profile for Team Fit Analyzer"""

    team_name: str
    playing_style: str = Field(..., description="possession, counter_attack, high_press, etc.")
    formation: str
    budget_millions: float
    priority_positions: List[str]
    desired_traits: List[str]
    requires_pace: bool = False
    requires_technique: bool = False
    average_age: Optional[float] = None
    squad_size: Optional[int] = None


class TeamStatsResponse(BaseModel):
    """Schema for team statistics"""

    team_id: str
    team_name: str
    league: str

    # Performance
    matches_played: int
    wins: int
    draws: int
    losses: int
    win_percentage: float
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int

    # Advanced
    possession_avg: Optional[float] = None
    shots_per_game: Optional[float] = None
    xg_for: Optional[float] = None
    xg_against: Optional[float] = None

    # Form
    form_last_5: str  # e.g., "WWDLW"
    position: Optional[int] = None
