#Importante: Este archivo gestiona la conexión a la base de datos utilizando SQLAlchemy.
from sqlalchemy import create_engine

from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.models import Base


#Crea el engine de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite ya que es single-threaded y SQLAlchemy usa múltiples hilos
)


#Crea las tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)
