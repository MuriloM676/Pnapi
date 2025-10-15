import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_tender_details():
    """Test the tender details endpoint with the fixed ID format"""
    # Test with the problematic ID
    original_id = "18428888000123-1-000178/2024"
    print(f"Testing with original ID: {original_id}")
    
    # Parse the ID to extract components
    if '-' in original_id and '/' in original_id:
        parts = original_id.split('-')
        cnpj = parts[0]
        # parts[1] is unknown
        sequencial_part = parts[2]  # 000178/2024
        
        # Split sequencial_part to get sequencial and year
        sequencial_year = sequencial_part.split('/')
        sequencial = sequencial_year[0]  # 000178
        year = sequencial_year[1]  # 2024
        
        # Remove leading zeros from sequencial
        sequencial_number = int(sequencial)
        
        # Construct the correct endpoint format
        api_endpoint = f"{cnpj}/{year}/{sequencial_number}"
        print(f"Converted to API endpoint format: {api_endpoint}")
        
        # Try to call the API with the converted format
        url = f"https://pncp.gov.br/api/consulta/v1/contratacoes/{api_endpoint}"
        print(f"Calling URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Success! Response received.")
                # Print first 500 characters of response
                print(f"Response preview: {response.text[:500]}")
            else:
                print(f"Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
        except Exception as e:
            print(f"Request failed: {e}")
    else:
        print("ID format not as expected")

if __name__ == "__main__":
    test_tender_details()