import requests
import json

# Test accessing the PNCP API to understand available endpoints
try:
    # Try to access the base API URL
    response = requests.get("https://pncp.gov.br/api/pncp/", timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error accessing PNCP API: {e}")

try:
    # Try to access a common health endpoint
    response = requests.get("https://pncp.gov.br/api/pncp/actuator/health", timeout=10)
    print(f"Health Status Code: {response.status_code}")
    print(f"Health Response: {response.text}")
except Exception as e:
    print(f"Error accessing health endpoint: {e}")

try:
    # Try to access what might be a tenders endpoint
    response = requests.get("https://pncp.gov.br/api/pncp/v1/licitacoes", timeout=10)
    print(f"Licitacoes Status Code: {response.status_code}")
    print(f"Licitacoes Response: {response.text[:500]}")  # First 500 chars
except Exception as e:
    print(f"Error accessing licitacoes endpoint: {e}")