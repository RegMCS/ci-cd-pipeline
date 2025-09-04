"""
E2E tests for Portfolio Analysis API endpoints
Tests the complete application flow for portfolio analysis endpoints
"""

import pytest
from datetime import date


@pytest.mark.e2e
class TestPortfolioAnalysisEndpoints:
    """Test class for Portfolio Analysis API endpoint E2E tests"""

    def test_root_endpoint(self, test_client):
        """Test the root endpoint shows portfolio endpoints"""
        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Portfolio Price API"
        assert "endpoints" in data
        assert "portfolio_price" in data["endpoints"]
        assert "daily_return" in data["endpoints"]

    def test_portfolio_price_endpoint(self, test_client):
        """Test portfolio price endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/portfolio-price",
            params={"portfolioId": "TEST_001", "date": "2024-01-15"},
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_daily_return_endpoint(self, test_client):
        """Test daily return endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/daily-return",
            params={"portfolioId": "TEST_001", "date": "2024-01-15"},
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_cumulative_price_endpoint(self, test_client):
        """Test cumulative price endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/cumulative-price",
            params={
                "portfolioId": "TEST_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_daily_volatility_endpoint(self, test_client):
        """Test daily volatility endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/daily-volatility",
            params={
                "portfolioId": "TEST_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_correlation_endpoint(self, test_client):
        """Test correlation endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/correlation",
            params={
                "portfolioId1": "TEST_001",
                "portfolioId2": "TEST_002",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_tracking_error_endpoint(self, test_client):
        """Test tracking error endpoint returns 500 (not implemented)"""
        response = test_client.get(
            "/api/v1/tracking-error",
            params={
                "portfolioId": "TEST_001",
                "benchmarkId": "BENCHMARK_001",
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
        )

        assert response.status_code == 500
        data = response.json()
        assert "not implemented" in data["detail"].lower()

    def test_portfolio_price_validation(self, test_client):
        """Test portfolio price endpoint validation"""
        # Test missing required parameters
        response = test_client.get("/api/v1/portfolio-price")
        assert response.status_code == 422  # Validation error

        # Test invalid date format
        response = test_client.get(
            "/api/v1/portfolio-price",
            params={"portfolioId": "TEST_001", "date": "invalid-date"},
        )
        assert response.status_code == 422  # Validation error

    def test_cumulative_price_validation(self, test_client):
        """Test cumulative price endpoint validation"""
        # Test start date after end date
        response = test_client.get(
            "/api/v1/cumulative-price",
            params={
                "portfolioId": "TEST_001",
                "startDate": "2024-01-31",
                "endDate": "2024-01-01",  # Invalid: start after end
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert "Start date must be before end date" in data["detail"]

    def test_correlation_validation(self, test_client):
        """Test correlation endpoint validation"""
        # Test same portfolio IDs
        response = test_client.get(
            "/api/v1/correlation",
            params={
                "portfolioId1": "TEST_001",
                "portfolioId2": "TEST_001",  # Same ID
                "startDate": "2024-01-01",
                "endDate": "2024-01-31",
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert "Portfolio IDs must be different" in data["detail"]

    def test_api_documentation(self, test_client):
        """Test API documentation is accessible"""
        response = test_client.get("/docs")
        assert response.status_code == 200

        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
        # Check that our portfolio endpoints are documented
        assert "/api/v1/portfolio-price" in schema["paths"]
        assert "/api/v1/daily-return" in schema["paths"]
        assert "/api/v1/cumulative-price" in schema["paths"]
        assert "/api/v1/daily-volatility" in schema["paths"]
        assert "/api/v1/correlation" in schema["paths"]
        assert "/api/v1/tracking-error" in schema["paths"]


@pytest.mark.e2e
class TestPortfolioAnalysisIntegration:
    """Integration tests for Portfolio Analysis endpoints"""

    def test_all_endpoints_respond(self, test_client):
        """Test that all portfolio endpoints respond (even if not implemented)"""
        endpoints = [
            (
                "/api/v1/portfolio-price",
                {"portfolioId": "TEST_001", "date": "2024-01-15"},
            ),
            ("/api/v1/daily-return", {"portfolioId": "TEST_001", "date": "2024-01-15"}),
            (
                "/api/v1/cumulative-price",
                {
                    "portfolioId": "TEST_001",
                    "startDate": "2024-01-01",
                    "endDate": "2024-01-31",
                },
            ),
            (
                "/api/v1/daily-volatility",
                {
                    "portfolioId": "TEST_001",
                    "startDate": "2024-01-01",
                    "endDate": "2024-01-31",
                },
            ),
            (
                "/api/v1/correlation",
                {
                    "portfolioId1": "TEST_001",
                    "portfolioId2": "TEST_002",
                    "startDate": "2024-01-01",
                    "endDate": "2024-01-31",
                },
            ),
            (
                "/api/v1/tracking-error",
                {
                    "portfolioId": "TEST_001",
                    "benchmarkId": "BENCHMARK_001",
                    "startDate": "2024-01-01",
                    "endDate": "2024-01-31",
                },
            ),
        ]

        for endpoint, params in endpoints:
            response = test_client.get(endpoint, params=params)
            # Should return 500 (not implemented) or 200 (if implemented)
            assert response.status_code in [200, 500]
            data = response.json()
            assert "detail" in data
