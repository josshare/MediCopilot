# Guía de Solución de Problemas - MediCopilot

## 🚨 Problemas Comunes y Soluciones

### 1. Problemas de Inicio

#### Error: "Docker no está ejecutándose"
**Síntomas:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solución:**
```bash
# Iniciar Docker Desktop (macOS/Windows)
# O iniciar el servicio Docker (Linux)
sudo systemctl start docker

# Verificar que Docker esté ejecutándose
docker --version
docker-compose --version
```

#### Error: "Puerto ya está en uso"
**Síntomas:**
```
Port 8000 is already in use
Port 8080 is already in use
```

**Solución:**
```bash
# Verificar qué proceso está usando el puerto
lsof -i :8000
lsof -i :8080

# Terminar el proceso (reemplaza PID con el número del proceso)
kill -9 PID

# O cambiar los puertos en docker-compose.yml
```

#### Error: "No se puede conectar a Weaviate"
**Síntomas:**
```
ConnectionError: Unable to connect to Weaviate
```

**Solución:**
```bash
# Verificar que Weaviate esté ejecutándose
docker-compose ps

# Reiniciar Weaviate
docker-compose restart weaviate

# Ver logs de Weaviate
docker-compose logs weaviate
```

### 2. Problemas de Configuración

#### Error: "SAPTIVA_API_KEY no encontrada"
**Síntomas:**
```
Environment variable SAPTIVA_API_KEY not set
```

**Solución:**
```bash
# Verificar que el archivo .env existe
ls -la .env

# Si no existe, copiarlo desde el ejemplo
cp env.example .env

# Editar el archivo .env y agregar tu clave API
nano .env

# Verificar que la variable esté configurada
grep SAPTIVA_API_KEY .env
```

#### Error: "URL de API inválida"
**Síntomas:**
```
Invalid API URL: None
```

**Solución:**
```bash
# Verificar configuración en .env
cat .env | grep SAPTIVA_API_URL

# Asegurarse de que la URL esté correcta
SAPTIVA_API_URL=https://api.saptiva.com/v1/chat
```

### 3. Problemas de Documentos

#### Error: "Documento no se puede procesar"
**Síntomas:**
```
Failed to process document: Unsupported file type
```

**Solución:**
- Verificar que el archivo esté en formato soportado (PDF, TXT, DOCX)
- Verificar que el archivo no esté corrupto
- Verificar que el archivo no esté vacío
- Verificar permisos de lectura del archivo

#### Error: "No se pueden extraer chunks"
**Síntomas:**
```
No chunks could be extracted from document
```

**Solución:**
```bash
# Verificar logs de procesamiento
docker-compose logs api | grep -i chunk

# Verificar que el documento tenga contenido de texto
# Algunos PDFs pueden tener solo imágenes
```

#### Error: "Documento muy grande"
**Síntomas:**
```
Document too large to process
```

**Solución:**
- Dividir el documento en partes más pequeñas
- Comprimir el documento
- Aumentar límites de memoria en Docker

### 4. Problemas de Consultas

#### Error: "No se encontraron fuentes relevantes"
**Síntomas:**
```
No relevant sources found for query
```

**Solución:**
- Verificar que hay documentos cargados: `curl http://localhost:8000/documents/stats`
- Reformular la pregunta con términos más específicos
- Cargar más documentos relacionados con el tema
- Verificar que los documentos contengan información relevante

#### Error: "Timeout en consulta"
**Síntomas:**
```
Request timeout after 30 seconds
```

**Solución:**
```bash
# Aumentar timeout en la configuración
# O simplificar la consulta
# Verificar conectividad con Saptiva OPS
```

#### Error: "Respuesta vacía del LLM"
**Síntomas:**
```
Empty response from LLM service
```

**Solución:**
- Verificar que la clave API de Saptiva sea válida
- Verificar conectividad a internet
- Verificar que el servicio de Saptiva esté disponible
- Reintentar la consulta

### 5. Problemas de Rendimiento

#### Error: "Memoria insuficiente"
**Síntomas:**
```
Out of memory error
```

**Solución:**
```bash
# Aumentar memoria para Docker
# En Docker Desktop: Settings > Resources > Memory

# Limpiar contenedores y volúmenes
docker system prune -a
docker volume prune

# Reiniciar servicios
docker-compose down
docker-compose up --build
```

#### Error: "Respuesta lenta"
**Síntomas:**
- Consultas que tardan más de 30 segundos
- Timeouts frecuentes

**Solución:**
```bash
# Verificar recursos del sistema
docker stats

# Optimizar consultas (usar menos max_results)
# Cargar menos documentos simultáneamente
# Verificar conectividad de red
```

### 6. Problemas de Base de Datos

#### Error: "Weaviate no responde"
**Síntomas:**
```
Weaviate connection timeout
```

**Solución:**
```bash
# Reiniciar Weaviate
docker-compose restart weaviate

# Verificar logs
docker-compose logs weaviate

# Verificar que el puerto 8080 esté libre
lsof -i :8080
```

#### Error: "Esquema no encontrado"
**Síntomas:**
```
Schema not found in Weaviate
```

**Solución:**
```bash
# Reinicializar Weaviate
docker-compose down
docker volume rm medicopilot_weaviate_data
docker-compose up --build
```

