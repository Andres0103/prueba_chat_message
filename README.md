# Chat Message API

API RESTful para procesamiento de mensajes de chat construida con **FastAPI**, **SQLAlchemy** y siguiendo los principios de **Clean Architecture**.

## Descripción General

Chat Message API es una aplicación backend que permite:

- **Crear mensajes** con validación de contenido
- **Filtrar contenido inapropiado** (spam, malware, intentos de hack)
- **Recuperar mensajes** con paginación y filtrado por remitente
- **Gestionar sesiones** de chat aisladas
- **Extraer metadatos** automáticamente (contador de palabras, caracteres, etc.)

### Características Principales

**Validación robusta** de datos de entrada  
**Filtrado de contenido** intelligent (spam, malware, hack)  
**Paginación** flexible de mensajes  
**Filtrado por remitente** (usuario/sistema)  
**Metadatos automáticos** (fecha/hora, conteos)  
**Manejo de errores** completo con códigos HTTP apropiados  
**78 tests** con 89% de cobertura de código  
**Documentación interactiva** (Swagger UI y ReDoc)  

---

## Arquitectura

El proyecto sigue **Clean Architecture** con 4 capas independientes:

```
src/
├── API/                          # Capa de Presentación
│   └── v1/controllers/          # Endpoints HTTP
│   └── v1/schemas/              # Schemas Pydantic
│
├── Application/                  # Capa de Aplicación
│   ├── use_cases/               # Lógica de negocio (CreateMessage, GetMessages)
│   ├── dtos/                    # Data Transfer Objects
│   └── interfaces/              # Contratos/Interfaces
│
├── Domain/                       # Capa de Dominio (sin dependencias)
│   ├── entities/                # MessageEntity
│   ├── services/                # ContentFilterService, MessageProcessor
│   └── value_objects/           # SenderType, MessageMetadata
│
└── Infrastructure/              # Capa de Infraestructura
    ├── database/                # Conexión, modelos SQLAlchemy
    ├── repositories/            # MessageRepositoryImpl
    └── config/                  # Configuración
```

### Ventajas de la Arquitectura

- **Independencia de frameworks**: La lógica de negocio no depende de FastAPI ni SQLAlchemy
- **Testabilidad**: Cada capa puede ser testeada en aislamiento
- **Mantenibilidad**: Cambios en una capa no afectan las otras
- **Escalabilidad**: Fácil agregar nuevos features sin modificar código existente

---

## Instalación y Configuración

### Requisitos Previos

- **Python 3.11+**
- **pip** (gestor de paquetes de Python)
- **Git**
- **Docker y Docker Compose** (opcional, solo para containerización)

### Opción 1: Instalación Local

#### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd chat-message-api
```

#### 2. Crear entorno virtual

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno (opcional)

```bash
# Crear archivo .env
cp .env.example .env

# Editar .env con tus valores (opcional, hay defaults)
# DATABASE_URL=sqlite:///./chat_messages.db
# DEBUG=True
```

#### 5. Iniciar la aplicación

```bash
# Desarrollo con auto-reload
uvicorn src.main:app --reload

# Producción
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: **http://localhost:8000**

### Opción 2: Instalación con Docker

#### Requisitos
- Docker 20.10+
- Docker Compose 1.29+

#### Pasos

```bash
# 1. Construir imagen
docker-compose build

# 2. Iniciar servicios
docker-compose up -d

# 3. Ver logs
docker-compose logs -f api
```

La API estará disponible en: **http://localhost:8000**

---

## Documentación de API

### Endpoints Disponibles

#### 1. Crear Mensaje

**POST** `/api/v1/messages`

Crea un nuevo mensaje en una sesión.

**Request Body:**
```json
{
  "message_id": "msg-001",
  "session_id": "sesion-abc-123",
  "content": "Hola, este es un mensaje de prueba",
  "timestamp": "2026-01-30T14:30:00",
  "sender": "user"
}
```

