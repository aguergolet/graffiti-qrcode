#!/bin/bash

# Script de deploy simplificado para o QR Code Generator
set -e

echo "🚀 Iniciando deploy do QR Code Generator..."

# Verificar se estamos na raiz do projeto
if [ ! -f "webserver/Dockerfile" ]; then
    echo "❌ Erro: Dockerfile não encontrado. Execute este script da raiz do projeto."
    exit 1
fi

# Verificar se o Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Erro: Docker não está rodando. Inicie o Docker primeiro."
    exit 1
fi

echo "📥 Atualizando código do repositório..."
git pull

echo "🐳 Construindo imagem Docker..."
cd webserver
docker build -t tlgcode .

echo "🔄 Parando containers existentes..."
docker-compose down

echo "🚀 Iniciando containers..."
docker-compose up -d

echo "⏳ Aguardando aplicação inicializar..."
sleep 3

echo "🔍 Verificando status dos containers..."
if docker ps | grep -q qrcode_website; then
    echo "✅ Deploy concluído com sucesso!"
    echo "🌐 Aplicação disponível em: http://localhost:8000"
    echo "📊 Logs: docker logs qrcode_website"
else
    echo "❌ Erro: Container não está rodando"
    docker logs qrcode_website || echo "Logs não disponíveis"
    exit 1
fi
