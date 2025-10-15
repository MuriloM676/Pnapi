# PNCP API Client - Clean Architecture Implementation

A web application that provides a client interface for the Portal Nacional de Contratações Públicas (PNCP) API with Redis caching, following clean architecture principles and best practices.

## Features

- Browse open tenders from PNCP
- View tender details
- Access statistics by modality, state, and organization type
- Redis caching for improved performance
- Responsive web interface
- API documentation
- Clean architecture implementation

## Architecture

This project follows clean architecture principles with a clear separation of concerns:

```
pnapi/
├── app/                    # Main application package
│   ├── __init__.py         # Application factory
│   ├── config/             # Configuration files
│   ├── api/                # API layer (routes/controllers)
│   ├── core/               # Core business logic
│   │   ├── services/       # Business services
│   │   ├── models/         # Data models
│   │   └── utils/          # Utility functions
│   ├── extensions/         # Flask extensions
│   └── templates/          # HTML templates
├── static/                 # Static files
├── tests/                  # Test suite
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

### Key Components

1. **Application Factory** (`app/__init__.py`): Creates and configures the Flask application
2. **Configuration** (`app/config/`): Environment-specific configuration management
3. **API Layer** (`app/api/`): Routes and controllers organized by feature
4. **Core Business Logic** (`app/core/`): Services, models, and utilities
5. **Extensions** (`app/extensions/`): Flask extensions like Redis client
6. **Templates** (`app/templates/`): HTML templates
7. **Static Files** (`static/`): CSS, JavaScript, images
8. **Tests** (`tests/`): Unit and integration tests
9. **Documentation** (`docs/`): Project documentation

## Requirements

- Python 3.7+
- Flask
- Redis server
- PNCP API access

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pnapi
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install and start Redis server (see [install_redis_windows.md](install_redis_windows.md) for Windows instructions)

5. Configure environment variables (copy `.env.example` to `.env` and modify as needed):
   ```
   cp .env.example .env
   ```

## Redis Integration

This application uses Redis for caching API responses to improve performance:

- Open tenders are cached for 10 minutes
- Statistics are cached for 15 minutes
- Cache keys are generated based on request parameters
- Automatic cache invalidation based on TTL

See [REDIS_INTEGRATION.md](REDIS_INTEGRATION.md) for detailed documentation on the Redis implementation.

## Usage

1. Start the application:
   ```
   python wsgi.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

## Endpoints

- `/` - Home page
- `/licitacoes` - Open tenders
- `/estatisticas` - Statistics
- `/api_docs` - API documentation
- `/api/licitacoes/abertas` - Open tenders API
- `/api/estatisticas/*` - Statistics APIs

## Development

- The application is built with Flask following clean architecture principles
- Templates are in the `app/templates/` directory
- Static files are in the `static/` directory
- Redis caching is implemented in `app/extensions/redis_client.py`
- Business logic is in `app/core/services/`

## Testing

Run tests with pytest:
```
pytest
```

## License

This project is licensed under the MIT License.