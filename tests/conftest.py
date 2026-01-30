"""
Pytest configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.Infrastructure.database.models import Base
from src.Infrastructure.database.connection import get_db
from src.main import app


@pytest.fixture(scope="function")
def test_db():
    """
    Creates a test database for each test function.
    Uses an in-memory SQLite database.
    """
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db_engine():
    """
    Creates a test database engine.
    Useful for testing at the engine level.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client_with_db(tmp_path):
    """
    Creates a TestClient with a temporary SQLite database for testing.
    """
    # Create a temporary database file
    test_db_path = tmp_path / "test.db"
    test_db_url = f"sqlite:///{test_db_path}"
    
    # Create test engine and tables
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=test_engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override the dependency
    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db
    
    # Create client
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    app.dependency_overrides.clear()
    test_engine.dispose()