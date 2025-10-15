"""
Integration tests for API endpoints.
"""
from app import create_app


def test_home_page():
    """Test home page loads correctly."""
    app = create_app('testing')
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_licitacoes_page():
    """Test licitacoes page loads correctly."""
    app = create_app('testing')
    with app.test_client() as client:
        response = client.get('/licitacoes')
        assert response.status_code == 200


def test_estatisticas_page():
    """Test estatisticas page loads correctly."""
    app = create_app('testing')
    with app.test_client() as client:
        response = client.get('/estatisticas')
        assert response.status_code == 200


def test_api_docs_page():
    """Test API docs page loads correctly."""
    app = create_app('testing')
    with app.test_client() as client:
        response = client.get('/api_docs')
        assert response.status_code == 200