from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Incident(Base):
    """Model for security incidents."""
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    incident_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False)
    description = Column(String)
    source_ip = Column(String)
    target_systems = Column(JSON)
    evidence_ids = Column(JSON)
    containment_status = Column(String)
    resolution_status = Column(String)
    
    # Relationships
    assessments = relationship("ThreatAssessment", back_populates="incident")
    evidence = relationship("Evidence", back_populates="incident")
    actions = relationship("Action", back_populates="incident")

class ThreatAssessment(Base):
    """Model for threat assessments."""
    __tablename__ = "threat_assessments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    threat_level = Column(String, nullable=False)
    confidence_score = Column(Float)
    attack_vector = Column(String)
    impact_analysis = Column(JSON)
    recommendations = Column(JSON)
    
    # Relationships
    incident = relationship("Incident", back_populates="assessments")

class Evidence(Base):
    """Model for forensic evidence."""
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    evidence_type = Column(String, nullable=False)
    source = Column(String)
    hash = Column(String)
    chain_of_custody = Column(JSON)
    metadata = Column(JSON)
    storage_path = Column(String)
    
    # Relationships
    incident = relationship("Incident", back_populates="evidence")

class Action(Base):
    """Model for response actions."""
    __tablename__ = "actions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String, ForeignKey("incidents.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    action_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    agent_id = Column(String)
    parameters = Column(JSON)
    result = Column(JSON)
    
    # Relationships
    incident = relationship("Incident", back_populates="actions")

class ComplianceRecord(Base):
    """Model for compliance records."""
    __tablename__ = "compliance_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    framework = Column(String, nullable=False)
    record_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    details = Column(JSON)
    notification_sent = Column(Boolean, default=False)
    notification_details = Column(JSON)

class SystemMetrics(Base):
    """Model for system performance metrics."""
    __tablename__ = "system_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    metric_type = Column(String, nullable=False)
    value = Column(Float)
    metadata = Column(JSON)

class AgentStatus(Base):
    """Model for agent status tracking."""
    __tablename__ = "agent_status"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    capabilities = Column(JSON)
    metrics = Column(JSON)
    last_heartbeat = Column(DateTime)

class SimulationResult(Base):
    """Model for simulation results."""
    __tablename__ = "simulation_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    simulation_type = Column(String, nullable=False)
    scenario = Column(JSON)
    results = Column(JSON)
    metrics = Column(JSON)
    recommendations = Column(JSON) 