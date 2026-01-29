"""
Pytest configuration and fixtures.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Infrastructure.database.models import Base


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