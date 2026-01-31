#Dependencia para la gestión de la sesión de la base de datos
from src.Infrastructure.database.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
