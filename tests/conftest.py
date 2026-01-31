#Configuracion de pytest para pruebas con base de datos SQLite asíncrona temporal
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
from src.Infrastructure.database.models import Base
from src.Infrastructure.database.dependencies import get_db
from src.main import app

# Fixture para crear una base de datos SQLite asíncrona temporal para cada función de prueba
@pytest.fixture(scope="function")
async def test_db(tmp_path):
    db_path = tmp_path / "test_func.db"
    database_url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(database_url, connect_args={"check_same_thread": False}, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session():
        async with AsyncSessionLocal() as session:
            yield session

    try:
        yield AsyncSessionLocal
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

# Fixture para crear un motor de base de datos SQLite asíncrona temporal para cada función de prueba
@pytest.fixture(scope="function")
async def test_db_engine(tmp_path):
    db_path = tmp_path / "engine.db"
    database_url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(database_url, connect_args={"check_same_thread": False}, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

# Fixture para crear un cliente de prueba AsyncClient con una base de datos SQLite asíncrona temporal
@pytest.fixture(scope="function")
async def client_with_db(tmp_path):
    test_db_path = tmp_path / "test.db"
    database_url = f"sqlite+aiosqlite:///{test_db_path}"

    engine = create_async_engine(database_url, connect_args={"check_same_thread": False}, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()