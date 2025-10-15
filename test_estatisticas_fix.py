#!/usr/bin/env python3
"""
Test script to verify all statistics endpoints are working correctly.
"""

import requests
import json
import time

def test_endpoint(endpoint_name, url):
    """Test a single endpoint and print results."""
    print(f"\n{'='*50}")
    print(f"Testing {endpoint_name}")
    print(f"URL: {url}")
    print(f"{'='*50}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=15)
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Received {len(data)} records")
            
            # Print first few records for verification
            for i, item in enumerate(data[:3]):
                print(f"  Record {i+1}: {item}")
                
            return True
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED - Connection refused. Is the server running?")
        return False
    except requests.exceptions.Timeout:
        print("❌ FAILED - Request timeout")
        return False
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("Testing PNCP API Client - Statistics Endpoints")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000/api/estatisticas"
    
    endpoints = [
        ("Modalidades", f"{base_url}/modalidades"),
        ("Estados (UF)", f"{base_url}/uf"),
        ("Tipo de Órgão", f"{base_url}/tipo_orgao"),
        ("Contratos", f"{base_url}/contratos"),
        ("Atas de Registro", f"{base_url}/atas"),
        ("Planos de Contratação", f"{base_url}/planos"),
    ]
    
    results = []
    
    for name, url in endpoints:
        success = test_endpoint(name, url)
        results.append((name, success))
        time.sleep(1)  # Small delay between requests
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name:<25} {status}")
    
    print(f"\nResults: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All statistics endpoints are working correctly!")
        return True
    else:
        print("⚠️  Some endpoints need attention.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)