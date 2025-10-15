from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)

# PNCP API endpoints
PNCP_API_BASE = "https://pncp.gov.br/api/pncp"
CONSULTA_API_BASE = "https://pncp.gov.br/api/consulta"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pncp')
def pncp_page():
    return render_template('pncp.html')

@app.route('/consulta')
def consulta_page():
    return render_template('consulta.html')

@app.route('/licitacoes')
def licitacoes_page():
    return render_template('licitacoes.html')

@app.route('/api/pncp/<path:endpoint>')
def proxy_pncp_api(endpoint):
    """Proxy endpoint to query PNCP API"""
    try:
        url = f"{PNCP_API_BASE}/{endpoint}"
        params = request.args.to_dict()
        
        response = requests.get(url, params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consulta/<path:endpoint>')
def proxy_consulta_api(endpoint):
    """Proxy endpoint to query Consulta API"""
    try:
        url = f"{CONSULTA_API_BASE}/{endpoint}"
        params = request.args.to_dict()
        
        response = requests.get(url, params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New endpoint to get open tenders
@app.route('/api/licitacoes/abertas')
def get_open_tenders():
    """Get open tenders from PNCP API"""
    try:
        # Get parameters from request
        params = {}
        
        # Set default dates (today) in the required format (yyyyMMdd)
        data_final = request.args.get('dataFinal', datetime.now().strftime('%Y%m%d'))
        # If the date is in YYYY-MM-DD format, convert it
        if '-' in data_final:
            date_obj = datetime.strptime(data_final, '%Y-%m-%d')
            data_final = date_obj.strftime('%Y%m%d')
        params['dataFinal'] = data_final
        
        # Add other filters if provided
        codigoModalidadeContratacao = request.args.get('codigoModalidadeContratacao')
        if codigoModalidadeContratacao:
            params['codigoModalidadeContratacao'] = codigoModalidadeContratacao
            
        uf = request.args.get('uf')
        if uf:
            params['uf'] = uf
            
        palavraChave = request.args.get('palavraChave')
        if palavraChave:
            params['palavraChave'] = palavraChave
            
        pagina = request.args.get('pagina', 1)
        params['pagina'] = pagina
        
        # Ensure tamanhoPagina is at least 10 (API requirement)
        tamanhoPagina = request.args.get('tamanhoPagina', 10)
        tamanhoPagina = max(int(tamanhoPagina), 10)
        params['tamanhoPagina'] = tamanhoPagina
        
        # Call the actual API endpoint for open tenders
        url = f"{CONSULTA_API_BASE}/v1/contratacoes/proposta"
        
        response = requests.get(url, params=params)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get tender details
@app.route('/api/licitacoes/<numeroControlePNCP>')
def get_tender_details(numeroControlePNCP):
    """Get details for a specific tender"""
    try:
        # This would call the appropriate API endpoint to get tender details
        # For now, we'll return a placeholder response
        return jsonify({
            "numeroControlePNCP": numeroControlePNCP,
            "detalhes": "Detalhes da licitação (implementação futura)"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)