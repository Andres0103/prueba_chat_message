#Importante: Este archivo maneja la creación y gestión de sesiones de base de datos usando SQLAlchemy.
from src.Infrastructure.database.connection import AsyncSessionLocal

# Exportar el factory de sesiones asíncronas
SessionLocal = AsyncSessionLocal

