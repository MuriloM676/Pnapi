"""
Unit tests for helpers module.
"""
import pytest
from app.core.utils.helpers import (
    format_currency, 
    format_date, 
    get_modalidade_name, 
    truncate_text,
    convert_pncp_id_to_url
)


def test_format_currency():
    """Test currency formatting."""
    assert format_currency(1234.56) == "1.234,56"
    assert format_currency(1000000.00) == "1.000.000,00"
    assert format_currency(0) == "0,00"


def test_format_date():
    """Test date formatting."""
    # Test ISO format
    assert format_date("2023-10-15T10:30:00Z") == "15/10/2023"
    
    # Test YYYYMMDD format
    assert format_date("20231015") == "15/10/2023"
    
    # Test invalid format
    assert format_date("invalid") == "invalid"
    
    # Test empty string
    assert format_date("") == "N/A"


def test_get_modalidade_name():
    """Test modalidade name retrieval."""
    assert get_modalidade_name("6") == "Pregão"
    assert get_modalidade_name("1") == "Concorrência"
    assert get_modalidade_name("999") == "999"  # Unknown code


def test_truncate_text():
    """Test text truncation."""
    assert truncate_text("This is a long text", 10) == "This is a ..."
    assert truncate_text("Short", 10) == "Short"
    assert truncate_text("", 10) == "N/A"


def test_convert_pncp_id_to_url():
    """Test PNCP ID to URL conversion."""
    # Test valid format
    assert convert_pncp_id_to_url("18428888000123-1-000178/2024") == "18428888000123/2024/178"
    
    # Test invalid format
    assert convert_pncp_id_to_url("invalid") == "invalid"