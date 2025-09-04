"""
Database configuration module
Handles all database-related configuration settings
"""
import os
from typing import Dict, Any

# Default database connection configuration
DEFAULT_DB_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "port": 5432,
    "database": "app_db",
    "user": "app_user",
    "password": "your_password_here"
}

# Default connection pool configuration
DEFAULT_POOL_CONFIG: Dict[str, Any] = {
    "minconn": 1,
    "maxconn": 20,
    "host": DEFAULT_DB_CONFIG["host"],
    "port": DEFAULT_DB_CONFIG["port"],
    "database": DEFAULT_DB_CONFIG["database"],
    "user": DEFAULT_DB_CONFIG["user"],
    "password": DEFAULT_DB_CONFIG["password"]
}

# Environment-based configuration (for production)
def get_db_config() -> Dict[str, Any]:
    """Get database configuration, with environment variable overrides"""
    return {
        "host": os.getenv("DB_HOST", DEFAULT_DB_CONFIG["host"]),
        "port": int(os.getenv("DB_PORT", str(DEFAULT_DB_CONFIG["port"]))),
        "database": os.getenv("DB_NAME", DEFAULT_DB_CONFIG["database"]),
        "user": os.getenv("DB_USER", DEFAULT_DB_CONFIG["user"]),
        "password": os.getenv("DB_PASSWORD", DEFAULT_DB_CONFIG["password"])
    }

def get_pool_config() -> Dict[str, Any]:
    """Get connection pool configuration, with environment variable overrides"""
    db_config = get_db_config()
    return {
        "minconn": int(os.getenv("DB_MIN_CONN", str(DEFAULT_POOL_CONFIG["minconn"]))),
        "maxconn": int(os.getenv("DB_MAX_CONN", str(DEFAULT_POOL_CONFIG["maxconn"]))),
        **db_config
    }