"""
Portfolio Price API
Main application entry point with proper separation of concerns
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import close_db_pool, initialize_db_pool
from app.routes import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Portfolio Price API",
    description="A FastAPI application for portfolio price management with PostgreSQL database integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router)


# Root endpoint
@app.get("/", tags=["root"])
def read_root():
    """Root endpoint with basic API information"""
    return {
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
            "tracking_error": "/api/v1/tracking-error"
        }
    }


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Portfolio Price API...")
    try:
        initialize_db_pool()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down Portfolio Price API...")
    try:
        close_db_pool()
        logger.info("Application shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
