#Importante: Este archivo maneja la creación y gestión de sesiones de base de datos usando SQLAlchemy.
from sqlalchemy.orm import sessionmaker, Session

from src.Infrastructure.database.connection import engine

# Factory de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

#Crea y retorna una sesión de base de datos
def get_session() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
