# Gunicorn configuration for PNCP API Client
import multiprocessing
import os

# Bind to all interfaces on port 8000
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")

# Workers and threads
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.getenv("GUNICORN_THREADS", 2))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")

# Timeouts and keepalive
timeout = int(os.getenv("GUNICORN_TIMEOUT", 60))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))

# Logging
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
accesslog = "-"  # stdout
errorlog = "-"   # stderr

# Max requests to recycle workers and prevent memory leaks
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 1000))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 100))

# Graceful timeout for worker restarts
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", 30))

# Secure headers (behind reverse proxy)
forwarded_allow_ips = "*"
proxy_protocol = False

# Preload app for faster worker spawn (ensure app is preload-safe)
preload_app = True
