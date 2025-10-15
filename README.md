# 🌐 PNCP API Client

Sistema web para consulta e análise de licitações públicas através da API do Portal Nacional de Contratações Públicas (PNCP).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Redis](https://img.shields.io/badge/Redis-5.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📋 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Contribuindo](#-contribuindo)

---

## ✨ Características

- 🔍 **Consulta de Licitações**: Busca licitações abertas com filtros avançados
- 📊 **Estatísticas**: Visualização de dados agregados e análises
- 💾 **Cache Redis**: Sistema de cache para melhor performance
- 🏥 **Health Check**: Monitoramento de saúde da aplicação
- 🎨 **Interface Responsiva**: Design adaptável para desktop e mobile
- 📈 **Gráficos Interativos**: Visualizações de dados dinâmicas
- 🔄 **Proxy API**: Acesso simplificado à API do PNCP

---

## 📦 Requisitos

### Obrigatórios
- **Python 3.8+**
- **Redis Server** (para cache)
- **pip** (gerenciador de pacotes Python)

### Opcional
- **Git** (para clonar o repositório)
- **virtualenv** (recomendado para ambiente isolado)

---

## 🚀 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/MuriloM676/Pnapi.git
cd Pnapi
```

### 2. Crie um Ambiente Virtual

#### Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Instale e Configure o Redis

#### Windows:
```powershell
# Veja instruções detalhadas em: docs/install_redis_windows.md
# Ou baixe de: https://github.com/microsoftarchive/redis/releases
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Mac (usando Homebrew):
```bash
brew install redis
brew services start redis
```

#### Verificar instalação:
```bash
redis-cli ping
# Deve retornar: PONG
```

---

## ⚙️ Configuração

### 1. Crie o arquivo `.env`

Copie o arquivo de exemplo e configure:

```bash
cp .env.example .env
```

### 2. Edite o `.env` com suas configurações

```env
# Flask Configuration
FLASK_APP=wsgi.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-forte

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
# REDIS_PASSWORD=sua_senha_se_necessario

# PNCP API (opcional - usa defaults se não configurado)
# PNCP_API_BASE=https://pncp.gov.br/api/pncp
# CONSULTA_API_BASE=https://pncp.gov.br/api/consulta
```

### 3. Gere uma Secret Key Segura

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o resultado e cole no `.env` como valor de `SECRET_KEY`.

---

## 🏃 Como Executar

### Modo Desenvolvimento

```bash
# Certifique-se que o Redis está rodando
redis-cli ping

# Execute a aplicação
python wsgi.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

### Modo Produção

```bash
# Instale gunicorn
pip install gunicorn

# Execute com gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:application
```

### Usando Scripts Auxiliares

#### Windows:
```powershell
# Inicie o Redis (se não estiver rodando)
.\scripts\start_redis.bat
```

---

## 📁 Estrutura do Projeto

```
Pnapi/
├── app/                        # Código principal da aplicação
│   ├── __init__.py            # Factory da aplicação Flask
│   ├── api/                   # Rotas da API
│   │   ├── routes/           # Endpoints organizados
│   │   └── blueprints.py     # Registro de blueprints
│   ├── config/               # Configurações
│   │   ├── settings.py       # Configurações por ambiente
│   │   └── environments/     # Dev, Test, Production
│   ├── core/                 # Lógica de negócio
│   │   ├── models/          # Modelos de dados
│   │   ├── services/        # Serviços (PNCP, etc)
│   │   └── utils/           # Utilitários
│   ├── extensions/           # Extensões Flask
│   │   ├── redis_client.py  # Cliente Redis
│   │   └── redis_cache.py   # Sistema de cache
│   ├── static/              # Arquivos estáticos
│   │   ├── css/
│   │   └── js/
│   ├── templates/           # Templates HTML
│   └── utils/               # Utilitários gerais
├── tests/                    # Testes automatizados
│   ├── unit/                # Testes unitários
│   ├── integration/         # Testes de integração
│   └── fixtures/            # Dados de teste
├── scripts/                  # Scripts auxiliares
├── docs/                     # Documentação
├── requirements.txt          # Dependências Python
├── wsgi.py                  # Entry point WSGI
└── .env                     # Variáveis de ambiente (não versionado)
```

---

## 🔌 API Endpoints

### Principais Endpoints

#### Health Check
```http
GET /api/health
```
Retorna o status de saúde da aplicação e serviços.

#### Licitações Abertas
```http
GET /api/licitacoes/abertas
```

**Parâmetros:**
- `dataFinal` (string): Data final no formato YYYYMMDD
- `uf` (string): Sigla do estado (ex: SP, RJ)
- `codigoModalidadeContratacao` (int): Código da modalidade
- `palavraChave` (string): Palavra-chave para busca
- `pagina` (int): Número da página (padrão: 1)
- `tamanhoPagina` (int): Itens por página (mínimo: 10)

**Exemplo:**
```bash
curl "http://localhost:5000/api/licitacoes/abertas?uf=SP&pagina=1&tamanhoPagina=20"
```

#### Estatísticas
```http
GET /api/estatisticas
```
Retorna estatísticas agregadas de licitações.

#### Proxy PNCP
```http
GET /api/proxy/pncp/<path:path>
POST /api/proxy/pncp/<path:path>
```
Proxy transparente para a API do PNCP.

### Páginas Web

- `/` - Página inicial
- `/licitacoes` - Busca de licitações
- `/estatisticas` - Dashboard de estatísticas
- `/consulta` - Consulta avançada
- `/api-docs` - Documentação da API do PNCP

---

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/
```

### Executar com Cobertura

```bash
pytest tests/ --cov=app --cov-report=html
```

O relatório será gerado em `htmlcov/index.html`.

### Executar Testes Específicos

```bash
# Testes unitários apenas
pytest tests/unit/

# Testes de integração
pytest tests/integration/

# Teste específico
pytest tests/test_api.py::test_health_endpoint
```

---

## 🚢 Deploy

### Deploy com Docker (Recomendado)

```dockerfile
# Dockerfile exemplo
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:application"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - REDIS_HOST=redis
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### Deploy Manual

1. Configure o servidor (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx redis-server
```

2. Clone e configure:
```bash
cd /var/www
git clone https://github.com/MuriloM676/Pnapi.git
cd Pnapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure Nginx como proxy reverso
4. Configure systemd service para auto-start
5. Configure SSL com Let's Encrypt

---

## 🐛 Troubleshooting

### Redis não conecta

```bash
# Verifique se o Redis está rodando
redis-cli ping

# Se não estiver, inicie:
# Windows: execute start_redis.bat
# Linux/Mac: sudo systemctl start redis-server
```

### Erro de importação de módulos

```bash
# Certifique-se que está no ambiente virtual
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### API do PNCP retorna erro

- Verifique sua conexão com a internet
- A API do PNCP pode estar temporariamente indisponível
- Verifique o health check: http://localhost:5000/api/health

---

## 📊 Monitoramento

### Verificar Saúde da Aplicação

```bash
curl http://localhost:5000/api/health
```

### Monitorar Redis

```bash
redis-cli info stats
redis-cli info memory
```

### Logs da Aplicação

Os logs são escritos no console. Em produção, configure para arquivo:

```python
# No wsgi.py ou config
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o código PEP 8 compliant
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Use commits semânticos (feat, fix, docs, etc)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autores

- **Murilo M** - *Desenvolvimento inicial* - [@MuriloM676](https://github.com/MuriloM676)

---

## 🙏 Agradecimentos

- Portal Nacional de Contratações Públicas (PNCP) pela API pública
- Comunidade Flask e Redis
- Todos os contribuidores do projeto

---

## 📞 Suporte

- 📧 Email: [criar issue no GitHub]
- 🐛 Bugs: [GitHub Issues](https://github.com/MuriloM676/Pnapi/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/MuriloM676/Pnapi/discussions)

---

## 🔗 Links Úteis

- [Documentação da API PNCP](https://pncp.gov.br/api/swagger-ui/index.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Redis Documentation](https://redis.io/documentation)

---

**Feito com ❤️ para facilitar o acesso a dados públicos de licitações no Brasil**
