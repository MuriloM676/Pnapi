import requests
import json

# Test our new statistics endpoints
try:
    print("Testing modalidade statistics endpoint...")
    response = requests.get('http://127.0.0.1:5000/api/estatisticas/modalidades', timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Modalidade Statistics:")
        for item in data:
            print(f"  {item['modalidade']}: {item['quantidade']} licitações, R$ {item['valor']}")
    else:
        print(f"Error: {response.text}")
        
    print("\nTesting UF statistics endpoint...")
    response = requests.get('http://127.0.0.1:5000/api/estatisticas/uf', timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("UF Statistics:")
        for item in data:
            print(f"  {item['uf']}: {item['quantidade']} licitações, R$ {item['valor']}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")