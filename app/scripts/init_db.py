import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import db_manager
from app.models.database import Base
from app.core.config import config_manager

def init_database():
    """Initialize the database with required tables and initial data."""
    print("Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=db_manager.engine)
    print("Database tables created successfully.")
    
    # Add any initial data here if needed
    print("Database initialization completed.")

if __name__ == "__main__":
    init_database() 