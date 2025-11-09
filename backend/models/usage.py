"""
Usage tracking model
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base


class UsageTracking(Base):
    """Track resource usage per user per month"""
    __tablename__ = "usage_tracking"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Resource type (player_reports_per_month, team_fit_analyses_per_month, etc.)
    resource_type = Column(String, nullable=False, index=True)

    # Usage count
    count = Column(Integer, default=0, nullable=False)

    # Period (monthly tracking)
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="usage_records")

    def __repr__(self):
        return f"<UsageTracking {self.user_id} {self.resource_type}: {self.count}>"
