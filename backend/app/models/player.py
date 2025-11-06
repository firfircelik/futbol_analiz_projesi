"""
Player Database Model
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Player(Base):
    __tablename__ = "players"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String(100), unique=True, index=True, nullable=False)

    # Basic Info
    name = Column(String(255), nullable=False, index=True)
    age = Column(Integer)
    nationality = Column(String(100))
    position = Column(String(50), index=True)

    # Relationships
    team_id = Column(Integer, ForeignKey("teams.id"))
    league_id = Column(Integer, ForeignKey("leagues.id"))

    team = relationship("Team", back_populates="players")
    league = relationship("League", back_populates="players")

    # Physical Attributes
    height_cm = Column(Float)
    weight_kg = Column(Float)
    preferred_foot = Column(String(10))

    # Market Data
    market_value_millions = Column(Float)
    contract_expiry = Column(Date)
    wage_weekly_thousands = Column(Float)

    # Performance Metrics (Season)
    matches_played = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)

    # Advanced Passing
    passes_attempted = Column(Integer, default=0)
    passes_completed = Column(Integer, default=0)
    pass_completion_rate = Column(Float, default=0.0)
    key_passes = Column(Integer, default=0)
    progressive_passes = Column(Integer, default=0)
    long_passes = Column(Integer, default=0)
    through_balls = Column(Integer, default=0)

    # Advanced Shooting
    shots = Column(Integer, default=0)
    shots_on_target = Column(Integer, default=0)
    shot_accuracy = Column(Float, default=0.0)
    expected_goals_xg = Column(Float, default=0.0)
    goals_vs_xg = Column(Float, default=0.0)

    # Dribbling
    dribbles_attempted = Column(Integer, default=0)
    dribbles_completed = Column(Integer, default=0)
    dribble_success_rate = Column(Float, default=0.0)
    touches = Column(Integer, default=0)

    # Defensive
    tackles = Column(Integer, default=0)
    interceptions = Column(Integer, default=0)
    clearances = Column(Integer, default=0)
    blocks = Column(Integer, default=0)
    pressures = Column(Integer, default=0)

    # Technical Attributes (0-100)
    pace = Column(Integer, default=75)
    shooting = Column(Integer, default=70)
    passing = Column(Integer, default=70)
    dribbling = Column(Integer, default=70)
    defending = Column(Integer, default=50)
    physical = Column(Integer, default=70)

    # Mental Attributes (0-100)
    decision_making = Column(Integer, default=70)
    composure = Column(Integer, default=70)
    vision = Column(Integer, default=70)
    positioning = Column(Integer, default=70)
    leadership = Column(Integer, default=60)

    # Opta Performance Index
    opta_index = Column(Float, default=65.0)
    form_rating = Column(String(20), default='average')

    # Personality
    personality_type = Column(String(50), default='professional')
    temperament = Column(String(20), default='calm')
    professionalism = Column(Integer, default=80)

    # Data Quality
    data_completeness = Column(Float, default=0.0)
    data_sources = Column(Text)  # Comma-separated list
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Player(name='{self.name}', position='{self.position}', opta_index={self.opta_index})>"
