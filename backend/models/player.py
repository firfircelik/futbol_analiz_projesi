"""
Player cache model
"""
from sqlalchemy import Column, String, JSON, DateTime, Text
from datetime import datetime
import uuid

from core.database import Base


class PlayerCache(Base):
    """Cache player data from external APIs"""
    __tablename__ = "player_cache"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Player identification
    player_id = Column(String, unique=True, nullable=False, index=True)
    player_name = Column(String, nullable=False, index=True)

    # Cached data (JSON)
    data = Column(JSON, nullable=False)

    # Data source information
    source = Column(String, nullable=False)  # statsbomb, understat, fbref, etc.
    data_quality = Column(String, nullable=True)  # complete, partial, estimated

    # Timestamps
    cached_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PlayerCache {self.player_name} (from {self.source})>"

    @property
    def is_expired(self) -> bool:
        """Check if cached data is expired"""
        return datetime.utcnow() > self.expires_at
