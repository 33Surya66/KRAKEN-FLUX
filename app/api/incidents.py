from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import logging

from ..core.agent_manager import AgentManager
from ..core.database import db_manager
from ..models.database import Incident, ThreatAssessment, Evidence, Action
from ..core.logging_config import log_incident

router = APIRouter()
logger = logging.getLogger("IncidentAPI")

# Initialize agent manager
agent_manager = AgentManager()

@router.post("/incidents/", response_model=dict)
async def create_incident(incident_data: dict):
    """Create a new security incident."""
    try:
        # Log the incident
        log_incident(incident_data)
        
        # Create incident record
        with db_manager.get_session() as session:
            incident = Incident(
                incident_type=incident_data.get("type"),
                severity=incident_data.get("severity", "low"),
                status="detected",
                description=incident_data.get("description"),
                source_ip=incident_data.get("source_ip"),
                target_systems=incident_data.get("target_systems", []),
                evidence_ids=[],
                containment_status="pending",
                resolution_status="pending"
            )
            session.add(incident)
            session.commit()
            
            # Coordinate response using agents
            response = await agent_manager.coordinate_response({
                "incident_id": incident.id,
                **incident_data
            })
            
            return {
                "status": "success",
                "incident_id": incident.id,
                "response": response
            }
    except Exception as e:
        logger.error(f"Error creating incident: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/incidents/{incident_id}", response_model=dict)
async def get_incident(incident_id: str):
    """Get incident details."""
    try:
        with db_manager.get_session() as session:
            incident = session.query(Incident).filter(Incident.id == incident_id).first()
            if not incident:
                raise HTTPException(status_code=404, detail="Incident not found")
            
            # Get related data
            assessments = session.query(ThreatAssessment).filter(
                ThreatAssessment.incident_id == incident_id
            ).all()
            
            evidence = session.query(Evidence).filter(
                Evidence.incident_id == incident_id
            ).all()
            
            actions = session.query(Action).filter(
                Action.incident_id == incident_id
            ).all()
            
            return {
                "incident": incident.__dict__,
                "assessments": [a.__dict__ for a in assessments],
                "evidence": [e.__dict__ for e in evidence],
                "actions": [a.__dict__ for a in actions]
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving incident: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/incidents/", response_model=List[dict])
async def list_incidents(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """List incidents with optional filters."""
    try:
        with db_manager.get_session() as session:
            query = session.query(Incident)
            
            if status:
                query = query.filter(Incident.status == status)
            if severity:
                query = query.filter(Incident.severity == severity)
            if start_date:
                query = query.filter(Incident.timestamp >= start_date)
            if end_date:
                query = query.filter(Incident.timestamp <= end_date)
            
            incidents = query.order_by(Incident.timestamp.desc()).all()
            return [incident.__dict__ for incident in incidents]
    except Exception as e:
        logger.error(f"Error listing incidents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/incidents/{incident_id}", response_model=dict)
async def update_incident(incident_id: str, update_data: dict):
    """Update incident details."""
    try:
        with db_manager.get_session() as session:
            incident = session.query(Incident).filter(Incident.id == incident_id).first()
            if not incident:
                raise HTTPException(status_code=404, detail="Incident not found")
            
            # Update incident fields
            for key, value in update_data.items():
                if hasattr(incident, key):
                    setattr(incident, key, value)
            
            session.commit()
            
            return {
                "status": "success",
                "incident_id": incident_id,
                "updated_fields": list(update_data.keys())
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating incident: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/incidents/{incident_id}/actions", response_model=dict)
async def add_incident_action(incident_id: str, action_data: dict):
    """Add a new action to an incident."""
    try:
        with db_manager.get_session() as session:
            incident = session.query(Incident).filter(Incident.id == incident_id).first()
            if not incident:
                raise HTTPException(status_code=404, detail="Incident not found")
            
            # Create action record
            action = Action(
                incident_id=incident_id,
                action_type=action_data.get("type"),
                status="pending",
                agent_id=action_data.get("agent_id"),
                parameters=action_data.get("parameters", {}),
                result={}
            )
            session.add(action)
            session.commit()
            
            # Execute action using appropriate agent
            result = await agent_manager.execute_task({
                "type": action.action_type,
                "agent_type": action_data.get("agent_type"),
                "action_id": action.id,
                **action_data
            })
            
            # Update action with result
            action.status = "completed" if result.get("status") == "success" else "failed"
            action.result = result
            session.commit()
            
            return {
                "status": "success",
                "action_id": action.id,
                "result": result
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding incident action: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))