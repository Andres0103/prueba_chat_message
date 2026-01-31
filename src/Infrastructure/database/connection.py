#Importante: Este archivo gestiona la conexión a la base de datos utilizando SQLAlchemy.
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.models import Base


# Convertir DATABASE_URL a formato async si es sqlite
database_url = settings.DATABASE_URL
if database_url.startswith("sqlite:") and not database_url.startswith("sqlite+"):
    async_database_url = database_url.replace("sqlite:", "sqlite+aiosqlite:", 1)
else:
    async_database_url = database_url


# Crea el engine asíncrono de la base de datos
engine: AsyncEngine = create_async_engine(async_database_url, echo=False, future=True)


# Factory de sesiones asíncronas
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

