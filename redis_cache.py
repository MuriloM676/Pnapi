import json
import logging
from functools import wraps
from typing import Any, Optional

# Try to import redis
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

# Configure logging
logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """Initialize Redis connection"""
        if not REDIS_AVAILABLE:
            logger.warning("Redis module not installed. Cache will be disabled.")
            self.redis_client = None
            return
            
        try:
            self.redis_client = redis.Redis(  # type: ignore
                host=host,
                port=port,
                db=db,
                password=password,
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
        """Set a key-value pair in cache with expiration time (in seconds)"""
        if not self.redis_client:
            return False
            
        try:
            serialized_value = json.dumps(value)
            result = self.redis_client.setex(key, expire, serialized_value)
            logger.debug(f"Cache set for key: {key}")
            return result
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key from cache"""
        if not self.redis_client:
            return None
            
        try:
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
        """Delete a key from cache"""
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
        """Check if key exists in cache"""
        if not self.redis_client:
            return False
            
        try:
            return self.redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking existence of key {key}: {e}")
            return False
    
    def flush(self) -> bool:
        """Clear all cache"""
        if not self.redis_client:
            return False
            
        try:
            self.redis_client.flushdb()
            logger.info("Cache flushed")
            return True
        except Exception as e:
            logger.error(f"Error flushing cache: {e}")
            return False

# Create a global cache instance
cache = RedisCache()

def cached(expire: int = 3600):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If Redis is not available, just call the function directly
            if not cache.redis_client:
                return func(*args, **kwargs)
            
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # If not in cache, call the function
            result = func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator