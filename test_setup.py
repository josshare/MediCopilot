#!/usr/bin/env python3
"""
Simple test script to verify MediCopilot setup
Run this after setting up your .env file with Saptiva API key
"""

import os
import sys
import requests
import time
from pathlib import Path

def test_weaviate_connection():
    """Test Weaviate connection"""
    try:
        response = requests.get("http://localhost:8080/v1/meta", timeout=5)
        if response.status_code == 200:
            print("✅ Weaviate is running")
            return True
        else:
            print(f"❌ Weaviate returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Weaviate: {e}")
        return False

def test_api_connection():
    """Test API connection"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running - Status: {data['status']}")
            print(f"   Weaviate: {data['weaviate_status']}")
            print(f"   API: {data['api_status']}")
            return data['status'] == 'healthy'
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_document_upload():
    """Test document upload with a sample text file"""
    try:
        # Create a sample medical document
        sample_content = """
        PARACETAMOL (ACETAMINOFEN)
        
        Indicaciones:
        - Analgesia leve a moderada
        - Antipirético
        - Dolor de cabeza, dental, muscular
        
        Dosis:
        - Adultos: 500-1000mg cada 6-8 horas
        - Máximo: 4g por día
        
        Efectos secundarios:
        - Raros: reacciones alérgicas
        - En sobredosis: hepatotoxicidad
        
        Contraindicaciones:
        - Insuficiencia hepática severa
        - Alergia conocida al paracetamol
        """
        
        # Create temporary file
        with open("data/test_document.txt", "w", encoding="utf-8") as f:
            f.write(sample_content)
        
        # Upload file
        with open("data/test_document.txt", "rb") as f:
            files = {"file": ("test_document.txt", f, "text/plain")}
            response = requests.post("http://localhost:8000/documents/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document uploaded successfully")
            print(f"   Document ID: {data['document_id']}")
            print(f"   Chunks created: {data['chunks_created']}")
            return data['document_id']
        else:
            print(f"❌ Document upload failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Document upload test failed: {e}")
        return None

def test_query(document_id):
    """Test query functionality"""
    try:
        query_data = {
            "question": "¿Cuáles son los efectos secundarios del paracetamol?",
            "max_results": 3
        }
        
        response = requests.post("http://localhost:8000/query/", json=query_data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query successful")
            print(f"   Question: {data['query']}")
            print(f"   Answer: {data['answer'][:100]}...")
            print(f"   Sources found: {len(data['sources'])}")
            return True
        else:
            print(f"❌ Query failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 MediCopilot Setup Test")
    print("=" * 40)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ .env file not found. Please copy env.example to .env and add your Saptiva API key")
        sys.exit(1)
    
    # Check if Saptiva API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("SAPTIVA_API_KEY") or os.getenv("SAPTIVA_API_KEY") == "your_saptiva_api_key_here":
        print("❌ Saptiva API key not configured in .env file")
        sys.exit(1)
    
    print("✅ Configuration looks good")
    print()
    
    # Test connections
    print("Testing connections...")
    weaviate_ok = test_weaviate_connection()
    api_ok = test_api_connection()
    
    if not weaviate_ok or not api_ok:
        print("\n❌ Basic connections failed. Make sure Docker Compose is running:")
        print("   docker-compose up")
        sys.exit(1)
    
    print()
    
    # Test document upload
    print("Testing document upload...")
    document_id = test_document_upload()
    
    if not document_id:
        print("\n❌ Document upload failed")
        sys.exit(1)
    
    print()
    
    # Wait a moment for processing
    print("Waiting for document processing...")
    time.sleep(2)
    
    # Test query
    print("Testing query functionality...")
    query_ok = test_query(document_id)
    
    if not query_ok:
        print("\n❌ Query functionality failed")
        sys.exit(1)
    
    print()
    print("🎉 All tests passed! MediCopilot is ready to use.")
    print("\nNext steps:")
    print("1. Visit http://localhost:8000/docs for API documentation")
    print("2. Upload your medical documents")
    print("3. Start asking medical questions!")

if __name__ == "__main__":
    main()

