import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime

from .config import config_manager

def setup_logging() -> None:
    """Configure logging for the KRAKEN-FLUX system."""
    
    # Get logging settings from config
    log_level = getattr(logging, config_manager.get_setting("LOG_LEVEL"))
    log_format = config_manager.get_setting("LOG_FORMAT")
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create formatters
    formatter = logging.Formatter(log_format)
    
    # Create handlers
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # File handler for all logs
    all_logs_file = logs_dir / "kraken_flux.log"
    file_handler = logging.handlers.RotatingFileHandler(
        all_logs_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # File handler for errors
    error_logs_file = logs_dir / "kraken_flux_error.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_logs_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    
    # Create agent-specific loggers
    agent_loggers = [
        "GuardianAgent",
        "ForensicAgent",
        "ContainmentAgent",
        "ComplianceAgent",
        "SimulationAgent",
        "AgentManager"
    ]
    
    for logger_name in agent_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        
        # Create agent-specific log file
        agent_log_file = logs_dir / f"{logger_name.lower()}.log"
        agent_handler = logging.handlers.RotatingFileHandler(
            agent_log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        agent_handler.setFormatter(formatter)
        agent_handler.setLevel(log_level)
        logger.addHandler(agent_handler)
    
    # Log system startup
    logging.info("KRAKEN-FLUX logging system initialized")
    logging.info(f"Log level: {logging.getLevelName(log_level)}")
    logging.info(f"Log directory: {logs_dir.absolute()}")

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