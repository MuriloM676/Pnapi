"""
Proxy routes for PNCP API Client.
"""
from flask import Blueprint, request, jsonify
import requests
import logging
from app.config.settings import config

# Create blueprint
proxy_bp = Blueprint('proxy', __name__, url_prefix='/api')

# Configure logging
logger = logging.getLogger(__name__)

# Get configuration
current_config = config['default']()


@proxy_bp.route('/pncp/<path:endpoint>')
def proxy_pncp_api(endpoint):
    """Proxy endpoint to query PNCP API."""
    try:
        url = f"{current_config.PNCP_API_BASE}/{endpoint}"
        params = request.args.to_dict()
        
        logger.info(f"Proxying request to {url} with params: {params}")
        response = requests.get(url, params=params, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout"}), 504
    except Exception as e:
        logger.error(f"Error in proxy_pncp_api: {str(e)}")
        return jsonify({"error": str(e)}), 500


@proxy_bp.route('/consulta/<path:endpoint>')
def proxy_consulta_api(endpoint):
    """Proxy endpoint to query Consulta API."""
    try:
        url = f"{current_config.CONSULTA_API_BASE}/{endpoint}"
        params = request.args.to_dict()
        
        logger.info(f"Proxying request to {url} with params: {params}")
        response = requests.get(url, params=params, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout"}), 504
    except Exception as e:
        logger.error(f"Error in proxy_consulta_api: {str(e)}")
        return jsonify({"error": str(e)}), 500