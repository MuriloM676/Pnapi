"""
Health check utilities for PNCP API Client.
"""
import time
import requests
from datetime import datetime, timedelta
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
            redis_client.ping()
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "connection": "active"
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
            url = f"{current_config.CONSULTA_API_BASE}/v1/contratacoes/modalidades"
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
            # Get basic Redis info
            info = redis_client.info()
            
            return {
                "connected_clients": info.get('connected_clients', 0),
                "used_memory_human": info.get('used_memory_human', 'N/A'),
                "keyspace_hits": info.get('keyspace_hits', 0),
                "keyspace_misses": info.get('keyspace_misses', 0),
                "hit_ratio": round(
                    info.get('keyspace_hits', 0) / 
                    max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0), 1) * 100, 
                    2
                )
            }
        except Exception as e:
            return {
                "error": str(e),
                "hit_ratio": 0
            }
    
    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        """Get basic system metrics."""
        try:
            import psutil
            
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage_percent": psutil.disk_usage('/').percent
            }
        except ImportError:
            return {
                "error": "psutil not installed",
                "note": "Install psutil for system metrics"
            }
        except Exception as e:
            return {
                "error": str(e)
            }