**Campos requeridos:**
- `message_id` (string): ID único del mensaje
- `session_id` (string): ID de la sesión
- `content` (string): Contenido del mensaje (no vacío, no solo espacios)
- `timestamp` (ISO 8601): Fecha/hora del mensaje
- `sender` (string): "user" o "system"

**Response (201 Created):**
```json
{
  "data": {
    "message_id": "msg-001",
    "session_id": "sesion-abc-123",
    "content": "Hola, este es un mensaje de prueba",
    "timestamp": "2026-01-30T14:30:00",
    "sender": "user",
    "metadata": {
      "word_count": 7,
      "character_count": 37,
      "processed_at": "2026-01-30T14:30:00.123456"
    }
  }
}
```

**Posibles errores:**

| Código | Descripción |
|--------|-------------|
| 201 | Mensaje creado exitosamente |
| 400 | Validación fallida (sender inválido, contenido inapropiado) |
| 422 | Campo requerido faltante o formato inválido |
| 500 | Error interno del servidor |

**Ejemplos de contenido inapropiado rechazado:**
- "Este es spam" → Rechazado (palabra: spam)
- "Contiene malware" → Rechazado (palabra: malware)
- "Intento de hack" → Rechazado (palabra: hack)

**Ejemplo cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message_id": "msg-001",
    "session_id": "sesion-123",
    "content": "Hola mundo",
    "timestamp": "2026-01-30T14:30:00",
    "sender": "user"
  }'
```

---

#### 2. Obtener Mensajes de Sesión

**GET** `/api/v1/messages/{session_id}`

Recupera mensajes de una sesión con paginación y filtrado.

**Parámetros de Query:**
- `limit` (integer, default=10): Número de mensajes a retornar (máximo 100)
- `offset` (integer, default=0): Número de mensajes a saltar
- `sender` (string, optional): Filtrar por "user" o "system"

**Response (200 OK):**
```json
{
  "data": {
    "items": [
      {
        "message_id": "msg-001",
        "session_id": "sesion-abc",
        "content": "Primer mensaje",
        "timestamp": "2026-01-30T14:30:00",
        "sender": "user",
        "metadata": {
          "word_count": 2,
          "character_count": 14,
          "processed_at": "2026-01-30T14:30:00.123456"
        }
      },
      {
        "message_id": "msg-002",
        "session_id": "sesion-abc",
        "content": "Segundo mensaje",
        "timestamp": "2026-01-30T14:31:00",
        "sender": "system",
        "metadata": {
          "word_count": 2,
          "character_count": 15,
          "processed_at": "2026-01-30T14:31:00.654321"
        }
      }
    ],
    "total": 2,
    "limit": 10,
    "offset": 0
  }
}
```

**Parámetros de ejemplo:**

```bash
# Obtener primeros 10 mensajes (default)
GET /api/v1/messages/sesion-abc

# Obtener 5 mensajes saltando los primeros 10
GET /api/v1/messages/sesion-abc?limit=5&offset=10

# Solo mensajes del usuario
GET /api/v1/messages/sesion-abc?sender=user

# Solo mensajes del sistema
GET /api/v1/messages/sesion-abc?sender=system

# Combinado: 20 mensajes del usuario, saltando 5
GET /api/v1/messages/sesion-abc?limit=20&offset=5&sender=user
```

**Ejemplo cURL:**
```bash
# Básico
curl "http://localhost:8000/api/v1/messages/sesion-123"

