"""
Analytics Cache Database Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.database import Base


class AnalyticsCache(Base):
    __tablename__ = "analytics_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, index=True, nullable=False)

    # Cache metadata
    cache_type = Column(String(50), index=True)  # 'opta_index', 'team_fit', 'xg', 'scouting', 'moneyball'
    entity_id = Column(String(100), index=True)  # player_id, team_id, match_id, etc.

    # Cached data (JSON)
    data = Column(JSONB, nullable=False)  # For PostgreSQL
    # data = Column(Text, nullable=False)  # For SQLite, would need JSON serialization

    # Expiration
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<AnalyticsCache(type='{self.cache_type}', entity='{self.entity_id}')>"
