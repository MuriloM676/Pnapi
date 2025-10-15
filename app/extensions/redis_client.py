"""
Redis client extension for PNCP API Client.
"""
# Try to import redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

import logging
from typing import Any, Optional
from flask import Flask

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper for Flask applications."""
    
    def __init__(self, app: Optional[Flask] = None):
        """Initialize Redis client."""
        self.redis_client: Optional[Any] = None
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app: Flask) -> None:
        """Initialize Redis client with Flask app."""
        if not REDIS_AVAILABLE:
            logger.warning("Redis module not installed. Cache will be disabled.")
            self.redis_client = None
            return
            
        try:
            self.redis_client = redis.Redis(  # type: ignore
                host=app.config.get('REDIS_HOST', 'localhost'),
                port=app.config.get('REDIS_PORT', 6379),
                db=app.config.get('REDIS_DB', 0),
                password=app.config.get('REDIS_PASSWORD'),
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}. Cache will be disabled.")
            self.redis_client = None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set a key-value pair in cache with expiration time (in seconds)."""
        if not self.redis_client:
            return False
            
        try:
            import json
            serialized_value = json.dumps(value)
            result = self.redis_client.setex(key, expire, serialized_value)
            logger.debug(f"Cache set for key: {key}")
            return result
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key from cache."""
        if not self.redis_client:
            return None
            
        try:
            import json
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                return json.loads(value)
            else:
                logger.debug(f"Cache miss for key: {key}")
                return None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {e}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache."""
        if not self.redis_client:
            return False
            
        try:
            result = self.redis_client.delete(key)
            logger.debug(f"Cache deleted for key: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting cache for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.redis_client:
            return False
            
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking existence of key {key}: {e}")
            return False
    
    def flush(self) -> bool:
        """Clear all cache."""
        if not self.redis_client:
            return False
            
        try:
            self.redis_client.flushdb()
            logger.info("Cache flushed")
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")
            return False


# Create global Redis client instance
redis_client = RedisClient()