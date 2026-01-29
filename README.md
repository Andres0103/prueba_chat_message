API RESTful para procesamiento de mensajes de chat construida con FastAPI y Clean Architecture.

## 🏗️ Arquitectura

Este proyecto sigue los principios de **Clean Architecture** con cuatro capas principales:

- **Domain**: Entidades y lógica de negocio pura (sin dependencias de frameworks)
- **Application**: Casos de uso y DTOs
- **Infrastructure**: Implementaciones técnicas (base de datos, configuraciones)
- **API**: Capa de presentación (endpoints HTTP)

## 🚀 Tecnologías

- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- SQLite
- Alembic (migraciones)
- Pytest
- Docker

## 📋 Requisitos Previos

- Python 3.11 o superior
- Docker y Docker Compose (opcional)

## ⚙️ Instalación

### Opción 1: Local (sin Docker)

1. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno
```bash
cp .env.example .env
```

4. Iniciar la aplicación
```bash
uvicorn src.main:app --reload
```

### Opción 2: Con Docker

```bash
docker-compose up --build
```

## 🧪 Testing

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Solo unitarios
pytest tests/unit
```

## 📚 Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📝 Estado del Proyecto

✅ Base sólida completada:
- Estructura Clean Architecture
- Domain entities (Python puro)
- Infrastructure (SQLAlchemy)
- Tests unitarios funcionando
- Docker configurado

🚧 Próximos pasos:
- Application layer (Use Cases)
- API endpoints
- Repository implementations
EOFREADME