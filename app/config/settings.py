"""
Configuration settings for PNCP API Client.
"""
import os
from typing import Optional


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY: str = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # PNCP API endpoints
    PNCP_API_BASE: str = os.environ.get('PNCP_API_BASE') or "https://pncp.gov.br/api/pncp"
    CONSULTA_API_BASE: str = os.environ.get('CONSULTA_API_BASE') or "https://pncp.gov.br/api/consulta"
    
    # Redis configuration
    REDIS_HOST: str = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT: int = int(os.environ.get('REDIS_PORT') or 6379)
    REDIS_DB: int = int(os.environ.get('REDIS_DB') or 0)
    REDIS_PASSWORD: Optional[str] = os.environ.get('REDIS_PASSWORD') or None


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG: bool = True
    ENV: str = 'development'


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING: bool = True
    DEBUG: bool = True
    ENV: str = 'testing'


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG: bool = False
    ENV: str = 'production'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}