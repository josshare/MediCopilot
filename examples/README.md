# Ejemplos y Documentación - MediCopilot

Esta carpeta contiene ejemplos, scripts de testing y documentación completa para MediCopilot.

## 📁 Estructura

```
examples/
├── test-documents/          # Documentos médicos de ejemplo
├── scripts/                 # Scripts de testing automatizado
├── guides/                  # Guías de usuario y desarrollador
├── test-data/              # Datos de prueba adicionales
└── README.md               # Este archivo
```

## 🚀 Inicio Rápido

### 1. Configurar el Entorno

```bash
# Desde el directorio raíz del proyecto
cd MediCopilot

# Configurar variables de entorno
cp env.example .env
# Editar .env con tu clave API de Saptiva

# Iniciar servicios
docker-compose up --build
```

### 2. Ejecutar Tests

```bash
# Test rápido
python examples/scripts/test_quick.py

# Test completo
python examples/scripts/test_api_complete.py

# Cargar documentos de prueba
python examples/scripts/load_test_documents.py
```

### 3. Explorar Documentación

- **Guía de Usuario**: `guides/GUIA_USUARIO.md`
- **Guía de Desarrollador**: `guides/GUIA_DESARROLLADOR.md`
- **Solución de Problemas**: `guides/GUIA_SOLUCION_PROBLEMAS.md`

## 📚 Documentos de Prueba

### Contenido Disponible

Los documentos en `test-documents/` incluyen:

1. **paracetamol_efectos_secundarios.txt**
   - Efectos secundarios del paracetamol
   - Contraindicaciones y precauciones
   - Dosis recomendadas
   - Interacciones medicamentosas

2. **ibuprofeno_guia_clinica.txt**
   - Guía clínica completa del ibuprofeno
   - Mecanismo de acción
   - Indicaciones y contraindicaciones
   - Efectos secundarios y precauciones

3. **protocolo_hipertension.txt**
   - Protocolo de manejo de hipertensión arterial
   - Clasificación y diagnóstico
   - Tratamiento farmacológico y no farmacológico
   - Seguimiento y complicaciones

4. **diabetes_tipo2_manejo.txt**
   - Manejo integral de diabetes tipo 2
   - Objetivos de control
   - Tratamiento farmacológico
   - Complicaciones y seguimiento

5. **antibioticos_uso_racional.txt**
   - Uso racional de antibióticos
   - Clasificación por espectro
   - Indicaciones comunes
   - Prevención de resistencia

### Cargar Documentos

```bash
# Cargar todos los documentos de prueba
python examples/scripts/load_test_documents.py

# Cargar un documento específico
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@examples/test-documents/paracetamol_efectos_secundarios.txt"
```

## 🧪 Scripts de Testing

### test_quick.py
Script de testing rápido que verifica:
- Salud de la API
- Servicio de consultas
- Estadísticas de documentos
- Consulta de prueba

```bash
python examples/scripts/test_quick.py
```

### test_api_complete.py
Suite completa de testing que incluye:
- Tests de todos los endpoints
- Carga de múltiples documentos
- Consultas variadas
- Gestión de documentos
- Resumen de resultados

```bash
python examples/scripts/test_api_complete.py
```

### load_test_documents.py
Script para cargar todos los documentos de prueba:
- Carga automática de todos los archivos .txt
- Verificación de éxito/fallo
- Estadísticas finales

```bash
python examples/scripts/load_test_documents.py
```

## 📖 Guías de Documentación

### Guía de Usuario
**Archivo**: `guides/GUIA_USUARIO.md`

Contenido:
- Configuración inicial
- Cómo cargar documentos
- Cómo hacer consultas médicas
- Tipos de consultas recomendadas
- Consejos para mejores resultados
- Interpretación de respuestas
- Solución de problemas comunes
- Uso de la interfaz web

### Guía de Desarrollador
**Archivo**: `guides/GUIA_DESARROLLADOR.md`

Contenido:
- Arquitectura del sistema
- Configuración del entorno de desarrollo
- Desarrollo de nuevas funcionalidades
- Testing y debugging
- Monitoreo y métricas
- Seguridad
- Despliegue
- Integración continua
- Contribución

### Guía de Solución de Problemas
**Archivo**: `guides/GUIA_SOLUCION_PROBLEMAS.md`

Contenido:
- Problemas comunes y soluciones
- Diagnóstico avanzado
- Herramientas de diagnóstico
- Logs y debugging
- Optimización
- Soporte técnico

## 🔍 Ejemplos de Consultas

### Consultas sobre Medicamentos

```bash
# Efectos secundarios
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los efectos secundarios del paracetamol?"}'

# Dosis pediátricas
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo se debe dosificar el ibuprofeno en niños?"}'

# Contraindicaciones
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuándo no se debe usar paracetamol?"}'
```

### Consultas sobre Enfermedades

```bash
# Síntomas
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son los síntomas de la diabetes tipo 2?"}'

# Diagnóstico
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cómo se diagnostica la hipertensión arterial?"}'

# Complicaciones
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué complicaciones puede tener la diabetes?"}'
```

### Consultas sobre Protocolos

```bash
# Manejo de hipertensión
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuál es el protocolo de manejo de hipertensión?"}'

# Uso de antibióticos
curl -X POST "http://localhost:8000/query/" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuándo se debe usar un antibiótico?"}'
```

## 🛠️ Personalización

### Agregar Nuevos Documentos

1. Coloca tu documento en `test-documents/`
2. Asegúrate de que esté en formato soportado (PDF, TXT, DOCX)
3. Cárgalo usando el script o la API

### Crear Nuevos Tests

1. Crea un nuevo archivo en `scripts/`
2. Sigue el patrón de los scripts existentes
3. Incluye manejo de errores y logging
4. Documenta el propósito del script

### Modificar Configuración

1. Edita `docker-compose.yml` para cambios de infraestructura
2. Edita `app/config.py` para cambios de aplicación
3. Edita `.env` para variables de entorno

## 📊 Monitoreo

### Verificar Estado del Sistema

```bash
# Estado de servicios
docker-compose ps

# Logs en tiempo real
docker-compose logs -f

# Estadísticas de documentos
curl http://localhost:8000/documents/stats
```

### Métricas de Rendimiento

```bash
# Uso de recursos
docker stats

# Logs de errores
docker-compose logs api | grep -i error

# Logs de consultas
docker-compose logs api | grep -i query
```

## 🤝 Contribución

### Agregar Nuevos Ejemplos

1. Crea el archivo en la carpeta apropiada
2. Sigue las convenciones de naming
3. Incluye documentación
4. Actualiza este README

### Mejorar Documentación

1. Identifica áreas de mejora
2. Actualiza las guías correspondientes
3. Incluye ejemplos prácticos
4. Mantén la consistencia de estilo

### Reportar Problemas

1. Usa la guía de solución de problemas
2. Incluye logs relevantes
3. Proporciona pasos para reproducir
4. Especifica versión y configuración

## 📞 Soporte

Para soporte técnico:

1. **Revisa la documentación**: Comienza con las guías
2. **Ejecuta los tests**: Verifica que todo funcione
3. **Revisa los logs**: Identifica el problema específico
4. **Consulta la guía de solución de problemas**: Busca soluciones conocidas
5. **Contacta al equipo**: Si el problema persiste

---

**¡Esperamos que estos ejemplos y documentación te ayuden a usar MediCopilot efectivamente!** 🚀
