from fastapi import APIRouter, Depends
from typing import Dict
from ....core.database import get_db
from sqlalchemy.orm import Session
from ....core.config import config_manager

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """Get the current system status."""
    return {
        "status": "operational",
        "version": config_manager.VERSION,
        "environment": config_manager.ENVIRONMENT
    }

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Perform a health check of the system."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "components": {
            "database": db_status,
            "api": "healthy"
        }
    } 