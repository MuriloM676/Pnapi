# Production Dockerfile for PNCP API Client
# Small, secure, and fast image
FROM python:3.11-slim AS base

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Create non-root user
ARG APP_USER=appuser
ARG APP_HOME=/app

# Install system dependencies (curl for healthcheck, build deps optional)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR ${APP_HOME}

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./

# Install python dependencies
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY . ${APP_HOME}

# Create non-root user and set permissions
RUN useradd -m -u 10001 ${APP_USER} \
    && chown -R ${APP_USER}:${APP_USER} ${APP_HOME}

USER ${APP_USER}

# Expose the application port
EXPOSE 8000

# Environment defaults (can be overridden by compose or runtime)
ENV FLASK_ENV=production \
    GUNICORN_CMD_ARGS="--config gunicorn.conf.py"

# Healthcheck (relies on curl installed in the image)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -fsS http://127.0.0.1:8000/api/health || exit 1

# Start the app with Gunicorn (Flask factory is in wsgi:application)
CMD ["gunicorn", "wsgi:application"]
