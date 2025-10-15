import requests
import json
from datetime import datetime

# Test our new endpoint for open tenders
try:
    # Set up parameters with correct date format (yyyyMMdd)
    params = {
        'dataFinal': datetime.now().strftime('%Y%m%d'),  # Correct format
        'pagina': 1,
        'tamanhoPagina': 10  # Minimum allowed value
    }
    
    # Call our Flask API endpoint
    response = requests.get('http://127.0.0.1:5000/api/licitacoes/abertas', params=params, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    
    if response.status_code == 200:
        data = response.json()
        print("\nResponse Data:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(f"Error Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")