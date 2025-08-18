# GitHub Actions - Deploy Configuration

Este diretório contém a configuração do GitHub Actions para deploy automático da aplicação.

## 📋 Secrets Necessários

Para que o deploy funcione, você precisa configurar os seguintes secrets no seu repositório GitHub:

### 🔑 SSH_PRIVATE_KEY
- **Descrição**: Chave privada SSH para acessar o servidor
- **Como gerar**: 
  ```bash
  ssh-keygen -t rsa -b 4096 -C "github-actions@your-domain.com"
  ```
- **Onde colocar**: Copie o conteúdo do arquivo `~/.ssh/id_rsa` (chave privada)
- **Importante**: Adicione a chave pública correspondente ao `~/.ssh/authorized_keys` do servidor

### 🌐 SERVER_HOST
- **Descrição**: Endereço IP ou domínio do servidor
- **Exemplo**: `192.168.1.100` ou `guergolet.com.br`

### 👤 SERVER_USER
- **Descrição**: Nome do usuário no servidor
- **Exemplo**: `andre` ou `root`

### 📁 DEPLOY_PATH
- **Descrição**: Caminho completo para o diretório da aplicação no servidor
- **Exemplo**: `/home/andre/graffiti-qrcode/webserver`

## ⚙️ Configuração dos Secrets

1. Vá para seu repositório no GitHub
2. Clique em **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Adicione cada um dos secrets acima

## 🚀 Como Funciona

### Trigger Automático
- O deploy acontece automaticamente quando você faz push para as branches `main` ou `master`

### Trigger Manual
- Você também pode executar o deploy manualmente através do GitHub Actions
- Vá para **Actions** → **Deploy to Production Server** → **Run workflow**

## 📝 Processo de Deploy

1. **Checkout**: Baixa o código mais recente
2. **SSH Setup**: Configura a conexão SSH com o servidor
3. **Deploy**: 
   - Conecta ao servidor
   - Navega para o diretório da aplicação
   - Executa `git pull origin main`
   - Executa o script `build.sh`
4. **Verificação**: Confirma se o container está rodando
5. **Resumo**: Mostra informações sobre o deploy

## 🔧 Script build.sh

O script `build.sh` no servidor executa:
```bash
git pull
docker build -t tlgcode .
docker-compose down
docker-compose up -d
```

## 🐛 Troubleshooting

### Erro de SSH
- Verifique se a chave privada está correta
- Confirme se a chave pública está no servidor
- Teste a conexão SSH manualmente

### Erro de Permissão
- Verifique se o usuário tem permissão para executar docker
- Confirme se o diretório de deploy existe e tem permissões corretas

### Container não inicia
- Verifique os logs: `docker logs qrcode_website`
- Confirme se as variáveis de ambiente estão configuradas
- Verifique se a porta 8000 está disponível

## 📊 Monitoramento

Após o deploy, você pode monitorar:
- Status do container: `docker ps`
- Logs da aplicação: `docker logs qrcode_website`
- Uso de recursos: `docker stats qrcode_website`
