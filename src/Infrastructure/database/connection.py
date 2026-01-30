#Importante: Este archivo gestiona la conexión a la base de datos utilizando SQLAlchemy.
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.models import Base
from src.Infrastructure.database.session import SessionLocal


#Crea el engine de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite ya que es single-threaded y SQLAlchemy usa múltiples hilos
)


#Crea las tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

#Dependency para obtener una sesión de base de datos y se usa en los endpoints 
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()