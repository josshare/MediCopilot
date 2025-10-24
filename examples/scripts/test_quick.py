#!/usr/bin/env python3
"""
Script de testing rápido para MediCopilot API
Tests básicos para verificar funcionalidad esencial
"""

import requests
import json
import time

def test_api_quick():
    """Ejecuta tests rápidos de la API"""
    base_url = "http://localhost:8000"
    
    print("🚀 Test rápido de MediCopilot API")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. Verificando salud de la API...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API funcionando - Status: {data.get('status')}")
        else:
            print(f"   ❌ Error en health check - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error conectando a la API: {e}")
        return False
    
    # Test 2: Query health
    print("2. Verificando servicio de consultas...")
    try:
        response = requests.get(f"{base_url}/query/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Servicio de consultas funcionando - Status: {data.get('status')}")
        else:
            print(f"   ❌ Error en query health - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en servicio de consultas: {e}")
    
    # Test 3: Document stats
    print("3. Verificando estadísticas de documentos...")
    try:
        response = requests.get(f"{base_url}/documents/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estadísticas disponibles - Documentos: {data.get('total_documents', 0)}")
        else:
            print(f"   ❌ Error en stats - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error obteniendo estadísticas: {e}")
    
    # Test 4: Consulta de prueba
    print("4. Probando consulta médica...")
    try:
        payload = {
            "question": "¿Qué es el paracetamol?",
            "max_results": 3
        }
        response = requests.post(f"{base_url}/query/", json=payload)
        if response.status_code == 200:
            data = response.json()
            answer_length = len(data.get('answer', ''))
            sources_count = len(data.get('sources', []))
            print(f"   ✅ Consulta exitosa - Respuesta: {answer_length} chars, Fuentes: {sources_count}")
        else:
            print(f"   ❌ Error en consulta - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error en consulta: {e}")
    
    print("\n✅ Test rápido completado")
    return True

if __name__ == "__main__":
    test_api_quick()
