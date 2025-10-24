# MediCopilot MVP

Asistente médico de nueva generación entrenado con documentos internos, regulaciones clínicas y un wiki de fármacos. Permite a doctores resolver consultas simples, mapear principios activos a nombres comerciales y acceder a información confiable en tiempo real.

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Weaviate      │    │  Saptiva OPS    │
│   (Backend)     │◄──►│  (Vector DB)    │    │     (LLM)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   Documentos    │
│   (PDF/TXT/DOCX)│
└─────────────────┘
```

## 🚀 Características MVP

- ✅ **Carga de documentos**: PDF, TXT, DOCX
- ✅ **Búsqueda semántica**: Weaviate vector database
- ✅ **Integración LLM**: Saptiva OPS API
- ✅ **API REST**: FastAPI con documentación automática
- ✅ **Docker**: Despliegue local con Docker Compose
- ✅ **RAG Pipeline**: Retrieval-Augmented Generation

## 📋 Prerrequisitos

- Docker
- Docker Compose
- Clave API de Saptiva OPS

## ⚙️ Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd MediCopilot
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
```

Editar `.env` y agregar tu clave API de Saptiva:
```env
SAPTIVA_API_KEY=tu_clave_api_aqui
SAPTIVA_API_URL=https://api.saptiva.com/v1/chat
WEAVIATE_URL=http://weaviate:8080
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 3. Ejecutar la aplicación
```bash
docker-compose up --build
```

La aplicación estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **Weaviate**: http://localhost:8080

## 📖 Uso

### 1. Cargar un documento médico

```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@documento_medico.pdf"
```

Respuesta:
```json
{
  "document_id": "uuid-del-documento",
  "filename": "documento_medico.pdf",
  "chunks_created": 15,
  "message": "Document 'documento_medico.pdf' processed successfully with 15 chunks"
}
```

### 2. Hacer una consulta médica

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuáles son los efectos secundarios del paracetamol?",
    "max_results": 5
  }'
```

Respuesta:
```json
{
  "answer": "Basándome en los documentos disponibles, el paracetamol puede causar...",
  "sources": [
    {
      "filename": "documento_medico.pdf",
      "chunk_index": 3,
      "content_preview": "Efectos secundarios del paracetamol incluyen...",
      "relevance_score": 0.95,
      "document_id": "uuid-del-documento"
    }
  ],
  "query": "¿Cuáles son los efectos secundarios del paracetamol?",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 3. Verificar estado del sistema

```bash
curl http://localhost:8000/health
```

## 🔧 API Endpoints

### Documentos
- `POST /documents/upload` - Cargar documento
- `GET /documents/{document_id}/summary` - Resumen del documento
- `DELETE /documents/{document_id}` - Eliminar documento
- `GET /documents/stats` - Estadísticas de documentos

### Consultas
- `POST /query/` - Hacer consulta médica
- `GET /query/health` - Estado del servicio de consultas

### Sistema
- `GET /` - Información básica
- `GET /health` - Estado general del sistema
- `GET /docs` - Documentación interactiva

## 🐳 Servicios Docker

### Weaviate
- **Puerto**: 8080
- **Función**: Base de datos vectorial
- **Persistencia**: Volumen `weaviate_data`

### API
- **Puerto**: 8000
- **Función**: Backend FastAPI
- **Dependencias**: Weaviate

## 📁 Estructura del Proyecto

```
MediCopilot/
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile                  # Imagen de la API
├── requirements.txt            # Dependencias Python
├── env.example                # Plantilla de configuración
├── README.md                  # Este archivo
├── app/
│   ├── main.py               # Aplicación FastAPI
│   ├── config.py             # Configuración
│   ├── models.py             # Modelos Pydantic
│   ├── services/
│   │   ├── vectorstore.py    # Cliente Weaviate
│   │   ├── llm.py           # Cliente Saptiva OPS
│   │   ├── ingest.py        # Procesamiento de documentos
│   │   └── rag.py           # Pipeline RAG
│   └── routers/
│       ├── documents.py      # Endpoints de documentos
│       └── query.py         # Endpoints de consultas
└── data/                     # Almacenamiento local
```

## 🔍 Flujo RAG

1. **Ingesta**: Documento → Extracción de texto → Chunking → Embeddings
2. **Almacenamiento**: Chunks + embeddings → Weaviate
3. **Consulta**: Pregunta → Embedding → Búsqueda semántica
4. **Generación**: Contexto + Pregunta → Saptiva OPS → Respuesta

## 🚧 Próximas Características

### Fase 2: Procesamiento Avanzado
- [ ] Google Document AI para parsing avanzado
- [ ] Unstructured para múltiples formatos
- [ ] scispaCy/medspaCy para NER clínica

### Fase 3: Bases de Datos Médicas
- [ ] DrugBank/PLM (México)
- [ ] COFEPRIS (registros)
- [ ] ATC/WHO
- [ ] RxNorm/SNOMED CT

### Fase 4: Seguridad y Privacidad
- [ ] Presidio para enmascaramiento PHI/PII
- [ ] Guardrails AI/LlamaGuard
- [ ] Autenticación JWT
- [ ] Open Policy Agent

### Fase 5: Observabilidad
- [ ] Langfuse para monitoreo
- [ ] Great Expectations para validación
- [ ] PostgreSQL/Redis para persistencia
- [ ] LangChain/LangGraph para orquestación

## 🐛 Solución de Problemas

### Error de conexión a Weaviate
```bash
# Verificar que Weaviate esté ejecutándose
docker-compose ps
docker-compose logs weaviate
```

### Error de API de Saptiva
```bash
# Verificar la clave API en .env
cat .env | grep SAPTIVA_API_KEY
```

### Problemas de memoria
```bash
# Aumentar memoria para Docker
docker-compose down
docker system prune -a
docker-compose up --build
```

## 📝 Logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api
docker-compose logs -f weaviate
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo

---

**MediCopilot MVP** - Asistente médico inteligente con RAG

