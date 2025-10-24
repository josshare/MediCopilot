#!/usr/bin/env python3
"""
Script para cargar todos los documentos de prueba en la API
"""

import requests
import os
import time
from pathlib import Path

def load_test_documents(base_url="http://localhost:8000", docs_dir="test-documents"):
    """Carga todos los documentos de prueba"""
    
    print("📚 Cargando documentos de prueba en MediCopilot")
    print("=" * 50)
    
    if not os.path.exists(docs_dir):
        print(f"❌ Directorio no encontrado: {docs_dir}")
        return
    
    # Obtener lista de archivos de texto
    text_files = [f for f in os.listdir(docs_dir) if f.endswith('.txt')]
    
    if not text_files:
        print(f"❌ No se encontraron archivos .txt en {docs_dir}")
        return
    
    print(f"📁 Encontrados {len(text_files)} documentos:")
    for file in text_files:
        print(f"   - {file}")
    
    print("\n🚀 Iniciando carga...")
    
    loaded_documents = []
    failed_documents = []
    
    for i, filename in enumerate(text_files, 1):
        file_path = os.path.join(docs_dir, filename)
        
        print(f"\n{i}/{len(text_files)} Cargando: {filename}")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f, 'text/plain')}
                response = requests.post(f"{base_url}/documents/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                document_id = data.get('document_id')
                chunks = data.get('chunks_created', 0)
                
                loaded_documents.append({
                    'filename': filename,
                    'document_id': document_id,
                    'chunks': chunks
                })
                
                print(f"   ✅ Cargado exitosamente - ID: {document_id}, Chunks: {chunks}")
            else:
                print(f"   ❌ Error - Status: {response.status_code}")
                failed_documents.append(filename)
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            failed_documents.append(filename)
        
        # Pausa entre cargas
        time.sleep(1)
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE CARGA")
    print("=" * 50)
    
    print(f"✅ Documentos cargados exitosamente: {len(loaded_documents)}")
    print(f"❌ Documentos con error: {len(failed_documents)}")
    
    if loaded_documents:
        print("\n📋 DOCUMENTOS CARGADOS:")
        for doc in loaded_documents:
            print(f"   - {doc['filename']} (ID: {doc['document_id']}, Chunks: {doc['chunks']})")
    
    if failed_documents:
        print("\n❌ DOCUMENTOS CON ERROR:")
        for doc in failed_documents:
            print(f"   - {doc}")
    
    # Verificar estadísticas finales
    print("\n📈 Verificando estadísticas finales...")
    try:
        response = requests.get(f"{base_url}/documents/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total de documentos en el sistema: {data.get('total_documents', 0)}")
            print(f"   Total de chunks: {data.get('total_chunks', 0)}")
        else:
            print(f"   ❌ Error obteniendo estadísticas: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Carga de documentos completada")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cargar documentos de prueba en MediCopilot")
    parser.add_argument("--url", default="http://localhost:8000", help="URL base de la API")
    parser.add_argument("--docs-dir", default="test-documents", help="Directorio con documentos de prueba")
    
    args = parser.parse_args()
    
    load_test_documents(args.url, args.docs_dir)

if __name__ == "__main__":
    main()
