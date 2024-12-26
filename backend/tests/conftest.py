import os
import pytest
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import app
from db.base import Base
from db.session import get_db

from core.directory import directory

SQLALCHEMY_DATABASE_URL = f"sqlite:///{directory.base_dir}/tests/test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)  # Create the tables.


@pytest.fixture(scope="session", autouse=True)
def cleanup_database(request: pytest.FixtureRequest) -> None:
    """Cleanup the test database after tests have run."""

    def remove_test_db() -> None:
        # Ensure that connections and sessions are closed
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

        # Remove the test database file
        if os.path.exists(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")):
            os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))

    request.addfinalizer(remove_test_db)


@pytest.fixture(scope="function")
def db_session(request: pytest.FixtureRequest) -> Generator[Session, None, None]:
    """Create a new database session with a rollback at the end of the test."""

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    def teardown() -> None:
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    yield session


@pytest.fixture(scope="function")
def test_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_func_logger(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Dynamically mock the logger's error method for testing."""

    def _mock_func_logger(logger_path: str) -> MagicMock:
        """Create a mock for the specified logger path."""
        mock = MagicMock()
        monkeypatch.setattr(logger_path, mock)
        return mock

    return _mock_func_logger


@pytest.fixture
def mock_file_methods() -> MagicMock:
    """Fixture to mock file input."""

    mock_path = Path("/fake/path")

    mock_file = MagicMock()
    mock_file.filename = "test_image.png"
    mock_file.file.read.return_value = (
        b"\x00\x00\x00\x00"  # Simulate binary file content
    )

    return mock_path, mock_file
