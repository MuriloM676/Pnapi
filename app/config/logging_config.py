"""
Logging configuration for PNCP API Client.
"""
import logging
import sys
from typing import Optional
from flask import Flask

try:
    from pythonjsonlogger import jsonlogger
    JSON_LOGGING_AVAILABLE = True
except ImportError:
    JSON_LOGGING_AVAILABLE = False


def setup_logging(app: Flask) -> None:
    """
    Configure structured logging for the application.
    
    Args:
        app: Flask application instance
    """
    log_level = logging.DEBUG if app.debug else logging.INFO
    
    # Remove existing handlers
    app.logger.handlers = []
    
    # Create handler
    log_handler = logging.StreamHandler(sys.stdout)
    
    # Configure formatter based on environment
    if not app.debug and JSON_LOGGING_AVAILABLE:
        # JSON formatter for production (machine-readable)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s %(pathname)s %(lineno)d',
            rename_fields={
                'levelname': 'level',
                'asctime': 'timestamp'
            }
        )
    else:
        # Human-readable formatter for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    log_handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(log_handler)
    app.logger.setLevel(log_level)
    
    # Configure third-party loggers
    logging.getLogger('werkzeug').setLevel(log_level)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    # Log startup message
    app.logger.info(f"Logging configured - Level: {logging.getLevelName(log_level)}")
    
    if not app.debug and not JSON_LOGGING_AVAILABLE:
        app.logger.warning(
            "python-json-logger not installed. "
            "Install for structured logging in production: pip install python-json-logger"
        )


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