# Con parámetros
curl "http://localhost:8000/api/v1/messages/sesion-123?limit=5&sender=user"
```

**Posibles errores:**

| Código | Descripción |
|--------|-------------|
| 200 | Exitoso (puede ser lista vacía) |
| 400 | Parámetros inválidos |
| 500 | Error interno del servidor |

---

### Formatos Aceptados

#### Timestamps (ISO 8601)

```
2026-01-30T14:30:00              # Con hora
2026-01-30T14:30:00Z             # Con zona UTC
2026-01-30T14:30:00+00:00        # Con offset
2026-01-30T14:30:00.123456       # Con microsegundos
```

#### Senders Válidos

```
"user"       # Mensaje de usuario
"system"     # Mensaje del sistema
```

---

### Documentación Interactiva

Acceda a la documentación interactiva de la API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

En estas interfaces puede:
- Ver todos los endpoints
- Probar endpoints directamente
- Ver esquemas de request/response
- Descargar especificación OpenAPI

---

##  Guía de Pruebas

### Ejecutar Todos los Tests

```bash
# Tests básicos
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ --cov=src --cov-report=html

# Con reporte detallado
pytest tests/ --cov=src --cov-report=term-missing
```

### Ejecutar por Categoría

```bash
# Solo tests de integración (API endpoints)
pytest tests/integration/ -v

# Solo tests unitarios
pytest tests/unit/ -v

# Solo tests de casos de uso
pytest tests/unit/test_application/ -v

# Solo tests de dominio
pytest tests/unit/test_domain/ -v
```

### Ejecutar Tests Específicos

```bash
# Test específico
pytest tests/unit/test_application/test_create_message_use_case.py::TestCreateMessageUseCaseSuccess::test_create_message_with_valid_data_returns_response_dto -v

# Clase específica
pytest tests/unit/test_domain/test_content_filter.py::TestContentFilterServiceFilter -v

# Por nombre
pytest tests/ -k "test_filter" -v
```

### Estadísticas de Pruebas

- **Total Tests**: 78 
- **Cobertura**: 89% 
- **Tiempo ejecución**: ~2.2 segundos
- **Status**: Todos pasando

**Desglose:**
- 16 Tests de Integración (API endpoints)
- 13 Tests CreateMessageUseCase
- 13 Tests GetMessagesUseCase
- 27 Tests ContentFilterService
- 9 Tests de entidades de dominio

### Generador HTML de Cobertura

```bash
# Generar reporte HTML
pytest tests/ --cov=src --cov-report=html

# Abrir en navegador (Windows)
start htmlcov/index.html

# Abrir en navegador (macOS)
open htmlcov/index.html

# Abrir en navegador (Linux)
firefox htmlcov/index.html
```

---

##  Estructura del Proyecto

```
chat-message-api/
├── src/
│   ├── main.py                          # Punto de entrada FastAPI
│   ├── API/
│   │   ├── v1/
│   │   │   ├── controllers/
│   │   │   │   └── message_controller.py    # Endpoints HTTP
│   │   │   └── schemas/
│   │   │       ├── message_schema.py        # Schemas request/response
│   │   │       ├── response_schema.py       # Envoltura de respuesta
│   │   │       └── error_schema.py          # Schemas de error
│   │   └── exceptions/
│   │       └── handlers.py
│   │
│   ├── Application/
│   │   ├── use_cases/
│   │   │   ├── create_message_use_case.py   # Crear mensaje
│   │   │   └── get_messages_use_case.py     # Obtener mensajes
│   │   ├── dtos/
│   │   │   ├── message_dto.py
│   │   │   └── pagination_dto.py
│   │   └── interfaces/
│   │       ├── content_filter_interface.py
│   │       ├── message_processor_interface.py
│   │       └── message_repository_interface.py
│   │
│   ├── Domain/
│   │   ├── entities/
│   │   │   └── message_entity.py           # Entidad de dominio
│   │   ├── services/
│   │   │   ├── content_filter.py           # Filtrador de spam
│   │   │   └── message_processor.py        # Procesador de metadatos
│   │   └── value_objects/
│   │       ├── sender_type.py              # Enum: user/system
│   │       └── message_metadata.py         # Metadatos del mensaje
│   │
│   └── Infrastructure/
│       ├── database/
│       │   ├── models.py                   # Modelos SQLAlchemy
│       │   ├── connection.py               # Conexión a DB
│       │   └── session.py
│       ├── repositories/
│       │   └── message_repository_impl.py  # Implementación repositorio
│       └── config/
│           └── settings.py                 # Configuración
│
├── tests/
│   ├── integration/
│   │   └── test_message_controller_api.py  # 16 tests API
│   ├── unit/
│   │   ├── test_application/
│   │   │   ├── test_create_message_use_case.py   # 13 tests
│   │   │   └── test_get_messages_use_case.py     # 13 tests
│   │   └── test_domain/
│   │       ├── test_content_filter.py            # 27 tests
│   │       ├── test_message_entity.py
│   │       ├── test_message_metadata.py
│   │       └── test_sender_type.py
│   └── conftest.py                         # Fixtures pytest
│
├── alembic/                                 # Migraciones de DB
├── data/                                    # Datos de la aplicación
├── docker-compose.yml                       # Composición Docker
├── Dockerfile                               # Imagen Docker
├── requirements.txt                         # Dependencias Python
├── pytest.ini                               # Configuración pytest
└── README.md                                # Este archivo
```

---

##  Flujo de Desarrollo

### Crear un Mensaje

```python
# 1. Request llega al endpoint (API)
POST /api/v1/messages
{
  "message_id": "msg-001",
  "session_id": "sesion-abc",
  "content": "Hola",
  "timestamp": "2026-01-30T14:30:00",
  "sender": "user"
}

