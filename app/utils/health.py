"""
Health check utilities for PNCP API Client.
"""
import time
import requests
from datetime import datetime
from typing import Dict, Any
from app.extensions import redis_client
from app.config.settings import config

# Get configuration
current_config = config['default']()


class HealthChecker:
    """Health check utilities."""
    
    @staticmethod
    def check_redis_health() -> Dict[str, Any]:
        """Check Redis connection health."""
        try:
            start_time = time.time()
            is_connected = redis_client.ping()
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if is_connected:
                return {
                    "status": "healthy",
                    "response_time_ms": round(response_time, 2),
                    "connection": "active"
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": "Redis not available",
                    "connection": "failed"
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connection": "failed"
            }
    
    @staticmethod
    def check_pncp_api_health() -> Dict[str, Any]:
        """Check PNCP API health."""
        try:
            start_time = time.time()
            # Use the licitacoes endpoint which is more reliable
            url = f"{current_config.API_BASE}/pncp/v1/orgaos/siafi"
            response = requests.get(url, timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy" if response.status_code == 200 else "degraded",
                "response_time_ms": round(response_time, 2),
                "status_code": response.status_code,
                "last_check": datetime.now().isoformat()
            }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "error": "Request timeout after 5 seconds",
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    @staticmethod
    def get_cache_statistics() -> Dict[str, Any]:
        """Get cache performance statistics."""
        try:
            # Check if Redis is connected first
            if not redis_client.is_connected():
                return {
                    "error": "Redis not connected",
                    "hit_ratio": 0,
                    "status": "disconnected"
                }
            
            # Get basic Redis info
            info = redis_client.info()
            
            if not info:
                return {
                    "error": "Could not retrieve Redis info",
                    "hit_ratio": 0,
                    "status": "error"
                }
            
            # Calculate hit ratio
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total_operations = hits + misses
            hit_ratio = round((hits / max(total_operations, 1)) * 100, 2)
            
            return {
                "connected_clients": info.get('connected_clients', 0),
                "used_memory_human": info.get('used_memory_human', 'N/A'),
                "keyspace_hits": hits,
                "keyspace_misses": misses,
                "hit_ratio": hit_ratio,
                "status": "connected"
            }
        except Exception as e:
            return {
                "error": str(e),
                "hit_ratio": 0,
                "status": "error"
            }
    
    @staticmethod
    def get_system_health() -> Dict[str, Any]:
        """Get comprehensive system health status."""
        redis_health = HealthChecker.check_redis_health()
        api_health = HealthChecker.check_pncp_api_health()
        cache_stats = HealthChecker.get_cache_statistics()
        
        # Determine overall system status
        overall_status = "healthy"
        if redis_health["status"] == "unhealthy" and api_health["status"] in ["unhealthy", "timeout"]:
            overall_status = "critical"
        elif redis_health["status"] == "unhealthy" or api_health["status"] in ["degraded", "timeout"]:
            overall_status = "degraded"
        elif api_health["status"] == "unhealthy":
            overall_status = "unhealthy"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "services": {
                "redis": redis_health,
                "pncp_api": api_health
            },
            "cache": cache_stats,
            "system_info": {
                "version": "1.0.0",
                "environment": current_config.__class__.__name__.lower()
            }
        }