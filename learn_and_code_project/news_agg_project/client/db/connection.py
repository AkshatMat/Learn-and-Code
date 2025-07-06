import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional
from client.config.settings import settings
from client.utils.exception import ConnectionError
from client.utils.logger import logger

class DatabaseConnection:
    _pool: Optional[SimpleConnectionPool] = None
    
    @classmethod
    def initialize_pool(cls) -> None:
        if cls._pool is None:
            try:
                cls._pool = SimpleConnectionPool(
                    settings.DB_MIN_CONNECTIONS,
                    settings.DB_MAX_CONNECTIONS,
                    dbname=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    cursor_factory=RealDictCursor
                )
                logger.info(f"Database pool initialized with {settings.DB_MIN_CONNECTIONS}-{settings.DB_MAX_CONNECTIONS} connections")
                cls._ensure_tables_exist()
            except Exception as e:
                raise ConnectionError(f"Failed to initialize database pool: {str(e)}")
    
    @classmethod
    def _ensure_tables_exist(cls) -> None:
        try:
            with cls.get_cursor() as cursor:
                create_api_table_query = """
                    CREATE TABLE IF NOT EXISTS api_table (
                        api_url TEXT PRIMARY KEY,
                        status TEXT NOT NULL,
                        api_key TEXT NOT NULL,
                        name TEXT NOT NULL UNIQUE,
                        last_accessed TIMESTAMP
                    )
                """
                cursor.execute(create_api_table_query)
                logger.info("Database tables ensured to exist")
        except Exception as e:
            logger.error(f"Error ensuring tables exist: {e}")
            raise ConnectionError(f"Failed to ensure tables exist: {str(e)}")
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize_pool()
        
        conn = None
        try:
            conn = cls._pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise ConnectionError(f"Database operation failed: {str(e)}")
        finally:
            if conn:
                cls._pool.putconn(conn)
    
    @classmethod
    @contextmanager
    def get_cursor(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise ConnectionError(f"Database cursor operation failed: {str(e)}")
            finally:
                cursor.close()
    
    @classmethod
    def close_pool(cls) -> None:
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None
            logger.info("Database connection pool closed")
