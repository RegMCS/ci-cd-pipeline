"""
Portfolio analysis models
Pydantic models for portfolio-related API responses
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class PortfolioPriceResponse(BaseModel):
    """Response model for portfolio price endpoint"""
    portfolioId: str = Field(..., description="Portfolio identifier")
    date: date = Field(..., description="Date of the price")
    price: float = Field(..., description="Portfolio price on the given date")


class DailyReturnResponse(BaseModel):
    """Response model for daily return endpoint"""
    portfolioId: str = Field(..., description="Portfolio identifier")
    date: date = Field(..., description="Date of the return")
    return_value: float = Field(..., alias="return", description="Daily return percentage")
    
    class Config:
        populate_by_name = True


class CumulativePriceItem(BaseModel):
    """Individual item in cumulative price series"""
    date: date = Field(..., description="Date")
    cumulativePrice: float = Field(..., description="Cumulative price on this date")


class CumulativePriceResponse(BaseModel):
    """Response model for cumulative price endpoint"""
    portfolioId: str = Field(..., description="Portfolio identifier")
    cumulativePrices: List[CumulativePriceItem] = Field(..., description="List of cumulative prices")


class DailyVolatilityResponse(BaseModel):
    """Response model for daily volatility endpoint"""
    portfolioId: str = Field(..., description="Portfolio identifier")
    volatility: float = Field(..., description="Volatility value")


class CorrelationResponse(BaseModel):
    """Response model for correlation endpoint"""
    portfolioId1: str = Field(..., description="First portfolio identifier")
    portfolioId2: str = Field(..., description="Second portfolio identifier")
    correlation: float = Field(..., description="Correlation coefficient")


class TrackingErrorResponse(BaseModel):
    """Response model for tracking error endpoint"""
    portfolioId: str = Field(..., description="Portfolio identifier")
    benchmarkId: str = Field(..., description="Benchmark identifier")
    trackingError: float = Field(..., description="Tracking error value")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
