#!/bin/bash

echo "🚀 Starting MediCopilot MVP"
echo "=========================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please copy env.example to .env and add your Saptiva API key:"
    echo "   cp env.example .env"
    echo "   # Edit .env and add your SAPTIVA_API_KEY"
    exit 1
fi

# Check if Saptiva API key is configured
if grep -q "your_saptiva_api_key_here" .env; then
    echo "❌ Saptiva API key not configured!"
    echo "Please edit .env and add your actual Saptiva API key"
    exit 1
fi

echo "✅ Configuration looks good"
echo ""

# Start Docker Compose
echo "🐳 Starting Docker services..."
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

echo ""
echo "🧪 Running setup test..."
python3 test_setup.py

echo ""
echo "🎉 MediCopilot is ready!"
echo ""
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Weaviate Console: http://localhost:8080"
echo ""
echo "To stop the services: docker-compose down"

