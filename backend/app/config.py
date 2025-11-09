"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App
    APP_NAME: str = "Sports Analytics Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sports_analytics"

    # For SQLite (development)
    # DATABASE_URL: str = "sqlite:///./sports_analytics.db"

    # Redis (for caching)
    REDIS_URL: str = "redis://localhost:6379"

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Cache TTL (seconds)
    CACHE_TTL_SHORT: int = 300  # 5 minutes
    CACHE_TTL_MEDIUM: int = 1800  # 30 minutes
    CACHE_TTL_LONG: int = 86400  # 24 hours

    # External APIs
    STATSBOMB_BASE_URL: str = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
    BALLDONTLIE_BASE_URL: str = "https://www.balldontlie.io/api/v1"
    THESPORTSDB_BASE_URL: str = "https://www.thesportsdb.com/api/v1/json/3"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
