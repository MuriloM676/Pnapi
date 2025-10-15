def test_id_conversion():
    """Test the ID conversion function"""
    # Test with the problematic ID
    original_id = "18428888000123-1-000178/2024"
    print(f"Original ID: {original_id}")
    
    # Convert from format: 18428888000123-1-000178/2024
    # To format: 18428888000123/2024/178
    if '-' in original_id and '/' in original_id:
        parts = original_id.split('-')
        cnpj = parts[0]
        sequencial_part = parts[2]  # 000178/2024
        
        # Split sequencial_part to get sequencial and year
        sequencial_year = sequencial_part.split('/')
        sequencial = sequencial_year[0]  # 000178
        year = sequencial_year[1]  # 2024
        
        # Remove leading zeros from sequencial
        sequencial_number = int(sequencial)
        
        # Construct the PNCP web URL
        pncp_web_url = f"https://pncp.gov.br/app/editais/{cnpj}/{year}/{sequencial_number}"
        print(f"Converted URL: {pncp_web_url}")
        
        # Expected: https://pncp.gov.br/app/editais/18428888000123/2024/178
        expected = "https://pncp.gov.br/app/editais/18428888000123/2024/178"
        if pncp_web_url == expected:
            print("SUCCESS: ID conversion is working correctly!")
        else:
            print(f"ERROR: Expected {expected}, got {pncp_web_url}")
    else:
        print("ERROR: ID format not as expected")

if __name__ == "__main__":
    test_id_conversion()