# 2. Controller valida y convierte a DTO (Application)
CreateMessageDTO(...)

# 3. Use Case procesa la lógica
a) ContentFilterService.filter() → valida contenido
b) MessageProcessor.process() → extrae metadatos
c) Repository.save() → persiste en BD

# 4. Response con metadata
{
  "data": {
    "message_id": "msg-001",
    ...
    "metadata": {
      "word_count": 1,
      "character_count": 4,
      "processed_at": "2026-01-30T14:30:00.123456"
    }
  }
}
```

---

##  Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'src'"

**Solución:**
```bash
# Asegurarse de estar en el directorio raíz
cd chat-message-api

# Instalar dependencias
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"

**Solución:**
```bash
# Usar puerto diferente
uvicorn src.main:app --port 8001

# O matar proceso en puerto 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### Tests fallan con "database locked"

**Solución:**
```bash
# Usar SQLite con archivo en lugar de en-memoria
# El proyecto ya usa archivo por defecto
pytest tests/ -v
```

### Cobertura baja en reportes

**Solución:**
```bash
# Generar reporte detallado
pytest tests/ --cov=src --cov-report=term-missing

# Ver archivos con baja cobertura en htmlcov/index.html
pytest tests/ --cov=src --cov-report=html
start htmlcov/index.html
```

---

##  Dependencias Principales

| Librería | Versión | Propósito |
|----------|---------|----------|
| FastAPI | 0.104+ | Framework web |
| Pydantic | 2.0+ | Validación de datos |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migraciones DB |
| Pytest | 7.0+ | Testing |
| Uvicorn | 0.24+ | Servidor ASGI |

Ver `requirements.txt` para versiones exactas.

---

##  Contribuir

1. Fork el repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

---

## Licencia


---

##  Soporte


##  Configuración Avanzada

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Database
DATABASE_URL=sqlite:///./chat_messages.db

# App
APP_NAME=chat-message-api
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Entornos

**Desarrollo:**
```env
DEBUG=True
DATABASE_URL=sqlite:///./chat_messages_dev.db
LOG_LEVEL=DEBUG
```

**Producción:**
```env
DEBUG=False
DATABASE_URL=sqlite:///./chat_messages.db
LOG_LEVEL=WARNING
HOST=0.0.0.0
PORT=8000
```

### PostgreSQL (Producción)

Para usar PostgreSQL en lugar de SQLite:

```bash
# Instalar driver
pip install psycopg2-binary

