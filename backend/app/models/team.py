"""
Team and League Database Models
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(String(100), unique=True, index=True, nullable=False)

    name = Column(String(255), nullable=False)
    sport = Column(String(50), nullable=False)  # 'football' or 'basketball'
    country = Column(String(100))
    prestige = Column(String(20))  # 'elite', 'high', 'medium', 'emerging'

    # External IDs
    thesportsdb_id = Column(String(100))
    competition_id = Column(String(100))

    # Relationships
    teams = relationship("Team", back_populates="league")
    players = relationship("Player", back_populates="league")

    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<League(name='{self.name}', sport='{self.sport}')>"


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String(100), unique=True, index=True, nullable=False)

    name = Column(String(255), nullable=False, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    # Relationships
    league = relationship("League", back_populates="teams")
    players = relationship("Player", back_populates="team")

    # Basic Info
    stadium = Column(String(255))
    founded_year = Column(Integer)
    city = Column(String(100))
    country = Column(String(100))

    # Tactical Info
    playing_style = Column(String(50))  # 'possession', 'counter_attack', 'high_press', etc.
    formation = Column(String(20))
    manager = Column(String(255))

    # Performance (Current Season)
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    goals_for = Column(Integer, default=0)
    goals_against = Column(Integer, default=0)
    points = Column(Integer, default=0)

    # Financial (optional)
    budget_millions = Column(Float)

    # Team Profile (for Team Fit)
    priority_positions = Column(Text)  # Comma-separated
    desired_traits = Column(Text)  # Comma-separated

    # External IDs
    thesportsdb_id = Column(String(100))

    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Team(name='{self.name}', league='{self.league.name if self.league else 'N/A'}')>"
