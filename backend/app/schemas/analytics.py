"""
Analytics Pydantic Schemas
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class OptaIndexResponse(BaseModel):
    """Opta Performance Index response"""

    player_id: str
    player_name: str
    position: str

    opta_index: float = Field(..., ge=0, le=100)
    rating: str  # 'world_class', 'excellent', 'good', 'average', 'poor'

    breakdown: Dict[str, float]  # Component scores
    strengths: List[str]
    weaknesses: List[str]

    percentile_league: Optional[int] = None  # Percentile in league
    percentile_position: Optional[int] = None  # Percentile in position


class XGResponse(BaseModel):
    """Expected Goals (xG) response"""

    match_id: Optional[str] = None
    player_id: Optional[str] = None

    xg: float
    actual_goals: int
    performance: str  # 'overperforming', 'as_expected', 'underperforming'

    shot_breakdown: List[Dict] = []  # Individual shot xG values


class TeamFitRequest(BaseModel):
    """Request for Team Fit Analysis"""

    player_id: str
    team_profile: Dict  # TeamProfile as dict

    include_alternatives: bool = False
    max_alternatives: int = Field(5, ge=1, le=20)


class TeamFitResponse(BaseModel):
    """Team Fit Analysis response"""

    player_id: str
    player_name: str
    team_name: str

    overall_fit_score: float = Field(..., ge=0, le=100)
    fit_rating: str  # 'EXCELLENT_FIT', 'GOOD_FIT', 'AVERAGE_FIT', 'POOR_FIT'
    recommendation: str  # 'STRONG_BUY', 'BUY', 'MONITOR', 'PASS'

    # 7-dimensional scores
    statistical_fit: float
    tactical_fit: float
    personality_fit: float
    chemistry_fit: float
    cultural_fit: float
    budget_fit: float
    age_fit: float

    # Details
    key_strengths: List[str]
    key_concerns: List[str]
    adaptation_timeline: str  # 'IMMEDIATE', 'SHORT', 'MEDIUM', 'LONG'

    # Alternatives (if requested)
    alternatives: List[Dict] = []


class TeamFitBatchRequest(BaseModel):
    """Batch team fit analysis"""

    league: str
    position: str
    team_profile: Dict
    top_n: int = Field(10, ge=1, le=50)


class ScoutingReportResponse(BaseModel):
    """Scouting Report response"""

    player_id: str
    player_name: str
    position: str
    age: int
    current_team: str

    # Executive Summary
    executive_summary: str
    overall_rating: float = Field(..., ge=0, le=100)

    # Player Profile
    player_profile: Dict

    # Performance Analysis
    performance_analysis: Dict

    # Technical Assessment
    technical_assessment: Dict

    # Physical Profile
    physical_profile: Dict

    # Tactical Analysis
    tactical_analysis: Dict

    # Mental Attributes
    mental_attributes: Dict

    # Market Intelligence
    market_intelligence: Dict

    # SWOT Analysis
    swot: Dict  # {'strengths': [], 'weaknesses': [], 'opportunities': [], 'threats': []}

    # Final Verdict
    scouting_verdict: Dict

    generated_at: datetime


class MoneyballAnalysis(BaseModel):
    """Moneyball valuation analysis"""

    player_id: str
    player_name: str
    position: str

    # Valuation
    estimated_market_value: float
    actual_market_value: float
    value_ratio: float  # performance / price

    # Classification
    valuation_status: str  # 'undervalued', 'fair_value', 'overvalued'
    roi_potential: str  # 'high', 'medium', 'low'

    # Performance metrics
    performance_score: float
    consistency_score: float
    potential_score: float

    # Recommendations
    recommendation: str
    target_price: Optional[float] = None
    reasoning: str

    # Comparisons
    similar_players: List[Dict] = []


class PlayerComparisonResponse(BaseModel):
    """Compare multiple players"""

    players: List[Dict]  # List of player data
    comparison_metrics: Dict  # Side-by-side metrics
    best_at: Dict  # Which player is best at each metric
    recommendation: Optional[str] = None
