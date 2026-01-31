# Dependencia para la gestión de la sesión de la base de datos (async)
from src.Infrastructure.database.session import SessionLocal


async def get_db():
    async with SessionLocal() as session:
        yield session
