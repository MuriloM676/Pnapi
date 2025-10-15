"""
Main pages routes for PNCP API Client.
"""
from flask import Blueprint, render_template

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html')


@main_bp.route('/pncp')
def pncp_page():
    """PNCP page route."""
    return render_template('pncp.html')


@main_bp.route('/consulta')
def consulta_page():
    """Consulta page route."""
    return render_template('consulta.html')


@main_bp.route('/licitacoes')
def licitacoes_page():
    """Licitações page route."""
    return render_template('licitacoes.html')


@main_bp.route('/estatisticas')
def estatisticas_page():
    """Estatísticas page route."""
    return render_template('estatisticas.html')


@main_bp.route('/api_docs')
def api_docs_page():
    """API documentation page route."""
    return render_template('api_docs.html')