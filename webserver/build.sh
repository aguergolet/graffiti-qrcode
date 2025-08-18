#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting build process..."

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found. Please run this script from the webserver directory."
    exit 1
fi

# Check if docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: docker-compose is not installed or not in PATH."
    exit 1
fi

echo "📥 Pulling latest changes from git..."
if git pull; then
    echo "✅ Git pull successful"
else
    echo "⚠️  Git pull failed or no changes"
fi

echo "🐳 Building Docker image..."
if docker build -t tlgcode .; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

echo "🔄 Stopping existing containers..."
if docker-compose down; then
    echo "✅ Containers stopped"
else
    echo "⚠️  No containers to stop or error occurred"
fi

echo "🚀 Starting containers..."
if docker-compose up -d; then
    echo "✅ Containers started successfully"
else
    echo "❌ Failed to start containers"
    exit 1
fi

echo "⏳ Waiting for application to start..."
sleep 5

echo "🔍 Checking container status..."
if docker ps | grep -q qrcode_website; then
    echo "✅ Container is running:"
    docker ps | grep qrcode_website
else
    echo "❌ Container is not running"
    echo "📋 Container logs:"
    docker logs qrcode_website || echo "No logs available"
    exit 1
fi

echo "🎉 Build and deployment completed successfully!"
echo "🌐 Application should be available at: http://localhost:8000"
echo "📊 Container logs: docker logs qrcode_website"
echo "🔍 Container status: docker ps | grep qrcode_website"