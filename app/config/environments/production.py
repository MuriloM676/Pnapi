"""
Production environment configuration.
"""
from app.config.settings import ProductionConfig


class ProductionConfigExtended(ProductionConfig):
    """Extended production configuration."""
    
    # Production-specific settings
    LOG_LEVEL: str = 'WARNING'