from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# Agent schemas
class AgentBase(BaseModel):
    """Base Pydantic model for Agent."""
    name: str
    agent_type: str
    status: str
    capabilities: Dict[str, Any]
    configuration: Dict[str, Any]

class AgentCreate(AgentBase):
    """Pydantic model for creating an Agent."""
    pass

class Agent(AgentBase):
    """Pydantic model for Agent responses."""
    id: int
    created_at: datetime
    updated_at: datetime
    last_active: Optional[datetime] = None

    class Config:
        orm_mode = True

# Evidence schemas
class EvidenceBase(BaseModel):
    """Base Pydantic model for Evidence."""
    agent_id: int
    evidence_type: str
    evidence_data: Dict[str, Any]
    severity: str
    confidence: float
    source: str

class EvidenceCreate(EvidenceBase):
    """Pydantic model for creating Evidence."""
    pass

class Evidence(EvidenceBase):
    """Pydantic model for Evidence responses."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# SystemMetrics schemas
class SystemMetricsBase(BaseModel):
    """Base Pydantic model for SystemMetrics."""
    agent_id: int
    metric_type: str
    metrics_data: Dict[str, Any]
    timestamp: datetime

class SystemMetricsCreate(SystemMetricsBase):
    """Pydantic model for creating SystemMetrics."""
    pass

class SystemMetrics(SystemMetricsBase):
    """Pydantic model for SystemMetrics responses."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 