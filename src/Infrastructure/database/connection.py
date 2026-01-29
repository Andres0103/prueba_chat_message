"""
Infrastructure Layer - Database Connection
Maneja la conexión y sesiones de SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config.settings import settings
from .models import Base


# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Crea todas las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Dependency para obtener una sesión de base de datos.
    Se usa en los endpoints de FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()