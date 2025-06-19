import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional
from config.settings import settings
from utils.exception import DatabaseError
from utils.logger import logger

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
            except Exception as e:
                raise DatabaseError(f"Failed to initialize database pool: {str(e)}")
    
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
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            if conn:
                cls._pool.putconn(conn)
    
    @classmethod
    @contextmanager
    def get_cursor(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    @classmethod
    def close_pool(cls) -> None:
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None
            logger.info("Database connection pool closed")