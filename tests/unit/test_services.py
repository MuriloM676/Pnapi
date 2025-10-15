"""
Unit tests for services module.
"""
from unittest.mock import patch, MagicMock
from app.core.services.pncp_service import PNCPService


def test_pncp_service_initialization():
    """Test PNCP service initialization."""
    service = PNCPService()
    assert service is not None
    assert service.pncp_api_base is not None
    assert service.consulta_api_base is not None


@patch('app.core.services.pncp_service.requests.get')
def test_get_tender_details(mock_get):
    """Test get tender details method."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.json.return_value = {"test": "data"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    service = PNCPService()
    result, status_code = service.get_tender_details("123456")
    
    # Assert the result
    assert status_code == 200
    # Note: We can't easily test the jsonify result in unit tests