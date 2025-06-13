from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .core.database import db_manager
from .core.logging_config import setup_logging
from .api.v1.api import api_router
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    try:
        # Startup
        logger.info("Starting up KRAKEN-FLUX application...")
        await db_manager.initialize()
        logger.info("Database initialized successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise
    finally:
        # Shutdown
        try:
            logger.info("Shutting down KRAKEN-FLUX application...")
            await db_manager.close()
            logger.info("Database connection closed successfully")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

# Create FastAPI application
app = FastAPI(
    title="KRAKEN-FLUX",
    description="Autonomous Cybersecurity Platform",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI endpoint
    redoc_url="/redoc",  # ReDoc endpoint
    openapi_url="/openapi.json",  # OpenAPI schema endpoint
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "KRAKEN-FLUX",
        "version": "1.0.0",
        "description": "Autonomous Cybersecurity Platform",
        "status": "operational",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    } 