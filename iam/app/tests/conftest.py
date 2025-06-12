from app.core.config import settings as test_settings_reloaded
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SQLModel
from app.core.config import settings

# Override settings to use the test database
settings.TESTING = True

# Reload settings to ensure the test database is being used
SQLALCHEMY_DATABASE_URL = str(test_settings_reloaded.SQLALCHEMY_DATABASE_URI)

# Create a test engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session')
def db_engine():
    """Fixture to yield the SQLAlchemy engine for the test database."""
    print(f'\nUsing test database: {SQLALCHEMY_DATABASE_URL}')
    return engine


@pytest.fixture(scope='module')
def db_session(db_engine):
    """
    Fixture that provides a fresh database session for each test module.
    It creates all tables before each test module and drops them afterwards.
    """
    # Create tables
    SQLModel.metadata.create_all(engine)

    # Establish a connection and begin a transaction
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    # Override the app's dependency to use the test session
    # def override_get_db():
    #     try:
    #         yield session
    #     finally:
    #         session.close()

    # app.dependency_overrides[get_db] = override_get_db

    yield session

    # Rollback the transaction and close the session and connection
    session.close()
    transaction.rollback()
    connection.close()

    # Drop tables after each test function
    SQLModel.metadata.drop_all(bind=db_engine)


@pytest.fixture(scope='module')
def client(db_session):
    """
    Fixture that provides a TestClient for the FastAPI app.
    It uses the `db_session` fixture, so it will operate with the test database.
    """
    with TestClient(app) as c:
        yield c
