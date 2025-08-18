#!/bin/bash

# Script para desenvolvimento local
echo "🚀 Iniciando ambiente de desenvolvimento..."

cd webserver

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo "📥 Instalando dependências..."
pip install -r requirements.txt

echo "🌐 Iniciando servidor Flask..."
echo "Acesse: http://localhost:5000"
python main.py
