"""
Player schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict


class PlayerSearchResult(BaseModel):
    """Single player in search results"""
    player_id: str
    name: str
    team: str
    position: str
    league: str
    opta_index: Optional[float] = None
    market_value: Optional[float] = None  # in EUR millions
    nationality: Optional[str] = None


class PlayerSearchResponse(BaseModel):
    """Response schema for player search"""
    query: str
    results: List[PlayerSearchResult]
    total: int


class PlayerBasicStats(BaseModel):
    """Basic player statistics"""
    goals: int = 0
    assists: int = 0
    minutes_played: int = 0
    matches: int = 0


class PlayerAdvancedMetrics(BaseModel):
    """Advanced metrics (xG, xA, etc.)"""
    xg: float = 0.0
    xa: float = 0.0
    progressive_passes: int = 0
    progressive_carries: int = 0
    shots_on_target_pct: float = 0.0


class PlayerPerformance(BaseModel):
    """Player performance data"""
    opta_index: Optional[float] = None
    rating: Optional[str] = None  # POOR, AVERAGE, GOOD, EXCELLENT
    basic_stats: PlayerBasicStats
    advanced_metrics: Optional[PlayerAdvancedMetrics] = None


class MarketData(BaseModel):
    """Player market value data"""
    market_value: float  # EUR millions
    currency: str = "EUR"
    contract_expires: Optional[str] = None


class PlayerProfile(BaseModel):
    """Complete player profile"""
    player_id: str
    name: str
    age: int
    position: str
    team: str
    league: str
    nationality: str
    performance: PlayerPerformance
    market_data: MarketData

    class Config:
        from_attributes = True
