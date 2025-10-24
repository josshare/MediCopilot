# Guía de Usuario - MediCopilot

## 📖 Introducción

MediCopilot es un asistente médico inteligente que utiliza tecnología de inteligencia artificial para ayudar a profesionales de la salud a encontrar información médica relevante de manera rápida y precisa. El sistema puede procesar documentos médicos y responder consultas basándose en el contenido de esos documentos.

## 🚀 Inicio Rápido

### 1. Configuración Inicial

Antes de usar MediCopilot, asegúrate de tener:

- **Docker** instalado en tu sistema
- **Docker Compose** instalado
- Una **clave API de Saptiva OPS**

### 2. Instalación

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd MediCopilot

# 2. Configurar variables de entorno
cp env.example .env

# 3. Editar el archivo .env y agregar tu clave API
# SAPTIVA_API_KEY=tu_clave_api_aqui

# 4. Iniciar la aplicación
docker-compose up --build
```

### 3. Verificar Instalación

Una vez que los servicios estén ejecutándose, puedes verificar que todo funciona correctamente:

```bash
# Verificar salud de la API
curl http://localhost:8000/health

# Verificar servicio de consultas
curl http://localhost:8000/query/health
```

## 📚 Cómo Usar MediCopilot

### 1. Cargar Documentos Médicos

MediCopilot puede procesar documentos en formato PDF, TXT y DOCX. Para cargar un documento:

```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mi_documento_medico.pdf"
```

**Respuesta esperada:**
```json
{
  "document_id": "uuid-del-documento",
  "filename": "mi_documento_medico.pdf",
  "chunks_created": 15,
  "message": "Document 'mi_documento_medico.pdf' processed successfully with 15 chunks"
}
```

### 2. Hacer Consultas Médicas

Una vez que hayas cargado documentos, puedes hacer consultas médicas:

```bash
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuáles son los efectos secundarios del paracetamol?",
    "max_results": 5
  }'
```

**Respuesta esperada:**
```json
{
  "answer": "Basándome en los documentos disponibles, el paracetamol puede causar...",
  "sources": [
    {
      "filename": "mi_documento_medico.pdf",
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

### 3. Gestionar Documentos

#### Ver Resumen de un Documento
```bash
curl http://localhost:8000/documents/{document_id}/summary
```

#### Ver Estadísticas de Documentos
```bash
curl http://localhost:8000/documents/stats
```

#### Eliminar un Documento
```bash
curl -X DELETE http://localhost:8000/documents/{document_id}
```

## 🔍 Tipos de Consultas Recomendadas

### Consultas sobre Medicamentos
- "¿Cuáles son las dosis recomendadas del ibuprofeno?"
- "¿Qué contraindicaciones tiene el paracetamol?"
- "¿Cómo interactúa la warfarina con otros medicamentos?"

### Consultas sobre Enfermedades
- "¿Cuáles son los síntomas de la diabetes tipo 2?"
- "¿Cómo se diagnostica la hipertensión arterial?"
- "¿Qué complicaciones puede tener la diabetes?"

### Consultas sobre Protocolos
- "¿Cuál es el protocolo de manejo de hipertensión?"
- "¿Cómo se debe tratar una crisis hipertensiva?"
- "¿Cuáles son los objetivos de control en diabetes?"

### Consultas sobre Efectos Secundarios
- "¿Qué efectos secundarios puede tener el ibuprofeno?"
- "¿Cuándo debo suspender un antibiótico?"
- "¿Qué reacciones alérgicas puede causar la penicilina?"

## 💡 Consejos para Mejores Resultados

### 1. Formular Preguntas Específicas
- ✅ **Bueno**: "¿Cuáles son las dosis pediátricas del paracetamol?"
- ❌ **Menos efectivo**: "¿Qué pasa con el paracetamol?"

### 2. Usar Términos Médicos Precisos
- ✅ **Bueno**: "¿Cuáles son las contraindicaciones del ibuprofeno en pacientes con insuficiencia renal?"
- ❌ **Menos efectivo**: "¿Cuándo no puedo dar ibuprofeno?"

### 3. Especificar Contexto Clínico
- ✅ **Bueno**: "¿Cómo se debe dosificar la metformina en pacientes con diabetes tipo 2 y función renal normal?"
- ❌ **Menos efectivo**: "¿Cuánta metformina debo dar?"

## 📊 Interpretando las Respuestas

### Componentes de la Respuesta

1. **Answer**: La respuesta principal generada por la IA
2. **Sources**: Lista de fuentes utilizadas para generar la respuesta
3. **Query**: La pregunta original que hiciste
4. **Timestamp**: Momento en que se procesó la consulta

### Interpretando las Fuentes

Cada fuente incluye:
- **filename**: Nombre del documento de origen
- **chunk_index**: Número del fragmento utilizado
- **content_preview**: Vista previa del contenido relevante
- **relevance_score**: Puntuación de relevancia (0-1, más alto = más relevante)
- **document_id**: Identificador único del documento

## 🛠️ Solución de Problemas Comunes

### Error: "No se puede conectar a la API"
**Solución**: Verifica que Docker esté ejecutándose y que los servicios estén activos:
```bash
docker-compose ps
docker-compose logs api
```

### Error: "Documento no se puede procesar"
**Solución**: 
- Verifica que el archivo esté en formato soportado (PDF, TXT, DOCX)
- Asegúrate de que el archivo no esté corrupto
- Verifica que el archivo no esté vacío

### Error: "No se encontraron fuentes relevantes"
**Solución**:
- Asegúrate de haber cargado documentos relevantes
- Reformula tu pregunta con términos más específicos
- Verifica que los documentos contengan información sobre el tema consultado

### Error: "Respuesta muy genérica"
**Solución**:
- Haz preguntas más específicas
- Carga más documentos relacionados con el tema
- Usa términos médicos precisos en tus consultas

## 📱 Usando la Interfaz Web

MediCopilot incluye una interfaz web interactiva disponible en:
- **Documentación API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Usando la Interfaz Swagger

1. Ve a http://localhost:8000/docs
2. Expande el endpoint que quieres usar
3. Haz clic en "Try it out"
4. Completa los parámetros requeridos
5. Haz clic en "Execute"

## 🔒 Consideraciones de Seguridad

### Datos Sensibles
- **No cargues** documentos con información de pacientes identificables
- **Usa solo** documentos médicos generales o protocolos
- **Considera** anonimizar datos antes de cargar

### Uso Responsable
- Las respuestas son **sugerencias** basadas en los documentos cargados
- **Siempre verifica** la información con fuentes oficiales
- **No uses** las respuestas como único criterio para decisiones médicas

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. **Revisa los logs**: `docker-compose logs -f`
2. **Verifica la configuración**: Revisa el archivo `.env`
3. **Consulta la documentación**: Revisa este archivo y la documentación de la API
4. **Contacta al equipo**: Crea un issue en GitHub o contacta al equipo de desarrollo

## 🎯 Próximos Pasos

Una vez que te sientas cómodo con las funciones básicas:

1. **Carga más documentos**: Agrega protocolos, guías clínicas y referencias médicas
2. **Experimenta con consultas**: Prueba diferentes tipos de preguntas
3. **Integra con tu flujo de trabajo**: Usa la API en tus aplicaciones
4. **Comparte feedback**: Ayuda a mejorar el sistema reportando problemas o sugiriendo mejoras

---

**¡Feliz uso de MediCopilot!** 🚀
