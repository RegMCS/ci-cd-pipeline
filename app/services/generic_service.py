"""
Generic service layer
Handles basic business logic and database operations
"""

import logging
from datetime import datetime
from typing import Any, Dict

from app.database.connection import get_db_connection, return_db_connection
from app.models.generic import HealthResponse

logger = logging.getLogger(__name__)


class GenericService:
    """Generic service for basic operations"""

    @staticmethod
    def health_check() -> HealthResponse:
        """
        Check the health status of the API and database

        Returns:
            HealthResponse: Health status information
        """
        try:
            # Test database connection
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return_db_connection(conn)

            return HealthResponse(
                status="healthy",
                database="connected",
                timestamp=datetime.utcnow().isoformat(),
            )

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthResponse(
                status="unhealthy",
                database="disconnected",
                timestamp=datetime.utcnow().isoformat(),
                error=str(e),
            )

    @staticmethod
    def get_database_info() -> Dict[str, Any]:
        """
        Get basic database information

        Returns:
            Dict: Database information
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get database version
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]

            # Get current time
            cursor.execute("SELECT NOW()")
            current_time = cursor.fetchone()[0]

            cursor.close()
            return_db_connection(conn)

            return {
                "version": version,
                "current_time": current_time.isoformat(),
                "status": "connected",
            }

        except Exception as e:
            logger.error(f"Database info retrieval failed: {e}")
            return {"status": "disconnected", "error": str(e)}
