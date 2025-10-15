# Installing Redis on Windows

To use Redis caching in this application, you need to have Redis server running on your system.

## Option 1: Using Redis for Windows (Recommended)

1. Download Redis for Windows from: https://github.com/tporadowski/redis/releases
2. Extract the files to a folder (e.g., `C:\redis`)
3. Add the Redis folder to your system PATH
4. Start Redis server by running:
   ```
   redis-server.exe
   ```

## Option 2: Using Docker (Alternative)

If you have Docker installed, you can run Redis in a container:

```bash
docker run -d -p 6379:6379 --name redis redis:latest
```

## Option 3: Using Windows Subsystem for Linux (WSL)

If you have WSL installed:

1. Install Redis in your Linux distribution:
   ```bash
   sudo apt update
   sudo apt install redis-server
   ```

2. Start Redis service:
   ```bash
   sudo service redis-server start
   ```

## Testing the Installation

After installing and starting Redis, you can test the connection by running:

```bash
redis-cli ping
```

You should see `PONG` as the response.

## Configuration

The application will look for Redis at `localhost:6379` by default. You can change this by setting the following environment variables in your `.env` file:

```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
# REDIS_PASSWORD=your_password_here (if authentication is required)
```