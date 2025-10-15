import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PNCP API endpoints
PNCP_API_BASE = "https://pncp.gov.br/api/pncp"
CONSULTA_API_BASE = "https://pncp.gov.br/api/consulta"

def debug_tender_details(numeroControlePNCP):
    """Debug tender details fetching from PNCP API"""
    print(f"Debugging tender details for: {numeroControlePNCP}")
    print("="*50)
    
    # Try different endpoints
    endpoints = [
        f"{CONSULTA_API_BASE}/v1/contratacoes/{numeroControlePNCP}",
        f"{PNCP_API_BASE}/v1/contratacoes/{numeroControlePNCP}",
        f"{PNCP_API_BASE}/contratacoes/{numeroControlePNCP}"
    ]
    
    for url in endpoints:
        print(f"\nTrying URL: {url}")
        try:
            response = requests.get(url, timeout=30)
            print(f"Status Code: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Content Length: {len(response.content)}")
            
            if response.content:
                print(f"Content Preview (first 500 chars): {response.text[:500]}")
                
                # Try to parse as JSON
                try:
                    json_data = response.json()
                    print("Successfully parsed as JSON")
                    print(f"JSON Keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Not a dict'}")
                except Exception as e:
                    print(f"Failed to parse as JSON: {e}")
                    if response.text.strip().startswith('<'):
                        print("Content appears to be HTML")
            else:
                print("Response is empty")
                
        except Exception as e:
            print(f"Request failed: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    # Test with the problematic IDs
    test_ids = [
        "18428888000123-1-000178/2024",
        "17254509000163-1-000017/2025"
    ]
    
    for tender_id in test_ids:
        debug_tender_details(tender_id)
        print("\n" + "="*60 + "\n")