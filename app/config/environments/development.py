"""
Development environment configuration.
"""
from app.config.settings import DevelopmentConfig


class DevelopmentConfigExtended(DevelopmentConfig):
    """Extended development configuration."""
    
    # Development-specific settings can be added here
    LOG_LEVEL: str = 'DEBUG'