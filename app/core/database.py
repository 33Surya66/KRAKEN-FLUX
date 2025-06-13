from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from .config import config_manager
import logging
from contextlib import contextmanager
from typing import Generator

from ..models.database import Base

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    config_manager.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database manager class
class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.Base = declarative_base()
        self._initialized = False
    
    async def initialize(self):
        """Initialize the database connection and create tables."""
        if self._initialized:
            return

        try:
            # Create database engine
            self.engine = create_engine(
                config_manager.DATABASE_URL,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10
            )

            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            # Create all tables
            self.Base.metadata.create_all(bind=self.engine)
            self._initialized = True
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            raise
    
    async def close(self):
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def get_db(self) -> Session:
        """Get database session."""
        if not self._initialized:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        
        db = self.SessionLocal()
        try:
            return db
        except Exception as e:
            db.close()
            raise e
    
    @contextmanager
    def get_session(self) -> Generator:
        """Get a database session."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
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
                logger.error(f"Error executing query: {str(e)}")
                raise
    
    def bulk_insert(self, model_class, data_list: list) -> bool:
        """Perform bulk insert operation."""
        with self.get_session() as session:
            try:
                session.bulk_insert_mappings(model_class, data_list)
                return True
            except Exception as e:
                logger.error(f"Error performing bulk insert: {str(e)}")
                return False
    
    def bulk_update(self, model_class, data_list: list) -> bool:
        """Perform bulk update operation."""
        with self.get_session() as session:
            try:
                session.bulk_update_mappings(model_class, data_list)
                return True
            except Exception as e:
                logger.error(f"Error performing bulk update: {str(e)}")
                return False
    
    def cleanup(self) -> None:
        """Clean up database resources."""
        try:
            if self.engine:
                self.engine.dispose()
            logger.info("Database connection cleaned up successfully")
        except Exception as e:
            logger.error(f"Error cleaning up database: {str(e)}")

    def init_db(self):
        """Initialize the database by creating all tables."""
        self.Base.metadata.create_all(bind=self.engine)

# Create global database manager instance
db_manager = DatabaseManager() 