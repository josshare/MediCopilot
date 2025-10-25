#!/usr/bin/env python3
"""
Script para probar consultas sobre diabetes en MediCopilot
Incluye 20 ejemplos específicos de consultas médicas sobre diabetes
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Configuración de la API
API_BASE_URL = "http://localhost:8000"
QUERY_ENDPOINT = f"{API_BASE_URL}/query/"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

class DiabetesQueryTester:
    def __init__(self):
        self.results = []
        self.session = requests.Session()
        
    def check_api_health(self) -> bool:
        """Verifica que la API esté funcionando"""
        try:
            response = self.session.get(HEALTH_ENDPOINT, timeout=10)
            if response.status_code == 200:
                print("✅ API está funcionando correctamente")
                return True
            else:
                print(f"❌ API no responde correctamente: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando con la API: {e}")
            return False
    
    def send_query(self, question: str, max_results: int = 5) -> Dict[str, Any]:
        """Envía una consulta a la API"""
        payload = {
            "question": question,
            "max_results": max_results
        }
        
        try:
            response = self.session.post(
                QUERY_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Error {response.status_code}: {response.text}",
                    "question": question
                }
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Error de conexión: {e}",
                "question": question
            }
    
    def run_diabetes_tests(self):
        """Ejecuta todas las pruebas de diabetes"""
        print("🩺 Iniciando pruebas de consultas sobre diabetes...")
        print("=" * 60)
        
        # Verificar que la API esté funcionando
        if not self.check_api_health():
            print("❌ No se puede continuar sin conexión a la API")
            return
        
        # Cargar ejemplos de diabetes
        diabetes_queries = self.load_diabetes_queries()
        
        for i, query_data in enumerate(diabetes_queries, 1):
            print(f"\n🔍 Prueba {i}/20: {query_data['category']}")
            print(f"Pregunta: {query_data['question']}")
            print("-" * 40)
            
            start_time = time.time()
            result = self.send_query(query_data['question'], query_data.get('max_results', 5))
            end_time = time.time()
            
            # Agregar metadatos
            result['test_number'] = i
            result['category'] = query_data['category']
            result['response_time'] = round(end_time - start_time, 2)
            result['timestamp'] = datetime.now().isoformat()
            
            self.results.append(result)
            
            # Mostrar resultado
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Respuesta obtenida en {result['response_time']}s")
                print(f"📄 Fuentes encontradas: {len(result.get('sources', []))}")
                if result.get('sources'):
                    print(f"📊 Relevancia promedio: {self.calculate_avg_relevance(result['sources']):.2f}")
            
            # Pausa entre consultas para no sobrecargar la API
            time.sleep(1)
        
        # Guardar resultados
        self.save_results()
        self.print_summary()
    
    def load_diabetes_queries(self) -> List[Dict[str, Any]]:
        """Carga las consultas de diabetes desde el archivo JSON"""
        try:
            with open('/Volumes/Nueva/code/sapiva/MediCopilot/examples/test-data/diabetes_queries.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data['diabetes_queries']
        except FileNotFoundError:
            print("❌ Archivo diabetes_queries.json no encontrado")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error leyendo JSON: {e}")
            return []
    
    def calculate_avg_relevance(self, sources: List[Dict]) -> float:
        """Calcula la relevancia promedio de las fuentes"""
        if not sources:
            return 0.0
        relevance_scores = [source.get('relevance_score', 0) for source in sources]
        return sum(relevance_scores) / len(relevance_scores)
    
    def save_results(self):
        """Guarda los resultados en un archivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/Volumes/Nueva/code/sapiva/MediCopilot/examples/scripts/diabetes_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'test_info': {
                    'total_queries': len(self.results),
                    'timestamp': datetime.now().isoformat(),
                    'api_url': API_BASE_URL
                },
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {filename}")
    
    def print_summary(self):
        """Imprime un resumen de los resultados"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE PRUEBAS DE DIABETES")
        print("=" * 60)
        
        total_queries = len(self.results)
        successful_queries = len([r for r in self.results if 'error' not in r])
        failed_queries = total_queries - successful_queries
        
        print(f"Total de consultas: {total_queries}")
        print(f"✅ Exitosas: {successful_queries}")
        print(f"❌ Fallidas: {failed_queries}")
        print(f"📈 Tasa de éxito: {(successful_queries/total_queries)*100:.1f}%")
        
        if successful_queries > 0:
            avg_response_time = sum(r.get('response_time', 0) for r in self.results if 'error' not in r) / successful_queries
            print(f"⏱️  Tiempo promedio de respuesta: {avg_response_time:.2f}s")
            
            # Estadísticas por categoría
            categories = {}
            for result in self.results:
                if 'error' not in result:
                    cat = result.get('category', 'unknown')
                    if cat not in categories:
                        categories[cat] = {'success': 0, 'total': 0}
                    categories[cat]['success'] += 1
                categories[result.get('category', 'unknown')]['total'] = categories.get(result.get('category', 'unknown'), {'success': 0, 'total': 0})['total'] + 1
            
            print("\n📋 Resultados por categoría:")
            for cat, stats in categories.items():
                success_rate = (stats['success'] / stats['total']) * 100 if stats['total'] > 0 else 0
                print(f"  {cat}: {stats['success']}/{stats['total']} ({success_rate:.1f}%)")

def main():
    """Función principal"""
    print("🩺 MediCopilot - Probador de Consultas sobre Diabetes")
    print("=" * 60)
    
    tester = DiabetesQueryTester()
    tester.run_diabetes_tests()

if __name__ == "__main__":
    main()
