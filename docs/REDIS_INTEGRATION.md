# Redis Integration Documentation

This document explains how Redis caching has been integrated into the PNCP API Client application.

## Overview

Redis caching has been implemented to improve the performance of the application by caching API responses from the PNCP (Portal Nacional de Contratações Públicas). This reduces the number of requests made to the PNCP API and speeds up response times for frequently requested data.

## Cached Endpoints

The following endpoints now use Redis caching:

1. `/api/licitacoes/abertas` - Open tenders (cached for 10 minutes)
2. `/api/estatisticas/modalidades` - Statistics by modality (cached for 15 minutes)
3. `/api/estatisticas/uf` - Statistics by state (cached for 15 minutes)
4. `/api/estatisticas/tipo_orgao` - Statistics by organization type (cached for 15 minutes)

## How It Works

1. When a request is made to a cached endpoint, the application first checks if the response is already in the Redis cache.
2. If found (cache hit), the cached response is returned immediately.
3. If not found (cache miss), the application makes a request to the PNCP API, caches the response, and then returns it.
4. Cached responses expire after a set time to ensure data freshness.

## Cache Keys

Cache keys are generated based on the endpoint and request parameters to ensure that different parameter combinations are cached separately.

Example cache key format:
```
open_tenders:{hash_of_parameters}
modalidade_stats:{hash_of_parameters}
```

## Configuration

The Redis connection can be configured using the following environment variables in your `.env` file:

```
REDIS_HOST=localhost    # Redis server host
REDIS_PORT=6379         # Redis server port
REDIS_DB=0              # Redis database number
REDIS_PASSWORD=         # Redis password (if required)
```

## Cache Management

The application includes a Redis cache utility (`redis_cache.py`) with the following features:

- `set(key, value, expire)` - Set a key-value pair with expiration time
- `get(key)` - Get a value by key
- `delete(key)` - Delete a key from cache
- `exists(key)` - Check if a key exists
- `flush()` - Clear all cache entries

## Fallback Mechanism

If Redis is not available or there are connection issues, the application will continue to work normally by making direct requests to the PNCP API without caching.

## Cache Invalidation

Cache entries automatically expire based on their TTL (Time To Live) settings:
- Open tenders: 10 minutes
- Statistics: 15 minutes

Manual cache invalidation can be implemented as needed by calling `cache.delete(key)` or `cache.flush()`.

## Performance Benefits

With Redis caching implemented:
- Response times for cached endpoints are significantly improved
- Load on the PNCP API is reduced
- User experience is enhanced with faster data retrieval
- Bandwidth usage is reduced

## Monitoring

Cache hits and misses are logged for monitoring purposes:
- Cache hits are logged at DEBUG level
- Cache misses are logged at DEBUG level
- Connection errors are logged at ERROR level

## Troubleshooting

If you encounter issues with Redis caching:

1. Check that Redis server is running
2. Verify Redis connection settings in `.env`
3. Check application logs for Redis-related errors
4. Test Redis connection with `redis-cli ping`

## Future Improvements

Possible future enhancements:
- Add cache warming for frequently accessed data
- Implement more granular cache invalidation
- Add metrics collection for cache performance
- Implement cache warming strategies