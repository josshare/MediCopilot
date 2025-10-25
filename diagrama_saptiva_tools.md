# Diagrama: Uso de Herramientas Saptiva en MediCopilot

## Arquitectura del Sistema con Saptiva OPS

```mermaid
graph TB
    %% Usuario y Frontend
    User[👨‍⚕️ Usuario Médico] --> Frontend[🖥️ Frontend Next.js]
    
    %% API Layer
    Frontend --> API[🚀 FastAPI Backend]
    
    %% Document Processing
    API --> DocUpload[📄 Document Upload]
    DocUpload --> DocProcessor[🔧 Document Processor]
    DocProcessor --> TextExtract[📝 Text Extraction]
    TextExtract --> Chunking[✂️ Text Chunking]
    Chunking --> Embeddings[🧠 Generate Embeddings]
    
    %% Vector Storage
    Embeddings --> Weaviate[🗄️ Weaviate Vector DB]
    
    %% Query Processing
    API --> QueryEndpoint[❓ Query Endpoint]
    QueryEndpoint --> RAGPipeline[🔄 RAG Pipeline]
    RAGPipeline --> VectorSearch[🔍 Vector Search]
    VectorSearch --> Weaviate
    
    %% Saptiva Integration
    RAGPipeline --> SaptivaLLM[🤖 Saptiva OPS LLM]
    SaptivaLLM --> SaptivaAPI[🌐 Saptiva API]
    
    %% Response Generation
    SaptivaAPI --> Response[💬 Medical Response]
    Response --> API
    API --> Frontend
    Frontend --> User
    
    %% Styling
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef frontendClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef apiClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef saptivaClass fill:#fff3e0,stroke:#e65100,stroke-width:3px
    classDef dataClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    
    class User userClass
    class Frontend frontendClass
    class API,DocUpload,QueryEndpoint,RAGPipeline apiClass
    class SaptivaLLM,SaptivaAPI saptivaClass
    class Weaviate,DocProcessor,TextExtract,Chunking,Embeddings,VectorSearch dataClass
```

## Flujo Detallado de Saptiva OPS

```mermaid
sequenceDiagram
    participant U as Usuario
    participant F as Frontend
    participant A as FastAPI
    participant R as RAG Pipeline
    participant V as Weaviate
    participant S as Saptiva OPS
    
    U->>F: Pregunta médica
    F->>A: POST /query/
    A->>R: Procesar consulta
    
    R->>R: Generar embedding de la pregunta
    R->>V: Búsqueda semántica
    V-->>R: Chunks relevantes
    
    R->>R: Construir contexto médico
    R->>S: Enviar prompt + contexto
    
    Note over S: Saptiva OPS procesa<br/>con GPT-3.5-turbo
    
    S-->>R: Respuesta médica generada
    R->>R: Preparar fuentes y metadatos
    R-->>A: Respuesta completa
    A-->>F: JSON con respuesta
    F-->>U: Mostrar respuesta médica
```

## Componentes de Saptiva en el Código

### 1. Cliente LLM (llm.py)
```python
class SaptivaLLMClient:
    - API Key: settings.SAPTIVA_API_KEY
    - Endpoint: settings.SAPTIVA_API_URL
    - Modelo: gpt-3.5-turbo
    - Funciones:
      * generate_response()
      * test_connection()
      * _build_prompt()
```

### 2. Integración en RAG (rag.py)
```python
class RAGPipeline:
    - Usa SaptivaLLMClient para generar respuestas
    - Construye contexto médico con chunks relevantes
    - Procesa respuestas y fuentes
```

### 3. Configuración (config.py)
```python
SAPTIVA_API_KEY = "tu_clave_api_aqui"
SAPTIVA_API_URL = "https://api.saptiva.com/v1/chat"
```

## Flujo de Datos con Saptiva

```mermaid
flowchart LR
    subgraph "Documentos Médicos"
        D1[📄 PDF]
        D2[📄 DOCX]
        D3[📄 TXT]
    end
    
    subgraph "Procesamiento"
        P1[Extracción de Texto]
        P2[Chunking]
        P3[Embeddings]
    end
    
    subgraph "Almacenamiento"
        W[Weaviate Vector DB]
    end
    
    subgraph "Consulta"
        Q[Pregunta del Usuario]
        VS[Búsqueda Vectorial]
        C[Contexto Médico]
    end
    
    subgraph "Saptiva OPS"
        S1[API Key]
        S2[Modelo GPT-3.5-turbo]
        S3[Prompt Médico]
        S4[Respuesta Generada]
    end
    
    D1 --> P1
    D2 --> P1
    D3 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> W
    
    Q --> VS
    VS --> W
    W --> C
    C --> S3
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> Q
```

## Características de Saptiva en MediCopilot

### ✅ Implementado
- **Integración API**: Cliente HTTP para Saptiva OPS
- **Modelo GPT-3.5-turbo**: Configurado para respuestas médicas
- **Prompt Engineering**: Contexto médico especializado
- **Manejo de Errores**: Timeout y retry logic
- **Autenticación**: Bearer token con API key

### 🔧 Configuración
- **API Key**: Variable de entorno `SAPTIVA_API_KEY`
- **Endpoint**: `https://api.saptiva.com/v1/chat`
- **Timeout**: 30 segundos
- **Max Tokens**: 1000
- **Temperature**: 0.7

### 📊 Flujo de Respuesta
1. **Pregunta** → Embedding → Búsqueda en Weaviate
2. **Contexto** → Construcción con chunks relevantes
3. **Prompt** → Envío a Saptiva OPS con contexto médico
4. **Respuesta** → Procesamiento y envío al usuario
5. **Fuentes** → Metadatos de chunks utilizados

## Ventajas de Saptiva OPS

- 🎯 **Especialización Médica**: Modelo entrenado para contexto médico
- 🔒 **Seguridad**: API key para autenticación
- ⚡ **Rendimiento**: Respuestas rápidas y confiables
- 🌐 **Escalabilidad**: Servicio en la nube
- 🔧 **Configurabilidad**: Parámetros ajustables (temperature, max_tokens)

## Próximas Mejoras

- [ ] **Modelos Especializados**: Integrar modelos médicos específicos
- [ ] **Streaming**: Respuestas en tiempo real
- [ ] **Caching**: Cache de respuestas frecuentes
- [ ] **Monitoreo**: Métricas de uso de Saptiva
- [ ] **Fallback**: Modelos alternativos en caso de fallo
