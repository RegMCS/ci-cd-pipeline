"""
Test data fixtures for E2E tests
"""

from datetime import date

# Sample test data
SAMPLE_DATA = [
    {
        "id": 1,
        "name": "Test Item 1",
        "description": "First test item",
        "created_at": date(2024, 1, 15),
        "updated_at": date(2024, 1, 15),
    },
    {
        "id": 2,
        "name": "Test Item 2",
        "description": "Second test item",
        "created_at": date(2024, 1, 15),
        "updated_at": date(2024, 1, 15),
    },
]

# Expected API responses
EXPECTED_RESPONSES = {
    "health_healthy": {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2024-01-15T10:30:00Z",
    },
    "health_unhealthy": {
        "status": "unhealthy",
        "database": "disconnected",
        "error": "Connection failed",
        "timestamp": "2024-01-15T10:30:00Z",
    },
    "status_response": {
        "status": "running",
        "timestamp": "2024-01-15T10:30:00Z",
        "version": "1.0.0",
    },
}

# Test cases for different scenarios
TEST_CASES = {
    "health_checks": [
        {
            "expected_status": 200,
            "expected_response": EXPECTED_RESPONSES["health_healthy"],
        }
    ],
    "status_checks": [
        {
            "expected_status": 200,
            "expected_response": EXPECTED_RESPONSES["status_response"],
        }
    ],
}

# Database query results for mocking
MOCK_DB_RESULTS = {
    "health_check": {"status": "connected", "version": "PostgreSQL 15.0"},
    "empty_result": None,
    "error_result": Exception("Database connection failed"),
}

# Health check responses
HEALTH_CHECK_RESPONSES = {
    "healthy": {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2024-01-15T10:30:00",
    },
    "unhealthy": {
        "status": "unhealthy",
        "database": "disconnected",
        "error": "Connection failed",
        "timestamp": "2024-01-15T10:30:00",
    },
}
