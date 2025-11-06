"""
Match Database Model
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String(100), unique=True, index=True, nullable=False)

    league_id = Column(Integer, ForeignKey("leagues.id"))
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))

    # Relationships
    league = relationship("League")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])

    # Match Info
    match_date = Column(DateTime, nullable=False, index=True)
    status = Column(String(20), default='scheduled')  # 'scheduled', 'live', 'finished', 'postponed'

    # Scores
    home_score = Column(Integer)
    away_score = Column(Integer)

    # Advanced Stats
    home_possession = Column(Integer)  # Percentage
    away_possession = Column(Integer)

    home_shots = Column(Integer)
    away_shots = Column(Integer)

    home_shots_on_target = Column(Integer)
    away_shots_on_target = Column(Integer)

    home_xg = Column(Float)  # Expected Goals
    away_xg = Column(Float)

    # Metadata
    venue = Column(String(255))
    attendance = Column(Integer)
    referee = Column(String(255))

    # External IDs
    thesportsdb_id = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Match({self.home_team.name if self.home_team else 'TBD'} vs {self.away_team.name if self.away_team else 'TBD'}, {self.match_date})>"
