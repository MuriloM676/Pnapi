import requests
import time

def test_advanced_statistics():
    """Test the new advanced statistics endpoints"""
    base_url = "http://127.0.0.1:5000/api"
    
    # Test contracts statistics endpoint
    print("Testing contracts statistics endpoint...")
    try:
        response = requests.get(f"{base_url}/estatisticas/contratos", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Contracts data: {data}")
            print("✓ Contracts statistics endpoint working correctly")
        else:
            print(f"✗ Contracts statistics endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Contracts statistics endpoint failed with error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test price registration records statistics endpoint
    print("Testing price registration records statistics endpoint...")
    try:
        response = requests.get(f"{base_url}/estatisticas/atas", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Price registration records data: {data}")
            print("✓ Price registration records statistics endpoint working correctly")
        else:
            print(f"✗ Price registration records statistics endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Price registration records statistics endpoint failed with error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test procurement plans statistics endpoint
    print("Testing procurement plans statistics endpoint...")
    try:
        response = requests.get(f"{base_url}/estatisticas/planos", timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Procurement plans data: {data}")
            print("✓ Procurement plans statistics endpoint working correctly")
        else:
            print(f"✗ Procurement plans statistics endpoint failed with status {response.status_code}")
    except Exception as e:
        print(f"✗ Procurement plans statistics endpoint failed with error: {e}")

if __name__ == "__main__":
    test_advanced_statistics()