### 7. Problemas de Red

#### Error: "No se puede conectar a Saptiva OPS"
**Síntomas:**
```
ConnectionError: Unable to connect to Saptiva OPS
```

**Solución:**
```bash
# Verificar conectividad
curl -I https://api.saptiva.com/v1/chat

# Verificar configuración de proxy (si aplica)
# Verificar firewall
# Verificar DNS
```

#### Error: "SSL/TLS error"
**Síntomas:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solución:**
```bash
# Actualizar certificados
# Verificar fecha del sistema
# Configurar certificados personalizados si es necesario
```

## 🔍 Diagnóstico Avanzado

### Verificar Estado del Sistema

```bash
# Estado de todos los servicios
docker-compose ps

# Uso de recursos
docker stats

# Logs de todos los servicios
docker-compose logs --tail=100

# Logs de un servicio específico
docker-compose logs --tail=100 api
docker-compose logs --tail=100 weaviate
```

### Verificar Conectividad

```bash
# Verificar API local
curl -v http://localhost:8000/health

# Verificar Weaviate
curl -v http://localhost:8080/v1/meta

# Verificar Saptiva OPS (con tu clave API)
curl -v -H "Authorization: Bearer TU_CLAVE_API" https://api.saptiva.com/v1/chat
```

### Verificar Configuración

```bash
# Verificar variables de entorno
docker-compose config

# Verificar archivo .env
cat .env

# Verificar configuración de la aplicación
curl http://localhost:8000/health | jq
```

## 🛠️ Herramientas de Diagnóstico

### Script de Diagnóstico

```bash
#!/bin/bash
# diagnostic.sh

echo "🔍 Diagnóstico de MediCopilot"
echo "=============================="

echo "1. Verificando Docker..."
docker --version
docker-compose --version

echo "2. Verificando servicios..."
docker-compose ps

echo "3. Verificando puertos..."
lsof -i :8000
lsof -i :8080

echo "4. Verificando API..."
curl -s http://localhost:8000/health | jq

echo "5. Verificando Weaviate..."
curl -s http://localhost:8080/v1/meta | jq

echo "6. Verificando configuración..."
cat .env | grep -v "SAPTIVA_API_KEY"

echo "7. Verificando logs recientes..."
docker-compose logs --tail=10 api
```

### Monitoreo en Tiempo Real

```bash
# Monitorear logs en tiempo real
docker-compose logs -f

# Monitorear recursos
watch docker stats

# Monitorear puertos
watch lsof -i :8000,8080
```

## 📊 Logs y Debugging

### Niveles de Log

```python
# En app/config.py
import logging

# Configurar nivel de log
logging.basicConfig(level=logging.DEBUG)

# Para desarrollo
LOGGING_LEVEL = "DEBUG"

# Para producción
LOGGING_LEVEL = "INFO"
```

### Logs Estructurados

```python
import structlog

logger = structlog.get_logger()

# En lugar de print()
logger.info("Processing document", document_id=doc_id, filename=filename)

# Para errores
logger.error("Failed to process document", 
            document_id=doc_id, 
            error=str(e), 
            exc_info=True)
```

### Análisis de Logs

```bash
# Buscar errores
docker-compose logs api | grep -i error

# Buscar warnings
docker-compose logs api | grep -i warning

# Buscar por timestamp
docker-compose logs api --since="2024-01-01T10:00:00"

# Exportar logs
docker-compose logs api > api_logs.txt
```

## 🚀 Optimización

### Optimización de Docker

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

### Optimización de Weaviate

```yaml
# docker-compose.yml
services:
  weaviate:
    environment:
      - QUERY_DEFAULTS_LIMIT=25
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      - PERSISTENCE_DATA_PATH=/var/lib/weaviate
      - DEFAULT_VECTORIZER_MODULE=none
      - ENABLE_MODULES=text2vec-transformers
      - TRANSFORMERS_INFERENCE_API=http://t2v-transformers:8080
```

### Optimización de Consultas

```python
# Limitar resultados para mejorar rendimiento
query_request = QueryRequest(
    question=question,
    max_results=3  # En lugar de 10
)

# Usar filtros específicos
filters = {
    "where": {
        "path": ["filename"],
        "operator": "Equal",
        "valueString": "documento_especifico.pdf"
    }
}
```

## 📞 Soporte Técnico

### Información para Reportar Problemas

Cuando reportes un problema, incluye:

1. **Versión del sistema:**
   ```bash
   docker --version
   docker-compose --version
   python --version
   ```

2. **Configuración:**
   ```bash
   cat .env | grep -v "SAPTIVA_API_KEY"
   ```

3. **Logs relevantes:**
   ```bash
   docker-compose logs --tail=50 api
   ```

4. **Pasos para reproducir:**
   - Comando exacto que ejecutaste
   - Resultado esperado vs resultado actual
   - Screenshots si aplica

5. **Información del sistema:**
   ```bash
   uname -a
   df -h
   free -h
   ```

### Canales de Soporte

- **GitHub Issues**: Para bugs y feature requests
- **Documentación**: Revisar esta guía primero
- **Logs**: Siempre incluir logs relevantes
- **Reproducción**: Proporcionar pasos para reproducir

---

**¡Esperamos que esta guía te ayude a resolver cualquier problema!** 🚀
