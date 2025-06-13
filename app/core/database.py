from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging
from typing import Generator

from .config import config_manager
from ..models.database import Base

class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self):
        self.logger = logging.getLogger("DatabaseManager")
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize database connection and session factory."""
        try:
            database_url = config_manager.get_setting("DATABASE_URL")
            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            
            # Create session factory
            session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            self.SessionLocal = scoped_session(session_factory)
            
            # Create tables
            Base.metadata.create_all(bind=self.engine)
            
            self.logger.info("Database connection initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self) -> Generator:
        """Get a database session."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: dict = None) -> list:
        """Execute a raw SQL query."""
        with self.get_session() as session:
            try:
                result = session.execute(query, params or {})
                return result.fetchall()
            except Exception as e:
                self.logger.error(f"Error executing query: {str(e)}")
                raise
    
    def bulk_insert(self, model_class, data_list: list) -> bool:
        """Perform bulk insert operation."""
        with self.get_session() as session:
            try:
                session.bulk_insert_mappings(model_class, data_list)
                return True
            except Exception as e:
                self.logger.error(f"Error performing bulk insert: {str(e)}")
                return False
    
    def bulk_update(self, model_class, data_list: list) -> bool:
        """Perform bulk update operation."""
        with self.get_session() as session:
            try:
                session.bulk_update_mappings(model_class, data_list)
                return True
            except Exception as e:
                self.logger.error(f"Error performing bulk update: {str(e)}")
                return False
    
    def cleanup(self) -> None:
        """Clean up database resources."""
        try:
            if self.engine:
                self.engine.dispose()
            self.logger.info("Database connection cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Error cleaning up database: {str(e)}")

# Create global database manager instance
db_manager = DatabaseManager() 