"""
Blueprints registration for PNCP API Client.
"""
from flask import Flask
from app.api.routes.main import main_bp
from app.api.routes.api import api_bp
from app.api.routes.proxy import proxy_bp


def register_blueprints(app: Flask) -> None:
    """
    Register all blueprints with the Flask application.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(proxy_bp)