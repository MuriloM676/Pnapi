"""
Helper functions for PNCP API Client.
"""
from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Modalidade mapping
MODALIDADES = {
    '1': 'Concorrência',
    '2': 'Tomada de Preços',
    '3': 'Convite',
    '4': 'Concurso',
    '5': 'Leilão',
    '6': 'Pregão',
    '7': 'Dispensa de Licitação',
    '8': 'Inexigibilidade de Licitação',
    '12': 'Credenciamento'
}


def format_currency(value: float) -> str:
    """
    Format currency value for Brazilian format.
    
    Args:
        value: Currency value to format
        
    Returns:
        Formatted currency string
    """
    return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_date(date_string: str) -> str:
    """
    Format date string for Brazilian format.
    
    Args:
        date_string: Date string to format
        
    Returns:
        Formatted date string
    """
    if not date_string:
        return 'N/A'
    
    # Handle both date formats that might come from the API
    try:
        if 'T' in date_string:
            from datetime import datetime
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        elif len(date_string) == 8:
            # Assume format is YYYYMMDD
            year = date_string[:4]
            month = date_string[4:6]
            day = date_string[6:8]
            from datetime import date as date_cls
            date = date_cls(int(year), int(month), int(day))
        else:
            return date_string
        
        return date.strftime('%d/%m/%Y')
    except Exception as e:
        logger.error(f"Error formatting date {date_string}: {e}")
        return date_string


def get_modalidade_name(code: str) -> str:
    """
    Get modalidade name by code.
    
    Args:
        code: Modalidade code
        
    Returns:
        Modalidade name
    """
    return MODALIDADES.get(str(code), str(code))


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text:
        return 'N/A'
    if len(text) <= max_length:
        return text
    return text[:max_length] + '...'


def convert_pncp_id_to_url(id_string: str) -> str:
    """
    Convert PNCP ID format to URL format.
    
    Args:
        id_string: PNCP ID in format 18428888000123-1-000178/2024
        
    Returns:
        URL format: 18428888000123/2024/178
    """
    if '-' in id_string and '/' in id_string:
        try:
            # Convert from format: 18428888000123-1-000178/2024
            # To format: 18428888000123/2024/178
            parts = id_string.split('-')
            cnpj = parts[0]
            sequencial_part = parts[2]  # 000178/2024
            
            # Split sequencial_part to get sequencial and year
            sequencial_year = sequencial_part.split('/')
            sequencial = sequencial_year[0]  # 000178
            year = sequencial_year[1]  # 2024
            
            # Remove leading zeros from sequencial
            sequencial_number = int(sequencial)
            
            return f"{cnpj}/{year}/{sequencial_number}"
        except Exception as e:
            logger.error(f"Error converting ID {id_string}: {e}")
            return id_string
    
    return id_string