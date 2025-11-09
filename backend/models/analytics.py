"""
Analytics results models
"""
from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base


class OptaIndexHistory(Base):
    """Store Opta Performance Index calculations"""
    __tablename__ = "opta_index_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Player reference
    player_id = Column(String, nullable=False, index=True)
    player_name = Column(String, nullable=False)

    # Opta Index value (0-100)
    index_value = Column(Float, nullable=False)
    rating = Column(String, nullable=False)  # POOR, AVERAGE, GOOD, EXCELLENT

    # Component scores (stored as JSON)
    component_scores = Column(JSON, nullable=True)

    # Metadata
    season = Column(String, nullable=True)
    competition = Column(String, nullable=True)

    # Timestamps
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<OptaIndex {self.player_name}: {self.index_value} ({self.rating})>"


class TeamFitAnalysis(Base):
    """Store Team Fit Analysis results"""
    __tablename__ = "team_fit_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Player and team references
    player_id = Column(String, nullable=False, index=True)
    player_name = Column(String, nullable=False)
    team_id = Column(String, nullable=False, index=True)
    team_name = Column(String, nullable=False)

    # Fit score (0-100)
    fit_score = Column(Float, nullable=False)
    fit_rating = Column(String, nullable=False)  # POOR_FIT, GOOD_FIT, EXCELLENT_FIT
    recommendation = Column(String, nullable=False)  # AVOID, MONITOR, BUY, STRONG_BUY

    # 7-dimensional breakdown
    breakdown = Column(JSON, nullable=False)  # statistical_fit, tactical_fit, etc.

    # Insights
    strengths = Column(JSON, nullable=True)
    concerns = Column(JSON, nullable=True)
    adaptation_timeline = Column(String, nullable=True)

    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<TeamFit {self.player_name} → {self.team_name}: {self.fit_score}>"


class MoneyballValuation(Base):
    """Store Moneyball player valuations"""
    __tablename__ = "moneyball_valuations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Player reference
    player_id = Column(String, nullable=False, index=True)
    player_name = Column(String, nullable=False)

    # Valuation
    market_value = Column(Float, nullable=False)  # Current market value (EUR millions)
    calculated_value = Column(Float, nullable=False)  # Our calculated value
    value_ratio = Column(Float, nullable=False)  # calculated / market

    # Classification
    category = Column(String, nullable=False)  # OVERVALUED, FAIR, UNDERVALUED, BARGAIN
    roi_potential = Column(Float, nullable=False)  # % return potential
    recommendation = Column(String, nullable=False)  # SELL, HOLD, BUY, STRONG_BUY

    # Comparable players
    comparables = Column(JSON, nullable=True)

    # Timestamps
    valuated_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<MoneyballValuation {self.player_name}: €{self.market_value}M → €{self.calculated_value}M ({self.category})>"
