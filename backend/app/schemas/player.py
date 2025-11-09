"""
Player Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


class PlayerBase(BaseModel):
    """Base player schema"""

    name: str = Field(..., min_length=1, max_length=255)
    age: Optional[int] = Field(None, ge=15, le=50)
    nationality: Optional[str] = None
    position: str
    team_id: Optional[int] = None
    league_id: Optional[int] = None


class PlayerCreate(PlayerBase):
    """Schema for creating a player"""

    player_id: str = Field(..., min_length=1, max_length=100)


class PlayerResponse(PlayerBase):
    """Schema for player responses"""

    id: int
    player_id: str

    # Physical
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    preferred_foot: Optional[str] = None

    # Market
    market_value_millions: Optional[float] = None
    contract_expiry: Optional[date] = None

    # Performance
    matches_played: int = 0
    goals: int = 0
    assists: int = 0
    minutes_played: int = 0

    # Advanced stats
    passes_completed: int = 0
    passes_attempted: int = 0
    pass_completion_rate: float = 0.0
    shots: int = 0
    shots_on_target: int = 0
    expected_goals_xg: float = 0.0

    # Attributes
    pace: int = 75
    shooting: int = 70
    passing: int = 70
    dribbling: int = 70
    defending: int = 50
    physical: int = 70

    # Analytics
    opta_index: float = 65.0
    form_rating: str = 'average'

    # Metadata
    data_completeness: float = 0.0
    last_updated: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class PlayerDetailed(PlayerResponse):
    """Detailed player schema with all statistics"""

    # All passing stats
    key_passes: int = 0
    progressive_passes: int = 0
    long_passes: int = 0
    through_balls: int = 0

    # All shooting stats
    shot_accuracy: float = 0.0
    goals_vs_xg: float = 0.0

    # Dribbling
    dribbles_attempted: int = 0
    dribbles_completed: int = 0
    dribble_success_rate: float = 0.0
    touches: int = 0

    # Defensive
    tackles: int = 0
    interceptions: int = 0
    clearances: int = 0
    blocks: int = 0
    pressures: int = 0

    # Mental attributes
    decision_making: int = 70
    composure: int = 70
    vision: int = 70
    positioning: int = 70
    leadership: int = 60

    # Personality
    personality_type: str = 'professional'
    temperament: str = 'calm'
    professionalism: int = 80


class PlayerSearch(BaseModel):
    """Schema for player search"""

    query: Optional[str] = None
    position: Optional[str] = None
    league_id: Optional[int] = None
    team_id: Optional[int] = None
    min_age: Optional[int] = Field(None, ge=15)
    max_age: Optional[int] = Field(None, le=50)
    min_opta_index: Optional[float] = Field(None, ge=0, le=100)
    min_market_value: Optional[float] = None
    max_market_value: Optional[float] = None

    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class PlayerCompare(BaseModel):
    """Schema for comparing multiple players"""

    player_ids: List[str] = Field(..., min_items=2, max_items=6)


class PlayerStatsResponse(BaseModel):
    """Schema for player statistics"""

    player_id: str
    player_name: str
    season: str

    # Core stats
    matches_played: int
    minutes_played: int
    goals: int
    assists: int

    # Per 90 minutes stats
    goals_per_90: float
    assists_per_90: float
    shots_per_90: float
    key_passes_per_90: float

    # Percentiles (compared to league)
    goals_percentile: Optional[int] = None
    assists_percentile: Optional[int] = None
    passing_percentile: Optional[int] = None

    # Form
    last_5_games_rating: Optional[float] = None
    trend: str = 'stable'  # 'improving', 'stable', 'declining'
