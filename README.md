# Chat Message API

API RESTful para procesamiento de mensajes de chat construida con **FastAPI**, **SQLAlchemy (asyncio)** y siguiendo los principios de **Clean Architecture**.

---

## Tabla de Contenidos

- [Instalación y Configuración](#instalación-y-configuración)
- [Configuración de Base de Datos (OBLIGATORIO)](#configuración-de-base-de-datos-obligatorio)
- [Ejecutar la Aplicación](#ejecutar-la-aplicación)
- [Ejecutar Tests](#ejecutar-tests)
- [Documentación de API](#documentación-de-api)
- [Estructura del Proyecto](#estructura-del-proyecto)

---

## Instalación y Configuración

### Requisitos Previos

- **Python 3.11+**
- **pip** (gestor de paquetes de Python)
- **Git**
- **Docker y Docker Compose** (opcional, para containerización)

---

### FLUJO DE INSTALACIÓN CORRECTO (IMPORTANTE)

Este proyecto **NO crea tablas automáticamente**. Debes seguir estos pasos en orden:

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd chat-message-api

# 2. Crear entorno virtual
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. PASO CRÍTICO: Ejecutar migraciones de base de datos
alembic revision --autogenerate -m "create messages table"
alembic upgrade head

# 5. AHORA SÍ: Levantar Docker (si usas Docker)
docker-compose up --build
```

**Si omites el paso 4, obtendrás:**
```
sqlite3.OperationalError: no such table: messages
```

---

## Configuración de Base de Datos (OBLIGATORIO)

### ¿Por qué necesito hacer esto?

Este proyecto usa **Alembic** para gestionar el esquema de la base de datos. Las tablas **NO se crean automáticamente** al arrancar la aplicación.

### Flujo Correcto (EJECUTAR UNA VEZ POR ENTORNO)

#### Verificar URL de Base de Datos

**Por defecto**, el proyecto usa SQLite con archivo persistente:

```python
# En producción/Docker
DATABASE_URL = "sqlite:////app/data/chat_messages.db"

# En desarrollo local
DATABASE_URL = "sqlite:///./data/chat_messages.db"
```

---

#### Inicializar Base de Datos con Alembic (LOCAL)

Desde la raíz del proyecto, con el **entorno virtual activado**:

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1
alembic upgrade head

# macOS/Linux
source venv/bin/activate
alembic upgrade head
```

**¿Qué hace este comando?**

Crea el archivo `data/chat_messages.db` (si no existe)  
Crea todas las tablas definidas (`messages`)  
Registra la versión actual en `alembic_version`

---

#### Verificar que la Base de Datos se Creó

```bash
# Verificar que el archivo existe
ls data/

# Verificar tablas creadas
sqlite3 data/chat_messages.db ".tables"
```

**Salida esperada:**
```
messages         alembic_version
```

---

#### Levantar Docker (DESPUÉS de migrar)

```bash
# IMPORTANTE: Solo DESPUÉS de ejecutar alembic upgrade head
docker-compose up --build
```

**¿Por qué este orden?**

El volumen de Docker está configurado así:

```yaml
volumes:
  - ./data:/app/data
```

Esto significa que Docker **comparte** la carpeta `data/` con la máquina local. Si ejecuta `alembic upgrade head` **antes** de levantar Docker, el contenedor usará la base de datos ya migrada.

---

### Comandos Útiles de Alembic

```bash
# Ver estado actual de migraciones
alembic current

# Ver historial de migraciones
alembic history

# Deshacer última migración
alembic downgrade -1

# Volver a versión específica
alembic downgrade <revision_id>

# Crear nueva migración (para desarrolladores)
alembic revision --autogenerate -m "descripción del cambio"
```

---

### Flujo Completo con Docker

```bash
# 1. Clonar proyecto
git clone <repo-url>
cd chat-message-api

# 2. Crear entorno virtual e instalar dependencias
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS
pip install -r requirements.txt

# 3. CRÍTICO: Migrar base de datos
alembic revision --autogenerate -m "create messages table"
alembic upgrade head

# 4. Verificar que la BD existe
ls data/
sqlite3 data/chat_messages.db ".tables"

# 5. Levantar Docker
docker-compose up --build

# 6. Verificar que funciona
curl http://localhost:8000/docs
```

---

### Solución de Problemas - Base de Datos

#### Error: "no such table: messages"

**Causa:** No ejecutaste `alembic upgrade head`.

**Solución:**
```bash
# Detener Docker si está corriendo
docker-compose down

# Migrar base de datos
alembic upgrade head

# Volver a levantar Docker
docker-compose up --build
```

---

#### Error: "database is locked"

**Causa:** Múltiples procesos intentando acceder a SQLite.

**Solución:**
```bash
# Detener todos los procesos
docker-compose down
pkill -f uvicorn

# Reiniciar desde cero
alembic upgrade head
docker-compose up --build
```

---

#### Error: "alembic.util.exc.CommandError: Can't locate revision identified by 'xxxxx'"

**Causa:** Tu copia local no tiene las migraciones actualizadas.

**Solución:**
```bash
# Hacer pull de las últimas migraciones
git pull origin main

# Aplicar migraciones
alembic upgrade head
```

---

## Ejecutar la Aplicación

### Opción 1: Desarrollo Local (sin Docker)

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS

# Desarrollo con auto-reload
uvicorn src.main:app --reload

# Producción local
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

La API estará en: **http://localhost:8000**

---

### Opción 2: Con Docker

```bash
# Construir e iniciar
docker-compose up --build

# En modo detached (segundo plano)
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Detener
docker-compose down
```

La API estará en: **http://localhost:8000**

---

## Ejecutar Tests

### Comandos Básicos

```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS

# Ejecutar todos los tests
.\venv\Scripts\Activate.ps1 
venv\Scripts\python -m pytest -q

# Con cobertura
pytest tests/ --cov=src --cov-report=html

# Reporte en terminal
pytest tests/ --cov=src --cov-report=term-missing
```

### Tests por Categoría

```bash
# Solo integración (API)
pytest tests/integration/ -v

# Solo unitarios
pytest tests/unit/ -v

# Solo use cases
pytest tests/unit/test_application/ -v

# Solo dominio
pytest tests/unit/test_domain/ -v
```

### Estadísticas

- **Total:** 84 tests
- **Cobertura:** 89%
- **Tiempo:** ~2.48 segundos
- **Status:** Todos pasando

---

## Documentación de API

### Endpoints Principales

#### 1. Crear Mensaje

**POST** `/api/v1/messages`

```json
{
  "message_id": "msg-001",
  "session_id": "sesion-abc-123",
  "content": "Hola, este es un mensaje de prueba",
  "timestamp": "2026-01-30T14:30:00",
  "sender": "user"
}
```

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

---

#### 2. Obtener Mensajes

**GET** `/api/v1/messages/{session_id}?limit=10&offset=0&sender=user`

**Response (200 OK):**
```json
{
  "data": {
    "items": [...],
    "total": 2,
    "limit": 10,
    "offset": 0
  }
}
```
### 3. Mensaje de Error

**POST** `/api/v1/messages`
**Response (400 Bad Request):**
```json
{
  "status": "error",
  "error": {
  "code": "INVALID_FORMAT",
  "message": "Formato de mensaje inválido",
  "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}
```
### Documentación Interactiva

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Estructura del Proyecto

```
chat-message-api/
├── src/
│   ├── main.py
│   ├── API/v1/
│   │   ├── controllers/message_controller.py
│   │   └── schemas/
│   │   └── exceptions/handlers.py
│   ├── Application/
│   │   ├── use_cases/
│   │   └── interfaces/
│   │   └── dtos/
│   ├── Domain/
│   │   ├── entities/
│   │   ├── services/
│   │   └── value_objects/
│   └── Infrastructure/
│       ├── database/
│       │   ├── models.py
│       │   └── connection.py
│       └── repositories/
│       └── config/
│       └── Services/
├── alembic/              # Migraciones de BD
│   └── versions/
├── data/                 # Base de datos SQLite
│   └── chat_messages.db
├── tests/
│   └── integration/
│   └── unit/
├── .env
├── alembic.ini          # Configuración Alembic
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Dependencias Principales

| Librería | Versión | Propósito |
|----------|---------|-----------|
| FastAPI | 0.104+ | Framework web |
| SQLAlchemy | 2.0+ | ORM asíncrono |
| Alembic | 1.12+ | Migraciones BD |
| Pydantic | 2.0+ | Validación |
| Pytest | 7.0+ | Testing |
| Uvicorn | 0.24+ | Servidor ASGI |
| Mako | 1.3+ | Mako Templates |

---

## Configuración Avanzada

### Variables de Entorno

Crear `.env` en la raíz:

```env
DATABASE_URL=sqlite:///./data/chat_messages.db
DEBUG=True
LOG_LEVEL=INFO
```

### PostgreSQL (Producción)

```bash
pip install psycopg2-binary
```

```env
DATABASE_URL=postgresql://user:password@localhost:5432/chat_db
```

```bash
alembic upgrade head
```

---

## Checklist Pre-Deployment

- [ ] `alembic upgrade head` ejecutado
- [ ] Todos los tests pasan: `pytest tests/ -v`
- [ ] Cobertura >= 85%
- [ ] Variables de entorno configuradas
- [ ] Health check funciona: `curl http://localhost:8000/health`

---

## Solución de Problemas

### Port 8000 en uso

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:8000 | xargs kill -9
```

### ModuleNotFoundError

```bash
cd chat-message-api
pip install -r requirements.txt
```

---

## Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

---

**Última actualización:** 31 de Enero de 2026  
**Versión:** 1.0.0  
**Estado:** Producción Ready