"""
Main entry point for PNCP API Client.
"""
import os
from app import create_app


def main():
    """Main entry point."""
    # Get configuration name from environment variable or default to development
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create application
    app = create_app(config_name)
    
    # Run application
    app.run(
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )


if __name__ == "__main__":
    main()