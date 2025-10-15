"""
Testing environment configuration.
"""
from app.config.settings import TestingConfig


class TestingConfigExtended(TestingConfig):
    """Extended testing configuration."""
    
    # Testing-specific settings
    LOG_LEVEL: str = 'DEBUG'
    TESTING: bool = True