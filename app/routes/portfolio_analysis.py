"""
Portfolio analysis API routes
FastAPI endpoints for portfolio calculations
"""

from datetime import date
from fastapi import APIRouter, HTTPException, Query
from typing import Union

from app.models.portfolio import (
    PortfolioPriceResponse,
    DailyReturnResponse,
    CumulativePriceResponse,
    DailyVolatilityResponse,
    CorrelationResponse,
    TrackingErrorResponse,
    ErrorResponse,
)
from app.services.portfolio_service import portfolio_service

router = APIRouter(prefix="/api/v1", tags=["Portfolio Analysis"])


@router.get(
    "/portfolio-price",
    response_model=PortfolioPriceResponse,
    summary="Get portfolio price on a specific date",
    description="Retrieve the price of a portfolio for a given date",
)
async def get_portfolio_price(
    portfolioId: str = Query(..., description="Portfolio identifier"),
    date: date = Query(..., description="Date for which to get the price"),
) -> PortfolioPriceResponse:
    """Get portfolio price for a specific date"""
    try:
        return portfolio_service.get_portfolio_price(portfolioId, date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/daily-return",
    response_model=DailyReturnResponse,
    summary="Get daily return for a portfolio",
    description="Calculate the daily return percentage for a portfolio on a specific date",
)
async def get_daily_return(
    portfolioId: str = Query(..., description="Portfolio identifier"),
    date: date = Query(..., description="Date for which to calculate the return"),
) -> DailyReturnResponse:
    """Get daily return for a portfolio"""
    try:
        return portfolio_service.get_daily_return(portfolioId, date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/cumulative-price",
    response_model=CumulativePriceResponse,
    summary="Get cumulative portfolio price from a base date",
    description="Get a series of cumulative prices for a portfolio over a date range",
)
async def get_cumulative_price(
    portfolioId: str = Query(..., description="Portfolio identifier"),
    startDate: date = Query(
        ..., description="Start date for the cumulative price series"
    ),
    endDate: date = Query(..., description="End date for the cumulative price series"),
) -> CumulativePriceResponse:
    """Get cumulative price series for a portfolio"""
    try:
        if startDate > endDate:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

        return portfolio_service.get_cumulative_prices(portfolioId, startDate, endDate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/daily-volatility",
    response_model=DailyVolatilityResponse,
    summary="Compute volatility over a date range",
    description="Calculate the daily volatility (standard deviation of returns) for a portfolio over a date range",
)
async def get_daily_volatility(
    portfolioId: str = Query(..., description="Portfolio identifier"),
    startDate: date = Query(..., description="Start date for volatility calculation"),
    endDate: date = Query(..., description="End date for volatility calculation"),
) -> DailyVolatilityResponse:
    """Calculate daily volatility for a portfolio"""
    try:
        if startDate > endDate:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

        return portfolio_service.get_daily_volatility(portfolioId, startDate, endDate)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/correlation",
    response_model=CorrelationResponse,
    summary="Compute correlation between two portfolios",
    description="Calculate the correlation coefficient between two portfolios over a date range",
)
async def get_correlation(
    portfolioId1: str = Query(..., description="First portfolio identifier"),
    portfolioId2: str = Query(..., description="Second portfolio identifier"),
    startDate: date = Query(..., description="Start date for correlation calculation"),
    endDate: date = Query(..., description="End date for correlation calculation"),
) -> CorrelationResponse:
    """Calculate correlation between two portfolios"""
    try:
        if startDate > endDate:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

        if portfolioId1 == portfolioId2:
            raise HTTPException(
                status_code=400, detail="Portfolio IDs must be different"
            )

        return portfolio_service.get_correlation(
            portfolioId1, portfolioId2, startDate, endDate
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/tracking-error",
    response_model=TrackingErrorResponse,
    summary="Compute tracking error against benchmark",
    description="Calculate the tracking error (standard deviation of excess returns) between a portfolio and its benchmark",
)
async def get_tracking_error(
    portfolioId: str = Query(..., description="Portfolio identifier"),
    benchmarkId: str = Query(..., description="Benchmark identifier"),
    startDate: date = Query(
        ..., description="Start date for tracking error calculation"
    ),
    endDate: date = Query(..., description="End date for tracking error calculation"),
) -> TrackingErrorResponse:
    """Calculate tracking error against benchmark"""
    try:
        if startDate > endDate:
            raise HTTPException(
                status_code=400, detail="Start date must be before end date"
            )

        return portfolio_service.get_tracking_error(
            portfolioId, benchmarkId, startDate, endDate
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
