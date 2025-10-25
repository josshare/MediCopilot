#!/bin/bash

# Script para ejecutar las pruebas de diabetes en MediCopilot
# Asegúrate de que la aplicación esté ejecutándose antes de correr este script

echo "🩺 MediCopilot - Ejecutando Pruebas de Diabetes"
echo "=============================================="

# Verificar que Docker esté ejecutándose
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose. Por favor inicia Docker primero."
    exit 1
fi

# Verificar que los servicios estén activos
echo "🔍 Verificando servicios..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ La API no está respondiendo en http://localhost:8000"
    echo "💡 Asegúrate de ejecutar: docker-compose up --build"
    exit 1
fi

echo "✅ Servicios verificados correctamente"

# Ejecutar el script de pruebas
echo "🚀 Iniciando pruebas de diabetes..."
cd /Volumes/Nueva/code/sapiva/MediCopilot

# Verificar que Python esté disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

# Instalar dependencias si es necesario
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "📋 Instalando dependencias..."
pip install requests

echo "🏃‍♂️ Ejecutando pruebas..."
python3 examples/scripts/test_diabetes_queries.py

echo "✅ Pruebas completadas. Revisa los resultados en examples/scripts/"
