"""
Pytest configuration and fixtures
"""

from unittest.mock import MagicMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(scope="session")
def async_client():
    """Create an async HTTP client for testing."""
    return httpx.AsyncClient(base_url="http://localhost:8000")


@pytest.fixture(scope="function")
def mock_db_connection():
    """Mock database connection for testing without real DB."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture(scope="function")
def sample_data():
    """Sample data for testing."""
    return {
        "id": 1,
        "name": "Test Item",
        "description": "Test description",
        "created_at": "2024-01-15T10:30:00Z",
    }


@pytest.fixture(scope="function")
def sample_response():
    """Sample response for testing."""
    return {
        "status": "success",
        "message": "Operation completed",
        "timestamp": "2024-01-15T10:30:00Z",
    }


@pytest.fixture(scope="function")
def mock_database_pool():
    """Mock the database pool for testing."""
    with patch("app.database.connection.db_pool") as mock_pool:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_pool.get_connection.return_value = mock_conn
        mock_pool.return_connection.return_value = None
        mock_pool.get_cursor.return_value = mock_cursor
        yield mock_pool, mock_conn, mock_cursor


@pytest.fixture(autouse=True)
def mock_db_operations():
    """Mock database operations to avoid real DB connections during tests."""
    with patch("app.database.connection.initialize_db_pool"), patch(
        "app.database.connection.close_db_pool"
    ):
        yield
