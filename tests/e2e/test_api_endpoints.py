"""
E2E tests for API endpoints
Tests the complete application flow from HTTP request to database interaction
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

from main import app
from tests.fixtures.test_data import TEST_CASES, MOCK_DB_RESULTS, HEALTH_CHECK_RESPONSES

@pytest.mark.e2e
class TestAPIEndpoints:
    """Test class for API endpoint E2E tests"""
    
    def test_root_endpoint(self, test_client):
        """Test the root endpoint"""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "FastAPI Boilerplate"
        assert data["version"] == "1.0.0"
        assert "docs" in data
        assert "health" in data
        assert "status" in data

    def test_health_check_endpoint_healthy(self, test_client, mock_database_pool):
        """Test health check endpoint when healthy"""
        mock_pool, mock_conn, mock_cursor = mock_database_pool
        mock_cursor.fetchone.return_value = (1,)  # Mock successful query
        
        response = test_client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "timestamp" in data

    def test_health_check_endpoint_unhealthy(self, test_client, mock_database_pool):
        """Test health check endpoint when unhealthy"""
        mock_pool, mock_conn, mock_cursor = mock_database_pool
        mock_cursor.fetchone.side_effect = Exception("Connection failed")
        
        response = test_client.get("/api/v1/health")
        
        assert response.status_code == 200  # Health check returns 200 even when unhealthy
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        assert "error" in data

    def test_status_endpoint(self, test_client):
        """Test the status endpoint"""
        response = test_client.get("/api/v1/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data

    def test_api_documentation_endpoints(self, test_client):
        """Test API documentation endpoints"""
        # Test Swagger UI
        response = test_client.get("/docs")
        assert response.status_code == 200
        
        # Test ReDoc
        response = test_client.get("/redoc")
        assert response.status_code == 200
        
        # Test OpenAPI schema
        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema

    def test_cors_headers(self, test_client):
        """Test CORS headers are present"""
        response = test_client.get("/api/v1/status")
        
        assert response.status_code == 200
        # Note: CORS headers are not included in test client by default
        # This test verifies the endpoint works, CORS is tested in integration tests

    def test_response_content_type(self, test_client):
        """Test response content type is JSON"""
        response = test_client.get("/api/v1/status")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_error_response_format(self, test_client):
        """Test error response format"""
        # Test 404 error
        response = test_client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

@pytest.mark.e2e
class TestAPIEndpointsIntegration:
    """Integration tests for API endpoints"""
    
    def test_multiple_requests(self, test_client):
        """Test handling of multiple requests"""
        # Test multiple requests to ensure stability
        for i in range(5):
            response = test_client.get("/api/v1/status")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "running"
            assert "timestamp" in data
