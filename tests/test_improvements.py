import requests
import json
from datetime import datetime

# Test our improved endpoint for open tenders with additional filters
try:
    # Set up parameters with correct date format (yyyyMMdd)
    params = {
        'dataFinal': datetime.now().strftime('%Y%m%d'),  # Correct format
        'pagina': 1,
        'tamanhoPagina': 10,  # Minimum allowed value
        'uf': 'SP',  # Filter by São Paulo
        'palavraChave': 'serviço'  # Filter by keyword
    }
    
    # Call our Flask API endpoint
    response = requests.get('http://127.0.0.1:5000/api/licitacoes/abertas', params=params, timeout=10)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Total de registros: {data.get('totalRegistros', 'N/A')}")
        print(f"Total de páginas: {data.get('totalPaginas', 'N/A')}")
        print(f"Número de itens retornados: {len(data.get('data', []))}")
        
        # Show first item as example
        if data.get('data'):
            first_item = data['data'][0]
            print("\nPrimeiro item:")
            print(f"  Número: {first_item.get('numeroCompra', 'N/A')}")
            print(f"  Órgão: {first_item.get('orgaoEntidade', {}).get('razaoSocial', 'N/A')}")
            print(f"  Objeto: {first_item.get('objetoCompra', 'N/A')[:100]}...")
    else:
        print(f"Error Response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")