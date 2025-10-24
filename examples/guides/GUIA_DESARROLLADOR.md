# Guía para Desarrolladores - MediCopilot

## 🏗️ Arquitectura del Sistema

MediCopilot está construido con una arquitectura de microservicios que incluye:

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

### Componentes Principales

- **FastAPI**: Backend REST API con documentación automática
- **Weaviate**: Base de datos vectorial para búsqueda semántica
- **Saptiva OPS**: Servicio de LLM para generación de respuestas
- **Docker**: Containerización y orquestación de servicios

## 🚀 Configuración del Entorno de Desarrollo

### Prerrequisitos

- Python 3.8+
- Docker y Docker Compose
- Git
- Editor de código (VS Code recomendado)

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd MediCopilot

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp env.example .env
# Editar .env con tus configuraciones

# 5. Iniciar servicios
docker-compose up -d weaviate
python app/main.py
```

### Estructura del Proyecto

```
MediCopilot/
├── app/
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── config.py              # Configuración y variables de entorno
│   ├── models.py              # Modelos Pydantic para validación
│   ├── services/              # Lógica de negocio
│   │   ├── vectorstore.py     # Cliente Weaviate
│   │   ├── llm.py            # Cliente Saptiva OPS
│   │   ├── ingest.py         # Procesamiento de documentos
│   │   └── rag.py            # Pipeline RAG
│   └── routers/              # Endpoints de la API
│       ├── documents.py      # Gestión de documentos
│       └── query.py         # Consultas médicas
├── examples/                 # Ejemplos y documentación
├── docker-compose.yml        # Orquestación de servicios
├── Dockerfile               # Imagen de la API
└── requirements.txt         # Dependencias Python
```

## 🔧 Desarrollo de Nuevas Funcionalidades

### 1. Agregar Nuevos Endpoints

Para agregar un nuevo endpoint, crea o modifica un archivo en `app/routers/`:

```python
# app/routers/nuevo_endpoint.py
from fastapi import APIRouter, HTTPException
from app.models import NuevoModelo

router = APIRouter(prefix="/nuevo", tags=["nuevo"])

@router.post("/accion")
async def nueva_accion(data: NuevoModelo):
    try:
        # Lógica de negocio aquí
        result = await procesar_datos(data)
        return {"resultado": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Luego regístralo en `app/main.py`:

```python
from app.routers import nuevo_endpoint

app.include_router(nuevo_endpoint.router)
```

### 2. Agregar Nuevos Modelos

Define nuevos modelos Pydantic en `app/models.py`:

```python
class NuevoModelo(BaseModel):
    campo1: str
    campo2: Optional[int] = None
    campo3: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "campo1": "valor_ejemplo",
                "campo2": 42,
                "campo3": ["item1", "item2"]
            }
        }
```

### 3. Agregar Nuevos Servicios

Crea nuevos servicios en `app/services/`:

```python
# app/services/nuevo_servicio.py
from app.config import settings
import httpx

class NuevoServicio:
    def __init__(self):
        self.api_url = settings.nueva_api_url
        self.api_key = settings.nueva_api_key
    
    async def procesar_datos(self, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/procesar",
                json=data,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()
```

## 🧪 Testing

### Ejecutar Tests Existentes

```bash
# Test rápido
python examples/scripts/test_quick.py

# Test completo
python examples/scripts/test_api_complete.py

# Cargar documentos de prueba
python examples/scripts/load_test_documents.py
```

### Crear Nuevos Tests

```python
# tests/test_nueva_funcionalidad.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_nueva_funcionalidad():
    response = client.post("/nuevo/accion", json={"campo1": "test"})
    assert response.status_code == 200
    assert response.json()["resultado"] is not None
```

## 🔍 Debugging

### Logs de la Aplicación

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver logs de Weaviate
docker-compose logs -f weaviate

# Ver logs de todos los servicios
docker-compose logs -f
```

### Debugging con VS Code

Crea `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app/main.py",
            "console": "integratedTerminal",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### Debugging de Weaviate

Accede a la consola de Weaviate en http://localhost:8080 para:
- Ver esquemas de datos
- Ejecutar consultas GraphQL
- Monitorear el estado de la base de datos

## 📊 Monitoreo y Métricas

### Health Checks

El sistema incluye varios endpoints de salud:

- `GET /health` - Estado general del sistema
- `GET /query/health` - Estado del servicio de consultas
- `GET /documents/stats` - Estadísticas de documentos

### Métricas Personalizadas

Para agregar métricas personalizadas:

```python
# app/services/metrics.py
import time
from functools import wraps

def track_metrics(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            # Log success metrics
            return result
        except Exception as e:
            # Log error metrics
            raise
        finally:
            duration = time.time() - start_time
            # Log duration metrics
    return wrapper
```

## 🔒 Seguridad

### Validación de Entrada

Siempre valida las entradas usando modelos Pydantic:

```python
from pydantic import BaseModel, validator

class DocumentUpload(BaseModel):
    filename: str
    content_type: str
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if v not in allowed_types:
            raise ValueError('Tipo de archivo no permitido')
        return v
```

### Manejo de Errores

```python
from fastapi import HTTPException
from app.models import ErrorResponse

async def procesar_documento(file):
    try:
        # Procesamiento aquí
        return resultado
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Archivo no encontrado"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )
```

## 🚀 Despliegue

### Desarrollo Local

```bash
# Iniciar todos los servicios
docker-compose up --build

# Iniciar solo servicios de base de datos
docker-compose up -d weaviate

# Ejecutar API localmente
python app/main.py
```

### Producción

```bash
# Construir imagen de producción
docker build -t medicopilot:latest .

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 Documentación de la API

### Documentación Automática

La API genera documentación automáticamente:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Documentar Nuevos Endpoints

```python
@router.post(
    "/nuevo-endpoint",
    response_model=NuevoModelo,
    summary="Descripción breve",
    description="Descripción detallada del endpoint",
    responses={
        200: {"description": "Operación exitosa"},
        400: {"description": "Datos inválidos"},
        500: {"description": "Error interno del servidor"}
    }
)
async def nuevo_endpoint(data: InputModel):
    """
    Descripción detallada del endpoint.
    
    - **param1**: Descripción del parámetro
    - **param2**: Descripción del segundo parámetro
    
    Returns:
        - **resultado**: Descripción del resultado
    """
    pass
```

## 🔄 Integración Continua

### GitHub Actions

Crea `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python examples/scripts/test_quick.py
```

## 🤝 Contribución

### Flujo de Trabajo

1. **Fork** el repositorio
2. **Crea** una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. **Desarrolla** tu funcionalidad
4. **Escribe** tests para tu código
5. **Ejecuta** todos los tests: `python examples/scripts/test_api_complete.py`
6. **Commit** tus cambios: `git commit -m "Agregar nueva funcionalidad"`
7. **Push** a tu rama: `git push origin feature/nueva-funcionalidad`
8. **Abre** un Pull Request

### Estándares de Código

- **PEP 8** para estilo de código Python
- **Type hints** para todas las funciones
- **Docstrings** para todas las funciones públicas
- **Tests** para toda la funcionalidad nueva

### Revisión de Código

Antes de hacer merge:
- [ ] Código sigue los estándares establecidos
- [ ] Tests pasan correctamente
- [ ] Documentación actualizada
- [ ] No hay vulnerabilidades de seguridad
- [ ] Performance aceptable

## 📞 Soporte

Para soporte técnico:

1. **Revisa** la documentación existente
2. **Busca** en los issues existentes
3. **Crea** un nuevo issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Logs relevantes
   - Versión del sistema

---

**¡Feliz desarrollo!** 🚀
