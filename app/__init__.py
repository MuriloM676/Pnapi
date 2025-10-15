"""
Main application package for PNCP API Client.
"""
from flask import Flask
from app.config.settings import config
from app.extensions import redis_client
from app.api.blueprints import register_blueprints
from app.config.logging_config import setup_logging
import os


def create_app(config_name: str = 'development') -> Flask:
    """
    Application factory pattern implementation.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Flask application instance
    """
    # Get the directory where this file is located
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create Flask app with explicit static folder path
    app = Flask(
        __name__,
        static_folder=os.path.join(app_dir, 'static'),
        template_folder=os.path.join(app_dir, 'templates')
    )
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup logging
    setup_logging(app)
    
    # Initialize extensions
    redis_client.init_app(app)
    
    # Register blueprints
    register_blueprints(app)
    
    app.logger.info(f"Application created with config: {config_name}")
    
    return app