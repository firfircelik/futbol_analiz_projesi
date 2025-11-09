"""
Analytics schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Optional


class OptaIndexResponse(BaseModel):
    """Response schema for Opta Performance Index"""
    player_id: str
    player_name: str
    index_value: float  # 0-100
    rating: str  # POOR, AVERAGE, GOOD, EXCELLENT
    component_scores: Optional[Dict[str, float]] = None
    season: Optional[str] = None


class TeamFitBreakdown(BaseModel):
    """7-dimensional team fit breakdown"""
    statistical_fit: float  # 0-100
    tactical_fit: float
    personality_fit: float
    chemistry_fit: float
    cultural_fit: float
    budget_fit: float
    age_fit: float


class TeamFitRequest(BaseModel):
    """Request schema for team fit analysis"""
    player_id: str
    team_id: str


class TeamFitResponse(BaseModel):
    """Response schema for team fit analysis"""
    player_id: str
    player_name: str
    team_id: str
    team_name: str
    fit_score: float  # 0-100 overall score
    fit_rating: str  # POOR_FIT, GOOD_FIT, EXCELLENT_FIT
    recommendation: str  # AVOID, MONITOR, BUY, STRONG_BUY
    breakdown: TeamFitBreakdown
    strengths: List[str]
    concerns: List[str]
    adaptation_timeline: str  # IMMEDIATE, SHORT (1-3mo), MEDIUM (3-6mo), LONG (6mo+)


class ComparablePlayer(BaseModel):
    """Comparable player for Moneyball valuation"""
    name: str
    value: float  # EUR millions
    similarity: float  # 0-1


class MoneyballValuationResponse(BaseModel):
    """Response schema for Moneyball player valuation"""
    player_id: str
    player_name: str
    market_value: float  # EUR millions
    calculated_value: float  # EUR millions
    value_ratio: float  # calculated / market
    category: str  # OVERVALUED, FAIR, UNDERVALUED, BARGAIN
    roi_potential: float  # % potential return
    recommendation: str  # SELL, HOLD, BUY, STRONG_BUY
    comparable_players: List[ComparablePlayer]
