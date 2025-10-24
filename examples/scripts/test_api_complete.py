#!/usr/bin/env python3
"""
Script completo de testing para MediCopilot API
Incluye tests de todos los endpoints y funcionalidades
"""

import requests
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Any

class MediCopilotTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.uploaded_documents = []
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """Registra el resultado de un test"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
    def test_health_check(self) -> bool:
        """Test del endpoint de salud"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_document_upload(self, document_path: str) -> str:
        """Test de carga de documento"""
        try:
            if not os.path.exists(document_path):
                self.log_test("Document Upload", False, f"File not found: {document_path}")
                return None
                
            with open(document_path, 'rb') as f:
                files = {'file': (os.path.basename(document_path), f, 'text/plain')}
                response = self.session.post(f"{self.base_url}/documents/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                document_id = data.get('document_id')
                self.uploaded_documents.append(document_id)
                self.log_test("Document Upload", True, 
                            f"Uploaded {data.get('filename')} with {data.get('chunks_created')} chunks")
                return document_id
            else:
                self.log_test("Document Upload", False, f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_test("Document Upload", False, f"Error: {str(e)}")
            return None
    
    def test_document_summary(self, document_id: str) -> bool:
        """Test de resumen de documento"""
        try:
            response = self.session.get(f"{self.base_url}/documents/{document_id}/summary")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Document Summary", True, f"Summary length: {len(data.get('summary', ''))}")
                return True
            else:
                self.log_test("Document Summary", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Document Summary", False, f"Error: {str(e)}")
            return False
    
    def test_query(self, question: str, max_results: int = 5) -> bool:
        """Test de consulta médica"""
        try:
            payload = {
                "question": question,
                "max_results": max_results
            }
            response = self.session.post(f"{self.base_url}/query/", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                answer_length = len(data.get('answer', ''))
                sources_count = len(data.get('sources', []))
                self.log_test("Medical Query", True, 
                            f"Answer length: {answer_length}, Sources: {sources_count}")
                return True
            else:
                self.log_test("Medical Query", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Medical Query", False, f"Error: {str(e)}")
            return False
    
    def test_document_stats(self) -> bool:
        """Test de estadísticas de documentos"""
        try:
            response = self.session.get(f"{self.base_url}/documents/stats")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Document Stats", True, f"Total documents: {data.get('total_documents')}")
                return True
            else:
                self.log_test("Document Stats", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Document Stats", False, f"Error: {str(e)}")
            return False
    
    def test_query_health(self) -> bool:
        """Test de salud del servicio de consultas"""
        try:
            response = self.session.get(f"{self.base_url}/query/health")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Query Health", True, f"Status: {data.get('status')}")
                return True
            else:
                self.log_test("Query Health", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Query Health", False, f"Error: {str(e)}")
            return False
    
    def test_document_deletion(self, document_id: str) -> bool:
        """Test de eliminación de documento"""
        try:
            response = self.session.delete(f"{self.base_url}/documents/{document_id}")
            if response.status_code == 200:
                self.log_test("Document Deletion", True, f"Document {document_id} deleted")
                return True
            else:
                self.log_test("Document Deletion", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Document Deletion", False, f"Error: {str(e)}")
            return False
    
    def run_comprehensive_test(self, test_documents_dir: str = "test-documents"):
        """Ejecuta una suite completa de tests"""
        print("🚀 Iniciando tests completos de MediCopilot API")
        print("=" * 50)
        
        # Test 1: Health check
        if not self.test_health_check():
            print("❌ Health check falló. Verifica que la API esté ejecutándose.")
            return
        
        # Test 2: Query health
        self.test_query_health()
        
        # Test 3: Document stats (inicial)
        self.test_document_stats()
        
        # Test 4: Cargar documentos de prueba
        test_docs = [
            "paracetamol_efectos_secundarios.txt",
            "ibuprofeno_guia_clinica.txt",
            "protocolo_hipertension.txt",
            "diabetes_tipo2_manejo.txt",
            "antibioticos_uso_racional.txt"
        ]
        
        document_ids = []
        for doc in test_docs:
            doc_path = os.path.join(test_documents_dir, doc)
            if os.path.exists(doc_path):
                doc_id = self.test_document_upload(doc_path)
                if doc_id:
                    document_ids.append(doc_id)
                    time.sleep(1)  # Pausa entre cargas
        
        # Test 5: Resúmenes de documentos
        for doc_id in document_ids[:2]:  # Solo los primeros 2
            self.test_document_summary(doc_id)
            time.sleep(1)
        
        # Test 6: Consultas médicas
        test_questions = [
            "¿Cuáles son los efectos secundarios del paracetamol?",
            "¿Cómo se debe dosificar el ibuprofeno?",
            "¿Cuáles son los objetivos de control en hipertensión?",
            "¿Qué complicaciones puede tener la diabetes tipo 2?",
            "¿Cuándo se debe usar un antibiótico?"
        ]
        
        for question in test_questions:
            self.test_query(question)
            time.sleep(2)  # Pausa entre consultas
        
        # Test 7: Document stats (después de cargas)
        self.test_document_stats()
        
        # Test 8: Eliminar algunos documentos
        for doc_id in document_ids[:2]:
            self.test_document_deletion(doc_id)
            time.sleep(1)
        
        # Test 9: Document stats (después de eliminaciones)
        self.test_document_stats()
        
        # Resumen final
        self.print_summary()
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE TESTS")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de tests: {total_tests}")
        print(f"✅ Exitosos: {passed_tests}")
        print(f"❌ Fallidos: {failed_tests}")
        print(f"📈 Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ TESTS FALLIDOS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        
        print("\n📋 DOCUMENTOS CARGADOS:")
        for doc_id in self.uploaded_documents:
            print(f"  - {doc_id}")
    
    def save_results(self, filename: str = "test_results.json"):
        """Guarda los resultados en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados guardados en: {filename}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test completo de MediCopilot API")
    parser.add_argument("--url", default="http://localhost:8000", help="URL base de la API")
    parser.add_argument("--docs-dir", default="test-documents", help="Directorio con documentos de prueba")
    parser.add_argument("--save-results", action="store_true", help="Guardar resultados en archivo")
    
    args = parser.parse_args()
    
    # Verificar que el directorio de documentos existe
    if not os.path.exists(args.docs_dir):
        print(f"❌ Directorio de documentos no encontrado: {args.docs_dir}")
        print("💡 Asegúrate de ejecutar el script desde el directorio examples/")
        return
    
    # Crear tester y ejecutar tests
    tester = MediCopilotTester(args.url)
    tester.run_comprehensive_test(args.docs_dir)
    
    if args.save_results:
        tester.save_results()

if __name__ == "__main__":
    main()
