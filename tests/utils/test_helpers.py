"""
Test utility functions and helpers for Portfolio Analysis API
"""

from datetime import date, datetime
from typing import Any, Dict, List


def assert_portfolio_price_response(response_data: Dict[str, Any]) -> None:
    """Assert portfolio price response structure"""
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


def assert_daily_return_response(response_data: Dict[str, Any]) -> None:
    """Assert daily return response structure"""
    assert isinstance(response_data, dict)
    assert "portfolioId" in response_data
    assert "date" in response_data
    assert "return" in response_data

    assert isinstance(response_data["portfolioId"], str)
    assert isinstance(response_data["date"], str)
    assert isinstance(response_data["return"], (int, float))


def assert_cumulative_price_response(response_data: Dict[str, Any]) -> None:
    """Assert cumulative price response structure"""
    assert isinstance(response_data, dict)
    assert "portfolioId" in response_data
    assert "cumulativePrices" in response_data

    assert isinstance(response_data["portfolioId"], str)
    assert isinstance(response_data["cumulativePrices"], list)

    # Validate cumulative price items
    for item in response_data["cumulativePrices"]:
        assert "date" in item
        assert "cumulativePrice" in item
        assert isinstance(item["date"], str)
        assert isinstance(item["cumulativePrice"], (int, float))


def assert_volatility_response(response_data: Dict[str, Any]) -> None:
    """Assert volatility response structure"""
    assert isinstance(response_data, dict)
    assert "portfolioId" in response_data
    assert "volatility" in response_data

    assert isinstance(response_data["portfolioId"], str)
    assert isinstance(response_data["volatility"], (int, float))


def assert_correlation_response(response_data: Dict[str, Any]) -> None:
    """Assert correlation response structure"""
    assert isinstance(response_data, dict)
    assert "portfolioId1" in response_data
    assert "portfolioId2" in response_data
    assert "correlation" in response_data

    assert isinstance(response_data["portfolioId1"], str)
    assert isinstance(response_data["portfolioId2"], str)
    assert isinstance(response_data["correlation"], (int, float))


def assert_tracking_error_response(response_data: Dict[str, Any]) -> None:
    """Assert tracking error response structure"""
    assert isinstance(response_data, dict)
    assert "portfolioId" in response_data
    assert "benchmarkId" in response_data
    assert "trackingError" in response_data

    assert isinstance(response_data["portfolioId"], str)
    assert isinstance(response_data["benchmarkId"], str)
    assert isinstance(response_data["trackingError"], (int, float))


def assert_error_response(response_data: Dict[str, Any]) -> None:
    """Assert error response structure"""
    assert isinstance(response_data, dict)
    assert "detail" in response_data
    assert isinstance(response_data["detail"], str)
    assert len(response_data["detail"]) > 0


def create_portfolio_test_data(
    portfolio_id: str = "TEST_001",
    price_date: str = "2024-01-15",
    price: float = 1000.0,
) -> Dict[str, Any]:
    """Create test portfolio data"""
    return {"portfolioId": portfolio_id, "date": price_date, "price": price}


def create_daily_return_test_data(
    portfolio_id: str = "TEST_001",
    return_date: str = "2024-01-15",
    return_value: float = 0.05,
) -> Dict[str, Any]:
    """Create test daily return data"""
    return {"portfolioId": portfolio_id, "date": return_date, "return": return_value}


def create_cumulative_price_test_data(
    portfolio_id: str = "TEST_001",
    start_date: str = "2024-01-01",
    end_date: str = "2024-01-31",
) -> Dict[str, Any]:
    """Create test cumulative price data"""
    return {
        "portfolioId": portfolio_id,
        "startDate": start_date,
        "endDate": end_date,
    }


def create_volatility_test_data(
    portfolio_id: str = "TEST_001",
    start_date: str = "2024-01-01",
    end_date: str = "2024-01-31",
) -> Dict[str, Any]:
    """Create test volatility data"""
    return {
        "portfolioId": portfolio_id,
        "startDate": start_date,
        "endDate": end_date,
    }


def create_correlation_test_data(
    portfolio_id1: str = "TEST_001",
    portfolio_id2: str = "TEST_002",
    start_date: str = "2024-01-01",
    end_date: str = "2024-01-31",
) -> Dict[str, Any]:
    """Create test correlation data"""
    return {
        "portfolioId1": portfolio_id1,
        "portfolioId2": portfolio_id2,
        "startDate": start_date,
        "endDate": end_date,
    }


def create_tracking_error_test_data(
    portfolio_id: str = "TEST_001",
    benchmark_id: str = "BENCHMARK_001",
    start_date: str = "2024-01-01",
    end_date: str = "2024-01-31",
) -> Dict[str, Any]:
    """Create test tracking error data"""
    return {
        "portfolioId": portfolio_id,
        "benchmarkId": benchmark_id,
        "startDate": start_date,
        "endDate": end_date,
    }


def validate_date_range(start_date: str, end_date: str) -> bool:
    """Validate that start date is before end date"""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start < end
    except ValueError:
        return False


def format_test_case_name(endpoint: str, params: Dict[str, Any]) -> str:
    """Format test case name for better readability"""
    portfolio_id = params.get("portfolioId", params.get("portfolioId1", "unknown"))
    return f"{endpoint}_portfolio_{portfolio_id}"
