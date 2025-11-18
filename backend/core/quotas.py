"""
Quota enforcement and tracking
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Tuple

from core.database import get_db
from core.products import PlanTier, get_plan_features, get_upgrade_recommendation
from core.auth import get_current_user


class QuotaExceeded(HTTPException):
    """Custom exception for quota exceeded"""
    def __init__(self, message: str, upgrade_to: str = None):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Quota exceeded",
                "message": message,
                "upgrade_to": upgrade_to
            }
        )


def get_current_usage(user_id: str, resource_type: str, db: Session) -> int:
    """
    Get current usage for a user and resource type this month

    Args:
        user_id: User ID
        resource_type: Type of resource (player_reports_per_month, etc.)
        db: Database session

    Returns:
        Current usage count
    """
    from models.usage import UsageTracking

    # Get start of current month
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    # Query usage for this month
    usage = db.query(UsageTracking).filter(
        UsageTracking.user_id == user_id,
        UsageTracking.resource_type == resource_type,
        UsageTracking.period_start >= month_start
    ).first()

    return usage.count if usage else 0


def increment_usage(user_id: str, resource_type: str, db: Session):
    """
    Increment usage counter for a user and resource type

    Args:
        user_id: User ID
        resource_type: Type of resource
        db: Database session
    """
    from models.usage import UsageTracking

    # Get start of current month
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    month_end = (month_start + timedelta(days=32)).replace(day=1)

    # Get or create usage record
    usage = db.query(UsageTracking).filter(
        UsageTracking.user_id == user_id,
        UsageTracking.resource_type == resource_type,
        UsageTracking.period_start >= month_start
    ).first()

    if usage:
        usage.count += 1
        usage.updated_at = now
    else:
        usage = UsageTracking(
            user_id=user_id,
            resource_type=resource_type,
            count=1,
            period_start=month_start,
            period_end=month_end
        )
        db.add(usage)

    db.commit()


def check_quota_limit(user, resource_type: str, db: Session) -> Tuple[bool, int]:
    """
    Check if user has remaining quota for a resource

    Args:
        user: User object
        resource_type: Type of resource to check
        db: Database session

    Returns:
        Tuple of (has_quota, remaining_count)
    """
    # Get plan features
    features = get_plan_features(user.plan_tier)

    # Get limit for this resource
    limit = getattr(features, resource_type, 0)

    # Unlimited access (999999 or similar)
    if limit >= 999999:
        return True, 999999

    # Get current usage
    current_usage = get_current_usage(user.id, resource_type, db)

    # Check if under limit
    remaining = max(0, limit - current_usage)
    has_quota = remaining > 0

    return has_quota, remaining


async def check_and_increment_quota(
    resource_type: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Dependency that checks quota and increments if available

    Usage:
        @app.get("/players/{id}")
        def get_player(
            player_id: str,
            _: dict = Depends(check_and_increment_quota("player_reports_per_month"))
        ):
            return player_data

    Args:
        resource_type: Type of resource to check

    Raises:
        QuotaExceeded: If user has no remaining quota
    """
    # Check if user has quota
    has_quota, remaining = check_quota_limit(user, resource_type, db)

    if not has_quota:
        upgrade_to = get_upgrade_recommendation(user.plan_tier)
        raise QuotaExceeded(
            message=f"You've reached your monthly limit for {resource_type.replace('_', ' ')}",
            upgrade_to=upgrade_to
        )

    # Increment usage
    increment_usage(user.id, resource_type, db)

    return {"allowed": True, "remaining": remaining - 1}


def check_quota_dependency(resource_type: str):
    """
    Factory function to create quota check dependency

    Usage:
        @app.get("/players/{id}")
        def get_player(
            player_id: str,
            _: dict = Depends(check_quota_dependency("player_reports_per_month"))
        ):
            return player_data
    """
    async def _check_quota(
        user = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return await check_and_increment_quota(resource_type, user, db)

    return _check_quota


# Convenience dependencies for common resources
check_player_reports_quota = check_quota_dependency("player_reports_per_month")
check_team_fit_quota = check_quota_dependency("team_fit_analyses_per_month")
check_api_requests_quota = check_quota_dependency("api_requests_per_month")
