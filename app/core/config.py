import os
from typing import List, Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "KRAKEN-FLUX"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Security settings
    SECRET_KEY: str = Field(
        default="development_secret_key_that_is_at_least_32_chars_long",
        min_length=32
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/kraken_flux",
        description="PostgreSQL connection string"
    )
    
    # Redis settings
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string"
    )
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Agent settings
    AGENT_HEARTBEAT_INTERVAL: int = 30  # seconds
    AGENT_CLEANUP_TIMEOUT: int = 300  # seconds
    
    # Compliance frameworks
    COMPLIANCE_FRAMEWORKS: List[str] = [
        "NIST",
        "ISO27001",
        "PCI-DSS",
        "GDPR",
        "HIPAA"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Create a global settings instance
config_manager = get_settings()