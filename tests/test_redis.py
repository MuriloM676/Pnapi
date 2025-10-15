import redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_redis_connection():
    """Test Redis connection"""
    try:
        # Redis configuration
        REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
        REDIS_DB = int(os.getenv('REDIS_DB', 0))
        REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
        
        # Create Redis connection
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
        
        # Test connection
        redis_client.ping()
        print("✓ Successfully connected to Redis")
        
        # Test basic operations
        redis_client.set("test_key", "test_value")
        value = redis_client.get("test_key")
        print(f"✓ Set and retrieved test value: {value}")
        
        # Clean up
        redis_client.delete("test_key")
        print("✓ Cleaned up test key")
        
        return True
    except Exception as e:
        print(f"✗ Failed to connect to Redis: {e}")
        return False

if __name__ == "__main__":
    print("Testing Redis connection...")
    success = test_redis_connection()
    if success:
        print("\n✓ All Redis tests passed!")
    else:
        print("\n✗ Redis tests failed!")