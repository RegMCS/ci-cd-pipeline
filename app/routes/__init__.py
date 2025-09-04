"""
Routes package
Exports all API routers
"""

from fastapi import APIRouter
from .portfolio import api_router as portfolio_router
from .portfolio_analysis import router as portfolio_analysis_router

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(portfolio_router)
api_router.include_router(portfolio_analysis_router)

__all__ = ["api_router"]
