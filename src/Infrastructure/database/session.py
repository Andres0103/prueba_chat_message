#Importante: Este archivo maneja la creación y gestión de sesiones de base de datos usando SQLAlchemy.
from sqlalchemy.orm import sessionmaker

from src.Infrastructure.database.connection import engine

# Factory de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

