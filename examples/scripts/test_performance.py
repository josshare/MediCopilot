#!/usr/bin/env python3
"""
Script de testing de rendimiento para MediCopilot API
Mide tiempos de respuesta y rendimiento del sistema
"""

import requests
import time
import json
import statistics
from typing import List, Dict, Any
import concurrent.futures
import threading

class PerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def test_single_query(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Ejecuta una consulta individual y mide el rendimiento"""
        start_time = time.time()
        
        try:
            payload = {
                "question": query,
                "max_results": max_results
            }
            
            response = self.session.post(f"{self.base_url}/query/", json=payload)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            result = {
                "query": query,
                "response_time": response_time,
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if response.status_code == 200:
                data = response.json()
                result.update({
                    "answer_length": len(data.get('answer', '')),
                    "sources_count": len(data.get('sources', [])),
                    "max_results": max_results
                })
            else:
                result["error"] = response.text
                
        except Exception as e:
            end_time = time.time()
            result = {
                "query": query,
                "response_time": end_time - start_time,
                "status_code": 0,
                "success": False,
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        
        return result
    
    def test_concurrent_queries(self, queries: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:
        """Ejecuta múltiples consultas concurrentemente"""
        print(f"🚀 Ejecutando {len(queries)} consultas concurrentes con {max_workers} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.test_single_query, query) for query in queries]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        return results
    
    def test_sequential_queries(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Ejecuta consultas secuencialmente"""
        print(f"🔄 Ejecutando {len(queries)} consultas secuenciales...")
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"   {i}/{len(queries)}: {query[:50]}...")
            result = self.test_single_query(query)
            results.append(result)
            time.sleep(0.5)  # Pausa entre consultas
        
        return results
    
    def test_load_scenario(self, base_queries: List[str], iterations: int = 3) -> Dict[str, Any]:
        """Simula carga del sistema con múltiples iteraciones"""
        print(f"📊 Ejecutando escenario de carga con {iterations} iteraciones...")
        
        all_results = []
        
        for iteration in range(iterations):
            print(f"\n🔄 Iteración {iteration + 1}/{iterations}")
            
            # Mezclar las consultas para simular uso real
            import random
            shuffled_queries = base_queries.copy()
            random.shuffle(shuffled_queries)
            
            # Ejecutar consultas concurrentemente
            iteration_results = self.test_concurrent_queries(shuffled_queries, max_workers=3)
            all_results.extend(iteration_results)
            
            # Pausa entre iteraciones
            time.sleep(2)
        
        return self.analyze_results(all_results)
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analiza los resultados de las pruebas"""
        if not results:
            return {"error": "No hay resultados para analizar"}
        
        successful_results = [r for r in results if r.get('success', False)]
        failed_results = [r for r in results if not r.get('success', False)]
        
        if not successful_results:
            return {
                "total_queries": len(results),
                "successful_queries": 0,
                "failed_queries": len(failed_results),
                "success_rate": 0.0,
                "error": "No se completó ninguna consulta exitosamente"
            }
        
        response_times = [r['response_time'] for r in successful_results]
        answer_lengths = [r.get('answer_length', 0) for r in successful_results if 'answer_length' in r]
        sources_counts = [r.get('sources_count', 0) for r in successful_results if 'sources_count' in r]
        
        analysis = {
            "total_queries": len(results),
            "successful_queries": len(successful_results),
            "failed_queries": len(failed_results),
            "success_rate": len(successful_results) / len(results) * 100,
            "response_times": {
                "min": min(response_times),
                "max": max(response_times),
                "mean": statistics.mean(response_times),
                "median": statistics.median(response_times),
                "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0
            },
            "answer_lengths": {
                "min": min(answer_lengths) if answer_lengths else 0,
                "max": max(answer_lengths) if answer_lengths else 0,
                "mean": statistics.mean(answer_lengths) if answer_lengths else 0,
                "median": statistics.median(answer_lengths) if answer_lengths else 0
            },
            "sources_counts": {
                "min": min(sources_counts) if sources_counts else 0,
                "max": max(sources_counts) if sources_counts else 0,
                "mean": statistics.mean(sources_counts) if sources_counts else 0,
                "median": statistics.median(sources_counts) if sources_counts else 0
            }
        }
        
        if failed_results:
            analysis["errors"] = [r.get('error', 'Unknown error') for r in failed_results]
        
        return analysis
    
    def print_analysis(self, analysis: Dict[str, Any]):
        """Imprime el análisis de resultados de forma legible"""
        print("\n" + "=" * 60)
        print("📊 ANÁLISIS DE RENDIMIENTO")
        print("=" * 60)
        
        print(f"Total de consultas: {analysis['total_queries']}")
        print(f"Consultas exitosas: {analysis['successful_queries']}")
        print(f"Consultas fallidas: {analysis['failed_queries']}")
        print(f"Tasa de éxito: {analysis['success_rate']:.1f}%")
        
        if 'response_times' in analysis:
            rt = analysis['response_times']
            print(f"\n⏱️  TIEMPOS DE RESPUESTA (segundos):")
            print(f"   Mínimo: {rt['min']:.2f}s")
            print(f"   Máximo: {rt['max']:.2f}s")
            print(f"   Promedio: {rt['mean']:.2f}s")
            print(f"   Mediana: {rt['median']:.2f}s")
            print(f"   Desviación estándar: {rt['std_dev']:.2f}s")
        
        if 'answer_lengths' in analysis:
            al = analysis['answer_lengths']
            print(f"\n📝 LONGITUD DE RESPUESTAS (caracteres):")
            print(f"   Mínimo: {al['min']}")
            print(f"   Máximo: {al['max']}")
            print(f"   Promedio: {al['mean']:.1f}")
            print(f"   Mediana: {al['median']:.1f}")
        
        if 'sources_counts' in analysis:
            sc = analysis['sources_counts']
            print(f"\n📚 NÚMERO DE FUENTES:")
            print(f"   Mínimo: {sc['min']}")
            print(f"   Máximo: {sc['max']}")
            print(f"   Promedio: {sc['mean']:.1f}")
            print(f"   Mediana: {sc['median']:.1f}")
        
        if 'errors' in analysis:
            print(f"\n❌ ERRORES ENCONTRADOS:")
            for error in set(analysis['errors']):
                count = analysis['errors'].count(error)
                print(f"   - {error} ({count} veces)")
    
    def run_performance_suite(self):
        """Ejecuta una suite completa de pruebas de rendimiento"""
        print("🚀 Iniciando suite de pruebas de rendimiento")
        print("=" * 60)
        
        # Cargar consultas de prueba
        try:
            with open('test-data/sample_queries.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Obtener consultas de prueba
            test_queries = []
            for category in data['medical_queries']:
                test_queries.extend(category['queries'][:3])  # Tomar 3 de cada categoría
            
            performance_queries = [scenario['query'] for scenario in data['performance_tests']]
            
        except FileNotFoundError:
            print("⚠️  Archivo sample_queries.json no encontrado, usando consultas por defecto")
            test_queries = [
                "¿Cuáles son los efectos secundarios del paracetamol?",
                "¿Cómo se debe dosificar el ibuprofeno?",
                "¿Cuáles son los síntomas de la diabetes tipo 2?",
                "¿Cuál es el protocolo de manejo de hipertensión?",
                "¿Cuándo se debe usar un antibiótico?"
            ]
            performance_queries = test_queries
        
        # Test 1: Consultas secuenciales
        print("\n1️⃣  PRUEBA SECUENCIAL")
        print("-" * 30)
        sequential_results = self.test_sequential_queries(test_queries[:5])
        sequential_analysis = self.analyze_results(sequential_results)
        self.print_analysis(sequential_analysis)
        
        # Test 2: Consultas concurrentes
        print("\n2️⃣  PRUEBA CONCURRENTE")
        print("-" * 30)
        concurrent_results = self.test_concurrent_queries(test_queries[:5], max_workers=3)
        concurrent_analysis = self.analyze_results(concurrent_results)
        self.print_analysis(concurrent_analysis)
        
        # Test 3: Escenario de carga
        print("\n3️⃣  ESCENARIO DE CARGA")
        print("-" * 30)
        load_analysis = self.test_load_scenario(performance_queries, iterations=2)
        self.print_analysis(load_analysis)
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        all_results = sequential_results + concurrent_results
        final_analysis = self.analyze_results(all_results)
        
        print(f"✅ Rendimiento general: {final_analysis['success_rate']:.1f}% de éxito")
        
        if 'response_times' in final_analysis:
            avg_time = final_analysis['response_times']['mean']
            if avg_time < 5:
                print("🚀 Excelente rendimiento (< 5s promedio)")
            elif avg_time < 10:
                print("✅ Buen rendimiento (< 10s promedio)")
            elif avg_time < 20:
                print("⚠️  Rendimiento aceptable (< 20s promedio)")
            else:
                print("❌ Rendimiento lento (> 20s promedio)")
        
        # Guardar resultados
        self.save_results(final_analysis, "performance_results.json")
    
    def save_results(self, analysis: Dict[str, Any], filename: str):
        """Guarda los resultados en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados guardados en: {filename}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pruebas de rendimiento de MediCopilot API")
    parser.add_argument("--url", default="http://localhost:8000", help="URL base de la API")
    parser.add_argument("--save-results", action="store_true", help="Guardar resultados en archivo")
    
    args = parser.parse_args()
    
    tester = PerformanceTester(args.url)
    tester.run_performance_suite()

if __name__ == "__main__":
    main()
