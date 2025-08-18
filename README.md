# 🎨 Graffiti QRCode Generator

[![Deploy Status](https://github.com/your-username/graffiti-qrcode/workflows/Deploy%20to%20Production%20Server/badge.svg)](https://github.com/your-username/graffiti-qrcode/actions)
[![Test Status](https://github.com/your-username/graffiti-qrcode/workflows/Test%20and%20Validate/badge.svg)](https://github.com/your-username/graffiti-qrcode/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Gerador moderno de QR Codes para criação de stencils de impressão 3D, com interface web responsiva e autenticação Google OAuth.

## ✨ Características

- 🎯 **Geração de QR Codes** para URLs personalizadas
- 🖨️ **Exportação STL** otimizada para impressão 3D
- 🔐 **Autenticação Google OAuth** para controle de acesso
- 📱 **Interface responsiva** com design moderno
- 🚀 **Deploy automatizado** via GitHub Actions
- 🐳 **Containerização Docker** para fácil implantação
- 📊 **Histórico de arquivos** gerados por usuário
- 🎨 **Design glassmorphism** com gradientes modernos

## 🚀 Tecnologias

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Containerização**: Docker & Docker Compose
- **Autenticação**: Google OAuth 2.0
- **Deploy**: GitHub Actions + SSH
- **Servidor Web**: Traefik (reverse proxy)
- **SSL**: Let's Encrypt (automático)

## 📋 Pré-requisitos

- Python 3.9+
- Docker & Docker Compose
- Conta Google para OAuth
- Servidor Linux com SSH habilitado

## 🛠️ Instalação Local

### 1. Clone o repositório
```bash
git clone https://github.com/your-username/graffiti-qrcode.git
cd graffiti-qrcode
```

### 2. Configure as variáveis de ambiente
```bash
# Configure as variáveis de ambiente
cp env.example .env
# Edite o arquivo .env com suas credenciais do Google OAuth
```

### 3. Scripts disponíveis
```bash
# Deploy completo com Docker (recomendado para produção)
./deploy.sh

# Build rápido (apenas reconstrói e inicia)
./build.sh

# Desenvolvimento local sem Docker
./dev.sh
```

### 3. Execute com Docker
```bash
# Deploy completo (recomendado)
./deploy.sh

# Ou apenas build rápido
./build.sh

# Ou desenvolvimento local sem Docker
./dev.sh
```

### 4. Acesse a aplicação
```
http://localhost:8000 (com Docker)
http://localhost:5000 (desenvolvimento local)
```

## 🌐 Deploy em Produção

### Configuração Automática (Recomendado)

1. **Configure os Secrets do GitHub**:
   - `SSH_PRIVATE_KEY`: Chave privada SSH para o servidor
   - `SERVER_HOST`: IP/domínio do servidor
   - `SERVER_USER`: Usuário do servidor
   - `DEPLOY_PATH`: Caminho da aplicação no servidor

2. **Deploy automático**:
   - Push para `main` ou `master` = deploy automático
   - Ou execute manualmente via GitHub Actions

### Configuração Manual

```bash
# No servidor
cd /home/user/graffiti-qrcode/webserver
git pull origin main
chmod +x build.sh
./build.sh
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# Flask
FLASK_ENV=production
SERVER_NAME=your-domain.com
APPLICATION_ROOT=/qrcode
PREFERRED_URL_SCHEME=https
```

### Docker Compose

O arquivo `docker-compose.yml` inclui:
- Configuração Traefik para reverse proxy
- Volume persistente para arquivos de usuário
- Rede externa para integração com outros serviços
- Labels para roteamento automático

## 📱 Uso

### 1. **Login**
- Acesse a aplicação
- Clique em "Entrar com Google"
- Autorize o acesso

### 2. **Gerar QR Code**
- Cole a URL desejada no campo
- Clique em "Gerar QR Code"
- Aguarde 2-3 minutos para processamento

### 3. **Download**
- Visualize o QR Code gerado
- Baixe o arquivo STL para impressão 3D
- Siga as instruções de impressão

## 🎯 Instruções de Impressão 3D

- ✅ **Mantenha as proporções** para não deixar retangular
- ✅ **Preenchimento indiferente**
- ❌ **NÃO coloque SUPORTE**
- ❌ **NÃO coloque ADESÃO** (vai tapar o stencil)

## 🔍 Estrutura do Projeto

```
graffiti-qrcode/
├── .github/                 # GitHub Actions workflows
│   ├── workflows/
│   │   ├── deploy.yml      # Deploy automático
│   │   └── test.yml        # Testes e validação
│   └── README.md           # Documentação do deploy
├── webserver/              # Aplicação principal
│   ├── main.py            # Servidor Flask
│   ├── Dockerfile         # Container da aplicação
│   ├── docker-compose.yml # Orquestração Docker
│   ├── build.sh           # Script de build
│   ├── requirements.txt   # Dependências Python
│   ├── templates/         # Templates HTML
│   ├── static/            # Arquivos estáticos
│   └── tlgCode/           # Código de geração STL
├── LICENSE                 # Licença MIT
└── README.md              # Este arquivo
```

## 🧪 Testes

### Execução Local
```bash
cd webserver
python -m pytest
```

### Validação Automática
- **Linting**: flake8, black
- **Validação HTML**: html5validator
- **Segurança**: Snyk Docker scan
- **Build**: Teste de construção Docker

## 🚀 CI/CD

### GitHub Actions
- **Test**: Executa em PRs e pushes
- **Deploy**: Deploy automático para produção
- **Validação**: Verificação de qualidade de código

### Workflows
1. **Test and Validate**: Validação de código
2. **Deploy to Production**: Deploy automático

## 📊 Monitoramento

### Logs
```bash
# Container
docker logs qrcode_website

# Aplicação
docker exec qrcode_website tail -f /app/logs/app.log
```

### Status
```bash
# Containers
docker ps

# Recursos
docker stats qrcode_website
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [Bootstrap](https://getbootstrap.com/) - Framework CSS
- [Docker](https://www.docker.com/) - Containerização
- [Traefik](https://traefik.io/) - Reverse proxy
- [Google OAuth](https://developers.google.com/identity/protocols/oauth2) - Autenticação

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-username/graffiti-qrcode/issues)
- **Documentação**: [Wiki](https://github.com/your-username/graffiti-qrcode/wiki)
- **Email**: suporte@guergolet.com.br

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!**
