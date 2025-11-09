"""
ScoutAI - FastAPI Application
Production-ready SaaS API for sports analytics
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional
import os
from datetime import datetime

# App configuration
from app.config.products import (
    PlanTier, get_plan, get_plan_features,
    check_usage_limit, get_upgrade_recommendation
)

# Initialize FastAPI
app = FastAPI(
    title="ScoutAI API",
    description="Professional Sports Analytics API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()


# =====================================================
# AUTHENTICATION & AUTHORIZATION
# =====================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Validate JWT token and return current user.

    In production, this would:
    1. Decode JWT token
    2. Validate signature
    3. Check expiration
    4. Load user from database
    """
    token = credentials.credentials

    # TODO: Implement real JWT validation
    # For now, return mock user
    return {
        "user_id": "user_123",
        "email": "demo@scoutai.com",
        "plan_tier": PlanTier.PROFESSIONAL,
        "created_at": datetime.now(),
        "usage": {
            "player_reports_per_month": 45,
            "team_fit_analyses_per_month": 12,
            "api_requests_per_month": 3456,
        }
    }


async def check_feature_access(
    feature: str,
    user: dict = Depends(get_current_user)
):
    """Check if user has access to a feature."""
    from app.config.products import can_access_feature

    if not can_access_feature(user["plan_tier"], feature):
        upgrade_to = get_upgrade_recommendation(user["plan_tier"], feature)
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "error": "Feature not available in your plan",
                "feature": feature,
                "current_plan": user["plan_tier"],
                "upgrade_to": upgrade_to,
                "message": f"Upgrade to {upgrade_to} to access {feature}"
            }
        )
    return True


async def check_usage_quota(
    usage_type: str,
    user: dict = Depends(get_current_user)
):
    """Check if user has remaining quota."""
    current_usage = user["usage"].get(usage_type, 0)
    allowed, remaining = check_usage_limit(user["plan_tier"], usage_type, current_usage)

    if not allowed:
        upgrade_to = get_upgrade_recommendation(user["plan_tier"])
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Usage limit exceeded",
                "usage_type": usage_type,
                "limit_reached": True,
                "upgrade_to": upgrade_to,
                "message": f"You've reached your monthly limit. Upgrade to {upgrade_to} for more."
            }
        )

    return {"allowed": True, "remaining": remaining}


# =====================================================
# API ENDPOINTS
# =====================================================

@app.get("/")
async def root():
    """API health check."""
    return {
        "service": "ScoutAI API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/v1/pricing")
async def get_pricing():
    """Get all pricing plans."""
    from app.config.products import PLANS

    plans_data = []
    for tier, plan in PLANS.items():
        plans_data.append({
            "tier": tier,
            "name": plan["pricing"].name,
            "description": plan["pricing"].description,
            "price_monthly": plan["pricing"].price_monthly_eur,
            "price_yearly": plan["pricing"].price_yearly_eur,
            "savings_percent": plan["pricing"].yearly_savings_percent,
            "features": {
                "player_reports": plan["features"].player_reports_per_month,
                "leagues": plan["features"].leagues_access,
                "team_fit": plan["features"].team_fit_analyses_per_month,
                "api_requests": plan["features"].api_requests_per_month,
                "advanced_metrics": plan["features"].advanced_metrics,
                "moneyball": plan["features"].moneyball_valuation,
            },
            "popular": plan.get("popular", False),
            "recommended": plan.get("recommended", False),
        })

    return {"plans": plans_data}


@app.get("/api/v1/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):
    """Get current user information and plan details."""
    plan = get_plan(user["plan_tier"])
    features = get_plan_features(user["plan_tier"])

    # Calculate remaining quotas
    usage = user["usage"]
    quotas = {
        "player_reports": {
            "used": usage.get("player_reports_per_month", 0),
            "limit": features.player_reports_per_month,
            "remaining": max(0, features.player_reports_per_month - usage.get("player_reports_per_month", 0))
        },
        "team_fit": {
            "used": usage.get("team_fit_analyses_per_month", 0),
            "limit": features.team_fit_analyses_per_month,
            "remaining": max(0, features.team_fit_analyses_per_month - usage.get("team_fit_analyses_per_month", 0))
        },
        "api_requests": {
            "used": usage.get("api_requests_per_month", 0),
            "limit": features.api_requests_per_month,
            "remaining": max(0, features.api_requests_per_month - usage.get("api_requests_per_month", 0))
        }
    }

    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "plan": {
            "tier": user["plan_tier"],
            "name": plan["pricing"].name,
            "price_monthly": plan["pricing"].price_monthly_eur,
        },
        "quotas": quotas,
        "features": {
            "advanced_metrics": features.advanced_metrics,
            "moneyball_valuation": features.moneyball_valuation,
            "pdf_exports": features.pdf_exports,
            "api_access": features.api_access,
        }
    }


@app.get("/api/v1/players/search")
async def search_players(
    query: str,
    league: Optional[str] = None,
    user: dict = Depends(get_current_user),
    _: dict = Depends(check_usage_quota("api_requests_per_month"))
):
    """
    Search for players.

    Requires: API access
    Counts towards: API request quota
    """
    # TODO: Implement real search using unified data aggregator

    return {
        "query": query,
        "league": league,
        "results": [
            {
                "player_id": "player_1",
                "name": "Lionel Messi",
                "team": "Inter Miami",
                "position": "FWD",
                "opta_index": 82.5,
                "market_value": 25.0,
            },
            {
                "player_id": "player_2",
                "name": "Erling Haaland",
                "team": "Manchester City",
                "position": "FWD",
                "opta_index": 88.3,
                "market_value": 180.0,
            }
        ],
        "total": 2
    }


