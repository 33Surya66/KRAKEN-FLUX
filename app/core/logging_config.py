import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler

from .config import config_manager

def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get log level from settings
    log_level = getattr(logging, config_manager.LOG_LEVEL)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=config_manager.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log")
        ]
    )
    
    # Configure file handler with custom formatter
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_formatter = logging.Formatter(config_manager.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Get root logger and add file handler
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified name."""
    return logging.getLogger(name)

def log_incident(incident_data: dict) -> None:
    """Log security incident details."""
    logger = get_logger("IncidentLogger")
    
    # Create incident-specific log file
    logs_dir = Path("logs/incidents")
    logs_dir.mkdir(exist_ok=True)
    
    incident_id = incident_data.get("incident_id", datetime.utcnow().strftime("%Y%m%d_%H%M%S"))
    incident_log_file = logs_dir / f"incident_{incident_id}.log"
    
    # Create incident-specific handler
    incident_handler = logging.FileHandler(incident_log_file)
    incident_handler.setFormatter(logging.Formatter(config_manager.get_setting("LOG_FORMAT")))
    incident_handler.setLevel(logging.INFO)
    
    # Add handler to logger
    logger.addHandler(incident_handler)
    
    # Log incident details
    logger.info(f"Security incident detected: {incident_id}")
    logger.info(f"Incident details: {incident_data}")
    
    # Remove handler after logging
    logger.removeHandler(incident_handler)
    incident_handler.close() 