# Prompt para ChatGPT - Diagrama de Tecnología MediCopilot

## Prompt Principal

```
Crea un diagrama Mermaid que muestre la arquitectura tecnológica completa del sistema MediCopilot, un asistente médico con RAG (Retrieval-Augmented Generation). Incluye los siguientes componentes y flujos:

**TECNOLOGÍAS PRINCIPALES:**
- Frontend: Next.js con TypeScript
- Backend: FastAPI (Python)
- Base de Datos Vectorial: Weaviate
- LLM: Saptiva OPS (GPT-3.5-turbo)
- Embeddings: SentenceTransformers (all-MiniLM-L6-v2)
- Procesamiento: PyPDF, python-docx
- Contenedores: Docker & Docker Compose

**FLUJO DE DATOS:**
1. Carga de documentos médicos (PDF, DOCX, TXT)
2. Extracción y chunking de texto
3. Generación de embeddings
4. Almacenamiento en Weaviate
5. Consulta del usuario
6. Búsqueda semántica
7. Generación de respuesta con Saptiva OPS
8. Presentación en frontend

**COMPONENTES DEL SISTEMA:**
- Document Processor (ingest.py)
- Vector Store Client (vectorstore.py) 
- LLM Client (llm.py)
- RAG Pipeline (rag.py)
- API Endpoints (documents.py, query.py)

**REQUISITOS DEL DIAGRAMA:**
- Usa colores diferentes para cada tipo de tecnología
- Muestra las conexiones entre componentes
- Incluye puertos (8000 para API, 8080 para Weaviate)
- Destaca el flujo RAG con Saptiva OPS
- Muestra la integración frontend-backend
- Incluye el procesamiento de documentos médicos

Formato: Diagrama Mermaid con nodos, conexiones y colores apropiados.
```

## Prompt Alternativo (Más Específico)

```
Genera un diagrama Mermaid de arquitectura de software que ilustre un sistema de asistente médico llamado MediCopilot. El sistema debe mostrar:

**ARQUITECTURA EN CAPAS:**
- Capa de Presentación: Next.js frontend
- Capa de API: FastAPI backend
- Capa de Procesamiento: Python services
- Capa de Datos: Weaviate vector database
- Capa de IA: Saptiva OPS LLM

**SERVICIOS PRINCIPALES:**
1. Document Upload Service (procesa PDF/DOCX/TXT)
2. Text Extraction & Chunking Service
3. Embedding Generation Service (SentenceTransformers)
4. Vector Search Service (Weaviate)
5. RAG Pipeline Service
6. LLM Integration Service (Saptiva OPS)
7. Query Processing Service

**FLUJO TÉCNICO:**
Documento → Extracción → Chunking → Embeddings → Weaviate → Consulta → Búsqueda Vectorial → Contexto → Saptiva OPS → Respuesta → Frontend

**DETALLES TÉCNICOS:**
- Puerto 8000: FastAPI
- Puerto 8080: Weaviate
- Modelo: all-MiniLM-L6-v2 para embeddings
- LLM: GPT-3.5-turbo via Saptiva OPS
- Contenedores: Docker Compose

Crea un diagrama visualmente atractivo con iconos, colores y etiquetas claras.
```

## Prompt para Diagrama de Secuencia

```
Crea un diagrama de secuencia Mermaid que muestre la interacción paso a paso en MediCopilot:

**ACTORES:**
- Usuario Médico
- Frontend Next.js
- FastAPI Backend
- RAG Pipeline
- Weaviate Vector DB
- Saptiva OPS LLM

**SECUENCIA:**
1. Usuario sube documento médico
2. FastAPI procesa y extrae texto
3. Sistema genera chunks y embeddings
4. Almacena en Weaviate
5. Usuario hace consulta médica
6. RAG Pipeline busca chunks relevantes
7. Construye contexto médico
8. Envía a Saptiva OPS
9. Recibe respuesta médica
10. Presenta resultado al usuario

Incluye manejo de errores y timeouts.
```

## Prompt para Diagrama de Componentes

```
Diseña un diagrama de componentes Mermaid para MediCopilot mostrando:

**COMPONENTES PRINCIPALES:**
- Frontend Component (Next.js)
- API Gateway (FastAPI)
- Document Service (ingest.py)
- Vector Service (vectorstore.py)
- LLM Service (llm.py)
- RAG Service (rag.py)
- Database (Weaviate)

**INTERFACES:**
- REST API endpoints
- Vector search interface
- LLM API interface
- File upload interface

**DEPENDENCIAS:**
- Docker containers
- External APIs (Saptiva OPS)
- File system storage
- Network connections

Muestra las relaciones entre componentes y sus responsabilidades.
```

## Prompt para Diagrama de Despliegue

```
Crea un diagrama de despliegue Mermaid para MediCopilot en Docker:

**CONTENEDORES:**
- mediocopilot-api (FastAPI)
- weaviate (Vector DB)
- nginx (opcional, reverse proxy)

**VOLÚMENES:**
- weaviate_data (persistencia)
- app_data (documentos)

**REDES:**
- Docker network interno
- Exposición de puertos
- Variables de entorno

**CONFIGURACIÓN:**
- docker-compose.yml
- Dockerfile
- .env variables

Muestra la infraestructura completa de despliegue.
```

## Instrucciones de Uso

1. **Copia el prompt principal** y pégalo en ChatGPT
2. **Especifica el tipo de diagrama** que prefieres (arquitectura, secuencia, componentes, despliegue)
3. **Personaliza** según tus necesidades específicas
4. **Solicita modificaciones** si necesitas ajustar el diagrama

## Ejemplo de Uso Completo

```
Hola ChatGPT, necesito que me ayudes a crear un diagrama técnico. 

[PEGA AQUÍ EL PROMPT PRINCIPAL]

Por favor, genera el diagrama en formato Mermaid y también incluye una explicación breve de cada componente y cómo interactúan entre sí.
```

## Notas Adicionales

- Los prompts están optimizados para generar diagramas técnicos precisos
- Incluyen todos los componentes principales del sistema MediCopilot
- Son específicos sobre tecnologías y flujos de datos
- Permiten personalización según necesidades específicas
