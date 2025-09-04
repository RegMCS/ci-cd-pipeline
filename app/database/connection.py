"""
Database connection pool module
Handles database connection pooling and management
"""

import atexit
import logging
from typing import Optional

import psycopg2
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from psycopg2_pool import ThreadSafeConnectionPool

from app.config.database import get_pool_config

logger = logging.getLogger(__name__)


class DatabasePool:
    """Database connection pool manager"""

    def __init__(self) -> None:
        self._pool: Optional[ThreadSafeConnectionPool] = None
        self._pool_config = get_pool_config()

    def initialize(self) -> None:
        """Initialize the database connection pool"""
        try:
            # Separate connection parameters from pool parameters
            connection_params = {
                "host": self._pool_config["host"],
                "port": self._pool_config["port"],
                "database": self._pool_config["database"],
                "user": self._pool_config["user"],
                "password": self._pool_config["password"],
            }
            
            pool_params = {
                "minconn": self._pool_config["minconn"],
                "maxconn": self._pool_config["maxconn"],
            }
            
            self._pool = ThreadSafeConnectionPool(
                connection_factory=lambda: psycopg2.connect(**connection_params),
                **pool_params
            )
            min_conn = self._pool_config["minconn"]
            max_conn = self._pool_config["maxconn"]
            logger.info(
                f"Database connection pool initialized with "
                f"{min_conn}-{max_conn} connections"
            )
        except psycopg2.Error as e:
            logger.error(f"Failed to create connection pool: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Database connection pool initialization failed: {str(e)}",
            )

    def get_connection(self) -> psycopg2.extensions.connection:
        """Get a connection from the pool"""
        if self._pool is None:
            self.initialize()
            if self._pool is None:
                raise HTTPException(
                    status_code=500, detail="Database connection pool not initialized"
                )

        try:
            conn = self._pool.getconn()
            if conn is None:
                raise HTTPException(
                    status_code=503, detail="No available database connections in pool"
                )
            return conn
        except psycopg2.Error as e:
            logger.error(f"Failed to get connection from pool: {e}")
            raise HTTPException(
                status_code=500, detail=f"Database connection failed: {str(e)}"
            )

    def return_connection(self, conn: psycopg2.extensions.connection) -> None:
        """Return a connection to the pool"""
        if self._pool and conn:
            try:
                self._pool.putconn(conn)
            except psycopg2.Error as e:
                logger.error(f"Error returning connection to pool: {e}")

    def close_all(self) -> None:
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("Database connection pool closed")

    def get_cursor(
        self,
        conn: psycopg2.extensions.connection,
        cursor_factory: type = RealDictCursor,
    ) -> psycopg2.extras.RealDictCursor:
        """Get a cursor from a connection"""
        return conn.cursor(cursor_factory=cursor_factory)


# Global database pool instance
db_pool = DatabasePool()

# Register cleanup function
atexit.register(db_pool.close_all)


def get_db_connection() -> psycopg2.extensions.connection:
    """Get a database connection from the pool"""
    return db_pool.get_connection()


def return_db_connection(conn: psycopg2.extensions.connection) -> None:
    """Return a database connection to the pool"""
    return db_pool.return_connection(conn)


def get_db_cursor(
    conn: psycopg2.extensions.connection, cursor_factory: type = RealDictCursor
) -> psycopg2.extras.RealDictCursor:
    """Get a database cursor"""
    return db_pool.get_cursor(conn, cursor_factory)


def initialize_db_pool() -> None:
    """Initialize the database pool"""
    return db_pool.initialize()


def close_db_pool() -> None:
    """Close the database pool"""
    return db_pool.close_all()
