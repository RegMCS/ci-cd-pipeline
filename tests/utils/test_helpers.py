"""
Test utility functions and helpers
"""
import json
from typing import Dict, Any, Optional
from datetime import datetime, date

def assert_valid_portfolio_response(response_data: Dict[str, Any]) -> None:
    """Assert that a portfolio response has the correct structure and types"""
    assert isinstance(response_data, dict)
    assert "portfolioId" in response_data
    assert "date" in response_data
    assert "price" in response_data
    
    assert isinstance(response_data["portfolioId"], str)
    assert isinstance(response_data["date"], str)
    assert isinstance(response_data["price"], (int, float))
    
    # Validate date format
    try:
        datetime.strptime(response_data["date"], "%Y-%m-%d")
    except ValueError:
        raise AssertionError(f"Invalid date format: {response_data['date']}")

def assert_error_response(response_data: Dict[str, Any], expected_status: int) -> None:
    """Assert that an error response has the correct structure"""
    assert isinstance(response_data, dict)
    assert "detail" in response_data
    assert isinstance(response_data["detail"], str)
    assert len(response_data["detail"]) > 0

def create_test_portfolio_data(
    portfolio_id: str = "TEST_PORTFOLIO",
    price_date: str = "2024-01-15",
    price: float = 1000.0
) -> Dict[str, Any]:
    """Create test portfolio data"""
    return {
        "portfolioId": portfolio_id,
        "date": price_date,
        "price": price
    }

def create_mock_db_result(
    portfolio_id: str = "TEST_PORTFOLIO",
    price_date: date = date(2024, 1, 15),
    price: float = 1000.0
) -> Dict[str, Any]:
    """Create mock database result"""
    return {
        "portfolio_id": portfolio_id,
        "price_date": price_date,
        "price": price
    }

def validate_api_response_structure(response_data: Dict[str, Any], expected_keys: list) -> None:
    """Validate that API response contains expected keys"""
    for key in expected_keys:
        assert key in response_data, f"Missing key: {key}"

def format_test_case_name(test_case: Dict[str, Any]) -> str:
    """Format test case name for better readability"""
    portfolio_id = test_case.get("portfolioId", "unknown")
    date = test_case.get("date", "unknown")
    return f"portfolio_{portfolio_id}_date_{date}"

def create_health_check_assertions(response_data: Dict[str, Any]) -> None:
    """Assert health check response structure"""
    assert "status" in response_data
    assert "database" in response_data
    assert "timestamp" in response_data
    
    assert response_data["status"] in ["healthy", "unhealthy"]
    assert response_data["database"] in ["connected", "disconnected"]
    
    # Validate timestamp format
    try:
        datetime.fromisoformat(response_data["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        raise AssertionError(f"Invalid timestamp format: {response_data['timestamp']}")
