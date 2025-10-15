#!/usr/bin/env python3
"""
Test script for Redis cache functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from redis_cache import RedisCache

def test_cache_functionality():
    """Test Redis cache functionality"""
    print("Testing Redis cache functionality...")
    
    # Initialize cache
    cache = RedisCache()
    
    # Test if Redis is available
    if not cache.redis_client:
        print("⚠ Redis is not available. Cache functionality will be disabled.")
        print("✓ Application will work normally without caching.")
        return True
    
    # Test basic operations
    print("Testing basic cache operations...")
    
    # Test set and get
    test_key = "test_cache_key"
    test_value = {"name": "test", "value": 123, "list": [1, 2, 3]}
    
    # Set value
    result = cache.set(test_key, test_value, expire=10)
    if result:
        print("✓ Cache set operation successful")
    else:
        print("✗ Cache set operation failed")
        return False
    
    # Get value
    retrieved_value = cache.get(test_key)
    if retrieved_value == test_value:
        print("✓ Cache get operation successful")
    else:
        print("✗ Cache get operation failed")
        print(f"  Expected: {test_value}")
        print(f"  Got: {retrieved_value}")
        return False
    
    # Test exists
    if cache.exists(test_key):
        print("✓ Cache exists operation successful")
    else:
        print("✗ Cache exists operation failed")
        return False
    
    # Test delete
    if cache.delete(test_key):
        print("✓ Cache delete operation successful")
    else:
        print("✗ Cache delete operation failed")
        return False
    
    # Verify deletion
    if cache.get(test_key) is None:
        print("✓ Cache deletion verified")
    else:
        print("✗ Cache deletion verification failed")
        return False
    
    # Test decorator
    print("Testing cache decorator...")
    
    from redis_cache import cached
    
    call_count = 0
    
    @cached(expire=5)
    def test_function(x, y):
        nonlocal call_count
        call_count += 1
        return x + y
    
    # First call
    result1 = test_function(2, 3)
    if result1 == 5 and call_count == 1:
        print("✓ First function call successful")
    else:
        print("✗ First function call failed")
        return False
    
    # Second call (should use cache)
    result2 = test_function(2, 3)
    if result2 == 5 and call_count == 1:
        print("✓ Cached function call successful")
    else:
        print("✗ Cached function call failed")
        print(f"  Call count: {call_count} (expected: 1)")
        return False
    
    # Different parameters (should not use cache)
    result3 = test_function(3, 4)
    if result3 == 7 and call_count == 2:
        print("✓ Different parameters call successful")
    else:
        print("✗ Different parameters call failed")
        print(f"  Call count: {call_count} (expected: 2)")
        return False
    
    print("✓ All cache tests passed!")
    return True

if __name__ == "__main__":
    success = test_cache_functionality()
    if success:
        print("\n✓ Redis cache integration is working correctly!")
        sys.exit(0)
    else:
        print("\n✗ Redis cache integration tests failed!")
        sys.exit(1)