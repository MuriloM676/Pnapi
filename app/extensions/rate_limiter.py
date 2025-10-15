"""
Rate limiting extension for PNCP API Client.
"""
from functools import wraps
from flask import request, jsonify, current_app
import time
from typing import Dict, List, Callable, Any
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter.
    Tracks requests per IP and endpoint.
    """
    
    def __init__(self):
        """Initialize rate limiter."""
        self.requests: Dict[str, List[float]] = {}
        self.cleanup_interval = 300  # Clean old entries every 5 minutes
        self.last_cleanup = time.time()
    
    def _get_identifier(self, endpoint: str) -> str:
        """
        Get unique identifier for the request.
        
        Args:
            endpoint: Endpoint name
            
        Returns:
            Unique identifier string
        """
        # Use X-Forwarded-For if behind proxy, otherwise remote_addr
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return f"{ip}:{endpoint}"
    
    def _cleanup_old_requests(self, window: int) -> None:
        """
        Remove old request timestamps.
        
        Args:
            window: Time window in seconds
        """
        if time.time() - self.last_cleanup < self.cleanup_interval:
            return
        
        now = time.time()
        for key in list(self.requests.keys()):
            self.requests[key] = [
                timestamp for timestamp in self.requests[key]
                if now - timestamp < window
            ]
            # Remove empty entries
            if not self.requests[key]:
                del self.requests[key]
        
        self.last_cleanup = now
        logger.debug(f"Rate limiter cleanup completed. Active keys: {len(self.requests)}")
    
    def limit(self, max_requests: int = 60, window: int = 60) -> Callable:
        """
        Decorator for rate limiting endpoints.
        
        Args:
            max_requests: Maximum number of requests allowed
            window: Time window in seconds
            
        Returns:
            Decorated function
            
        Example:
            @api_bp.route('/endpoint')
            @rate_limiter.limit(max_requests=30, window=60)
            def my_endpoint():
                return jsonify({"data": "value"})
        """
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                # Skip rate limiting in testing
                if current_app.config.get('TESTING'):
                    return f(*args, **kwargs)
                
                key = self._get_identifier(f.__name__)
                now = time.time()
                
                # Periodic cleanup
                self._cleanup_old_requests(window)
                
                # Initialize or filter old requests
                if key not in self.requests:
                    self.requests[key] = []
                else:
                    self.requests[key] = [
                        timestamp for timestamp in self.requests[key]
                        if now - timestamp < window
                    ]
                
                # Check if limit exceeded
                if len(self.requests[key]) >= max_requests:
                    logger.warning(
                        f"Rate limit exceeded for {key}. "
                        f"Requests: {len(self.requests[key])}/{max_requests}"
                    )
                    return jsonify({
                        "error": "Rate limit exceeded",
                        "message": f"Maximum {max_requests} requests per {window} seconds",
                        "retry_after": window
                    }), 429
                
                # Add current request
                self.requests[key].append(now)
                
                # Execute the actual function
                return f(*args, **kwargs)
            
            return wrapped
        return decorator
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get rate limiter statistics.
        
        Returns:
            Dictionary with stats
        """
        return {
            "active_keys": len(self.requests),
            "total_tracked_requests": sum(len(v) for v in self.requests.values()),
            "last_cleanup": self.last_cleanup
        }
    
    def reset(self) -> None:
        """Reset all rate limiting data."""
        self.requests = {}
        logger.info("Rate limiter reset")


# Global rate limiter instance
rate_limiter = RateLimiter()
