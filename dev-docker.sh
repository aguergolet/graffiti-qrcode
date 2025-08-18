#!/bin/bash

# Script para desenvolvimento local com Docker
echo "🚀 Iniciando ambiente de desenvolvimento com Docker..."

cd webserver

# Verificar se a imagem existe
if ! docker images | grep -q tlgcode; then
    echo "📦 Construindo imagem Docker..."
    docker build -t tlgcode .
fi

echo "🐳 Iniciando container de desenvolvimento..."
docker-compose -f docker-compose.dev.yml up -d

echo "⏳ Aguardando aplicação inicializar..."
sleep 3

echo "🔍 Verificando status dos containers..."
if docker ps | grep -q qrcode_website; then
    echo "✅ Container de desenvolvimento rodando!"
    echo "🌐 Aplicação disponível em: http://localhost:8000/qrcode/"
    echo "📊 Logs: docker logs qrcode_website"
else
    echo "❌ Erro: Container não está rodando"
    docker logs qrcode_website || echo "Logs não disponíveis"
    exit 1
fi
