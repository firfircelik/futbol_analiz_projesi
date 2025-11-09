"""
User schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Dict, Any


class QuotaInfo(BaseModel):
    """Quota information for a resource"""
    used: int
    limit: int
    remaining: int


class UserQuotas(BaseModel):
    """All quotas for a user"""
    player_reports: QuotaInfo
    team_fit: QuotaInfo
    api_requests: QuotaInfo


class PlanInfo(BaseModel):
    """User's plan information"""
    tier: str
    name: str
    price_monthly: float


class UserResponse(BaseModel):
    """Response schema for user information"""
    user_id: str
    email: EmailStr
    full_name: str = None
    plan: PlanInfo
    quotas: UserQuotas
    features: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
