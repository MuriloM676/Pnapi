"""
API endpoints routes for PNCP API Client.
"""
from flask import Blueprint, request, jsonify
import requests
from datetime import datetime, timedelta
import logging
from app.extensions import redis_client
from app.core.services.pncp_service import PNCPService

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configure logging
logger = logging.getLogger(__name__)

# Initialize services
pncp_service = PNCPService()


@api_bp.route('/test')
def test_api():
    """Test endpoint to verify API is working."""
    return jsonify({"message": "API is working correctly"}), 200


@api_bp.route('/licitacoes/abertas')
def get_open_tenders():
    """Get open tenders from PNCP API with Redis caching."""
    try:
        return pncp_service.get_open_tenders(request.args)
    except Exception as e:
        logger.error(f"Error in get_open_tenders: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/licitacoes/detalhes/<path:numeroControlePNCP>')
def get_tender_details(numeroControlePNCP):
    """Get details for a specific tender."""
    try:
        return pncp_service.get_tender_details(numeroControlePNCP)
    except Exception as e:
        logger.error(f"Error in get_tender_details: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/modalidades')
def get_modalidade_stats():
    """Get statistics by modality from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_modalidade_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_modalidade_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/uf')
def get_uf_stats():
    """Get statistics by UF from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_uf_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_uf_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/tipo_orgao')
def get_tipo_orgao_stats():
    """Get statistics by organization type from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_tipo_orgao_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_tipo_orgao_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/contratos')
def get_contratos_stats():
    """Get contracts statistics from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_contratos_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_contratos_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/atas')
def get_atas_stats():
    """Get price registration records statistics from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_atas_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_atas_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


@api_bp.route('/estatisticas/planos')
def get_planos_stats():
    """Get procurement plans statistics from real PNCP API with Redis caching."""
    try:
        return pncp_service.get_planos_stats(request.args)
    except Exception as e:
        logger.error(f"Error in get_planos_stats: {str(e)}")
        return jsonify({"error": str(e)}), 500


