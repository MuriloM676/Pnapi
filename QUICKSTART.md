# 🚀 Guia Rápido de Início - PNCP API Client

## ⚡ Início Rápido em 5 Minutos

### 1️⃣ Clone e Entre no Diretório
```bash
git clone https://github.com/MuriloM676/Pnapi.git
cd Pnapi
```

### 2️⃣ Crie o Ambiente Virtual
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure o Ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Gere uma secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Cole o resultado no .env como SECRET_KEY
```

### 5️⃣ Instale e Inicie o Redis

**Windows:**
- Baixe Redis para Windows: https://github.com/microsoftarchive/redis/releases
- Extraia e execute `redis-server.exe`
- Ou use: `.\scripts\start_redis.bat`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Verificar Redis:**
```bash
redis-cli ping
# Deve retornar: PONG
```

### 6️⃣ Execute a Aplicação
```bash
python wsgi.py
```

### 7️⃣ Acesse o Site
Abra seu navegador em: **http://127.0.0.1:5000**

---

## 🎯 Primeiros Testes

### Verificar Saúde da API
```bash
curl http://localhost:5000/api/health
```

### Buscar Licitações Abertas
```bash
curl "http://localhost:5000/api/licitacoes/abertas?uf=SP&pagina=1"
```

### Ver Estatísticas
Acesse: http://localhost:5000/estatisticas

---

## 🐛 Problemas Comuns

### Erro: "Redis connection refused"
**Solução:** Certifique-se que o Redis está rodando
```bash
redis-cli ping
# Se não responder, inicie o Redis
```

### Erro: "ModuleNotFoundError: No module named 'flask'"
**Solução:** Ative o ambiente virtual
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Port 5000 already in use"
**Solução:** Mude a porta no wsgi.py ou mate o processo
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

---

## 📚 Próximos Passos

1. ✅ Explore a interface em: http://localhost:5000
2. ✅ Teste os filtros de busca
3. ✅ Veja as estatísticas
4. ✅ Consulte a documentação da API em: http://localhost:5000/api-docs
5. ✅ Leia o README.md completo para funcionalidades avançadas

---

## 🆘 Precisa de Ajuda?

- 📖 README completo: [README.md](README.md)
- 🐛 Reportar problemas: [GitHub Issues](https://github.com/MuriloM676/Pnapi/issues)
- 📚 Documentação técnica: [docs/](docs/)

---

**Pronto! Você está rodando o PNCP API Client! 🎉**
