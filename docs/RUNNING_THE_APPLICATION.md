# Running the Application

This document explains how to run the PNCP API Client application with the new clean architecture structure.

## Prerequisites

Before running the application, ensure you have:

1. Python 3.7 or higher installed
2. Required Python packages installed (see `requirements.txt`)
3. Redis server (optional, for caching functionality)

## Installation

1. Clone or download the repository
2. Navigate to the project root directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
   
4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses environment variables for configuration. Copy the example file and modify as needed:

```bash
cp .env.example .env
```

Edit the `.env` file to set your configuration values:
- `FLASK_ENV`: Environment (development, production, testing)
- `FLASK_HOST`: Host to bind to (default: 127.0.0.1)
- `FLASK_PORT`: Port to listen on (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: True)
- `SECRET_KEY`: Flask secret key
- `REDIS_HOST`: Redis server host (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `REDIS_PASSWORD`: Redis password (if required)

## Running the Application

### Method 1: Using the WSGI Entry Point (Recommended for Production)

```bash
python wsgi.py
```

### Method 2: Using Python Module Execution

```bash
python -m app
```

### Method 3: Using Flask CLI

```bash
export FLASK_APP=app
flask run
```

On Windows:
```bash
set FLASK_APP=app
flask run
```

### Method 4: Direct Application Creation

```bash
python -c "from app import create_app; app = create_app(); app.run()"
```

## Development Mode

For development, the application will run in debug mode by default. To explicitly set development mode:

```bash
export FLASK_ENV=development
python wsgi.py
```

## Production Mode

For production deployment:

```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
python wsgi.py
```

## Running with Gunicorn (Linux/macOS)

For production deployments on Linux or macOS, you can use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application
```

## Running with uWSGI

For production deployments, you can also use uWSGI:

```bash
pip install uwsgi
uwsgi --http :5000 --wsgi-file wsgi.py --callable application
```

## Testing

To run the test suite:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=app
```

## Development Workflow

1. **Start the development server**:
   ```bash
   python wsgi.py
   ```

2. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

3. **View logs**:
   The application will output logs to the console

4. **Make changes**:
   - Routes: Modify files in `app/api/routes/`
   - Business logic: Modify files in `app/core/services/`
   - Models: Modify files in `app/core/models/`
   - Utilities: Modify files in `app/core/utils/`
   - Configuration: Modify files in `app/config/`

5. **Test changes**:
   Run specific tests or the full test suite

## Environment Variables

The application recognizes the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development, production, testing) | development |
| `FLASK_HOST` | Host to bind to | 127.0.0.1 |
| `FLASK_PORT` | Port to listen on | 5000 |
| `FLASK_DEBUG` | Enable debug mode | True |
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `REDIS_HOST` | Redis server host | localhost |
| `REDIS_PORT` | Redis server port | 6379 |
| `REDIS_DB` | Redis database number | 0 |
| `REDIS_PASSWORD` | Redis password | None |

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   Ensure you're running the application from the project root directory

2. **Template not found errors**:
   Verify that templates are in the correct location (`app/templates/`)

3. **Redis connection errors**:
   - Ensure Redis server is running
   - Check Redis configuration in environment variables
   - The application will work without Redis (caching will be disabled)

4. **Port already in use**:
   Change the port using the `FLASK_PORT` environment variable

### Debugging

To enable more verbose logging, you can set the logging level:

```bash
export LOG_LEVEL=DEBUG
python wsgi.py
```

## Deployment

### Docker Deployment

Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "wsgi.py"]
```

Build and run:

```bash
docker build -t pnapi-client .
docker run -p 5000:5000 pnapi-client
```

### Heroku Deployment

1. Create a `Procfile`:
   ```
   web: python wsgi.py
   ```

2. Deploy to Heroku:
   ```bash
   heroku create
   git push heroku main
   ```

## Performance Considerations

1. **Caching**: Redis caching is enabled by default for API responses
2. **Static Files**: In production, serve static files through a web server like Nginx
3. **Database**: For applications with database needs, consider connection pooling
4. **Concurrency**: Use a WSGI server like Gunicorn for handling multiple requests

## Security Considerations

1. **Secret Key**: Always set a strong secret key in production
2. **Environment Variables**: Never commit sensitive configuration to version control
3. **Debug Mode**: Disable debug mode in production
4. **HTTPS**: Use HTTPS in production environments