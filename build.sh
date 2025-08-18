#!/bin/bash
# Script de build rápido - use deploy.sh para deploy completo
cd webserver
docker build -t tlgcode .
docker-compose up -d