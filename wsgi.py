"""
WSGI entry point for PNCP API Client.
"""
import os
from app import create_app

# Get configuration name from environment variable or default to development
config_name = os.environ.get('FLASK_ENV', 'development')

# Create application
application = create_app(config_name)

if __name__ == "__main__":
    application.run()