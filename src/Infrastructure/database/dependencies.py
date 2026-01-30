# src/Infrastructure/database/dependencies.py
from src.Infrastructure.database.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
