"""
Test data fixtures for Portfolio Analysis API E2E tests
"""

from datetime import date

# Portfolio test data
PORTFOLIO_TEST_DATA = {
    "valid_portfolio_ids": ["TEST_001", "TEST_002", "BENCHMARK_001"],
    "valid_dates": ["2024-01-01", "2024-01-15", "2024-01-31"],
    "invalid_dates": ["invalid-date", "2024-13-01", "2024-01-32"],
    "date_ranges": {
        "january_2024": {"start": "2024-01-01", "end": "2024-01-31"},
        "q1_2024": {"start": "2024-01-01", "end": "2024-03-31"},
        "invalid_range": {"start": "2024-01-31", "end": "2024-01-01"},
    },
}

# Expected error responses for unimplemented endpoints
ERROR_RESPONSES = {
    "not_implemented": {
        "status_code": 500,
        "detail_contains": "not implemented",
    },
    "validation_error": {
        "status_code": 422,
        "detail_contains": "validation error",
    },
    "bad_request": {
        "status_code": 400,
        "detail_contains": "bad request",
    },
}

# Test cases for portfolio endpoints
PORTFOLIO_TEST_CASES = {
    "portfolio_price": [
        {
            "params": {"portfolioId": "TEST_001", "date": "2024-01-15"},
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
        {
            "params": {"portfolioId": "TEST_001"},
            "expected_status": 422,
            "description": "Missing required date parameter",
        },
        {
            "params": {"portfolioId": "TEST_001", "date": "invalid-date"},
            "expected_status": 422,
            "description": "Invalid date format",
        },
    ],
    "daily_return": [
        {
            "params": {"portfolioId": "TEST_001", "date": "2024-01-15"},
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
        {
            "params": {"portfolioId": "TEST_001"},
            "expected_status": 422,
            "description": "Missing required date parameter",
        },
    ],
    "cumulative_price": [
        {
            "params": {
                "portfolioId": "TEST_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
        {
            "params": {
                "portfolioId": "TEST_001",
                "startDate": "2024-01-31",
                "endDate": "2024-01-01",
            },
            "expected_status": 400,
            "description": "Start date after end date",
        },
    ],
    "daily_volatility": [
        {
            "params": {
                "portfolioId": "TEST_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
    ],
    "correlation": [
        {
            "params": {
                "portfolioId1": "TEST_001",
                "portfolioId2": "TEST_002",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
        {
            "params": {
                "portfolioId1": "TEST_001",
                "portfolioId2": "TEST_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
            "expected_status": 400,
            "description": "Same portfolio IDs",
        },
    ],
    "tracking_error": [
        {
            "params": {
                "portfolioId": "TEST_001",
                "benchmarkId": "BENCHMARK_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
            "expected_status": 500,
            "description": "Valid parameters, not implemented",
        },
    ],
}

# Mock response data for when endpoints are implemented
MOCK_RESPONSES = {
    "portfolio_price": {
        "portfolioId": "TEST_001",
        "date": "2024-01-15",
        "price": 1000.50,
    },
    "daily_return": {
        "portfolioId": "TEST_001",
        "date": "2024-01-15",
        "return": 0.025,
    },
    "cumulative_price": {
        "portfolioId": "TEST_001",
        "cumulativePrices": [
            {"date": "2024-01-01", "cumulativePrice": 1000.0},
            {"date": "2024-01-02", "cumulativePrice": 1002.5},
            {"date": "2024-01-03", "cumulativePrice": 1005.0},
        ],
    },
    "daily_volatility": {
        "portfolioId": "TEST_001",
        "volatility": 0.15,
    },
    "correlation": {
        "portfolioId1": "TEST_001",
        "portfolioId2": "TEST_002",
        "correlation": 0.75,
    },
    "tracking_error": {
        "portfolioId": "TEST_001",
        "benchmarkId": "BENCHMARK_001",
        "trackingError": 0.08,
    },
}

# API endpoint configurations
API_ENDPOINTS = {
    "portfolio_price": "/api/v1/portfolio-price",
    "daily_return": "/api/v1/daily-return",
    "cumulative_price": "/api/v1/cumulative-price",
    "daily_volatility": "/api/v1/daily-volatility",
    "correlation": "/api/v1/correlation",
    "tracking_error": "/api/v1/tracking-error",
}

# Root endpoint expected response
ROOT_RESPONSE = {
    "message": "Portfolio Price API",
    "version": "1.0.0",
    "docs": "/docs",
    "health": "/api/v1/health",
    "status": "/api/v1/status",
    "endpoints": {
        "portfolio_price": "/api/v1/portfolio-price",
        "daily_return": "/api/v1/daily-return",
        "cumulative_price": "/api/v1/cumulative-price",
        "daily_volatility": "/api/v1/daily-volatility",
        "correlation": "/api/v1/correlation",
        "tracking_error": "/api/v1/tracking-error",
    },
}