@app.get("/api/v1/players/{player_id}")
async def get_player_profile(
    player_id: str,
    user: dict = Depends(get_current_user),
    _: dict = Depends(check_usage_quota("player_reports_per_month"))
):
    """
    Get comprehensive player profile.

    Counts towards: Player reports quota
    """
    from src.data_collection.unified_data_aggregator import UnifiedDataAggregator

    # TODO: Use real data aggregator
    # aggregator = UnifiedDataAggregator()
    # profile = aggregator.get_player_complete_profile(player_name)

    return {
        "player_id": player_id,
        "name": "Mohamed Salah",
        "age": 31,
        "position": "RW",
        "team": "Liverpool FC",
        "league": "Premier League",
        "nationality": "Egypt",
        "performance": {
            "opta_index": 85.2,
            "rating": "EXCELLENT",
            "goals": 18,
            "assists": 12,
            "minutes_played": 2847,
        },
        "advanced_metrics": {
            "xg": 16.8,
            "xa": 9.3,
            "progressive_passes": 156,
        } if get_plan_features(user["plan_tier"]).advanced_metrics else None,
        "market_data": {
            "market_value": 65.0,
            "currency": "EUR",
        }
    }


@app.post("/api/v1/team-fit/analyze")
async def analyze_team_fit(
    player_id: str,
    team_id: str,
    user: dict = Depends(get_current_user),
    _: bool = Depends(lambda: check_feature_access("team_fit_analyses_per_month")),
    __: dict = Depends(check_usage_quota("team_fit_analyses_per_month"))
):
    """
    Analyze how well a player fits a team.

    Requires: Team Fit Analysis feature
    Counts towards: Team Fit quota
    """
    from src.team_fit.team_fit_analyzer import TeamFitAnalyzer

    # TODO: Load real player and team profiles
    # analyzer = TeamFitAnalyzer()
    # fit = analyzer.analyze_fit(player_profile, team_profile)

    return {
        "player_id": player_id,
        "team_id": team_id,
        "fit_score": 87.5,
        "fit_rating": "EXCELLENT_FIT",
        "recommendation": "STRONG BUY - Perfect tactical and cultural fit",
        "breakdown": {
            "statistical_fit": 90,
            "tactical_fit": 88,
            "personality_fit": 85,
            "chemistry_fit": 87,
            "cultural_fit": 92,
            "budget_fit": 75,
            "age_fit": 95,
        },
        "adaptation_timeline": "IMMEDIATE (0-1 months)",
        "key_strengths": [
            "Plays in priority position",
            "High performance level",
            "Perfect age bracket",
            "Cultural fit excellent",
        ]
    }


@app.post("/api/v1/moneyball/valuations")
async def get_moneyball_valuation(
    player_id: str,
    user: dict = Depends(get_current_user),
    _: bool = Depends(lambda: check_feature_access("moneyball_valuation"))
):
    """
    Get Moneyball-style player valuation.

    Requires: Moneyball Valuation feature (Professional plan+)
    """
    return {
        "player_id": player_id,
        "market_value": 50.0,
        "calculated_value": 75.0,
        "value_ratio": 1.5,
        "category": "UNDERVALUED",
        "roi_potential": 50.0,
        "recommendation": "BUY - Significant upside potential",
        "comparable_players": [
            {"name": "Player A", "value": 70.0, "similarity": 0.92},
            {"name": "Player B", "value": 80.0, "similarity": 0.88},
        ]
    }


@app.get("/api/v1/reports/{report_id}")
async def get_report(
    report_id: str,
    format: str = "json",  # json, pdf, excel
    user: dict = Depends(get_current_user)
):
    """Get generated report in various formats."""
    features = get_plan_features(user["plan_tier"])

    if format == "pdf" and not features.pdf_exports:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="PDF exports require Scout plan or higher"
        )

    if format == "excel" and not features.excel_exports:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Excel exports require Professional plan or higher"
        )

    return {
        "report_id": report_id,
        "format": format,
        "download_url": f"/api/v1/reports/{report_id}/download?format={format}",
        "expires_at": "2025-01-10T00:00:00Z"
    }


@app.get("/api/v1/stats")
async def get_api_stats():
    """Public API statistics."""
    return {
        "total_players": 50000,
        "total_teams": 3000,
        "leagues_covered": 52,
        "data_freshness": "Last updated 2 hours ago",
        "uptime_percent": 99.9,
    }


# =====================================================
# WEBHOOK ENDPOINTS (for Stripe)
# =====================================================

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: dict):
    """
    Handle Stripe webhooks for subscription events.

    Events to handle:
    - customer.subscription.created
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_succeeded
    - invoice.payment_failed
    """
    # TODO: Implement Stripe webhook handling
    # 1. Verify webhook signature
    # 2. Handle event type
    # 3. Update user subscription in database

    return {"received": True}


# =====================================================
# ERROR HANDLERS
# =====================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail if isinstance(exc.detail, str) else exc.detail.get("message"),
            "details": exc.detail if isinstance(exc.detail, dict) else None,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
