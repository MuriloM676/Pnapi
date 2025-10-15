import requests
import json

# Get the Consulta API documentation
try:
    response = requests.get("https://pncp.gov.br/api/consulta/v3/api-docs", timeout=10)
    if response.status_code == 200:
        # Save the raw JSON response
        with open("consulta_api_docs_raw.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        print("Consulta API documentation saved to consulta_api_docs_raw.json")
        
        # Print some key information about the API
        api_data = response.json()
        print("\nAPI Title:", api_data.get("info", {}).get("title", "Unknown"))
        print("API Description:", api_data.get("info", {}).get("description", "Unknown"))
        
        # List some of the available paths
        paths = api_data.get("paths", {})
        print("\nAvailable endpoints (first 10):")
        for i, (path, methods) in enumerate(paths.items()):
            if i >= 10:
                break
            print(f"  {path}: {list(methods.keys())}")
    else:
        print(f"Failed to get API docs. Status code: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")