# 🛠️ Comandos Úteis - PNCP API Client

## 📦 Gerenciamento de Dependências

### Instalar todas as dependências
```bash
pip install -r requirements.txt
```

### Atualizar uma dependência específica
```bash
pip install --upgrade flask
```

### Gerar requirements.txt atualizado
```bash
pip freeze > requirements.txt
```

### Instalar dependências de desenvolvimento
```bash
pip install pytest pytest-cov black flake8 mypy
```

---

## 🐳 Redis

### Iniciar Redis
```bash
# Windows
.\scripts\start_redis.bat

# Linux/Mac
sudo systemctl start redis-server
# ou
redis-server
```

### Verificar Status
```bash
redis-cli ping
```

### Conectar ao Redis CLI
```bash
redis-cli
```

### Comandos úteis no Redis CLI
```redis
# Ver todas as chaves
KEYS *

# Ver informações
INFO

# Limpar todas as chaves (cuidado!)
FLUSHALL

# Ver memória usada
INFO memory

# Ver estatísticas
INFO stats

# Sair
EXIT
```

---

## 🧪 Testes

### Executar todos os testes
```bash
pytest tests/
```

### Executar com cobertura
```bash
pytest tests/ --cov=app --cov-report=html
```

### Executar testes específicos
```bash
# Por arquivo
pytest tests/test_api.py

# Por função
pytest tests/test_api.py::test_health_endpoint

# Por diretório
pytest tests/unit/
```

### Executar com verbose
```bash
pytest tests/ -v
```

### Executar e parar no primeiro erro
```bash
pytest tests/ -x
```

---

## 🎨 Qualidade de Código

### Formatar código com Black
```bash
# Formatar tudo
black app/ tests/

# Ver o que seria mudado (dry-run)
black app/ --check

# Formatar arquivo específico
black app/api/routes/api.py
```

### Linting com Flake8
```bash
# Verificar tudo
flake8 app/ tests/

# Ignorar erros específicos
flake8 app/ --ignore=E501,W503

# Ver estatísticas
flake8 app/ --statistics
```

### Type checking com MyPy
```bash
# Verificar tipos
mypy app/

# Mais rigoroso
mypy app/ --strict
```

---

## 🚀 Executar Aplicação

### Modo Desenvolvimento
```bash
# Padrão
python wsgi.py

# Com auto-reload
FLASK_ENV=development python wsgi.py
```

### Modo Produção
```bash
# Com Gunicorn (4 workers)
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:application

# Com logs
gunicorn --bind 0.0.0.0:8000 --workers 4 --access-logfile - --error-logfile - wsgi:application

# Em background
gunicorn --bind 0.0.0.0:8000 --workers 4 --daemon wsgi:application
```

---

## 🔍 Debugging

### Ver logs em tempo real
```bash
# Linux/Mac
tail -f app.log

# Windows (PowerShell)
Get-Content app.log -Wait
```

### Testar endpoints com curl

#### Health Check
```bash
curl http://localhost:5000/api/health
```

#### Licitações Abertas
```bash
# Básico
curl "http://localhost:5000/api/licitacoes/abertas"

# Com filtros
curl "http://localhost:5000/api/licitacoes/abertas?uf=SP&pagina=1&tamanhoPagina=20"

# Com palavra-chave
curl "http://localhost:5000/api/licitacoes/abertas?palavraChave=computador"

# Formatado (com jq)
curl "http://localhost:5000/api/licitacoes/abertas?uf=SP" | jq
```

#### Estatísticas
```bash
curl http://localhost:5000/api/estatisticas
```

### Testar com Python
```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Licitações
response = requests.get('http://localhost:5000/api/licitacoes/abertas', 
                       params={'uf': 'SP', 'pagina': 1})
print(response.json())
```

---

## 📊 Monitoramento

### Ver processos Python rodando
```bash
# Windows (PowerShell)
Get-Process python

# Linux/Mac
ps aux | grep python
```

### Ver uso de porta
```bash
# Windows (PowerShell)
Get-NetTCPConnection -LocalPort 5000

# Linux/Mac
lsof -i :5000
```

### Matar processo na porta
```bash
# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

---

## 🗄️ Banco de Dados / Cache

### Limpar cache Redis
```python
# Via Python
from app.extensions import redis_client
redis_client.flushall()
```

```bash
# Via CLI
redis-cli FLUSHALL
```

### Ver estatísticas de cache
```bash
curl http://localhost:5000/api/health | jq '.cache'
```

---

## 🔧 Manutenção

### Limpar arquivos temporários
```bash
# Windows (PowerShell)
Remove-Item -Recurse -Force __pycache__, .pytest_cache, htmlcov, *.pyc

# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache htmlcov .coverage
```

### Atualizar Git
```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Commit
git commit -m "feat: adicionar melhorias"

# Push
git push origin main
```

### Criar backup
```bash
# Windows (PowerShell)
Compress-Archive -Path . -DestinationPath "../backup-$(Get-Date -Format 'yyyyMMdd').zip"

# Linux/Mac
tar -czf ../backup-$(date +%Y%m%d).tar.gz .
```

---

## 🐛 Troubleshooting

### Reinstalar ambiente do zero
```bash
# Desativar e remover venv
deactivate
rm -rf venv/  # Linux/Mac
Remove-Item -Recurse -Force venv  # Windows

# Recriar
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Reinstalar
pip install -r requirements.txt
```

### Verificar versões
```bash
python --version
pip --version
redis-cli --version
flask --version
```

### Ver configuração atual
```bash
# Variáveis de ambiente
# Windows
Get-ChildItem Env:

# Linux/Mac
printenv | grep FLASK
```

---

## 📚 Documentação

### Gerar documentação da API
```bash
# Se tiver Swagger/OpenAPI configurado
# Acesse: http://localhost:5000/api-docs
```

### Ver rotas disponíveis
```python
# Execute no shell Python
from app import create_app
app = create_app()
print(app.url_map)
```

---

## 🚀 Deploy

### Preparar para produção
```bash
# Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Configurar .env
echo "FLASK_ENV=production" > .env
echo "SECRET_KEY=sua_chave_aqui" >> .env

# Testar
gunicorn wsgi:application --bind 0.0.0.0:8000
```

---

## 💡 Dicas

### Ambiente Virtual Automático
Adicione ao seu `.bashrc` ou `.zshrc`:
```bash
# Auto-ativar venv ao entrar na pasta
cd() {
    builtin cd "$@"
    if [[ -d ./venv ]]; then
        source ./venv/bin/activate
    fi
}
```

### Alias úteis
```bash
# .bashrc ou .zshrc
alias pncp-run="python wsgi.py"
alias pncp-test="pytest tests/ -v"
alias pncp-format="black app/ tests/"
alias pncp-lint="flake8 app/ tests/"
```

---

**Estes comandos cobrem 90% das tarefas diárias de desenvolvimento!** 🎯
