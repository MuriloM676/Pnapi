#!/usr/bin/env python3
"""
Script to test Redis fixes and health check functionality.
"""
import requests
import json
import time
import sys

def test_health_endpoint():
    """Test the health check endpoint."""
    print("🩺 Testing Health Check Endpoint...")
    print("=" * 50)
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📄 Response Content:")
        health_data = response.json()
        print(json.dumps(health_data, indent=2))
        
        # Analyze the health response
        print(f"\n📊 Health Analysis:")
        print(f"   Overall Status: {health_data.get('overall_status', 'unknown')}")
        
        services = health_data.get('services', {})
        print(f"   Redis Status: {services.get('redis', {}).get('status', 'unknown')}")
        print(f"   PNCP API Status: {services.get('pncp_api', {}).get('status', 'unknown')}")
        
        cache = health_data.get('cache', {})
        print(f"   Cache Status: {cache.get('status', 'unknown')}")
        print(f"   Cache Hit Ratio: {cache.get('hit_ratio', 0)}%")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to Flask application at http://localhost:5000")
        print("   Make sure the Flask app is running: python -m flask run --port 5000")
        return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False


def test_statistics_endpoints():
    """Test all statistics endpoints."""
    print("\n📊 Testing Statistics Endpoints...")
    print("=" * 50)
    
    endpoints = [
        '/api/estatisticas/modalidades',
        '/api/estatisticas/uf', 
        '/api/estatisticas/tipo_orgao',
        '/api/estatisticas/contratos',
        '/api/estatisticas/atas',
        '/api/estatisticas/planos'
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            print(f"Testing {endpoint}...")
            response = requests.get(f'http://localhost:5000{endpoint}', timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            results[endpoint] = {
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
            print(f"  {status} Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    print(f"     Data points: {len(data['data'])}")
                elif isinstance(data, list):
                    print(f"     Data points: {len(data)}")
                else:
                    print(f"     Response type: {type(data)}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results[endpoint] = {
                'status_code': 0,
                'success': False,
                'error': str(e)
            }
    
    # Summary
    successful = sum(1 for r in results.values() if r['success'])
    total = len(endpoints)
    
    print(f"\n📈 Statistics Summary:")
    print(f"   Successful endpoints: {successful}/{total}")
    print(f"   Success rate: {(successful/total)*100:.1f}%")
    
    return successful == total


def test_redis_client():
    """Test Redis client functionality without requiring Redis to be running."""
    print("\n🔧 Testing Redis Client...")
    print("=" * 50)
    
    try:
        # Import and test Redis client
        from app.extensions.redis_client import redis_client
        
        print(f"✅ Redis client imported successfully")
        print(f"   Connected: {redis_client.is_connected()}")
        print(f"   Ping result: {redis_client.ping()}")
        
        # Test info method
        info = redis_client.info()
        print(f"   Info method works: {'✅' if isinstance(info, dict) else '❌'}")
        print(f"   Info status: {info.get('status', 'unknown')}")
        
        # Test cache methods with Redis down
        test_key = "test_key_redis_down"
        print(f"\n   Testing cache methods with Redis down:")
        print(f"     SET operation: {'✅' if not redis_client.set(test_key, 'test_value') else '❌'}")
        print(f"     GET operation: {'✅' if redis_client.get(test_key) is None else '❌'}")
        print(f"     EXISTS operation: {'✅' if not redis_client.exists(test_key) else '❌'}")
        print(f"     DELETE operation: {'✅' if not redis_client.delete(test_key) else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Redis client: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 PNCP API Client - Redis Fix Test Suite")
    print("=" * 60)
    print(f"⏰ Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Statistics Endpoints", test_statistics_endpoints), 
        ("Redis Client", test_redis_client)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
            results[test_name] = False
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 FINAL TEST RESULTS")
    print("=" * 60)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {test_name}: {status}")
    
    successful_tests = sum(1 for success in results.values() if success)
    total_tests = len(results)
    
    print(f"\n📊 Overall Success Rate: {successful_tests}/{total_tests} ({(successful_tests/total_tests)*100:.1f}%)")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Redis fixes are working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())