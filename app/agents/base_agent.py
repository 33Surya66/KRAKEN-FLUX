from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime
import uuid

class BaseAgent(ABC):
    """Base class for all KRAKEN-FLUX agents."""
    
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid.uuid4())
        self.logger = logging.getLogger(f"{self.__class__.__name__}_{self.agent_id}")
        self.status = "initialized"
        self.last_heartbeat = datetime.utcnow()
        self.capabilities: List[str] = []
        self.metadata: Dict[str, Any] = {}
        
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the agent and its resources."""
        pass
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary function."""
        pass
    
    @abstractmethod
    async def cleanup(self) -> bool:
        """Clean up resources and prepare for shutdown."""
        pass
    
    async def heartbeat(self) -> Dict[str, Any]:
        """Update agent status and return current state."""
        self.last_heartbeat = datetime.utcnow()
        return {
            "agent_id": self.agent_id,
            "status": self.status,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "capabilities": self.capabilities
        }
    
    def register_capability(self, capability: str) -> None:
        """Register a new capability for this agent."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
            self.logger.info(f"Registered new capability: {capability}")
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update agent metadata."""
        self.metadata[key] = value
        self.logger.debug(f"Updated metadata: {key}={value}")
    
    def get_metadata(self, key: str) -> Any:
        """Get agent metadata."""
        return self.metadata.get(key)
    
    async def handle_error(self, error: Exception) -> Dict[str, Any]:
        """Handle errors during agent operation."""
        self.logger.error(f"Agent error: {str(error)}", exc_info=True)
        return {
            "error": str(error),
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        } 