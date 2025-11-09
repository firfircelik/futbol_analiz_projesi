"""
Redis connection and caching utilities
"""
import redis
import json
import os
from typing import Optional, Any, Callable
from functools import wraps
import logging

logger = logging.getLogger(__name__)

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    # Test connection
    redis_client.ping()
    REDIS_AVAILABLE = True
    logger.info("✅ Redis connected successfully")
except Exception as e:
    logger.warning(f"⚠️  Redis not available: {e}. Caching disabled.")
    redis_client = None
    REDIS_AVAILABLE = False


class Cache:
    """Simple cache interface"""

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        if not REDIS_AVAILABLE:
            return None

        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None

    @staticmethod
    def set(key: str, value: Any, ttl: int = 3600):
        """
        Set value in cache with TTL (time to live) in seconds

        Default TTL: 1 hour
        """
        if not REDIS_AVAILABLE:
            return

        try:
            redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    @staticmethod
    def delete(key: str):
        """Delete key from cache"""
        if not REDIS_AVAILABLE:
            return

        try:
            redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    @staticmethod
    def clear_pattern(pattern: str):
        """Delete all keys matching pattern"""
        if not REDIS_AVAILABLE:
            return

        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


def cached(ttl: int = 3600, key_prefix: str = ""):
    """
    Decorator for caching function results

    Usage:
        @cached(ttl=900, key_prefix="player")
        def get_player(player_id: str):
            # Expensive operation
            return player_data

    Args:
        ttl: Cache time-to-live in seconds (default 1 hour)
        key_prefix: Prefix for cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(filter(None, key_parts))

            # Try to get from cache
            cached_value = Cache.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached_value

            # Cache miss - call function
            logger.debug(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)

            # Store in cache
            Cache.set(cache_key, result, ttl)
            return result

        return wrapper
    return decorator


# Convenience functions
def cache_player_data(player_id: str, data: dict, ttl: int = 86400):
    """Cache player data for 24 hours"""
    Cache.set(f"player:{player_id}", data, ttl)


def get_cached_player(player_id: str) -> Optional[dict]:
    """Get cached player data"""
    return Cache.get(f"player:{player_id}")


def cache_analytics_result(result_type: str, player_id: str, data: dict, ttl: int = 604800):
    """Cache analytics result for 7 days"""
    Cache.set(f"analytics:{result_type}:{player_id}", data, ttl)


def get_cached_analytics(result_type: str, player_id: str) -> Optional[dict]:
    """Get cached analytics result"""
    return Cache.get(f"analytics:{result_type}:{player_id}")
