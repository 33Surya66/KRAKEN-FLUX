from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from .core.config import config_manager
from .core.logging_config import setup_logging
from .core.database import db_manager
from .core.agent_manager import AgentManager
from .api import incidents

# Setup logging
setup_logging()
logger = logging.getLogger("KRAKEN-FLUX")

# Initialize agent manager
agent_manager = AgentManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    try:
        # Initialize database
        db_manager._initialize()
        
        # Initialize agents
        if not await agent_manager.initialize():
            raise Exception("Failed to initialize agents")
        
        logger.info("KRAKEN-FLUX system initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Shutdown
        try:
            # Clean up agents
            await agent_manager.cleanup()
            
            # Clean up database
            db_manager.cleanup()
            
            logger.info("KRAKEN-FLUX system shutdown successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

# Create FastAPI application
app = FastAPI(
    title="KRAKEN-FLUX",
    description="Kinetic Response Agent for Critical Events Network - Forensic Logic Unity eXecutor",
    version=config_manager.get_setting("VERSION"),
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(incidents.router, prefix="/api/v1", tags=["incidents"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "operational",
        "version": config_manager.get_setting("VERSION"),
        "system": "KRAKEN-FLUX"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        with db_manager.get_session() as session:
            session.execute("SELECT 1")
        
        # Check agent status
        agent_status = await agent_manager.get_agent_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": "operational",
                "agents": agent_status
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="System is not healthy"
        )

@app.get("/metrics")
async def get_metrics():
    """Get system metrics."""
    try:
        with db_manager.get_session() as session:
            # Get incident statistics
            incident_stats = session.execute("""
                SELECT 
                    COUNT(*) as total_incidents,
                    COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved_incidents,
                    COUNT(CASE WHEN severity = 'high' OR severity = 'critical' THEN 1 END) as high_severity_incidents
                FROM incidents
            """).first()
            
            # Get agent metrics
            agent_metrics = session.execute("""
                SELECT 
                    agent_type,
                    COUNT(*) as total_actions,
                    AVG(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as success_rate
                FROM actions
                GROUP BY agent_type
            """).fetchall()
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "incidents": {
                    "total": incident_stats.total_incidents,
                    "resolved": incident_stats.resolved_incidents,
                    "high_severity": incident_stats.high_severity_incidents
                },
                "agents": {
                    agent_type: {
                        "total_actions": total_actions,
                        "success_rate": success_rate
                    }
                    for agent_type, total_actions, success_rate in agent_metrics
                }
            }
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving system metrics"
        ) 