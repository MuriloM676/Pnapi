# Project Structure Documentation

This document describes the organized structure of the PNCP API Client following clean architecture principles.

## Overview

The project has been reorganized to follow clean architecture principles with a clear separation of concerns:

```
pnapi/
├── app/                          # Main application package
│   ├── __init__.py               # Application factory
│   ├── __main__.py               # Main entry point
│   ├── config/                   # Configuration files
│   │   ├── __init__.py
│   │   ├── settings.py           # Base configuration
│   │   └── environments/         # Environment-specific configs
│   │       ├── __init__.py
│   │       ├── development.py
│   │       ├── production.py
│   │       └── testing.py
│   ├── api/                      # API layer (routes/controllers)
│   │   ├── __init__.py
│   │   ├── routes/               # Route definitions
│   │   │   ├── __init__.py
│   │   │   ├── main.py           # Main pages routes
│   │   │   ├── api.py            # API endpoints routes
│   │   │   └── proxy.py          # Proxy routes
│   │   └── blueprints.py         # Blueprint registration
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── services/             # Business services
│   │   │   ├── __init__.py
│   │   │   └── pncp_service.py   # PNCP service implementation
│   │   ├── models/               # Data models
│   │   │   ├── __init__.py
│   │   │   └── tender.py         # Tender data model
│   │   └── utils/                # Utility functions
│   │       ├── __init__.py
│   │       └── helpers.py        # Helper functions
│   ├── extensions/               # Flask extensions
│   │   ├── __init__.py
│   │   ├── redis_client.py       # Redis client extension
│   │   └── redis_cache.py        # Redis cache implementation
│   ├── templates/                # HTML templates
│   └── static/                   # Static files (CSS, JS, images)
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # Test configuration
│   ├── unit/                     # Unit tests
│   │   ├── __init__.py
│   │   ├── test_services.py      # Service unit tests
│   │   └── test_utils.py         # Utility unit tests
│   ├── integration/              # Integration tests
│   │   ├── __init__.py
│   │   └── test_api.py           # API integration tests
│   └── fixtures/                 # Test data
├── docs/                         # Documentation
│   ├── PROJECT_STRUCTURE.md      # This file
│   ├── REDIS_INTEGRATION.md      # Redis integration documentation
│   └── install_redis_windows.md  # Redis installation guide
├── scripts/                      # Utility scripts
│   ├── debug_pncp_api.py         # Debug script for PNCP API
│   ├── get_api_docs.py           # Script to fetch API docs
│   ├── get_consulta_api_docs.py  # Script to fetch consulta API docs
│   └── start_redis.bat           # Script to start Redis on Windows
├── .env.example                  # Environment variables example
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py                      # Package setup
└── wsgi.py                      # WSGI entry point
```

## Architecture Layers

### 1. Presentation Layer (app/api/)
- **Routes**: Handle HTTP requests and responses
- **Blueprints**: Organize routes into logical groups
- **Templates**: HTML templates for server-side rendering

### 2. Application Layer (app/core/services/)
- **Services**: Business logic implementation
- **Models**: Data structures and domain models
- **Utils**: Helper functions and utilities

### 3. Infrastructure Layer (app/extensions/)
- **Extensions**: Third-party integrations (Redis, databases, etc.)
- **Configuration**: Environment-specific settings

### 4. Test Layer (tests/)
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Fixtures**: Sample data for testing

## Key Design Principles

### Separation of Concerns
Each layer has a specific responsibility:
- **API Layer**: Handles HTTP requests/responses
- **Core Layer**: Contains business logic
- **Extensions Layer**: Manages external dependencies
- **Config Layer**: Manages application configuration

### Dependency Inversion
Higher-level modules don't depend on lower-level modules. Both depend on abstractions.

### Single Responsibility
Each module has one reason to change.

### Open/Closed Principle
Modules are open for extension but closed for modification.

## Benefits of This Structure

1. **Maintainability**: Clear separation makes code easier to understand and modify
2. **Testability**: Each component can be tested in isolation
3. **Scalability**: New features can be added without affecting existing code
4. **Flexibility**: Easy to swap implementations (e.g., different cache providers)
5. **Reusability**: Components can be reused across different parts of the application

## How to Add New Features

1. **New Route**: Add to `app/api/routes/` and register in `app/api/blueprints.py`
2. **New Service**: Add to `app/core/services/`
3. **New Model**: Add to `app/core/models/`
4. **New Utility**: Add to `app/core/utils/`
5. **New Extension**: Add to `app/extensions/`
6. **New Tests**: Add to appropriate directory in `tests/`

## Environment Configuration

The application supports multiple environments:
- **Development**: For local development
- **Testing**: For running tests
- **Production**: For production deployment

Configuration is managed through:
- Environment variables
- Configuration classes in `app/config/`
- `.env` file for local development

## Testing Strategy

The project follows a comprehensive testing strategy:
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and service interactions
- **Fixtures**: Provide sample data for consistent testing

Tests can be run with:
```bash
pytest
```

## Deployment

The application can be deployed using:
- **WSGI**: Using `wsgi.py` as the entry point
- **Direct Execution**: Using `python -m app`
- **Package Installation**: Using `pip install .`

Environment variables control deployment settings:
- `FLASK_ENV`: Environment name (development, testing, production)
- `FLASK_HOST`: Host to bind to
- `FLASK_PORT`: Port to listen on
- `FLASK_DEBUG`: Enable/disable debug mode