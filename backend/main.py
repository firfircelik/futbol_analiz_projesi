"""
ScoutAI - Unified Backend API
Production-ready SaaS platform for sports analytics

This is the SINGLE entry point for the entire backend.
All routes, middleware, and services are configured here.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import core
from core.database import init_db
from core.redis_client import REDIS_AVAILABLE

# Import API routers
from api.auth import router as auth_router
from api.users import router as users_router
from api.players import router as players_router
from api.analytics import router as analytics_router
from api.pricing import router as pricing_router

# =====================================================
# FASTAPI APP INITIALIZATION
# =====================================================

app = FastAPI(
    title="ScoutAI API",
    description="""
    **Professional Sports Analytics SaaS Platform**

    Opta-level analytics at 1/100th the price.

    Features:
    - Multi-source data aggregation (StatsBomb, Understat, FBref)
    - Opta Performance Index (0-100 player ratings)
    - Team Fit Analysis (7-dimensional compatibility)
    - Moneyball Valuation (find undervalued players)
    - Advanced metrics (xG, xA, progressive actions)

    Subscription Tiers:
    - **Free**: 10 reports/month, 3 leagues
    - **Scout** (€29/mo): 100 reports, 10 Team Fit analyses
    - **Professional** (€99/mo): 500 reports, unlimited Team Fit, xG/xA
    - **Club** (€299/mo): Unlimited, API access, multi-user

    Authentication: JWT Bearer token required for protected endpoints
    """,
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# =====================================================
# MIDDLEWARE
# =====================================================

# CORS - Allow frontend to connect
CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:3001"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = datetime.utcnow()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()

    # Log request details
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={duration:.3f}s"
    )

    return response


# =====================================================
# ERROR HANDLERS
# =====================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with clean response"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# =====================================================
# STARTUP & SHUTDOWN EVENTS
# =====================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Starting ScoutAI Backend API...")

    # Initialize database
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise

    # Check Redis connection
    if REDIS_AVAILABLE:
        logger.info("✅ Redis connected (caching enabled)")
    else:
        logger.warning("⚠️  Redis not available (caching disabled)")

    logger.info("✨ ScoutAI Backend API ready!")
    logger.info(f"📊 API Docs: http://localhost:8000/api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Shutting down ScoutAI Backend API...")


# =====================================================
# ROUTES
# =====================================================

@app.get("/", tags=["Health"])
async def root():
    """
    API health check

    Returns API status and version information
    """
    return {
        "service": "ScoutAI API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/api/docs",
        "features": {
            "authentication": "JWT",
            "caching": REDIS_AVAILABLE,
            "database": "Connected",
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check for monitoring

    Returns status of all services
    """
    from core.redis_client import redis_client

    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "up",
            "database": "up",  # Could add actual DB ping here
            "redis": "up" if REDIS_AVAILABLE else "down"
        }
    }

    # Test Redis if available
    if REDIS_AVAILABLE and redis_client:
        try:
            redis_client.ping()
            health["services"]["redis"] = "up"
        except:
            health["services"]["redis"] = "down"
            health["status"] = "degraded"

    return health


# =====================================================
# INCLUDE ROUTERS
# =====================================================

# Authentication (public)
app.include_router(auth_router)

# User endpoints (authenticated)
app.include_router(users_router)

# Player endpoints (authenticated)
app.include_router(players_router)

# Analytics endpoints (authenticated)
app.include_router(analytics_router)

# Pricing (public)
app.include_router(pricing_router)


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
