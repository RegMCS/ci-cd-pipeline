"""
Generic API routes
Handles HTTP endpoints for basic operations
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter

from app.models.generic import HealthResponse
from app.services.generic_service import GenericService

# Create router for generic endpoints
api_router = APIRouter(prefix="/api/v1", tags=["api"])


@api_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the API and database connection",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"},
    },
)
def health_check() -> HealthResponse:
    """
    Health check endpoint

    Returns:
        HealthResponse: Health status information
    """
    return GenericService.health_check()


@api_router.get(
    "/status",
    response_model=Dict[str, Any],
    summary="API Status",
    description="Get basic API status information",
    responses={200: {"description": "API status retrieved successfully"}},
)
def get_status() -> Dict[str, Any]:
    """
    Get API status information

    Returns:
        Dict: API status data
    """
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
    }
