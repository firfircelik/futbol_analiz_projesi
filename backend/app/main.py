"""
FastAPI Backend - Sports Analytics Platform
Main application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List
import asyncio

from app.api.v1 import leagues, players, teams, analytics, team_fit, scouting, moneyball
from app.config import settings
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Sports Analytics Platform API",
    description="Opta-style professional sports analytics for Football & Basketball",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket connection manager for live scores
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Sports Analytics Platform API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "features": [
            "Opta-style Analytics",
            "Team Fit Analyzer",
            "Moneyball Valuation",
            "Scouting Reports",
            "85+ Leagues Worldwide",
        ],
    }


# Health check
@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}


# WebSocket endpoint for live scores
@app.websocket("/ws/live")
async def websocket_live_scores(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for now (will implement live score updates)
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Include API routers
app.include_router(
    leagues.router,
    prefix="/api/v1/leagues",
    tags=["Leagues"],
)

app.include_router(
    players.router,
    prefix="/api/v1/players",
    tags=["Players"],
)

app.include_router(
    teams.router,
    prefix="/api/v1/teams",
    tags=["Teams"],
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"],
)

app.include_router(
    team_fit.router,
    prefix="/api/v1/team-fit",
    tags=["Team Fit Analyzer"],
)

app.include_router(
    scouting.router,
    prefix="/api/v1/scouting",
    tags=["Scouting"],
)

app.include_router(
    moneyball.router,
    prefix="/api/v1/moneyball",
    tags=["Moneyball"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development only
    )