# Variable de entorno
DATABASE_URL=postgresql://user:password@localhost:5432/chat_db
```

---

## Guía de Desarrollo

### Crear una Nueva Feature

#### 1. Crear Schema (API)
```python
# src/API/v1/schemas/
class MiSchema(BaseModel):
    campo: str
```

#### 2. Crear Use Case (Application)
```python
# src/Application/use_cases/
class MiUseCase:
    def execute(self, request):
        # Lógica de negocio
        pass
```

#### 3. Crear Entidad (Domain)
```python
# src/Domain/entities/
class MiEntidad:
    # Entidad de dominio
    pass
```

#### 4. Implementar Repositorio (Infrastructure)
```python
# src/Infrastructure/repositories/
class MiRepository:
    def save(self):
        pass
```

#### 5. Crear Endpoint (API)
```python
# src/API/v1/controllers/
@router.post("/mi-endpoint")
async def mi_endpoint(request: MiSchema):
    # Lógica del endpoint
    pass
```

#### 6. Crear Tests
```python
# tests/integration/ o tests/unit/
def test_mi_feature():
    # Tests
    pass

# Ejecutar
pytest tests/ -v
```

### Estándares de Código

**Type Hints:**
```python
#  Siempre usar type hints
def procesar(mensajes: List[str]) -> Dict[str, int]:
    return {"total": len(mensajes)}

#  Sin type hints
def procesar(mensajes):
    return {"total": len(mensajes)}
```

**Docstrings:**
```python
# Docstrings detallados
def filtrar_spam(contenido: str) -> bool:
    """
    Detectar spam en contenido.
    
    Args:
        contenido: Texto a validar
        
    Returns:
        True si es spam, False si no
    """
    pass
```

**Commits:**
```bash
# Mensajes descriptivos
git commit -m "feat: agregar nuevo endpoint de búsqueda"
git commit -m "fix: corregir error en filtro de spam"
git commit -m "docs: actualizar README"

# Genéricos
git commit -m "fix"
git commit -m "actualizar"
```

### Debugging

**Con Python Debugger:**
```python
import pdb

@router.post("/messages")
async def create_message(request: CreateMessageRequest):
    pdb.set_trace()  # Se detendrá aquí
    # Comandos: n (next), c (continue), l (list)
```

**Con Logging:**
```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Mensaje de debug")
logger.info("Información")
logger.error("Error ocurrido")
```

---

## Checklist de Release

Antes de hacer deploy a producción:

- [ ] Todos los tests pasan: `pytest tests/ -v`
- [ ] Cobertura >= 85%: `pytest tests/ --cov=src`
- [ ] Código sin linting errors: `flake8 src/`
- [ ] Documentación actualizada
- [ ] Variables de entorno configuradas
- [ ] Base de datos migrada: `alembic upgrade head`
- [ ] Health check funciona: `curl http://localhost:8000/health`
- [ ] API docs accesibles: `http://localhost:8000/docs`

---

## Troubleshooting Avanzado

### "database is locked"

```bash
# SQLite no soporta múltiples conexiones concurrentes
# Solución: Usar PostgreSQL o cambiar a archivo DB

# Reiniciar aplicación
pkill -f "uvicorn"
sleep 2
uvicorn src.main:app --reload
```

### Tests fallan aleatoriamente

```bash
# Ejecutar tests secuencialmente
pytest tests/ -n 1

# Limpiar estado previo
pytest tests/ --tb=short
```

### Slow queries

```python
# Agregar índices en BD
from sqlalchemy import Index

class Message(Base):
    __tablename__ = "message"
    
    # Agregar índice
    __table_args__ = (
        Index('idx_session_id', 'session_id'),
    )
```

---

## 🎓 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Clean Architecture en Python](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [pytest Documentation](https://docs.pytest.org/)

---

**Última actualización**: 31 de Enero de 2026  
**Versión**: 1.0.0  
**Estado**:  Producción Ready
